# Claude — Human Report, Session 88

**Date and time:** 2026-08-07 00:20 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.

**Fits run this session:** **0.** Checkpoints written: **0.** Data generated: **0.** Pilot / validation / test reads: **0.**

**Progress-report session:** **yes** — regular cadence, my Session 88, covering Sessions 81–88.

---

## Summary

Codex's Session 87 did two things: it approved my strengthened test blob and correctly
observed that I had never explicitly approved it myself, leaving the loop open on a process
gate rather than a technical one; and it blocked my capacity-escalation design on five
substantive findings plus three rulings.

This session closed the first and answered the second.

**I explicitly approved test blob `6f29bf05...` unchanged**, after re-opening the file and
re-running it rather than approving from memory. With both approvals now naming the same
bytes, the Gate-4 dev-fit readback loop is closed in all three of its parts — analyzer,
tracked artifact, and tests.

**I accepted all five of Codex's findings and all three of its rulings, without contest.** I
went looking for something to push back on and did not find it; in two places its argument was
better than the one I had written, and I recorded its reasoning rather than mine.

**Then I found three more defects while implementing the accepted revisions, two of them one
layer below anything either review had reached.** The first is the one that matters:
**the approved trainer cannot fit a network of any width other than the one it already
fitted.** The size is hard-coded, there is no CLI flag for it, and the word does not appear in
the file or its contract. So the sweep I designed — and that Codex reviewed in detail and
returned five criticisms of — could not have been implemented at all. Worse, my own
comparability invariant would have refused the only edit that fixes it, because editing the
trainer moves the code fingerprint that the reused anchor arms recorded as their producer. The
repair is to stop asserting the two fit paths are equivalent and to **measure** it: refit one
32-channel arm through the new path and require bit-identical weights.

The second is that the saturation criterion was on the wrong quantity, and the error discards
real evidence rather than admitting bad evidence.

**The revised document is returned at blob `ccd12ef4...`, explicitly approved by me.**

---

## Work completed

### 1. Context-first startup, complete

Read `Project Details/Project Details.md` in full, `AgentPrompt.md` in full, my own continuity
summary, every `Summary.md` in the four chat folders that include me, and both active chats.
Then Codex's `HumanReport87.md` and its Session-87 turn in the Phase-2 transcript, which is the
cross-review duty for the session.

### 2. The explicit owner approval — the missing gate

Codex was right and the correction is narrow: "state returned" plus "approve or contest" is a
handoff, and the review playbook forbids inferring approval from one. I re-verified before
saying it:

```text
git hash-object tests/test_dev_fit_analysis.py   6f29bf05ddebae9f33817381f4713089f99ee7e4
_DERIVED_CLASS_COUNTS                            (1, 2, 4, 3)   majority index 2 = actuator
focused suite under python -O                    35 passed, 1 expected warning
```

**I approve exact blob `6f29bf05...`, unchanged.** The Gate-4 dev-fit readback loop is now
closed on `analyze_dev_fit.py` (`31381b18`), `dev_fit_analysis.json` (`0d00b5ca`, canonical
`7bec34a1...`) and this test file.

### 3. Every Codex finding and ruling, accepted and implemented

| Codex finding | what changed |
|---|---|
| **A** — the `CAPACITY_BOUND` verdict outruns a fixed-epoch width sweep, and a rising paired difference can mean C1 got worse | verdict removed; the statement that width and optimization are not separable now appears in §1, §4.1 and §9; the absolute per-suite curves are first-class outputs (§3) and §5.4's interpretation table keys on them |
| **B** — the outcome function was not executable, not exhaustive, and licensed Stage 2 from opposite branches | the executable now emits **no verdict at all** — exactly-defined descriptive fields only, with the interpretation pre-registered as prose and applied jointly, and **no observation licensing anything** |
| **C** — the same seed number is not cross-width CRN | §4.3 rewritten as three claims with three scopes, each independently measured this session |
| **G** — the grid needs a second point above the fitted anchor | grid is `{16, 24, 32, 40, 48}`; 61,010 parameters reproduced independently; cost re-measured |
| **I** — a forty-fit action needs a run-level plan and a partial-failure contract | new §7: zero-fit plan mode, run-level artifact on every terminal path, explicit retry/resume rules, and invariant C10 |

The three rulings — review the design now, no within-dev trajectory holdout, and reconcile
Slot 14 with bound 5 rather than banning a report sentence — are all taken. The holdout ruling
is recorded on **Codex's** grounds rather than mine, because its argument is better: the two
dev trajectories are different regimes (one carries the diagnostic probe, one does not, with
different onsets, origins and run lengths), so the estimand would be regime transfer, not
held-out generalization. My draft's reasons were comparability and sample size, which are
weaker.

I verified Finding C rather than accepting it, because it decomposes into three statements
with different truth values:

```text
(channels=32, seed=3) twice          bit-identical state dict      -> suite pairing IS real CRN
(channels=40, seed=3) twice          bit-identical state dict
(32, 3) vs (40, 3)                   DIFFERENT, as they must be    -> no cross-width CRN
default_rng(k).permutation(152)      width-independent, k in {0,3} -> row order IS common
```

### 4. Finding Y — the approved trainer is width-locked, and my own invariant would have blocked the fix

Measured this session:

```text
dev_fit_trainer.py:968     net = TemporalAttributionNet(seed=seed).to(device)
                           the file's ONLY network construction site
CLI flags                  --mode --output-dir --data-root --epochs --batch-size
                           --learning-rate --device        (no capacity flag)
grep -c 'channels'         dev_fit_trainer.py 0 | dev_fit_contract.py 0
```

`fit_one_arm` takes examples, seed, epochs, batch size, learning rate and device. Width is not
among them. **The Gate-4 fit path is width-locked at the 32-channel default**, so the
measurement as designed and as reviewed was unimplementable.

The collision is the interesting part. My invariant C3 requires the reused anchor row's
recorded `code_identity` to match the code fitting the new points. Threading `channels`
through `dev_fit_trainer.py` changes `training_code_identity()["dev_fit_trainer.py"]`, so
**the anchor would fail its own identity check by construction** — the invariant written to
guarantee comparability refuses the only edit that makes the measurement possible. And that
file's bytes are the recorded producer of ten git-ignored checkpoints whose sole provenance
record is `dev_fit_result.json`, which is precisely why we agreed not to touch it.

New invariant **C9**: before any sweep fit, fit one 32-channel arm through whatever new fit
path is used, into a scratch root, and require the parameter tensors to be **bit-identical** to
the corresponding approved checkpoint — refusing loudly on difference, on a missing checkpoint
(a fresh clone has the ledger without the weights), and on an unmakeable comparison. One fit,
about seven seconds, dev rows only.

I wrote two routes into the document and **handed the choice to Codex** rather than taking it,
and said in the document that the recommendation arguably favours me: Route A is a new module
importing the approved loss and contract, leaving the trainer untouched; Route B is an
additive keyword-only argument in `fit_one_arm`. C9 is mandatory under both.

### 5. Finding Z — the saturation criterion measured the wrong quantity

Codex objected to the aggregation (a suite mean hides seed-level saturation). It is right, and
the quantity was wrong too, which is the deeper error. The read is over macro-F1; the criterion
was over accuracy; under this split's 8/16/32/96 census they are far apart:

```text
3 healthy examples misclassified as sensor, everything else correct
    accuracy 0.9803  -> the S87 rule calls the point SATURATED
    macro-F1 0.9385  -> |d| could still be as large as 0.0615
3 structure examples misclassified as healthy, everything else correct
    accuracy 0.9803   macro-F1 0.9347  -> |d| could still be as large as 0.0653
```

Both exceed the project's own 0.05 success bar, so the rule would have discarded a point at
which a bar-sized difference was still arithmetically available. **A guard that throws evidence
away is failing in the wrong direction.**

The replacement is an identity rather than a threshold. For macro-F1 values in [0, 1],
`|d| = max − min ≤ 1 − min`, so `headroom(c,k) = 1 − min(macro_f1_C1, macro_f1_S)` is an exact
upper bound on the paired difference at that seed. A pair is BAR_CONSTRAINED iff
`headroom < BAR` — and **`BAR` is read at run time from the approved artifact's
`paired_macro_f1.claim_sheet_success_bar` field**, not written as a literal, so the criterion
inherits an already-approved constant instead of inventing one. Session 87's open question 3
disappears rather than being answered. Aggregation is per pair, then per point as
NONE / PARTIAL / ALL, which is Codex's finding implemented. At rung 1 the per-seed headroom is
0.3157 to 0.5133, nowhere near constrained.

### 6. The cost table did not reproduce, and I said so

Codex required the 40-channel cost measured rather than interpolated. I re-ran the whole probe
on synthetic tensors (no data read, no checkpoint, no fit). The 40-channel row is 0.024 s/step,
9.2 s/arm; the forty new fits are about 338 s. But the four rows I measured in Session 87 came
back different — 0.015/0.021/0.023/0.026 then against 0.016/0.018/0.019/0.031 now, up to 19%
apart at 48 channels and in both directions. §8 now states that **no cost figure in the
document may be quoted as anything but an order of magnitude**, and that nothing may be trimmed
on the strength of it.

### 7. The returned state

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  git blob          ccd12ef4ac0a670a01b30c863fca2c8fede45324
  canonical sha256  283de293f1557f28757454570c3029e5958eea1b171ce9acb57c945b43980fab
  45,400 bytes / 752 lines / LF / raw == canonical / no BOM / eol=lf via git check-attr
```

Kept at v0.1, as Codex asked: the document has never been jointly approved, so this is an
in-place revision of an unapproved draft rather than an edit to an approved version, and the
document says the bump-and-`git mv` rule takes over the moment we both approve a state.
**I explicitly approve these exact bytes.** §10 records Codex's five findings and three rulings
against the sections they changed and closes all five of my Session-87 open questions; §11
carries five new ones, of which the route decision is the only load-bearing one.

### 8. Live-Run README heartbeat — checked, deliberately unchanged

Ran the check per `Playbooks/live-run-readme.md` and added nothing, for the third consecutive
session. The only loop that closed is a test fixture's, which is not a stranger-facing
artifact; the design is a revised draft in an open review round, which is work in progress and
is exactly what the lean log is not for; and Finding Y, interesting as it is, is a mid-review
engineering discovery rather than a project-level event. The banner is already current at
2026-08-06 and `README.md` remains at blob `a544f9d2`.

### 9. Transcript-order monitoring — verified, no recurrence, no note added

Verified at the git level rather than assumed. Codex's Session-87 commit `08434d2` touches the
Phase-2 transcript as a single tail hunk `@@ -23790,3 +23790,186 @@`, additions only
(`+183/−0`), and touches the monitoring file not at all. My own append is likewise a single
tail hunk. The duty is to flag recurrences, so a clean session adds no note.

---

## Challenges and how they were handled

- **A process gate that was not a technical defect.** Codex approved my bytes and still held
  the loop open because I had never literally approved them. The temptation is to treat that as
  bookkeeping. It is not — the whole review cycle rests on approval never being inferred — so I
  re-opened and re-ran the file before saying the words, rather than approving from memory.
- **Nothing to contest, which is its own risk.** Five findings and three rulings and I agreed
  with all eight. A round in which the reviewer is simply right is a round where the temptation
  is to accept quickly and move on. I verified Finding C by measurement instead, and that
  verification is what surfaced the fact that the network's shape does not depend on the sensor
  suite at all — which is the property Finding Y then collided with.
- **The defect was found by asking "how would this actually be built?"** Neither review found
  Finding Y, because both were reviewing a design document against its own logic. It surfaced
  the moment I went to write down which function the executable would call. That is the ninth
  consecutive round in which the defect sat one layer below the layer being reviewed.
- **Nearly reintroducing a struck claim into the progress report.** My first draft of the
  accessible explanation used the phrase "spread the same capacity over more incoming
  information" — the exact unmeasured mechanism Codex had struck from the public log in its
  Session 85 and that I approved the removal of in my Session 86. I caught it while checking my
  own continuity notes and rewrote the section to state the measured facts and say explicitly
  that the mechanism is not among them. **A claim withdrawn from one document will walk back in
  through another unless the withdrawal is carried as a rule rather than as an edit.**

---

## Important decisions and reasoning

1. **Approve `6f29bf05...` literally and unchanged.** The fixture is correct, the loop's only
   remaining gap was mine, and it costs nothing to close it properly.
2. **Accept all eight of Codex's items without contest, and record two of them on its
   reasoning rather than mine.** Where the reviewer's argument is better than the author's, the
   document should carry the reviewer's argument.
3. **Remove the verdict from the executable entirely rather than repairing the classifier.**
   Codex's finding was that the outcome rules were not executable and licensed contradictory
   actions. Repairing them would have left a machine emitting scientific claims. Separating
   "what was observed" (executable, exact inequalities, no licence) from "what it means"
   (pre-registered prose, applied jointly) removes the whole class of defect, and it answers my
   own Session-87 open question 4 in the direction I had leaned away from.
4. **Measure the fit-path equivalence rather than assert it (C9).** The alternative was a
   sentence claiming a new fit path reproduces an approved one. One fit and seven seconds turns
   that into a check that fails loudly.
5. **Hand the Route A / Route B decision to Codex, and say the recommendation favours me.**
   Route A avoids reopening a file I helped close. That is a real reason and also a
   self-interested one, and naming it is cheaper than being caught by it.
6. **Replace the saturation threshold with an algebraic bound rather than a better number.**
   The criterion now inherits the Claim Sheet's own success bar from a field the approved
   artifact already publishes, which removes the last invented constant in the read.
7. **Disclose that the cost table did not reproduce.** Silently replacing four numbers with
   four different numbers would have looked identical to a clean re-measurement.
8. **Leave the public README alone.** Third consecutive session; the reasoning is the same and
   is recorded so it is a rule rather than a habit.

---

## Insights gained

- **A design document can be complete, internally consistent, reviewed in detail by both
  agents, and unimplementable.** The reviews checked the design against itself. Nothing checked
  it against the function it would have to call. The cheapest instrument for that class of
  defect is to write one paragraph naming the exact call site before the design is frozen.
- **An invariant that guarantees comparability can forbid the change that makes the measurement
  possible.** When a rule and its purpose come apart, the answer is usually to convert the rule
  from an assertion into a measurement — the rule was standing in for a check nobody had run.
- **A guard can fail in two directions and only one of them is loud.** The accuracy-based
  saturation rule would have thrown away good evidence, which produces a smaller reported
  result and no error message anywhere. Ask of every guard not only "what does it let through"
  but "what does it discard."
- **A constant that comes from an already-approved artifact is not the same kind of object as a
  constant chosen in the document that uses it.** Reading `BAR` at run time from the approved
  artifact removed an open question instead of answering it.
- **A withdrawn claim needs a rule, not an edit.** The struck public-log phrase was one
  keystroke from reappearing in a different document, in a session whose entire subject was
  reviewing carefully.

---

## Files created or updated

Created:

- `agents/Claude/Session Summaries/HumanReport88.md` (this file)
- `agents/Claude/Progress Reports/Progress Report Session 88.md` (regular cadence, S81–S88)

Updated:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` (revised; blob `ccd12ef4`)
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` (`+203/−0`, single tail hunk)
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md` (rewritten)

Reviewed and deliberately unchanged:

- `Reproducibility Packet/tests/test_dev_fit_analysis.py` (`6f29bf05`, approved)
- `Reproducibility Packet/scripts/analyze_dev_fit.py` (`31381b18`)
- `Reproducibility Packet/results/dev_fit/dev_fit_analysis.json` (`0d00b5ca`)
- `Reproducibility Packet/results/dev_fit/dev_fit_result.json` (`d4cefb61`)
- `Reproducibility Packet/scripts/utils/dev_fit_trainer.py` (read only — Finding Y is a
  *report* about this file, not an edit to it)
- `README.md` (root, `a544f9d2`)
- `.gitignore`, `.gitattributes`
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`

---

## Verification

```text
test blob approved            6f29bf05ddebae9f33817381f4713089f99ee7e4  UNCHANGED
focused suite under -O        tests/test_dev_fit_analysis.py 35 passed, 1 expected warning
FULL PACKET SUITE             1,551 passed in 119.03 s  (Codex S87 1,551 — NO change)
design document               blob ccd12ef4 | canonical 283de293... | 45,400 B / 752 lines
                              LF | raw == canonical | no BOM | eol=lf via git check-attr
40-channel probe              61,010 parameters | receptive field 1,023 | band guard accepts
init-weight probe             (32,3)==(32,3), (40,3)==(40,3), (32,3)!=(40,3)
row-order probe               default_rng(k).permutation(152) width-independent, k in {0,3}
census counterexample         3 healthy errors -> acc 0.9803 / macro-F1 0.9385 / headroom 0.0615
cost probe                    synthetic tensors only; no data read, no checkpoint, no fit
production blobs UNCHANGED    analyze_dev_fit.py 31381b18 | dev_fit_analysis.json 0d00b5ca
                              dev_fit_result.json d4cefb61 | README.md a544f9d2
                              dev_fit_trainer.py and attribution_net.py untouched
transcript append             pre-write 1,506,399 B / 23,975 lines / sha 1f4602a8...
                              post-write 1,518,959 B / 24,178 lines; prefix byte-identical
                              asserted INSIDE the writer; +203/-0; header unique at line
                              23,977; Claude physically last; turn asserted pure ASCII
Codex S87 append              single tail hunk @@ -23790,3 +23790,186 @@, +183/-0,
                              monitoring file untouched. NO RECURRENCE.
FITS 0 | CHECKPOINTS 0 | GENERATION 0 | ROLLOUTS 0
REAL-DATA TOUCHES             *** ZERO OF EVERY KIND. No manifest, no .npz, no checkpoint,
                              no regeneration, no fit, no generation, no rollout. The only
                              reads were the tracked dev_fit_analysis.json and source files.
                              PILOT / VAL / TEST: 0. ***
```

---

## Next steps

1. **Codex reviews the revised capacity design at blob `ccd12ef4...`** and rules on the Route A
   / Route B question in §11. Even a same-state approval authorizes only writing the executable.
2. If it approves, the executable and its tests are built and run through the review cycle —
   a separate gate.
3. Then the zero-fit plan artifact is produced and reviewed — a third gate.
4. Then the C9 equivalence fit and the forty sweep fits are jointly authorized — a fourth.
5. Everything downstream stays closed: pilot, validation and test outcomes, thresholds, the
   config freeze, generation, and every confirmatory boundary.
