# Summary of Only Necessary Context - Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 141, 2026-08-15.*

**S112 SPLIT THIS FILE, AND THAT IS THE FIRST THING TO KNOW ABOUT IT.** It was ~3,430 lines and ~400 KB, and reading it was the single largest cost of starting a session — in tension with its own stated purpose. **Codex approved the split in its S111** with one binding condition: *the current gate map, the current exact-state handoff, and the next-read routing stay here.* So this file is now **current state + gates + routing**, and every permanent instrument moved **verbatim, not summarized** into:

> ### `agents/Claude/Permanent Instruments.md`  ← READ ON DEMAND, NOT AT STARTUP
> It holds the audit sets, the append-gate list, the closed findings and their lessons, the executable and C7 descriptions, the numbered limitations, and the standing lessons. **The routing table at the bottom of this file says which section answers which question.** Nothing was deleted in the split — the move was done by a script that reproduces each section byte-for-byte and verifies it.

**DO NOT UNDO THE SPLIT BY DRIFTING CONTENT BACK.** If a permanent instrument improves, the improvement goes into **the block that owns it in the reference file** — that is the S105 correction, and it is the reason the append writer's last five rebuilds were faithful. Only *current state* belongs here.

## S142 FIRST - 4b-ii-a IS UNDER REVIEW AND 4b-ii-b IS THE ONLY UNBUILT WORK.

```text
*** THE REVIEW METHOD IS THE DIRECTOR'S SUPERSEDING PROTOCOL, appended to
    `Playbooks/review-cycle.md`, WHICH OVERRIDES THE REST OF THAT PLAYBOOK.  READ IT BEFORE ANY
    REVIEW WORK.  The short form: THE OWNER WRITES A REVIEW CARD in the root `Review Card/` folder
    before review begins; ROUND 1 IS THE ONLY FULL-ARTIFACT REVIEW and records EVERY reasonably
    discoverable finding in ONE numbered ledger; ROUND 2 AND LATER ARE DELTA-ONLY; a new
    pre-existing blocker after Round 1 is a LATE-BLOCKER and must say why it was missed; AT MOST
    THREE OWNER-REVIEWER ROUND-TRIPS and THE LIMIT NEVER FORCES APPROVAL.  Reviewers apply
    MECHANICAL corrections directly and PROPOSE substantive ones - JUDGED BY EFFECT, NOT BY EDIT
    SIZE.  Once both agents approve the scoped candidate THE REVIEW CLOSES and later implementation,
    amendments, data gates or versions get NEW CARDS AND NEW CHATS.
    *** `Escalated` IS GONE AS OF S140.  THE CONVERGENCE LADDER REPLACED IT AND IT IS WRITTEN INTO
    `Playbooks/review-cycle.md` (section "Convergence at the round limit") AND `Review Card/README.md`.
    IT IS AGREED BY BOTH AGENTS - DO NOT TREAT IT AS MY PROPOSAL AND DO NOT RE-PROPOSE IT.  The
    shape: the turn that first hits the limit in disagreement CLASSIFIES the residual issue FACTUAL
    or JUDGMENT in that same turn (differing classifications make it judgment); FACTUAL -> ONE probe
    both agents commit to IN WRITING BEFORE IT RUNS, one counterproposal permitted, INCONCLUSIVE
    BECOMES JUDGMENT, and *** THE PROBE MAY SPEND NO GATED OR OTHERWISE UNAUTHORIZED RESOURCE - a
    disagreement is never a door around a gate ***; JUDGMENT -> EXACTLY ONE narrowing split into a
    card carrying both positions verbatim, ONE owner handoff + ONE reviewer response + ONE owner
    re-review, no re-split, NO FRESH ROUND ALLOWANCE, and uncontested material closes only as an
    EXACT CANDIDATE STATE both approve (prose is not a separation); if that does not converge THE
    CONTESTED ELEMENT DOES NOT SHIP - and on an APPEND-ONLY artifact the withholding is a FORWARD
    CORRECTION OR AN OMISSION, NEVER A REWRITE.  Terminal outcomes `Approved - Contested Element
    Withheld` and `Withheld - Contested Candidate Not Adopted`; the director notice is NON-BLOCKING
    and reinstatement is a NEW candidate under a NEW card.  CEILING from the classification turn:
    FACTUAL at most TWO further agent sessions, JUDGMENT at most THREE. ***
    *** FOUR OPERATING RULES BIND ME: (1) name every tracked candidate state THREE WAYS - full blob
    id, raw SHA-256, size/line-endings - and RESOLVE EVERY BLOB ID WITH `git cat-file -t` BEFORE THE
    CARD GOVERNS; (2) acceptance criteria name DURABLE ARTIFACT PROPERTIES, never one agent's
    private audit count; (3) an owner delta response NAMES WHAT CHANGED **AND** WHAT IS
    BYTE-IDENTICAL, with machine-checkable evidence; (4) QUOTE `git diff --numstat` BESIDE THE
    REGION MAP, NEVER A HAND-COUNTED TOTAL (Codex's S138 correction against me). ***

*** THE PROJECT STATE IN ONE LINE: EVERY SCIENTIFIC LANE IS STILL SPENT OR SHUT; SLOT-8 STEPS 1, 2,
    3, 4a AND SUB-STEP 4b-i ARE CLOSED AT BOTH APPROVALS; SUB-STEP **4b-ii-a IS BUILT AND HANDED
    OFF FOR ROUND 1**; AND THE ONLY UNBUILT WORK IN THE PROJECT IS **4b-ii-b**.  *** THERE IS NO
    SECOND LANE. ***

*** S141 SPLIT THE 4b-ii REVIEW IN TWO AND CODEX HAS NOT RULED ON THE SPLIT YET.  DO NOT TREAT THE
    SPLIT AS SETTLED AND DO NOT BUILD 4b-ii-b UNTIL EITHER (a) CODEX ACCEPTS THE SPLIT, OR (b) YOU
    HAVE READ ITS RESPONSE AND KNOW WHAT IT RULED.  IF IT REJECTS THE SPLIT, THE CANDIDATE COMES
    BACK UNREVIEWED AND THE RIGHT MOVE IS TO ASK WHAT BOUNDARY IT WANTS, NOT TO RE-ARGUE MINE. ***

=== WHAT S141 DID, SO S142 DOES NOT REDO IT ===================================================
  1  BUILT 4b-ii-a - READ-ORDER ROWS 4 THROUGH 12 - AS **TWO NEW FILES**.  No closed blob was
     edited, no tracked artifact regenerated, no protocol document touched.
  2  SPLIT THE 4b-ii REVIEW, taking the boundary from section 4.1's own SECOND BOUNDARY.  New card,
     new chat, and the split is THE FIRST THING CODEX IS ASKED TO RULE ON.
  3  DISCHARGED B8 IN FULL and DELIBERATELY DID NOT CLAIM B4 / THE AUDIT-HOOK OBSERVER.
  4  RAN THE TWO-PASS MUTATION SWEEP BEFORE THE HANDOFF.  IT FOUND FOUR SURVIVORS AND ONE OF THEM
     WAS A PRODUCTION DEFECT OF MINE.  See below.
  *** S141 SPENT ZERO SCIENTIFIC RESOURCE.  It opened no role payload, checkpoint, estimator
      output, controller log, production config or pilot/val/test result; built no MuJoCo model;
      stepped no rollout; ran no fit; rendered no figure.  Counters unchanged: 278 rollouts, 67
      fits, 67 checkpoints, zero pilot/val/test reads.
      *** ONE DISCLOSED READ OF DELIVERED METADATA: the two dataset audit files in the delivered
      role root (generation_audit.json 1,256 B, independent_audit.json 1,470 B) were read ONCE to
      learn the shape the step-6 contract had to be written against.  Same kind of read S132 made.
      NO PAYLOAD BEHIND THEM WAS OPENED AND NO TEST DEPENDS ON THAT TREE EXISTING (finding DB). ***
      *** THE PACKET-WIDE SUITE IS NOW **2,717** (0 failed, 169.01 s).  2,608 + 109 = 2,717
      EXACTLY, WHICH IS WHAT SAYS THE CANDIDATE ADDS TESTS AND CHANGES NO EXISTING ONE. *** ***

=== THE OPEN REVIEW - 4b-ii-a.  MINE, HANDED OFF, AWAITING CODEX'S ROUND 1 ========================
  Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md            <- OPEN, Round 1 handed off
  chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/...- Active.md
  Reproducibility Packet/scripts/utils/connection_adapter.py
    blob dafa73b5f12a3aded79b707777758547785d274e
    raw  c694dd2a81574441dc21d5e9f836ccbe74e46915f61024c2c1d0e44d38af0f80  70,511 B / 1,635 LF
  Reproducibility Packet/tests/test_connection_adapter.py
    blob 9cadb11da061d9793f01c3c8dfd58baf6ba97b76
    raw  c189e0ceca7fe223833c7cbdc844e4f3d9539e7c260b3983bcd54192e81a571d  77,397 B / 1,909 LF
                                                                          109 tests
  *** BOTH ARE `*.py`, CODEX'S S128 NO-EOL-PIN RULING STANDS, `core.autocrlf` IS TRUE HERE, SO A
      FRESH WINDOWS CHECKOUT RENDERS THEM CRLF AND ITS WORKING-TREE DIGEST IS A THIRD NUMBER THAT IS
      NOBODY'S IDENTITY.  COMPARE THE BLOBS.  Nothing in the packet hashes either file at runtime. ***
  *** SUPERSEDED: NONE.  This is the first state under this card. ***

  THE SPLIT, AS I ARGUED IT.  DO NOT RE-DERIVE IT; IT IS IN THE CARD AND THE CHAT:
    4b-ii-a  rows 4-12, the W8 roles-mode entry point, B8 IN FULL, the B3 rows for 4-12, W1 (rows
             4-12), W4, W5, W8, W11 and W6's config/audit half                    UNDER REVIEW
    4b-ii-b  rows 13-21, the coherent geometry fixture, X_GEOMETRY_UNSUPPORTED at 15, the
             audit-hook observer (W3/B4), B2, B5, the remaining B3 rows, the roles CLI wiring, the
             additive build_role_bundle change (incl. its stale `--config` docstring gloss),
             W9, W10, W13, W14                                                    NOT STARTED
  *** SUB-STEP 4b NOW CLOSES ON THREE CARDS: 4b-i + 4b-ii-a + 4b-ii-b.  NO GATE, PRECONDITION,
      INVARIANT, EXIT CODE OR AUTHORIZATION MOVES.  Lesson 224 applied a second time. ***
  *** THE TWO THINGS I SAID OUT LOUD BECAUSE BOTH CUT AGAINST ME, AND A LATER SESSION MUST NOT
      QUIETLY DROP EITHER:
      1  B4 AND THE AUDIT-HOOK OBSERVER ARE NOT DISCHARGEABLE HERE AND ARE NOT CLAIMED.  W3 compares
         the expected set against what a hook observed FOR THE DURATION OF ONE ADAPTER CALL, and
         there is no complete call until row 21 exists.  4b-ii-a carries only the EXPECTED side.
      2  B8 *IS* DISCHARGEABLE HERE BECAUSE ITS POSITIVE LEGS STOP AT A STEP-5 REFUSAL, so it is
         discharged here rather than left half-open across two cards. ***

  WHAT THE BUILD DECIDED, ALL THREE RECORDED IN THE MODULE DOCSTRING, NOT ONLY IN A REPORT:
    1  *** THE AUTHORITY RULE IS THE ADAPTER'S OWN AND `require_frozen` IS NOT IT. ***
       `require_authority_config_policy` is TOTAL over the 2x2 and is driven directly over all four
       cells.  IT EARNED ITS KEEP: B8's two opposite-authority legs FIRE AT DIFFERENT LAYERS - leg 2
       (draft under FINAL) refuses INSIDE `load_config`, leg 4 (frozen under DEVELOPMENT_ONLY)
       refuses in the adapter's own rule, because `require_frozen=False` ACCEPTS A FROZEN DOCUMENT.
    2  "CASE AND RUN IDENTITIES" ARE CHECKED WHERE THEIR EVIDENCE IS.  Case identity = exact set
       equality against `cases_field_path`, duplicates refused.  RUN identity is NOT a field of the
       result artifact (the field table names no `runs_field_path`), so it is checked against the
       AUTHENTICATED MANIFEST at row 6 and by the 20-field equality at row 10.  *** FLAGGED TO CODEX
       AS THE INTERPRETATION MOST LIKELY TO BE READ DIFFERENTLY.  If it wants something stronger,
       BUILD IT; do not defend the reading. ***
    3  THE CENSUS IS RECOMPUTED, NEVER ADOPTED - all six fields from `manifest.csv` itself, plus the
       two audits' `manifest_audit` blocks required EQUAL TO EACH OTHER.

  THE DIGEST DOMAINS, WHICH CONSUME FORWARD ITEM 1 AND DO NOT REOPEN IT:
    CANONICAL (`canonical_text_sha256`)  every TRACKED PACKET TEXT file - schema, config, established
                                        result, model-selection source, both threshold sources, the
                                        geometry PRODUCER and the geometry-validation artifact
    RAW (`storage_contract.file_sha256`) every file under `--role-root` and `--checkpoint-root`
  *** THE RAW HALF IS FORCED, NOT PREFERRED: the role index rows carry RAW digests and row 11 must
      compare the record AGAINST THE AUTHENTICATED INDEX ROW, so a different domain there would
      compare two numbers that were never meant to be equal. ***
  *** ONE INTERACTION, NAMED SO NOBODY REDISCOVERS IT AS A DEFECT: `validate_config_document`
      compares the config's declared `schema_sha256` against the schema's RAW bytes while the record
      declares the schema's CANONICAL digest.  TWO DIFFERENT FIELDS WITH TWO DIFFERENT OWNERS; they
      need not be equal, AND ON `schema/schema.json` THEY ARE EQUAL ANYWAY because that one file is
      LF-pinned as load-bearing in BOTH `.gitattributes`.  The closed config contract is undisturbed. ***

  *** THE MUTATION SWEEP FOUND FOUR SURVIVORS ON ITS FIRST RUN AND ONE WAS MY PRODUCTION CODE.
      FINAL: 29 mutants (27 real + 2 negative controls), 27/27 REAL CAUGHT, BOTH CONTROLS SURVIVING,
      IDENTICAL ACROSS BOTH PASSES, no bad anchors, target digest restored after every mutant, run
      ENTIRELY IN A SCRATCH DIRECTORY OUTSIDE THE REPOSITORY (deleted).
      THREE WERE ONE SHAPE - MY GREEN WAS OWED TO A **LATER** GUARD REFUSING THE SAME INPUT (lesson
      241): the FINAL-requires-frozen check (a realistic draft also carries `dev-`), the row-4
      `config_hash` comparison (row 5 echoes the DECLARED hash), and the recursive finiteness walk
      (bare NaN/Infinity are caught by `parse_constant`; THE REACHABLE PATH IS `1e9999`, which
      `json` turns into `inf` inside its own number parser).
      THE FOURTH WAS A DEFECT: `require_role_layout` guarded that the role DIRECTORY existed above a
      guard on its `index.csv`.  *** THE INDEX PATH IS A CHILD OF THE ROLE ROOT, so an absent or
      non-directory root fails the CHILD guard in every case; the parent guard could never be the
      only check to refuse.  DELETED, WITH THE PROOF WRITTEN WHERE IT STOOD.  Lesson 239. ***
      *** THIS IS THE FOURTH CONSECUTIVE BUILD ON THIS LANE WHERE THE SWEEP CHANGED THE TESTS RATHER
      THAN CONFIRMING THEM.  BUDGET IT BEFORE THE HANDOFF FOR 4b-ii-b TOO. *** ***

=== THE NEXT BUILD - 4b-ii-b, NOT STARTED =========================================================
  ROWS 13-21 + the coherent geometry fixture + `X_GEOMETRY_UNSUPPORTED` at exit 15 + the audit-hook
  observer (W3/B4) + B2 + B5 + the remaining B3 rows + the roles CLI wiring + the ADDITIVE
  `build_role_bundle` change.  IT NEEDS A NEW REVIEW CARD AND A NEW SUBJECT CHAT, WRITTEN BEFORE THE
  HANDOFF, AND ITS MUTATION SWEEP BUDGETED **BEFORE** THE HANDOFF.
  *** `build_role_bundle` STILL REFUSES UNCONDITIONALLY WITH `X_CONNECTION_UNAUTHORIZED` AND THAT IS
      THE CORRECT STATE UNTIL THE WHOLE OF 4b CLOSES.  4b-ii-a CHANGED NO PUBLIC SURFACE. ***

FORWARD ITEM 1 WAS SETTLED BY MEASUREMENT (S139) AND **THE 4b-ii-a BUILD HAS NOW CONSUMED IT**
(S141: every tracked packet text file is hashed with `canonical_text_sha256`, every role-root and
checkpoint-root file raw).  KEPT HERE BECAUSE 4b-ii-b HASHES THE SAME KINDS OF FILE.  IT DOES NOT
REOPEN THE QUESTION:
  *** `render_geometry.source.producer_sha256` AND EVERY OTHER RUNTIME DIGEST THE ADAPTER TAKES
      OVER A **TRACKED TEXT FILE** USE `canonical_text_sha256`.  NOT A RAW DIGEST, AND NOT A NEW
      EOL PIN. ***
  WHAT I MEASURED, AND THE FIRST ROW IS THE DANGEROUS ONE:
    tracked blob == this working tree   20,987 B / 527 LF / 0 CR
                                        raw `1acaf60c...`  canonical `1acaf60c...`  <- THE SAME
    fresh checkout (`git checkout-index`)  21,514 B / 527 LF / 527 CR
                                        raw `58adb3fb...`  canonical `1acaf60c...`
  *** A RECORD AUTHORED ON THIS MACHINE RECORDS THE IDENTICAL NUMBER UNDER EITHER RULE.  The two
      designs are INDISTINGUISHABLE by anything comparable on this hardware, and a raw rule is
      GREEN HERE AND RED ON A CORRECT FRESH WINDOWS CLONE.  The instrument that sees this class is
      A FRESH CHECKOUT, not a test and not a review of the number.  Lesson 232. ***
  FOUR SUPPORTS, NONE OF THEM MY PREFERENCE:
    1  Requirement X11 / (cc), in `protocol/payload-boundary-extension-v0.2.md`: every digest a
       result artifact records is taken in the DOMAIN OF THE FILE'S KIND - canonical for tracked
       text, raw only for binary.
    2  The ROOT `.gitattributes` says it about itself: the pins "are not what makes a digest
       portable"; they are DEFENCE IN DEPTH.
    3  DIRECT PRECEDENT FOR HASHING `.py`: `dev_fit_contract.code_identity` uses the TEXT domain,
       with the reason in its docstring - "a raw digest of a tracked text file is a digest of the
       COPY, not of the DOCUMENT".
    4  EVERY runtime digest of a tracked text file in the packet already uses
       `canonical_text_sha256` (measured: analyze_capacity_sweep, analyze_dev_fit,
       analyze_protocol_p_payload_conditioning, analyze_protocol_p_role_coverage,
       analyze_rung2_escalation).
  *** AND IT LEAVES CODEX'S S128 RULING STANDING.  That ruling declined a `*.py` EOL pin on the
      PREMISE that no packet runtime hashes those files.  Step 5 ends the PREMISE; choosing the
      canonical domain preserves the CONCLUSION for a better reason.  A FORWARD CORRECTION TO A
      PREMISE, NOT A REVERSAL OF A RULING - say it that way to Codex.  Lesson 233. ***
  A PIN PROTECTS THE ONE FILE IT NAMES; THE DOMAIN RULE PROTECTS EVERY FILE THE ADAPTER WILL EVER
  HASH, INCLUDING THE ONES NOBODY HAS PINNED YET.

FORWARD ITEM 2 NEEDS NO MEASUREMENT AND CARRIES INTO THE 4b-ii CARD AS WRITTEN: the source-class
interpretation below (design 3.2 requires a jointly-present structure/actuator/sensor case, there is
NO `source_class` field, and a case's class is carried by its authenticated `labels` payload).

STEP 4a IS CLOSED AND IS NOT TO BE REOPENED.
  Reproducibility Packet/protocol/slot8-connection-record-v0.1.md
    blob   032db1666efbe00adec5696de70424d531ba33a2
    raw    f761a673ff8fcca6c58fe530a3faaed57630315a87a5e241d8ca9675a13c4ffc
    83,181 B / 1,062 LF / 0 CR / no BOM / final newline / LF-pinned by `protocol/*.md`
    APPROVED BY ME S135 AND BY CODEX S135 AT THE SAME BYTES.  Card outcome: **Approved**.
  *** READ THE FILE.  IT IS THE SPEC FOR EVERYTHING 4b BUILDS and this block is an index.  It is
      authoritative on the field table (3.2), the six load-bearing properties (3.3), the 21-row
      READ ORDER (4.1), the allowlist rule (4.2), the reuse table (4.3), the output rules (4.7),
      invariants W1-W14, acceptance tests B1-B8, decisions E1-E4 and Codex's rulings (9.1), and
      findings CU, CV, CW, CX, CY/CZ, DA, DB, DC, DD and DE in sections 9.2-9.6.  ALL OF THOSE ARE
      SETTLED.  DO NOT RE-LITIGATE ANY OF THEM AND DO NOT SUMMARISE THEM FROM MEMORY. ***
  *** AN APPROVED VERSION IS NEVER EDITED IN PLACE; a correction bumps the version and `git mv`s.
      SUPERSEDED, never review or build from: `d9ad2169`, `8d06792c`, `12b6240b`, `fab21261`,
      `806d6fb9`, `b968886f`, `968fa895fb81`, `425ce011`. ***
  THE CHAT IS CONCLUDED: `chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/`.

THE SCOPE-EXPANSION RULE IS ADOPTED AND HAS NOW BEEN USED ONCE END TO END.  An owner may PROPOSE an
out-of-card repair as an authenticated, bounded scope expansion with the prior state named and
revert offered, and THE REVIEWER RULES SCOPE BEFORE CONTENT.  It is in `Playbooks/review-cycle.md`
and `Review Card/README.md`.  *** THE LESSON THE RULING CARRIES: WIDENING THE CARD BOUGHT ME
NOTHING - Codex accepted the scope and blocked the content in the same turn.  That separation is
the point. ***

CODEX'S ONE ROUND-2 FINDING - ACCEPTED WITHOUT CONTEST, INTEGRATED, AND ALL THREE OF ITS STATES
RE-DRIVEN BY ME AGAINST THE PRE-REPAIR BYTES FIRST.  DO NOT RE-LITIGATE IT:
  *** CONTAINMENT IS NECESSARY AND IS NOT SUFFICIENT.  The composed output namespace was neither
      LENGTH-BOUNDED nor ONE-TO-ONE, and all three states passed every containment check. ***
  WHAT I MEASURED AGAINST THE ROUND-2 BYTES, AND THE NUMBERS ARE THE PART TO CARRY:
    251-char `case_id`      THREE FILES WRITTEN (bundle json, its .sha256, the case PNG) and then
                            a RAW `OSError` [Errno 22] on the 256-char scene JSON.  A PARTIAL
                            PUBLICATION produced by the helper whose docstring said it validated
                            the complete set BEFORE writing.
    `verification_bundle`   ACCEPTED.  `verification_bundle.json` on disk held the SCENE document
                            and digested `3f1fab04...` while the manifest returned
                            `bundle_sha256 = 608fd5ce...`.  *** TWO DIFFERENT NUMBERS: the digest a
                            reader is told to check no longer hashed the file it names. ***
    `Case-A` + `case-a`     ACCEPTED.  Manifest reported FOUR cases; the directory held EIGHT files.
  WHAT IS IN THE CANDIDATE NOW, AT TWO INDEPENDENT LAYERS:
    RECORD BOUNDARY  `MAX_PORTABLE_COMPONENT_CHARS = 255` on every component of every declared
      path, and `MAX_CASE_ID_CHARS = 250` on `case_id` - 255 LESS THE LONGEST SUFFIX THE RENDERER
      APPENDS, because bounding the TOKEN at the filesystem limit accepts a token whose every
      DERIVED name is over it.  `_parse_cases` claims the two fixed bundle names BEFORE reading a
      case, then records `folded derived name -> claiming case_id`.
    WRITE BOUNDARY   `_contained_output_paths` re-enforces both: `MAX_OUTPUT_NAME_BYTES = 255` in
      UTF-8 BYTES and pairwise distinctness under the same fold, before containment and all of it
      before the first write.  *** THE LAYER IS INDEPENDENT BY CONSTRUCTION - the renderer imports
      NOTHING from `utils.connection_record`, so deleting either rule leaves the other standing.
      DO NOT "DE-DUPLICATE" THEM. ***
  THREE DECISIONS INSIDE THE REPAIR, ALL DELIBERATE:
    1  `_portable_fold` IS `str.lower`, NOT `str.casefold`.  They agree exactly over the ASCII
       grammar the record allows, and `casefold` would map characters the grammar already refused.
    2  THE RENDERER COUNTS UTF-8 BYTES, ONCE.  My first version took
       `max(len(name), len(name.encode()))` for ext4's bytes and NTFS's UTF-16 units.  *** THAT
       MAXIMUM IS ALWAYS THE BYTE COUNT - a string's UTF-8 length is never below its UTF-16 length -
       so the first term was a branch nothing could distinguish from its deletion, which is finding
       5's own defect shape.  Lesson 231.  DO NOT REINTRODUCE THE SECOND TERM. ***
    3  THE TWO FIXED BUNDLE FILENAMES AND THE TWO DERIVED SUFFIXES ARE LITERALS IN THE CONTRACT
       MODULE, PINNED BY EQUALITY against the TRACKED Step-3 figure set
       (`test_bundle_output_names_equal_the_published_write_set`).  Importing the renderer would
       pull matplotlib into a module that opens nothing and draws nothing.  Same discipline
       `ROLE_NAMES` gets against `schema.json`.
  *** A CONSEQUENCE FOR THE MUTATION SWEEP'S STAGING SET: THAT TEST READS
      `results/verification_fixture/`, SO A STAGED TREE MUST NOW CARRY `scripts`, `tests`, `schema`
      AND `results/verification_fixture` - four, not three.  A staged tree missing it is a RED
      CONTROL AND MEASURES NOTHING. ***

CODEX'S FIVE ROUND-1 FINDINGS - ALL ACCEPTED WITHOUT CONTEST, ALL INTEGRATED, ALL RE-DRIVEN BY ME
AGAINST THE ROUND-1 BYTES BEFORE REPAIR, AND CODEX CLOSED 1, 2 AND 3 ON THE ROUND-2 DELTA.
DO NOT RE-LITIGATE ANY OF THEM:
  1  THE RECORD'S OWN LOCATION WAS NOT BOUND AND WAS MISSING FROM W3's EXPECTED SET.
     `bind_root_domains` now takes `connection_record_path` and requires it to resolve to
     `packet_root / record_relative_path(record_label)`, PROVED CONTAINED via `_resolve_under`;
     `BoundPaths.record_path` carries it; `expected_open_set` includes it.  Code
     `X_IDENTITY_MISMATCH`.  *** THE POINT I HAD BACKWARDS: STEP 1 *OPENS* THE RECORD, so an
     expected set without it is unequal to any honest observed set - 4b-ii would have gone red for
     a CORRECT adapter, or been "fixed" by filtering the OBSERVED side. ***
  2  `frozen=True` IS SHALLOW.  Every nested dict was mutable, so an authenticated record could be
     edited into a different allowlist without touching a hashed byte.  Now `_freeze` (deep:
     `MappingProxyType` + tuples) on `document`, and `_frozen_mapping` (read-only view over a
     COPY) on `Case.arms`, `Arm.roles`, `Arm.manifest_row`, `RenderGeometry.links`,
     `ThresholdsRef.sources` AND all three `BoundPaths` mappings.  Lesson 227.
     *** CONSEQUENCE TO CARRY: arrays are TUPLES, so `record.document == source_dict` is FALSE
     wherever an array appears - freeze the source to compare.  And `json.dumps` CANNOT serialise a
     `MappingProxyType`; the record's canonical bytes already exist and are the answer. ***
  3  THE FINITE-NUMBER GATE WAS NOT TOTAL.  `10**400` passes the non-finite walk (it only inspects
     floats) and made `float()` raise a RAW `OverflowError`.  `_require_finite_float` now guards the
     conversion and translates it into `X_CONNECTION_UNAUTHORIZED`.  *** `1e9999` IS A DIFFERENT
     PATH - `json.loads` turns it into `inf` inside the parser and it never reaches the conversion. ***
  4  THE PATH RULE REFUSED TRAVERSAL BUT NOT NON-PORTABLE SPELLINGS, AND CONTAINMENT WAS PARTIAL.
     Now a portable component grammar (`[A-Za-z0-9._-]+`, no trailing dot, no reserved DOS device
     stem) on every component; `_resolve_safely` translating every resolution failure into the named
     refusal; and `_resolve_under` on the authority output parent, the record location AND the
     output root.  Lesson 226 carries the four measurements.
  5  `case_id` REACHED THE SHARED RENDERER AS A FILENAME.  Two layers: a portable leaf token at the
     record boundary, and `render_bundle` resolving its COMPLETE write set through ONE
     `_contained_output_paths` call BEFORE THE FIRST WRITE.  *** ONE CALL, NOT A GUARD PER WRITE:
     two duplicated guards have branches no test can distinguish. ***

THREE DECISIONS I TOOK THAT THE DESIGN LEFT TO THE BUILD.  CODEX'S ROUND-1 LEDGER DID NOT CONTEST
ANY OF THEM, SO THEY STAND UNLESS ROUND 2 SAYS OTHERWISE:
  1  ROW 3'S THREE CODES, assigned by what the failure is ABOUT.  Authority/split disagreement ->
     `X_SPLIT_FORBIDDEN`.  A wrong `--output-dir` -> `X_PROVENANCE_UNRESOLVED`, because the
     destination is a FUNCTION OF THE AUTHENTICATED AUTHORITY, not a digest complaint.  Everything
     else in row 3 -> `X_IDENTITY_MISMATCH`.
  2  `FINAL` REQUIRES ONLY THAT THE SPLIT IS NOT `dev`.  *** DO NOT NARROW IT TO ONE NAMED SPLIT -
     that would make this contract the place that CHOSE which confirmatory split gets rendered,
     and that is a later separately approved decision. ***
  3  SHAPE GATES ONLY, NEVER RANGE GATES, on both thresholds, the rung, the width and the distal
     tolerance.  Their correctness is established AT STEP 5 by equality against each one's own
     named approved source.  A plausibility band here would be an unapproved number entering
     through the back door, and 4b is forbidden from choosing one.

ONE INTERPRETATION THE DESIGN STATES BUT ITS FIELD TABLE CANNOT EXPRESS.  RECORDED IN THE MODULE
DOCSTRING, NOT ONLY IN A REPORT:
  3.2 says the menu must jointly contain a `structure`, an `actuator` and a `sensor` case, BUT
  THERE IS NO SOURCE-CLASS FIELD and a case's class is carried by its authenticated `labels`
  payload, where `verification_scene.validate_bundle` ALREADY establishes it.  So the record
  constrains WHICH CASES EXIST and the check stays where the evidence is.  *** DO NOT ADD A
  `source_class` FIELD - it would let an author assert a class the payload contradicts, which is
  design property 2's own failure mode. ***

TWO FORWARD ITEMS FOR THE 4b-ii CARD.  NEITHER IS A FINDING AGAINST THE CLOSED DESIGN:
  1  *** THE GEOMETRY PRODUCER'S DIGEST DOMAIN IS UNSETTLED AND IT COLLIDES WITH A RULING.
     `render_geometry.source` hashes `scripts/utils/cable_mechanics.py` and READ-ORDER STEP 5 DOES
     THAT AT RUNTIME.  Codex's S128 ruling declined an EOL pin for `*.py` on the stated premise
     that NO PACKET RUNTIME HASHES THOSE FILES.  STEP 5 ENDS THAT PREMISE.  Under requirement (cc)
     a tracked text file's recorded digest belongs in the TEXT domain, so 4b-ii must either use
     `canonical_text_sha256` for that one field OR add an EOL pin for that one file.  A raw digest
     with no pin is GREEN HERE AND RED ON A FRESH WINDOWS CLONE. ***
  2  the source-class interpretation above, so a later reader does not read 3.2 as requiring a
     record field that does not exist.

THE MEASUREMENT THAT WENT AGAINST ME IN S138, AND IT IS THE ONE TO CARRY:
  THE FOCUSED SUITE WAS GREEN AT EVERY STEP, 341 TESTS.  The mandatory two-pass mutation control -
  27 MUTANTS (25 real + 2 negative controls) across BOTH the module and the renderer, staged
  entirely OUTSIDE the repository - REPORTED ONE SURVIVOR ON ITS FIRST SWEEP, AND IT WAS IN MY NEW
  TESTS RATHER THAN IN MY NEW CODE.
    `m01-portable-ceiling-raised`  RAISING `MAX_PORTABLE_COMPONENT_CHARS` FROM 255 TO 4096
      SURVIVED.  Every length in the new tests was written as an OFFSET FROM THE CONSTANT UNDER
      TEST (`MAX_CASE_ID_CHARS + 1`, `"x" * MAX_PORTABLE_COMPONENT_CHARS`), so the inputs MOVED
      WITH THE MUTATION.  *** 341 GREEN TESTS WOULD HAVE STAYED GREEN ON A MODULE THAT ACCEPTED A
      FOUR-THOUSAND-CHARACTER FILENAME.  What the suite held was the RELATIONSHIP, which was never
      in doubt; what it did not hold was the VALUE, which is the only part a reviewer cannot check
      by reading. ***  EVERY LENGTH IS A LITERAL NOW, and ONE test
      (`test_the_two_ceilings_are_the_filesystem_numbers_stated_as_literals`) pins both constants
      to 255 and 250 with the reason attached.  Lesson 229.
  AFTER THE FIX: 25/25 REAL MUTANTS CAUGHT, BOTH NEGATIVE CONTROLS SURVIVING, IDENTICAL ACROSS BOTH
  PASSES, NO BAD ANCHORS, BOTH TARGET DIGESTS RESTORED EQUAL.
  *** THE SWEEP HAS NOW CHANGED THE TESTS ON THREE CONSECUTIVE BUILDS.  IT IS NOT A CONFIRMATION
      STEP.  BUDGET FOR IT AND RUN IT BEFORE THE HANDOFF, NOT AFTER. ***

MY S138 EVIDENCE, SO A LATER SESSION DOES NOT RE-MEASURE IT TO FIND OUT WHETHER IT WAS DONE:
  341 focused / 341 under `python -O` / 2,608 packet-wide, zero failures, zero collection errors.
  `py_compile` and `git diff --check` clean; `git status --porcelain` exactly the three candidate
  files.  *** THE STEP-3 FIGURE SET IS BYTE-IDENTICAL AFTER THIS RENDERER EDIT, MEASURED TWICE -
  once after the containment work and again after the byte-count change: all TEN tracked files
  reproduce at the same SHA-256 at `--fixture-seed 7` under `MPLBACKEND=Agg`, bundle digest
  `3bf51e94...` unchanged.  The regeneration went to a git-ignored scratch directory and was
  deleted. ***

*** THE SINGLE MOST IMPORTANT CARRIED CORRECTION IS UNCHANGED: `ADAPTER_DISTAL_AGREEMENT_TOL_M` IS
    GONE AND MUST NOT BE BUILT.  The adapter has NO guessed universal tolerance;
    `render_geometry.distal_tolerance_m` must equal a field in a SEPARATELY APPROVED
    GEOMETRY-VALIDATION ARTIFACT THAT DOES NOT EXIST YET, and 4b CHOOSES NO REAL-DATA TOLERANCE.
    The contract fixture CANNOT be the geometry oracle - its `deform_coords` and `true_task_output`
    come from INDEPENDENT synthetic maps - so 4b-ii MUST BUILD A SECOND, COHERENT FIXTURE.
    A NUMBER MEASURED AGAINST THE WRONG OBJECT IS WORSE THAN NO NUMBER. ***

*** THE CY RULING STILL GOVERNS WHAT 4b-ii BUILDS: BRANCH B, AUTHORITY-SCOPED P1.
      DEVELOPMENT_ONLY  an exact approved versioned DRAFT config - NOT named `config.json`,
                        `status = draft`, `confirmatory_payloads_allowed` FALSE, `config_hash`
                        beginning `dev-`, validated with `load_config(require_frozen=False)`;
                        record / `--config` path / file digest / semantic hash must all agree;
                        split is `dev`.
      FINAL             `load_config(require_frozen=True)`, frozen `config.json`,
                        `decision = APPROVE_CONFIG_FREEZE`, all eight freeze-required paths
                        complete, no `dev-` string anywhere.
    `require_frozen` IS A FUNCTION OF THE RECORD'S AUTHENTICATED `authority`, NEVER A CONSTANT
    (finding DA).  AND THE MEASURED FACT A 4b BUILDER WOULD OTHERWISE GET WRONG:
    `require_frozen=False` ***ACCEPTS*** A FROZEN CONFIG - it is PERMISSIVE, not draft-only - so
    B8's opposite-authority refusals are owed to THE ADAPTER'S OWN `dev-`/frozen rule at step 4 and
    NEVER to `require_frozen`.  RUNTIME PROVES BYTES AND SEMANTICS ONLY; exact-state config
    approval, record review and both 4e halves remain SEPARATE SOCIAL GATES. ***

*** ONE TRACKED FOLLOW-UP FOR 4b-ii, NOT A FINDING: `build_role_bundle`'s LIVE DOCSTRING in the
    closed Step-2 blob still glosses `--config` as "path to the exact frozen config file" - THE
    SAME SENTENCE DA CORRECTED IN THE DESIGN.  Under branch B that gloss is `FINAL`-ONLY.  THE
    ADDITIVE 4b-ii EDIT SHOULD FIX IT.  DO NOT TOUCH THE CLOSED BLOB BEFORE THEN. ***

CODEX'S EIGHT S131 REPAIRS - ALL ACCEPTED UNCONTESTED, ALL VERIFIED AGAINST PRIMARY OBJECTS.
DO NOT RE-LITIGATE ANY OF THEM:
  1  APPROVAL WAS CONFLATED WITH AUTHORIZATION, AND IT WAS MY ERROR.  My 1.1 said exact-state
     record approval IS the authorization while 10.4d said it authorizes nothing.  Codex's
     three-way split (design approval -> eligible record state -> two halves authorize ONE
     invocation) is correct and is not to be re-merged.
  2  THE ABSENT-WORLD CLAIM WAS FALSE.  *** MEASURED BY ME INDEPENDENTLY: manifest.csv is 944 rows
     / 20 fields / 472 distinct (split,pair_id) keys / 472 COMPLETE C1-S PAIRS / dev 152, pilot
     152, val 168.  The delivered root holds ONLY labels/ observations/ plant/. ***  So P6 is
     UNINSTANTIATED, not false-for-lack-of-pairs, and the true absent fact is that the DOWNSTREAM
     roles do not exist.  *** B1 MUST NOT ASSERT THAT NO PAIR EXISTS. ***
  3  THE CONTRACT FIXTURE CANNOT VALIDATE GEOMETRY.  *** READ AT SOURCE BY ME: synthetic_plant.py
     line 95 draws `deform_coords` from an INDEPENDENT `rng.uniform` phase set at 0.9 Hz; line 98
     builds `curvature_true` DETERMINISTICALLY at 1.5 Hz; line 128 computes
     `true_task_output = _deformed_tip(q_true, curvature_true)`.  DEFORM_COORDS ENTERS THE TIP
     NOWHERE. ***  MY OWN PROBE at delivered settings (n_steps 96, f_ctrl 500, n_def 90): the whole
     deformation contribution to the tip is `0.01*mean(curvature_true)` = 2.549-4.513 mm against a
     1 nm constant.  *** I DID NOT REPRODUCE CODEX'S 2.81-6.20 mm AND SHOULD NOT HAVE - mine is a
     RIGID reconstruction contributing zero deformation, its contributes a WRONG one, so its
     figure is larger.  BOTH ARE MILLIMETRES; THAT IS THE FINDING. ***  *** THE SHARPER FACT I
     FOUND, CARRY IT: `curvature_true` CONTAINS NO RNG AT ALL and is byte-identical across seeds
     while `deform_coords` IS seed-dependent - so the fixture's two pairs have DIFFERENT
     deformation and an IDENTICAL tip deflection; corr(means) = +0.168/+0.217/-0.500/-0.071 at
     seeds 0/1/2/3.  THE CHANNELS ARE UNRELATED BY CONSTRUCTION. ***
  4  AUTHENTICATION HAPPENED AFTER INTERPRETATION.  My order parsed role indexes at step 6 and
     hashed them at step 10.  THE 21-ROW ORDER IN 4.1 IS NORMATIVE AND IS NOT TO BE REORDERED.
  5  P4 GAINED THE STRONGER `established_result` BINDING - the mechanism I offered in E2.
  6  THE PROPOSED MODEL FILE DOES NOT EXIST.  `cable_mechanics.model_xml` builds the MJCF IN
     MEMORY.  My draft asked a record to name and hash a static model file while the same document
     said there is none.  `render_geometry.source` now names and hashes the PRODUCER.
  7  SCHEMA-VALID BYTES ARE NOT PROVENANCE.  *** MEASURED BY ME: the research root carries
     generation_audit.json (1,256 B, `7db736e3...`) and independent_audit.json (1,470 B,
     `40c37551...`), manifest.csv is `55ea5f0e...` - ALL THREE OF CODEX'S DIGESTS REPRODUCE - and
     both audits carry status/assignment_hash/config_hash/manifest_audit, so its new semantic
     checks rest on fields that EXIST.  build_data_contract_fixture.py:298 writes ONLY
     build_summary.json. ***  CW now has FOUR mechanisms, not two.
  8  THE SYNTHETIC ACCEPTANCE LANGUAGE OVERCLAIMED.  B2/B7 now say what 4b can actually reach.

E1-E4 AND THE PUBLIC LOG - ALL SETTLED, INCLUDING E3'S REACHABILITY HALF (S132 RULING):
  E1  YES, with the SPLIT FIXTURE BOUNDARY: the EXISTING contract fixture drives authenticated
      storage/refusal plumbing; a DEDICATED COHERENT synthetic fixture drives geometry.  Neither
      may acquire production authority.  ACCEPTED AS RULED.
  E2  the STRONGER established-result binding is NORMATIVE.  ACCEPTED AS RULED.
  E4  D3 REMAINS OPEN; the adapter carries NO cross-arm scalar (W13).  ACCEPTED AS RULED.
  E3  FULLY SETTLED.  The operative half was always accepted - the adapter computes
      DEVELOPMENT_ONLY and can REFUSE it, and the present accept path is SYNTHETIC_FIXTURE.
      *** ITS REACHABILITY HALF WAS RULED IN CODEX'S S132 ON FINDING CZ: DEVELOPMENT_ONLY IS A
      FUTURE AUTHORABLE PRODUCTION STATE UNDER THE AUTHORITY-SCOPED P1 (branch B).  ACCEPTED BY ME
      IN S133 AND NOT REOPENED.  See the CY block in the head section. ***
  *** THE PUBLIC-LOG QUESTION IS SETTLED AND I DO NOT RAISE IT AGAIN.  Codex ruled NO SUCCESSOR
      ENTRY: the dated log is historical, the banner is current, and Step-3 review closure does
      not warrant duplicating the already-logged surface milestone.  ACCEPTED. ***
  ALSO STILL ACCEPTED WITHOUT ARGUMENT: Codex's forward-only note that my S130 public entry, at
  495 words, is not the lean shape the playbook names.  FUTURE HEARTBEATS RETURN TO THE LEAN FORM.
  THE PUBLISHED ENTRY IS NOT REWRITTEN.

MY TWO S132 SCOPE STATEMENTS - STILL STANDING, MEASURED, DELIBERATELY NOT RAISED AS DEFECTS.
DO NOT "FIX" EITHER
WITHOUT A NEW REASON:
  1  `--role-root` basename = `dataset_label` (read-order step 3).  *** MEASURED: `dataset_label`
     has NO anchor anywhere in `schema.json` or `scripts/utils/`; it is new in this document. ***
     The identity in `data_root` is carried by the THREE DIGESTS and the basename rule adds none;
     what it adds is a constraint on where a reader may put their data, against the portability
     standard.  It DOES fail earlier and more legibly than a digest mismatch.  I LEFT IT IN PLACE
     rather than relax a reviewer's check with no defect to show.
  2  Read-order step 12 maps `RolePayloadLoader`'s SCHEMA/SEMANTIC failures to
     `X_IDENTITY_MISMATCH`.  A payload whose digest is exactly right but whose dtype or shape is
     wrong is NOT an identity mismatch, and none of the twelve codes fits it.  *** I AM NOT
     PROPOSING A SIXTEENTH CODE - inventing one for a branch nobody has built is exactly what Q1's
     ruling forbade.  4b BUILDS THE BRANCH AND IS THE ROUND ENTITLED TO SPLIT IT. ***

Q1 IS DISCHARGED AND CODEX CONFIRMED THE ASSIGNMENT.  DO NOT REOPEN THE CHOICE:
  `X_GEOMETRY_UNSUPPORTED` AT EXIT STATUS 15.  *** RE-MEASURED S132: EXIT_CODES maps X_SCENE_OK to
  0 and the twelve refusals to 3..14 CONTIGUOUSLY, so 15 is free, no existing value moves, and the
  change is PURELY ADDITIVE. ***

WHAT THE STEP-4 DESIGN SAYS, so a reviewer or a later session does not re-derive it.  *** READ THE
FILE; this block is an index. ***
  A CONNECTION RECORD is a reviewed JSON data object naming every scientific file the role adapter
  may open and every identity it must find inside them.  The adapter authenticates what the record
  names; it discovers nothing, defaults nothing, widens nothing, opens nothing else.
  *** THE DOCUMENT AUTHORIZES NO SCIENTIFIC READ OR RUN.  Approving it authorizes 4b ONLY. ***
  SECTION 10 DECOMPOSES STEP 4, and 4a/4b are BUILDABLE:
    4a  this design reviewed and frozen                 blocked on NOTHING   <- CLOSED S135
    4b  adapter + tests, storage/refusal plumbing on    blocked on 4a   <- SPLIT: 4b-i BUILT S136
        the EXISTING contract fixture and geometry on                      and UNDER REVIEW;
        a DEDICATED COHERENT synthetic fixture; NO                         4b-ii NOT STARTED
        real-data tolerance is guessed or recorded
    4c  preconditions P1-P6 met  (+ CY settled)         blocked on the freeze, the capacity
                                                        selection, the calibration, the
                                                        established result and the geometry
                                                        validation artifact
    4d  the record authored and reviewed                blocked on 4c
    4e  the joint authorization, two halves             blocked on 4d
    4f  the ONE authorized invocation + exact-state review
  THE SECOND DESIGN TEST, in its repaired form: "NO PATH THROUGH THE CONNECTION RECORD MAY DISCOVER
    A SCIENTIFIC RESULT OR OPEN SCIENTIFIC ROLE BYTES WITHOUT A SEPARATE AUTHORIZATION FOR THAT
    EXACT READ.  The verification artifact PRESENTS a result; it is never the OCCASION of one."
    *** A PREVIOUS READ DOES NOT MAKE A LATER FILE ACCESS CEASE TO BE A READ - that is Codex's
    correction to my draft, and 4e separately authorizes the adapter's own role re-open. ***
  THE PRECONDITION LEDGER: P1-P5 FALSE TODAY; P6 UNINSTANTIATED (see repair 2).  P1's WORDING IS
    NOT FINAL - see CY.
  FOURTEEN INVARIANTS W1-W14 and SEVEN ACCEPTANCE TESTS B1-B7 are in the file.
  V18'S CONDITIONAL IS DISCHARGED AND WAS RE-MEASURED IN S132: importing `utils.role_contract`,
    `utils.storage_contract`, `utils.config_contract`, `utils.estimator`, `utils.metrics` AND
    `utils.protocol_p` in a FRESH INTERPRETER leaves `torch` AND `mujoco` ABSENT; only numpy
    arrives.  NO DEPENDENCY SEPARATION IS NEEDED.  RE-MEASURE IN 4b; an import graph is a property
    of a checkout, not of a document.

MY EARLIER FINDINGS CU/CV/CW STAND, BUT TWO OF THEIR RESOLUTIONS MOVED IN THE REVIEW.  CARRY THE
CURRENT ONES, NOT MY S131 WORDING:
  CU  the shared 1 nm tolerance constant asked to be two things.  *** CURRENT RESOLUTION:
      `CENTERLINE_TASK_OUTPUT_TOL_M` stays exactly as it is and stays the FIXTURE'S - no existing
      value moves, no closed test changes - and THE ADAPTER HAS NO UNIVERSAL TOLERANCE AT ALL
      until an approved geometry-validation artifact supplies one.  NOT a second measured
      constant. ***
  CV  the render geometry belongs to the RECORD, not the config.  *** CURRENT RESOLUTION:
      `render_geometry.source` names and HASHES the PRODUCER `scripts/utils/cable_mechanics.py`
      and never imports it; `planar_convention` and `links` state the chain explicitly.  NOT a
      static model file - THERE IS NONE. ***
  CW  provenance cannot be computed from schema-conformant bytes.  *** CURRENT RESOLUTION: FOUR
      mechanisms - both dataset audits strict-parsed with their echoed fields and recomputed
      censuses; the established-result binding; the synthetic accept path staying SYNTHETIC; and
      ONE mechanically fixed development scratch parent.  `.gitignore` IS EXPLICITLY NOT TREATED
      AS ACCESS CONTROL. ***

STEPS 1, 2 AND 3 ARE ALL CLOSED.  DO NOT REOPEN ANY OF THEM:
  1  design frozen        blob `0753d4ed`                                    me S127 / Codex S127
  2  module + tests       `c12745ab` `0ae5b19d` `cf61e5aa` `1833a472`        me S129 / Codex S129
  3  figure set + Step 32 ten fixture blobs + packet README `4bc07f18`       me S130 / Codex S130
                          + both `.gitattributes` + packet `.gitignore` + public README `3ab96e38`
  *** A CLOSED REVIEW LOOP AUTHORIZES THE NEXT STEP ONLY, AND NEVER A RUN. ***

DO NOT RE-LITIGATE ANY OF THESE.  ALL SETTLED, ALL ACCEPTED:
  CODEX'S FOUR STEP-2 REPAIRS CP/CQ/CR/CS (S128), accepted in full by me S129:
    CP  the radio menu shows the NAMED BODY-CHANGE LABELS, `select_label` maps label -> case_id,
        `validate_bundle` refuses DUPLICATE labels.  *** ORDERING IS LOAD-BEARING:
        `validate_bundle` is the FIRST statement of `__init__`, BEFORE
        `_case_id_by_label = dict(zip(...))`.  DO NOT MOVE IT. ***
    CQ  V1 is a SURFACE gate, not only a builder gate - both `render_bundle` and
        `InteractiveVerificationSurface` call `validate_bundle` before creating anything.
    CR  `advance_frame` is ONE LINE and moves the VISIBLE SLIDER; the frame moves only as a
        consequence of the slider observer.  DO NOT "RESTORE" A DIRECT `self.frame = ...`.
    CS  `_project_relative_output_dir` refuses rooted / drive-qualified / `..` forms on BOTH
        subcommands at PARSE time, through argparse's existing `SystemExit(2)`.
  MY FINDING CT (S129), test-only: `select_label`'s refusal branch, and driving EVERY radio entry.
  Q2  a decision failing the live schema-D contract keeps `X_DECISION_UNSUPPORTED`.
  D1  DESIGN FIRST, THEN MODULE.  D2 `matplotlib.widgets` IS SUFFICIENT (discharged S128,
  strengthened S129).  D3 NO CROSS-ARM SCALAR THIS ROUND - still open for the connection, see E4.
  D4 FABRICATED TRUTH MAY RENDER, ONLY UNDER THAT EXPLICIT LABEL.
  CODEX'S CLOSED FINDINGS ON THE STEP-1 DESIGN: BR-BZ (S123) - CC/CD (S124) - CG/CH (S125) - CM (S126).
  MY CLOSED FINDINGS ON THE STEP-1 DESIGN: CA/CB (S124) - CE/CF (S125) - CI/CJ/CK/CL (S126) - CN/CO (S127).
  *** THE STEP-1 DESIGN AT `0753d4ed` IS THE AUTHORITY ON ALL THE STEP-1 ONES.  READ THE FILE.  AN
      APPROVED VERSION IS NEVER EDITED IN PLACE - a correction bumps the version and `git mv`s.
      SUPERSEDED, never review or build from: `260e2042`, `0fabe547`, `d56c25c1`, `7536a6eb`,
      `7a62b93d`, `968feb29`, `ca158698`, `c674c022`. ***

WHAT THE STEP-2 BUILD IS, so a reviewer or a later session does not re-derive it:
  verification_scene.py   the scene/bundle VALUE contract, the canonical-JSON codec (including
                          the three-string non-finite encoding from CA), construction-time
                          validation, the frame semantics, and the labeled synthetic fixture.
  render_verification_scene.py
                          `draw_scene(scene, *, frame) -> Figure` (PURE, pyplot-free, opens and
                          writes NOTHING), `render_bundle` (the scripted 300-DPI path, the only
                          thing that writes), `InteractiveVerificationSurface` (RadioButtons /
                          Slider / Button / FuncAnimation), and the two-subcommand CLI.
  *** THE INTERACTIVE SURFACE PAINTS NOTHING ITSELF - it calls the same painter, renders the
      figure to an RGBA buffer and displays it.  Sameness is a SINGLE SOURCE, not a promise
      maintained across two code paths.  DO NOT "OPTIMIZE" THIS INTO A SECOND DRAW PATH. ***
  *** `_fixture_mode` RENDERS AND THEN CALLS `launch_interactive`.  Under a non-interactive
      backend `launch()` prints a note and RETURNS, which is what makes the scripted path usable
      from a script at all.  SET `MPLBACKEND=Agg` FOR ANY SCRIPTED REGENERATION. ***
  `build_role_bundle` REFUSES UNCONDITIONALLY with `X_CONNECTION_UNAUTHORIZED` before reading any
  argument, and THAT IS THE CORRECT STATE UNTIL 4b CLOSES.

THE FOUR PLACES THE BUILD POINTS AT A FACT'S OWNER INSTEAD OF COPYING IT (lesson 199 applied):
  1  DECISIONS ARE `utils.estimator.EstimatorOutput` VALUES - the live schema-D struct ITSELF,
     not a scene-local mirror of its nine fields.  *** DO NOT INTRODUCE A SCENE-LOCAL DECISION
     CLASS. ***
  2  THE WINDOW CHECK IS A CALL.  `_validate_tracking_window` calls `utils.metrics.j_5s` and
     re-raises whatever it raises as `X_WINDOW_UNSUPPORTED`.
  3  CLASS ORDER IS `utils.metrics.SOURCE_CLASS_ORDER`, imported.
  4  CANONICAL JSON IS `utils.protocol_p.canonical_json`, `allow_nan=False` still on.
  FIELD NAMES ARE PINNED BY EQUALITY AGAINST `schema/schema.json` - the nine `estimator_outputs`
  fields and the eight `labels` fields, two tests, EQUALITY not adoption.  *** THOSE TWO ARE THE
  ONLY TESTS IN THE FOCUSED PAIR THAT NEED A FILE OUTSIDE `scripts/` AND `tests/` - which is why
  A MUTATION CONTROL MUST STAGE `scripts`, `tests` AND `schema` (a red control measures nothing). ***

TWO CLOCK FACTS DELIBERATELY LEFT UNBOUND.  BINDING EITHER REJECTS FAITHFUL REAL DATA:
  `controller_t_s` IS NEVER COMPARED TO `playback_t_s` (finding CI).  The fixture deliberately
    carries the ONE-CONTROL-INTERVAL OFFSET the live loop produces, and TWO tests hold the accept
    side open - one requires the offset grid to be ACCEPTED, one requires an EQUAL grid to be
    accepted too, so neither convention gets frozen in.
  `onset_index` IS NEVER USED TO INDEX `playback_t_s`.  `assignment_generator._step_index` makes
    the label's onset `onset_s / dt` while `cable_plant` stamps `t_s` AFTER advancing, so
    `plant.t_s[onset_index]` is one control interval LATER than `onset_time_s` in real data.
    Only `onset_time_s` is used, and only by the live metric.

THE FOUR TESTS THAT MUST NOT BE DELETED, AND WHY:
  V15 DELEGATION - monkeypatches `j_5s` to raise a SENTINEL STRING no design document contains and
    requires construction to refuse CARRYING THAT SENTENCE.  An AST test also asserts the call
    exists, but that one is satisfied by a function that calls and ignores.  *** ONLY THE
    MONKEYPATCH TEST CAN HOLD THE DELEGATION.  Deleting it is how CN comes back.  Lesson 201. ***
  V6 ACCEPT SIDE - a controller payload on the one-interval-offset grid is REQUIRED TO BE
    ACCEPTED.  Deleting it is how CI comes back.
  `test_v17_every_menu_entry_is_exposed_by_both_surfaces` - MUST KEEP DRIVING EVERY ENTRY.  Cutting
    it back to one `set_active` is exactly mutant B, and mutant B passes.  Lesson 205.
  `test_d2_the_interactive_surface_refuses_an_unknown_display_label` - the only test on the refusal
    branch of the method the RADIO actually calls.

ONE THING I NEARLY GOT WRONG IN S128 AND ONLY V15 SAVED ME FROM.  RECORDED SO IT IS NOT
RE-INTRODUCED:
  I ALMOST CHECKED `playback_t_s` FOR UNIFORMITY / MONOTONICITY / FINITENESS AT CONSTRUCTION under
  `X_TIMEBASE_MISMATCH`.  *** THAT WOULD HAVE BROKEN V15, which requires a NON-UNIFORM GRID to
  surface as `X_WINDOW_UNSUPPORTED` - my check would have pre-empted the delegation for exactly
  the shape the delegation exists to cover. ***  Construction therefore checks ONLY THE GRID'S
  RANK; every property OF the grid is delegated to `j_5s`.

THE FIXTURE - FOUR CASES, AND ITS NUMBERS ARE MEASURED, NOT REMEMBERED (lesson 208):
  `soften_link_2` (structure), `weaken_actuator_1` (actuator), `bias_encoder_1` (sensor),
  `indistinguishable_softening` (structure).  *** THE DISPLAY LABELS ARE DATA AND MUST STAY
  UNIQUE: "Soften link 2 by 30%", "Weaken actuator 1", "Bias encoder 1", "Soften link 1 by 10%
  (the two suites are indistinguishable)".  THE FIRST THREE ARE A1'S OWN WORDS. ***
  *** THE ASYMMETRY, DRIVEN THROUGH THE LIVE `j_5s` IN S130 AND REPRODUCED INDEPENDENTLY BY CODEX
      IN ITS S130 - USE THESE, NOT A MEMORY:
        soften_link_2                J_C1 0.323744  J_S 0.111086   S BETTER
        weaken_actuator_1            J_C1 0.138729  J_S 0.365796   C1 BETTER
        bias_encoder_1               J_C1 0.263766  J_S 0.263766   EXACT TIE, identical tracking
                                     outputs but DIFFERENT decisions
        indistinguishable_softening  J_C1 0.192470  J_S 0.192470   EXACT TIE, and the two arms are
                                     identical in EVERY canonical field but `suite`
      MY S129 SUMMARY SAID "the same value to both once, and identical arms once" AND THAT WAS
      WRONG - THERE ARE TWO EXACT TIES.  I only caught it because I drove the metric instead of
      quoting this file.  A test requires at least one case smaller for EACH suite. ***
  Also jointly covered: confident correct, a CONFIDENT WRONG CALL (C1 says `actuator` at 0.850
  where the fabricated truth is `structure`), TWO abstentions, a high `unknown_score` (0.900 /
  0.950 on `bias_encoder_1`), `+inf` severity scale rendering as `UNAVAILABLE` with a
  pre-detection `NaN`, and a decision that CHANGES (S on case 1 abstains at 1.5 s and resolves to
  `structure` at 3.0 s).  Every arm carries TWO decisions; the grid starts at 0.05 s so every case
  drives `NO DECISION YET` early.
  GRID: 141 samples at 20 Hz on the plant's own `(k+1)*dt` convention; onset EXACTLY on sample 19
  at 1.000 s; window close EXACTLY on sample 119 at 6.000 s (which IS the derived scripted frame);
  grid runs on to 7.05 s so that frame is INTERIOR, not terminal.
  THE FIGURE SET: `--fixture-seed 7`, `MPLBACKEND=Agg`, ten files / 2,489,056 B, bundle sha256
  `3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70`, PNGs 3,600 x 2,550 with
  pHYs 11,811 px/m both axes = 300 DPI.  SEED 7 IS THE ONLY CANONICAL SEED - the module docstring
  names it and both test files pin it.  Do not introduce a second one.
  *** DO NOT "IMPROVE" THE FIXTURE INTO A WIN.  A synthetic menu whose every panel favoured the
      structural suite is the exact misreading this whole design exists to prevent. ***
  *** AND DO NOT USE IT AS A GEOMETRY ORACLE - see Codex's repair 3 above.  IT IS THE STORAGE AND
      REFUSAL FIXTURE ONLY.  4b MUST BUILD A SECOND, COHERENT ONE. ***

WHY SLOT 8 STILL CANNOT BE BUILT AT ITS FINAL FORM, RE-MEASURED IN S131 RATHER THAN QUOTED:
  The only config in the packet is `config/draft-config-v0.1.json`: `status` "draft", `decision`
  `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`, `config_hash` beginning
  `dev-`.  `values.models`, `values.calibration` AND `values.evaluation` are LITERALLY NULL, and
  all three are among `config_contract.freeze_required_paths`' eight entries.
  *** A DEMO BUILT ON TODAY'S DEVELOPMENT RECORD WOULD PRESENT A RUNG-2 ARM SET SCORING EXACTLY
  ZERO ON TWO OF FOUR CLASSES AS A FINDING.  THE WHOLE DESIGN EXISTS TO MAKE THAT STRUCTURALLY
  IMPOSSIBLE, NOT MERELY DISCOURAGED. ***

*** THE MUJOCO BLOCK IS OVER.  DELETE ANY MEMORY OF "THE SUITE IS UNMEASURABLE". ***
  `import mujoco` failed at the interpreter level in S128 and S129 under Windows SMART APP
  CONTROL, which had refused an UNSIGNED native binary for about two hours after a Windows update
  and then cleared on its own when Microsoft's reputation service vouched for it.  A REPAIR AGENT
  Randy authorized for the machine problem diagnosed it to root cause from the Code Integrity log
  and appended the finding under `director_requests.md` ENTRY 2.  *** THE TRUE FULL-SUITE FIGURE
  IS 2,267, MEASURED INDEPENDENTLY FOUR TIMES NOW: the Repair Agent, Codex S129, me S130, and me
  S131 (204.35 s). ***
  *** THE DEGRADED COUNTS ARE ARTIFACTS AND DO NOT TRAVEL: entry 2's own 1,328 / 1 / 28 and my
      S129's 1,344 / 1 / 28 are honest measurements of a broken environment and WORTHLESS as
      measurements of the suite.  THE DATED DOCUMENTS THAT RECORD THEM ARE LEFT STANDING; the
      correction propagates FORWARD.  THE TECHNICAL REPORT INHERITS THE SAME OBLIGATION. ***
  THE STANDING PROCEDURE, and it is the director's:
    1  Before treating any native-import failure as a bug, run the read-only diagnostic:
       `powershell -ExecutionPolicy Bypass -File "C:\Users\cresp\Documents\Dandelion Engineering\tools\Check-NativeImportBlocks.ps1"`
       (that tool lives OUTSIDE this repository and is not project content).
    2  A NUMBER MEASURED DURING A BLOCK IS DISCARDED, NOT PUBLISHED WITH A CAVEAT.  This is the
       part S128 and S129 got wrong.  Re-run once the diagnostic reports healthy.
    3  EXPECT RECURRENCE AND DO NOT ABSORB IT.  Any unsigned binary here can be blocked again
       after a Windows update or a package install.  APPEND A NEW NUMBERED `director_requests.md`
       ENTRY with the diagnostic's output - Randy is deciding policy from the pattern of
       incidents, and a silently absorbed incident is one he cannot see.
    4  DO NOT PROPOSE TURNING SMART APP CONTROL OFF.  Randy has decided it stays ON for now,
       having been shown the alternatives, and will reassess after the next incident.

THE S130 EOL PIN, KEPT BECAUSE IT IS A RULING WITH A PREMISE (lesson 209).  DO NOT UNDO IT:
  ONLY `results/verification_fixture/*.sha256 text eol=lf` is pinned, in BOTH `.gitattributes`
  files.  MEASURED with `git checkout-index`: that 65-byte digest file materializes at 66 B with
  one CRLF on a fresh checkout; the canonical JSONs carry NO newline at all and the PNGs
  round-trip as binary, so neither is pinned.  *** CODEX'S S128 RULING THAT NO EOL PIN IS ADDED
  FOR `*.py` STANDS AND IS NOT CONTESTED - its premise was that no packet runtime hashes those
  files.  THAT PREMISE DOES NOT REACH A FILE WHOSE CONTENT IS A DIGEST A READER IS TOLD TO
  COMPARE.  Codex explicitly accepted the narrow pin in its S130. ***
  *** THE STEP-4 DESIGN ADDS A FUTURE PIN, NOT YET WRITTEN: `results/verification_connection/**/*.json`
      for the record itself, because the RUNTIME HASHES THE RECORD.  That rule lands in 4b/4d, not
      before. ***

SECTION 5.4 - BOTH APPLICATIONS APPLIED, CLOSED, AND NOT TO BE ADDED TO.  EVER.
  RUNG 2:  Codex's half its S119, my half my S120.  SAME artifact bytes, SAME two sentences:
    "Slot 9's rung 2 is built and fitted; the ladder has more than one rung on it, and the
     development record contains one rung-2 fit at five seeds under the approved protocol."
    "At rung 2, in-sample, the paired sign was not consistent across the five seeds."
  *** NO `because`, `so`, `therefore`, `which shows`, `capacity-bound`, `resolves` or `confirms`
      MAY BE ATTACHED TO EITHER, AND THE TWO DO NOT BECOME EVIDENCE BY BEING COMBINED.  5.4 IS
      SPENT: a later session APPLIES NOTHING FURTHER FROM IT.  BOTH SENTENCES ARE PUBLIC; THAT IS
      PUBLICATION, NOT A NEW APPLICATION. ***
  THE DEGENERACY OBSERVATION TRAVELS WHEREVER THE TWO SENTENCES GO (standing lesson 185): every
  one of the ten rung-2 arms scored F1 = 0.000000 on `healthy` AND on `structure`; four of ten sit
  exactly at the recorded majority-class baseline.  *** USE `structure`, NOT "four non-zero
  values" - EVERY anchor is non-zero on `structure` and EVERY rung-2 arm is exactly zero, which is
  the stronger and the TRUE statement (finding BN corrected the other one). ***  It is in packet
  README Step 31 and in the public log, in the same paragraph as the two sentences and after them.
  IT STILL OWES THE TECHNICAL REPORT THE SAME ADJACENCY.  NO CAUSE IS ATTACHED, and the class
  imbalance is deliberately NOT in the record as a conclusion because nothing in this run tested it.

THE PROHIBITIONS THAT SURVIVE, AND THEY ARE PERMANENT:
  1  DO NOT RE-RUN C7 AND DO NOT REGENERATE ITS ARTIFACT.  Exclusive create, consumed.
  2  DO NOT RE-RUN THE RUNG-2 EXECUTION OR THE RUNG-2 READ AND DO NOT REGENERATE EITHER ARTIFACT.
     THREE consumed exclusive destinations in the project.  A retry needs a NEW label, a NEW plan
     and a FRESH joint authorization; none exists and none is sought.
  3  DO NOT ADD A SENTENCE TO WHAT STAGE 1'S 5.4 LICENSES.  Exactly one row matched:
       "the paired curve does not have a readable shape at five points and five seeds"
     ANY TREND STATEMENT IS FORBIDDEN.
  4  DO NOT ADD A SENTENCE TO WHAT RUNG 2'S 5.4 LICENSES.  See the exact pair above.  Rung 2's own
     5.3 carries the no-trend rule ACROSS rungs: two rungs are TWO POINTS.
  WHAT REMAINS FORBIDDEN, UNCHANGED: no capacity selected, no rung selected, no threshold set, no
  generation, no rollout, no pilot/val/test read, and nothing about C1-versus-S.  The 32-channel
  anchor result is UNTOUCHED.  *** A COMPLETED, INTERPRETED READ IS NOT A LICENCE TO SAY MORE
  ABOUT IT. ***

THE ARTIFACT SHAPES AND THE AUDIT INSTRUMENTS ARE IN `agents/Claude/Permanent Instruments.md`.
  Read it ON DEMAND, not at startup.  The routing table at the bottom of THIS file says which of
  its sections answers which question.  *** STANDING LESSONS NOW REACH 238 AND ALL OF THEM LIVE
  THERE - S132 added 213 (A DEFECT THAT ONLY THE UNREACHABLE PATH CAN EXPOSE IS THE EXPENSIVE
  KIND: CX would have passed every test 4b writes, because 4b's accept path is synthetic and its
  output goes to a temp root - ASK WHAT THE ACCEPT PATH ACTUALLY REACHES, which is the third time
  that question has found this shape), 214 (A RULING CAN BE INCONSISTENT WITH A PRECONDITION
  WITHOUT EITHER BEING WRONG ALONE - CY is a collision between two statements written in different
  sessions for different purposes, invisible to whoever wrote either half, and it is an argument
  for the re-review step existing INDEPENDENT of whether the reviewer's edits were good), and 215
  (REPRODUCING A NUMBER IS NOT THE SAME AS CONFIRMING A FINDING - I could not reproduce Codex's
  millimetre figure because we built different reconstructions, and saying so WITH THE REASON is
  more useful than adopting its number or treating the mismatch as a disagreement; the STRUCTURAL
  fact carried the finding).  S133 added 216 (A CORRECT RULING CAN LEAVE A WRONG DOCUMENT -
  making an unreachable state REACHABLE can turn a dormant contradiction somewhere else into a LIVE
  one, and the agent who made the decision is the least likely to see it; that is finding DA) and
  217 (PORTABILITY IS A PROPERTY OF TESTS, NOT ONLY OF SCRIPTS - an acceptance test that can only be
  green on the machine holding the data is a reproducibility failure even when no script changed;
  that is finding DB).  S134 added 218 (A CONTRACT CAN MAKE A FILENAME AN AUTHORITY, AND A
  SYNTHETIC INSTANCE OF AN AUTHORITY IS THE AUTHORITY - ask whether a thing's identity is carried by
  its CONTENT, which can be synthesised freely, or by its NAME or LOCATION, which cannot; that is
  finding DD, and the reusable repair is the in-memory validator seam that asserts a filename
  without creating the file) and 219 ("TEMPORARY" IS NOT A MITIGATION WHEN THE HAZARD IS EXISTENCE -
  a crashed run does not keep the promise to delete, and CW already ruled the ignore rule is not
  access control, so the only real mitigation is not creating the object).
  S135 ADDED 220 (AN ABBREVIATED IDENTIFIER WITH THE RIGHT PREFIX IS NOT A VERIFIED IDENTIFIER - the
  Review Card's blob id shared its first EIGHT characters with the real one and did not exist; name a
  governing state THREE ways and resolve every id against the object store), 221 (WHEN YOU OWN THE
  ARTIFACT, INTEGRATING THE REVIEWER'S REPAIR COSTS ONE ROUND LESS THAN NAMING A NEW FINDING, and the
  technical content is identical - reserve the finding for DISAGREEMENT; the test is whether you
  could write the repair yourself in the same session) and 222 (A SEAM NAMED AFTER ONE STEP MUST BE
  CHECKED AGAINST THE STOP CONDITION OF THE TEST THAT USES IT - ask what the LAST thing the test must
  reach is, and whether the seam reaches that far).  S136 ADDED 223 (A UNIQUE PHRASE IS NOT ENOUGH; THE PHRASE MUST NOT APPEAR AT A *LATER* SITE THAT ALSO REFUSES THE SAME INPUT - four of my S136 tests asserted a word that was unique to the branch under test and ALSO present in the sentence of a broader later check, so deleting the branch left the suite green, and ONLY THE MUTATION SWEEP FINDS THAT) and 224 (WHEN A DESIGN NAMES ONE BUILD STEP THAT IS REALLY A PROGRAM, SPLIT THE *REVIEW*, NOT THE DESIGN - name the halves, say explicitly that the design's sub-step does not close until both close, show that no gate moves, take the boundary from the design's own text, and ask the reviewer to rule on the split before reviewing the contents).  STANDING LESSONS NOW REACH 224.
  S137 ADDED 225 (A REVIEWER'S BLOCKING FINDING CAN NAME A REPAIR THAT LIVES OUTSIDE THE CARD'S CANDIDATE, and the only non-defective move is to make the edit, name it as a SCOPE EXPANSION in card and chat, and OFFER THE REVERT - the scope of a card is the reviewer's to rule on, and the owner's job is to make the ruling possible; corollary, when you touch a closed file that PRODUCES a tracked artifact, REGENERATE IT AND COMPARE EVERY DIGEST), 226 (SPELLING AND CONTAINMENT ARE DIFFERENT PROPERTIES AND NEITHER SUBSUMES THE OTHER - measured here: an embedded NUL makes `Path.resolve()` raise before any containment comparison, `schema.json:stream` writes an INVISIBLE NTFS stream, `trailing.` and `trailing` ARE ONE FILE, and `Path("CON").resolve()` looks perfectly ordinary because a device alias is CONTAINED BY EVERY ROOT), 227 (`@dataclass(frozen=True)` REBINDS THE ATTRIBUTE, NOT THE OBJECT - deep immutability is explicit work, the proxy must wrap a PRIVATE COPY, and EVERY mapping-bearing layer gets its own probe) and 228 (A TEST THAT SKIPS ON THE ONLY MACHINE THE PROJECT HAS HOLDS NOTHING - a Windows DIRECTORY JUNCTION needs no privilege where a symlink does, and the trap must be built so THE EQUALITY STILL HOLDS and only the guard under test separates accept from refuse).  S138 ADDED 229 (A TEST WHOSE INPUT IS A FUNCTION OF THE CONSTANT IT IS TESTING HOLDS NOTHING ABOUT
  THAT CONSTANT - it holds the RELATIONSHIP, which was never in doubt; state boundary lengths as
  LITERALS and pin the constants themselves in one place with the reason attached), 230 (CONTAINMENT
  IS NECESSARY AND IS NOT SUFFICIENT - ask also whether the write set is WRITABLE and whether it is
  ONE-TO-ONE; when a value becomes a name, the names it competes with are part of its contract, so
  bound the DERIVED name, claim the FIXED names first, and compare FOLDED) and 231 (A GUARD WITH A
  TERM THAT CAN NEVER DECIDE ANYTHING IS THE SAME DEFECT AS A DUPLICATED GUARD - `max(chars, utf8
  bytes)` is always the byte count, so the first term was unreachable and no sweep could ever have
  flagged it; the repair is deleting the term and writing down the proof, not adding a test).
  STANDING LESSONS NOW REACH 231.  S139 ADDED 232-235 AND S140 ADDED THREE MORE, ALL THREE OF
  WHICH WENT AGAINST ME: 236 (A CEILING AND A SPLIT MUST BE WRITTEN AS ONE BOUND, OR THE DOCUMENT
  PROMISES A LIMIT IT DOES NOT ENFORCE - my convergence proposal bounded the whole thing in SESSIONS
  and its mechanism in CARDS AND ROUNDS, and the two did not compose; ask what OTHER rule in the same
  document also grants budget to the thing you just bounded), 237 (ON AN APPEND-ONLY ARTIFACT THE
  "MINIMAL" REPAIR IS A REWRITE OF HISTORY - before proposing a deletion ask whether the artifact is
  append-only and whether the bytes are already published; a reviewer's repair is minimal in EDIT
  SIZE, which is not the axis that matters) and 238 (THE CLAUSE A FINDING *CONCEDES* IS THE CLAUSE
  NOBODY MEASURES - the reviewer has no motive to probe the part they are agreeing with and the owner
  has no motive to probe the part that favours them, so a conceded clause is the one place two
  adversarial readers are ALIGNED, and alignment is where nothing gets checked).
  STANDING LESSONS NOW REACH 238.
  ALL OF THEM WERE WRITTEN STRAIGHT INTO THE REFERENCE FILE, WHICH IS THE S105 CORRECTION APPLIED. ***
```

## THE RUNG-2 STATE - ALL SEVEN STEPS CLOSED, 5.4 JOINTLY APPLIED, THE LANE IS SPENT

```text
THE DESIGN IS FROZEN AND JOINTLY APPROVED.  DO NOT REOPEN IT AND DO NOT EDIT IT IN PLACE -
a correction bumps the version and `git mv`s.
  Reproducibility Packet/protocol/rung2-escalation-v0.1.md
    Git blob 404c9f1fc1b0112e5ed8164853b261e97d510662
    sha256   9a154f902d7a98dcaa3e8bd34109e2ea6c4f29ba08c86a4ad301bfd62e69bf1f
    53,497 B / 807 LF.  LF-pinned by protocol/*.md in BOTH .gitattributes.
    Approved by me S112 and by Codex S112 at the SAME bytes.  Digest RE-MEASURED S120.
  SUPERSEDED, never review or build from: b7449993 (mine S111), 1f65ab5f (Codex S111).
  *** READ THE FILE.  It is the authority on the architecture ledger, the seven-row grid, the
      four handed-over decisions D1-D4, the thirteen invariants R1-R13, the pre-declared 5.4
      read and the failure path.  This block is an index, not the document. ***

WHAT IS BUILT, AND EVERY ONE OF THESE IS CLOSED:
  BUILT     attribution_net_rung2.py - RecurrentAttentionAttributionNet, 219,018 parameters,
            no training loop.  Plus 71 tests.  S113, JOINTLY APPROVED S114, ca192af0 / c43d33b0.
  BUILT     rung2_escalation.py + tests/test_rung2_escalation.py - S115, 735f8dee / 7cefcb63,
            142 tests.  JOINTLY APPROVED S115/S115 in ONE round.
  BUILT     results/rung2_escalation/plans/rung2-run-1/rung2_escalation_plan.json - S116,
            blob 61a2bd22, canonical == raw b51b0009...  JOINTLY APPROVED (me S116 after 132
            checks + a 23/23 mutation control, Codex S116 after its own 107-check instrument).
  SPENT     results/rung2_escalation/rung2-run-1/ - THE EXECUTION ROOT, CLAIMED AND CONSUMED.
            14 files: 2 tracked JSON + 12 ignored .pt.
            *** DO NOT DELETE IT, DO NOT WRITE INTO IT, DO NOT REUSE THE LABEL. ***
  BUILT     scripts/analyze_rung2_escalation.py + tests/test_rung2_escalation_analysis.py -
            S118, 7cf3cc6a / a642b3d3, 103 tests.  JOINTLY APPROVED - Codex S118 approved my
            exact bytes WITH NO EDIT, so no owner re-review was owed and step 6 CLOSED.
  SPENT     results/rung2_escalation_analysis/rung2-run-1/ - THE ANALYSIS ROOT, CLAIMED AND
            CONSUMED.  EXACTLY ONE FILE: rung2_escalation_analysis.json, blob a2fa857b.
            *** JOINTLY APPROVED - me S119 (165 checks), Codex S119 (its own 853-check
            standalone audit, no defect found).  DO NOT DELETE, REGENERATE OR RE-AUDIT IT. ***
  BUILT     the rung-2 RUNBOOK STEPS in the packet README - MY S120, Steps 30 and 31.
            *** CLOSED AT BLOB `f5e677c8` - Codex approved those exact bytes UNEDITED in its
            S121, after my S121 owner re-review repaired BN/BO/BP.  `9a3a878c` was my S120
            handoff and `7c9f394d` was Codex's S120 reviewer state, and BOTH ARE SUPERSEDED.
            DO NOT REOPEN IT. ***

THE SEVEN-STEP SEQUENCING - ALL SEVEN ARE DONE:
  1 design reviewed and frozen            DONE (S112, both agents, blob 404c9f1f)
  2 module + tests built and reviewed     DONE (S113/S114, both agents, ca192af0 / c43d33b0)
  3 executable + tests                    DONE (S115/S115, both agents, 735f8dee / 7cefcb63)
  4 plan run, artifact reviewed           DONE (S116/S116, both agents, 61a2bd22)
  5 execution, TWO authorization halves    SPENT.  Mine S117, Codex's S117, RAN ONCE S117.
                                           X_RUNG2_OK, 1,274.6 s, 12 fits.  NO RETRY AUTHORITY.
  6 read-only analyzer                     DONE (S118/S118, both agents, 7cf3cc6a / a642b3d3)
    6b the READ, TWO authorization halves   SPENT.  Codex's S118, mine S119, RAN ONCE S119.
                                           X_ANALYSIS_OK, 11.97 s.  NO RETRY AUTHORITY.
  7 exact-state review by both agents,     DONE.  Me S119, Codex S119, SAME BYTES.
    THEN 5.4 jointly                       DONE.  Codex S119 half + my S120 half = 2/2.
  *** THE LANE IS FULLY SPENT.  THE ONLY THING LEFT ON IT IS DOCUMENTATION, AND THAT IS THE
      PACKET-README LOOP IN THE HEAD BLOCK. ***

*** THE POSITION MARKER RULE STILL BINDS - lesson 182.  There is exactly one authority on
    where the project is and it is this file's head block.  GREP YOUR FINISHED REWRITE FOR
    `WE ARE HERE` AND CHECK IT.  There is deliberately NO LIVE marker in this file now, because
    the position it would mark is "nothing scientific is pending".  The phrase occurs exactly
    TWICE and BOTH are rule text about the hazard - this line, and the S104 chain's own note in
    the Order section.  A THIRD occurrence would be a real marker and would need checking. ***

EVERY DESIGN FIGURE WAS REBUILT FROM THE CONSTRUCTED MODULE IN S113, NOT TRANSCRIBED:
  ledger      2,368 + 66,560 + 128 + 102,528 + 27,936 + 18,528 + 970 = 219,018
  grid        all seven rows, parameter count AND stem RF, including the 82,778 row the band
              refuses by name
  MHA         228,330 - INSIDE the band [100,001, 1,000,000], so ONLY the exact count refuses it
  census      rung 2  Conv1d 9 / Linear 8 / GRU 1 (2 layers) / LayerNorm 5
              rung 1  Conv1d 19 / Linear 4 / GRU 0 / LayerNorm 10
  causality   perturbing every input after step 24 moved recurrent features at steps <= 24 by
              EXACTLY 0.0; later ones by > 0
  RNG order   caller's CPU RNG state unchanged
  suite       masking the gauge columns: 219,018 -> 219,018, shapes identical, outputs differ
  wrapper     TemporalAttributionEstimator accepts a rung-2 net with NO EDIT
  *** "eight gauge columns" in the design counts INPUT-TENSOR columns.  CHANNEL_WIDTH
      ["gauge_obs"] is 4 REGISTRY columns, each arriving twice (value + mask). ***
  *** THE STEM RECEPTIVE FIELD IS 31 AND THE PARAMETER COUNT 219,018.  My S118 test file pins
      both against `rung2_shape()` rather than trusting its own literals. ***

FOUR DISCLOSED LIMITATIONS PINNED BY TESTS RATHER THAN REPAIRED, ALL FROM DECISION D4:
  CAPACITY_LADDER's rung-2 entry still reads built=False; TemporalAttributionEstimator's and
  capacity_sweep.score_arm's annotations still say TemporalAttributionNet; and rung 2 exposes
  stem_receptive_field and DELIBERATELY NO receptive_field.  *** DO NOT EDIT
  attribution_net.py, dev_fit_trainer.py OR capacity_sweep.py.  A one-word edit to a
  comment-level field changes a RECORDED IDENTITY and R3 would then refuse every future run
  that reads the approved anchors - AND the S118 analyzer would refuse the completed run. ***

THE SEED BUDGET: FIVE seeds {0,1,2,3,4}, justified by COMMENSURABILITY WITH THE ANCHOR and
  EXPLICITLY NOT BY PRECISION.  Priced 5/10/20 = 12/22/42 fits; the run spent the 12.

TWO NUMBERS THAT ARE IN THE DESIGN BECAUSE THEY ARE THE INCONVENIENT ONES.  KEEP THEM:
  1  RUNG 1 REACHED THE LOWER SYNTHETIC LOSS.  Random labels on random inputs measure
     memorization and NOTHING ELSE.
  2  RUNG 2 COSTS ~12x PER STEP WHILE CARRYING 5.5x THE PARAMETERS - the GRU's sequential
     steps do not parallelize on CPU.  *** CONFIRMED AT SCALE: the real twelve-fit run took
     1,274.6 s.  A REAL EFFICIENCY FINDING, and it is now written into packet Step 30 with its
     own paragraph: on the hardware this project actually has, the cheaper-LOOKING axis of the
     ladder is the expensive one. ***
```

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 141**; next session I run is **Session 142**. **SESSION 141 BUILT SUB-STEP 4b-ii-a AND HANDED IT OFF, AND IT SPLIT THE 4b-ii REVIEW IN TWO.** It wrote two new files - `Reproducibility Packet/scripts/utils/connection_adapter.py` (blob `dafa73b5`, 70,511 B / 1,635 LF) and `Reproducibility Packet/tests/test_connection_adapter.py` (blob `9cadb11d`, 77,397 B / 1,909 LF, 109 tests) - implementing **read-order rows 4 through 12**, the roles-mode entry point of invariant W8, and **acceptance test B8 in full**; it opened `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md` and a new subject chat, and it **asked Codex to rule on the split before reviewing any content**. **THE FIRST WORK OF S142 IS WHATEVER CODEX'S ROUND 1 SAYS**, and if no Round 1 has landed the work is **4b-ii-b** - rows 13-21, the coherent geometry fixture, `X_GEOMETRY_UNSUPPORTED` at 15, the audit-hook observer, B2/B4/B5, the roles CLI wiring and the additive `build_role_bundle` change - under **its own new card and chat**, with **the two-pass mutation sweep budgeted BEFORE the handoff** (it has now changed the tests rather than confirmed them on **four** consecutive builds). **DO NOT BUILD 4b-ii-b BEFORE READING WHAT CODEX RULED ON THE SPLIT.** **SESSION 136 WAS A REGULAR PROGRESS-REPORT SESSION** - `agents/Claude/Progress Reports/Progress Report Session 136.md` covers S129-S136. **MY NEXT REGULAR PROGRESS REPORT IS SESSION 144**, or sooner if a phase transition or an approved written Claim-Sheet amendment fires. **THE STEP-1 DESIGN LOOP IS CLOSED at blob `0753d4ed` (me S127, Codex S127), THE STEP-2 LOOP AT `c12745ab`/`0ae5b19d`/`cf61e5aa`/`1833a472` (me S129, Codex S129), THE STEP-3 LOOP AT the ten fixture blobs + packet README `4bc07f18` + public README `3ab96e38` (me S130, Codex S130), AND THE STEP-4a DESIGN LOOP AT `032db166` (me S135, Codex S135) - DO NOT REOPEN ANY OF THEM, and an approved version is never edited in place.** **THE RUNG-2 ANALYSIS ARTIFACT IS CLOSED at blob `a2fa857b` / `604d7272...` (me S119, Codex S119), AND SECTION 5.4 IS JOINTLY APPLIED AND SPENT.** Both rung-2 authorization halves are spent, the one authorized run executed in Codex's S117 (`X_RUNG2_OK`, 12 fits) and the one authorized read in my S119 (`X_ANALYSIS_OK`, 11.97 s, zero fits). See the head block; this bullet is an index. **THE S112 REGULAR** is at `Progress Reports/Progress Report Session 112.md` (covers S105-S112); Codex read it in its S112 general recent-work review, raised exactly one correction, carried it forward onto the public log rather than into the report, and I approved it - no cycle is open on the report itself. **THE S104 AND S120 REGULARS ARE WRITTEN and still unreviewed by Codex; if it opens a loop on either, that loop is mine to close.** **THE S96 REGULAR'S LOOP IS CLOSED** at blob `c824173c` (Codex S97) and **THE S88 REPORT'S LOOP IS CLOSED** at blob `58276bb4` (Codex S89) - **DO NOT REOPEN EITHER.** *(The S80 report is still unreviewed; the S72 one was read in Codex's S72 general recent-work review, which found no correction to carry, so no explicit cycle ever opened on it.)* **A2 ALREADY FIRED AN AMENDMENT-TRIGGERED REPORT AND IT WAS CODEX'S TO WRITE** (its S76 wrote the approving turn); that does not reset either counter.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **THE "SLATED FOR FULL REGENERATION FROM ZERO AFTER A2" EXPECTATION IS RETIRED AS OF MY S75 — see A2.3.** Option C inserts no severity, so no seed ordinal shifts and A2 by itself invalidates none of this. If the set is ever superseded it is for some other reason, under its own authorization. **Still: read them, do not build on them** — nothing downstream of them is authorized either way.
- **THE PAYLOAD-BOUNDARY EXTENSION HAS RUN — Codex's S73, 127 physical rollouts, `X_CASE_EMPTY`, and the result artifact is JOINTLY APPROVED (Codex S73 / me S74).** The measurement is spent and no further payload-extension execution is authorized. **A2 IS IN FORCE at `baa8fd53…` / `203aab77…` — both agents approved those exact bytes (me S76, Codex S76). The two-file loop is CLOSED and the amendment is not to be reopened or status-edited.**
- **STAGES A/B/C HAVE RUN — Codex's S57, 135 physical rollouts, CASE_B, JOINTLY APPROVED.** Stage 0 RAN in S48 at ZERO rollouts; `results/protocol_p/sensor_only_difference_null.json` is tracked and **JOINTLY APPROVED**. The §9 role-coverage read is now **JOINTLY APPROVED** (above). The payload read's **RESULT ARTIFACT is JOINTLY APPROVED** (S60 Codex / S61 me); its **script + tests are JOINTLY APPROVED (Codex S61)**.
- **THE ROLLOUT COUNT HAS BEEN WRONG FIVE TIMES: one → four → thirteen → fourteen → FIFTEEN pre-run. Carry the table, never a remembered number.**
```text
*** THE LIVE COUNTERS.  TAKE THEM FROM HERE; TAKE THE DERIVATION FROM THE REFERENCE FILE. ***
  ROLLOUTS  278        FITS  67 PROJECT-WIDE, and 67 checkpoints
  *** THE FIT COUNTER READ `13 lifetime` FROM S98 TO S115 AND IT WAS SELF-SCOPE WHILE THE
      ROLLOUT COUNTER BESIDE IT WAS PROJECT-SCOPE.  Corrected S116.  RE-DERIVE, DO NOT
      REMEMBER - all three sources agree:
        fits         10 (dev_fit fits_run) + 3 (stage1-run-1) + 42 (stage1-run-2)
                     + 12 (rung2-run-1, Codex S117)                             = 67
        checkpoints  10 + 3 + 42 + 12 = 67, and `find results -name "*.pt" | wc -l` = 67
                     MEASURED AGAIN S118
        rollouts     15 pre-run replays + 136 (Codex S57) + 127 (Codex S73)         = 278
      OF THE 67 FITS, 13 ARE MINE (ten S84 dev + three S98 sweep) AND 54 ARE CODEX'S
      (42 in its S100, 12 in its S117).  *** THE RUNG-2 TWELVE ARE 2 EQUIVALENCE + 10
      MEASURED ARMS AND THEY ARE THE FIRST FITS SINCE S100. ***
      A COUNTER'S SCOPE IS PART OF THE COUNTER; two counters under one heading are read as
      sharing one scope, and if they do not, nothing in the file will say so. ***
  PILOT / VAL / TEST reads   0, every session, without exception
  *** S141 SPENT ZERO SCIENTIFIC RESOURCE - it is the 4b-ii-a BUILD SESSION.  It read
      `AgentPrompt.md`, `Project Details/Project Details.md`, this file, the APPROVED Step-4a design's
      sections 2.4, 3.1-3.5, 4.1-4.8, 5, 6 and 7, `Review Card/README.md`, four chat `Summary.md`
      files and Codex's HumanReport140; read `utils/connection_record.py`, `utils/storage_contract.py`,
      `utils/config_contract.py`, `utils/role_contract.py`, `utils/protocol_p.py` and
      `scripts/build_data_contract_fixture.py` AT SOURCE; WROTE TWO NEW PACKET FILES (one module, one
      test file, 109 tests); ran the focused suite (109), the focused suite under `-O` (109) and THE
      PACKET-WIDE SUITE (**2,717 passed, 0 failed, 169.01 s**); ran a TWO-PASS 29-MUTANT CONTROL
      ENTIRELY IN A SCRATCH DIRECTORY OUTSIDE THE REPOSITORY (deleted); wrote one new Review Card,
      opened one new chat with the owner handoff, and edited its own report, README, Permanent
      Instruments (lessons 239-241) and continuity file.
      *** IT OPENED NO ROLE INDEX, ROLE PAYLOAD, CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG,
      PRODUCTION CONFIG OR PILOT/VAL/TEST RESULT, BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT, RAN NO
      FIT AND RENDERED NO FIGURE.  Every tree its tests bind is under `tmp_path`.  Checkpoint count
      NOT RE-READ - no fit ran; it stands at 67. ***
      *** THE ONE DISCLOSED READ: `data/gate3-base-dev-pilot-val-c1-s/generation_audit.json` (1,256 B)
      and `independent_audit.json` (1,470 B), READ ONCE for their SHAPE so the step-6 contract would be
      written against the structure the delivered audits actually carry rather than an invented one.
      That is a read of delivered METADATA to inform a contract - the same kind S132 made - it opened
      no payload behind it, and NO TEST IN THE CANDIDATE DEPENDS ON THAT TREE EXISTING (finding DB). ***
  *** S140 SPENT ZERO SCIENTIFIC RESOURCE - it is the README ROUND-2 CLOSURE, THE CONVERGENCE RULE
      AND ONE MEASUREMENT AGAINST MYSELF.  It read `AgentPrompt.md`, `Project Details/Project
      Details.md`, this file, `Playbooks/review-cycle.md` IN FULL, `Playbooks/live-run-readme.md` IN
      FULL, `Review Card/README.md`, the README heartbeat card, both active-chat tails and Codex's
      HumanReport139; AUTHENTICATED the candidate and predecessor README blobs from the object store
      and PROVED the unchanged regions by reconstructing the predecessor BYTE FOR BYTE from the
      candidate; MEASURED ONE component-length bisect in a scratch directory OUTSIDE the repository
      (250/254/255 write, 256-260 raise `OSError` errno 22) and DELETED the scratch tree; APPENDED to
      two chats and one Review Card; WROTE the convergence ladder into `Playbooks/review-cycle.md`
      (+100/-1) and `Review Card/README.md` (+24/-0); and edited its own report, README, Permanent
      Instruments (lessons 236-238) and continuity file.
      *** IT OPENED NO ROLE INDEX, ROLE PAYLOAD, CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG,
      CONFIG OR PILOT/VAL/TEST RESULT, BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT, RAN NO FIT AND
      RENDERED NO FIGURE.  NO PACKET TEST WAS RUN - no executable file changed; the suite stands at
      2,608 as Codex measured it in S138.  Checkpoint count NOT RE-READ; it stands at 67.
      *** IT CHANGED NO PACKET CODE, TEST, SCHEMA, PROTOCOL DOCUMENT, CONFIGURATION OR RESULT, AND
      IT DID NOT EDIT `README.md` - it APPROVED Codex's bytes. *** ***
  *** S139 SPENT ZERO SCIENTIFIC RESOURCE - it is the README ROUND-1 REVIEW, RANDY'S DIRECTIVE
      AND ONE SETTLED FORWARD ITEM.  It read `AgentPrompt.md`, `Project Details/Project Details.md`,
      this file, `Playbooks/review-cycle.md`'s superseding section, `Review Card/README.md`, the
      README heartbeat card, all three active chats, the concluded 4b-i chat `Summary.md` and
      Codex's HumanReport138; AUTHENTICATED both README blobs from the object store; MEASURED two
      scratch probes OUTSIDE the repository - a filesystem case-fold/name-length probe and a
      `git checkout-index` EOL probe on `cable_mechanics.py` - and DELETED both scratch trees;
      APPENDED to two chats and one Review Card; and edited its own report, README, Permanent
      Instruments (lessons 232-235) and continuity file.
      *** IT OPENED NO ROLE INDEX, ROLE PAYLOAD, CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG,
      CONFIG OR PILOT/VAL/TEST RESULT, BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT, RAN NO FIT AND
      RENDERED NO FIGURE.  NO PACKET TEST WAS RUN - no executable file changed; the suite stands at
      2,608 as Codex measured it in S138.  Checkpoint count NOT RE-READ; it stands at 67.
      *** IT CHANGED NO PACKET CODE, TEST, SCHEMA, PROTOCOL DOCUMENT, CONFIGURATION OR RESULT, AND
      IT DID NOT TOUCH `README.md` - that file is the candidate under review. *** ***
  *** S137 SPENT ZERO SCIENTIFIC RESOURCE - it is the 4b-i ROUND-2 OWNER RESPONSE.  It read the
      approved Step-4a design's sections 3.1, 3.2, 4.2, 4.7, 4.8 and 5, `Playbooks/review-cycle.md`,
      the governing Review Card, Codex's Round-1 chat turn and its HumanReport136; MEASURED four
      Windows path hazards in a scratch directory outside the repository (NUL, NTFS alternate data
      stream, trailing dot, device alias); EDITED THREE PACKET FILES - `connection_record.py`
      (+338/-43), `test_connection_record.py` (+620/-4) and, as a disclosed scope expansion,
      `render_verification_scene.py` (+66/-4); ran the focused suite (311), the focused suite under
      `-O` (311) and THE PACKET-WIDE SUITE (**2,578 passed, 0 failed, 176.07 s**); ran TWO complete
      TWO-PASS 49-MUTANT CONTROLS entirely in SCRATCH DIRECTORIES OUTSIDE THE REPOSITORY; and
      REGENERATED THE STEP-3 FIXTURE FIGURE SET to the git-ignored
      `results/verification_fixture_reproduced/` to prove the renderer edit moved no published byte
      - all ten files at the same SHA-256.
      *** THAT REGENERATION IS THE ONLY FIGURE RENDER, AND IT IS A REPRODUCTION OF AN ALREADY
      APPROVED ARTIFACT INTO AN IGNORED DIRECTORY.  IT OPENED NO ROLE INDEX, ROLE PAYLOAD,
      CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG, CONFIG OR PILOT/VAL/TEST RESULT, BUILT NO MuJoCo
      MODEL, STEPPED NO ROLLOUT AND RAN NO FIT.  Every path the new tests bind names a file that
      DOES NOT EXIST, under `tmp_path`.  Checkpoint count NOT RE-READ - no fit ran; it stands at
      67. ***
  *** S136 SPENT ZERO SCIENTIFIC RESOURCE - it is the 4b-i BUILD SESSION.  It read the APPROVED
      Step-4a design in full, `Playbooks/review-cycle.md`, both Review Cards, the concluded Step-4a
      chat summary, the governance chat and Codex's HumanReport135; read `storage_contract.py`,
      `config_contract.py`, `protocol_p.py`, `role_contract.py`, `verification_scene.py`'s exit
      table and `build_role_bundle`, `cable_mechanics.extract_deformation_coordinates` and
      `schema/schema.json`'s storage/roles sections AT SOURCE; WROTE TWO NEW PACKET FILES (one
      module, one test file, 212 tests); ran the focused suite (212), the focused suite under `-O`
      (212) and THE PACKET-WIDE SUITE (**2,479 passed, 0 failed, 192.86 s**); ran a TWO-PASS
      44-MUTANT CONTROL entirely in a SCRATCH DIRECTORY OUTSIDE THE REPOSITORY; wrote one new
      Review Card, opened one new chat with the owner handoff, wrote the S136 progress report, and
      edited its own report, README (pruning the 7,800-character Slot-8 bullet to 2,259 per the
      README's own S104 rule), Permanent Instruments (lessons 223-224) and continuity file.
      *** IT OPENED NO ROLE INDEX, ROLE PAYLOAD, CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG,
      CONFIG OR PILOT/VAL/TEST RESULT, BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT, RAN NO FIT AND
      RENDERED NO FIGURE.  Every path the new tests bind names a file that DOES NOT EXIST, under
      `tmp_path`.  Checkpoint count NOT RE-READ - no fit ran; it stands at 67. ***
  *** S135 SPENT ZERO OF EVERYTHING - the OWNER HALF OF ROUND-TRIP 1 under the new method.  It read
      `Playbooks/review-cycle.md`, both new `Review Card/` files and the two new chats; authenticated
      the new subject chat (1,610 B / 34 LF / 0 CR, sha256 `8e77062e...`, matching HEAD) and BOTH of
      Codex's published artifact digests; read `utils/config_contract.py`'s validator and loader,
      `render_verification_scene.py`'s roles CLI and `verification_scene.py`'s `build_role_bundle` AT
      SOURCE; measured the packet-root derivation and that NO `config.json` exists anywhere in the
      packet; ran ONE focused test file (`tests/test_data_contract.py`, 18 passed, 0.79 s); edited
      TWO tracked documents (the design, +104/-35; the Review Card); appended TWO chat turns
      (+7,832 B and +4,400 B, both prefix-verified); and edited its own report, README, Permanent
      Instruments (lessons 220-222) and continuity file.
      *** IT OPENED NO ROLE INDEX, ROLE PAYLOAD, CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG OR
      PILOT/VAL/TEST RESULT, BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT, RAN NO FIT AND RENDERED NO
      FIGURE.  The packet-wide suite was NOT re-run - no executable file changed; it stands at 2,267
      as last measured in S131.  Checkpoint count NOT RE-READ; it stands at 67. ***
      *** NO PROBE FILE WAS CREATED THIS SESSION - unlike S134, nothing needed materialising.  The
      only scratch artifacts are my audit script and the two chat-turn drafts, all outside the
      repository. ***
  *** S134 SPENT ZERO OF EVERYTHING - the THIRD STEP-4 OWNER RE-REVIEW.  It authenticated the
      transcript boundary (BOTH of Codex's published prefix digests reproduce byte for byte) and
      the reviewer artifact; read the reviewer's turn and the full diff; re-read
      `utils/config_contract.py` END TO END and `schema/schema.json`'s config contract; DROVE a
      synthetic complete frozen document through the live contract under THREE FILENAMES at BOTH
      `require_frozen` settings, in a scratch directory OUTSIDE the repository, deleting the probe
      files and re-measuring that the packet holds no `config.json`; read
      `tests/test_data_contract.py`'s frozen-shape tests; edited ONE tracked design document; ran a
      53-check audit over the result; appended one chat turn; and edited its own report, README and
      continuity file.
      *** IT OPENED NO ROLE INDEX, ROLE PAYLOAD, CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG OR
      PILOT/VAL/TEST RESULT, BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT, RAN NO FIT AND RENDERED NO
      FIGURE.  The packet suite was NOT re-run - no executable file changed. ***
      *** THE PROBE IS THE ONE THING WORTH NOTICING: it CREATED a file named `config.json` in a
      SCRATCH DIRECTORY OUTSIDE THE REPOSITORY, drove it through the validator, and DELETED it.
      That is the safe form of the very hazard finding DD names, and it is why DD's repair moves
      4b's frozen test OFF the filesystem entirely. ***
  *** S133 SPENT ZERO OF EVERYTHING - the SECOND STEP-4 OWNER RE-REVIEW.  It authenticated the
      transcript boundary and the reviewer artifact; read the reviewer's turn and the full diff;
      read `utils/config_contract.py` and `schema/schema.json`'s config contract AT SOURCE; DROVE
      the tracked draft config through `load_config` BOTH WAYS; re-read the FROZEN Slot-8 design's
      argument table, provenance table, fixture-mode paragraph and exit table; LISTED the delivered
      role root's top level (DIRECTORY METADATA, no file opened) and grepped `tests/` for its name;
      edited ONE tracked design document; appended one chat turn; and edited its own report, README,
      Permanent Instruments (lessons 216-217) and continuity file.
      *** IT OPENED NO ROLE INDEX, ROLE PAYLOAD, CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG OR
      PILOT/VAL/TEST RESULT, BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT, RAN NO FIT AND RENDERED NO
      FIGURE.  Loading the TRACKED DRAFT CONFIG through the packet's own validator is a read of
      tracked draft bytes to check a reviewer's claim, not a scientific input. ***
      *** THE PACKET SUITE WAS NOT RE-RUN - no executable file changed, the S127 judgment applied
      again.  It stands at 2,267 as last measured in S131.  Checkpoint count NOT RE-READ - no fit
      ran; it stands at 67. ***
  *** S132 SPENT ZERO OF EVERYTHING - the STEP-4 OWNER RE-REVIEW.  It read the reviewer-repaired
      design and the diff against my own handoff; read `scripts/utils/synthetic_plant.py`,
      `scripts/build_data_contract_fixture.py`, `scripts/utils/verification_scene.py` and the FROZEN
      Slot-8 design AT SOURCE; read `manifest.csv`, BOTH DATASET AUDITS and the DRAFT CONFIG and
      recomputed the manifest census itself; drove `synthetic_privileged_record` at the delivered
      fixture settings IN MEMORY to measure the tip-deflection range; re-measured the EXIT_CODES
      table and the six-module import graph in a FRESH INTERPRETER; edited ONE tracked design
      document (+264/-163 against Codex's state, my own edits on top); appended one chat turn
      (`+179/-0`); and edited its own README (+1/-1) and continuity file.
      *** IT OPENED NO ROLE INDEX, ROLE PAYLOAD, CHECKPOINT, ESTIMATOR OUTPUT, CONTROLLER LOG OR
      PILOT/VAL/TEST RESULT, BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT, RAN NO FIT AND RENDERED NO
      FIGURE.  Reading `manifest.csv` and the two audits is a READ OF DELIVERED METADATA to check a
      reviewer's census claim, not a scientific input, and it opened no payload behind them. ***
      *** THE PACKET SUITE WAS NOT RE-RUN - no executable file changed this round, which is the
      S127 judgment applied again.  It stands at 2,267 as last measured in S131. ***
      Checkpoint count NOT RE-READ - no fit ran; it stands at 67. ***
  *** S131 SPENT ZERO OF EVERYTHING - it read the frozen Slot-8 design, the packet module and
      renderer at source, `utils/role_contract.py`, `utils/storage_contract.py`,
      `utils/cable_mechanics.py`, `utils/synthetic_plant.py`, `scripts/build_data_contract_fixture.py`,
      `schema/schema.json` and the DRAFT CONFIG; measured two import graphs in FRESH INTERPRETERS;
      ran the PACKET-WIDE SUITE (2,267 passed, 0 failed, 204.35 s); WROTE ONE NEW TRACKED DESIGN
      DOCUMENT; appended one chat turn (`+203/-0`); and edited its own README and continuity file.
      *** IT OPENED NO CONFIG PAYLOAD, ROLE INDEX, ROLE PAYLOAD, CHECKPOINT OR CONNECTION RECORD,
      BUILT NO MuJoCo MODEL, STEPPED NO ROLLOUT AND RENDERED NO FIGURE.  Reading the draft config's
      JSON to measure which `values.*` paths are null is a READ OF A TRACKED DRAFT, not a
      scientific input. ***  Checkpoint count NOT RE-READ - no fit ran; it stands at 67. ***
  *** S130 SPENT ZERO SCIENTIFIC RESOURCE AND IS THE FIRST SESSION SINCE S119 THAT WROTE
      BINARY ARTIFACTS INTO THE PACKET - it ran ONE scripted render of the SYNTHETIC fixture
      (`--fixture-seed 7`) into `Reproducibility Packet/results/verification_fixture/`, ten
      files / 2,489,056 B, plus TWO further renders into scratch directories OUTSIDE the
      repository for the determinism comparison; drove the `roles` subcommand to its refusal;
      ran `git checkout-index` into a short scratch path to measure fresh-checkout EOL
      behaviour; and ran the focused suite (159), the focused suite under `-O` (159) and THE
      PACKET-WIDE SUITE (2,267).  It edited the packet README, both `.gitattributes`, the packet
      `.gitignore` and the public README, and appended two chat turns.  *** IT OPENED NO CONFIG,
      ROLE INDEX, ROLE PAYLOAD, CHECKPOINT OR CONNECTION RECORD, BUILT NO MuJoCo MODEL AND
      STEPPED NO ROLLOUT.  A SCRIPTED RENDER OF A LABELLED SYNTHETIC FIXTURE IS NOT A RUN AND
      MOVES NO COUNTER HERE. ***  Checkpoint count NOT RE-READ - no fit ran; it stands at 67. ***
  *** S129 SPENT ZERO OF EVERYTHING - the Step-2 owner re-review: a 48-check independent probe,
      a five-mutant control and a two-mutant test-justification control, all in SCRATCH
      DIRECTORIES OUTSIDE THE REPOSITORY; one changed test blob; one chat turn.  Its packet-wide
      figure (1,344 / 1 / 28) IS AN ARTIFACT OF THE SMART APP CONTROL BLOCK AND MUST NOT BE
      QUOTED AS A SUITE MEASUREMENT - see the head block. ***
  *** S128 SPENT ZERO OF EVERYTHING - it read the frozen Slot-8 design, `schema/schema.json`,
      `utils/metrics.py`, `utils/estimator.py`, `utils/role_contract.py`,
      `utils/assignment_generator.py`, `utils/cable_plant.py` and `utils/protocol_p.py` AT
      SOURCE; WROTE FOUR NEW PACKET FILES (two modules, two test files, 144 tests); rendered
      the synthetic fixture figure set into SCRATCH DIRECTORIES OUTSIDE THE REPOSITORY ONLY;
      appended one chat turn (+205/-0) and one `director_requests.md` entry (+41/-0).  It
      opened NO real payload, role index, checkpoint or config, BUILT NO MuJoCo MODEL and
      STEPPED NO ROLLOUT.  *** THE PACKET-WIDE SUITE COULD NOT BE MEASURED - see the MuJoCo
      block in the head.  My two new files: 144 passed, and 144 again under `python -O`. ***
      Checkpoint count NOT RE-READ - no fit ran; it stands at 67 as last measured. ***
  *** S127 SPENT ZERO OF EVERYTHING - it read `utils/metrics.py`, `utils/role_contract.py`,
      `utils/assignment_generator.py`, `utils/online_loop.py`,
      `scripts/build_data_contract_fixture.py` and `schema/schema-v1.0.md` AT SOURCE; drove the
      live `j_5s` against SIX fabricated window/grid cases IN A SCRATCH DIRECTORY OUTSIDE THE
      REPOSITORY; edited one tracked design document (+34/-11) and appended one chat turn
      (+149/-0).  It opened NO real payload or role index, BUILT NO MuJoCo MODEL and STEPPED NO
      ROLLOUT, and ran NO packet test suite because no executable file changed.  Checkpoint count
      NOT RE-READ - no fit ran and nothing this round depends on it; it stands at 67 as last
      measured. ***
  *** S126 SPENT ZERO OF EVERYTHING - it read `utils/metrics.py`, `utils/estimator.py`,
      `utils/role_contract.py`, `utils/online_loop.py`, `utils/cable_plant.py`,
      `utils/schema_types.py`, `utils/assignment_generator.py`, `schema.json`, the draft config
      and the approved Gate-3 assignment AT SOURCE; drove `j_5s` on EIGHT reconstructed real
      control grids and the role contract on synthetic payloads, ALL IN MEMORY; edited one
      tracked design document (+71/-23) and appended one chat turn (+155/-0).  It BUILT NO MuJoCo
      MODEL and STEPPED NO ROLLOUT - the grid reconstruction is pure float arithmetic.  It opened
      NO real data and ran NO packet test suite, because no executable file changed.  Checkpoint
      count unchanged at 67. ***
  *** MY S105-S127 EACH SPENT ZERO FITS, CHECKPOINTS, ROLLOUTS, GENERATION RUNS, C7
      INVOCATIONS AND PILOT/VAL/TEST READS.  *** S125 SPENT ZERO OF EVERYTHING - it read
      `utils/metrics.py`, `utils/estimator.py` and `utils/protocol_p.py` AT SOURCE, drove a
      `json` behaviour sweep, a 300-DPI PNG chunk walk and SIX `j_5s` time grids entirely in a
      SCRATCH DIRECTORY OUTSIDE THE REPOSITORY against synthetic arrays, edited one tracked
      design document (+85/-25) and appended one chat turn (+205/-0).  It opened NO real data and
      ran NO packet test suite.  Checkpoint count unchanged at 67.  *** S124 SPENT ZERO OF EVERYTHING - it read
      `schema.json`, `utils/estimator.py`, `utils/metrics.py`, `utils/role_contract.py`,
      `utils/protocol_p.py`, `utils/config_contract.py` and the packet `requirements.txt` AT
      SOURCE, drove an argparse replica and a matplotlib PNG probe entirely in a SCRATCH
      DIRECTORY OUTSIDE THE REPOSITORY, edited one tracked design document (+44/-8) and
      appended one chat turn (+151/-0).  It opened NO real data and ran NO packet test
      suite.  Checkpoint count unchanged at 67.  *** S123 SPENT ZERO OF EVERYTHING - it read the
      rung-2 analysis artifact under a digest refusal, the Claim Sheet, the draft config's
      `config_hash` and the packet `requirements.txt`, ran `pytest --collect-only` on the packet
      suite (2,108 collected, 35.80 s, UNCHANGED), wrote ONE new tracked design document, and
      appended one chat turn.  It touched NO real data.  Checkpoint count unchanged at 67.
      *** S122 SPENT ZERO OF EVERYTHING - it read four
      TRACKED files (the analysis artifact under a digest refusal, the run record, the
      equivalence artifact and the frozen design), appended one public log entry and one
      chat turn, and touched NO real data at all.  Checkpoint count unchanged at 67.
      *** S121 SPENT ZERO OF EVERYTHING INCLUDING
      PLAN MODE - it read the tracked artifacts, constructed the two networks in memory to
      count parameters, and read two executables at source.  Checkpoint count unchanged at
      67 (Codex re-counted 67 on disk in its S120).  *** S120 SPENT ZERO OF EVERYTHING - its probe and
      10-mutant control read only the TRACKED artifact and the FROZEN design, and wrote their
      mutants into TEMPORARY DIRECTORIES, never into the packet.  Checkpoint count re-measured
      on disk in S120: 67, unchanged.  *** S119 SPENT ONE PRODUCTION ANALYZER
      INVOCATION - THE ONLY ONE EVER AUTHORIZED ON THIS LANE, AND IT IS SPENT.  It read the
      approved DEVELOPMENT rows and twelve checkpoints, moved NO counter here, and left the
      checkpoint count at 67 (re-measured on disk in S119). ***  S118 ALSO SPENT ZERO ANALYZER
      INVOCATIONS AND TOUCHED NO REAL DATA AT ALL - its recomputation tests construct a FRESHLY
      INITIALIZED, NEVER-FITTED rung-2 network in a temp directory and score it on four
      synthetic examples, which is the only way to give the score comparison an accept
      side.  THE TWELVE FITS ON THE COUNTER ABOVE ARE CODEX'S, NOT MINE.  S113-S116 touched no real data at all.
      *** S116 IS THE ONE THAT TOOK THE GATED PLAN ACTION: four plan-mode invocations, three
      into SCRATCH and ONE into the packet, producing the tracked artifact above.  A PLAN IS
      NOT A FIT AND NOT A ROLLOUT; it moves no counter here. ***
      *** S117 READ REAL DATA FOR THE FIRST TIME SINCE S112, AND ONLY AS A PRE-AUTHORIZATION
      CHECK: one `load_dev_examples` call through the APPROVED `load_authorized_examples`
      (dev split only, 304 of 944 rows, 2.1 s), plus a sha256 of the ten approved .pt files.
      A READ IS NOT A FIT.  It moved no counter and it wrote nothing into the packet. ***
  *** A FIT IS NOT A ROLLOUT and A READ IS NEITHER.  Do not let the counters merge. ***
  *** THE ROLLOUT COUNT HAS BEEN WRONG FIVE TIMES: one -> four -> thirteen -> fourteen ->
      FIFTEEN pre-run.  TAKE THE COUNT FROM THE ARTIFACT'S OWN LEDGER, NEVER FROM A
      PER-ROLLOUT FIGURE, AND NEVER FROM MEMORY. ***
  The full per-session spend history and the fifteen-rollout reconciliation table are in
  `agents/Claude/Permanent Instruments.md`, section "THE RESOURCE-SPEND HISTORY".
```
- **Progress report DONE at S64** (regular, covers S57–S64) at `agents/Claude/Progress Reports/Progress Report Session 64.md`. **ITS LOOP IS CLOSED AT `b0ff7496` — Codex explicitly approved that exact blob in its S65 (`HumanReport65.md:81-82`), and I had already approved it, so both approvals name the same bytes. DO NOT REOPEN.** *(This line said OPEN through five of my own sessions after the loop had closed, and the Pointers section said CLOSED the whole time — my own summary contradicted itself and I only caught it in S80 by grepping the file rather than reading it. Lesson 65 exactly: a status clause that has been true for several consecutive rewrites is the most likely thing to be carried into one where it is false.)* Round history, kept because the figure it argues about was wrong five times: Codex made two edits in its S64 (the ledger refuses a duplicate LOUDLY, not silently; and "151 rollouts, about 70 minutes" contradicted my own line 14's audited 4,432.16 s), I verified both against primary records and accepted both diagnoses AND implementations, then moved one clause out of the present tense (+4/-3) because "still cannot run until payload mass is part of the key" stopped being true in S63/S64. Prior status — the S56 one ran five review rounds, so expect Codex may open one. `Progress Report Session 56.md` (S49–S56) stays closed at blob `83c527ce…`; do not reopen it. **THE S72 REGULAR IS WRITTEN** — `agents/Claude/Progress Reports/Progress Report Session 72.md`, covering S65–S72. **Codex read it in its S72 general recent-work review and found no correction to carry, so no explicit review cycle opened on it.** Its spine: eight complete adversarial rounds on one program, every round finding something real and each structurally below the last; then the loop closing and the program producing the zero-rollout plan. It states both halves of the trade — what the rounds bought, and that eight of my sessions produced no science — and names where I think the cost stopped being obviously worth it. **THE S88 REGULAR IS WRITTEN AND IN AN OPEN LOOP AT `58276bb4`.** Codex's S88 struck two sentences of mine that said the sweep would tell us whether the first result was *caused* by an undersized network — a causal claim the design I wrote in the same session explicitly disclaims. It was right; I kept the substance whole in S89 and added only two things: the register (its replacement carried unglossed jargon in the paragraph a non-specialist reads first, and this report is at the Accessible-Piece bar) and two forward-looking statements that went stale between the sessions (the route is now ruled; the count is 42, not 40). Its spine: the ten development fits ran and produced the project's first learned-model numbers; the two findings that matter are that S fit slightly worse at a fixed width (a capacity statement, with the MECHANISM explicitly unmeasured) and that the seed spread is 3x the success bar; and the stretch's recurring lesson, that a fixture repaired along the measured axis stayed degenerate along one nobody named while the real data shares the same accident. *(That paragraph originally closed "my next regular is Session 96"; that was true when written, the S96 report has since been written and jointly closed, and the live figure is the one in the session line above. Corrected S103 after a grep of my own finished rewrite found this contradicting it - lesson 65 exactly, and the second time in one session.)*

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

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → Protocol P v2.3.3 spec ✓✓ → seam + 37 tests ✓✓ → replay gate ✓✓ → Stage-0 implementation ✓✓ → **Stage 0 RAN, S48 ✓** → Stage-0 result ✓✓ → Progress Report S48 ✓✓ → packet Step 24 ✓✓ → public README ✓✓ → extraction + construction layer ✓✓ (S51–S53) → driver + results layer (S54 built, S54 blocked, S55 corrected, S55 approved ✓✓) → S56 pre-registered helper + Step 25 ✓✓ → **Codex S57: replay gate (36.42 s) then STAGES A/B/C — 135 rollouts, CASE_B ✓** → **my S58: every number independently reproduced, result APPROVED; §9's role-coverage read found UNIMPLEMENTED and built at zero rollouts — dev 0 / pilot 0 / val 1 / test 1** → **Codex S58 BLOCKED it on three real findings and corrected it** → **my S59: all three CONFIRMED; a FOURTH found in the repair (raw-domain digest of a tracked text file); 23-case sweep, 13 survivors, 12 real, closed with 12 tests** → **Codex S59 APPROVED all four states and held the loop open for my explicit approval** → **my S60: approval posted, LOOP CLOSED AT THE SAME STATE; the mutation-sweep harness found to give false verdicts and fixed; the approved analyzer re-swept clean (28/28); the payload-conditioning read built at zero rollouts** → **Codex S60 blocked the payload read on two real defects, corrected them, ruled MEASURE FIRST via a separate development-only pre-registration, and blocked A2** → **my S61: both findings confirmed independently; the result artifact and both READMEs approved at Codex's states; the sweep over Codex's repair found a SILENT GAP in one of its own new guards and a three-way message collision one copy of which is built by an f-string; script+tests returned at new blobs; the payload-boundary extension v0.1 DRAFTED** → **Codex S61 APPROVED the analyzer/tests (loop CLOSED) and BLOCKED the extension on four findings** → **my S62: all four confirmed against primary sources, none contested; v0.1 `git mv`'d to v0.2 and rewritten — CRN across masses, a SECOND prerequisite (`PhysicalKey`), one ordered exhaustive classifier, pinned artifact/provenance contracts, the anchor staged first; plus three findings of my own (zero gravity, probe 97x below the lowest mode, a noise-fragile anchor)** → **Codex S62 made FIVE direct edits to v0.2 and approved its own state `e5192eaa` — circular provenance payload, plan/execute split, the anchor cannot prove payload liveness (its source reservation already carries 0.050 kg), result joins as data, reduced coverage licenses nothing** → **my S63: all five accepted, three verified at source; ONE NEW DEFECT found in Codex's own new text — R10 `X_CASE_EMPTY` kept the weaker Option-B rule Codex had just tightened at R11, and over all 19,448 states DELETING a result raised the licensed cap in 3,185 of them; fixed by unifying the rule (0 remain), state returned at `538ae06b`** → **Codex S63 APPROVED `538ae06b`, CLOSING THE DOCUMENT LOOP, then built two of the three Step-2 prerequisites and approved its own four-file state** → **my S64: both of Codex's changes verified with my own 10-case two-pass sweep (10/10 caught, 0 survivors); ONE defect found — `PhysicalKey` gained the payload field while `LogicalRow.physical`, the ONLY producer of a key in that module, could not set it, so the extension's 126 rollouts resolved to 18 keys; fixed additively; four-file state approved at `b7b2430a`/`c23e61d3`/`2f7c33b2`/`ad6b32fe`** → **my S65: Codex's executable could not have completed ONE execute run — wrong replay reservation, `UnboundLocalError` in the XR handler, an exception class outside the measurement handler; five corrections, state returned at `ff0cdbe6`/`ebdfdf83`** → **Codex S65 accepted all five including the `resolve_replay_source` extraction, found TWO more real X6/X7 exits, corrected them, approved `eb94afb2`/`5d8dd369`, and closed my progress-report loop at `b0ff7496`** → **my S66: both of Codex's findings accepted in full; FOUR MORE defects found by RUNNING — X7's writer guard destroying the X6 record on the wrong-plan exit, the same crash reachable through Codex's brand-new missing-argument exit, `//host/share` surviving both scrubbers, and my own S65 Windows regex eating every URL — plus two silent execute exits and an untested branch; state returned at `431d9c08`/`4d194a67`** → **Codex S66 accepted all four, found TWO more — a non-object `inputs` field crashing `execute_document_skeleton` while assembling the failure record, and an absolute path used as a JSON MEMBER NAME surviving both the scrubber and the writer — corrected both and approved `86fc3fdb`/`e081a26d`** → **my S67: both reproduced against my own blob and both implementations kept unchanged; a THIRD family found by ENUMERATION rather than reading — the scrubber is a list of spellings and the writer's guard is a `PurePath` predicate, and they disagreed on 1,358 of 37,448 strings (bare roots; drive letters `PurePath` accepts and `[A-Za-z]` does not), nine of which killed the write through `main()`; fixed by making the scrubber's post-condition BE the guard, run to a fixpoint; plus the authorized path closed at the gate by a refusal rather than a rewrite; state returned at `5a5b0562`/`f2f5031d`** → **Codex S67 accepted all three, ruled that the authorization-gate refusal does NOT reopen the verbatim-embedding scope, found THREE more execute-exit shapes — a real Windows path glued onto prose with no delimiter, values `json.loads` accepts that canonical JSON cannot represent (`1e9999` -> `inf`, a lone surrogate), and a foreign plan too deeply nested for the recursive visitors — and approved `25386e27`/`ab4ddfc0`** → **my S68: all three accepted and kept unchanged, with a SCOPE CORRECTION on two (the unserializable values only reach the writer under `inputs`/`protocol`/`plan`, and the recursion threshold is a property of the CALLER'S stack, not of this file — measured at two ambient depths); ONE NEW DEFECT found in the repair itself — dropping the drive-letter token boundary made a state reachable where the post-condition discards the WHOLE reason, measured on three realistic sentences and 6 of 37,448; fixed by running the substitutions to a FIXPOINT; state returned at `04ec936e`/`4979af07`** → **Codex S68 accepted all of it and found ONE more — the embedded-path regex accepted a narrower drive alphabet than the file's own declared `PureWindowsPath` semantics, so an embedded `1:\…` was published — corrected it and approved `9cd10305`/`ce0cd642`** → **my S69: that finding reproduced (82 leaking renderings of 286 under my blob, 34 under Codex's, 0 under the state I returned) and every line of its repair kept; FOUR MORE found by a CROSS-PRODUCT rather than a reading — a UNC path glued to prose published whole, a path CONTAINING A SPACE reduced only to its first space-free run (this repo's own parent has a space), a mixed-separator span whose reduction kept the parent directory, and the single-slash POSIX form glued to a word, which I DID NOT FIX and disclosed instead because closing it turns `dev/pilot/val` into `val`; state returned at `9fd723b0`/`191d9b4d`** → **Codex S69 accepted all four and the single-slash judgment, changed NO operational expression (executable AST identical, which I verified), and corrected the DISCLOSURE — it was narrower than the measured behaviour, because a space-containing forward-drive, forward-UNC or mixed-separator path also leaves a relative private suffix — approving `f2d9f3b1`/`eb10bb23`** → **my S70: every word of that kept, and a NEW defect found by widening the grid where it was thinnest (a prefix ending in a letter-colon) — `reason://host/PRIVATE/row.npz` was published BYTE-IDENTICAL because the forward-UNC lookbehind read "any alphanumeric + colon is a URI scheme", and the writer's guard shares the pattern so it declined too; eight more cells kept the DRIVE DESIGNATOR; repaired by NAMING the protected schemes (`file` deliberately off the list) and by having the forward-slash drive form refuse a second slash, at zero measured prose cost, with the converse cost disclosed and pinned; the sweep also caught that my own repair had made `_final_component`'s both-separator split untestable; state returned at `c7451068`/`485dcc3d`** → **Codex S70 accepted both diagnoses and the whitelist judgment and found ONE more — my per-name lookbehind matched a listed scheme as the SUFFIX of a longer unlisted token — approving `c850a4b6`/`150870f4`** → **my S71: every line kept and NO operational expression changed (verified AST-identical), and THREE COVERAGE GAPS found by MUTATION rather than by a red check — `_URI_SCHEMES` was adopted by its own parametrized tests so adding a scheme leaked silently, the accept side was only ever tested at a space or at start-of-string, and one of my own disclosures misstated its measured behaviour; 18 cases added, state returned at `95040d93`/`0d7b68fc`** → **Codex S71 ACCEPTED ALL THREE AND APPROVED THOSE EXACT BYTES — the eight-round loop CLOSED, and STEP 2 with it** → **my S72: STEP 3 run, plan mode only, 0 rollouts, `plan_valid=true`; every load-bearing number re-derived from the artifact's own published fields without importing the executable; artifact APPROVED and the second read handed to Codex** → **Codex S72: the second independent read, 35 checks, anchor rebuilt from the committed screen result, 126/126 keys reproducing the published digest — SAME BYTES APPROVED, so STEP 3 IS COMPLETE** → **my S73: the whole §3.3 pre-rollout surface audited at ZERO rollouts (14/14, including the two checks that sit BELOW the rollout in the gate), the authorization gate driven directly (14/14), the ephemerality bracket measured (0 of 3,203 watched files change across a warm plan run) and its one uncloseable residual named — a CONCURRENT WRITER — and MY HALF of the Step-4 execution authorization issued** → **Codex S73: the matching half, then STEP 5 RAN ONCE — 127 rollouts, `X_CASE_EMPTY`; artifact approved by Codex S73 and by me S74 after 130 checks** → **my S75 drafted AMENDMENT A2; Codex S75 edited it; my S76 made one `+1/-1` technical correction; Codex S76 APPROVED THOSE EXACT BYTES — A2 IS IN FORCE, and BOTH its duties (progress report, README milestone) fired in Codex's S76** → **my S77: GATE 4 OPENED — Slot 9 rung 1 built at 39,594 parameters, 0 rollouts; Codex S77 ruled on both requested questions and blocked one real defect; the rung's loop CLOSED at `c4fa3c63`/`5a401ca1` (me S78, Codex S78)** → **the DEV-FIT CONTRACT, three adversarial rounds and still open: I built it S78 → Codex S78 blocked on four → my S79 kept every line and found two more → Codex S79 blocked on two more (`$` before a final newline; foreign exceptions) → my S80 kept every predicate and found ONE more, the module's only silent accept, at `9d6ecfea`/`d4202c8e` → Codex S80 accepted all of it, ruled the forty escapes stay open, and blocked on ONE cross-field defect (Finding F) which it repaired → **my S81 reproduced F against my own blob, kept every line, measured both call sites load-bearing (7/7 mutation), found Finding G and DISCLOSED rather than blocked, and APPROVED `bd2c0d08`/`fbd941b5` — THE CONTRACT LOOP IS CLOSED → I then BUILT THE TRAINER (`275a7a50`/`80d9722f`) → **Codex S81 ruled Finding G as (b) (CLOSED) and BLOCKED the trainer on six executable findings (H–M) plus the missing training-window policy, returning `fd2c8c9b`/`9d9455b7` → my S82 PRESERVED ALL SIX (H reproduced against my own blob, I's four pins re-derived and its enforcement traced one layer down), found FINDING N inside Codex's own Finding-L repair, and SUPPLIED THE WINDOW POLICY — derived per trajectory from the approved assignment, reproducing Protocol P's `[1000, 1768)` exactly — returning `10054696`/`9e76923c` → **Codex S82 APPROVED THE WINDOW POLICY (the project's one outstanding SCIENTIFIC decision, now settled), narrowed my "excitation is the only difference" overstatement, and BLOCKED the executable on four findings (O identity-matching, P the persisted-label onset binding, Q malformed schedule controls, R mixed checkpoint generations), returning `788fc240`/`c95bd8fb` → my S83 reproduced ALL FOUR against my own blob and kept all four implementations, found FINDING S (the stale-output guard's own refusal wrote `dev_fit_result.json`, the SOLE provenance record for the checkpoints it was refusing to mix with — measured, and the exit above it destroyed the same record without the guard running) and FINDING T (set equality is not multiset equality, so an unmatched pairing was accepted), closed five coverage gaps the sweep exposed, and returned `b9d7bb6f`/`3a81eecc` → **Codex S83 reproduced both, ACCEPTED S and T and the sixth exit and the `_exact_steps` deletion, and blocked on TWO of its own — U (the refusal artifact sat outside the cleanliness guard, so a directory holding only it was accepted as clean and ended with two contradictory terminals) and V (one docstring still carried the superseded “excitation is the only difference” sentence) — returning `caa00418`/`cbc4064f` → **my S84 reproduced BOTH against my own blob, kept both repairs, MEASURED that the Finding-S recurrence I went looking for is NOT there, found FINDING W (the refusal reports through the name whose occupancy triggers it, so an unwritable occupant turns a named exit into an uncaught `PermissionError`) and DISCLOSED rather than blocked it under Codex's own S80 ruling, and **APPROVED `caa00418`/`cbc4064f` — THE LOOP IS CLOSED** → **THE TEN DEVELOPMENT FITS THEN RAN, X_FIT_OK, 0 rollouts** → **Codex S84 independently audited the ledger and approved it, RULED Finding W disclosed (on the stronger ground that the trainer's bytes are the ten checkpoints' recorded producer) and RULED Finding X forward into a new read-only analyzer rather than rewriting the ledger** → **my S85: OWNER APPROVAL of the ledger after independent verification, both rulings accepted, and five findings in the analyzer — a published RAW digest a fresh checkout cannot reproduce, a hand-copied loss with nothing comparing it to `arm_loss`, 15 of 22 mutation survivors, a false `hardware-stable` docstring, and no binding from the tracked artifact to its own producer — four repaired, the artifact regenerated with every number unchanged, state returned at `31381b18`/`f97c359b`** → **Codex S85 APPROVED the analyzer, the artifact and the packet README unchanged (those three loops CLOSED), RULED 6(a) no-refactor — REJECTING my premise, correctly — and RULED 6(b) correct-the-public-log-forward, appending a dated note rather than reverting; it then added five tests through the existing seams and honestly declined to quote a mutation score it had not measured** → **my S86: the public README correction APPROVED UNCHANGED after verifying it removed ZERO bytes and that its claim about the log's own history is faithful to the primary blobs; my limitation 130 CORRECTED as false; and the missing measurement supplied — 14 derivation-path cases, 10 caught against Codex's state, the 4 survivors traced to THREE DEGENERATE FIXTURES (uniform census, constant paired difference, self-counting loader stub) rather than to any code defect, all three repaired with no production change and no regeneration, re-swept to 14/14 and confirmed by a negative control; test file returned at `c7b0a093`** -> **Codex S86 accepted all three fixture repairs and corrected ONE FALSE COMMENT of mine (`sensor` IS the last key of the count mapping), approving its own state `4481ba32`** -> **my S87: Codex's correction ACCEPTED IN FULL, and its replacement comment CONTESTED because it carries the same defect one notch smaller - measured, two agreeing passes with both negative controls surviving, a last-key selector SURVIVES against `4481ba32` while first-key, `min` and `min(proportions)` are all caught; the cause is structural (the census is built in `SOURCE_CLASS_ORDER`, so ascending counts put the majority at the LAST key) and the delivered 8/16/32/96 census is peaked on `sensor` too, so nothing in the project separates the selector from the ordering unless the fixture's majority is deliberately INTERIOR; repaired by reordering the counts to `(1, 2, 4, 3)`, every published number unchanged, test count unchanged at 35, state returned at `6f29bf05`; and the SLOT-9 CAPACITY ESCALATION DESIGNED and handed over as `protocol/capacity-escalation-v0.1.md` (`b86d46aa`), against Codex's stated sequencing, flagged as a deviation with the call handed back** -> **Codex S87 APPROVED `6f29bf05` but held the loop open on a process gate (I had never literally approved my own returned bytes) and BLOCKED the design on five findings with three rulings** -> **my S88 CLOSED the test loop with an explicit owner approval, accepted all eight without contest, and found three more - the trainer is WIDTH-LOCKED AT 32 (limitation 134) and the saturation criterion was on the wrong quantity (limitation 135); returned at `ccd12ef4`** -> **Codex S88 EDITED BOTH my open artifacts, made five executable-contract repairs, RULED all five open questions (Route A; post-anchor label; 6-dp tie rule; exclude PARTIAL; TWO C9 arms -> 42 fits) and corrected my Route-A provenance claim (the trainer STAYS in the sweep identity, because the new module imports `arm_loss` from it); approved `e1c8f77c` and `b538547e`** -> **my S89: all ten items KEPT UNCONTESTED after checking each against objects OUTSIDE the document (constructor map rebuilt, `code_identity()` read for cardinality, the approved ledger read for C9's two arms, `require_authorized_plan` read at source); THREE findings of my own - AA (limitation 136) the INTERACTION of Codex's edits 1 and 3 made the Step-4 authorization RE-USABLE, repaired with `run_label`; AB (limitation 137) the exact call site was still unwritten and the batcher `_stack` is PRIVATE; AC `anchor_sample_sd` was sourced without naming its field - both documents returned at `51c86f68` and `58276bb4`** -> **Codex S89 APPROVED the progress report at `58276bb4` (THAT LOOP IS CLOSED) and made TWO corrections to the design - AD, `run_label` cannot make a digest single-use because `--approved-plan-sha256` names a document and the same document can be resubmitted; AE, the S89 call-surface table was the complete PROJECT-DEFINED surface and not the complete Python one, since the control flow and the torch/numpy expressions are necessarily copied - approving `618d9ada`** -> **my S90: BOTH CORRECTIONS KEPT UNCONTESTED, each checked against an object outside the document (the loop re-enumerated at `dev_fit_trainer.py:942-995`, giving exactly Codex's six project-defined names; the trainer's `--output-dir` read at source and found to be a REQUIRED HOST PATH, which is what makes AD correct); ONE finding of my own - AF (limitation 138) the run root was never bound to anything, so the audit claim Codex wrote in the same session ("repeated use is recorded rather than silently presented as a new authorization") had NO MECHANISM behind it, two runs at one label writing into two unrelated directories; repaired by binding the run root to `<base>/<run_label>/` in C2 at zero cost to byte-determinism, which turns the audit claim into a refusal at a named exit, collapses §7.3's "fresh output root" into the new label, and narrows the residual to a different base or a copied workspace; C9's own precondition MEASURED (the width-parameterized constructor reproduces the approved net bit-identically at 32 channels, both C9 seeds); design returned at `b2f650e1`** -> **Codex S90 corrected the guard to an ATOMIC absent-root claim plus a sibling refusal sink; my S91 kept it uncontested and found the THIRD write location, C9's scratch root, bound to nothing - repaired as a reserved `_equivalence/` subtree, returned at `b45efa47`** -> **Codex S91 APPROVED THOSE EXACT BYTES: THE FIVE-ROUND DESIGN LOOP IS CLOSED AND v0.1 IS FROZEN, authorizing the executable and its tests and nothing else** -> **my S92 BUILT THEM - `scripts/utils/capacity_sweep.py` (`9f2cc0ab`) + `tests/test_capacity_sweep.py` (`d8a8c86c`, 189 tests), 1,740 packet tests green, zero fits/plans/checkpoints/rollouts; the first mutation harness was INVALID and its corrected replacement found five real coverage gaps, four of them in my own tests, all now closed at 36/36 with surviving negative controls** -> **Codex S92 BLOCKED both blobs on SIX findings (AI C9 partial state discarded, AJ terminals omitting unrun arms, AK C10 counting cardinality not identity, AL the refusal filename unbound from its payload uuid, AM the plan omitting both approved digests and two result names, AN C9 loading an approved checkpoint without authenticating its bytes) and repaired all six itself, approving `9059bccb`/`42e22a70`** -> **my S93 ACCEPTED ALL SIX DIAGNOSES AND IMPLEMENTATIONS after driving each adversarially, and found THREE MORE - AO invariant C1 enforced PER MODE not PER EXECUTABLE, so plan mode wrote into the protected tree (reproduced with a redirected packet root); AP the C9 checkpoint filename had TWO definitions with nothing comparing them; AQ a comment claiming an assertion the code does not make - all three repaired, 11/11 mutation with 3/3 controls surviving, returned at `9a1d11a7`/`2a043f99`, 1,753 packet tests green** -> **Codex S93 blocked on AR (a check/use split in my plan-mode guard); my S94 accepted it, found AS (the channels_NNN name had two copies) and repaired it anyway at gate 3's price; Codex S94 APPROVED MY S94 BYTES UNCHANGED, closing the four-round loop, and RAN plan mode -> my S95 audited the artifact 59/59 without importing the executable, reproduced it byte-identically to two scratch destinations, and found **AT** - `analyze_dev_fit.py` scores and loads every arm and is in none of the nine identities; three mutations MEASURED, two leaving the plan byte-identical and one surviving all 238 behavioural tests; I approved every check and WITHHELD the gate-closing approval, handing the ruling to Codex -> **Codex S95 RULED AT IN, implemented the sibling check (not a tenth entry, which collides with C3), and thereby SUPERSEDED its own plan artifact** -> **my S96 APPROVED `61d4fb97` UNCHANGED - the executable's loop is CLOSED - measured and DECLINED the analysis-vs-ledger sibling as a non-finding, and closed two mutation survivors (a deletable shape guard; an unpinned canonical-vs-raw domain whose failure mode is a fresh Windows clone) with TESTS ONLY, returning `8e97f6a9`** -> **Codex S96 APPROVED `8e97f6a9` UNCHANGED (the test loop CLOSED, and Route A with it) and RAN the one permitted zero-fit re-plan at `stage1-run-1`, approving the new artifact `c048b54b` / `bdf674d5…1c0a5`** -> **my S97: the plan AUDITED AS A SECOND INSTRUMENT - 94 checks with ZERO imports from `utils.capacity_sweep`; Codex's "exactly one field change" confirmed at FULL LEAF DEPTH (413 leaves each side, 1 changed, 0 added, 0 removed); finding AT's chain re-verified END TO END THROUGH THE PUBLISHED DOCUMENT; and two measurements its audit could not reach - section 7.1's BYTE-DETERMINISM RE-MEASURED against the post-AT-repair executable (3 destinations, 1 digest, `cmp`-identical) and the AUTHORIZATION GATE DRIVEN AGAINST TWENTY-ONE NEIGHBOURS rather than only the exact bytes (22/22, one accept, and a gate that accepted everything would have passed the exact-bytes check identically). Nothing wrong; TWO SCOPE STATEMENTS RECORDED RATHER THAN RAISED (the raw digest domain of the four delivered-data files; `role_index_sha256` as a declaration rather than a gate). **THOSE EXACT BYTES APPROVED - STEP 3 IS CLOSED** -> **my S98: BOTH Step-4 halves issued and THE SWEEP RAN — and died on its SECOND CURVE ARM after 31.3 s at `X_OUTPUT_DIRTY`, 3 of 42 fits spent, because `require_clean_capacity_point` ran once per ARM against a directory TEN ARMS SHARE. FINDING AU: the executable could never have completed a sweep under any plan. Repaired (once per point, above C9), three tests, failed root preserved as evidence, plan and both halves spent** -> **Codex S98 reproduced the mechanism from the preserved state, APPROVED the production repair unchanged, RULED FOR the above-C9 placement, and found the three returned tests could be fooled by `for point in [48]` — reviewer-edited one test to assert all four points once each in order, returning `6d49edde`** -> **my S99: the edit driven rather than read, via a TEN-CASE TWO-STATE mutation sweep run twice — Codex's gap confirmed and found to be THREE mutations wide (M1/M3/M4), the edit a strict improvement (+3 caught, −0 lost), the requirement-(z) worry about its derived expectation SETTLED BY MEASUREMENT (M6/M7/M10), and my own suite's one catch shown to be an accident of a fixture width (limitation 142). **BOTH BLOBS APPROVED UNCHANGED — THE EXECUTABLE LOOP IS CLOSED.** Then section 7.1 byte-determinism RE-MEASURED under the repaired module (3 scratch destinations, 1 digest) and **THE GATE-2 PLAN DIGEST PRE-REGISTERED BEFORE THE ARTIFACT EXISTS: `ffb00965…f9b7cb31`** -> **Codex S99 published exactly it; my S100 audited it in three parts (136 checks) and APPROVED THE EXACT BYTES, closing step 3, then issued my Step-4 half** -> **Codex S100 issued the second half and RAN THE SWEEP: `X_SWEEP_OK`, 42 fits / 42 checkpoints, both C9 arms PASS, ten anchors REUSED, 0 rollouts / 0 generation / 0 non-development reads, 439.6 s; it audited and approved the exact terminal bytes** -> **my S101: the independent section-12 step-5 exact-state review, 176 checks in three parts with every negative control firing, both suites green (217 / 1,768), and **THE SAME BYTES APPROVED — STEP 5 IS CLOSED AND THE SWEEP IS FINISHED AS A MEASUREMENT**; the section-5 descriptive read deliberately NOT computed, and a sufficiency check run in its place** -> **Codex S101 accepted my approval unchanged (step 5 closed on the same state) and BUILT C7 - `scripts/analyze_capacity_sweep.py` (`5dcc0947`) + `tests/test_capacity_sweep_analysis.py` (`5e4497fd`, 21 tests) - approving both exact states and handing them to me** -> **my S102: TWO findings, both repaired, three tests added, state returned at `b9043fa2`/`a81d35c9` with my explicit approval. **AV** - the reader compared EVERY arm's recomputed score to the record EXACTLY, but the ten REUSED anchors reach the record through `analyze_dev_fit.rounded()` at twelve decimals while the forty new arms carry the raw float; measured from the published artifacts alone by reconstructing each per-class F1's exact rational, 32 of 40 per-class values and 10 of 10 anchor macro-F1 values differ from their persisted rendering, so C7 **could not have completed the read it exists to perform** - the AU shape again - and I drove Codex's own function against one real anchor to watch it refuse; repaired by comparing in the domain the value was PERSISTED in, keeping exact equality for new arms and asserting BOTH directions for anchors. **AW** - a second `TemporalAttributionNet(..., enforce_rung1_band=True)` construction site in the one file invariant C5's AST test cannot see; repaired to `sweep.build_network`. Four-case two-state mutation sweep, 4/4 caught by the tests that name them, M1 being the handed-over behaviour itself; and a 13/13 sufficiency check that drove the whole authentication chain against the real state and STOPPED BEFORE the read** ** -> **Codex S102: the owner re-review, genuinely re-opening both findings - AV's provenance-specific comparison accepted over rounding both sides, AW's single construction site accepted, the three added tests read for non-degeneracy - and THE EXACT BYTES APPROVED. GATE 1 IS CLOSED.** -> **my S103: 39 pre-authorization checks (29 driving the reader's whole authentication chain against the real state and stopping before `derive_analysis`; 10 measuring the destination, including that a SECOND write refuses and the first artifact survives it), 241 + 1,792 suites green, and MY HALF OF THE C7 EXECUTION AUTHORIZATION ISSUED AS ITS OWN TURN - the exact command, all eight arguments, three input digests with the anchor analysis stated in FULL for the first time, the destination deliberately outside the sweep base, the budget, what it does NOT authorize, and five named residuals of which the first is that THE PRE-REGISTRATION IS WHAT IS SPENT, NOT THE BYTES** -> **all three of those gates then closed: Codex's matching half and the one C7 execution in its S103, the exact-state review in my S104, and section 5.4 applied jointly across both S104 turns. THE C7 LANE IS FULLY SPENT AND NOTHING ON IT IS OPEN.** *** THIS CHAIN ENDS AT S104; IT IS HISTORY, NOT POSITION. A `<- WE ARE HERE` marker sat at the S103 link and stayed there through THIRTEEN of my rewrites after the position had moved — caught in S117 only by grepping my own finished rewrite for the marker rather than reading for it. **A POSITION MARKER IS A STATUS CLAUSE AND ROTS LIKE ONE. There is exactly one authority on where the project is, and it is the head block at the top of this file.** *** -> **(rung-2 escalation, steps 1-5 — see the head block)** -> **NOTE: A2.3 RETIRED the replacement-assignment / full-regeneration leg of this path - Option C inserts nothing, so no seed ordinal moves; if the delivered set is ever superseded it is for some OTHER reason under its own authorization** -> (4 trainer + 5 calibration) [me] -> (2 remaining roles) [Codex] -> (6 controller + sample-size) [shared] -> **joint immutable freeze** -> one-shot confirmatory generation + eval (7) -> Phase 3.

Not freeze blockers (still required before completion): **Slot-8 verification artifact - the Step-1 design is FROZEN AND JOINTLY APPROVED, steps 2 and 3 are CLOSED AT BOTH APPROVALS, sub-step 4a (the connection-record design) IS CLOSED at blob `032db166`, and sub-step 4b-i IS CLOSED at both approvals (me S138, Codex S138). **Sub-step 4b-ii-a - read-order rows 4-12 - IS BUILT AND UNDER REVIEW (my S141, Round 1 handed off); sub-step 4b-ii-b IS NOT STARTED.** Sub-step 4b now closes on THREE cards - 4b-i + 4b-ii-a + 4b-ii-b - and sub-steps 4c-4f stay blocked on the authority-appropriate approved config, the capacity selection, the threshold calibration, the established result and the geometry-validation artifact (see the head block)**; Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## My lanes — current state

- **SLOT 8 - THE DIRECTOR'S VERIFICATION ARTIFACT. OPENED S123. STEPS 1, 2 AND 3 ARE CLOSED AT BOTH APPROVALS, AND SO ARE SUB-STEP 4a AND SUB-STEP 4b-i (Round-3 **Approved**, me S138 / Codex S138, same bytes). SUB-STEP 4b-ii-a - ROWS 4-12 - IS BUILT AND UNDER REVIEW (my S141); THE NEXT WORK ON THIS LANE IS 4b-ii-b, AND SUB-STEP 4b NOW CLOSES ON THREE CARDS.** Mine to write, Codex reviews. **The Step-1 design is `Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md`, blob `0753d4ed`, raw == canonical `98e20ae1...`, 59,495 B / 790 LF / 0 CR, LF-pinned by the packet `.gitattributes` `protocol/*.md` rule - jointly approved at those exact bytes (me S127, Codex S127); NEVER EDIT IT IN PLACE.** **READ THE FILE - this bullet is an index, not the document.** It is authoritative on: the `VerificationBundle`/`VerificationScene` field table and its **eight** load-bearing properties; the two mode-specific subcommand contracts; the section-4.1 non-finite float encoding and its `parse_constant` decode rule; the `draw_scene(scene, *, frame)` signature, the one scene-level `playback_t_s` clock, the causal at-or-before call-panel rule and the derived scripted frame; the three-state provenance machine and its **thirteen** exit-code rows; the fixture's required branches; the six acceptance tests A1-A6; **invariants V1-V19**; the four things the artifact must **say** it does not do; and the four-step sequencing. **IT AUTHORIZES NOTHING.** **Step 2 discharged it at `c12745ab`/`0ae5b19d`/`cf61e5aa`/`1833a472` (me S129, Codex S129) and step 3 closed at the ten fixture blobs + packet README `4bc07f18` + both `.gitattributes` + packet `.gitignore` + public README `3ab96e38` (me S130, Codex S130).** **STEP 4's OWN DESIGN IS `Reproducibility Packet/protocol/slot8-connection-record-v0.1.md` AT BLOB `032db166` - CLOSED AT BOTH APPROVALS (me S135, Codex S135), and it is the spec for everything the 4b build does. READ IT; the head block indexes it.** **The whole design review history - BR-BZ, CA/CB, CC/CD, CE/CF, CG/CH, CI-CL, CM, CN/CO on Step 1; CP/CQ/CR/CS + CT on the Step-2 build; and CU, CV, CW, CX, CY/CZ, DA, DB, DC, DD, DE on Step 4a - is SETTLED, and none of it is to be re-litigated.** Codex's D1-D4 rulings and Q1/Q2 are accepted without contest and are NOT to be reasked. **The current build state, the split, the three build decisions and the two forward items are in the head block.**

- **GATE-4 RUNG 2 — ALL SEVEN STEPS ARE CLOSED AND SECTION 5.4 IS JOINTLY APPLIED AND SPENT. THE RUN HAPPENED (Codex S117, `X_RUNG2_OK`, 12 fits / 12 checkpoints / 0 rollouts, 1,274.6 s), THE DESCRIPTIVE READ HAPPENED (me S119, `X_ANALYSIS_OK`, 0 fits, 11.97 s), BOTH AGENTS APPROVED THE DERIVED ARTIFACT (me S119 / Codex S119), AND THE TWO PRE-REGISTERED SENTENCES WERE APPLIED BY CODEX IN ITS S119 AND BY ME IN MY S120. NOTHING FURTHER IS LICENSED AND NOTHING SCIENTIFIC ON THIS LANE IS OPEN — only the packet-runbook documentation loop.** Mine to write, Codex reviews. Design `Reproducibility Packet/protocol/rung2-escalation-v0.1.md` at blob `404c9f1f`; module `scripts/utils/attribution_net_rung2.py` at blob `ca192af0` + `tests/test_attribution_net_rung2.py` at blob `c43d33b0` (71 tests; **superseded, never build from: `52809287`**); executable `scripts/utils/rung2_escalation.py` at blob `735f8dee` + `tests/test_rung2_escalation.py` at blob `7cefcb63` (142 tests) — **JOINTLY APPROVED, DO NOT REOPEN**; plan `results/rung2_escalation/plans/rung2-run-1/rung2_escalation_plan.json` at blob `61a2bd22`, canonical == raw `b51b0009…` — **JOINTLY APPROVED, DO NOT RE-AUDIT AND DO NOT REGENERATE**. **THE TWO RAW RUN ARTIFACTS ARE TRACKED AND MUST NOT BE REGENERATED:** `results/rung2_escalation/rung2-run-1/rung2_escalation_result.json` (blob `0eb78d0f`, raw `9d94b03e…`, 33,038 B) and `…/_equivalence/rung2_escalation_equivalence.json` (blob `351f47f4`, raw `ddcb5fed…`), plus twelve git-ignored `.pt` files — fourteen files exactly. Codex audited that raw state with its own instrument, 261 checks, all passed. **MY STEP-6 BUILD IS JOINTLY APPROVED AND CLOSED (Codex S118, no edit):** `Reproducibility Packet/scripts/analyze_rung2_escalation.py` blob `7cf3cc6a`, canonical == raw `83234943…`, 48,308 B / 1,125 lines; and `Reproducibility Packet/tests/test_rung2_escalation_analysis.py` blob `a642b3d3`, canonical == raw `169a3cb2…`, 54,947 B / 1,398 lines, **103 tests** (packet suite **2,108**). **THE PROJECT'S ONE OPEN LOOP IS NOW THE DERIVED ARTIFACT IT PRODUCED:** `Reproducibility Packet/results/rung2_escalation_analysis/rung2-run-1/rung2_escalation_analysis.json`, blob `a2fa857b`, raw == canonical `604d7272…`, 40,270 B, one line, tracked. I approved those exact bytes in my S119 turn after 165 independent checks and **Codex approved the same bytes in its S119 after its own 853-check standalone audit — THAT LOOP IS CLOSED, DO NOT REOPEN OR RE-AUDIT IT.** **DO NOT REGENERATE IT — the destination is an exclusive create and it is consumed, and both authorization halves are spent.** **THE LANE HAS NO REMAINING ITEM. `Reproducibility Packet/README.md` CLOSED AT BLOB `f5e677c8` (Steps 30 and 31 written my S120; Codex's BM repair its S120; my BN/BO/BP repairs my S121; Codex approved those exact bytes UNEDITED in its S121) - DO NOT REOPEN IT. The lane's account is now PUBLIC as well: the root README's running log carries the heartbeat, published in my S122 at blob `964231a4` and CLOSED at blob `f00ea0d9` after Codex's Finding-BQ scope correction (Codex S122, me S123) — DO NOT REOPEN IT.** See the head block for the nine required arguments, the derived-field list, the three flagged decisions, invariant R7's positive reading, and the M21 mutation survivor and its closure. **THE EXECUTION ROOT NOW EXISTS AND IS CONSUMED — a retry at `rung2-run-1` is impossible by construction, which is what R2 is for; a retry needs a new label, a new plan and a fresh joint authorization.** **A closed review loop authorizes the next step only, and never a run.**

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])`; **requires `record.n_steps <= W` and right-aligns (`estimator.py:366-375`) — it refuses a full run, so the caller owns the window origin**; `window_features(record)` → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `MIN_SYNC_SAMPLES=8`.
- **`synchronous_coefficient_vector(record, extractor)`** → **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** · `_SCORE_STD_FLOOR=1e-3` · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)`. **The learned ATTRIBUTION rung is now BUILT — see below. `RMALatentEncoder` remains specified-not-built.**
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
- **GATE-4 RUNG 1 — LOOP CLOSED, BOTH AGENTS APPROVED THE SAME BYTES (me S78, Codex S78). DO NOT REOPEN.** `scripts/utils/attribution_net.py` (`c4fa3c63`) + `tests/test_attribution_net.py` (`5a401ca1`, 68 tests). `TemporalAttributionNet` (39,594 params, 9 causal dilated blocks, receptive field 1,023) + `TemporalAttributionEstimator` (a `DiagnosisEstimator`) + `window_to_input` + `deterministic_conv_precision` + `CAPACITY_LADDER`. **No training loop, no fitted weights.** The estimator DEEP-COPIES the net it is handed (`nn.Module.to` moves in place — adopting it aliases two estimators onto one set of weights). `severity_uncertainty` is `+inf` even when fitted; the raw head scale is exposed only as `raw_severity_scale`. **`torch==2.11.0` is pinned in the packet's `requirements.txt` (blob `3b103c52`, ACCEPTED BY CODEX S77) — the FIRST new packet dependency since S45.** **`attach_trained_weights` is TRANSACTIONAL *and* IDENTITY-PRESERVING: it validates on a deep copy, then copies the validated tensors INTO the live network rather than rebinding `self.net`. Both properties are load-bearing and both were bought by a real defect (Codex found the first, I found the second inside its repair — limitation 108, lesson 102). The docstring carries the argument for why the second load cannot fail partway; do not delete it.**
- **THE DEV-FIT CONTRACT — LOOP CLOSED AT ROUND FOUR; BOTH AGENTS APPROVED THE SAME BYTES (Codex S80, me S81). DO NOT REOPEN.** `scripts/utils/dev_fit_contract.py` (`bd2c0d08`) + `tests/test_dev_fit_contract.py` (`fbd941b5`, 93 tests). The executable form of Codex's S77 bounds 1/3/4 — see the block at the top of this file. Imports neither `mujoco` nor `torch` (checked in a FRESH interpreter). **All four flagged design choices were RULED ON by Codex S78 and upheld.** **`require_code_identity` (S80) is the ONE statement of bound 4's code-identity rule; `code_identity()` and `DevFitProvenance.validate()` both call it and neither carries a copy — do not re-introduce a second copy.** `_HEX64`/`_DEV_HEX64` are UNANCHORED and safe only under `fullmatch`. Superseded, never review: `73e5e743`/`3959ff28` (mine S78), `6541cebc`/`9df7d7f7` (Codex S78), `2448ad4d`/`2aa5f762` (mine S79), `872c6b12`/`3125a618` (Codex S79), `9d6ecfea`/`d4202c8e` (mine S80). **`code_identity()` has TWO non-substitutable `require_bare_name` call sites — one early in the loop, one via the `require_code_identity` post-condition. Deleting either goes red (measured, S81). The rule itself still exists ONCE.**
- **THE DEV-FIT TRAINER — LOOP CLOSED, BOTH AGENTS APPROVED THE SAME BYTES (Codex S83, me S84). IT HAS RUN ONCE.** `scripts/utils/dev_fit_trainer.py` (`caa00418`) + `tests/test_dev_fit_trainer.py` (`cbc4064f`, 49 tests). **Do not reopen the loop; do NOT re-run `--mode fit` into `results/dev_fit` — the guard refuses it and rightly so. A second fit needs a NEW output directory and a reason.** See the blocks at the top of this file for the approved window policy, Codex's four preserved S82 corrections, and my Findings S and T; **do not redesign it.** Superseded, never review: `275a7a50`/`80d9722f` (mine S81), `fd2c8c9b`/`9d9455b7` (Codex S81), `10054696`/`9e76923c` (mine S82), `788fc240`/`c95bd8fb` (Codex S82), `b9d7bb6f`/`3a81eecc` (mine S83). **10 fits, 10 checkpoints, 0 rollouts.** **THE FIRST DEVELOPMENT FIT RESULT is `results/dev_fit/dev_fit_result.json` (tracked) + ten git-ignored `.pt` files — see the head of this file.** **THE WINDOW POLICY ITSELF IS SETTLED — Codex approved it in its S82 and that is not part of this loop.**
- **THE DEV-FIT IN-SAMPLE READBACK — CODEX OWNS IT, I AM THE REVIEWER. ALL THREE PARTS ARE NOW JOINTLY APPROVED AND CLOSED.** `scripts/analyze_dev_fit.py` (`31381b18`) and `results/dev_fit/dev_fit_analysis.json` (`0d00b5ca`, canonical `7bec34a1`) are **JOINTLY APPROVED (me S85, Codex S85) — DO NOT REOPEN.** `tests/test_dev_fit_analysis.py` is **CLOSED at `6f29bf05`, 35 collected — Codex approved it in its S87 and I gave the explicit owner approval in my S88, so both approvals name the same bytes. DO NOT REOPEN.** Codex built the readback in its S84 to carry Finding X forward without rewriting the ledger; my S85 review kept every published number and made four repairs (loss decomposition bound to `trainer.arm_loss`, plan cardinality and seed set derived from the contract, two unsupported docstring claims corrected, a producer binding added); Codex's S85 approved all of that unchanged, rejected my no-refactor-possible premise, and added five tests through the loader/evaluator seams; **my S86 measured what those tests actually catch (10 of 14) and repaired three degenerate fixtures to reach 14 of 14, changing no production code and no number.** **Superseded, never review: `cef8c35a`/`9837499e`/`d61edd33` (Codex S84), `f97c359b` (mine S85), `850d0fe3` (Codex S85), `c7b0a093` (mine S86), `4481ba32` (Codex S86 - I CONTESTED it in S87; see limitation 133).** **Limitation 130 is now a CORRECTION, not a limitation — the derivation path IS coverable through those seams and my S85 claim to the contrary was false.**
- **C7, THE READ-ONLY CAPACITY-SWEEP ANALYSIS - CODEX OWNS IT, I AM THE REVIEWER, AND THE CODE/TEST LOOP IS JOINTLY CLOSED AT `b9043fa2`/`a81d35c9` (me S102, Codex S102).** `Reproducibility Packet/scripts/analyze_capacity_sweep.py` + `tests/test_capacity_sweep_analysis.py`. Codex built and approved `5dcc0947`/`5e4497fd` in its S101; my S102 found AV and AW, repaired both, added three tests and returned the current state with my explicit approval; **Codex's S102 re-opened both findings, accepted the diagnoses AND the implementations, and approved those exact bytes.** See the AV/AW block and the "WHAT C7 IS" block at the head of this file. **GATE 2 IS SPENT: both halves were issued (me S103, Codex S103) and Codex ran the one authorized invocation in its S103.** Its terminal artifact is jointly approved (Codex S103 owner, me S104 reviewer after a 73-check independent audit). **DO NOT RE-RUN IT AND DO NOT REGENERATE THE ARTIFACT - the destination is an exclusive create and it is consumed.** **NOTHING IS OPEN ON THIS LANE.** Both section-5.4 halves are paid — mine in the transcript at S104, Codex's in its own S104 — so the joint application is complete. *(This sentence claimed Codex's half was outstanding through three of my rewrites after it had been paid; corrected S108. Lesson 65.)*
- **THE STAGE-1 CAPACITY SWEEP - THE MEASUREMENT IS FINISHED. `stage1-run-2` completed 42/42 in Codex's S100 and both agents approved the exact terminal bytes (Codex S100, me S101). SECTION-12 STEP 5 IS CLOSED. The history below is S98's and its status clauses are superseded.** IT RAN IN MY S98 AND FAILED AT ARM TWO (finding AU). **[S98 STATUS, LONG SUPERSEDED — the executable/test loop CLOSED in my S99 and NOTHING ON THIS LANE IS OPEN; see the Pointers entry below for the approved pair]** the executable and its tests were then open on Codex at `53e5dcb7`/`2dc93297`; the S95/S96 jointly-approved pair `61d4fb97`/`8e97f6a9` is SUPERSEDED, and so is the S97-approved plan `c048b54b`/`bdf674d5...`. Both Step-4 authorization halves are spent. 3 fits, 3 checkpoints, 0 rollouts; C9 PASSED; the failed run root is PRESERVED EVIDENCE.** See the head of this file for the full state, the AT repair, the non-finding I declined, and the S96 mutation sweep. `scripts/utils/capacity_sweep.py` + `tests/test_capacity_sweep.py`, authorized by the frozen `protocol/capacity-escalation-v0.1.md`. **Zero fits, zero checkpoints, zero rollouts.** The C7 read-only analysis script is the next separate build, after the re-plan.
- **THE PAYLOAD-CONDITIONING READ — RESULT JOINTLY APPROVED, CODE UNDER REVIEW.** `results/protocol_p/payload_conditioning.json` (`c11f7067`, canonical sha256 `47ec3571…`) is **jointly approved** (Codex S60, me S61) and my S61 edits regenerate it byte-identically. `scripts/analyze_protocol_p_payload_conditioning.py` (`39048d26`) + `tests/test_protocol_p_payload_conditioning.py` (`b9e81f63`, 105) are **under review at my S61 blobs**. **Not pre-registered; the artifact's second key is an `authority` field saying so and a test asserts that string.** Same post-A2 revision obligation as the role-coverage read.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** (`utils/rng.py:76-78`). **Measured S39: a `pair_id` change alone moves `gauge_obs` by up to 6.50 µε**, against `D` of order 0.1–0.5. **Nothing else is in the key.**
- Deployable floors are *detection*, not learned attribution; abstention untestable on this fault library; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path, the operation, the construction, the identity, the fault's activation step, and — S60 — the CONTEXT POPULATION, of which payload mass is the dominant factor. The SIGNAL it is compared against depends on excitation, task, plant and payload.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**. **S77 added the FIRST new PACKET dependency since the packet was created: `torch==2.11.0` in `Reproducibility Packet/requirements.txt`, pinned as the BASE version (not `+cu128`) so a reader without a CUDA machine can still run the whole suite.** The venv itself gained nothing — torch was already installed.
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** - a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. *** THE FULL-SUITE FIGURE IS **2,608** (Codex S138, 203.27 s, 0 failed, 0 collection errors) - it was 2,267, the S136 4b-i build added 212, the S137 Round-2 repairs added 99 and the S138 Round-3 repairs added 30. S139 DID NOT RE-RUN IT - no executable file changed.  It is CLEAN: the Smart App Control block that made S128 and S129 unmeasurable is OVER - see the head block and `director_requests.md` entry 2. **DO NOT QUOTE 1,328 OR 1,344; THEY ARE ARTIFACTS OF A BROKEN ENVIRONMENT.** *** The two Slot-8 files run **159 passed in 31.70 s**, and 159 again under `python -O`. Earlier clean history: 2,479 (S136, 192.86 s), 2,267 (S130, 221.38 s; S131, 204.35 s), 2,108 (S118, 126.88 s), 2,005 (S115-S117), 1,863 (S114), 1,861 (S113), 1,792 (S102), 1,753 (S93), 1,551 (S85-S90), 1,370 (S77), 1,306 (S72), 595 (pre-S51 baseline). *** MY S115 REPORT SAID 2,004 AND THAT WAS A TYPO IN MY OWN ARITHMETIC: 1,863 + 142 = 2,005; Codex corrected it forward and I MEASURED the correction in S116 rather than conceding it. *** `test_payload_boundary_extension.py` collects **170**; the two closed Step-2 seam files together collect 124; `test_dev_fit_analysis.py` collects 35; **`test_connection_record.py` collects 341** at the approved Round-3 state (S138, 7.42 s, and 341 again under `python -O`; it was 212 at the S136 Round-1 state and 311 at the S137 Round-2 state). **Set `PYTHONIOENCODING=utf-8` for anything that prints non-ASCII** - the console is cp1252. **Use ASCII in probe scripts and in anything a gate prints.** **Set `MPLBACKEND=Agg` for anything that renders a figure outside pytest** - the Slot-8 test files call `matplotlib.use('Agg')` at import, but a bare probe script or the fixture CLI will pick up the interactive backend, and the CLI's fixture mode ends by opening the menu.
- **MUTATION SWEEPS — MANDATORY HARNESS SHAPE AFTER S60:** clear `__pycache__` before every run **and** set `PYTHONDONTWRITEBYTECODE=1` in the subprocess env; drop `-x`; translate anchors to the target file's own newline; report bad anchors separately from survivors; restore exact bytes in a `finally` and verify the blob afterwards. **Run the whole sweep twice and require identical results** — that is the cheapest detector for a harness fault.
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`. **BUT A MODULE UNDER `scripts/utils/` IS NOT A PACKET SCRIPT AND THIS DOES NOT APPLY TO IT — MEASURED S95.** There is no `utils` package at the packet root and no `scripts/__init__.py`, so from the packet dir `-m utils.<mod>` and `-m scripts.utils.<mod>` both raise `ModuleNotFoundError` and running the file by path fails on its relative import. **Run it from `Reproducibility Packet/scripts/`: `..\..\venv\Scripts\python.exe -B -m utils.<mod> … --output-dir ..\results\<name>`.** **In my PowerShell tool the working directory is not the repo root — use `Set-Location` or absolute paths. My Bash tool's cwd PERSISTS between calls — prefer absolute paths or re-`cd` every time.**
- **Timings (measured S35–S60):** full packet suite ~150 s; one MuJoCo rollout (3000 steps) **25.6–27.5 s**; a PARTIAL rollout is proportionally cheap — 480 steps ≈ 3.0 s; at reduced fidelity (`point_count=9`, `simulation_timestep_s=2e-4`) 501 control steps ≈ 0.37 s; a 200-realization sensor-only null at W=768 ~40 s; an offline re-observation ≈ instantaneous; the driver's `--mode plan` 0.30–0.33 s; **the payload-extension executable's `--mode plan` 0.36–0.38 s (eight MuJoCo model compilations, zero steps)**; **one driver-file mutation case ≈ 100 s** (a 17-case sweep is ~28 min and belongs in the background); **a small-analyzer mutation case ≈ 0.5–0.7 s with the fixed harness, so a 44-case sweep is under a minute.** **NO figure exists for the pinned `pairs=100` Stage-0 run — see limitation 45; do not invent one.**
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — use `flush=True` in the job and poll the file it writes, not a pipe.**
- **PowerShell 5.1** primary (no ternary/`??`; **`^` is not a continuation**); Bash tool also available. **`bc` and `/usr/bin/time` do NOT exist in the Bash tool** — time a subprocess from Python with `time.perf_counter()`. Use `git diff --numstat` to confirm `+N/−0` after every chat turn. **A bash heredoc (`<<'PY'`) is the reliable way to run a multi-line Python script from the Bash tool; inline `-c` with `chr()`/byte literals is where I make syntax errors.**
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise, and the three session locks (`.claude-session.lock`, `.codex-session.lock`, **`.agent-session.lock`** — the scheduled-task runner creates the last one at the repo root). **Root `.gitattributes`** pins `schema.json`, the assignment JSON, and **`Reproducibility?Packet/protocol/*.md`** to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked). **S130 ADDED TWO THINGS, BOTH MEASURED: `results/verification_fixture/*.sha256 text eol=lf` in BOTH `.gitattributes` files (a fresh Windows checkout renders that 65-byte digest file at 66 B with one CRLF; the canonical JSONs carry no newline and the PNGs round-trip as binary, so neither is pinned), and `/results/verification_fixture_reproduced/` in the packet `.gitignore` beside the other runbook reproduction outputs. Verified again S61 and S130; no other change needed. The scheduled-task runner's `.agent-session.lock` is ignored and must be deleted at session end.**

## Pointers

- **C7, THE READ-ONLY ANALYSIS - CODE/TEST LOOP CLOSED (me S102, Codex S102), ONE EXECUTION SPENT (Codex S103), TERMINAL ARTIFACT JOINTLY APPROVED (Codex S103, me S104). NOTHING HERE IS OPEN AT ALL — Codex paid its section-5.4 half in its S104 and mine was in the transcript at S104, so the joint application is COMPLETE.** *(This clause said "NOTHING HERE IS OPEN EXCEPT CODEX'S 5.4 HALF" through my S105, S106 and S107 rewrites after that half had already been paid — lesson 65 again, and caught in S108 by grepping the file rather than reading it. **A status clause about ANOTHER agent's obligation is the most likely one to rot, because nothing in my own work forces me to revisit it.**)* **The files:** `Reproducibility Packet/scripts/analyze_capacity_sweep.py` blob `b9043fa266dc7c35a6acdb240216ae0ec3337f6e` / canonical == raw `7eca4016d7ffb73c15ec1e35642e5f6e1ecb95a7c6757e72cc875cf79f87ffbe`, 44,600 B / 1,088 lines; and `Reproducibility Packet/tests/test_capacity_sweep_analysis.py` blob `a81d35c952fba158f647a64b9cd13bad0c301c93` / canonical == raw `bd8c36316b4be433cac0000ef2597137cb35b68b0f5407c7b992764d9976d229`, 29,957 B / 805 lines, **24 tests**. Both LF, pure ASCII, no BOM, final newline. Suites re-run green at this state in S104: **241 focused, 1,792 packet.** Codex built and approved `5dcc0947`/`5e4497fd` (21 tests) in its S101; I found **AV** and **AW**, repaired both, added three tests and returned the state above with my explicit approval in my S102; Codex approved those exact bytes in its S102 after genuinely re-opening both findings. **Superseded, never review or build from: `5dcc0947`/`5e4497fd`.** **DO NOT RE-RUN C7 AND DO NOT REGENERATE ITS ARTIFACT - the destination is an exclusive create and it is consumed.** The next thing to touch this pair is a NEW finding, not a re-review. Read the head block at the top of this file and the "WHAT C7 IS" block at the head of this file before anything else; this bullet is an index.
- **THE STAGE-1 EXECUTABLE AND ITS TESTS - JOINTLY APPROVED S99, LOOP CLOSED, DO NOT REOPEN:** `Reproducibility Packet/scripts/utils/capacity_sweep.py` blob `53e5dcb7` / canonical `be07d95e4b4b9fa1a8934a165681fdbc9e7e885236bd1de3c38b661288f641fa`, and `Reproducibility Packet/tests/test_capacity_sweep.py` blob `6d49edde` / canonical `640f23b5990d9fc9f17fe0eeb39bbf9192abaa26ab1726653d9df9942c1747d3`, **217 focused tests, 1,768 full packet suite, both re-run green in S99 (also under `python -O`).** Codex approved the pair in its S98; I approved the same pair unchanged in my S99 after the ten-case two-state sweep. **The next thing to touch this pair is a NEW finding, not a re-review.**
- **THE CAPACITY-ESCALATION DESIGN - FROZEN AND JOINTLY APPROVED, DO NOT REOPEN: `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`, blob `b45efa47`, canonical/raw sha256 `05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002`, 72,630 B / 1,084 lines / LF / raw == canonical / no BOM.** Codex approved these exact bytes in its S91 and I had already approved them, so both approvals name the same state. **FIVE ROUNDS.** *(This bullet said "round four, blob `b2f650e1`, authorizes nothing" through my S92 and S93 while the head block said FROZEN the whole time - my own summary contradicting itself, which is lesson 65 exactly, caught in S93 by grepping the file rather than reading it. Same failure as the S64 progress-report status line. **A status clause that has been true for several consecutive rewrites is the most likely thing to be carried into one where it is false.**)* **Superseded, NEVER review or build from: `b2f650e1` (mine S90), `b359ba0b` (Codex S90), `51c86f68` (mine S89), `618d9ada` (Codex S89 — SUPERSEDED BUT NOT REJECTED; both its corrections AD and AE are preserved in the frozen state, uncontested), `ccd12ef4` (mine S88), `e1c8f77c` (Codex S88 — likewise preserved), `b86d46aa` (mine S87, which Codex BLOCKED).** **IT IS STILL NAMED v0.1 AND THAT IS NOW PERMANENT: a correction bumps the version and `git mv`s, and MUST move `DESIGN_CANONICAL_SHA256` in `capacity_sweep.py` with it. Editing v0.1 in place turns plan mode RED.** **WHAT THE FREEZE AUTHORIZED, AND ONLY THIS: writing the executable and its tests.** **READ THE FILE - this block is an index, not the document.** Settled and NOT to be re-derived: **no Claim Sheet amendment is needed** (Slot 9 (b) IS limitation 127 restated, and Slot 14 already contracts "the within-suite capacity sweep"); **width and not depth**, because `n_blocks` moves the receptive field too; **the ten approved 32-channel arms are REUSED, never re-fitted as curve arms, and carry status `REUSED` rather than `COMPLETED`**; **every point stays inside Slot 9's rung-1 band**, so `enforce_rung1_band` stays ON and Stage 1 does not climb the ladder; **the executable emits NO VERDICT AT ALL**, with the interpretation pre-registered as prose in §5.4, applied jointly, and **no observation licensing any action**, Stage 2 included; **the absolute per-suite curves are first-class outputs**; **`{16, 24, 32, 40, 48}`, 50 arms, 40 new**; **§4.3 states the seed claim as three claims with three scopes** (suite pairing IS real CRN at fixed `(c,k)`; row order IS common across widths; initialization is NOT); **§2.1 reconciles Slot 14 with bound 5** — development-only instrument diagnosis and capacity-search history, never held-out evidence, a headline result, or a capacity selection. **RULED BY CODEX S88 AND CLOSED: Route A** (new module `scripts/utils/capacity_sweep.py`; `dev_fit_trainer.py` NOT edited; because the module imports `arm_loss` from it, **the trainer STAYS in the sweep's code identity** — all eight historical entries match exactly and the new module is a **ninth**); **one derived label, made post-anchor**; **6-dp `ROUND_HALF_EVEN` as a numerical tie rule carrying no inferential meaning**; **`PARTIAL` points excluded from the eligible subsequence**; **TWO C9 arms, `(C1,0)` and `(S,4)` → 42 fits / 42 checkpoints, not 41**. **The load-bearing invariants are C9 (the two-arm equivalence gate, limitation 134), C10 (no partial run may present itself as a curve), the `run_label` field (S89, limitation 136), and — new at S90 — C2's binding of the run root to `<base>/<run_label>/` (limitation 138), which is what gives the audit claim and the fresh-root rule a mechanism.** **`run_label` does NOT make an authorization mechanically single-use — Codex's AD, accepted; the residual is a different base directory or a copied workspace, and §7.1 states it at that width.** **§7.3: a retry is a SECOND execution and needs a SECOND joint authorization at a new `run_label`.** **§4.4 carries the exact call site of the copied loop (limitation 137) — read it before writing one line of the executable — and its table is the complete PROJECT-DEFINED surface (six names), not the complete Python call surface; the control flow and the torch/numpy expressions are copied, and C9 is the backstop over the whole seam.** **C9's own precondition is MEASURED (S90): the width-parameterized constructor reproduces the approved net bit-identically at 32 channels, both C9 seeds.**
- **THE STEP-3 PLAN ARTIFACT - JOINTLY APPROVED IN S97 AND *SUPERSEDED* IN S98 BY THE FINDING-AU REPAIR. IT IS NOT RUNNABLE AND ITS TWO AUTHORIZATION HALVES ARE SPENT. DO NOT RE-AUDIT IT, DO NOT APPROVE IT, DO NOT DELETE IT - it is the state the AU run consumed, and the run artifact names its digest. A regeneration goes to a NEW LABEL and a NEW FILE.** `Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json`, blob `c048b54b8081271d76a6adacf8526d201c446c17`, canonical == raw `bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5`, **13,786 B**, one canonical JSON record, pure ASCII, **no CR and no LF at all**, no BOM, no terminal newline, and re-emitting the parsed document under `sort_keys` + `(",",":")` + `ensure_ascii=False` + `allow_nan=False` reproduces it **byte for byte**. Thirty top-level keys; 10 read-only anchors + 40 new arms + 2 C9 arms; 44 declared output paths all under `results/capacity_sweep/stage1-run-1/`; budget 42/42/0/0/0; nine code identities; `training_protocol` IDENTICAL to the approved ledger's including the two-entry `window_schedule`. **Run and approved by Codex S96; approved unchanged by me S97 after a 94-check independent audit, a full-leaf-depth diff, a 3-destination determinism measurement and a 22-case gate-neighbour sweep.** **SUPERSEDED, DO NOT APPROVE, DO NOT RE-AUDIT, DO NOT DELETE:** blob `d2584d28`, canonical == raw `740d5db96657c7a5e9a86b49816daf091439e7661a6bd971fb8ce6ab3ae1c00e` — owner-approved by Codex S94 and audited 59/59 by me S95, then invalidated when the AT repair moved the sweep's digest; `require_authorized_plan` refuses it with *"the authorized plan was written by a different code state"*, which I re-drove in S97. It is kept unregenerated as the visible state that produced AT. **DO NOT run `--mode execute` AGAINST THIS SPENT PLAN AT ALL.** *(Status of the LIVE plan and its authorization, updated S100: the runnable plan is `results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json`, blob `d7104e55`, canonical `ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31`, 13,786 B — **jointly approved, Codex S99 and me S100, gate 2 CLOSED**. **BOTH Step-4 halves were then issued (mine S100, Codex's S100) AND ARE NOW SPENT: Codex ran the one authorized execution in its S100 and the sweep completed, `X_SWEEP_OK`, 42/42.** This plan is therefore CONSUMED as well; do not re-audit it, do not delete it, and do not point `--approved-plan` at it again. See the head block at the top of this file at the top of this file, which is the authority on gate state — this bullet is an index.)*
- **Protocol P (in force, JOINTLY APPROVED): `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`, canonical sha256 `5689dad7…8bdf421f`. READ THE FILE.**
- **The payload-boundary extension — JOINTLY APPROVED AND FROZEN, NOT YET EXECUTABLE: `Reproducibility Packet/protocol/payload-boundary-extension-v0.2.md`, canonical sha256 `538ae06b…df33b6a`, blob `d9f6e188`, 71,188 bytes, 1,285 lines, LF, raw == canonical.** Approved by me S63 and by Codex S63; **DO NOT EDIT IT — a change needs a version bump and a `git mv`.** It authorizes **Step 2 only**: build and review the three prerequisites. READ THE FILE — the blocks above are an index, not the document. Superseded states, never cite or build from them: v0.1 (`32a03930…`, blob `903962f8`, bytes in `Claude Session 61`), and inside v0.2 `c7facc13`/`e734c498…` (my S62 handoff) and `3d72e1f4`/`e5192eaa…` (Codex's S62 edits, which I did not approve).
- **THE PAYLOAD-BOUNDARY EXTENSION IS FULLY SPENT AND CLOSED. NOTHING HERE IS OPEN.** All three Step-2 prerequisites jointly approved (S71); Step 3 run and its plan approved by BOTH agents (me S72, Codex S72); Step 4 authorized by both halves (me S73, Codex S73); **STEP 5 RAN ONCE - Codex S73, 127 physical rollouts, `X_CASE_EMPTY` - and its result artifact is JOINTLY APPROVED (Codex S73, me S74 after 130 checks).** The measurement is spent; no further execution is authorized. *(This bullet and the block below both said "CODEX OWES THE SECOND READ" through every rewrite from S73 to S95, while the Order line six sections up said Codex completed that read in its S72 and that Step 5 had run. My own summary contradicting itself for twenty-three sessions: lesson 65 again, and caught in S96 only by grepping the file rather than reading it. **A status clause about ANOTHER agent's obligation is the most likely one to rot, because nothing in my own work forces me to revisit it.**)*
```text
THE STEP-3 ARTIFACT - JOINTLY APPROVED (me S72, Codex S72).  CLOSED:
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
STEP 2 CLOSED S71.  STEP 3 RUN AND JOINTLY APPROVED S72.  STEP 4 AUTHORIZED S73.
STEP 5 RAN ONCE, Codex S73: 127 rollouts, X_CASE_EMPTY, result JOINTLY APPROVED.
```
- **THE GATE-4 DEV-FIT ARTIFACTS — the project's first learned-model numbers.**
```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json     THE LEDGER, owner-approved
  canonical == raw sha256  f18c98b2...   blob d4cefb61   33,193 B   NO NEWLINES AT ALL
  Ten git-ignored dev_fit_{C1,S}_seed{0..4}.pt beside it; this document is their SOLE
  provenance record (limitation 122/128).  DO NOT MOVE, REGENERATE OR OVERWRITE IT.
Reproducibility Packet/results/dev_fit/dev_fit_analysis.json   THE READBACK, NOW JOINTLY
  APPROVED (me S85, Codex S85) -- CLOSED, do not regenerate to a different state.
  canonical sha256  7bec34a1...   blob 0d00b5ca   14,165 B / 426 LF in my working tree
  *** A FRESH CHECKOUT RENDERS 14,591 B / 426 CRLF AND A DIFFERENT RAW DIGEST.  QUOTE THE
      CANONICAL ONE.  Limitation 129. ***
  Regenerate it (overwrites in place, deterministic, ~4.2 s, ZERO fits/rollouts) with the
  Step-27 invocation in the packet README.  A review probe may point --output-dir at a
  scratch dir and diff the bytes.
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
- Director requests: `director_requests.md` (root) — **entry 1** (Claim Sheet review) non-blocking, **still awaiting director reply**. **ENTRY 2 (the MuJoCo / Application Control block, logged by me S128) IS RESOLVED** — a director-authorized **Repair Agent** appended the root-cause diagnosis and the standing procedure on 2026-08-13 17:19 PDT, and Codex committed that append in its S129. *** THE ENTRY IS APPEND-ONLY AND THE `*Awaiting director reply.*` line above the Repair Agent’s note IS SUPERSEDED BUT LEFT STANDING. DO NOT EDIT IT. *** **A FUTURE NATIVE-IMPORT INCIDENT GETS A NEW NUMBERED ENTRY with the diagnostic’s output — Randy is deciding Smart App Control policy from the pattern of incidents, so a silently absorbed one is invisible to him; and do NOT propose turning SAC off.** Nothing else is blocked on the director.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S60 entries — reproduction/construction/measurement/review sessions, no external sources read**).
- **Live-Run README (co-maintained): root `README.md` - Phase 2 / In Progress, banner **2026-08-15**, blob `11a424b7` (154,471 B / 220 LF / 0 CR), raw `f3d1dd86...`. **CLOSED AND JOINTLY APPROVED - Codex S139, me S140, same bytes; terminal outcome Approved with Follow-ups. DO NOT REOPEN IT.** The Step-4b-i heartbeat Codex published in its S138 stands BYTE-IDENTICAL; my S139 blocking finding was repaired by an APPENDED dated correction (2026-08-15) plus the banner date, `+3/-1` in two hunks, and the unchanged regions were proved by reconstructing the predecessor byte for byte. *** THE SCOPE PRECEDENT: THE BANNER `Last updated` LINE IS IN SCOPE whenever an append makes it stale - the playbook requires the banner be current, so refusing it leaves the candidate in violation of its own playbook. *** *** AND THE LESSON: A DELETION FROM A PUBLISHED LOG IS A REWRITE OF HISTORY, however small. Codex's append-only repair was right and I withdrew mine. Lesson 237. *** **S140 APPENDED NO NEW ENTRY and that was the correct heartbeat outcome** - no artifact finished, no phase closed, and an internal review-process rule is not something a stranger would care about. THE HISTORICAL NOTE BELOW IS PRESERVED:** *** CORRECTED S137: this bullet said blob `3ab96e38` / banner 2026-08-13 after CODEX MOVED THE FILE IN ITS S135 - `git diff 40a212f 7818d96 -- README.md` is `3ab96e3..7a47907`, a `+4/-2` that bumps the banner date and appends ONE two-sentence dated entry saying the Step-4a design is approved by both agents and authorizes only the next synthetic build. I READ IT IN MY S137 GENERAL RECENT-WORK REVIEW: it is accurate, it IS the lean shape the playbook asks for, and I have NO correction to carry, so no cycle is open on it. Lesson 65 again - and again the stale clause was about ANOTHER AGENT'S change to a file I index. *** **The S130 loop closed at `3ab96e38` - Codex approved that exact blob unedited in its S130 - and that closure is history, not current state.** *(It had previously been CLOSED at blob `f00ea0d9`, Codex S122 reviewer and me S123 owner; I reopened it deliberately in S130 by publishing the heartbeat Step-2 closure earned, and it closed again in the same round.)* **CODEX'S FORWARD-ONLY PROCESS NOTE, ACCEPTED WITHOUT ARGUMENT: at 495 words / 12 sentences my S130 entry is NOT the lean one-or-two-sentence shape the playbook names. THE PUBLISHED ENTRY IS NOT REWRITTEN; FUTURE HEARTBEATS RETURN TO THE LEAN FORM.** **S131 RAISED THE STALE-SENTENCE QUESTION IN CHAT AND CODEX RULED IN ITS S131: NO SUCCESSOR ENTRY. The dated log is historical, the banner is current, and Step-3 review closure does not warrant duplicating the already-logged surface milestone; the stale-forward-sentence rule is outweighed here by the log's dated-history and lean-milestone rules. I ACCEPTED THAT RULING IN MY S132 AND THE QUESTION IS SETTLED - DO NOT RAISE IT AGAIN. S132 RAN THE CHECK AND APPENDED NOTHING: no artifact was finished, no phase closed, and a design inside an OPEN REVIEW ROUND is none of the three triggers.** My S130 append is `+3/-1`: ONE new log entry, and the `-1` is the banner `Last updated` line the playbook requires be kept current - **NO LOG ENTRY WAS REWRITTEN, and do not raise that `-1` as a log rewrite.** The entry leads with the verification surface existing and with it being CONNECTED TO NOTHING, names the three absent inputs, says every number on the screen was fabricated, describes the fixture's measured refusal to flatter the structural suite, and states that the figure set and runbook step are WITH CODEX FOR REVIEW rather than approved. **S123 THROUGH S129 EACH RAN THE CHECK AND CORRECTLY APPENDED NOTHING** - Codex ruled in its S127 that the lean public milestone is the **REVIEWED WORKING** Slot-8 surface, not the design closing and not an unreviewed build, and that condition was met in S129. *** THE DEFERRAL WAS AN INSTRUMENT, NOT A DELAY, AND IT WORKED: six sessions each ran the check, each declined for a stated reason, and the condition was written down - so the session that published did not have to reconstruct why it had been waiting. USE THAT SHAPE AGAIN. *** *** THE MEASUREMENT RULE ON THIS FILE BINDS BOTH AGENTS: PUBLISH THE FILTERED BLOB. `core.autocrlf=true` and no `.gitattributes` pin, so the working tree is CRLF and `git hash-object --no-filters` gives a THIRD value that is nobody's identity. EVERY TRACKED README BLOB HAS ZERO CR. *** I re-read the playbook in full before publishing, as in every session where the append answer was NO (105-108, 113, 115-118, 121, 123-129). **The standing rules on this file are unchanged: an entry earns its place only if a stranger would care; a program still inside an open review round is none of the three triggers; and an entry that leaves an earlier entry's forward-looking sentence standing after it goes stale is a defect, corrected by appending a dated successor and NEVER by editing the entry that went stale.** **The open debt is unchanged and now belongs to the Technical Report:** the entry reporting the capacity read's result never tells the reader that the reader-script as first written could not have read the finished sweep at all.
- **CHATS - WHERE REVIEW NOW HAPPENS.** *** THE `Phase 2 Integration and Config Freeze` CHAT IS CONCLUDED at the director's instruction (Codex S134): "all of Phase 2" is not a bounded subject. IT RECEIVES NO FURTHER WORK. Final state 2,296,416 physical bytes, sha256 `06508a94430ea91f59037a004cfc74773be3959a97fe131ec894d2a2742bf388`; its `Summary.md` carries the load-bearing state at conclusion. DO NOT APPEND TO IT. *** **The `Slot-8 Step-4a Connection-Record Design` chat is ALSO CONCLUDED** (Codex S135, on approval) with its own `Summary.md`. **THE `Slot-8 Step-4b-i Connection-Record Contract` CHAT IS ALSO CONCLUDED** (Round-3 **Approved**, me S138 / Codex S138 at the same bytes) with its own `Summary.md`; it receives no further work. **THERE IS NO OPEN OWNER-REVIEWER REVIEW AT ALL AS OF MY S140.** The public README heartbeat card CLOSED at Round 2 (**Approved with Follow-ups**, Codex S139 / me S140, blob `11a424b7`) and the convergence-method chat reached consensus and the rule is written into `Playbooks/review-cycle.md` and `Review Card/README.md`. **BOTH OF THOSE CHATS ARE STILL NAMED `- Active.md` ONLY BECAUSE NEITHER AGENT HAS RENAMED THEM YET** - I offered to conclude both and said either agent may; if Codex has not, conclude them with `Summary.md` files and move on. **THE NEXT CHAT TO EXIST IS THE 4b-ii SUBJECT CHAT, WHICH I OPEN WHEN I HAND OFF THAT BUILD - WRITE ITS REVIEW CARD BEFORE THE HANDOFF.** READ EVERY TAIL BEFORE ANY WORK.** *** THE APPEND DISCIPLINE STILL BINDS ON EVERY CHAT, and it was bought by real failures. MY APPEND ROUTINE READS THE ENTIRE PRIOR FILE, REFUSES UNLESS ITS SHA-256 MATCHES, WRITES PREFIX-THEN-PAYLOAD, AND RE-READS TO ASSERT BOTH HALVES. USE IT. Codex's S119 proved why: its patch verified and applied the COMPLETE EOF context and STILL normalised fifteen CRLF endings, so a `+99/-0` content diff was honestly clean while the byte-prefix claim was FALSE. A PATCH IS DEFINED OVER LINES; THE CLAIM IS DEFINED OVER BYTES; ON A MIXED-EOL FILE THOSE ARE NOT THE SAME STATEMENT. And lesson 206: A PATCH ANCHOR IS A SEARCH, and a search over a repeated string returns its FIRST match - authenticating the file's digest constrains what the file IS, never where the write GOES. *** *** THE S117 RULE: a wrong number found inside my own turn may be repaired by rewriting my own payload onto a re-asserted byte-identical prefix ONLY BEFORE A COMMIT OR A HANDOVER. Afterwards the answer is A NEW APPENDED CORRECTION and nothing else. READ THE OTHER AGENT'S REPORT BEFORE ASSIGNING A FINDING LETTER, not only its chat turn (lesson 192). *** *** THE CROSS-AGENT DIGEST CONVENTION STILL STANDS and is non-blocking; an absent prior digest is not a fault and not a blocker. *** **If a judgment comes back contested and one exchange does not settle it from source, ESCALATE to the director rather than trade turns - and under the superseding method the round limit and the five terminal outcomes are the mechanism for that.** **DO NOT RE-OPEN:** the payload-boundary extension document, the five S62 edits, the unified Option-B rule, the measure-first ruling, the payload analyzer/tests, the role-coverage states, the readback ruling, `.gitattributes`, Step 25, the screen result, A2, Codex's two S77 rulings, its four S78 rulings, its S80 ruling on the forty escapes, its S81 Finding-G ruling, its S83 rulings, the closed attribution rung, the closed dev-fit contract, the closed trainer, the frozen rung-2 design, the closed rung-2 module, executable, plan, run and two raw artifacts, the closed public-entry loops, the S128 ruling that no EOL pin is added for `*.py` (S130's `*.sha256` pin does not contest it - different premise, and measured; **but see the head block's forward item 1, where step 5's runtime hashing of `cable_mechanics.py` ends that ruling's premise**), and every Slot-8 loop closed at Steps 1, 2, 3 and 4a. *(Per-session chat byte histories pruned S113 and again S136; they are in Git and in `Session Summaries/`.)*
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/...- Active.md` - **S130 ADDED ONE ENTRY AND IT HAD A REASON: CODEX REPORTED A REAL APPEND-ORDER FAULT AGAINST ITSELF.** Post state 46,906 B / 811 LF / 161 CR, sha256 `28fe384d9f6753d43d5fc9fd40b87323d14cc374027fd0b2b9ccddce47e9c2ce`, my append `+65/-0`, prior `0f738373...` at 42,714 B (Codex's own disclosure, which it posted first). What I posted is the monitor's INDEPENDENT confirmation against primary Git objects: two addition-only hunks `+118/-0`; **deleting exactly the 72 inserted lines and the 46 appended lines from Codex's blob reproduces my S129 blob byte for byte**; the 2,214,481-byte intermediate prefix digest `94621642...` reproduces; both headers occur exactly once; Codex is physically last. *** THE TRANSFERABLE POINT IS ONE RUNG BELOW THE S120 ONE: this time the anchor was `-- Claude` plus a separator, a string that occurs at almost every turn boundary. A PATCH ANCHOR IS A SEARCH, AND A SEARCH OVER A REPEATED STRING RETURNS ITS FIRST MATCH. Authenticating the file's digest beforehand does not constrain where the anchor lands - a digest constrains what the file IS, an anchor constrains where the write GOES. Lesson 206. *** *** I ALSO RECORDED THE HALF THAT IS NOT A FAILURE: Codex's own post-write assertions caught it in the same turn, on three independent post-conditions, before closeout. TWO CONSECUTIVE RECURRENCES HAVE BEEN DETECTED AND DISCLOSED BY THE AGENT THAT CAUSED THEM. *** *(S121-S129 and S131 each added nothing, correctly: no fault occurred in any of them and a clean check is not a reason to post. S131's own single append was verified clean - one tail hunk, prefix and payload both asserted - and my in-turn timezone correction is not an order fault, so it belongs in the human report and not here.)* *** THE STANDARD: an entry needs a reason — a fault, or a proposal to close. A fault reported by the other agent IS a reason; a clean check is NOT, and belongs in the human report instead. *** **DO NOT EXTEND A STREAK NUMBER FROM MEMORY, AND DO NOT COMPARE A HEADER COUNT ACROSS REBUILDS** — it is a property of the recognizer, not of the transcript; this project has had a remembered count wrong five times running. *(Per-session history pruned S113; it is in Git and in `Session Summaries/`.)*

## ROUTING - which section of `Permanent Instruments.md` answers which question

*Read on demand. The file is tracked; the sections below are its `## ` headings,
in order. Nothing in it is current state.*

- `THE THREE LESSONS LIFTED OUT OF THE CLOSED BF/BG/BH ROUND - the block is gone, these are not`
- `THE PRECISION MEASUREMENT - COMPACTED S111. The full 5x10 table lives in the tracked note.`
- `THE S109 OWNER RE-REVIEW - findings BC/BD/BE, and the lesson that outranks all three`
- `THE S105-S107 PACKET-RULE ROUND - FIVE FINDINGS, ALL REPAIRED. Do not undo any of them.`
- `THE S105-S106 RUNBOOK FINDINGS - Do not undo any of them.`
- `THE FIVE PER-POINT MEANS, so a later session does not re-derive them from the artifact`
- `THE S104 AUDIT INSTRUMENT - 73 checks + a 12-mutant whole-probe control. Reuse this shape.`
- `FINDINGS AV AND AW - JOINTLY CLOSED (me S102, Codex S102). Do not undo either repair.`
- `WHAT C7 IS, so a later session does not redesign it`
- `THE TWO ROOTS THAT MUST SURVIVE, AND WHAT EACH ONE IS`
- `THE S101 AUDIT SET - 176 checks, and it is the instrument to reuse for ANY published artifact`
- `MY OPEN SCOPE STATEMENT, S101 - measured, deliberately NOT raised as a defect`
- `FINDING AU - CLOSED BY A COMPLETED RUN. What must not be undone.`
- `THE STEP-4 SHAPE, kept only because it will be needed again if anything else ever spends`
- `THE THREE PHASE-3 ITEMS - TWO NOW DISCHARGED IN S105, ONE DISCLOSED. Do not redo the two.`
- `THE TIMESTAMP GATE - built S100, held in S101-S104, AND IT EXPIRED ONCE. Rebuild it from this list.`
- `FINDING AT - CLOSED. The two sentences a future session must not undo.`
- `THE NON-FINDING I MEASURED AND DECLINED - do not "fix" this in a later session`
- `THE TWO S97 SCOPE STATEMENTS - measured, deliberately NOT raised, do not "fix" either`
- `THE EXECUTABLE - WHAT IT IS, SO A LATER SESSION DOES NOT REDESIGN IT`
- `READ THIS FIRST — Protocol P lives in a file, not in this summary`
- `Escalation trigger — content-based, and it has now held ten times`
- `HONEST ODDS — revised by the S60 finding`
- `The two zero-rollout measurements from S39 (still valid)`
- `THE STAGE-0 RESULT — the project's first pre-registered measurement (RAN S48, APPROVED S49)`
- `THE SCREEN RESULT — approved, do not re-run, do not re-review the arithmetic`
- `The delivered dataset — layout and how to read it`
- `Codex's Gate-1/2/3 layer — reference`
- `Codex's OTHER lanes — reference`
- `The evidence tables (development-evidence boundary)`
- `The agreed contract's load-bearing specifics`
- `Carried limitations for the Technical Report / Gate 7`
- `STANDING LESSONS`
- `Scratchpad (S111, NOT committed) - THE DESIGN-BY-MEASUREMENT SHAPE, and it is reusable`
- `THE RESOURCE-SPEND HISTORY`

**If a question is not answered by one of those, it is probably current state and belongs in this file rather than that one.**
