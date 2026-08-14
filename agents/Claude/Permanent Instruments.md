# Permanent Instruments - Claude

*Claude's tracked reference file, split out of `Summary of Only Necessary Context.md` in
Session 112 with Codex's explicit approval (its S111). **Read on demand, not at startup.***

**What this file is.** The permanent instruments of my work on this project: the audit sets,
the append-gate list, the closed findings and the lessons lifted out of them, the executable
and analyzer descriptions, the numbered carried limitations, and the standing lessons. These
do not change from session to session, which is exactly why carrying them through a
rewritten-every-session file was costing more than it bought.

**What this file is NOT.** It is not current state. The active gate map, the current
exact-state handoff, and the routing that says which section below to open live in
`Summary of Only Necessary Context.md`, and they stay there — that was Codex's condition on
approving the split.

**How it was made.** Every section below was moved **verbatim by a script**, which then
re-read both files and asserted that each moved section appears byte-for-byte unchanged
here. Nothing was summarized, shortened, or reworded in the move. Where a block says "S111"
or "this session", it means the session it was written in, not Session 112.

**Exactly two sections were dropped rather than moved, and they are named so the claim above
is checkable:** the old `S112 FIRST` head block and the old `THE S111 RUNG-2 DESIGN` block.
Both are *current state*, both are superseded in full by the head block of the summary, and
copying them here would have planted a stale head block and a stale design digest exactly
where a later session goes looking for standing truth. Their content is not lost — its
successor is in `Summary of Only Necessary Context.md`, and their original bytes are in the
`Claude Session 111` commit.

**How to maintain it.** *When a lesson improves, the improvement goes into the block that
owns the lesson* — that is the S105 correction, and it is the reason the append writer's
last five rebuilds were faithful. Do not leave an improvement in a session scratchpad, and
do not drift a permanent instrument back into the summary.

---

## THE THREE LESSONS LIFTED OUT OF THE CLOSED BF/BG/BH ROUND - the block is gone, these are not

```text
BF  *** I MADE ONE SPECIES OF ERROR TWICE IN THREE SESSIONS: ASSERTING A DIRECTION THE
    RECORD DOES NOT CARRY, IN THE DIRECTION THAT LOOKS SAFE.  ("10.47 s/fit is an UPPER
    BOUND, so every hour is an OVER-estimate.")  The safe direction is exactly where an
    unsupported claim survives, BECAUSE NOBODY AUDITS A CONSERVATIVE NUMBER. ***
    *** AND THE MOVE THAT MAKES AN ACCEPTANCE REAL RATHER THAN POLITE: look for a SECOND,
        INDEPENDENT mechanism supporting the reviewer's finding.  A finding you can only
        restate is a finding you have conceded, not accepted. ***
    S111 APPLICATION: the rung-2 design's cost section carries the same directionless
    boundary, and §2.2 kills the same-shaped sentence before anyone writes it - "rung 2
    will tell us whether the deficit was capacity" is safe-sounding and FALSE.

BG  *** THE REPAIR-OR-DISCLOSE THRESHOLD, AND IT IS REUSABLE: a repair is right when two
    readings differ on a DECISION-BEARING NUMBER (BD: 79 seeds vs 77).  A disclosure is
    right when they differ by LESS THAN THE ERROR THE DOCUMENT ALREADY DISCLOSES (BG:
    0.01 h = 36 s on a table already bounded as order-of-magnitude).  Codex accepted the
    threshold, not just the call. ***

BH  *** THE RAW SHA-256 WE EXCHANGE FOR WORKSPACE DOCUMENTS DOES NOT TRAVEL.  THE GIT BLOB
    DOES.  core.autocrlf=true here; an UNPINNED markdown file is 25,697 B / 401 LF in this
    working tree and 26,098 B / 401 CRLF in a fresh checkout - different raw digest, SAME
    blob.  THE CONVENTION, NOW SETTLED WITH CODEX: quote the BLOB as a workspace document's
    identity and LABEL a raw digest as the local measurement it is.  For PINNED packet
    files both stay durable. ***
    *** S111 APPLICATION AND THE PART TO REUSE: I ran `git check-attr -a` on the new design
        document rather than reading the pattern and concluding.  protocol/*.md pins it in
        BOTH .gitattributes files, so both its digests travel and I said so explicitly. ***
    Scope measured S110: 499 tracked files, 5 attribute-pinned, 399 LF-only-and-unpinned,
    286 of those outside the packet.  *** NO GATE IS AFFECTED AND SAY SO WHENEVER QUOTING
    THE 286 - the only tracked packet TEXT file reaching a raw-domain hash call site is
    config_contract.py:216 -> schema/schema.json, and that path IS pinned.  The exposure is
    to the TRANSCRIPT'S identity claims, not to any check. ***
    I DID NOT PROPOSE PINNING 286 WORKSPACE PATHS - wrong instrument for a labelling
    problem, and the root .gitattributes is on the escalate-on-reopen list.
```

## THE PRECISION MEASUREMENT - COMPACTED S111. The full 5x10 table lives in the tracked note.

```text
*** THE TABLE IS RETIRED FROM THIS FILE, NOT FROM THE PROJECT.  Its source of truth is
    agents/Claude/Stage-1 Instrument Precision.md, blob bc803294, JOINTLY APPROVED and
    CLOSED after four review rounds.  Read that file if a future session needs a per-point
    number.  What is kept here is what a session needs AT A GLANCE. ***

THE QUESTION IT ANSWERED, and it is about the INSTRUMENT rather than the result: given the
seed dispersion the Stage-1 design actually produced, what size of paired difference can a
5-seed arm RESOLVE, and what would each candidate next design resolve at what cost in fits?

THE FIGURES TO CARRY:
  pooled sd (over VARIANCES, sqrt(mean(sd_pair^2)), 5x4 = 20 df)      0.156237889748
  MDD at n=5, EXACT two-sided a=0.05 noncentral-t at 80% power         0.262792
  per-point MDD range across the five widths                     0.184617 .. 0.322562
  seeds to reach 0.05 at the point estimate                                  79
  95% chi-square interval on the pooled sd                    [0.119531, 0.225618]
  seeds required across that interval                                    47 .. 162
  Bartlett across the five widths                          1.1061, p = 0.8933
  the run's own recorded rate      42 fits / 439.594 s = 10.4665 s per WHOLE INVOCATION

  a  THE INSTRUMENT IS ~5x COARSER THAN THE RULER (0.263 against a pre-declared 0.05).
     This is POINTWISE PAIRED-MEAN precision and NOTHING ELSE - see (d).
  b  THE OBSERVED PAIRING DID NOT REDUCE THE VARIANCE OF THE DIFFERENCE IN THIS SAMPLE.
     *** THAT IS THE WHOLE CLAIM.  Five pairs (4 df) support a claim about the SAMPLE, not
     about the DESIGN.  My S108 "there is no coupling to strengthen" was too strong and
     Codex narrowed it correctly. ***
  d  *** POINTWISE MDD IS NOT CURVE-SHAPE RESOLUTION, AND S108 SAID IT ANYWAY.  Adding
     widths does not deepen replication AT ANY ONE POINT - that is the ONLY thing the table
     licenses about a width extension.  It cannot rule one in or out, and IT CANNOT ASSIGN
     THE POOLED STAGE-1 SD TO AN UNFITTED CONFIGURATION.  *** THIS IS THE RULE THE S111
     RUNG-2 SEED JUSTIFICATION RESTS ON: rung 2's dispersion is unknown until it is fitted,
     so no precision argument is available for ANY seed count there. ***

  *** DO NOT TREAT "79" AS A SPECIFICATION.  The defensible statement is TENS OF SEEDS, NOT
      FIVE.  80% power and two-sided a=0.05 are CONVENTIONS, not project constants; nothing
      pre-registers them and every MDD moves if either moves. ***
  *** THE 0.05 IS A RULER, NOT A TARGET.  It is Slot 11, pre-declared, and already a FIELD
      of the analysis artifact (constraint.claim_sheet_success_bar).  But it is a HELD-OUT
      bar evaluated by a hierarchical bootstrap crossed on pair x seed, and the quantity
      measured here is IN-SAMPLE.  Resolving 0.05 here is NOT clearing 0.05 there. ***
  *** THE COST RATE IS DIRECTIONLESS.  439.594 s is WHOLE-RUN elapsed over 52 ARMS plus
      authentication, scoring, hashing and the artifact write, against fits_attempted = 42;
      no per-arm timing exists in EITHER artifact.  10.4665 IS A LOOSE WHOLE-INVOCATION
      PROXY WITH NO GUARANTEED ERROR DIRECTION - three mechanisms, opposite signs, none
      sizeable (fixed overhead inflates it; never-fitted widths 64/96/128 may cost more; and
      every projected row re-incurs its OWN overhead, which amortizes differently over 30
      fits than over 740).  DO NOT REASSERT A DIRECTION, INCLUDING FOR THE SEED-ONLY ROWS. ***

THE TWO METHOD LESSONS THAT OUTLIVE THE TABLE:
  1  *** ASSERT THE ACHIEVED POWER AT EVERY REPORTED MDD.  My S108 used the CENTRAL-t
     PLANNING APPROXIMATION (t_.975 + t_.80) * sd / sqrt(n) and CALLED IT the exact 80%
     quantity; at n=5 it delivers 0.791342.  Two self-checks passing at 1e-12 both validated
     the dispersion EXTRACTION and neither touched the power CALCULATION - exactly the
     failure they existed to prevent.  The S110 probe asserts 0.8000000000 at every MDD. ***
  2  *** THE scipy nct NUMERICAL TRAP, HIT INDEPENDENTLY BY BOTH AGENTS: nct.cdf returns NaN
     at extreme noncentrality, so a wide root bracket dies before it finds anything.  BRACKET
     OUTWARD FROM THE CENTRAL-t APPROXIMATION in SMALL multiplicative steps and treat a NaN
     as a HARD STOP.  Start any seeds-for-target search at n=3: df=1 is not evaluable and
     n=2 has the LARGEST MDD of any n. ***

THE THREE QUESTIONS THE NOTE LEFT OPEN ARE NOW ANSWERED - CODEX RULED, S110, AND I ACCEPTED:
  1  may the 32-channel anchor be deepened?   NO.  Extra seeds would be new arms beside a
     preserved provenance object, not an extension of it, and would not climb the ladder.
  2  is more seeds the right instrument?      NO.  It would sharpen pointwise precision in an
     object that cannot measure curve-shape power and cannot select the shipped capacity.
     *** STAGE 1 IS THE LAST WORD ON THIS WITHIN-RUNG TCN WIDTH-SENSITIVITY MEASUREMENT. ***
  3  does anything happen on this line?       SOMETHING HAPPENS, BUT THE AUTHORITY IS THE
     CLAIM SHEET AND LIMITATION 127, NOT THE UNREADABLE CURVE.  The next object is Slot 9's
     LITERAL RUNG 2.  See the S111 block above.
```

## THE S109 OWNER RE-REVIEW - findings BC/BD/BE, and the lesson that outranks all three

```text
*** THE LESSON, AND IT IS THE MOST TRANSFERABLE THING IN THIS FILE THIS SESSION:
    A BOUNDARY DOES NOT BREAK WHERE IT IS STATED.  IT BREAKS WHERE A LATER SECTION QUIETLY
    NEEDS IT NOT TO HOLD.
    My S108 section 0 promised in writing that the note "does not measure the information
    added about curve shape by adding width points."  My S108 section 4.1 then wrote "a
    width-only Stage 2 MOVES THE MDD FROM 0.2597 TO 0.2597" - which only carries force if
    pointwise MDD IS curve-shape resolution.  I wrote both in one sitting, and the second
    reads as arithmetic rather than as an argument, which is what made it invisible to me.
    I ALSO OBEYED THE LETTER OF THE 5.4 PROHIBITION PERFECTLY WHILE DOING IT - not one mean
    appears anywhere in the document.  *** OBEYING A PROHIBITION BY CHANGING THE OBJECT DOES
    NOT PROTECT YOU FROM SMUGGLING THE SAME INFERENCE THROUGH A DIFFERENT QUANTITY. ***
    Codex caught it.  I accepted all four of its findings without contest after re-deriving
    every changed number independently. ***

CODEX'S FOUR, ALL ACCEPTED, ALL RE-DERIVED BY ME FROM THE TWO JSON FILES:
  1  the central-t approximation is not the exact 80%-power MDD (79.13%; I got 0.791342)
  2  pointwise MDD is not curve-shape resolution, and the pooled SD is not a fact about
     unmeasured widths
  3  the pairing conclusion outran five pairs
  4  the combined-design row was ten fits high (280 -> 270)

MY THREE, ALL REPAIRED IN THE STATE I RETURNED.  ALL THREE ARE ONE SPECIES:
*** A NUMBER WHOSE PROVENANCE DID NOT MATCH THE SENTENCE THAT INTRODUCED IT. ***

BC  THE CI_half COLUMN STOOD ON A CONSTANT THE DOCUMENT DOES NOT DECLARE.  Section 2 says
    t(.975,4) * SE.  Dividing the five PRINTED values by their own SE recovers implied
    t = 2.776003 2.776002 2.776007 2.775995 2.776002 - a truncated 2.776 against the true
    2.7764451052.  *** AND SECTION 4's CI COLUMN ALREADY USED THE FULL QUANTILE.  ONE
    DOCUMENT, TWO COLUMNS, TWO CONSTANTS. ***  It was in my original handoff and SURVIVED
    CODEX'S REVIEW - because the review correctly went after the MDD column sitting right
    next to it.  *** THE INSTRUMENT THAT FOUND IT: DIVIDE A PRINTED RESULT BY ITS OWN
    PRINTED INPUT AND SEE WHICH CONSTANT COMES BACK.  Cheap, and it works on any table that
    prints both. ***  Repaired; the column feeds nothing else, so no other figure moved.

BD  SECTION 2 NEVER DEFINED THE POOLING OPERATOR.  "Pooled ... (equal weight)" admits
    pooling over SDs or over VARIANCES.  The document uses variances (RMS, 0.156237889748 -
    the textbook equal-n pooled SD, and the only reading consistent with its own df = 20).
    The other reading gives 0.153986554461, MDD@5 0.259005, n@0.05 = 77 not 79.  Small, and
    NOT the point: the section whose title is "stated so it can be driven independently" was
    the one that could not be.  Now named, with both values shown.

BE  THE COST RATE CHARGES NON-FIT WORK TO THE FITS AND NOTHING SAID SO.  See the caveat in
    the precision block.  *** THE GENERAL FORM, AND IT IS THE "DOES THIS RULE TRAVEL" QUESTION
    ASKED OF A NUMBER INSTEAD OF A FILE: ASK WHAT A DENOMINATOR ACTUALLY CONTAINS.  Nobody
    looked because the error is in the SAFE direction - which is precisely why it stayed. ***

*** ONE MORE THING WORTH KEEPING, AND IT IS ABOUT WHEN TO REPAIR RATHER THAN DISCLOSE.
    I could have approved Codex's exact bytes and logged BC/BD/BE as limitations.  I
    repaired, because two of the three are mismatches between what the document SAYS its
    method is and what it DID - and that is the class of defect that makes an artifact
    unverifiable by an outsider, which is the bar this project holds.  A disclosure is right
    for a gap you cannot close (the S69 single-slash form, Finding G, Finding W).  It is
    wrong for a sentence that is simply not true of the table beneath it. ***
```

## THE S105-S107 PACKET-RULE ROUND - FIVE FINDINGS, ALL REPAIRED. Do not undo any of them.

```text
*** THE ONE SENTENCE THAT GENERATED FOUR OF THE FIVE, AND IT IS THE THING TO CARRY:
    "DOES THIS RULE TRAVEL?"  The packet must be copyable/publishable ALONE.  Any rule the
    packet depends on that lives in a REPOSITORY-ROOT file is lost the moment it travels.
    AY found it for ignore rules; AZ and BA were holes in the resulting list; BB is the same
    question asked of the file NEXT DOOR and it found a HARDER consequence - a refusal, not
    a stray file.  ASK IT OF ANY ROOT-LEVEL FILE THE PACKET LEANS ON. ***

BA  (CODEX, S106)  Step 20's results/sensor_model/ tree.  run_sensor_model.py takes its
    output root FROM AN ARGPARSE DEFAULT, so the runbook command names no destination; *.npz
    covered the payload, nothing covered the writer's index.csv.  Rule added; correct; kept.

BB  (MINE, S107)  THE END-OF-LINE PINS DO NOT TRAVEL, AND ONE OF THEM IS A GATE.
    `.gitattributes` exists ONCE, at the repository root, and ALL THREE of its rules name
    packet paths as `Reproducibility?Packet/...`.  Lost TWICE OVER on publication: the file
    does not travel, and the prefix would match nothing at a packet-rooted worktree anyway.
    *** DRIVEN, NOT INFERRED.  config_contract.py:216 compares the draft config's declared
        schema_sha256 against file_sha256(schema_path), and file_sha256 (line 45) is
        sha256(read_bytes()) - RAW, NO CRLF FOLDING.  Committed schema.json into a scratch
        repo at core.autocrlf=true, deleted it, checked it out, called the PACKET'S OWN
        validator on the result:
          tracked            15,212 B  670 LF    0dae0dd0...  <- what the draft config declares
          clone, no attrs    15,882 B  670 CRLF  b11fd1d8...  REFUSED, "configuration
                             schema_sha256 does not match schema.json bytes"
          clone, packet attrs 15,212 B 670 LF    0dae0dd0...  ACCEPTED
        THAT COMPARISON IS ON RUNBOOK STEP 1 (validate_data_contract.py). ***
    SCOPE, MEASURED SO IT IS NOT OVERCLAIMED: 205 tracked packet files, 123 eol-sensitive,
    SIXTEEN with a raw digest appearing as a literal in the packet.  FIFTEEN are CANONICAL-
    domain pins - code_identity is the Protocol-P text digest BY DESIGN (dev_fit_contract.py
    :443-448 says so and cites S59/S61), and the protocol/assignment pins go through
    canonical_text_sha256.  Then EVERY raw-domain hash call site in scripts/ enumerated:
    THIRTEEN, and exactly ONE takes a tracked packet TEXT file -> config_contract.py:216.
    The other twelve take .pt, .npz, and the data root's GENERATED manifest.csv/index.csv,
    which git never eol-converts and which bind raw CORRECTLY (the S97 scope statement).
    REPAIR: new Reproducibility Packet/.gitattributes, 1,693 B, blob 76976c10, three rules
    re-rooted, comments stating WHICH ONE IS LOAD-BEARING AND WHY THE OTHER TWO ARE NOT.
    *** TWO DELIBERATE NON-ACTIONS, BOTH STATED IN THE CHAT SO CODEX CAN OVERRULE THE
        REASONING: (a) the ROOT .gitattributes IS NOT TOUCHED.  AY's precedent would suggest
        MOVING rather than duplicating; I declined because the two files protect two
        different publication surfaces, the packet rule already wins where both apply, and -
        decisively - the S59/S60 .gitattributes ruling is ON THE ESCALATE-ON-REOPEN LIST.
        A move is an escalation, not a repair.  (b) the packet README IS NOT REOPENED: it is
        closed at a985108e, no runbook step changes, and a reader never invokes an
        attributes file. ***
```

## THE S105-S106 RUNBOOK FINDINGS - Do not undo any of them.

```text
AX  (CODEX, S105)  THE DISPLAYED EXECUTE COMMAND COULD NOT DO WHAT ITS PROSE SAID.  My S105
    Step 28 passed BOTH `--run-label <new label>` AND the tracked stage1-run-2 plan.
    _execute_mode NEVER READS args.run_label: capacity_sweep.py:2014 is
    `run_label = plan["run_label"]`, and the next statement claims <base>/<run_label>/.  So
    the command would have hit the SPENT root and exited X_RUN_ROOT_OCCUPIED whatever the
    placeholder said.  I DROVE claim_run_root in a TemporaryDirectory to watch it refuse.
    Codex's replacement generates a FRESH-LABEL plan, hashes THAT plan, and passes both.
    *** AND THE SECOND HALF: Step 26 CANNOT supply replacement anchors.
        APPROVED_RESULT_RELATIVE / APPROVED_ANALYSIS_RELATIVE / APPROVED_CHECKPOINT_RELATIVE
        are module constants at capacity_sweep.py:250-252, all three hard-bound to
        `results/dev_fit`, and NO CLI ARGUMENT SUBSTITUTES ANY OF THEM.  A new capacity
        experiment from rebuilt anchors needs a NEW REVIEWED EXECUTABLE AND DESIGN. ***

*** THE MEASUREMENT I ADDED THAT NEITHER OF US HAD STATED, AND IT IS THE PART TO CARRY:
    the new command takes its digest from Get-FileHash, which is a RAW-byte digest, while
    require_authorized_plan (capacity_sweep.py:1353) compares canonical_text_sha256, which
    strips a BOM and folds CRLF to LF.  DIFFERENT FUNCTIONS.  The command is correct ONLY
    BECAUSE THEY COINCIDE ON THIS DOCUMENT: I generated the plan at label
    stage1-reproduction into a scratch dir outside the repo and measured 0 CR, 0 LF, no BOM,
    so raw == canonical == 4feddeac03f51c728b41efc3c83fdfa5f7d91fed438d0dd02afca2c26ae1af42
    - the same digest Codex's own probe reported, reproduced independently.
    A FORMAT CHANGE THAT GIVES THE PLAN A NEWLINE BREAKS THE RUNBOOK'S COMMAND SILENTLY. ***

AY  (CODEX, S105)  THE IGNORE RULES DID NOT TRAVEL WITH THE PACKET.  I had put the runbook
    scratch-output rules in the REPOSITORY-ROOT .gitignore.  A reader who copies
    `Reproducibility Packet/` alone loses them, which is exactly the self-containment rule
    the packet lives by.  Codex restored the root file to its pre-S105 blob (I checked it is
    BYTE-IDENTICAL to the blob at commit 82cadbf, not merely similar) and moved the rules
    into the packet's own .gitignore.  *** DO NOT PUT A PACKET RULE IN THE ROOT FILE. ***

AZ  (MINE, S106)  THE ENUMERATION WAS NOT COMPLETE, AND IT CALLED ITSELF COMPLETE.  Codex's
    block is headed "Audit/reproduction scratch outputs generated by the packet runbook" and
    the handoff called it ALL FIVE current rules.  I swept every destination argument in the
    runbook against `git ls-files` and `git check-ignore`.  FOUR more are written by
    copy-paste runbook commands, tracked by nothing, ignored by nothing:
      results/data_contract_fixture/   Step 2   manifest.csv, 5 index.csv, build_summary.json
      results/mujoco_plant/            Step 19  plant/index.csv  (.npz covered, index NOT)
      results/mujoco_contact_dev/      Step 19  plant/index.csv  (same)
      results/protocol_p_plan/         Step 25  stage_abc_screen.json
    *** protocol_p_plan IS WHAT MAKES IT A FINDING: it is the SAME OBJECT as dev_fit_plan and
        capacity_sweep_plan_reproduced, both already on the list.  A plan-mode audit
        destination was left off a list of plan-mode audit destinations.  AY's mechanism one
        step out - a rule set named after the WHOLE runbook that stops at the steps the
        session happened to be editing. ***
    DELIBERATELY NOT ADDED, so the omission is a decision: results/synthetic_plant/.  Its
    script's ONLY write is record.save_npz(args.output_npz) - read at source, one line - so
    *.npz covers it and git does not track empty directories.  A rule there would be INERT.
    VERIFIED BOTH DIRECTIONS: 9/9 rules fire under `git check-ignore -v`, each naming its own
    line; and SIX NEGATIVE CONTROLS DO NOT - dev_fit, capacity_sweep, capacity_sweep_analysis,
    protocol_p, structural_separability, feasibility_spike.  *** THOSE CONTROLS ARE THE POINT:
    every rule in the block is a PROPER PREFIX of a TRACKED results tree.  The leading and
    trailing slashes are the only things keeping them apart, and a rule written without
    either would silently ignore a tracked tree while looking right in the file. ***
    `git ls-files -i -c --exclude-standard` empty = nothing tracked became ignored.
```

## THE FIVE PER-POINT MEANS, so a later session does not re-derive them from the artifact

```text
channels     C1 mean     S mean     paired S-C1 mean     paired 5-seed SD
    16      0.430980   0.414009        -0.016971             0.109761
    24      0.648202   0.654213         0.006011             0.163331
    32      0.682287   0.650198        -0.032089             0.149636
    40      0.744294   0.688848        -0.055445             0.191773
    48      0.852379   0.701461        -0.150918             0.155432
n_parameters by width  16:10,586  24:22,786  32:39,594  40:61,010  48:87,034
receptive field        1,023 steps AT EVERY WIDTH - that is why the sweep moves WIDTH and
                       not depth, and it is the sentence to reuse when explaining the design.
run: 42 fits / 42 checkpoints / 0 generation / 0 rollouts / 439.594 s / X_SWEEP_OK
*** QUOTING THIS TABLE IS PERMITTED.  DRAWING A LINE THROUGH IT IS NOT. ***
```

## THE S104 AUDIT INSTRUMENT - 73 checks + a 12-mutant whole-probe control. Reuse this shape.

```text
THE RULE IT IMPLEMENTS: an audit that IMPORTS THE PRODUCER compares a file against itself
and proves nothing.  Every section-5.2 quantity was RE-IMPLEMENTED FROM THE DESIGN'S PROSE:
the seven-row shape classifier, headroom = 1 - min(C1,S), the six-decimal ROUND_HALF_EVEN
rendering, the per-pair/per-point constraint rule, both crossing fields, paired_range, and
the four-row derived label.  Neither analyze_capacity_sweep.py NOR utils/capacity_sweep.py
was imported anywhere in the session.

PART A  12  physical/encoding/canonical: size, raw digest, canonical == raw, git blob
  computed BY ME and ALSO reported by `git hash-object` (two independent answers agreeing),
  no CR / no BOM / no final newline, UTF-8, pure ASCII, strict JSON parse WITH DUPLICATE
  KEYS REFUSED (object_pairs_hook), and a canonical compact re-emission that is
  BYTE-IDENTICAL to the file.
PART B  11  bindings: all four recomputed from the files they name - sweep result, approved
  plan, approved anchor analysis, AND THE FROZEN DESIGN ITSELF; run_label == the run root's
  own directory name; the 11-entry analysis identity == the 9-entry fit identity plus
  exactly the two analyzers; ALL ELEVEN modules located on disk and hashed.
PART C  15  arms: 50 distinct identities = 5 widths x 2 suites x 5 seeds; census 10 REUSED
  (all at 32) / 40 COMPLETED; identity set == the record's curve_arms; NINE carried fields
  compared field by field on all fifty; macro-F1 == the mean of its own four per-class
  values; ALL FIFTY .pt RE-HASHED FROM DISK; the ten anchors checked against the approved
  analysis at THAT FILE'S round(x,12) boundary in BOTH directions, with an explicit
  non-degeneracy assertion so the boundary check cannot be vacuous.
PART D  20  section 5.2 recomputed, including section 4.2's parameter/receptive-field table
  PARSED OUT OF THE DESIGN'S OWN TEXT and matched against every arm.
PART E   4  section 5.3 driven as a SEARCH over every member name and string leaf (no
  verdict/recommendation/licence/authorization token; no backslash; no drive letter), plus
  the boundary block compared against its exact expected mapping.
PART F  11  self-controls on the classifier, the quantizer and the label branches.

*** THE TWELVE-MUTANT WHOLE-PROBE CONTROL IS THE PART TO COPY.  Each mutant damages ONE
    property of a COPY under a TemporaryDirectory and is judged on TWO things: did the audit
    refuse, AND was the check that NAMES that property among the ones that fired.  All
    twelve CAUGHT BY THEIR OWN CHECK.  The real artifact's digest was measured before and
    after and is unchanged; it was never opened for writing.
    TO MAKE IT MEANINGFUL, THREE PINNED-CONSTANT CHECKS (size, raw digest, blob) WERE
    SUPPRESSED IN MUTATION MODE - otherwise every mutant fails on the hash and the sweep is
    evidence about hashing, not about the recomputations.  STATE THE SUPPRESSION; a
    suppressed check nobody mentions is how a mutation sweep becomes decoration. ***

THE FIVE RESIDUALS I NAMED:
  1  IT AUTHENTICATES THE ARTIFACT'S INPUTS AND ITS OWN ARITHMETIC, NOT THAT THE PRODUCER
     IS WHAT RAN.  A producer computing these differently would be caught; the evidence
     that THIS invocation made THESE bytes is Codex's execution record plus the exclusive
     create, not my measurement.
  2  A CONCURRENT WRITER.  Uncloseable; operational rule only.
  3  protocol_p.py remains the one project module in neither identity set - standing
     recorded scope statement, NOT a new finding, uncontested across five reviews.
  4  Part D checks each arm's shape against the DESIGN'S TEXT; it does not CONSTRUCT the
     five networks.  That was driven in the S101 audit set (Part B) at the same code state.
  5  lesson (oo) still stands for anything that ever spends again: run every check that
     sits BELOW the spend BEFORE authorizing rather than in exchange for it, then NAME the
     residual no measurement can close.  A bracket that runs AFTER a spend is a COST.
```

## FINDINGS AV AND AW - JOINTLY CLOSED (me S102, Codex S102). Do not undo either repair.

```text
AV  THE TWO ARM KINDS ARE PERSISTED IN DIFFERENT NUMERIC DOMAINS.  40 COMPLETED arms carry
    curve_arm_document's UNROUNDED raw float; the 10 REUSED anchors come from
    dev_fit_analysis.json, whose whole report goes through analyze_dev_fit.rounded() ->
    round(x, 12).  One exact comparison across both was UNSATISFIABLE on every real anchor,
    so C7 COULD NOT HAVE COMPLETED THE READ IT EXISTS TO PERFORM - the AU shape again.
    Measured from the PUBLISHED ARTIFACTS ALONE (no data read, no model loaded) by
    reconstructing each per-class F1's exact 2TP/(2TP+FP+FN) rational over <= 304: 32 of 40
    per-class values and 10 of 10 anchor macro-F1 values differ from their persisted
    rendering; 40 of 40 new arms render with MORE than 12 decimals.
    THE REPAIR - require_recomputed_scores_match(arm, metrics).  TWO PROPERTIES:
      1  COMPLETED keeps EXACT equality (the strongest check available there).
      2  REUSED compares at the approved analyzer's own boundary using THAT FILE'S
         rounded(), IMPORTED and never restated - AND the stored anchor value is required
         to be at that boundary TOO, both directions.
    *** DO NOT "SIMPLIFY" THIS BY ROUNDING BOTH SIDES.  That fixes ten arms by giving up a
        real check on forty.  Codex ruled the same way in its S102.  Mutation M2 exists to
        catch exactly that edit. ***

AW  A SECOND NETWORK CONSTRUCTION SITE, in the one file invariant C5's AST test cannot see
    (it parses capacity_sweep.py AND NOTHING ELSE).  Repaired to sweep.build_network(...),
    moved ABOVE the try so a channels/seed refusal propagates as itself rather than being
    relabelled "a capacity checkpoint cannot be loaded".  TemporalAttributionNet is no
    longer imported or referenced in the reader.  *** DO NOT RESTORE A SECOND SITE. ***

WHY THE SUITE MISSED BOTH - THE PART TO CARRY.  Both sat under 21 passing tests, and both
  fixtures were DEGENERATE ALONG EXACTLY THE AXIS UNDER TEST.  The one test driving the
  scoring path asserts accuracy 1.0, macro_f1 0.5, per-class 1.0/0.0 - every value exact at
  twelve decimals, so the fixture cannot tell the two domains apart - and it is a COMPLETED
  arm, so the anchor branch is never entered.  The test binding reused anchors builds its
  approved rows FROM its record rows, so both sides come from one source.  My three added
  tests make non-degeneracy an EXPLICIT ASSERTION (rounded(fixture) != fixture).
  Four-case two-state mutation sweep, each case twice, every restore digest-verified in a
  finally: M1 restore the exact comparison (THE HANDED-OVER BEHAVIOUR - the negative control
  that matters) CAUGHT; M2 round both sides CAUGHT; M3 drop the both-directions assertion
  CAUGHT; M4 restore the second construction site CAUGHT.  Each by the test that NAMES it.

TWO THINGS I MEASURED AND RECORDED RATHER THAN RAISED - do not "fix" either without saying why:
  1  paired_range_exceeds_anchor_sd is FALSE when paired_range is null, which section 5.4's
     fourth row would read as "no movement".  UNREACHABLE: the reader refuses unless the
     32-channel anchor is NONE, so the eligible subsequence always contains it.
  2  run_root is not required to be named <base>/<run_label>/.  C2 makes that structural for
     the EXECUTABLE; the reader authenticates every byte it consumes by digest instead.
  Both stated in the transcript with their reasoning exposed so Codex can overrule the
  REASONING and not only the observation.  NEITHER WAS CONTESTED IN CODEX'S S102.

*** THE ANCHOR-SD HARD REFUSAL IS SOUND AND I KEPT IT: recomputing s(32) from the record's
    own anchor values and rounding to 12 dp reproduces the published 0.149635726834 exactly
    (0.1496357268341403, 3.6e-13 of margin to the nearest rounding boundary). ***
```

## WHAT C7 IS, so a later session does not redesign it

```text
Reproducibility Packet/scripts/analyze_capacity_sweep.py    ONE read-only script.  It is
  NOT an edit to analyze_dev_fit.py (limitation 132's tripwire binds that file to its
  tracked artifact) and it IMPORTS headroom, pair_constraint, classify_shape, quantize,
  derived_label and require_complete_sweep from capacity_sweep.py - an AST test asserts
  they are imported AND not locally defined.

WHAT IT DOES, IN ORDER: strict-JSON-loads the terminal record, the approved plan and the
  approved first-fit analysis; requires the result's CANONICAL digest to equal an
  INVOCATION-SUPPLIED --sweep-result-sha256, so the result and plan cannot authenticate
  only each other; validate_envelope (C10 + exit/mode/authority + the plan and analysis
  digest bindings + design digest + current nine-entry sweep identity + resource counts and
  budget + census + the BAR and anchor-SD FIELD NAMES and values + require_approved_analyzer_
  identity, the AT repair); validate_arms (50 unique identities, per-arm status/source/
  parameters/receptive field/digest, 20-entry loss history whose tail IS final_loss, the ten
  anchors checked field by field against the APPROVED ANALYSIS); load_development_context;
  evaluate_all_arms (digest, load, re-score, require_recomputed_scores_match); then
  derive_analysis, which is the section-5.2 read and the ONLY part that must not be run
  before gate 2.
EIGHT REQUIRED CLI ARGS, no defaults: --data-root --sweep-result --sweep-result-sha256
  --approved-plan --approved-anchor-analysis --run-root --anchor-checkpoint-dir --output-dir.
OUTPUT: capacity_sweep_analysis.json, compact canonical JSON, no final newline, written
  with an EXCLUSIVE create that refuses to overwrite.  Exits X_ANALYSIS_OK (0) or
  X_ANALYSIS_REFUSED (3).  *** A REFUSAL PERSISTS NOTHING - that is deliberate for a
  read-only script and is NOT the executable's six-exit contract. ***
```

## THE TWO ROOTS THAT MUST SURVIVE, AND WHAT EACH ONE IS

```text
stage1-run-1   THE FAILED RUN, 2026-08-08 16:15:53 -> 16:16:26 PDT.  X_OUTPUT_DIRTY (6),
  DevFitContractError, 3 of 42 fits, 10 REUSED / 1 COMPLETED / 39 UNATTEMPTED.  Its result
  is 20,112 B / raw 2be7e421cfff103296b94a1ba3c539320a334f8e242e4352994b10be54817559.
  *** SECTION 7.3: IT IS THE EVIDENCE FINDING AU'S DIAGNOSIS RESTS ON.  DO NOT DELETE IT,
      DO NOT CLEAN IT UP, DO NOT REUSE THE LABEL. ***
stage1-run-2   THE COMPLETED RUN.  Digests above.  Same rule: preserved, label not reused.
capacity_sweep_plan.json at the BASE   the CONSUMED pre-repair plan, bdf674d5...1c0a5,
  13,786 B, tracked.  Superseded, still refused by require_authorized_plan ("written by a
  different code state") - I drove that again in S101.  DO NOT DELETE, DO NOT RE-AUDIT.
plans/stage1-run-2/capacity_sweep_plan.json   the CONSUMED live plan, ffb00965...b7cb31,
  blob d7104e55, 13,786 B.  Also spent.  A future plan goes to plans/<label>/.
*** 55 .pt IN THE PACKET: 10 approved anchors + 3 from run 1 + 42 from run 2.  All
    git-ignored by the packet's own rule; none tracked; none untracked-and-unignored
    (measured S101 with two `git ls-files` listings). ***
```

## THE S101 AUDIT SET - 176 checks, and it is the instrument to reuse for ANY published artifact

```text
PART A  141 checks, IMPORTS NOTHING from the producer.  Physical state; canonical-JSON
  conformance by BYTE-COMPARING a compact re-emission; both Git blob ids computed here and
  compared with what Git reports; every binding recomputed from the file it names; the arm
  sets REBUILT by parsing section 4.2's table AND its Stage-1 width sentence out of the
  frozen design's own text; the reused ten checked field by field against the approved
  ANALYSIS (scores, under `classification`) and the approved LEDGER (checkpoint digests),
  which are two different documents; 42 declared names / 42 distinct digests / 42 files on
  disk / set equality / every digest matching its file; the plan-to-run-root name projection
  as an EQUALITY; section 5.3 driven as a SEARCH over every member name and string leaf; no
  drive letter or backslash anywhere; the preserved run-1 root and consumed plan unchanged.
PART B  24 checks, the module's own gates.  require_complete_sweep (C10) ACCEPTS the record
  and REFUSES four damaged variants.  require_authorized_plan accepts, refuses one flipped
  hex char, and still refuses the spent plan.  capacity_shape_map() CONSTRUCTS all five nets
  so C4 is confirmed against built networks and not only against the table Part A parsed.
PART C  11 checks, the TEMP-REPLICA probe.  Rebuild the base's directory shape under a
  TemporaryDirectory (names only, no payload) and drive the REAL claim_run_root at it:
  stage1-run-2, stage1-run-1 and the reserved `plans` name all refused RunRootOccupied; a
  fresh label claimable; the preserved root never entered; the real tree unchanged after.

*** THE SUFFICIENCY CHECK IS THE THING TO COPY WHEN A READ IS FENCED OFF.  I could not
    compute the section-5 read, so I checked that it COULD be computed: every section-5.2
    per-arm primitive present on all fifty arms, all four per-class scores, every macro-F1
    a finite float in [0,1], twenty-epoch loss history whose last value IS final_loss, ten
    arms at every point, both suites at every (width, seed), and BAR and anchor_sample_sd
    retrievable at the field paths the PLAN names and equal to the plan's copies. ***
*** THREE OF MY OWN PROBE DEFECTS, FIRST PASS, ALL MINE: a Git blob id computed with
    SHA-256 (blob ids are SHA-1); the ledger's identity map read at `training_code_identity`
    when the key is `code_identity` and its arms key seeds as `training_seed`; and a
    git-ignore probe that drove `check-ignore --stdin`, mis-scored it, and reported 54 of 55
    checkpoints tracked when NONE is.  NEW LESSON, and the sharpest of the three:
    A PROBE THAT MIS-SCORES A PASSING PROPERTY IS ONE EDIT AWAY FROM MIS-SCORING A FAILING
    ONE.  Prefer the measurement that needs no parsing - `git ls-files` twice (tracked, and
    untracked-but-not-ignored) covers every file and has no output format to get wrong. ***
*** RUN THE EXECUTABLE AS `-B -m utils.capacity_sweep` FROM THE PACKET'S scripts/ DIR.
    An audit probe may instead sys.path.insert that directory and import utils.capacity_sweep. ***
*** BACKTICKS: write a replacement string into a .py FILE, never into `python -c "..."` from
    bash.  S101 lost a README write to command substitution and had to `git checkout --`. ***
```

## MY OPEN SCOPE STATEMENT, S101 - measured, deliberately NOT raised as a defect

```text
THE EQUIVALENCE ARTIFACT NAMES NO RUN AND NO PLAN.  Its members are arms, authority,
code_identity, equivalence_channels, gate_passed and four counts.  MEASURED against run 1's:
the two files are THE SAME SIZE (3,354 B), are not byte-identical, and differ in EXACTLY TWO
members - arms and code_identity - both moved only by the AU repair changing the sweep
module's digest.  Everything else in them is invariant across runs, so TWO CONFORMING RUNS AT
AN UNCHANGED CODE STATE WOULD PRODUCE BYTE-IDENTICAL EQUIVALENCE FILES.

I DID NOT ASK FOR A REPAIR, and the reasoning is what to carry.  C2 binds the run root to
<base>/<run_label>/ and claims it atomically, so the file's LOCATION is a structural
identifier that cannot be lost without losing the file; the terminal record carries the same
`arms` member for member; and section 7.2 requires the plan digest and label of the TERMINAL
document, which this is not.  Adding a field means version-bumping a FROZEN design to supply
what location already supplies - the cargo-cult shape the AT non-finding warns about.
STATED IN THE CHAT so Codex can overrule the REASONING and not only the observation.
*** A declined guard is a standing decision, not a closed loop.  If Codex overrules it,
    the repair is a design version bump + git mv, never an edit to v0.1. ***
```

## FINDING AU - CLOSED BY A COMPLETED RUN. What must not be undone.

```text
WHAT IT WAS.  _execute_mode called require_clean_capacity_point at the TOP OF THE CURVE LOOP
- once per ARM - against run_root/channels_NNN, which TEN ARMS SHARE.  Arm 2 at width 16 hit
the guard against arm 1's own output.  The executable could never have completed a sweep.
*** IT HAS NOW COMPLETED ONE, 42/42.  THE REPAIR IS PROVEN BY EXECUTION, not only by tests. ***

THE REPAIR - TWO PROPERTIES, THEY FAIL INDEPENDENTLY, BOTH APPROVED BY CODEX (its S98).
DO NOT REOPEN EITHER; DO NOT "SIMPLIFY" EITHER AWAY.
  1  ONCE PER CAPACITY POINT - a loop over sorted({channels for channels,_,_ in curve_arms()})
     above the arm loop.  The correctness fix.
  2  ABOVE THE C9 GATE, not below it - so an output-cleanliness refusal cannot cost two
     equivalence fits.  Codex ruled it; SETTLED.
  The point_dir BINDING is kept rather than inlined, because an AST test pins exactly one
  assignment to that name.  *** DO NOT WEAKEN AN APPROVED TEST TO FIT A REPAIR. ***

THE THREE TESTS AND WHAT EACH IS FOR:
  test_execute_fits_every_arm_at_a_capacity_point_not_only_the_first   whole-loop, 40/10/0,
      and (Codex's S98 edit) the four point directories checked ONCE EACH IN ORDER.
  test_the_cleanliness_guard_is_checked_once_per_point_and_above_every_spend   plants the
      stale file by WRAPPING claim_run_root - the only construction that can produce the
      state - and asserts equivalence_gate was NEVER CALLED.  Its stale file is at
      channels_048 and that width is ARBITRARY; see limitation 142.
  test_the_cleanliness_guard_is_not_called_inside_the_curve_loop        the structural half

*** THE TWO-STATE MUTATION SWEEP IS THE SHAPE TO REUSE FOR ANY TEST EDIT: run the SAME cases
    against BOTH test blobs so the two suites are compared on identical inputs; mutate the
    executable in place and restore in a finally with the restore DIGEST-VERIFIED; run twice
    and require identical results.  Copy a "restore the defect" mutation OUT OF THE PRE-REPAIR
    BLOB including its try/except shape - a mutation that fails for a different reason than
    the defect did is not evidence about the defect. ***
```

## THE STEP-4 SHAPE, kept only because it will be needed again if anything else ever spends

```text
BOTH HALVES FOR stage1-run-2 ARE SPENT (mine S100, Codex's S100) AND SO ARE THE TWO BEFORE
THEM.  No Step-4 act is currently in view: C7 is read-only and spends nothing.  If one ever
is: it is its own turn, never folded into a review (bundling converts a review into a spend);
it NAMES the digest, the run label, the BASE DIRECTORY, the executable blob, the budget, and
- explicitly - what it does NOT authorize; and per lesson (oo) it runs every check that sits
BELOW the spend BEFORE authorizing and names the residual no mechanism closes.

*** require_permitted_base IS NARROWER THAN THE DESIGN'S PROSE: it refuses a base only AT OR
    INSIDE results/dev_fit.  Every other destination on this machine is permitted.  So "every
    write is beneath the claimed root" is only as strong as the base NAMED in the
    authorization.  Name it.  (Re-driven S101: dev_fit -> ForbiddenBase; the real base -> ok.) ***

THE OPERATOR-SIDE BRACKET - nine lines of value, reuse it:  two domains, difference STATED.
  DIGEST domain  every file under the project root except .git, venv, __pycache__,
                 .pytest_cache, tmp.   STAT domain  the 3.86 GB data root: path, size,
                 mtime_ns only.  *** A CONTENT CHANGE PRESERVING BOTH IS NOT CAUGHT. ***
  Codex's S100 run: both domains byte-identical before and after, outside the claimed root.

THE FOUR RESIDUALS, none of which is a reason to withhold a half:
  1  a replay at a DIFFERENT BASE or from a COPIED WORKSPACE (section 7.1's own).
  2  a CONCURRENT WRITER.  Uncloseable - anything the bracket notices, it notices after.
  3  the stat-domain blindness above, data root only.
  4  the clean-machine anchor path.  Now 55 checkpoints; see the Phase-3 item below.

*** THE CONCURRENT-WRITER CHECK WAS WRONG TWICE BEFORE IT WAS RIGHT.  (a) "no foreign python
    process" fired on the director's own Dandelion Station suite in a SIBLING directory - the
    check must ask whether a process names THIS PROJECT, not whether the machine is idle.
    (b) On Windows venv\Scripts\python.exe is a LAUNCHER that re-executes the base
    interpreter, so ONE invocation is TWO processes; excluding by pid alone leaves the shim. ***
```

## THE THREE PHASE-3 ITEMS - TWO NOW DISCHARGED IN S105, ONE DISCLOSED. Do not redo the two.

```text
1  DISCHARGED, S105.  The packet runbook had ZERO occurrences of `capacity_sweep`.  It now
   carries STEP 28 (the design and its digest, the width/parameter/receptive-field table,
   plan mode, execute mode with the fresh-label rule, the recorded cost, the 55-checkpoint
   census, and why the failed run and the superseded plan are preserved) and STEP 29 (the
   eight required arguments, the exclusive-create destination, the five per-point means, the
   matching row, the near-miss row, the boundary-block scope rule, and the four "does not").
   `Reproducibility Packet/README.md` is now 104,852 B, blob 16afd81b74e94d3641737688a3ff84c76bf35eb6,
   canonical == raw 21c2e7fead4e7418907b20c9d95c534e791bcdec14fa7b7fbb6e63b56d76d1ce, LF, no CR.
   Edit was +207/-0, additions only.  *** I EXPLICITLY APPROVED THIS STATE AND HANDED IT TO
   CODEX IN MY S105 TURN.  It is documentation, not a gate - nothing waits on it - but if
   Codex returns edits, the owner re-review is MINE. ***
3  DISCHARGED, S105, in the same edit.  Step 29 states that an analyzer's `boundary` block
   describes THE READER, NOT THE RUN, names the sweep's real spend (42 fits / 42 checkpoints)
   and points at the producing run's own record.  It states this as a GENERAL rule covering
   Step 27's block too, so the obligation travels instead of being spot-fixed.
2  STILL OPEN, AND DELIBERATELY DISCLOSED RATHER THAN CLOSED - limitation 145.  The 55
   git-ignored checkpoints have no clean-machine recovery path, and Step 28 now says so in
   those words.  THE REASONING IS THE PART TO CARRY: the reader authenticates every
   checkpoint BY DIGEST, and the only bitwise-reproduction evidence we have (the run's two
   C9 equivalence arms) is ON THE RECORDED MACHINE.  So a rebuilt checkpoint that differs by
   one byte does not reproduce this analysis - it produces a different one, and Step 29
   cannot be re-driven against the TRACKED artifact on a machine lacking those files.
   *** DO NOT "CLOSE" THIS BY WRITING A PROCEDURE THAT READS LIKE A RESTORATION.  If Codex
   judges the cross-machine claim stronger than I allowed, that is a judgment about evidence
   and it should say so; I asked for exactly that in my S105 turn. ***

*** A FOURTH, NEW AND UNPAID - THE AV STORY.  My own note said the Live-Run README entry
    reporting the read's RESULT owed the reader that the reader-script as first written
    could not have read the finished sweep at all, because ten of its fifty models were
    described in numbers rounded by a DIFFERENT PROGRAM, and that this was settled by
    arithmetic on already-published values before any measurement was touched.  I WROTE THAT
    ENTRY IN MY S104 AND IT DOES NOT TELL THE STORY - measured in S105, the public log has no
    occurrence of it.  DATED ENTRIES ARE NEVER EDITED, so it is NOT repairable in place.  The
    obligation now belongs to the TECHNICAL REPORT and, if it earns a place, the ACCESSIBLE
    PIECE.  See lesson 166 for why this happened and what stops it recurring. ***

Do not fix any packet item inside a review session: a packet edit mixed into a review is how
a review stops being one.  S105 was the correct session precisely because nothing was open.
```

## THE TIMESTAMP GATE - built S100, held in S101-S104, AND IT EXPIRED ONCE. Rebuild it from this list.

```text
S100: my authorization-half header said 00:34 PDT against a 00:17:45 write - SIXTEEN MINUTES
INTO THE FUTURE - because I stamped each header while DRAFTING and never re-read the clock at
the APPEND.  Forward skew is the harmful direction: AgentPrompt says the timestamp is what
lets the director audit ORDER, and reconciled against mtimes a message appears to postdate
its own write.  THE PHYSICAL-TAIL CHECK CANNOT SEE THIS.
THE FIX IS A GATE: append_chat.py parses the timestamp out of --header and compares it to the
clock INSIDE THE WRITER, AT THE WRITE, refusing beyond +/-120 s.  S101 stamped the header in
the SAME command that ran the writer; declared 04:22, written 04:22.
*** MEASURE THE CLOCK IN THE SAME COMMAND THAT WRITES.  Do not carry a stamp across turns. ***

*** S104: THE WRITER WAS GONE.  It lived in an untracked session scratch directory and
    untracked scratch does not survive a session.  I found out by going to use it.  I rebuilt
    it from THIS BLOCK before writing anything and all three S104 appends passed (41 s, 27 s,
    54 s of skew against the 120 s limit) - but A CONTROL THAT LIVES OUTSIDE VERSION CONTROL
    IS A CONTROL THAT EXPIRES, and this one survived on a prose description.  It is NOT moved
    into the packet: it is session tooling, and the packet must stay a thing a stranger can
    run.  So the durable artifact is this list. ***

*** AND THE REBUILD WAS WEAKER THAN WHAT IT REPLACED, WHICH IS THE SHARPER HALF.  I rebuilt
    from this block, which describes the S100 five-gate writer that PARSES a hand-authored
    --header.  S103 had already improved it to SEVEN gates in which the writer BUILDS the
    timestamp from the clock at the write, so skew is unconstructible rather than merely
    refused - and that improvement was recorded only in the S103 scratchpad section near the
    BOTTOM of this file, which I did not read before rebuilding.  Nothing was harmed (all
    three skews were small and in the safe direction), but I regressed a control by reading
    the head block and not the whole file.  *** WHEN A LESSON IMPROVES, THE IMPROVEMENT MUST
    MOVE INTO THE BLOCK THAT OWNS THE LESSON, NOT ONLY INTO THE SESSION'S SCRATCHPAD. ***

*** S107: THE WRITER WAS GONE A THIRD TIME AND THE BLOCK REBUILT IT AT FULL STRENGTH AGAIN.
    Two appends, 14 s and 30 s of skew against the 120 s limit, both harmless direction; all
    seven gates printed their measured values.  THE MECHANISM HAS NOW PASSED TWO INDEPENDENT
    TESTS, and the reason is the S105 correction: the improvement was written back into THIS
    block rather than left in the session's own scratchpad.  DO NOT MOVE THE WRITER INTO THE
    PACKET - it is session tooling and the packet must stay a thing a stranger can run.  The
    durable artifact is this list, and the list is now load-bearing evidence for itself. ***

*** S108: THE WRITER WAS GONE A FOURTH TIME, THE LIST REBUILT IT, AND IT CAME BACK WEAKER
    AGAIN - IN A PLACE THE LIST DID NOT DESCRIBE.  I wrote gate 5's recognizer as
      ^\*\*(Claude|Codex|Randy|Human) \(Session \d+, .*\):\*\*
    which reports 215 headers in the Phase-2 transcript.  MY OWN S107 ENTRY RECORDED 254.
    I reconciled the two instead of assuming one was stale, and the difference is NOT the
    file - IT IS THE RECOGNIZER.  The permissive form finds 255 and the 40 it could not see
    all carry a QUALIFIER where the strict one demands a comma: "(Session 7 tail addendum,",
    "(Session 16 pilot handoff,".  A recognizer blind to 40 real header forms would let
    GATE 5 PASS WHILE ONE OF THOSE FORMS SAT UNDERNEATH MY TURN - and pass QUIETLY, because
    the gate prints a number and the number looks fine.  Verified this session's result was
    sound anyway (the permissive last match is my header at the SAME byte offset).
    *** THE LESSON, AND IT IS ONE LEVEL BELOW THE S104/S105 ONE: A CONTROL IS ITS PREDICATE
        AS MUCH AS ITS RULE.  The list described what each gate REQUIRES and not what it
        RECOGNIZES, so the rebuild regenerated a gate whose ACCEPT SIDE nobody ever
        specified - and the accept side is where damage is invisible.  Same shape as the
        S69-S71 scrubber rounds, arriving somewhere completely different. ***
    *** AND THE CHEAP INSTRUMENT THAT FOUND IT: TWO INDEPENDENT COUNTS OF THE SAME OBJECT
        DISAGREED AND I RECONCILED THEM.  Neither looked wrong alone.  The strict count was
        only wrong AGAINST ANOTHER NUMBER, in a file I had written myself six hours before. ***

*** S108, SECOND AND SMALLER, RECORDED AS A SUCCESS: GATE 4 REFUSED MY FIRST MONITORING
    ENTRY, correctly - that entry QUOTES header examples and the gate cannot tell a quoted
    header inside a code fence from a real one.  THE FIX BELONGS IN THE DOCUMENT: indent the
    quotation so it is not at column 0.  A control that has to be relaxed to let a document
    ABOUT the control through is a control that stops holding the week someone is in a hurry.

*** S109: THE WRITER WAS GONE A FIFTH TIME AND THE LIST REBUILT IT AT FULL STRENGTH,
    INCLUDING GATE 0.  This is the FIRST rebuild that inherited the recognizer, because S108
    wrote the recognizer INTO the list rather than leaving it in a session scratchpad - the
    S105 correction working a second time, one level deeper.  All seven gates printed their
    measured values: prior 1,869,733 B, +7,756, prefix byte-identical, SKEW 0 s (the writer
    BUILDS the stamp, so skew is unconstructible rather than merely refused), headers
    256 -> 257 under the permissive pattern, last header mine.
    *** THE MECHANISM HAS NOW SURVIVED THREE INDEPENDENT REBUILDS (S107, S108-corrected,
        S109).  DO NOT MOVE THE WRITER INTO THE PACKET - it is session tooling and the packet
        must stay a thing a stranger can run.  The durable artifact is this list. *** ***

THE GATE LIST TO REBUILD FROM (seven; the writer is a BYTE APPEND, never a patch, which is
what lets it promise a byte-identical prefix on a mixed-EOL file):
  0  THE RECOGNIZER, which is part of the control and not an implementation detail.  Use
     the PERMISSIVE form and nothing narrower:
         ^\*\*[A-Za-z]+ \(Session [^)]*\):\*\*        (re.MULTILINE, bytes)
     Measured S108 against the live transcript: this finds 255, a strict comma-and-digits
     form finds 215.  Gates 3, 4 and 5 are all applied THROUGH this pattern.
  1  re-read the prior bytes, record SHA-256, and RE-ASSERT them as an exact prefix AFTER
     the write;
  2  BUILD the header timestamp from the clock inside the writer at the write (do not parse
     one from an argument), and refuse anyway if a supplied stamp differs by > 120 s;
  3  refuse if that exact header already appears in the file;
  4  refuse an empty body, and refuse a body that itself contains a header line (one append
     is one turn).  A body that legitimately QUOTES a header indents the quote; do not
     weaken this gate to accommodate one;
  5  after the write, require MY header to be the LAST header in the file;
  6  emit the separator the file's own tail needs, measured from the tail, not assumed;
  7  print every gate's measured value, so the append's own record is in the transcript.

*** S110: THE WRITER WAS GONE A SIXTH TIME AND THE LIST REBUILT IT AT FULL STRENGTH AGAIN,
    INCLUDING GATE 0.  All seven gates printed their measured values: prior 1,881,576 B,
    +7,967, prefix byte-identical, SKEW 0 s (the writer BUILDS the stamp), headers 258 -> 259,
    last header mine, separator b'\n' MEASURED from the tail b'ex\n\n---\n'.
    *** THE MECHANISM HAS NOW SURVIVED FOUR INDEPENDENT REBUILDS (S107, S108-corrected, S109,
        S110).  The list is load-bearing evidence for itself and IT IS THE ONLY THING THAT
        SURVIVES A SESSION.  DO NOT MOVE THE WRITER INTO THE PACKET - it is session tooling
        and the packet must stay a thing a stranger can run. ***
    ONE IMPLEMENTATION DETAIL THE LIST DID NOT CARRY AND NOW DOES: on Windows the timezone
    name comes back LONG ("Pacific Daylight Time"), so gate 2 must abbreviate to initials or
    the header format silently stops matching the project's convention. ***

*** DO NOT COMPARE A HEADER COUNT ACROSS REBUILDS.  It is a property of the recognizer, not
    of the transcript.  Under the permissive pattern the count after my S110 append is 259
    on the Phase-2 chat (255 after my S108; +1 Codex S108, +1 mine S109, +1 Codex S109, +1
    mine S110) and 13 on the monitoring chat, which I did not append to in S109 or S110. ***
```

## FINDING AT - CLOSED. The two sentences a future session must not undo.

```text
THE REPAIR IS A SIBLING CHECK, NOT A TENTH IDENTITY ENTRY, and the distinction is load-
bearing: a tenth entry collides with C3's require_anchor_comparability, which requires
additions == {"capacity_sweep.py"}.
  APPROVED_ANALYZER_IDENTITY_FIELD_PATH = ("inputs","analysis_code_identity",
                                           "analyze_dev_fit.py")
  require_approved_analyzer_identity(analysis)   capacity_sweep.py ~line 641
    reads that field out of the ALREADY-BOUND approved analysis artifact, validates its
    shape, hashes the imported module through code_identity(), refuses on disagreement.
  Called from plan_document() AFTER require_anchor_comparability and BEFORE any arm is
  built; require_authorized_plan() REBUILDS plan_document(), so the same comparison runs
  again at the execution-authorization boundary, above every spend.
*** DO NOT "SIMPLIFY" IT INTO sweep_code_identity().  That is the collision above. ***
Re-driven green in S101, with a negative control: a zeroed analyzer identity is refused.

WHY IT IS RIGHT AND NOT THE AS DEFECT AGAIN: the guard calls code_identity, and
analyze_dev_fit.analysis_code_identity() - which produced the recorded 4caa2938... -
calls the SAME code_identity out of the same dev_fit_contract.  ONE definition consumed
twice, not two copies that agree today.

*** protocol_p.py IS THE ONE PROJECT MODULE IN NEITHER SET, and that is RECORDED, NOT A
    FINDING.  Codex has not contested this across four reviews. ***
Full account: HumanReport95.md / HumanReport96.md; lessons 143, 144, 150.
```

## THE NON-FINDING I MEASURED AND DECLINED - do not "fix" this in a later session

```text
The approved ANALYSIS artifact carries NINE identity entries; EIGHT are the same labels
the approved LEDGER carries; NOTHING in the executable compares those two eights.
MEASURED S96: no disagreement, all eight byte-identical.

I DID NOT ASK FOR A GUARD, and the reasoning is the thing to carry, not the measurement.
AT was LIVE - the plan's bytes could stay identical while an UNBOUND FILE ON DISK moved
underneath them.  This is TWO FROZEN DOCUMENTS whose exact canonical digests the plan
ALREADY binds as approved_analysis_sha256 and approved_fit_ledger_sha256.  Given those
bytes the property is FIXED, and a property of bound bytes that has been measured once
does not also need a runtime check.  *** Adding one would be the cargo-cult version of
AT: the ritual of the last finding applied where its mechanism does not exist. ***
Stated in the chat so Codex can overrule the REASONING and not only the code.  STILL NOT
OVERRULED AS OF S101 - a declined guard is a standing decision, not a closed loop.
```

## THE TWO S97 SCOPE STATEMENTS - measured, deliberately NOT raised, do not "fix" either

```text
1  THE FOUR DELIVERED-DATA DIGESTS BIND IN THE **RAW** DOMAIN, AND THAT IS CORRECT.
   manifest.csv 945 CRLF pairs, labels/index.csv 945, observations/C1 473, observations/S
   473; all four match the RAW digest, none matches the canonical one.  NOT the S59
   rule-(cc) violation it looks like: they are GIT-IGNORED GENERATED DATA, not tracked
   text; csv.DictWriter through open(..., newline="") pins lineterminator to '\r\n' as a
   STDLIB CONSTANT on every platform (read back AT RUNTIME, not trusted from docs); and
   ALL FOUR VALUES ARE BYTE-IDENTICAL TO THE ONES THE APPROVED LEDGER AND ANALYSIS CARRY.
   *** S100 CAUGHT ME FROM THE OTHER SIDE: my own audit applied the tracked-text rule to
       these GENERATED files and reported four false failures.  THE FIX IS TO ASSERT BOTH
       DIRECTIONS - raw matches AND canonical does not - so a future silent domain move
       fails loudly instead of quietly. ***
2  role_index_sha256 IS A PROVENANCE DECLARATION, NOT A GATE, and the plan does not claim
   otherwise.  require_authorized_dataset enforces the data-root NAME, the MANIFEST DIGEST
   and the CONFIG HASH at execute time.  NOTHING IN THIS READ PATH EVER OPENS AN index.csv
   - the trainer and the analyzer reach payloads through manifest.csv - so there is no
   execute-time gate a role-index digest could be.
Both stated in the chat with their reasoning exposed.  NEITHER is a defect.
```

## THE EXECUTABLE - WHAT IT IS, SO A LATER SESSION DOES NOT REDESIGN IT

```text
scripts/utils/capacity_sweep.py    ONE module, two modes.  BOTH MODES ARE SPENT for
  stage1-run-2.  Nothing in it should be edited without a new finding.

THE SIX PURE FUNCTIONS C7 MUST IMPORT RATHER THAN RESTATE - the module defines them and
  NEVER CALLS THEM, and its docstring says so:  headroom, pair_constraint, classify_shape,
  quantize, derived_label, and require_complete_sweep (C10).

require_approved_analyzer_identity()  THE AT REPAIR.  See the block above.  Do not fold
  it into sweep_code_identity(): that collides with C3.

capacity_point_directory()   THE ONE definition of the channels_NNN directory (S94, AS).
  It takes ONE arg and returns a BARE component - READ THE FUNCTION, do not remember it.
  checkpoint_relative_name COMPOSES it; _execute_mode's point_dir CONSUMES it.  An AST
  test pins that the format exists in exactly one f-string.

fit_arm_at_width()   IS dev_fit_trainer.fit_one_arm's body (lines 942-995 of the approved
  blob) with ONE expression changed: TemporalAttributionNet(seed=seed) becomes
  build_network(channels=channels, seed=seed).  EVERY project-defined name is IMPORTED,
  not retyped.  *** cs.arm_loss IS trainer.arm_loss and cs._stack IS trainer._stack - a
  test asserts identity, not similarity. ***

build_network()      THE ONE construction site.  enforce_rung1_band=True appears EXACTLY
  ONCE in the whole module and an AST test pins that.  No flag can turn it off.

sweep_code_identity()  NINE entries: the eight from trainer.training_code_identity() plus
  capacity_sweep.py.  C3 requires all eight to match the approved ledger EXACTLY and
  permits exactly ONE addition.  *** RE-MEASURED S101: all eight still match. ***
  AND: the ten REUSED anchors in the run record carry the LEDGER'S EIGHT, not this nine -
  writing the sweep module into their provenance would backdate a file that did not exist
  when they were fitted.  Do not "harmonize" that.

capacity_shape_map()   Constructs all five nets, reads n_parameters and receptive_field
  OFF THE NETWORK, and requires the design's section-4.2 table.  Re-driven S101.
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

107. **[NEW S77] CPU AND GPU DISAGREE ON THIS ARCHITECTURE UNDER PYTORCH'S OWN DEFAULT.**
    Measured over four seeds on a 768-step window, same weights, same input, max absolute
    difference on the four-class simplex: **8.842e-05** with `torch.backends.cudnn.allow_tf32
    = True` (the default), **5.960e-08** with it False. Three orders below Slot 11's 0.05
    macro-F1 bar, so it threatens no headline — but it falsifies two things the project does
    rely on: that a persisted result reproduces on another machine, and that a paired
    C1-vs-S difference is a difference in **sensing** rather than partly in which device or
    backend flag each arm ran under. `attribution_net.deterministic_conv_precision()` pins it
    and restores the previous value on exit. **Every later component that runs a forward or
    backward pass — the trainer, the calibration stage, the evaluation driver — must use that
    same context rather than re-deciding, and the Technical Report must state the setting the
    reported numbers were produced under.**

108. **[NEW S77] `nn.Module.to()` MOVES IN PLACE, SO ADOPTING A CALLER'S NETWORK ALIASES IT.**
    Two estimators built from one network shared weights, so loading trained weights into
    either reached into the other — which is exactly the matched C1-vs-S and multi-seed usage
    the rung exists for. Fixed by deep-copying. **It surfaced only because one test built TWO
    estimators from one net; a single-consumer test would have stayed green forever. An
    aliasing defect needs two consumers to become visible, and no amount of coverage of one
    consumer substitutes.**

109. **[NEW S78] `..` IS A BARE NAME TO PYTHON'S PATH LIBRARY, AND `.` IS NOT.**
    `PureWindowsPath("..").name == ".."`, so an "equals its own final component"
    predicate accepts it — and joining it to a root walks *up* the tree.
    `PurePath(".").name` is `""` and the same predicate already refuses it. The pair is
    now an explicit `RESERVED_COMPONENT_NAMES` constant pinned by equality, because it is
    a decision about NAMES and not a property of any shape. **Any future bare-name check
    anywhere in this packet inherits the same hole.**

110. **[NEW S78] HALF OF MY OWN PATH PREDICATE WAS DEAD CODE, AND ONLY THE SWEEP SAW IT.**
    I wrote the bare-name check as a conjunction over `PureWindowsPath` and
    `PurePosixPath`. Dropping the POSIX half survived the whole focused suite. Enumerated
    3,564 strings (11 cores x 18 prefixes x 18 suffixes): **1,009 the Windows parser
    refuses and the POSIX parser accepts, ZERO the other way.** `PureWindowsPath` is a
    *pure* type whose parsing does not depend on the host and treats both separators,
    drive designators and UNC roots as structure. The POSIX conjunct rejected nothing, so
    it was deleted rather than left looking authoritative, and the measurement is in the
    docstring. **A conjunction of two parsers is one parser plus decoration unless
    something has measured which inputs the weaker one alone rejects.**

111. **[NEW S78] TWO GUARDS IN MY OWN NEW MODULE WERE UNTESTABLE FOR THE OLDEST TWO
    REASONS.** The suite filter in `select_dev_rows` could be deleted entirely with the
    suite green, because my fixture had `dev` rows in C1 and S only — the fixture already
    had the property the filter establishes (Session 58's shape, recurring). And
    `as_document()` could skip its validation call, because my only invalid-record test
    went through `provenance_string()` — **a record that refuses to describe itself but
    agrees to be written to a file is the worse half.** Both closed. Both found by
    mutation, neither by reading.

112. **[NEW S79] "NO CONTROL CHARACTERS" IS NOT "ONE LINE", AND THE GAP IS THREE
    CODEPOINTS.** `U+0085` NEL, `U+2028` LINE SEPARATOR and `U+2029` PARAGRAPH SEPARATOR
    are line boundaries to `str.splitlines`, are not ASCII control characters, and are
    legal in a directory name on both hosts. Measured over every codepoint (1,112,064,
    surrogates excluded): 3 values accepted as bare names still split
    `provenance_string()` in two; after making the promise the post-condition, 0. **Both
    the control rule and the single-line rule are live and neither subsumes the other**
    (`	` and `` are single-line; `U+2028` is control-free). **Any other place in
    this packet that promises a one-line record and enumerates forbidden characters
    inherits the same gap.**

113. **[NEW S79] PYTHON'S EQUALITY DOES NOT AGREE WITH THIS PROJECT'S IDEA OF A SEED.**
    `("C1", True) == ("C1", 1)` with an equal hash, and `("S", 4.0) == ("S", 4)`, so a
    membership test over a set certified a *complete matched plan* containing a bool that
    `require_predeclared_seed` refuses outright — two guards in one module disagreeing
    about one quantity. Closed by an entry-shape check before the set arithmetic.
    **Any future check that decides membership by set or dict lookup over numeric keys
    has the same hole**, including anything keyed on a seed, an ordinal, or a count.

114. **[NEW S79] A CONTAINMENT CHECK ON THE AUTHORITY STRING SURVIVED THE WHOLE SUITE.**
    Replacing `self.authority == DEVELOPMENT_ONLY_AUTHORITY` with `in` passed every test
    in the file. That check is the one thing standing between a development-only
    checkpoint and a downstream artifact, and containment admits a record that wraps the
    mandated string in text of its own — *including text that contradicts it*. Now pinned
    by two constructed states. **Bound 4 says EXACT; every other equality pin in this
    packet deserves the same question asked of it.**

115. **[NEW S80] THE PRODUCER OF BOUND 4's CODE IDENTITY RETURNED THE VALUE THE RECORD
    REFUSES, SILENTLY.** `code_identity({})` returned `{}` with no refusal — the ONLY
    silently accepted cell in a 140-cell grid over every public entry point in
    `dev_fit_contract.py` — while `DevFitProvenance.validate()` refused exactly that
    mapping one step later, with a message about the record rather than about the call
    that built it. Label rule and digest rule already agreed in both places; only the
    non-empty rule disagreed. Closed by stating the rule ONCE as `require_code_identity`,
    called by producer and consumer, with the producer ending by asserting it. **Any
    future field validated in two places in this packet has the same hole, and copying
    the consumer's block into the producer would leave it — the fix is one source, not
    two matching ones.**

116. **[NEW S80] FORTY FOREIGN-EXCEPTION ESCAPES REMAIN IN THAT MODULE AND ARE DISCLOSED
    RATHER THAN CLOSED.** `require_dev_only`, `select_dev_rows` and
    `require_complete_matched_plan` raise `TypeError`/`AttributeError` rather than
    `DevFitContractError` when handed a non-iterable or a list of the wrong element type.
    **Measured: every one is LOUD and NO bound in the module is permeable** (0 silent
    accepts over 140 cells after S80). I left them because converting
    loud-in-the-wrong-domain into loud-in-the-right-domain is decoration unless something
    depends on the domain — **and because the choice favours me, it was handed to Codex to
    rule on rather than taken.** If Codex rules they should close, close them; the ruling
    is pending as of S80. **No write-up may say this module refuses every malformed input
    in its own exception domain.**

117. **[NEW S82] THE DEVELOPMENT FIT SEES ONE WINDOW PER RUN — 152 EXAMPLES PER ARM, 76
    PER TRAJECTORY PER SUITE.** This is deliberate (a stride is a second unregistered
    choice and yields correlated windows) and it is small. **No write-up may describe this
    as a training set of any size without the number.** Under bound 5 its purpose is to
    show the implementation learns and to expose failure modes — not to select capacity —
    which is what makes the size acceptable rather than a defect.
118. **[NEW S82] THE ORDINARY DEV TRAJECTORY'S WINDOW CONTAINS NO PROBE EXCITATION**, by
    construction — `trajectory_dev_ordinary_a` has `diagnostic_probe: null`. Half the
    development examples therefore carry gauge information driven by task motion alone.
    **State that as a property of the training distribution whenever a dev fit result is
    reported**; it is also the reason the two trajectories are held at the same
    time-since-onset. *** S83 CORRECTION: that equal lead removes an AVOIDABLE
    time-since-onset difference; it does NOT make excitation the only thing that differs,
    because the assignment also changes target joints and task timing. Codex narrowed this
    in its S82 and I accepted it in full. Do not restore the stronger sentence. ***
119. **[NEW S82] THE DEV SPLIT CARRIES NO OOD ROW**, so the unknown head is trained on an
    all-zero target in every arm. Nothing about OOD behaviour may be inferred from a
    development fit. (OOD settings exist only in val and test — limitation 2.)
120. **[S82, RESOLVED S83] THE WINDOW POLICY IS NOW JOINTLY APPROVED** (me S82, Codex
    S82), so the "one author" caveat is retired. Codex checked the derivation against the
    approved assignment and Protocol P rather than against my arithmetic. It also accepted
    the pilot/val/test rows of the derived table as **arithmetic over the assignment
    only** — expressly *not* authorization to read those roles.

121. **[NEW S83] `sum(examples_by_trajectory) == len(arm_rows)` IS FORCED BY
    CONSTRUCTION, NOT A LIVE CROSS-CHECK.** `load_arm_examples` appends exactly once per
    row and has no skip path, so the equality cannot fail against the current caller —
    measured: the mutation survives the focused sweep **and** the full 1,515-test suite.
    **My own S82 summary called it a run-time cross-check and that overstated it.** It
    stays as a regression guard against a future edit that drops or duplicates a row, and
    the code now says so. **No write-up may present it as evidence that
    `windows_per_run = 1` was measured.** Same family as limitations 55 and 76.

122. **[NEW S83] A CHECKPOINT FILE CARRIES NO PROVENANCE OF ITS OWN.**
    `torch.save(net.state_dict(), buffer)` writes bare weights, so `dev_fit_result.json`
    is the **sole** record binding each `dev_fit_*_seed*.pt` to its data root,
    manifest/config/assignment digests, suite, seed, training protocol, code identity and
    checkpoint digest. Anything that overwrites, relocates or regenerates that document
    orphans every checkpoint beside it. This is why the staleness guard cannot be allowed
    to write it (Finding S), and it is a standing constraint on anything downstream that
    touches that directory.

123. **[NEW S83] THE IDENTITY-MATCHING GUARD CANNOT FIRE ON THE DELIVERED DATA.** There
    are **0** duplicate `(trajectory, suite, pair_id)` keys in the delivered manifest, so
    both the set version and the multiset version accept it. The guard exists for a
    regenerated or corrupted manifest, which is the only population it was ever written
    for. **No write-up may present its passing as a measurement of the delivered set's
    matchedness** — the census counts (76/76 per trajectory per suite) are that
    measurement.

124. **[NEW S83] `X_OUTPUT_DIRTY` IS A SIXTH TERMINAL EXIT AND A DESIGN CHANGE I MADE
    UNILATERALLY.** The module's five-exit shape was settled before this session. I added
    the sixth because every alternative either destroys the protected record or stops
    persisting an artifact on an exit, and I would rather add a name than weaken either
    invariant — but **Codex has not ruled on it**, and neither has it ruled on my deletion
    of the dead `control_dt_s` guard inside `_exact_steps`. Both were flagged in the S83
    handback as its call. **If S84 finds them unanswered, ask rather than assume
    consent.**

125. **[NEW S84] `final_loss` AND `loss_history` ARE NOT LEARNING SIGNALS, AND THEY ARE WHAT
    THE ARTIFACT PERSISTS.** `arm_loss` sums four equally weighted terms, one of which is a
    Gaussian NLL carrying `+ log_scale` — **unbounded below**, and the head may drive it to
    its -10 clamp. Measured in-sample: class 0.434/0.557, loc 0.514/0.557, **sev
    -1.162/-1.116**, ood 0.023/0.017 (C1/S). The severity term is both what makes seven of
    ten arms report a NEGATIVE loss and the term that varies most between arms, so **ranking
    arms by `final_loss` ranks them by how confident the severity head became.** Nothing in
    the module is wrong; the reporting surface is. **No write-up may present a loss value or
    a loss curve from this artifact as evidence of classification quality.** I proposed to
    Codex that the artifact persist the four terms separately (Finding X); its ruling is
    pending as of S84.

126. **[NEW S84] THE SEED SPREAD SWAMPS THE EFFECT THE STUDY IS DESIGNED TO DETECT.** Paired
    S−C1 macro-F1 over five seeds: +0.075, +0.039, −0.239, +0.104, −0.140 — mean −0.032,
    **sd 0.150**, against a pre-declared bar of **≥0.05 absolute** over **≥5 seeds**. C1's
    own spread across seeds is 0.343. **Scope, and it must travel with the number:** this is
    IN-SAMPLE, at 20 epochs on 152 examples, at one capacity rung, with no early stopping,
    and in-sample spread is not held-out spread. It is not a power calculation and must not
    be reported as one. **It is the first direct measurement of how much this architecture
    moves with its seed alone, and it belongs in the Gate-6 sample-size decision before the
    confirmatory design is frozen.**

127. **[NEW S84] AT RUNG 1, IN-SAMPLE, S FITS WORSE THAN C1 — AND THAT IS A STATEMENT ABOUT
    CAPACITY, NOT ABOUT INFORMATION.** Per-class F1, paired S−C1: healthy +0.100, structure
    **−0.069**, actuator **−0.108**, sensor **−0.052**. S is C1 plus four gauge channels at a
    **fixed 39,594 parameters** — strictly more input, identically much capacity — so a net
    can fit worse while the extra channels carry real signal. The Efficiency standard already
    names this case (a null from an undersized model is evidence about the model), and Slot 9's
    capacity ladder is the instrument for it. **No write-up may present this as evidence
    against the hypothesis. What it licenses is: the ladder must be climbed for S before any
    C1-vs-S conclusion is drawn.** Two established limitations point the same way and are not
    double-counted here: 67 and 118. **I verified the gauge channels actually reach the
    network before reading any direction into this** — see the head of this file.

128. **[NEW S84] THE TEN CHECKPOINTS ARE GIT-IGNORED AND THEIR PROVENANCE IS ONE TRACKED
    FILE.** The packet's own `.gitignore` excludes `*.pt`, which is right (large rebuildable
    model payloads) and makes `results/dev_fit/dev_fit_result.json` the **sole** surviving
    record binding each checkpoint to its data root, digests, suite, seed, protocol and code
    identity. That is limitation 122 arriving in the real world rather than in a docstring.
    **Anything that overwrites, relocates or regenerates that document orphans all ten**, and
    a fresh clone of this repository has the record without the weights — which is the
    intended trade, but it means the weights are reproducible-in-principle and not archived.

129. **[NEW S85] THE PACKET PUBLISHED A RAW DIGEST FOR A TRACKED TEXT ARTIFACT WHOSE RAW
    BYTES ARE CHECKOUT-DEPENDENT — the fourth instance of limitation 80's class, and the
    first one inside a RUNBOOK INSTRUCTION.** `dev_fit_analysis.json` carries 426 LF
    newlines, the path is `text: unspecified`, and `core.autocrlf=true`, so a fresh
    checkout renders **14,591 bytes / 426 CRLF** and a different raw digest. Fixed by
    publishing the CANONICAL digest, which is stable everywhere; `.gitattributes` was
    deliberately NOT touched, because the root file's own comment says pinning is defence
    in depth and the digesting code folds CRLF to LF, so "publish canonical" is the settled
    position. **The contrast is the thing to carry: `dev_fit_result.json` has NO newline of
    either kind, so its raw and canonical digests are one number in every checkout. Two
    files in one folder, opposite exposure, and only the indented one is exposed.**

130. **[S85, WRONG — CORRECTED S86] THE ANALYZER'S DERIVATION PATH *IS* COVERABLE FROM THE
    PACKET, AND MY CLAIM THAT IT WAS NOT WAS FALSE.** I wrote that six mutation survivors
    inside `derive_analysis` / `load_authorized_examples` survive "by construction," that
    no test the packet can ship will reach them, and that closing them requires extracting
    pure functions. **All of that is wrong.** Codex rejected the premise in its S85:
    `load_authorized_examples` is already the real-data ingress and `derive_analysis`
    already consumes its return value through the `evaluate_arm` seam, so monkeypatching
    those two names drives the production guards and arithmetic with synthetic fixtures and
    **no production change at all**. Measured in my S86 sweep: with fixtures in place, 14 of
    14 derivation-path mutations are caught. **The correct statement for a write-up is that
    the derivation path is covered by synthetic-fixture tests through the loader and
    evaluator seams, and that no test exercises the physical loaders themselves** — which is
    a much narrower and true claim. The general form, and the reason this is kept rather
    than deleted: **"this needs real data to RUN" and "this needs real data to TEST" are
    different statements, and I collapsed them.**

131. **[NEW S85] `round(x, 12)` IS A NO-OP AT float32 RESOLUTION, SO IT STABILISES
    NOTHING.** Every float the analysis artifact carries round-trips through it to the
    **identical float32**, because the loss terms originate in float32 tensors and the
    rounding threshold sits several digits below float32's own resolution. Measured, all
    172 nonzero floats: 10–13 significant digits retained, zero merged values. The
    docstring claimed the rounding made the artifact "hardware-stable"; it does not, and
    what actually makes the artifact reproducible is the fixed CPU device, the deterministic
    convolution context and the verified checkpoint digests. **Cross-platform bit-identity
    of this artifact has NOT been measured — same standing gap as limitation 46.**

132. **[NEW S85] A TEST THAT BINDS AN ARTIFACT TO ITS PRODUCER IS A BYTE-IDENTITY TRIPWIRE
    AND IT DESTROYS MUTATION-SWEEP RESOLUTION OVER THAT FILE.**
    `test_tracked_analysis_names_the_current_analyzer` is correct and load-bearing — it is
    the missing half of the fit side's own producer binding, and it is what forces a
    regeneration after any analyzer edit. It is also why a sweep over `analyze_dev_fit.py`
    reported 19/19 and then 25/25 caught: it fails for ANY byte change. **Any sweep over
    that file must deselect it, and must ASSERT the deselection took effect — `pytest
    --deselect` silently ignores a node id that matches nothing.** The warning is written
    into the test's own docstring, which is the only place the next person will see it.

134. **[NEW S88] THE APPROVED DEV-FIT TRAINER CANNOT FIT ANY WIDTH BUT 32, AND MY OWN
    COMPARABILITY INVARIANT WOULD HAVE REFUSED THE ONLY FIX.** Measured:
    `dev_fit_trainer.py:968` is the file's ONLY network construction site and reads
    `TemporalAttributionNet(seed=seed)`; `fit_one_arm` takes examples, seed, epochs,
    batch size, learning rate and device and **no width**; the CLI has no capacity flag;
    and `grep -c 'channels'` returns **0** in both `dev_fit_trainer.py` and
    `dev_fit_contract.py`. **The Gate-4 fit path is width-locked at the 32-channel
    default**, so the capacity sweep as designed at S87 - and as Codex reviewed in detail
    - was unimplementable, and neither review saw it because both checked the design
    against its own logic. The collision on top: invariant C3 requires the reused anchor
    row's recorded `code_identity` to match the code fitting the new points, so threading
    `channels` through the trainer moves `training_code_identity()["dev_fit_trainer.py"]`
    and **the anchor fails its own check by construction**. Answered by invariant **C9**,
    which refits ONE 32-channel arm through the new path into a scratch root and requires
    **bit-identical** parameter tensors against the approved checkpoint, refusing loudly
    on difference, on a missing checkpoint (a fresh clone has the ledger without the
    weights) and on an unmakeable comparison. **The route - a new module vs an additive
    keyword on `fit_one_arm` - is CODEX'S CALL and was handed over, not taken.**

135. **[NEW S88] THE S87 SATURATION CRITERION WAS ON THE WRONG QUANTITY, AND IT FAILED IN
    THE DIRECTION THAT DISCARDS EVIDENCE.** The read is over macro-F1; the criterion was
    "mean in-sample four-way ACCURACY of both suites >= 0.98". Codex's aggregation
    objection was right and this one sits under it. Measured on the exact 8/16/32/96
    census: 3 healthy examples misclassified as sensor gives accuracy **0.9803** (the S87
    rule says SATURATED) with macro-F1 **0.9385**, so `|d|` could still be **0.0615**;
    3 structure errors give accuracy 0.9803, macro-F1 0.9347, `|d|` up to **0.0653**.
    Both exceed the project's own **0.05** bar, so the rule would have thrown away points
    where a bar-sized difference was still arithmetically available - **and a guard that
    discards good evidence produces a smaller reported result with no error message
    anywhere.** Replaced by an identity rather than a threshold: for macro-F1 in [0, 1],
    `|d| = max - min <= 1 - min`, so `headroom(c,k) = 1 - min(F1_C1, F1_S)` is an EXACT
    upper bound, and a pair is BAR_CONSTRAINED iff `headroom < BAR` where **`BAR` is read
    at run time from the approved artifact's `paired_macro_f1.claim_sheet_success_bar`
    field**, not written as a literal. Rung-1 per-seed headroom is **0.3157 to 0.5133** -
    nowhere near constrained. **The general form: check that a guard's quantity is the
    quantity the read is over, not merely a correlate of it.**


136. **[NEW S89] REMOVING THE OUTPUT PATH FROM A PLAN DOCUMENT MADE ITS EXECUTION
    AUTHORIZATION RE-USABLE, AND NOTHING IN EITHER AGENT'S REVIEW COULD HAVE SEEN IT.** The
    Step-4 authorization is a digest: `require_authorized_plan` (read at source, S89) checks
    `mode`, `plan_valid`, `terminal` and canonical-digest equality, and has **no notion of a
    run**. While the capacity plan serialized its host output root, two executions were
    necessarily two documents with two digests, so one joint authorization licensed exactly
    one execution — *accidentally, but really*. Codex's S88 removed the path, correctly (a
    physical path and byte-determinism cannot both be required), and its S88 also replaced
    resume with "a retry uses a fresh output root and a fresh plan and runs all forty new
    curve arms again." The retry plan is then **byte-identical** to the one already
    authorized, so a second full 42-fit spend passes the digest gate, passes the fresh-root
    cleanliness guard, and needs no second joint act — contradicting §10 step 4 of the same
    document. **Neither edit does this alone.** Repaired by a required `run_label` in the
    plan's logical namespace (machine-independent, so byte-determinism across hosts survives
    verbatim; run-scoped, so a retry is a different document), plus explicit §7.3 language
    that a retry is a second authorization and §7.2 recording of `run_label` beside the
    consumed digest. **The general rule: before deleting a field from a contract, ask what
    else was depending on it existing.** Third occurrence of limitation 95's shape (a digest
    names a document, it does not certify the act) — the other two are `config.json`'s
    eventual freeze and the payload extension's own plan gate, and **both are still live**.
    **[CORRECTED S89/S90 — THE OVERCLAIM HALF IS WITHDRAWN.]** Codex's S89 correction AD is
    right and I accepted it without contest: **`run_label` does not make a digest
    mechanically single-use.** `--approved-plan-sha256` names a document; the same document
    can be submitted twice, and no field inside a deterministic local document prevents that
    without an external durable consumption registry the design does not introduce. The
    check that settles it is not the argument but the code the design cites: **`--output-dir`
    in `dev_fit_trainer.py` is `required=True` and is a host path, and
    `require_clean_fit_output` checks that supplied directory** — so a replay into a fresh
    directory passes. What survives of this limitation is the *diagnosis* (removing the path
    removed the only run-level identity) and the general rule; what is withdrawn is the claim
    that the replacement field restores single-use. **See limitation 138 for what the
    remaining guarantee actually rests on.**

137. **[NEW S89] THE BATCHER IS PRIVATE, AND THE ROUTE-A RULING DID NOT SAY WHAT THE COPIED
    LOOP CALLS.** Route A's new module reimplements `fit_one_arm` (`dev_fit_trainer.py`
    942–995) with exactly one expression changed — `TemporalAttributionNet(seed=seed)` →
    `TemporalAttributionNet(seed=seed, channels=channels, enforce_rung1_band=True)`.
    Everything else in that body must be imported: `require_predeclared_seed`
    (`dev_fit_contract.py:183`), `deterministic_conv_precision` (`attribution_net.py:115`),
    `arm_loss`, `DevFitDataError`, and **`_stack` — which has a leading underscore and is the
    batching function**, i.e. the single place a retyped copy would most plausibly diverge in
    a way that changes weights. The row-order permutation
    (`np.random.default_rng(seed).permutation(len(examples))`) is in-body and
    **width-independent** (measured S88). The decision recorded in the design: **import
    `_stack`, disclose the private cross-module import, do not retype the batcher** — the
    alternative is exactly the divergence C9 exists to catch, and paying a gate failure to
    discover it wastes the gate. *(This project has one prior private-import precedent
    pointing the other way — Codex's S45 ruling to keep `_plant_payload` private. The
    difference is that there the import was avoidable; here the alternative is a duplicated
    definition of a weight-determining function.)* **[NARROWED S89/S90 BY CODEX'S AE, WHICH
    I ACCEPTED IN FULL.]** "Everything else in that body must be imported" is
    **unsatisfiable** and was my error. `fit_one_arm` also calls `torch.manual_seed`,
    `torch.optim.Adam`, `.to(device)`, `net.train()`, `optimizer.zero_grad`,
    `loss.backward()`, `optimizer.step()`, `loss.detach().cpu()`, `np.mean` and two
    finiteness checks, **and its control flow is itself copied** — none of it importable,
    because no project helper wraps it. The correct statement: the table is the complete
    **project-defined dependency surface**, and it has exactly six members —
    `TemporalAttributionNet` (which I had omitted), `require_predeclared_seed`,
    `deterministic_conv_precision`, `arm_loss`, `_stack`, `DevFitDataError`. **Re-enumerated
    at source in S90; the table is complete.** C9 is the measured backstop over the *whole*
    copied seam, not merely the tabulated calls.

138. **[NEW S90] THE RUN ROOT WAS NEVER BOUND TO ANYTHING, AND AN AUDIT CLAIM WAS RESTING ON
    IT.** The design named a `run_label` and a packet-relative namespace
    (`results/capacity_sweep/<run_label>/…`) and **never said how either relates to the
    directory the executable writes into**. Three rules depended on that unstated answer —
    "a non-empty output root is refused", "a retry uses a fresh output root", and the
    sentence Codex wrote in the same session, that repeated use of the same label/digest "is
    recorded rather than silently presented as a new authorization." **The third one fails
    under the free-choice reading**: two executions at one label write two run-level
    artifacts into two unrelated directories and nothing brings them together, so "auditable"
    described a diligent reader rather than a guard. Repaired in C2 by binding the run root
    to `<base>/<run_label>/` — `<base>` supplied, label read from the plan, **no host path
    enters the document and byte-determinism is untouched**. This buys three things: the
    audit claim becomes a refusal at a named exit; §7.3's "fresh output root" stops being a
    second operator obligation and follows from the new label; and the residual narrows from
    *any fresh directory* to **a different base or a copied workspace**, which §7.1 now
    states at that width. **The general rule: when a document says something is "recorded",
    "auditable", "visible" or "reconstructable", ask which named guard or which collision
    makes it so.** *(And the meta-rule this round produced: the dangerous moment in a review
    is the concession, not the disagreement — withdrawing a strong claim moves the load onto
    a weaker sentence nobody has examined.)*
139. **[NEW S91] TWO CORRECT REPAIRS BOUND TWO OF THREE WRITE LOCATIONS, AND THE THIRD WAS
    ONLY EVER DESCRIBED NEGATIVELY.** After limitation 138 bound the run root and Codex's S90
    correction bound the refusal sink, the design still named a third execute-mode write
    location — C9's scratch output root — in three places (§4.4 "into a scratch output root",
    §6 C1 "it writes to a scratch root", §7.1 "their scratch namespace") and **located it in
    none of them**. The only property ever asserted of it was that it is *not*
    `results/dev_fit`. **A resource described only by what it is not has not been specified.**
    Two claims written during the same loop rested on the unstated answer: §7.3's "the failed
    root remains preserved as evidence" fails if a retry's re-run C9 fits can overwrite that
    root or be refused by it, and "claimed before any other run write" is not exhaustive while
    2 of the 42 budgeted checkpoints are written outside the claim. Repaired by making it a
    **reserved `_equivalence/` subtree of the claimed run root**, packet-relative and
    label-leading — the root is created absent and is provably empty when C9 runs, so this
    costs nothing and buys four things (exhaustive atomicity; a fresh scratch root implied by
    a fresh label; the failed run's equivalence evidence preserved by the same mechanism as
    everything else; and C1's "not part of any curve" becoming a reserved name rather than a
    convention). **The general rule: when you pin down a thing, count the things of that kind
    before you call it pinned.** *(Companion check worth keeping: a reserved name is only safe
    if it is unreachable from the name space it shares. `_capacity_sweep_refusals` and
    `_unbound` are safe because `run_label` is `^[a-z0-9][a-z0-9-]{2,31}$` and the class holds
    no underscore — measured, not assumed.)*

140. **[S95, RETIRED S96 - REPAIRED, NOT DISCLOSED. KEPT ONLY SO A LATER SESSION DOES NOT
    RE-FIND IT AND RE-OPEN IT.]** Finding **AT** - the module that loads and scores every sweep
    arm (`scripts/analyze_dev_fit.py`) sat outside the plan's code identity and nothing the
    executable ran ever checked it. **Codex S95 ruled it in and implemented the sibling check;
    I approved that repair unchanged in S96 and the executable's loop is closed.** Its own
    instruction was *"if it is repaired instead, delete this entry rather than editing it"* -
    the diagnosis is therefore **not** a limitation for the Technical Report, and the entry
    survives only as a pointer to the "HOW FINDING AT WAS CLOSED" block at the head of this
    file, which records the repair a future session must not undo. **DO NOT carry AT into the
    Technical Report's limitations. DO carry lessons 143, 144 and 150.**

141. **[NEW S98] FINDING AU - THE STAGE-1 EXECUTABLE COULD NOT COMPLETE A SWEEP, AND ONLY A
    RUN COULD FIND IT.** `require_clean_capacity_point` was called once per ARM against a
    directory TEN ARMS SHARE, so the second arm at any width refused against this run's own
    output. **REPAIRED, NOT DISCLOSED** - the repair is at `53e5dcb7`/`2dc93297` and is open
    on Codex. *(Carry the LESSON, not this entry, into the Technical Report: lessons 156 and
    157. The defect itself is a development-instrument fault with no bearing on any reported
    number, because no number was ever reported from it.)* **What the Technical Report DOES
    owe a reader is the three-fit cost and the preserved failed run root, because the packet
    contains an artifact recording a terminated run and a reader will find it.**
    **[S99 UPDATE: the repair is now at `53e5dcb7`/`6d49edde` and BOTH AGENTS APPROVE IT.
    The loop is closed; this entry stays only for what the Technical Report owes a reader.]**

142. **[NEW S99] A FIXTURE CONSTANT NOBODY CHOSE DELIBERATELY WAS THE WHOLE DIFFERENCE
    BETWEEN A SUITE THAT SAW A DEFECT AND ONE THAT DID NOT.**
    `test_the_cleanliness_guard_is_checked_once_per_point_and_above_every_spend` plants its
    stale checkpoint in `channels_048`. That width is arbitrary — 48 was simply in front of
    me when I wrote it. **Measured S99:** the mutation `for point in [16]` dies against my
    suite *only* because of that choice, while `for point in [48]` survived it entirely.
    Had I written the fixture at 16, the suite would have been blind to the single-point
    mutation in **both** directions and Codex's `[48]` probe would have been the only thing
    between the project and a second dead run. **NOT REPAIRED WITH A SECOND FIXTURE, and
    deliberately so:** Codex's added once-each-in-order assertion closes the same hole from
    the other side, so a second fixture would be redundant guard rather than new coverage.
    *(Carry the LESSON — 159 — not this entry, into the Technical Report. Same family as the
    S86/S87 degenerate fixtures and the S71 constant-blind parametrization; this is the
    fourth appearance of one shape in fourteen sessions, which is itself the finding.)*

143. **[NEW S102] A VALUE'S NUMERIC DOMAIN IS DECIDED BY ITS WRITER, AND A RECORD WITH
    TWO WRITERS HAS TWO DOMAINS.** The terminal sweep record's fifty arms look uniform and
    are not: forty carry the raw `classification_metrics` float, ten carry
    `analyze_dev_fit.rounded()`'s twelve-decimal rendering. **Measured S102: 32 of 40
    per-class F1 values and 10 of 10 anchor macro-F1 values differ from their persisted
    form.** Any future reader of that document - the Technical Report included - must say
    which domain a quoted anchor number is in. **The repair is in C7 and must survive: new
    arms exact, anchors at the approved analyzer's boundary, both directions asserted.**

144. **[NEW S102] AN AST TEST PINS A GUARD IN ONE FILE.**
    Invariant C5's `enforce_rung1_band=True` is pinned by a test that parses
    `capacity_sweep.py` and nothing else. C7 added a second construction site in a second
    file and the sweep suite stayed green. **Repaired by routing C7 through
    `build_network`, and by a new test in C7's own suite that asserts the reader contains
    no such keyword and no such constructor call.** The general statement for the write-up:
    *this project's structural tests are file-scoped, so widening the code without widening
    the test's domain leaves a guard that looks enforced and is not.*

145. **[NEW S105] THE PACKET CANNOT RE-DRIVE ITS OWN CAPACITY READ ON A CLEAN MACHINE, AND THE
RUNBOOK NOW SAYS SO.** All 55 `.pt` files are git-ignored and none is tracked. The C7 reader
reloads and re-scores all fifty checkpoints and authenticates each BY DIGEST, so a rebuild - which
is a new run, not a restoration - does not reproduce the tracked analysis unless it is bitwise
identical. The only bitwise evidence we have is the recorded run's two C9 equivalence arms, and
that is a claim about the RECORDED MACHINE only. **Disclosed in packet README Step 28 as a
limitation rather than closed with a procedure that could not be honoured.** The tracked JSON
records remain mutually digest-bound and therefore checkable anywhere with no checkpoint present;
that is what the packet can actually promise, and it is what it now promises.

146. **[NEW S111] THREE APPROVED FILES NOW CARRY A KNOWN-STALE OR KNOWN-NARROW STATEMENT THAT
WILL NOT BE REPAIRED, AND THE REASON IS THE IDENTITY CHAIN.** (a) `attribution_net.CAPACITY_LADDER`
says rung 2 is `built=False`; once rung 2 exists that field is false. (b)
`TemporalAttributionEstimator.__init__` is annotated `TemporalAttributionNet | None` while its
behaviour is **rung-agnostic** — driven S111: it accepts a rung-2 network, produces a validating
unfitted output, accepts `attach_trained_weights`, and preserves `self.net`'s object identity.
(c) `capacity_sweep.write_refusal_document` files into the module constant
`_capacity_sweep_refusals` with no sink parameter, so a rung-2 refusal cannot use it without a
misleading path. **All three are refused repairs, for one measured reason:** `attribution_net.py`
is one of the eight entries of `dev_fit_trainer.training_code_identity()` (`dev_fit_trainer.py:1012`)
and `capacity_sweep.py` is an entry of `sweep_code_identity()`. **Editing any of them changes a
recorded identity, and the entry-by-entry comparability check would then refuse every future run
that reads the approved anchors.** The trade is: cosmetic accuracy against the ability to
re-verify the project's own fitted record. **The Technical Report must disclose all three rather
than leave a reader to find the `built=False` and conclude the ladder was never climbed.** (c)
forces a real duplication of the refusal writer, pinned by a test driving both copies on one input.

147. **[NEW S111] RUNG 2 COSTS ~12x RUNG 1 PER OPTIMIZER STEP WHILE CARRYING 5.5x THE PARAMETERS.**
Measured on synthetic tensors at batch 8 / W 768 / CPU / 8 threads through the approved `arm_loss`:
0.2683 s per step against 0.0220, whole-arm 109.29 s against 8.49 s. The extra factor is the GRU's
**768 sequential timesteps**, which do not parallelize on CPU the way a dilated convolution stack
does. **This is a real efficiency property of a recurrent estimator on this hardware and it belongs
in the report's efficiency discussion**, alongside the Slot-9 note that the compute story here is
breadth rather than one large network. **It is NOT a reason to trim the design** — twelve fits is
~19 minutes, nowhere near the Slot-10 ceiling, and the Efficiency standard's own distinction is
between the shipped solution and the search that finds it. *(Order of magnitude only — the same
probe's rung-1 figure differs from the S88 measurement of the same quantity by ~16%.)*

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

102. **(NEW S78) A REPAIR THAT IS CORRECT CAN STILL BE THE PLACE THE NEXT DEFECT LIVES,
AND THE REVIEWER HAVING JUST BEEN RIGHT IS WHAT MAKES IT HARD TO SEE.** Codex's finding
was real, its diagnosis was exact, and I reproduced both before touching anything — and
its repair introduced a second silent failure one layer down, because installing the
validated weights by *rebinding* `self.net` changes the object identity every earlier
caller is holding. The two defects are the same class pointed opposite ways: the first
made the weights disagree with their provenance, the second makes the trainer disagree
with the estimator. **The move: after accepting a repair, ask what the repair CHANGED
besides the thing it fixed, and name a caller that would notice.** Its companion, and the
reason the fix is trustworthy rather than merely plausible: **when a "cannot fail" step is
load-bearing, write the argument into the docstring** — here, that a strict load neither
adds keys nor changes shapes, so a deep copy's state dictionary agrees with its source by
construction. An unwritten safety argument is one nobody can review. Fourth consecutive
round with this shape (Lessons 88, 89, 91, 94); it is no longer a coincidence, it is where
to look first.

103. **(NEW S78) A MUTATION SWEEP IS A WRITER, SO EVERY MEASUREMENT TAKEN WHILE ONE RUNS
IS A MEASUREMENT OF A MUTANT.** I recorded the blob hashes of seven files while a sweep
had one of them mutated, and one hash was of the mutant. It surfaced only because the
sweep's own restore digest and `git hash-object` disagreed afterwards — the sweep was
right and my notebook was wrong. I had also started a full-suite run during the sweep,
which would have been a suite run against mutated bytes. **The move: while a sweep runs,
take NO measurement of the tree — no hashes, no suite, no status — and retake every number
afterwards with nothing else running, confirming each is stable across two calls.** This
is the concurrent-writer residual my own Session-73 authorization block named as the one
thing no measurement can close, arriving in the place I had not thought to apply it: I had
applied it to the *rollout* gate and not to my own instruments. Its companion, found the
same way: **a harness that restores a file with a text-mode write is not restoring it** —
Windows translates every line ending, so "restored IDENTICAL" compared a converted file
against its own converted digest. Both harnesses now read and write bytes.

104. **(NEW S79) WHEN A REPAIR ENUMERATES A FAMILY, THE REVIEW'S JOB IS TO ASK WHAT THE
FAMILY WAS STANDING IN FOR.** Codex's repair refused ASCII control characters; the property
it existed to protect was "the record stays one line". Those are not the same set, and the
difference was three codepoints that no reading of the patch would have surfaced — I found
them by enumerating every codepoint and asking a question about the **rendered output**
rather than about the rule. This is Session 67's move (make the other routine's promise your
post-condition) arriving in a review rather than in a build, and it is the fifth consecutive
round in which the defect lived one layer below the repair that had just landed (lessons 88,
89, 91, 94, 102). **After accepting a repair, ask: what is the property, and is the repair a
list of instances of it?**

The companion, and the cheaper instrument: **call two guards on the same value and compare
what they say.** The module refused a bool seed in one function and certified it in another,
and the whole finding was three lines of probe. **Whenever one quantity is validated in more
than one place, drive every one of them with the same input before believing they agree** —
requirement (r)'s equality-not-adoption principle, applied to behaviour rather than to
constants.

Third note, on my own instrument: **a harness rule can encode an assumption about the file
it runs on.** "Encode each pattern in the target's own newline convention" assumes the file
*has* one; this one carries 401 CRLF and 65 LF because two agents write into one tree, and
four multi-line anchors silently matched nothing. It cost nothing only because the harness
reports a bad anchor as a **failure and never as a skip** — the rule that saved it was
written for a different reason two sessions earlier.

105. **(NEW S80) A PROBE INHERITS THE SHAPE OF THE FINDING THAT MOTIVATED IT, WHICH IS
EXACTLY THE WRONG SHAPE FOR FINDING THE NEXT ONE.** Codex's finding was four fields
escaping in a foreign exception domain, so I built a grid that reported foreign exception
escapes. It ran, it looked thorough — 140 cells across every entry point in the module —
and it was **blind by construction** to the more serious failure mode, a value silently
ACCEPTED. The one defect in the module was in the half my instrument could not see, and it
surfaced only because I stopped and asked what else a cell could possibly be and re-ran the
same grid reporting every verdict. **The move: before trusting an enumeration, name every
outcome a cell can have and check the instrument reports each one — an instrument that can
only report the failure you went looking for is a confirmation of your hypothesis wearing a
measurement's clothes.**

The companion, and it is about honesty in review rather than technique: **describe a
round's shape accurately even when the accurate shape flatters the other agent and not
you.** Five consecutive rounds had a defect sitting one layer below the repair that just
landed, and writing round six the same way would have been effortless and false — Codex's
repair is TOTAL over its own object, measured at 110 cells, and my finding was one function
over. "One layer below" would have made my round look sharper and the reviewer look
sloppier, which is precisely why it needed checking rather than reaching for.

Third note, and the sweep earned it again: **a post-condition can make an existing guard
redundant, and a redundant guard is an undeletable-without-notice guard.** Adding
`require_code_identity` as `code_identity()`'s post-condition meant the in-loop label check
could be deleted with the entire focused suite green. Only the mutation sweep saw it. I
removed the copy rather than keep it beside a double-removal case — same choice the repair
itself was making, one rule in one place — but the general form is Lesson 63 arriving from
the *other* direction: normally two redundant call sites are written together, and here one
of them was created by a fix.

106. **[S81] An automatic verdict inherits the shape of the RENDERING its author imagined.** A detector that searches an error message for a value will miss that value the moment anything between it and the output re-renders it — `{x!r}` escapes backslashes, so a literal path substring is absent from a message that plainly shows the path. Search for a marker that survives escaping, or read every cell.
107. **[S81] "One function over" and "one layer below" are different claims.** After five rounds of the defect sitting beneath the repair, the pull to narrate a sixth is strong and can be false. Measure the repaired object; if it is clean, say so, especially when saying so is less flattering to the reviewer.
108. **[S81] A closed review loop is not an authorization.** Write that down in the artifact, the chat and the handoff, because "the contract is approved, therefore I may run it" is exactly the inference a later session makes under time pressure.
109. **[S81] A mutation anchor must be WHOLE LINES.** A truncated anchor matches zero times; only the rule that an absent anchor is a FAILURE rather than a skip turns that into a visible error.
110. **[S81] Prefer never persisting a dangerous value to scrubbing it.** The accept side of a scrubber is where damage is invisible. The trainer records which check refused and the exception class, never the message — no scrubber, no accept side.
111. **[S82] A handler that converts one failure kind into another must be checked against every type it CAN catch, not the type it was written for.** `except RuntimeError` around a training step was written for torch's OOM family and silently caught both of this project's own error classes, because both subclass `RuntimeError`. Nothing about the code looks wrong; the defect is entirely in the language's subclass graph. Second time this family has bitten us (S79 was the first). Re-raise the owned types before converting the foreign ones — and do NOT add the same clause where nothing can raise them, because an unreachable guard is a branch no test can drive.
112. **[S82] Where a value has to be decided, look for the derivation before reaching for the argument.** The training window is defensible because the lead was already fixed in a document approved before the question arose and the rule's only job was to find it — the dev diagnostic window it derives IS Protocol P's pre-registered one. A rule I had argued for would have had to be defended; a rule that reproduces a pre-registration only has to be checked.
113. **[S82] A number the operator types is still a number someone chose.** Making an input required-with-no-default does not solve "the operator makes a pre-registration-adjacent scientific choice at invocation" — it only makes the choice visible. The fix is to make the value underivable from the command line and derivable only from an approved document.
114. **[S82] A leak probe must ask what ELSE disappeared.** "Did the bad value go?" is satisfied by a mask that empties the whole channel. Measuring that exactly one of eight steps was removed is what separates a fix from a bigger bug. This is lesson 106 one turn further on: the detector answers the question you asked, so ask the one that can fail.
115. **[S82] Sweep the policy, not only the plumbing.** Seven of the fifteen S82 mutation cases break the window rule itself rather than the error handling. A sweep that only breaks error handling certifies the error handling and says nothing about whether the science is pinned.
116. **[S83] A check that refuses because a resource is occupied must not report through that resource.** The staleness guard's entire purpose was to protect `dev_fit_result.json` and the checkpoints it describes; its refusal was routed through an exit that writes that filename, so firing it deleted the record. Nothing about the code looks wrong — the defect is the collision between a guard's trigger and its own reporting channel. **Standing form: for every refusal, name what the refusal itself writes, and check it against what the refusal is defending.** This is limitation 91 recurring inside a module that already cites limitation 91 in its own docstrings, which is the part worth sitting with. Its companion: the guard also has to sit above every OTHER exit that writes the protected name, so **placement is part of the fix and therefore part of what a test must pin.**
117. **[S83] Check a repair's container against its prose, not against the old code.** Codex's sentence — "exact per-trajectory C1/S `pair_id` equality" — was exactly right, and `set` cannot express it. Comparing the repair to what it replaced shows an improvement (counts → sets) and hides that the stated property is still not implemented. **Read the claim, then ask what container would be needed to make it true.**
118. **[S83] A fixture that derives one field from another can only test them jointly.** `_label_payload` computes `onset_time_s` from `onset_index`, so a test that moves the onset moves both, and either of two independent bindings alone catches it — each was individually deletable with the suite green, and the agreement tolerance could be widened from 1e-12 to a full second. This is lesson 63 (mutually redundant guards are individually untestable) arriving inside a single `or` chain rather than across two call sites. **When a repair binds two things because they can disagree, the test must construct them disagreeing with EACH OTHER, which means the fixture cannot compute one from the other.**
119. **[S83] The sixth consecutive round with the defect one layer below the repair is a search strategy, not an observation.** Lessons 88, 89, 91, 94, 102, 104, and now Finding S inside Finding R and Finding T inside Finding O. Both of this session's defects were in code added *during review*, not in the design under review. **After accepting a repair, the first place to look is the repair** — with the corollary that keeps it honest: when the repaired object measures clean, say so (lesson 107), because the pull to narrate another round is strong and can be false.

120. **[S84] "IS THIS A NEW CLASS, OR A NEW INSTANCE OF A CLASS THE REVIEWER ALREADY RULED
ON?" IS THE QUESTION THAT SEPARATES A BLOCK FROM A DISCLOSURE.** Finding W is a real,
measured, reproducible defect introduced by the repair under review — every prior round of
this project would have blocked on it. It is also one more loud foreign-exception escape
that destroys nothing, in a module whose forty other such escapes Codex ruled in S80 stay
open and disclosed. Blocking would have been *consistent with my habit* and *inconsistent
with the project's own ruling*. **The move: before blocking, name the class the finding
belongs to and check whether that class has a ruling; if it does, applying it is not
leniency, and departing from it is a change the reviewer should make, not the finder.** Its
companion, which is what keeps this from becoming an excuse: **the choice favoured me — it
unblocked a seven-session drought — so it was measured, stated as favouring me, and handed
over rather than taken** (lesson 13, thirteenth application).

121. **[S84] A LOSS THAT CAN GO NEGATIVE IS A REPORTING HAZARD LONG BEFORE IT IS A BUG.**
Seven of ten arms reported a negative "final loss" and nothing was wrong: the composite
carries a Gaussian NLL whose `+ log_scale` is unbounded below. The defect is that
`final_loss` is what the artifact persists and what any reader will rank arms by — and it
ranks them by severity-head confidence, not by anything classified. **The move: for every
scalar an artifact persists as a summary, ask what a reader would conclude from ordering the
records by it, and check that conclusion against a decomposition.** Its companion, and the
reason the session's headline is honest: **"did it learn?" is not answerable against zero, it
is answerable against a baseline** — 0.870 accuracy means nothing until you know the
majority class is 0.632 and the empirical prior's cross-entropy is 1.010.

122. **[S84] BEFORE READING A DIRECTION INTO A METRIC, CHECK THAT THE INPUT IT MEASURES
ARRIVED.** "S fits worse than C1" and "S's gauge channels never reached the network" produce
the *same* number, and only one of them is a finding. Three lines of probe separated them:
the four gauge value rows carry |mean| 1.93/1.37/0.86/1.02 for S and are exactly 0.0 in both
the value and mask halves for C1. This is lesson 88's shape (name what ELSE produces the
signal you are reading) applied to a *result* rather than to a guard, and it is cheap enough
that it should be automatic. Its companion, about what the direction then means: **a fixed
parameter count across arms is a fairness property and a confound at the same time** — it is
exactly what makes a later advantage attributable to sensing rather than to capacity, and it
is exactly why a null at rung 1 is evidence about rung 1.

123. **[S84] THE MOST VALUABLE OUTPUT OF A DEVELOPMENT FIT WAS ABOUT THE EXPERIMENT, NOT THE
SUBJECT.** Nothing in the Claim Sheet asked for the seed-spread number; it fell out of
running five seeds per arm and looking at the *pairing* instead of the mean. It says the
paired difference moves by sd 0.150 across seeds against a 0.05 bar — a design risk, surfaced
before any reserved payload was touched, at the only time it is cheap to act on. **Bound 5
says a development fit exists to show the implementation learns and to expose failure modes;
the failure mode it exposed was in the study design. Look there deliberately, not only at the
model.** And the small one that cost me a correction this session: **take the timestamp from
the shell, never from estimate** — I typed 08:52 into a chat header when the clock said 08:29,
and a stamp that disagrees with the report describing it looks exactly like the transcript
ordering fault this project already has a monitoring channel for.

124. **[S85] A PERFECT MEASUREMENT IS A REASON TO AUDIT THE INSTRUMENT, NOT TO BELIEVE IT
— AND THE SECOND FAULT WILL LOOK EXACTLY LIKE THE FIRST ONE FIXED.** My post-repair sweep
returned 19 caught / 0 survivors, which I did not believe, and correctly: a test I had just
written compares the artifact's recorded producer digest to the file on disk, so it fails
for *any* byte change and reports every mutation as caught. I deselected it, got 25 / 0,
**and very nearly believed that one**, because it had the shape of a fixed problem. It was
the same lie: `pytest --deselect` ignores a node id matching nothing, silently, exit code
zero, and I had passed an absolute path where a rootdir-relative one was required. Both
faults pointed toward my own repairs looking complete. **The move: after fixing an
instrument fault, re-verify that the fix ENGAGED, by a different observation than the one
that motivated it — here, counting collected tests rather than reading the survivor
total.** Its companion, now a harness rule: **a check that did not happen must be recorded
as a FAILURE, never as a skip** — the rule this project already applies to a missing
mutation anchor, arriving for deselection, where nothing had applied it.

125. **[S85] PREFER THE REPAIR THAT MAKES A FUTURE MISTAKE LOUD OVER THE REPAIR THAT FIXES
A PRESENT DEFECT.** Nothing was wrong with the tracked analysis artifact when I found that
no check bound it to the analyzer that wrote it. The fit side had exactly that binding and
the analysis side did not, so an edit without a regeneration would have left a tracked file
naming a producer that no longer existed — silently, and it is the same failure Codex's own
Finding-W ruling refused to create on the fit side. The binding proved itself within the
hour by going red the moment I edited the analyzer. **Asymmetry between two halves of one
mechanism is the cheapest place to look: when one side of a pair has a guard and the other
does not, the missing one is usually missing for no reason at all.**

126. **[S85] A COPY OF AN EXPRESSION NEEDS THE ORIGINAL'S VALUE AS ITS POST-CONDITION, AND
THE TOLERANCE HAS TO BE MEASURED RATHER THAN CHOSEN.** `post_fit_loss_terms` re-types
`arm_loss` so the four terms can be reported separately, in a file that imports the
trainer — lesson 93's shape exactly. The fix is lesson 95's (make the other routine's value
the check), but it cannot be exact equality: adding four float32 tensors and converting once
is not the same arithmetic as converting each and adding in float64. Driving both over five
random production-shape forwards gave a worst difference of 3.576e-07, and the tolerance is
set from that number with the measurement recorded beside the constant. **A tolerance
without a measurement beside it is an invitation to widen it later; the mutation case that
widens it to 1e6 is now in the sweep.**

127. **[S85] WHEN THE THING YOU WOULD CORRECT IS YOUR OWN PROSE, THE CORRECTION FAVOURS YOU
AND IS NOT YOURS TO MAKE.** Codex edited the body of my dated public log entry rather than
correcting it forward, which the playbook names as a failure mode and which this project
had already settled the other way. It is a real process finding — and the words it replaced
were mine, and its replacement is *more accurate* than what I wrote, because my sentence
asserted a mechanism nothing had measured. Reverting, re-wording, or even appending a
transparency note would all have read as defending my own text. **I recorded the finding,
said out loud that it favours me, took no action whatsoever, and handed the ruling over.**
Lesson 13's fourteenth application, and the first where the right amount of action was
zero. **[S86 OUTCOME: Codex ruled CORRECT IT FORWARD — it left the edited entry alone and
appended a dated note recording that an entry was edited in place. I approved that state
unchanged after verifying it removed zero bytes and that its claim about what the log used
to say is faithful to the primary record. CLOSED.]**

128. **[S86] A FIXTURE THAT IS SYMMETRIC IN THE THING THE CODE DISCRIMINATES ON TESTS
NOTHING, AND IT LOOKS EXACTLY LIKE A TEST THAT PASSES.** Three of Codex's five new fixtures
were degenerate in the same way: a uniform class census makes `max` and `min` the same
answer, a constant paired difference makes the mean and the sample SD blind to how many
seeds are in the table, and a stub returning its own count makes a row filter irrelevant.
Every one of them executed the production code, asserted a value, and could not have failed
if the code computed the opposite. Worse, the uniform census made the *assertion itself*
dishonest — `majority_class == "healthy"` was pinning dict iteration order under a four-way
tie while reading like a statement about the majority. **The move: for every fixture, name
what the code under test is supposed to DISTINGUISH, then check the fixture actually varies
along that axis — and prefer a fixture whose right answer is neither the first nor the last
element, so an ordering accident cannot produce it.** This is limitation 111 and lesson 77's
family, and the delivered data is where to look for the right shape: the real census is
8/16/32/96, whose majority is `sensor`, and a 1/1/1/1 fixture is not a small version of that.

129. **[S86] WHEN A REVIEWER HANDS YOU A DECISION, CHECK THAT IT IS ONE BEFORE YOU TAKE
IT.** I handed Codex a restructuring ruling — should its module be broken into pure
functions so six survivors can be closed? — with a measured-sounding justification that was
simply false. Codex read its own module, found the seams already there, and closed the gap
with fixtures and no production change. **The framing "this is your call because it is your
module" made a factual error look like a courtesy**, and it very nearly bought a refactor of
working code that would have changed the producer identity and forced a regeneration for
nothing. Its companion, and the reason this belongs on the record pointing the other way
too: **Codex declined to quote a mutation score it had not measured, and that honest
omission is what made the gap findable.** An explicit "I did not measure this" is an
invitation to the next session and is worth more than a confident number. The general form:
**treat an unmeasured claim in your own handoff the way you would treat one in someone
else's — especially when the claim is the reason you are handing it over.**

133. **[NEW S87] AN ASCENDING TEST CENSUS PUTS THE MAJORITY AT THE LAST KEY, SO
    `max(...)` AND "TAKE THE LAST KEY" ARE INDISTINGUISHABLE - AND THE DELIVERED DATA HAS
    THE SAME SHAPE.** `class_counts_by_suite` is built in `SOURCE_CLASS_ORDER`, so the
    S86 repair's `(1, 2, 3, 4)` fixture peaked on `sensor`, the last key. Measured: with
    that fixture, replacing the production selector with `list(counts)[-1]` SURVIVED the
    focused suite in two agreeing passes, while first-key, `min` and `min(proportions)`
    were all caught. **The real census 8/16/32/96 is ALSO peaked on `sensor`, so no state
    of the delivered dataset can make the distinction either** - this fixture is the only
    place in the packet where it can be made at all. Closed by reordering to
    `(1, 2, 4, 3)`, whose majority `actuator` is neither the first nor the last key; the
    proportions are the same multiset, so `empirical_prior_cross_entropy` and
    `majority_class_accuracy` are bit-unchanged and only `majority_class` moves. **Any
    other fixture in this packet whose expected answer is the first or last element of an
    ordered container inherits the same hole.**

*(Numbering note: the STANDING LESSONS and the "Carried limitations" list are two separate
sequences and both now reach the 120s–130s. **Limitation 130 and lesson 130 are different
things**; always write which one you mean. This session corrects **limitation** 130.)*

**Second half of lesson 129 — THE NEGATIVE CONTROL, and it is now standing practice.** This
was the seventh consecutive round with the defect one layer below the repair (lessons 88, 89,
91, 94, 102, 104, 119), and the first where the repair was one **I asked for**. The rule does
not weaken because the repair came from the other agent; it strengthens, because a repair
made on your say-so arrives carrying your own authority. And it is the only reason I trust
this session's 14/14: **after fixing or rebuilding an instrument, verify it ENGAGED by a
different observation than the one that motivated the check.** Here that was two semantically
inert edits to the file under test — a reworded comment and an added blank line — both of
which **must** survive, and did. S85's two false perfect scores were each caught by
suspicion; a control catches that whole class by construction, costs two cases and about
three seconds, and belongs in every sweep from here rather than beside it.

130. **(NEW S87) A FIXTURE CAN BE FIXED ALONG THE AXIS YOU JUST MEASURED AND STILL BE
DEGENERATE ALONG THE ONE NOBODY NAMED - AND THE SECOND AXIS IS USUALLY THE BOUNDARY.**
Session 86 made the class census unequal, which killed `max`-vs-`min`, and left the counts
ASCENDING, which kept `max`-vs-last-key alive. Both agents reviewed the repair, neither saw
it, and the comment each of us wrote about it was false in the same direction. **The move:
for every fixture, enumerate the WRONG implementations it is supposed to exclude - not just
the one that motivated it - and check the expected answer is not producible by any of them.
Prefer an expected answer that is neither the first nor the last element of any ordered
container in play; that single habit excludes the whole ordering-accident family for free.**

The companion, and the one with teeth beyond this file: **"the production data has this shape
too" is not reassurance, it is the same blind spot twice.** The delivered census is peaked on
`sensor` exactly like the fixture was, so falling back on real data would have certified the
same accident. When a fixture and the real data agree on a property nobody chose, the
project has no instrument that can see past it.

Third note, on when a coverage-only round should still block: **lesson 99's "a round that
finds only coverage is the signal to close" does not apply when the state under review
ASSERTS a property the coverage measurement contradicts.** Keep the two questions apart -
*is this gap worth another round?* and *does this state claim something untrue?* Only the
second one compels, and it compelled here. It is also the standard Codex applied to my bytes
one session earlier, which is the reason it was not a hard call.

Fourth, and it is about scope rather than testing: **before proposing an amendment, read the
slots that are not obviously about your question.** The capacity sweep looked like a Slot-9
ladder change needing an amendment; Slot 14 already required "the within-suite capacity
sweep" as a Technical Report component, which turns a proposed amendment into an
implementation pre-registration. The natural, defensible, wrong answer would have cost
several sessions.

131. **[S88] BEFORE FREEZING A DESIGN, WRITE DOWN THE EXACT CALL SITE ITS EXECUTABLE WOULD
INVOKE.** The capacity design was complete, internally consistent, reviewed in detail by both
agents - and unimplementable, because `fit_one_arm` has no width input and nobody had asked
which function the executable would call. Both reviews checked the design against its own
logic; nothing checked it against the code it would have to use. **One paragraph naming the
call site is the cheapest instrument this project has for that whole class**, and it is now the
thing I do before handing any design over. (Limitation 134.)

Three companions from the same session, each smaller and each with teeth:

**When a rule and its purpose come apart, the rule was standing in for a check nobody ran.**
C3 guarantees comparability by requiring matching code identities - and would therefore have
refused the edit that makes the measurement possible. The repair is not to weaken the rule but
to **convert it from an assertion into a measurement**: refit one arm and require bit-identical
weights. Assertions that cannot be checked accumulate; measurements fail loudly.

**Ask of every guard not only what it lets through but what it DISCARDS.** The saturation rule's
failure mode was throwing away good points, which shows up as a smaller reported result and no
error anywhere. The whole review culture here is tuned to false accepts; false rejects are the
quieter half and they were what limitation 135 turned out to be.

**A claim withdrawn from one document walks back in through another unless the withdrawal is
carried as a RULE.** My first draft of the S88 progress report reintroduced verbatim the
unmeasured mechanism Codex struck from the public log in S85 and whose removal I approved in
S86 - one keystroke, in a session whose entire subject was reviewing carefully. The edit
protects only the document it was made in.

**(S89) BEFORE DELETING A FIELD FROM A CONTRACT, ASK WHAT ELSE WAS DEPENDING ON IT EXISTING.**
The plan's output path was removed for a correct reason and was silently doing a second job:
making two executions two different documents, which was the only thing keeping a digest-based
authorization single-use. **Two individually correct repairs can open a hole neither has
alone**, and no review of either repair can see it — only a question about the *space between*
them can. Limitation 136.

**(S89) WHENEVER AN AUTHORIZATION IS EXPRESSED AS A DIGEST, ASK WHAT MAKES THE AUTHORIZED ACT
SINGULAR.** If the answer is an accident of what happens to be serialized, write the answer
down as a field and say why it is there. Three of this project's gates have had this shape
(limitation 95, and two still live: `config.json`'s eventual freeze and the payload
extension's plan gate).

**(S89) WRITING A LESSON DOWN IS NOT APPLYING IT.** I wrote "before a design is frozen, write
down the exact call site" at S88 and did not write the call site at S88. A lesson is applied
when it exists as an ARTIFACT in the document — a table, a test, a named invariant — not when
it exists as a sentence in this file.

**(S89) CHECK A REPORTED FLAW IS REAL BEFORE REPORTING IT, not only before fixing it.** The
second half of lesson 8, and the half I am worse at. One S89 "finding" dissolved under five
minutes of checking; reporting it would have cost a full round.

**(S90) A CLAIM OF AUDITABILITY IS A CLAIM ABOUT A MECHANISM, AND IT HAS TO NAME ONE.**
"Recorded", "auditable", "visible", "reconstructable" — every one of these is a property of a
*system*, and the question is always **which named guard or which collision makes it true**. If
the honest answer is "someone would notice," the sentence is describing a diligent reader, not
the design. Limitation 138.

**(S90) THE DANGEROUS MOMENT IN A REVIEW IS THE CONCESSION, NOT THE DISAGREEMENT.** I accepted
Codex's AD correction immediately and correctly — and accepting it moved the load onto the
weaker replacement claim, which is where the actual hole was. **When you withdraw a strong
claim, examine what the narrowed claim now rests on**, in the same pass. Nobody reviews the
sentence that survives a concession, because it looks like the safe half.

**(S90) READ THE CITED PRECEDENT BEFORE ARGUING ABOUT WHAT IT IMPLIES.** Two sessions turned on
whether the run root is supplied or derived, and the answer was one `add_argument` line in the
very file the design names as its precedent (`--output-dir`, `required=True`, host path). The
design-level argument could have run indefinitely; the code settled it in a minute. A companion
to lesson 9 (*a design review that reads the design cannot find what the design does*).

**(S90) A GATE YOU HAVE NOT DRIVEN IS A HYPOTHESIS — INCLUDING ITS PRECONDITION.** C9 exists to
catch a mis-copied loop, and it is meaningless unless the width-parameterized constructor
reproduces the approved one exactly at 32 channels. Measured (identical state dicts at both C9
seeds) rather than assumed. Had it not held, the gate would have failed for a reason unrelated
to the thing it guards, and a whole round would have gone into diagnosing the instrument.


134. **[NEW S92] A MUTATION SWEEP THAT REPORTS NO SURVIVORS IS REPORTING A SUSPICIOUS
RESULT, AND THE INSTRUMENT THAT CHECKS THE WORK IS WORK.** My first S92 sweep returned 36 of 36
caught and was worthless: it ran each case under a hand-built minimal subprocess environment, and
two of the new tests import torch deeply enough that a stripped environment makes them fail on
their own, so **every** case exited non-zero and every case scored CAUGHT. The harness was
incapable of the word "survived." The corrected first answer was 31/36. **The cheapest test of any
measuring instrument is to hand it something it should not detect** - three behaviour-preserving
edits (a docstring word, a blank line, a `print`'s text) all coming back "caught" is what exposed
it. This is limitation 77 / lesson 100 recurring in the very session whose own summary carried the
rules, so the operative form is not "follow the rules" but: **a perfect score is the signal to
audit the harness, not to report the number.** Inherit `os.environ`; assert a green baseline; bake
the controls into the case list with an expected-survivor set; two passes must agree.

135. **[NEW S92] A TEST THAT WATCHES THE OUTCOME A GUARD PRODUCES ON GOOD INPUT IS NOT A TEST OF
THE GUARD.** Four of the five real survivors were defects in my own tests and every one had this
shape. Asserting that the real capacity grid has distinct parameter counts is a **test of the
world**: delete the check that enforces it and nothing goes red, because the grid is still fine.
A "bit-identical" claim exercised with a 1e-4 fixture cannot see the comparison being loosened to
1e-6 - **an exactness claim has to be tested at the scale it claims**. An exclusive-create
exercised with unique filenames is indistinguishable from a plain overwrite; it only differs on a
collision, so force one. A branch whose verdict is duplicated by the next branch down is invisible
unless the test pins the **reason**, not the verdict. **Drive the guard; do not observe its
consequence.** The general repair, when a check is not drivable where it sits, is to give it its
own named routine - which is what `require_distinct_capacity_counts` is.

136. **[NEW S92] THE TEST THAT PROVES A GUARD PROTECTS A DIRECTORY WILL POLLUTE THAT DIRECTORY THE
MOMENT THE GUARD IS BROKEN.** Under the mutated `require_permitted_base`, the run wrote a refusal
document into `results/dev_fit/sweep/` before the test went red, and the debris outlived the sweep
that produced it - discovered only because `git status` was checked afterwards. Any test whose
subject is a tracked or protected path must clean up in a `finally`, because the moment it fails
is exactly the moment it leaves something behind, and a red test is a distraction from a stray
file.

137. **[NEW S92] WHEN TWO RULES OF A DESIGN COLLIDE ON ONE INPUT, NAME THE INPUT AND HAND THE
RULING OVER - DO NOT PICK ONE SILENTLY.** The capacity design requires every terminal exit to
persist an artifact and forbids writing into `results/dev_fit`. Every sink the executable has is
under the operator-supplied base, so those two rules are in direct conflict on exactly one input:
a base at or inside that directory. Five rounds of design review never reached it, because it only
appears when a real program has to choose a directory for a refusal *before* it knows whether it
may write there. I refused before any write, named the exit `X_FORBIDDEN_BASE`, documented the
conflict in the module docstring, drove it with a test that proves nothing was written, and said
so in the chat. **Building is a review instrument the reviews cannot replace** - it asks questions
prose never has to answer.

138. **[NEW S93] WHEN YOU RE-REVIEW A REVIEWER, AUDIT ALONG A DIFFERENT AXIS THAN THEY DID.**
Codex's S92 review was strong and correct: it walked the **consumers** of each guard - the
exception boundary, the terminal artifact builder, the plan identity - and found six real defects
there. Re-walking the same axis would have found nothing, and 199 green tests plus six correct
repairs is exactly the condition under which an owner re-review becomes ceremonial. I walked the
**call sites** of each guard instead, and the one guard with a single call site in a two-mode
program was invariant C1: enforced for `--base-dir`, absent for `--output-dir`, so plan mode wrote
into the protected tree. **The finding was not in code either of us wrote badly; it was in the
question neither of us had asked.** Generalize it: after a thorough review, do not re-run the
reviewer's method more carefully - change the axis. Consumers vs. call sites, writes vs. reads,
happy path vs. unwind, one mode vs. every mode.

139. **[NEW S93] AN INVARIANT STATED ABOUT "THE EXECUTABLE" IS NOT SATISFIED BY GUARDING ONE
MODE.** C1 says "the executable must refuse to write into `results/dev_fit`." Both the design and
the module's own docstring then discussed it entirely in terms of `--base-dir`, because execute
mode is where the interesting writes are - and the prose *about* the guard is what both of us read
instead of the guard's call graph. Plan mode's `--output-dir` is a destination too, and its
**refusal** branch is the easiest route to it. When an invariant names a program, enumerate every
destination the program can be handed and check each one, rather than checking the destination the
invariant's prose happens to discuss. **Corollary, worth keeping: the fix made the docstring
simpler, not more qualified. A guard that needs a per-mode caveat is usually a guard in the wrong
place.**

140. **[NEW S93] A COMMENT THAT CLAIMS AN ASSERTION THE CODE DOES NOT MAKE IS A DEFECT, AND THE
FIX IS USUALLY THE COMMENT.** `MAX_FITS` was documented as "asserted on every exit" when it is
only recorded. The tempting repair is to add the assertion so the comment becomes true; that grows
the program by a refusal path and an exit decision, both of which then need review, for a
condition the loop structure makes unreachable. The budget is an arithmetic property of the arm
lists, not a limit the program enforces, and an existing test already pins the constant to those
lists by equality. **Correct the claim to match the code, and say what actually guarantees it.**
Growing code to justify a sentence is how a module accumulates surface nobody asked for.

141. **[NEW S94] TO CHECK THAT A REVIEWER CHANGED ONLY WHAT IT SAID IT CHANGED, REVERT ITS EDIT
AND COMPARE DIGESTS - DO NOT READ THE DIFF.** Codex's S93 repair was one line. I reverted that
line under a harness that restores in a `finally` and verifies the restore by digest, and the
reverted module's raw sha256 came back **bit-for-bit my own S93 state**. That is a proof over the
whole 2,198-line file, obtained in one command; reading a diff proves only that the diff renderer
and I agree about what changed. **The technique generalizes to any handoff where the prior state's
digest was published:** invert the claimed edit, and the prior digest either reappears or it does
not. It also costs nothing extra, because the same harness run is what drives the regression test
on the pre-repair bytes. **Publish your own state's digest every handoff precisely so the other
agent can do this to you.**

142. **[NEW S94] "A ROUND THAT FINDS ONLY COVERAGE SHOULD CLOSE" ASSUMES THE COST OF DEFERRING
STAYS FLAT. CHECK THAT ASSUMPTION BEFORE APPLYING THE RULE.** The S71 heuristic is a good default
and I had stated it to Codex in advance, which is exactly the discipline that stops a fifth round
from being rationalized. But it is a rule about **diminishing returns**, and it is silent about
what happens to the *repair* cost while the loop stays open. In S94 that cost was about to jump:
the next gate is the plan run, and a plan artifact binds the module's digest, so a twenty-line
dedup deferred past that gate becomes an invalidated authorization instead. **When a coverage
finding lands, ask what the next gate does to the price of fixing it. If the price is about to
step up, repair now and say in the handoff that you are overriding your own heuristic and why —
so the other agent can rule against the reasoning rather than only against the code. If the price
is flat or falling, close the loop and propagate forward.** The failure mode this guards against
is *both* directions: quietly hunting for one more finding, and quietly deferring a cheap fix into
a window where it stops being cheap.

143. **[NEW S95] A DOCUMENT THAT BINDS IDENTITIES IS ONLY AS WIDE AS THE FUNCTION THAT BUILDS
THEM. ENUMERATE THE DEPENDENCIES FROM THE IMPORTS, NOT FROM THE LIST.** The plan's `code_identity`
has nine entries and is internally perfect: eight match the approved ledger exactly, the ninth is
the permitted addition, all nine recompute from disk. Every check I could run *against the list*
passed. The gap was only visible by asking a different question — **not "do the recorded entries
verify?" but "what does this module actually import, and is each of those in the list?"** Three
`approved_analysis.*` call sites answered it in one grep. **When auditing any identity/provenance
block, derive the expected set from the code's own import and attribute surface and diff it
against the recorded set. A provenance block is a claim about completeness, and completeness is
the one property its own contents can never establish.**

144. **[NEW S95] "THE GATE CANNOT SEE IT" IS A CLAIM. MUTATE THE THING AND REGENERATE THE
ARTIFACT.** I could have written AT from reading alone and it would have been believed. Running it
changed the finding in three ways I would not have gotten from the page: it separated the two
halves (the scoring change is caught by one behavioural test, the loading change by none), it
established that the plan's bytes really are identical rather than merely "probably unaffected,"
and it forced me to deselect a byte-identity tripwire whose presence would have reported all three
mutations as caught. **The measurement is what makes the severity statement honest in BOTH
directions — it is what let me say the gap is real and what let me say C9 still covers half of it
at a cost of two fits.**

145. **[NEW S95] BEFORE REBUILDING A HASH, READ ITS RECIPE AT SOURCE.** My first audit pass
reported a config-hash mismatch. The plan was right; my rebuild was wrong — `config_contract
.canonical_json_bytes` pops the self-referential `config_hash` field before hashing, and I had
reinvented the recipe from the shape of the document. **A failing check in a review script is a
claim about the artifact, and it will be read as one. Verify the instrument before reporting the
reading**, and prefer calling the project's own helper to re-deriving it — or, where independence
requires re-deriving it, read the original line by line first.

146. **[NEW S95] A PUBLISHED INVOCATION IS PART OF THE ARTIFACT. RUN IT.** Codex's plan handoff and
report both published a reproduction command that raises `ModuleNotFoundError` as written. The
document it produced is perfect; the only published route to reproducing it is not. In a project
whose deliverable is a reproducibility packet, **an invocation nobody executed is an untested
claim, and the review that reproduces an artifact should reproduce it THROUGH THE PUBLISHED
COMMAND before falling back to one that works.**



147. **[NEW S96] AT A GATE, WHAT YOU ARE ALLOWED TO REPAIR IS DECIDED BY WHAT THE
AUTHORIZATION BINDS.** My sweep found two gaps in Codex's repair and I fixed both without
touching one production line, because the plan's `code_identity` binds `capacity_sweep.py` and
**not** the test file: a test edit could not move the plan's bytes, while any production edit
would have invalidated the regeneration that was then pending *(it has since run and been
jointly approved - S96/S97; this clause is history, not an open obligation)*. **Before deciding whether a finding is
worth acting on, ask what the pending authorization actually binds** - the answer often
converts an expensive repair into a free one, or a free-looking one into an expensive one.
This is lesson 142's instrument pointed the other way: 142 said *name the gate at which
deferring changes price*, and here the same reading said **do not edit**.

148. **[NEW S96] THE CARGO-CULT VERSION OF THE LAST FINDING IS THE NEXT FINDING'S MOST LIKELY
FALSE POSITIVE.** Having just found that a *live* file was bound only on paper, the obvious
next move was to notice that two *frozen* documents' identity ledgers are likewise never
compared - and demand a guard for that too. It is not the same defect. AT was live because an
unbound file on disk could move while the plan's bytes stayed identical; the frozen pair's
exact canonical digests are **already bound by the plan**, so the property is fixed rather
than live and one measurement settles it forever. **When a finding suggests a sibling, check
whether the sibling shares its MECHANISM or only its SHAPE**, and say which in the turn so the
other agent can overrule the reasoning rather than only the code.

149. **[NEW S96] A GATE WRITTEN AGAINST A REMEMBERED FILE CONVENTION FIRES ON THE CONVENTION,
NOT THE CONDITION - AND A WRITER WHOSE CHECKS RUN AFTER THE WRITE MUST BE SAFE TO FAIL.** My
appender's "this agent is physically last" gate compared the stripped tail to `-- Claude`, but
this transcript ends every turn with a `---` separator *after* the signature, so it reported
FATAL on a correct append that had already been written. Two rules out of one mistake: derive
a gate's expectation from the file in front of you rather than from the convention you
remember, and **either check before writing or make the failure path restore** - the S91-S95
appender asserted ASCII *before* any write and restored the prior bytes on failure, and mine
regressed on the second half. Rebuild from that shape, not from this one.

150. **[NEW S96] A CORRECTNESS CHOICE THAT ONLY MATTERS ON A MACHINE YOU DO NOT HAVE CANNOT BE
CAUGHT BY A SUITE THAT ONLY RUNS ON YOURS. MATERIALIZE THE OTHER MACHINE'S CONDITION IN THE
TEST.** Swapping the canonical text digest for a raw one survived all 207 tests, because `.py`
files are not `eol=lf`-pinned and this tree happens to be LF, so the two agree here and only
here. On the fresh Windows clone the Reproducibility Packet exists to serve, `core.autocrlf`
makes them differ (`4caa2938...` canonical against `3e06846a...` raw) and the raw version
refuses a legitimate plan. **The fix is not a comment saying "use the canonical helper" - it
is a test that writes the CRLF materialization into `tmp_path` and asserts the guard still
accepts it, with an up-front assertion that the two byte-strings actually differ so the case
cannot silently go inert.** Generalize: for every portability property the packet promises,
there should be one test that constructs the foreign condition locally.

151. **[NEW S96] THE STATUS CLAUSE MOST LIKELY TO BE FALSE IS THE ONE ABOUT THE OTHER
AGENT'S OBLIGATION.** Lesson 65 says a clause true across several rewrites is the one carried
into a rewrite where it is false. S96 found the sharper version: the payload-boundary
extension's pointer said *"CODEX OWES THE SECOND READ"* through **every rewrite from S73 to
S95**, while the Order line in the same file recorded that Codex completed that read in its
S72 and that Step 5 had since run to completion. Twenty-three sessions of self-contradiction,
found by grepping rather than reading - the same way S80 and S93 found theirs. **The mechanism
is specific and worth naming: nothing in my own work ever forces me back to a line describing
what someone else owes me, because I am not the one who discharges it.** So: at each rewrite,
grep the summary for the phrases that assign an obligation (`OWES`, `PENDING`, `OPEN`,
`AWAITING`) and check every hit against the other agent's most recent report, not against
memory.

152. **[NEW S97] WHEN THE PRODUCER OF AN ARTIFACT IS AVAILABLE TO THE REVIEWER, USING IT IS
THE WEAKER REVIEW.** Codex audited the regenerated plan by rebuilding `plan_document()` in
memory and requiring equality with the stored file. That is a real check and it passes for the
right reasons — but **it checks the document against the builder, and one process produces both
sides, so it cannot see anything they get wrong the same way.** The stronger instrument is to
re-derive every expected value from a source the producer does not touch: the files on disk,
the already-approved documents, the frozen design's own prose. **Where the module is
unavoidable — driving its own gate — it must be the THING UNDER TEST, never the source of the
expected answer.** Ninety-four checks, zero imports from `utils.capacity_sweep`. The corollary
is about claims rather than code: an "exactly one field changed" claim is checked by walking
**both documents to full leaf depth**, not by comparing the fields either party thought to
name — 413 leaves each side is a different statement from "I looked at the ones that matter."

153. **[NEW S97] A PROPERTY MEASURED AGAINST A SUPERSEDED VERSION IS NOT A PROPERTY OF THE
CURRENT ONE, AND THE SUMMARY IS WHERE THAT ERROR HIDES.** My own S96 summary carried *"section
7.1's byte-determinism requirement is MEASURED"* — true when written in S95, and no longer
covering anything after Codex's S95 repair moved `capacity_sweep.py`. Nothing in the review
that followed would have forced anyone back to it, because the sentence stays true-sounding
after the object it describes has been replaced. **So: when a production file's digest moves,
re-ask which recorded measurements were taken against the OLD digest, and re-run them rather
than inheriting them.** This is lesson 151's mechanism pointed at measurements instead of
obligations — the clause nobody's current work touches is the clause that goes stale.

154. **[NEW S97] A PROBE'S FAILING CHECK IS A STATEMENT ABOUT THE PROBE UNTIL ITS ASSUMPTION
IS INDEPENDENTLY ESTABLISHED.** Four of my checks failed on first run — the delivered-data
digests did not match the canonical text domain — and the failure had exactly the shape of a
real S59 rule-(cc) violation and of the M5 survivor I had closed the session before. **The
temptation to report it was a direct consequence of having just found that class of defect,
which is lesson 148's trap arriving from the reviewer's side rather than the repairer's.** The
discipline that resolved it was to measure the assumption instead of the artifact: read the
writer (`csv.DictWriter` through `open(..., newline="")`), read the dialect's line terminator
**back at runtime** rather than trusting the documentation, and check whether the two
already-approved documents record the same values. They do — which settles it, because the
domain was jointly approved two artifacts ago. **A reviewer's instrument is under review too.**

155. **[NEW S97] AN OBSERVATION A REVIEWER MEASURED AND THEN SAID NOTHING ABOUT IS
INDISTINGUISHABLE FROM ONE IT NEVER MADE.** Two things this session were measured, judged not
to be defects, and could have been dropped silently: the raw digest domain above, and the fact
that `role_index_sha256` is a declaration no execute-time gate enforces because nothing in the
read path opens an `index.csv`. **Recording them with the reasoning exposed costs one
paragraph and buys two things a silent drop does not: the other agent can overrule the
REASONING rather than only the code, and the next session does not re-measure them from
scratch.** The bar is not "raise everything" — it is that the record should distinguish *not a
problem* from *not looked at*.

156. **[NEW S98] A CLAIM OF UNREACHABILITY IS A CLAIM, AND IT NEEDS A TEST LIKE ANY OTHER.**
`require_clean_capacity_point`'s docstring said, citing the frozen design, that the guard *"is
now unreachable on the ordinary path, since the run root is created absent and owned by this
invocation."* It fired on the second arm of the only run there has ever been, and it killed
that run. The sentence was true of the placement the design DESCRIBED (once per point) and
false of the placement the code HAD (once per arm), and **nothing in five design rounds, four
executable review rounds, 214 tests, two independent plan audits or a 22-case gate-neighbour
sweep ever compared the two.** The general rule: *an unreachability claim is the one assertion
in a file that no test is ever written for, because the thing it asserts is that nothing
happens.* Where a guard is documented as unreachable, either drive the state that would reach
it or write down that you could not - and where a docstring cites the design for a behavioural
claim, check that the code implements what the design says rather than that the design says it.

157. **[NEW S98] SOME DEFECTS ARE ONLY REACHABLE BY SPENDING, AND THE SPEND IS THE
MEASUREMENT.** Every static instrument this project owns - adversarial review rounds, mutation
sweeps, AST tests, gate-neighbour sweeps, producer-free audits - examined this executable and
none of them found finding AU, because all of them examine the program and none of them ran
forty arms. **Three fits found in thirty-one seconds what nine review rounds did not.** This is
not an argument against the rounds (they found AI-AT, all real). It is an argument against
treating "reviewed to a closed loop" as equivalent to "will work": *a program that has never
been run at its real scale has an untested claim at every place where scale is what varies.*
Where a run is affordable, the cheapest remaining reviewer is the run. **Corollary for the
next design: ask what the SECOND iteration of every loop does, not the first.**

158. **[NEW S98] A PRECONDITION CHECK MUST TEST WHAT IT IS ABOUT, NOT A PROXY THAT USUALLY
CORRELATES.** My concurrent-writer check asked "is any other python process running on this
machine" and fired twice on things that could not touch the project: the director's own test
suite in a sibling directory, and then MY OWN PROBE, because on Windows `venv\Scripts\python.exe` is a launcher that re-executes the base interpreter, so one invocation appears as
two processes and excluding by `os.getpid()` alone leaves the shim behind. The right question
was "does any process name THIS PROJECT". **A precondition that fires on things it does not
care about will eventually be widened by someone in a hurry, and then it will not fire on the
thing it did care about.** Keep it narrow and honest, and cover the rest with the bracket -
which is what a bracket is for.

159. **[NEW S99] THE RIGHT INSTRUMENT FOR REVIEWING A *TEST* EDIT IS A MUTATION SWEEP RUN
AGAINST BOTH STATES, NOT A READING OF THE DIFF.** A diff tells you what changed. The only
property a test file actually has is what it can *see*, and a two-state sweep measures that
directly - same cases, both blobs, one table. It is what found that Codex's reported gap was
three mutations wide rather than one, and what proved the edit lost nothing (+3 caught, -0),
which is the failure I was most exposed to: accepting an edit that fixes the reported case
while silently dropping coverage somewhere else. **It also found the thing no diff could:
that one of MY OWN catches was luck, riding on a fixture width I never chose deliberately
(limitation 142).** *A test suite can be blind along an axis and look complete, and what
hides it is almost always a constant nobody argued about.* **Corollary: when a reviewer edits
your test, the question is not "is this edit correct" but "what can each suite see", and only
one of those two questions has an instrument.**

160. **[NEW S99] "DERIVED FROM THE SAME SOURCE" IS A SUSPICION, NOT A VERDICT - GO MEASURE
WHAT ELSE PINS THE SOURCE.** Requirement (z) is right that a comparison whose two sides come
from one function is a report of a check. But the honest question is whether *anything else*
anchors the shared source, and that is measurable in twenty minutes: mutate the source and
see who dies. Treating (z) as an automatic block would have cost a round-trip over a
non-problem; treating it as an automatic pass would have been the cargo-cult version of it
(lesson 148). **The middle move is the only one that produces evidence, and the evidence is
what goes in the chat so the other agent can overrule the MEASUREMENT rather than my taste.**

161. **[NEW S99] AN EXPECTATION PUBLISHED BEFORE THE ARTIFACT EXISTS IS A DIFFERENT
INSTRUMENT FROM ONE FORMED AFTER IT.** Auditing a deterministic artifact after seeing it
means the "independent" derivation happens with the answer already on screen - and no amount
of discipline fully removes that. Computing the digest first, in the open, does remove it,
and it costs one command. **Do this at EVERY future gate where the artifact is deterministic,
and state the number in the chat before the other agent produces it.** The converse rule
matters as much: **if the published artifact does not match, do NOT re-derive a new
expectation to fit what is on disk.** That is the whole value, spent.

162. **[NEW S100] A FIGURE THAT COMES FROM AN INSTRUMENT MUST BE TAKEN FROM THE INSTRUMENT AT
THE MOMENT IT IS USED - AND A TIMESTAMP IS SUCH A FIGURE.** I stamped a transcript header
while drafting and appended sixteen minutes later, publishing a time in the future. The header
time is an instrument reading about *when the file changed*, and drafting is not writing. This
is the same family as a field name remembered rather than read (S98), a rollout count carried
rather than recounted (five times), and a digest domain assumed rather than measured (S97/S100)
- but it is the first one where the wrong value was *my own clock*, which felt too obvious to
check. **The general form: the more mechanical a figure feels, the less likely anyone re-reads
it.** And the fix generalizes too - **do not resolve to be careful; put the comparison inside
the tool that performs the action**, where it can refuse. `append_chat.py` now measures the
clock at the write and refuses beyond ±120 s. *(Corollary, and the reason this survived so
long: the physical-tail assertion this project has run for twenty sessions cannot see a
timestamp error at all. A check that has never failed may be watching the wrong axis.)*

163. **[NEW S100] "THE LOCATION OBVIOUSLY CANNOT MATTER" IS A HYPOTHESIS.** When Codex moved
the plan into a plan-history directory, the tempting move was to read `require_authorized_plan`,
see that it takes an explicit path and rebuilds the document, and conclude. I measured instead:
the same bytes at three locations and under a different filename, plus a corrupted copy at those
same locations to prove the acceptance was not vacuous. It cost four lines. **A negative control
is what separates "the gate accepted it" from "the gate accepts anything."** The same session's
temp-replica probe (part C) is the general shape: **rebuild the real directory layout under a
TemporaryDirectory and drive the REAL guard at it** whenever the question is "what would the
executable do if…".

164. **[NEW S102] COMPARE A VALUE IN THE DOMAIN OF THE PROGRAM THAT PERSISTED IT, NOT THE
DOMAIN OF THE PROGRAM THAT RECOMPUTES IT.** This project already knew the file-level version -
rule (cc), canonical for tracked text and raw for binary. Finding AV is the same rule one level
down, on a *number*. The tell is structural and cheap to check: **ask which writer produced each
value in a record before writing a single `==` against it.** Two writers, two domains, and a
comparison that ignores the difference is not a strict check - it is an unsatisfiable one.
**And when a check has to cross a domain, assert BOTH directions**, so a silent domain move fails
loudly instead of collapsing the check into a tautology (S100's correction to me, reused).

166. **[NEW S105] AN OBLIGATION ATTACHED TO A FUTURE ARTIFACT IS DISCHARGED BY A CHECK, NOT BY
A NOTE - AND THE SESSION MOST LIKELY TO MISS IT IS THE ONE THAT WRITES THE ARTIFACT.** I carried
a written obligation for several sessions saying the public log entry reporting the capacity
read's result owed readers the AV story. I then wrote that entry, in the session that was still
carrying the note, and did not tell the story. The note was in my continuity file; the writing
happened at the end of a long session against a different anchor. **A sentence of the form "when
X is written, it owes Y" is inert unless the act of writing X re-reads it.** The durable form is
to attach the obligation to the ARTIFACT'S OWN CHECKLIST - here, the Technical Report's - rather
than to a status block that only gets read at session start. Same family as lesson 65: a clause
that has been true for several rewrites is the one carried into a rewrite where it is false;
this is its active twin, a clause that stays true because nothing ever forces the act it names.

167. **[NEW S105] A RECORDED PHYSICAL PROPERTY OF A FILE ROTS EXACTLY LIKE A STATUS CLAUSE.** My
notes carried a loud, repeatedly-restated warning that the public README's log tail is BARE LF
while the file overall is mixed, with an anchoring procedure built around it. I measured before
writing and the file is now **200 CRLF pairs and zero bare LF** - it has been renormalised since
the note was written. Nothing was harmed because the measurement came first, but the note would
have made a careful session anchor on bytes that no longer exist. **Line endings, sizes, digests
and directory censuses are observations with a timestamp, not properties of the object.** Carry
the INSTRUCTION TO MEASURE, and treat the recorded value as the last reading rather than the
current one. Same family as the S104 census correction (a listing of what I was thinking about
is not a census of the directory) and the rollout count that was wrong five times.

168. **[NEW S108] WHEN A LICENCE FORBIDS SAYING ANYTHING ABOUT AN OBJECT, CHANGE THE OBJECT - AND
THEN LEAVE THE FORBIDDEN INPUT OUT OF THE DOCUMENT ENTIRELY.** Section 5.4 licensed one sentence
about the CURVE and forbade every other. The curve was not the only measurable thing in the
artifact: its DISPERSION was, and dispersion is not shape. That one move turned a dead end into
the most decision-relevant measurement the project had - what the design could ever have
resolved. **The second half is the part that makes it defensible rather than merely clever:** I
kept the five per-point means out of the note completely, which converts "I made no trend
statement" from an assertion into something a reviewer verifies with a text search. *Compliance
you can demonstrate structurally beats compliance you have to be trusted on.* Same family as
lesson 165 - when the obvious route is fenced off, ask what else is already on the table.

169. **[NEW S108] PRICE AN AXIS AGAINST WHAT IT MOVES, NOT AGAINST ITS OWN SIZE.** The
width-only next design costs 30 fits and five minutes and moves the resolution from 0.2597 to
0.2597, because resolution is a function of SEEDS and DISPERSION and not of how many points sit
on the axis. The seed axis costs hundreds of fits and hours and buys the entire thing - and is
still an afternoon. **A cost intuition formed on the wrong axis sends a project somewhere
useless at a price that feels reassuringly small**, which is the exact failure mode the
efficiency Standard is most vulnerable to: "smallest sufficient" read as "cheapest available."
Before pricing a design, name the quantity that limits the read and check whether the axis
touches it.

170. **[NEW S108] A CONTROL IS ITS PREDICATE AS MUCH AS ITS RULE.** My rebuild list said gate 5
requires my header to be the LAST header in the file. It did not say what counts as a header. The
rebuild therefore regenerated a gate whose ACCEPT SIDE nobody had ever specified, and the strict
recognizer I happened to write was blind to 40 of this transcript's real header forms - so the
gate could have passed while a later turn sat underneath mine, quietly, while printing a
plausible number. **Where a rule is written down for reconstruction, the recognizer it is applied
through must be written down with it.** The accept side is where damage is invisible; this is the
S69-S71 scrubber lesson arriving somewhere completely different. *And the instrument that found
it was free: two independent counts of the same object disagreed, and I reconciled them instead
of picking one. Neither was wrong-looking alone.*

165. **[NEW S102] THE CHEAPEST DECISIVE MEASUREMENT MAY BE ARITHMETIC, AND THAT MATTERS MOST WHEN
THE EMPIRICAL ROUTE IS FENCED OFF.** Finding AV was settled before a single byte of data was read,
by reconstructing each published twelve-decimal F1 back to its exact `2TP/(2TP+FP+FN)` rational
over a 152-example split and comparing floats. Only *then* did I spend one anchor's forward pass
to watch the real function refuse. **When the obvious probe would spend a pre-registration, a
budget or an irreversible act, ask first whether the question is decidable from what is already
published** - and keep the empirical drive as confirmation rather than as the instrument.

171. **[NEW S111] A RULE ENFORCED BY DEFAULT IS NOT A RULE THAT CANNOT BE BROKEN.** Rung 1's
parameter-band check was on by default and one keyword argument turned it off. Nobody ever turned
it off, and the Stage-1 design even wrote down that a Stage-2 script must not — **but a note is a
request, and the request is read by whoever is in a hurry.** Rung 2 removes the argument entirely;
the check is unconditional and an AST test pins that no parameter matching
`enforce|band|skip|strict|check` exists. **The part that makes it affordable is the second half:
the tests were written so they never need the escape hatch** — rung 1's tests used
`enforce_rung1_band=False` for speed, and rung 2's get speed from short windows and small batches
instead. *A control with an off switch survives exactly until the first session that finds the
switch cheaper than the alternative; the fix is to make the alternative cheap.*

172. **[NEW S111] MEASURE THE THING YOU WERE ABOUT TO ASSERT — IT IS USUALLY UNDER HALF AN HOUR
AND IT USUALLY CHANGES SOMETHING.** Six of the rung-2 design's load-bearing claims (strict
causality, construction determinism, capacity identical across suites, the attention path being
live, cost, and whether the architecture optimizes at all) were assertions I could have written
and nobody would have questioned. Measuring all six cost ~25 minutes of probes on synthetic
tensors and **changed two of them**: the cost ratio is worse than the parameter ratio suggests
(12x against 5.5x), and **rung 1 reached the LOWER synthetic loss.** Both went into the document.
*The measurements that change nothing are not wasted either — they are the ones that let the
reviewer skip re-deriving them.*

173. **[NEW S111] A STRUCTURAL FACT ABOUT WHAT WAS BUILT MUST NEVER BE MADE CONDITIONAL ON WHAT
WAS FOUND.** I nearly wrote the rung-2 read so that "the ladder has been climbed" counted only if
the deficit persisted or vanished in some interpretable way. **A climb that only counts when the
result is favourable is not a climb**, and making it conditional would have handed a later
write-up a way to report the ladder as unclimbed whenever the numbers were inconvenient. Row 1 of
§5.4 is now true the moment rung 2 is fitted, whatever it says. *Same family as the honesty bounds,
arriving from a direction none of them names: not overclaiming a result, but letting a result
decide whether a fact about the process is reportable.*

174. **[NEW S111] "THE LADDER MUST BE CLIMBED BEFORE ANY CONCLUSION" IS A CONSTRAINT ON A
CONCLUSION, NOT A TASK WITH A COMPLETION CONDITION.** Read quickly, limitation 127's licensing
sentence looks like a checkbox: build rung 2, tick it. It is not — the conclusion it guards is the
**held-out confirmatory comparison at Gates 6-7**, which no development fit at any rung ever
reaches. So the rung-2 document builds the rung and **does not discharge 127**; what discharges it
is the confirmatory comparison being run at a validation-selected capacity from a ladder with more
than one rung on it. *Whenever a carried limitation ends with "X must happen before Y", ask what
kind of thing Y is before writing anything that claims to have done X.*

175. **[NEW S113] A PARAMETER COUNT IS A STATEMENT ABOUT COMPOSITION AND SAYS NOTHING ABOUT
WIRING - AND A DESIGN WHOSE MOST CONSPICUOUS ARTIFACT IS A PARAMETER LEDGER INVITES EXACTLY THE
REVIEW THAT CANNOT SEE THE DIFFERENCE.** Measured, not feared: of 21 mutations of the rung-2
module, the four that survived my first test suite were all wiring defects - the fusion reading
the attention context twice instead of final-plus-context; the two fusion operands swapped; the
per-timestep normalization CONSTRUCTED and never applied; and `forward` pooling the final
recurrent state directly, leaving **the entire attention block constructed, counted and dead.**
Every one of the four has the declared 219,018 parameters, the declared shapes, the declared
construction determinism, and passes the causality test. *The ledger, the band, the grid and the
module census - four separate instruments, all of them agreeing, none of them able to see it.*

176. **[NEW S113] THE GENERAL INSTRUMENT FOR A CONSTRUCTED-BUT-UNWIRED STAGE IS A GRADIENT, AND
IT IS ONE ASSERTION FOR EVERY TENSOR AT ONCE.** Reconstruction tests (rebuild `pool` and
`forward` from the named parts and compare) close the paths you thought of. **Requiring that
every constructed parameter receive a non-zero gradient from the network's own forward output
closes the ones you did not**, because a module built in `__init__` and never applied is exactly
a module whose gradient never arrives - while still contributing to `n_parameters`, still having
the right shape, and still passing every determinism check. *Prefer the instrument that catches
the family over three tests that catch the three instances you happened to mutate.*

177. **[NEW S113] AN EQUALITY PIN ON A DERIVED CONSTANT CANNOT SEE A RETYPE TO THE SAME VALUE,
AND THAT IS THE EDIT THAT ACTUALLY UNBINDS IT.** `RUNG2_MIN_PARAMETERS == RUNG1_MAX_PARAMETERS +
1` catches a floor retyped to the wrong number. Retyping it as the literal `100_001` is not a
behaviour change at all, so no runtime assertion can catch it - yet it is precisely what leaves
rung 2's floor stranded the day rung 1's constant moves. **"Derived, never retyped" is a
property of the EXPRESSION, so the instrument is the SOURCE**: an AST check that the right-hand
side is `Name + Constant(1)` and not a bare literal. *Third member of the S71 family - a test
that consumes the decision it is supposed to guard. Ask of every pinned constant: what edit
would leave this test green and the meaning gone?*

178. **[S112, moved here S113] A SPECIFICATION THAT IS TRUE OF THE RIGHT IMPLEMENTATION AND ALSO
TRUE OF THE WRONG ONE IS NOT A SPECIFICATION.** The rung-2 design's 4.2 said parameter creation
happens "inside `fork_rng(...)` after `manual_seed(seed)`" and never said the SEEDING is inside
the fork. Driven both ways: seeding inside leaves the caller's global CPU RNG state UNCHANGED,
seeding before MUTATES it, and **both orders build the same 219,018 parameters.** *The part that
made it a repair rather than a note: the parameter count - the invariant a builder checks FIRST -
cannot tell the two orders apart, and the guard that can is one clause at the end of a
thirteen-item list. The most-read invariant is blind and the least-read one is load-bearing.*

179. **[S112, moved here S113] READ AN EMIT-PROHIBITION AGAINST THE PERSIST-REQUIREMENTS IN THE
SECTION ABOVE IT.** The rung-2 design's 5.3 forbade "no trend, slope or direction across rungs"
against a 5.2 that REQUIRED a persisted `rung2_minus_rung1[suite][seed]` plus its per-suite mean.
**A contract a builder resolves by guessing is a contract with a hole in it.** The resolution was
already ours and neither agent invoked it: Stage 1's own settlement is that the per-point means
are quotable and a line through them is not - the prohibition is on ASSERTING a direction, never
on PERSISTING the primitive. *Both sections were written to be strict, and they were written
against each other.*

180. **[S117] A DIGEST IS ONLY AN IDENTITY IF THE THING IT DIGESTS IS THE THING THAT TRAVELS.**
Both agents published the root README's *raw working-tree* SHA-256 and CR count for three
sessions as if they identified the artifact. They do not: `core.autocrlf=true` and the file is
pinned in no `.gitattributes`, so a bare `git checkout` rewrites its line endings **at an
unchanged blob** - measured, 199 CR became 208 CR with the content untouched - and every tracked
README blob has ZERO CR. *Before quoting a digest, ask which side of the clean/smudge filter the
bytes are on. A digest taken on the wrong side names one machine's copy, not the artifact.* The
corollary that bit me: **a note describing the working tree will read like a note describing the
file, and will be carried forward as one.**

181. **[S117] WHEN A MEASUREMENT WOULD COST A GATED RESOURCE, ASK WHETHER THE PROPERTY CAN BE
ESTABLISHED OVER THE CODE RATHER THAN OVER ONE EXECUTION OF IT.** The rung-2 equivalence gate
depends on a bit-identity that had been measured only on synthetic inputs, and measuring it on
the real ones costs one of twelve authorized fits. It was closed instead by showing the two loop
bodies are AST-identical after normalizing the two *declared* differences, that every name the
shared body evaluates is literally the same object in all three modules, and that the two
constructors agree bit-for-bit at the two seeds in play. *Same source + same objects + same
construction is a statement about EVERY input; a bit-identity is a statement about one.* **And
the comparison proves nothing until the normalizer is shown unable to erase an UNDECLARED
difference** - twelve mutations, 12/12 caught, two no-op controls unaffected, and the four
erasures that remain named and measured rather than assumed away.

182. **[S117] A POSITION MARKER IS A STATUS CLAUSE AND ROTS LIKE ONE.** A `<- WE ARE HERE` marker
sat inside the summary's historical Order chain at the S103 link and stayed there through
thirteen rewrites after the position had moved. It survived because it reads as punctuation
rather than as a claim. *Caught only by grepping my own finished rewrite for the marker rather
than reading for it - the same instrument that caught lesson 65's recurrences.* **Keep exactly
one authority on where the project is, and grep the rewrite for every phrase that asserts a
position.**

183. **[S118] A WRONG VALUE THAT IS WRONG IN ONLY ONE DOCUMENT DOES NOT SEPARATE A REAL
COMPARISON FROM A SELF-COMPARISON.** Requirement (z) says a check needs a source independent of
the thing it checks. The instrument that *proves* the source is independent is narrower than
that, and I did not have it: my two code-identity tests each made the run record and the plan
disagree, and a mutation that sourced the "current" identity **from the record itself** survived
both, because a self-comparison still catches a disagreement between two documents. What it stops
catching is the state that matters - an older run whose record, plan and gate evidence all name
one another consistently, read by a newer executable. **To test that a comparison has a real
external source, make the value wrong EVERYWHERE AT ONCE and require the refusal.** Measured in
the S118 sweep: 24/25 caught on the first run, this the only survivor, closed with one test, then
25/25 with both no-op controls still surviving.

184. **[S118] INVARIANT R7'S "IMPORTING IS REQUIRED" IS A POSITIVE INSTRUCTION, NOT ONLY A
PROHIBITION.** The design's R7 reads "importing from them is required, editing them is
forbidden." The easy reading takes only the second clause and writes a fresh set of validators
beside the approved ones. The first clause is what keeps one definition of `finite_number`,
`unit_interval`, `sha256_digest`, `strict_object`, `safe_relative_path` and `observed` in the
project, and it is also the Software-engineering standard's shared-`utils` rule stated for one
artifact. **When a design says to import, import - and subclass the imported error rather than
opening a second family, so one handler names one family.**

185. **[S119] A CHECK THAT WAS PRE-DECLARED WEAK DOES ITS JOB ON THE DAY THE WEAK VERSION
PASSES - AND THAT IS THE DAY SOMEONE HAS TO SAY SO OUT LOUD.** Design section 5.1 wrote, before
anything ran, that the objective's severity Gaussian-NLL term can drive a reduction without
improving classification, so `OBJECTIVE_REDUCED` is not a learning signal. Ten of ten rung-2
arms reduced the objective, and every one of them scored F1 = 0.000000 on two of the four
classes, four of them sitting exactly on the majority-class baseline the artifact itself
records. Nothing failed. The gate certified exactly what it said it would certify. **The value
of pre-declaring a check's weakness is realised on the day the weak version passes, and it is
realised only if the session that sees it writes the disclosure next to the licensed sentence
rather than leaving the sentence to stand alone.** The corollary is a rule about scope: this is
not the failure path either. A pre-declared failure path has named branches, and reading it as
"or anything else that looks disappointing" destroys the thing pre-declaring it bought.

186. **[S119] AN AUDIT THAT PASSES ON THE FIRST ATTEMPT HAS USUALLY NOT BEEN CALIBRATED.** The
165-check step-7 audit was red three times before the artifact was green once - a status string
in the wrong case, a field-path walker assuming a structure the artifact does not use, and an
assumption that a mean is a bare float when the artifact publishes it as a `{raw, quantized}`
pair. Each red was mine. **The practical test of whether a second instrument is genuinely
second is whether it can be WRONG IN ITS OWN WAY; shared code cannot be.** This is the S56
independence requirement (z) stated from the other side: requirement (z) says give the check an
independent source; this says you can tell whether you did by whether the check ever disagreed
with the artifact for a reason that turned out to be the check's fault. An audit that has never
been red has usually been reading the artifact rather than measuring it.

187. **[S119] PUBLISH THE NUMBER AND ITS RENDERING TOGETHER.** Every mean, sample SD and
difference in the rung-2 analysis artifact is a `{raw, quantized}` pair - the full-precision
float beside its six-decimal string - so a reader never has to infer which domain a value is
in. That is **finding AV's lesson built into the SCHEMA rather than into a comparison**: AV
happened because a value crossed a rounding boundary between its producer and its reader with
nothing in the document saying so. A schema that carries both sides makes the question
unaskable. It costs one extra field per statistic. **Do not "simplify" such a pair to a bare
float**, and prefer this shape in any future artifact that publishes a derived statistic
alongside a rule that quantizes it.

188. **[S120] A REFUSAL THAT PRINTS NOTHING IS NOT A REFUSAL.** My S120 probe accumulated its
check results in a list and the caller printed them at the end. A structural mutant - one arm
removed from the artifact - then raised inside a later check, the process exited non-zero with
**zero output**, and every check it had already made was discarded. From outside, that is
indistinguishable from a broken harness: same exit code, same silence. It also cost the mutation
control a survivor, because the control could see the process refuse but not *which* check
refused, which is the only thing that makes a catch a catch. **Print each check as it is made,
not at the end**, and guard every lookup that a structural mutation can make missing so the
refusal comes out of the check that names the thing. This is lesson 186's partner: a control is
only informative if the instrument reports *where* it refused, so an instrument that can only
say "no" cannot be calibrated at all.

189. **[S120] CHASE A FLAG FROM YOUR OWN INSTRUMENT BEFORE PUBLISHING IT.** My path scan over the
new packet-README text reported a UNC-path hit. There was none. The pattern was `r"\\\\[^ ]"`
written inside a Bash heredoc, which is **one** literal backslash in the regex, not two, so it
matched every ordinary relative Windows path in a PowerShell block. Measured with an
`re.escape`-built pattern: zero matches, and the text contains no double backslash at all. The
near-miss is that publishing the flag would have put a false defect claim about my own work into
the record, and the fix would have been a change to text that was already correct. **A red result
from a hand-written pattern is a claim about the pattern until it is a claim about the file** -
confirm it with an independently constructed matcher before it leaves the session.

190. **[S121] A COUNT IN PROSE IS A CLAIM AND HAS TO BE MEASURED AT ITS SOURCE, AND BEING SURE OF
THE MECHANISM IS WHAT SUPPRESSES THE CHECK.** Three counted falsehoods sat within forty lines of
each other in the packet runbook: the six arms scoring "nothing else" when all ten score a
non-zero `sensor` F1 (Codex found it); the ten anchors "each" carrying four non-zero per-class
values when two are zero on `healthy`; and the equivalence gate authenticating "the ten"
`results/dev_fit/` checkpoint files when it opens **two** - `EQUIVALENCE_ARMS` is
`(("C1",0),("S",4))`, defined once in `capacity_sweep.py` and imported by `rung2_escalation.py`,
and each executable passes `checkpoint_dir` to exactly one function. The third one is the
diagnostic case: I had written *"refits the two approved rung-1 checkpoints"* three paragraphs
earlier in the same step and still wrote "the ten" downstream, because **"the ten approved
anchors" is the phrase this project says most often**. A correct model of the mechanism is not a
measurement of the count, and confidence in the model is exactly what stops the count being
checked. **Grep every cardinal in new prose and drive each one to a primary object.**

191. **[S121] TWO SENTENCES IN ONE PARAGRAPH CAN BE INDIVIDUALLY DEFENSIBLE AND JOINTLY
MISLEADING, AND THE FIX IS TO NAME THE SOURCE, NOT TO SOFTEN THE CLAIM.** Step 30 states a real
wall-clock figure (1,274.6 s) two sentences from an order-of-magnitude micro-benchmark figure
("roughly 12x per optimizer step") that came from the frozen design and not from this run, and the
run record's own `elapsed_s` (1,272.094) is a third number a reader will find and cannot
reconcile. None of the three is false; the arrangement invites a reader to think this run measured
all of them. **Where numbers of different provenance sit together, publish the provenance beside
each one** - the same discipline as lesson 187's {raw, quantized} pairing, one level up from the
value to where it came from.

192. **[S121] A FINDING LETTER IS A SHARED NAMESPACE AND THE OTHER AGENT MAY HAVE CLAIMED ONE
WITHOUT SAYING SO IN CHAT.** Codex's S120 chat turn named its finding only in prose; its
HumanReport120 called it **BM**. I had already appended a turn using BM, BN, BO. **Read the other
agent's report before assigning letters, not only its chat turn.** The recovery is the S117 rule
and it applies only before a commit or a handover: re-assert the complete prior transcript
byte-for-byte as a prefix and rewrite **your own payload only**. Afterwards the only answer is a
new appended correction.

193. **[S122] A WARNING YOU WROTE YOURSELF IS NOT A GUARD; THE GUARD IS THE CODE THAT CRASHES.**
My S122 read-back script opened `arms[].classification.per_class_f1` and died on a `KeyError`.
That path is not the shape of the `arms[]` rows at all - it is the **template string** the
`anchor_arms[]` rows carry in `per_class_f1_field` to name where their values came from. I had
written *"read the field, do not remember it"* into my own continuity file one session earlier
and walked into the identical conflation anyway. **The lesson is not "be more careful" - that is
what failed.** It is that the cost was thirty seconds ONLY because the access raised loudly
instead of silently resolving to something plausible. So: **index the record directly and let a
wrong path raise**, rather than writing a tolerant accessor (`.get(...)`, a try/except fallback,
an `if "classification" in arm` branch) that would have made the same mistake return a wrong
number with no crash. A tolerant accessor over an artifact you did not write converts a loud
schema error into a silent data error, and this project publishes what those accessors return.
*(Walked into the identical trap AGAIN in S123, one session after writing this. Same cost, same
reason: it raised. The lesson stands unchanged and its value is now measured twice.)*

194. **[S123] A REVIEWER BEING RIGHT IS NOT THE SAME STATEMENT AS A REVIEWER'S SET BEING
COMPLETE — CHECK THE CLAUSES IT DID NOT FLAG.** Codex's Finding BQ said two of the three clauses
in my published closing sentence were literally broader than the record. Both diagnoses were
correct and I accepted them. **The move that mattered was checking the third clause myself**:
*"the final test set remains untouched"* is exactly true (0 identities, 0 payloads), so two is
the WHOLE set of overbreadths rather than a sample of them. Had it been three, accepting BQ as
written would have closed the loop over a sentence still carrying a false clause, and the loop
closing is precisely what stops anyone looking again. **A finding names what the reviewer found;
it does not certify what the reviewer did not find.** The owner re-review is the only step in the
cycle positioned to complete the set, and completing it costs one pass over an artifact already
open. This composes with the review-cycle rule that diagnosis and implementation are separate
questions: there are in fact **three** questions on an owner re-review — is the diagnosis right,
is the implementation right, and **is the set complete**.

195. **[S124] FIELD-LEVEL DEFECTS ARE FOUND BY READING; INTERACTION-LEVEL DEFECTS ARE ONLY FOUND
BY ASKING WHAT HAPPENS WHEN THE THING RUNS.** All nine of Codex's S123 findings were field-level
(wrong role, missing field, incomplete call). Both of mine were interaction-level — two rules in
the **same document**, each individually sensible, **jointly impossible**. A review that does only
the first kind hands off a document that reads perfectly and cannot be built.

196. **[S125] LESSON 195 CONFIRMED A SECOND TIME IN THE SAME DIRECTION, AND THE INSTRUMENT NAMED.**
Both of Codex's S124 findings were field-level; both of mine were interaction-level. Two rounds
running. The instrument that finds the second kind is not *"is this sentence true"* — it is **what
happens when the thing runs**, and this round's version was literally two questions: *"what does
the slider move?"* and *"what does `j_5s` do with the numbers this fixture will actually hand
it?"* **Both answers required leaving the document.**

197. **[S126] THE MOST USEFUL QUESTION IN A RENDERING DESIGN IS "WHICH PANEL DRAWS THIS?"** A
constraint on a **rendered** quantity earns its strictness. A constraint on a
**carried-but-unrendered** quantity is pure downside risk: it can refuse, and it can never be seen
to be right. That question is what turned CI from *"an unusually strict rule"* into *"a rule that
refuses every real scene over something nobody looks at"*.

198. **[S126] AND THEN IT REVERSED: THE NEXT NOTCH OUT IS "DOES THIS RULE SURVIVE CONTACT WITH AN
OBJECT OUTSIDE THE DOCUMENT?"** Both of Codex's S125 findings were interaction-level — the harder
kind, and the kind I had been the only one finding for two rounds. What was left for me was one
notch further out: not *"do two rules in this document conflict"* but *"does this document's rule
survive contact with an object outside it"*. CI needed two source files and a driven validator; CJ
needed asking which function receives which argument; CK needed driving a live contract with an
empty payload. **The loop converges: the remaining defects get structurally smaller each round.**

199. **[S127] THE RECURRING DEFECT IN A SPECIFICATION HAS ONE SHAPE — A RULE STATED GENERALLY AND
THEN DISCHARGED BY A PARTIAL ENUMERATION, WHERE THE ENUMERATION IS WHAT THE IMPLEMENTATION WILL
ACTUALLY FOLLOW.** It appeared four times in one document: CA, CE, CI, CN. **The question that
finds it: when this document names a fact that some other object already owns, does it POINT at
that object or COPY it?** A copy takes on an obligation to stay current that nothing in this
project enforces. Ask it alongside lesson 197's *"which panel draws this?"*. **[S128 addendum: the
enforcement mechanism, when you can build one, is a test that makes the copy impossible rather
than a comment asking for it — see lesson 201.]**

200. **[S127] A REVIEWER BEING RIGHT IS NOT A REASON TO SKIP THE MEASUREMENT, AND THE MEASUREMENT
PAYS FOR ITSELF TWICE.** Finding CM was a narrow wording correction I could have taken on
authority at zero cost. Reproducing it is what put me inside `role_contract.py` and `metrics.py`
in the same session, **and CN came out of that**. This is lesson 194's rule (check the clauses the
reviewer did *not* flag) paying a second dividend.

201. **[S128] A TEST THAT ASSERTS A CALL HAPPENED IS WEAKER THAN A TEST THAT ASSUMES THE CALL AND
WATCHES IT FAIL.** An AST test proving `_validate_tracking_window` contains a `j_5s` call is
satisfied by a function that calls it and ignores the result. **The load-bearing test replaces the
delegated-to function with one that raises a sentence no design document contains, and requires
that exact sentence to appear in the refusal.** Both are in the suite; only the second can hold a
delegation in place. This is the executable form of lesson 199: where a specification says *point,
do not copy*, the test that enforces it must make the copy detectable, not merely make the
pointing visible.

202. **[S128] LOOKING AT THE PICTURE IS A MEASUREMENT, AND NO INVARIANT SUBSTITUTES FOR IT.**
Nineteen invariants and 144 tests passed on a figure whose fabricated-truth line overlapped its
title, whose equal-aspect body panel was a sliver, and whose panel titles ran off the axes. The
tests check what the artifact must never **do**; none of them checks whether a human can **read**
it — and for a *director's* verification artifact that is the property the whole thing exists for.
Render to scratch and open the image before handing it over.

203. **[S128] NEVER USE A BASH HEREDOC FOR CONTENT CONTAINING BACKSLASHES.** Three in-place edits
this session went through `python - <<'PY'`, and the shell collapsed backslash sequences despite
the quoted delimiter: one replacement pattern silently failed to match, one wrote a vertical tab
into a tracked document where `..\venv` belonged, and one turned `re.compile(r"\bci\b")` into
`re.compile(r"ci")` — which then matched *"confidence"*. **Two of the three were silent; the third
was caught only because it failed loudly.** Use the Write/Edit tools, or build the string from
`chr(92)` with no literal backslash anywhere in the command, and sweep the finished bytes for
control characters afterwards.

204. **[S129] A DIFF SHOWS WHAT MOVED; IT DOES NOT SHOW WHAT THE DESTINATION ALREADY CONTAINED.**
Codex's CQ repair *deleted* an explicit `bundle_version` guard from `render_bundle` and replaced it
with a call to `validate_bundle`. That is exactly the shape of an edit that quietly loses a
guarantee, and reading the diff alone cannot tell you whether it did: the removed lines are visible
and the destination's contents are not. Reading the callee settled it in one step — the version
check is the *first* `_require` inside `validate_bundle`, under the same exit code, so the
replacement is strictly stronger. **When a review moves a check rather than adding one, open the
place it moved to and confirm the check is there before accepting or rejecting.** The corollary is
the cheap instrument: drive the input the deleted branch existed to refuse, and require the refusal.

205. **[S129] A PROPOSED TEST ADDITION MUST BE JUSTIFIED BY A MUTANT THAT SURVIVES THE OTHER
VERSION.** "This looks under-tested" is an intuition; running the same mutant against both
test-file states converts it into a measurement. My two S129 additions were kept only because
mutant A (an unknown menu label silently swallowed) and mutant B (the label→case map swapping
entries 0 and 1 while leaving index 2 correct) both **survive** the reviewer's tests and are both
**killed** by mine. Mutant B is the general case worth remembering: a test that drives one index of
a collection certifies that index and nothing else, and the failure it misses is the asymmetric one
that a uniform implementation would never produce but a subtly wrong one does. **A test addition
the other version also kills is decorative — drop it rather than enlarging the review object.**
The related discipline learned the hard way in the same session: **a mutation control whose
unmutated control is red measures nothing.** Mine came back red on the first run because I staged
`scripts/` and `tests/` but not `schema/`, and the two failures were precisely the two tests that
pin field names by equality against `schema/schema.json`. Check the control before reading a single
mutant verdict.

*(Migrated into this file in S128. Lessons 195-200 above were introduced in the summary
file's head block during S124-S127 and were never moved here before that block was
rewritten - exactly the drift the S105 correction warns about. Their text is recovered in
substance from the S124-S127 commits of `agents/Claude/Summary of Only Necessary
Context.md` and condensed; 201-203 were new in S128 and 204-205 in S129 — both written
directly into this file rather than into the summary's head block, which is the S105
correction applied.)*

206. **[S130] A PATCH ANCHOR IS A SEARCH, AND A SEARCH OVER A REPEATED STRING RETURNS ITS FIRST
  MATCH, NOT ITS LAST.**  Codex's S129 approval landed 12,000 lines from the end of the Phase-2
  transcript because it placed the append with the context `-- Claude` plus a separator — a string
  that occurs on almost every turn boundary in a file where two agents alternate.  *** IT HAD
  AUTHENTICATED THE WHOLE FILE'S DIGEST FIRST, AND THAT DID NOT HELP, BECAUSE A DIGEST CONSTRAINS
  WHAT THE FILE IS AND AN ANCHOR CONSTRAINS WHERE THE WRITE GOES.  THOSE ARE TWO DIFFERENT
  OBJECTS — the same root as the S118 and S120 entries, one rung narrower. ***  This is the third
  recurrence of one cause and the rule does not change: THE WHOLE PRIOR FILE TRAVELS AS AN
  EXPLICIT ASSERTED PREFIX.  The transferable addition is the diagnosis, not a new rule.  *** AND
  THE SECOND HALF IS WORTH AS MUCH AS THE FIRST: Codex's own post-write assertions caught it in
  the same turn, before closeout, on three independent post-conditions.  TWO CONSECUTIVE
  RECURRENCES HAVE BEEN DETECTED AND DISCLOSED BY THE AGENT THAT CAUSED THEM.  ASSERTIONS THAT CAN
  FAIL ARE WORTH WRITING BECAUSE OCCASIONALLY THEY DO. ***

207. **[S130] A LINE-LEVEL `-0` IS A REPORT ABOUT LINES.  THE CLAIM THAT MATTERS IS ABOUT BYTES,
  AND THERE IS A CHEAP CHECK THAT SETTLES IT — RECONSTRUCT THE PRIOR OBJECT.**  `git diff --numstat`
  said `+118/-0` on the misplaced-append commit, which is true and is *not* the same statement as
  "every prior byte survived".  The check that is: take the new blob, delete exactly the added line
  ranges the hunks name, and require the result to equal the prior blob byte for byte.  It did.
  *** THAT ONE RECONSTRUCTION IS STRONGER THAN ANY NUMBER OF AGREEING DIGEST QUOTES, BECAUSE IT
  RE-DERIVES THE PRIOR OBJECT INSTEAD OF COMPARING TWO SUMMARIES OF IT.  USE IT WHENEVER AN APPEND
  LANDS ANYWHERE OTHER THAN THE TAIL. ***

208. **[S130] DRIVE THE FIXTURE; DO NOT QUOTE YOUR OWN CONTINUITY FILE.**  Writing packet runbook
  Step 32 I described the fixture's deliberate asymmetry as "the same value to both once, and
  identical arms once", taken verbatim from my own summary.  Driving the live `j_5s` over the four
  cases showed **two** exact ties, not one — `bias_encoder_1` has identical tracking outputs with
  *different* decisions, and `indistinguishable_softening` is identical in every recorded field but
  the suite name.  *** THE SENTENCE WAS PLAUSIBLE, IT CAME FROM MY OWN FILE, AND IT WAS HEADED FOR
  A READER-FACING RUNBOOK.  A SUMMARY IS A RECORD OF WHAT WAS MEASURED ONCE, NOT AN INSTRUMENT.
  ANY NUMBER THAT IS ABOUT TO BE PUBLISHED IS RE-DERIVED FROM THE OBJECT, EVEN WHEN I AM THE ONE
  WHO WROTE IT DOWN. ***  Same family as lesson 65, one level in: 65 is about a status clause
  rotting across rewrites, this is about a *measurement* being carried instead of retaken.

209. **[S130] A STANDING RULING HAS A PREMISE, AND THE PREMISE IS WHAT BINDS — CHECK IT AGAINST THE
  NEW CASE BEFORE EITHER OBEYING OR REOPENING.**  Codex ruled in its S128 that no EOL pin is added
  for `*.py`, on the stated ground that no packet runtime hashes those files, Git blobs are the
  durable identities, and a pin would enlarge the review object without closing a runtime gap.
  S130 added a pin — for `results/verification_fixture/*.sha256` — and that is not a reopening: the
  file's CONTENT IS A DIGEST, the runbook written in the same session tells a reader to compare it,
  and `git checkout-index` MEASURED a fresh Windows checkout rendering it at 66 B with one CRLF
  against the tracked 65 B.  *** THE DISCIPLINE HAS TWO HALVES AND BOTH ARE LOAD-BEARING: name the
  ruling's premise and say why it does not reach the new case, AND pin only what was measured to
  move.  The canonical JSONs carry no newline and the PNGs round-trip as binary, so neither is
  pinned — pinning what does not move is exactly the object enlargement the ruling refuses. ***

210. **[S131] A BLOCKED STATUS IS A MEASUREMENT AND ROTS LIKE ONE — RE-MEASURE IT BEFORE CARRYING
  IT FORWARD AGAIN.**  "Slot-8 step 4 is blocked on three inputs that do not exist" was written in
  S123 and carried unexamined through eight of my sessions.  It was roughly two thirds false.  The
  frozen design's step 4 bundles four separable things — the connection-record design, the adapter
  build, the record itself, and the authorized run — and only the last two actually need the
  missing inputs.  *** WHAT FALSIFIED IT WAS A FILE THE PACKET ALREADY HAD:
  `scripts/build_data_contract_fixture.py` writes a role-complete, schema-conformant storage tree
  and imports neither `mujoco` nor `torch`, so the adapter can be built and driven end to end
  today.  I found it by opening the packet's own scripts while writing the design, not by thinking
  harder about the blocker. ***  THE GENERAL FORM: lesson 65 says a status clause true for several
  rewrites is the most likely to be carried into one where it is false — this is that lesson
  applied to a BLOCKER rather than to a review state, and blockers are worse, because nothing in
  the work forces you to revisit one.  ASK OF EVERY CARRIED BLOCKER: *is it one thing, or several
  bundled under one name, and is every one of them actually blocked?*

211. **[S131] A SHARED CONSTANT WHOSE COMMENT ARGUES FOR WHY IT IS SHARED IS A GOOD PLACE TO LOOK
  FOR A DEFECT.**  `CENTERLINE_TASK_OUTPUT_TOL_M = 1.0e-9` carries a comment saying it is declared
  once "so the fixture generator and the future read-only role adapter check the same thing with
  the same number".  That comment is an ARGUMENT, and the argument is wrong: the fixture's distal
  point IS its task output by construction, so 1 nm measures construction exactness, while the
  adapter compares an independently derived forward-kinematic endpoint against a MuJoCo site
  position, where 1 nm is a bit-equality demand.  *** THE COMMENT IS WHAT MADE IT FINDABLE.  A bare
  constant invites no scrutiny; a constant with a justification invites exactly one question — *is
  the justification true?* — and that question is cheap and occasionally very productive. ***  THE
  FAILURE MODE IT WOULD HAVE CAUSED IS THE EXPENSIVE PART: the adapter would refuse every real arm,
  and the obvious repair under time pressure is to loosen the SHARED constant, silently weakening
  the fixture's check at the same time.  WHEN ONE VALUE IS ASKED TO BE TWO THINGS, SPLIT IT, AND
  MEASURE THE NEW ONE RATHER THAN CHOOSING IT.

212. **[S131] `%Z` RENDERS THE LONG TIMEZONE NAME ON WINDOWS — CHECK THE RENDERED HEADER, NOT THE
  FORMAT STRING.**  My first S131 transcript append stamped "2026-08-13 20:21 Pacific Daylight
  Time" where the project's convention is "PDT", because `datetime.strftime("%Z")` on this machine
  returns the full name.  Caught in the same turn, before committing and before handover, and
  corrected by rewriting my own payload onto a prefix re-asserted byte-identical — which is the
  S117 rule and is the only form this correction may ever take.  *** THE TRANSFERABLE HALF IS NOT
  ABOUT TIMEZONES: a format string is a statement of INTENT and the rendered output is the FACT,
  and every convention this project enforces is enforced over the fact.  PRINT WHAT YOU ARE ABOUT
  TO WRITE AND READ IT, rather than trusting the expression that produced it. ***  Use the shell's
  `date "+%Y-%m-%d %H:%M %Z"`, which does give `PDT`, or assert the rendered header against the
  convention before the write.

213. **[S132] A DEFECT THAT ONLY THE UNREACHABLE PATH CAN EXPOSE IS THE EXPENSIVE KIND — ASK WHAT
  THE ACCEPT PATH ACTUALLY REACHES.**  Finding CX: the Step-4 design pinned the `FINAL` output
  parent to the same tree the connection record itself lives in, while the adapter must create its
  output root EXCLUSIVELY and refuse a non-empty one.  Those are one directory, and it is non-empty
  before the adapter starts, because the record must exist and be reviewed before the authorization
  that names its digest.  *** A `FINAL` INVOCATION COULD NEVER HAVE REACHED EXIT 0 — and every test
  the next build round writes would have PASSED, because that round's accept path is synthetic and
  writes to a temporary root.  It would have surfaced at the last sub-step, after a one-shot
  authorization had been spent. ***  THE GENERAL FORM, and this project has now paid for it THREE
  TIMES — AU (the sweep executable could not have completed a sweep under any plan), AV (C7 could
  not have completed the read it exists to perform), CX — is that a guard, a destination rule or a
  precondition can be individually correct and jointly impossible, and the tests that would catch it
  are exactly the ones the current round cannot run.  *** THE QUESTION THAT FOUND ALL THREE IS THE
  SAME ONE: enumerate what the REAL accept path touches, and check that nothing on it is already
  occupied, already spent, or already refused.  Ask it of every design before approving it, not of
  every executable after building it. ***

214. **[S132] A RULING CAN BE INCONSISTENT WITH A PRECONDITION WITHOUT EITHER BEING WRONG ALONE.**
  Finding CY: Codex's E3 ruling said a `DEVELOPMENT_ONLY` record is reachable "after P1–P6 are
  satisfied", while P1 — which I wrote a session earlier — requires a frozen config with no `dev-`
  string, and the frozen design's own entry condition for that authority requires a `dev-` config.
  Neither statement is wrong in isolation; they were written in different sessions for different
  purposes and they collide only in the merged document.  *** THIS IS AN ARGUMENT FOR THE OWNER
  RE-REVIEW STEP EXISTING INDEPENDENT OF WHETHER THE REVIEWER'S EDITS WERE GOOD — here all eight of
  them were, and the collision still appeared.  A collision of this shape is invisible to whoever
  wrote either half; only a cold read of the merged artifact finds it. ***  AND THE SECOND HALF:
  when what you find is a DECISION rather than a bug, and the decision was explicitly handed to the
  other agent, the repair is to REMOVE THE FALSE SENTENCE, write out both branches so the round
  that settles it does not re-derive them, bind the choice to the sub-step where it first matters,
  and state your own preference AS a preference.  Choosing its content while "repairing" it is the
  mirror image of the failure the re-review exists to prevent.

215. **[S132] REPRODUCING A NUMBER IS NOT THE SAME AS CONFIRMING A FINDING — AND SAYING WHY THEY
  DIFFER IS WORTH MORE THAN EITHER.**  Codex reported the contract fixture's geometry incoherence
  as a 2.81–6.20 mm endpoint miss.  My own probe gave 2.549–4.513 mm.  The gap is not a
  disagreement: mine is a rigid reconstruction contributing ZERO deformation, its contributes a
  WRONG one, so its figure is necessarily larger.  *** WHAT CARRIED THE FINDING WAS THE STRUCTURAL
  FACT, READ AT SOURCE, NOT EITHER NUMBER: `deform_coords` is drawn from an independent random
  phase set and `true_task_output` is computed from `curvature_true` alone, so the deformation
  channel enters the tip NOWHERE. ***  Quietly adopting the reviewer's number would have published
  a figure I had not produced; treating the mismatch as a defect would have opened a round over
  nothing.  THE RULE: when you cannot reproduce a collaborator's measurement, first ask whether you
  measured the same object — and if you did not, report both with the reason, and name the
  structural fact that makes the finding hold regardless of which number is quoted.

## Scratchpad (S111, NOT committed) - THE DESIGN-BY-MEASUREMENT SHAPE, and it is reusable

```text
<session scratchpad>/
  rung2_probe.py             THE PROTOTYPE LIVES IN THE PROBE, NOT IN THE PACKET.  It defines
                 the candidate architecture as a throwaway class, IMPORTING the approved
                 building blocks, and measures five things by CONSTRUCTION: A a 7-row candidate
                 grid (parameters, layer census, stem receptive field); B causality by
                 TRUNCATION (perturb everything after a cut, require EXACTLY 0.0 change at or
                 before it); C determinism at one seed and difference across seeds; D suite
                 agnosticism by MASKING the gauge columns and comparing parameter count, shape
                 and output; E one optimizer step timed through the APPROVED arm_loss.
                 *** THIS IS THE WHOLE METHOD: WRITE THE DESIGN AGAINST MEASURED NUMBERS, NOT
                     AGAINST ARITHMETIC YOU DID IN YOUR HEAD.  It cost ~25 min and changed two
                     of the six claims it checked. ***
  rung2_attention_probe.py   THE MECHANISM-IS-LIVE CHECK, and it is the S84 gauge-channel
                 discipline applied to an architecture: a path that is wired but INERT is worse
                 than one that is absent, because it looks like capacity.  Measures attention
                 entropy against uniform, the context's contribution against the pooled
                 magnitude, and sensitivity to a FIRST-32-step versus a LAST-32-step
                 perturbation.  *** REPORT "NEAR-UNIFORM AT INITIALIZATION" AS THE EXPECTED
                     RESULT IT IS, and say out loud that it is a wiring check rather than
                     evidence the mechanism learns. ***
  rung2_learnability_probe.py  THE CHEAPEST DE-RISKING AVAILABLE: run the EXACT fixed protocol
                 (20 epochs, batch 8, lr 1e-3, Adam, 152 examples) on RANDOM inputs with RANDOM
                 fixed targets, for the new architecture AND the old one.  It answers "does this
                 optimize at all under a protocol chosen for a different architecture" without
                 touching one development row.  *** A SYNTHETIC OPTIMIZER STEP IS NOT A
                     DEVELOPMENT FIT - the precedent is tests/test_capacity_sweep.py - AND THE
                     BOUNDARY STATEMENT MUST SAY SO EXPLICITLY. ***
  prune_summary.py           THE CLOSEOUT EDIT AS AN ASSERTED SCRIPT: delete/replace regions BY
                 INDEX, assert every boundary line BEFORE writing, and assert afterwards that
                 the retired headings are gone AND that six kept headings survive.  A closeout
                 that cuts 182 lines out of a 3,500-line file should not be done by hand.
  append_chat.py REBUILT A SEVENTH TIME from the timestamp-gate block, at full strength.
                 *** GATE 1 CAUGHT SOMETHING WORTH RECORDING: the prior-bytes digest it measured
                     (941dc96f...) EQUALS the post-write digest Codex published in its own S110
                     report - an independent confirmation that nothing touched the transcript
                     between the two sessions, obtained for free. ***
  turn_s111.md   one file per appended turn, so --body-file is a file and never a shell string.
```

*** S106 LESSON, KEPT: my post-write check on the workspace README FAILED because I chose a
    "stale marker must be gone" string that my own REPLACEMENT text also contains.  The write
    was correct; the CHECK was wrong.  A post-condition that can be satisfied or broken by the
    new text is a check on my choice of marker, not on the edit.  *** PICK THE RETIRED MARKER
    OUT OF THE TEXT BEING REMOVED AND VERIFY IT IS ABSENT FROM THE REPLACEMENT, FIRST. ***

*** S105 LESSON, KEPT: I carried a note for several sessions saying the log entry reporting the
    read's result owed the reader the AV story - and then I WROTE THAT ENTRY, in a session still
    carrying the note, without telling the story.  See lesson 166.  A note that describes a duty
    owed by a FUTURE act is not a control over that act. ***

*** S105 PATTERN, KEPT because it is still how every edit here gets made: put the replacement
    text in a .py FILE, assert the anchor is UNIQUE before writing, re-assert prefix + suffix +
    BYTE ACCOUNTING after.  Never a shell heredoc - it mangles before it reaches disk.  And a
    rewrite that RENAMES a section must sweep for REFERENCES to it, not just replace it. ***

## THE RESOURCE-SPEND HISTORY - moved out of "Where the project is" in S112

```text
*** THE LIVE COUNTERS ARE IN THE SUMMARY.  THIS IS THE DERIVATION AND THE
    PER-SESSION RECORD, WHICH IS A PERMANENT RECORD RATHER THAN CURRENT STATE. ***
```

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
+ Codex S117: THE ONE AUTHORIZED RUNG-2 EXECUTION.  12 fits / 12 checkpoints / 0 rollouts,
  1,274.6 s process wall clock (the run record's own elapsed_s = 1272.094...).
  *** A FIT IS NOT A ROLLOUT.  THE ROLLOUT TOTAL IS STILL 278; THE FIT TOTAL BECAME 67. ***
MY S112-S122 SPENT ZERO ROLLOUTS, ZERO FITS, ZERO CHECKPOINTS, ZERO GENERATION RUNS AND ZERO
  PILOT/VAL/TEST READS, WITH EXACTLY THREE NAMED EXCEPTIONS - and this block was backfilled in
  S122 from my own continuity record, which had carried it as a summary line rather than as
  per-session entries.  THE EXCEPTIONS:
    S116  FOUR PLAN-MODE INVOCATIONS - three into scratch, one into the packet, producing the
          tracked rung-2 plan artifact.  *** A PLAN IS NOT A FIT AND NOT A ROLLOUT. ***
    S117  ONE PRE-AUTHORIZATION READ of real data - `load_dev_examples` through the approved
          loader (dev split only, 304 of 944 rows, 2.1 s) plus a sha256 of ten approved .pt
          files.  *** A READ IS NEITHER A FIT NOR A ROLLOUT. ***
    S119  THE ONE AUTHORIZED PRODUCTION ANALYZER INVOCATION on this lane, X_ANALYSIS_OK,
          11.97 s, ZERO fits.  It read the approved development rows and twelve checkpoints.
  Everything else across those eleven sessions was review, probes over TRACKED artifacts, and
  documentation.  Checkpoint count re-measured on disk in S118, S119 and S120: 67 each time.
MY S122 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, no plan
  mode, NO C7 OR ANALYZER INVOCATION, and no edit to any executable, test, protocol, plan or
  result.  One appended public running-log entry (+2/-0), one appended chat turn (+123/-0),
  one workspace-README lead update, one report, this file's lesson 193 and this record.
  *** IT TOUCHED NO REAL DATA AT ALL - no manifest, no .npz, no label payload, no checkpoint
  and not even a hash of one.  The read-back probe opened EXACTLY ONE TRACKED JSON
  (rung2_escalation_analysis.json) under a digest refusal, plus the run record, the
  equivalence artifact and the frozen design, and wrote nothing. ***
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 67. ***
MY S111 SPENT ZERO OF EVERYTHING - no fit against any development row, no checkpoint, no
  generation, no rollout, no plan action, NO C7 INVOCATION and NO EDIT TO ANY EXECUTABLE,
  TEST, PROTOCOL, PLAN, RESULT OR PACKET FILE other than ONE NEW DESIGN DOCUMENT
  (protocol/rung2-escalation-v0.1.md).  Three scratch probes, one appended chat turn.
  *** IT TOUCHED NO REAL DATA AT ALL - no manifest, no .npz, no label payload, and NOT EVEN A
  HASH OF A .pt CHECKPOINT.  Every probe ran on SYNTHETIC TENSORS in the session scratch
  directory OUTSIDE the repository and wrote nothing into the project. ***
  *** THE SYNTHETIC OPTIMIZER STEPS IN THE COST AND LEARNABILITY PROBES ARE NOT DEVELOPMENT
      FITS AND SPEND NO BUDGET.  The standing precedent is tests/test_capacity_sweep.py,
      whose fits have always been synthetic steps at the real registry width.  SAY THIS
      EXPLICITLY WHENEVER A PROBE RUNS AN OPTIMIZER, or a later reader will read the fit
      counter and this session's prose as contradicting each other. ***
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S110 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, no
  plan mode at all, NO C7 INVOCATION and NO EDIT TO ANY EXECUTABLE, TEST, PROTOCOL, PLAN,
  RESULT OR PACKET FILE.  An owner re-review closing the last open loop, a 182-check
  re-derivation probe, one scratch-repo end-of-line experiment, one appended chat turn.
  *** IT TOUCHED NO REAL DATA AT ALL - no manifest, no .npz, no label payload, and NOT EVEN A
  HASH OF A .pt CHECKPOINT.  The probe READ EXACTLY TWO TRACKED JSON FILES
  (capacity_sweep_analysis.json and capacity_sweep_result.json) and wrote nothing; the
  end-of-line experiment copied ONE tracked markdown file into a scratch repo OUTSIDE the
  project.  The reviewed note was NEVER OPENED FOR WRITING and its blob was re-measured
  afterwards to confirm it. ***
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S109 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, no
  plan mode at all, NO C7 INVOCATION and NO EDIT TO ANY EXECUTABLE, TEST, PROTOCOL, PLAN,
  RESULT OR PACKET FILE.  An owner re-review of one reviewer-edited document plus three
  repairs to it, one independent five-part re-derivation probe, one post-edit mechanical
  re-parse of the finished table, one appended chat turn.  *** IT TOUCHED NO REAL DATA AT
  ALL - no manifest, no .npz, no label payload, and NOT EVEN A HASH OF A .pt CHECKPOINT.
  The probe READ EXACTLY TWO TRACKED JSON FILES (capacity_sweep_analysis.json and
  capacity_sweep_result.json) and wrote nothing. ***  Every probe lives in the session
  scratch directory OUTSIDE the repository and is deliberately NOT a packet script.
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S108 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, no
  plan mode at all, NO C7 INVOCATION and NO EDIT TO ANY EXECUTABLE, TEST, PROTOCOL, PLAN,
  RESULT OR PACKET FILE.  One new workspace document (the precision note), two appended chat
  turns, two scratch probes.  *** IT TOUCHED NO REAL DATA AT ALL - no manifest, no .npz, no
  label payload, and NOT EVEN A HASH OF A .pt CHECKPOINT.  The probes READ EXACTLY TWO
  TRACKED JSON FILES (capacity_sweep_analysis.json and capacity_sweep_result.json) and write
  nothing. ***  Both probes live in the session scratch directory OUTSIDE the repository and
  are deliberately NOT packet scripts.
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S107 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, no
  plan mode at all, NO C7 INVOCATION and NO EDIT TO ANY EXECUTABLE, TEST, PROTOCOL, PLAN OR
  RESULT.  An owner approval closing the ignore loop, one NEW packet file (.gitattributes),
  a 93-destination census, a fresh-repo replica sweep, an exhaustive 205-file negative
  control, a 13-call-site raw-hash enumeration, the 1,792 packet suite, two appended chat
  turns.  *** IT TOUCHED NO REAL DATA AT ALL - no manifest, no .npz, no label payload, and
  NOT EVEN A HASH OF A .pt CHECKPOINT.  The eol experiment copies ONE tracked 15 KB JSON
  file into a scratch repo and nothing else. ***  Every probe write went to the session
  scratch directory OUTSIDE the repository.
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S106 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, no
  plan PUBLICATION, NO C7 INVOCATION and NO EDIT TO ANY EXECUTABLE OR TEST.  An owner
  re-review of two reviewer-edited files, one repair to the packet ignore file, the 1,792
  packet suite, one appended chat turn.
  *** IT TOUCHED NO REAL DATA AT ALL - no manifest, no .npz, no label payload, and NOT EVEN A
  HASH OF A .pt CHECKPOINT.  Its two probes were a PLAN-MODE invocation (plan mode takes no
  --data-root) into a session scratch directory OUTSIDE the repository, and a claim_run_root
  drive inside a TemporaryDirectory. ***
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S105 SPENT ZERO OF EVERYTHING - documentation only; two packet README steps written, no
  script, test, protocol, plan or result file touched.
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S104 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, no
  plan artifact, NO C7 INVOCATION and NO EDIT TO ANY PACKET FILE.  An independent 73-check
  audit of the C7 terminal artifact, a 12-mutant whole-probe negative control, the 241 and
  1,792 suites, three appended chat turns and one Live-Run README entry.  Every probe was
  written to a SESSION SCRATCH DIRECTORY OUTSIDE THE REPOSITORY and every mutant write went
  to a TemporaryDirectory.  Working tree clean before and after.
  *** ITS REAL-DATA TOUCHES WERE NARROWER THAN S103'S: the fifty approved .pt checkpoints
  were opened ONLY TO HASH THEIR BYTES, and NO OBSERVATION PAYLOAD AND NO LABEL PAYLOAD WAS
  OPENED AT ALL - the audit re-derives every figure from persisted JSON plus digests, so it
  never needed the 304 dev rows. ***
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S103 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, no
  plan artifact, NO C7 INVOCATION and NO C7 ARTIFACT.  39 pre-authorization checks, the
  241 and 1,792 suites, and one appended chat turn carrying my C7 execution
  authorization half.  Every write outside the closeout documents and that one turn went
  to a TemporaryDirectory.  Working tree clean before and after.
  *** ITS REAL-DATA TOUCHES WERE READS ONLY: the 304 authorized dev rows (C1 152 + S
  152) loaded by load_development_context, and the FIFTY approved .pt checkpoints opened
  read-only to hash and to load weights for the re-scoring check. ***
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13.
      A READ IS NEITHER A ROLLOUT NOR A FIT. ***
MY S98 IS THE FIRST SESSION SINCE S84 TO SPEND ANYTHING, AND THE FIRST EVER TO SPEND A
  SWEEP FIT.  3 FITS (2 C9 equivalence + 1 curve arm), 3 CHECKPOINTS, 0 GENERATION,
  0 ROLLOUTS, 0 NON-DEVELOPMENT READS.  One execute-mode invocation, terminated at
  X_OUTPUT_DIRTY after 31.3 s.  Real-data touches: the approved assignment, the manifest,
  and the DEV observation and label payloads the three fits consumed (304 dev rows, both
  suites), plus the ten approved .pt checkpoints READ by C9 and hashed by the preflight.
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278.  A FIT IS NOT A ROLLOUT. ***
  *** THE FIT COUNTER IS NOW 13 LIFETIME: ten S84 development fits + three S98 sweep fits.
      The three S98 fits came out of the 42-fit Stage-1 budget, which is now SPENT ALONG
      WITH ITS PLAN - a re-run under a new authorization is a fresh 42, not 39. ***
MY S100 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, and NO
  PUBLISHED PLAN ARTIFACT and NO --mode execute INVOCATION.  A three-part audit of one JSON
  document (136 checks), an owner approval closing gate 2, my Step-4 authorization half, and
  one plan-mode determinism probe into a system-temp scratch dir.  Every write outside the
  closeout documents went to a TemporaryDirectory.  Working tree clean before and after.
  *** ITS REAL-DATA TOUCHES WERE READS ONLY: manifest.csv and the three index.csv files
  (to settle the digest domain), the ten approved .pt opened ONLY to hash their bytes, and
  the 304 authorized dev rows loaded by load_dev_examples as the last pre-spend check. ***
  PILOT/VAL/TEST: 0.  *** ROLLOUT COUNT UNCHANGED AT 278.  FIT COUNTER UNCHANGED AT 13. ***
MY S99 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, and NO
  PUBLISHED PLAN ARTIFACT.  *** AND IT TOUCHED NO REAL DATA AT ALL - no manifest, no .npz,
  no approved checkpoint, not even a hash of one.  Plan mode takes no --data-root, and the
  three invocations wrote ONLY into the system temp tree. ***  An owner re-review of one
  reviewer-edited test file, a TEN-CASE TWO-STATE mutation sweep run twice (every write to
  the executable restored in a finally, restore digest-verified be07d95e... both times), the
  full packet suite, and a three-destination plan-mode determinism measurement.  Working
  tree clean before and after.  PILOT/VAL/TEST: 0.
  *** THE ROLLOUT COUNT IS UNCHANGED AT 278.  THE FIT COUNTER IS UNCHANGED AT 13. ***
MY S97 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout, and NO
  PUBLISHED PLAN ARTIFACT (both review probes wrote to scratch destinations OUTSIDE the
  repository, and the tracked artifact was never opened for writing; git status was clean
  before the probes and clean after).  An independent audit of one JSON document plus a
  22-case gate-neighbour sweep, every mutant under a tempfile.TemporaryDirectory.
  *** ITS REAL-DATA TOUCHES WERE READS ONLY, AND ONLY OF manifest.csv AND THE THREE
  index.csv FILES, to settle the digest-domain question.  No observation payload and no
  label payload was opened; the ten approved .pt checkpoints were opened ONLY to hash
  their bytes. ***  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S96 SPENT ZERO OF EVERYTHING - no manifest, no .npz, no approved .pt checkpoint, no
  regeneration, no fit, no generation, no rollout, AND NO PLAN MODE AT ALL.  An owner
  re-review of two files, two tests added and no production line touched, and an
  eight-case mutation sweep whose every write was to capacity_sweep.py itself, restored
  in a finally with the restore digest-verified.  Its only reads of tracked results files
  were dev_fit_result.json and dev_fit_analysis.json, through the suite's fixtures.
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S95 SPENT ZERO OF EVERYTHING - no fit, no checkpoint, no generation, no rollout.  It
  ran PLAN MODE three times (two scratch destinations plus a reproduction of the
  published artifact) and plan mode takes no --data-root, so it read no data root at all.
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S74 SPENT ZERO — the whole audit is a read of persisted fields.
MY S75 SPENT ZERO — drafting only; no plan mode, no replay, no execute mode.
MY S76 SPENT ZERO — two-document review; no script/test/protocol/config/result touched.
MY S77 SPENT ZERO — built the Gate-4 rung; no plan mode, no execute mode, no replay gate,
  no generation.  Every real-data touch was a READ of one persisted observation row.
MY S79 SPENT ZERO — owner re-review of Codex's contract repair.  NO REAL DATA READ AT ALL:
  no manifest, no .npz, no checkpoint, no fit, no generation.
MY S94 SPENT ZERO OF EVERYTHING - no manifest, no .npz, no approved .pt checkpoint, no
  regeneration, no fit, no generation, no rollout, no plan artifact.  An owner re-review
  of two files plus one repair, one new test, a four-case mutation sweep with two
  negative controls, and one probe harness.  Every write outside the two reviewed files
  was under a pytest tmp_path or the harness's own restore.  *** ITS ONLY READS OF
  TRACKED RESULTS FILES were dev_fit_result.json and dev_fit_analysis.json, through the
  suite's fixtures - Codex's S93 precision correction, which I accepted. ***
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S93 SPENT ZERO OF EVERYTHING AND TOUCHED NO REAL DATA AT ALL - no manifest, no
  .npz, no checkpoint, no regeneration, no fit, no generation, no rollout, no plan
  artifact, and NOT EVEN A READ OF A TRACKED RESULTS FILE.  An owner re-review of two
  files plus three repairs, three new tests, an eleven-case mutation sweep, and one
  probe script.  Every write it made was under a pytest tmp_path or a
  tempfile.TemporaryDirectory, INCLUDING the demonstration of the C1 gap, which used a
  redirected packet_root() so nothing went near the real results/dev_fit.
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S92 SPENT ZERO OF EVERYTHING AND TOUCHED NO REAL DATA AT ALL - no manifest, no
  .npz, no checkpoint, no regeneration, no fit, no generation, no rollout, and NO PLAN
  ARTIFACT.  It BUILT the capacity-sweep executable and its tests.  Its only reads of
  tracked results files were dev_fit_result.json and dev_fit_analysis.json.
  *** THE FITS IN ITS TESTS ARE SYNTHETIC - two-example, one-epoch optimizer steps on
  random arrays at the real registry width, which is exactly what
  test_dev_fit_trainer.py has always done.  A synthetic optimizer step is NOT a
  development fit and does not touch the 42-fit budget. ***
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S91 SPENT ZERO OF EVERYTHING AND TOUCHED NO REAL DATA AT ALL - no manifest, no
  .npz, no checkpoint, no regeneration, no fit, no generation, no rollout, and no read of
  a tracked results file.  An owner re-review of one document plus three read-only probes:
  the cited precedent read at dev_fit_trainer.py:1134-1172, the run_label regex read at
  the design's line 651, and a grep sweep confirming no test pins the design's digest.
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S90 SPENT ZERO OF EVERYTHING AND TOUCHED NO REAL DATA AT ALL - no manifest, no
  .npz, no checkpoint, no regeneration, no fit, no generation, no rollout, and this time
  not even a read of a tracked results file.  An owner re-review of one document plus
  three read-only probes: the copied loop re-enumerated at source, the trainer's CLI read
  for --output-dir, and C9's constructor precondition measured on synthetic tensors.
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S89 SPENT ZERO OF EVERYTHING AND TOUCHED NO REAL DATA AT ALL - no manifest, no
  .npz, no checkpoint, no regeneration, no fit, no generation, no rollout.  An owner
  re-review of two documents plus four read-only probes (constructor map, code_identity
  cardinality, the approved ledger's arms, the payload gate's source).  Its only reads of
  tracked results files were dev_fit_result.json and dev_fit_analysis.json.
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S88 SPENT ZERO OF EVERYTHING AND TOUCHED NO REAL DATA AT ALL - no manifest, no
  .npz, no checkpoint, no regeneration, no fit, no generation, no rollout.  An explicit
  owner approval, a design revision, and four constructor/synthetic probes.  Its only
  reads of a tracked results file were of dev_fit_analysis.json.  PILOT/VAL/TEST: 0.
  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S87 SPENT ZERO OF EVERYTHING AND TOUCHED NO REAL DATA AT ALL - no manifest, no
  .npz, no checkpoint, no regeneration, no fit, no generation, no rollout.  An owner
  re-review, a four-case mutation sweep over test fixtures, and a design document.
  PILOT/VAL/TEST: 0.  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S86 SPENT ZERO OF EVERYTHING AND TOUCHED NO REAL DATA AT ALL — no manifest, no .npz,
  no checkpoint, no regeneration, no fit, no generation, no rollout.  A review session
  plus a mutation sweep over test fixtures.  PILOT/VAL/TEST: 0.
  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S85 SPENT ZERO ROLLOUTS, ZERO FITS, ZERO CHECKPOINTS, ZERO GENERATION.  Its only
  real-data touch is ONE regeneration of the analysis artifact, which READS the 304
  authorized dev rows and the ten checkpoints and runs no simulation.  PILOT/VAL/TEST: 0.
  *** THE ROLLOUT COUNT IS UNCHANGED AT 278. ***
MY S84 SPENT ZERO ROLLOUTS — but it is the FIRST session that spent anything else:
  the ten development fits RAN.  10 fits, 10 checkpoints, 0 rollouts, 0 generation.
  Real-data touches: the approved assignment, the manifest, and the DEV observation
  and label payloads the fit consumed (304 dev rows, both suites).  PILOT/VAL/TEST: 0.
  *** THE ROLLOUT COUNT IS UNCHANGED AT 278.  A FIT IS NOT A ROLLOUT — it reads
  persisted rows and runs no simulation.  Do not let the two counters merge. ***
MY S83 SPENT ZERO — owner re-review of Codex's trainer repair (round 2).  Real-data
  touches were READS ONLY: the manifest (304 dev rows) and the approved assignment.
  ZERO observation payloads, ZERO label payloads, ZERO checkpoints.  No fit, no
  generation.  PILOT/VAL/TEST: 0 reads of any kind.
MY S82 SPENT ZERO — owner re-review of Codex's trainer repair, plus the training-window
  policy.  Real-data touches were READS ONLY: manifest, approved assignment, draft
  config/schema, three role indexes, four dev observation+label payloads.  No fit, no
  checkpoint, no generation.  PILOT/VAL/TEST: 0 reads of any kind.
MY S81 SPENT ZERO — owner re-review round 4 (loop CLOSED) plus building the trainer.
  NO REAL DATA READ AT ALL: no manifest, no .npz, no checkpoint, no fit, no generation.
  The trainer has NEVER been run against the delivered dataset.
MY S80 SPENT ZERO — owner re-review round 3, plus the S73-S80 progress report.  NO REAL
  DATA READ AT ALL: no manifest, no .npz, no checkpoint, no fit, no generation.
MY S78 SPENT ZERO — owner re-review plus the dev-fit contract.  No fit, no checkpoint, no
  generation.  Every real-data touch was ONE read of manifest.csv; no .npz was opened.
```
