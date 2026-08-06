# Claude — Human Report, Session 86

**Date and time:** 2026-08-06 16:18 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total
remains **278.**

**Fits run:** **0.** Checkpoints written: **0.** Data generated: **0.**
**Real data read this session: none at all** — no manifest, no `.npz`, no checkpoint.

**Progress-report session:** no. My next regular progress report is Session **88**.

---

## Summary

This was a review session with one measurement in it, and the measurement is the whole story.

Codex's Session 85 handed me two states to approve or contest: five new tests it had added to
the development-fit analyzer's test file, and a correction it had appended to the public
running log. It also rejected a premise of mine — I had claimed in Session 85 that six
surviving mutation cases in that analyzer could not be tested without the project's 3.86 GB
dataset, and that closing them would require restructuring Codex's module. Codex said no: the
existing code already has the seams needed to drive those guards with small synthetic
fixtures, and it wrote five tests to prove it. It was careful to add that it had *not*
re-measured the mutation score, because my measuring harness lives in a scratch directory that
does not survive between sessions and it declined to invent a number.

**Codex was right and I was wrong.** No refactor was needed. I have corrected that finding
forward rather than quietly dropping it.

I then supplied the measurement Codex had honestly declined to make: I rebuilt the mutation
harness and ran fourteen deliberate breakages of the analyzer's derivation path against
Codex's new tests. **Ten were caught — including all five guards Codex set out to cover — and
four survived.** The four survivors were not defects in Codex's code or in mine. All three
underlying causes were the same shape: **the test fixture already had the property the thing
under test was supposed to establish**, so the test executed the code without being able to
fail on it.

The clearest one: Codex's fixture gave the four fault classes one example each. With a
perfectly even split, "pick the largest class" and "pick the smallest class" are the same
answer — every proportion is identical, and both selectors return the first name in the list.
So the test asserted that the majority class was "healthy" when what it was really pinning was
alphabetical-ish dictionary order. The real data is split 8 / 16 / 32 / 96, where the majority
class is `sensor` at 63.2% — and that 63.2% is the baseline the entire result is judged
against. It was the one number in the file the new tests could not actually see.

The other two were the same disease. The paired comparison fixture gave every random seed the
*same* difference between the two sensor suites, which makes the average and the spread blind
to how many seeds are in the table — so silently dropping three of the five seeds went
unnoticed. And the data-loading fixture handed back a hard-coded count rather than one example
per row, so the code that separates each sensor suite's own rows was never exercised.

I repaired all three fixtures. **No production code changed, no published number moved, and
the tracked result artifact was not regenerated.** Re-measured against the state I returned:
**fourteen cases, fourteen caught, zero survivors.**

Then — because last session taught me this the hard way — I refused to believe a perfect
score. I ran a negative control: two edits to the analyzer that cannot possibly change its
behaviour (a reworded comment, an added blank line). Both survived, as they must. That is what
distinguishes a real measurement from a harness that reports everything as caught, which is
exactly the fault that produced two false "perfect" readings in Session 85.

The public log correction I approved unchanged, after checking the one thing in it that nobody
would otherwise re-check: it makes a factual claim about what the log used to say. I recovered
the pre-edit text from the repository history and confirmed the description is faithful.

## Work completed

### 1. Reviewed and approved the public running-log correction

Background: in Session 84 I wrote a public log entry that explained an unfavourable result
with a mechanism nothing had measured — I said the structurally sensed robot scored worse
because a fixed-size network "has to spread the same capacity over more incoming information."
Codex rewrote that sentence in place. The rewrite was more accurate; editing a dated entry
violated the log's append-only rule. Because every possible move there flattered me, I took no
action in Session 85 and handed the ruling over. Codex ruled: correct it forward. It left the
edited entry alone and appended a dated note recording both that the edit happened and what
the evidence does and does not support.

I approved that state unchanged, after three checks:

- **Purely additive.** Rather than trust `git diff`'s "+2 / −0", I measured the longest common
  prefix and suffix of the two versions directly: 120,300 bytes of prefix, 2,274 of suffix,
  662 bytes inserted, **zero bytes removed**. No dated entry was touched.
- **Its claim about history is accurate.** A sentence describing what a document used to say is
  precisely the kind of claim both agents treat as a fact rather than a measurement. I pulled
  the pre-edit text out of the `Claude Session 84` commit and compared it against the
  post-edit text in `Codex Session 84`. Codex's description of what was removed, and of why it
  was unsupported, is faithful to what I actually wrote.
- **The form matches the playbook**, which says the log is append-only and names "rewriting
  the running log" as a failure mode.

I did name one tension out loud rather than let it pass: a note *about the log* is not one of
the three things the playbook says earns an entry (a finished artifact, a phase close, or a
genuinely noteworthy event). I still think Codex called it right — a log whose credibility
rests on being append-only owes the reader the one occasion it was not — but I flagged that a
future session should not read it as a general licence for process entries.

### 2. Accepted Codex's rejection of my premise, and corrected my own limitation

My Session-85 limitation 130 said the analyzer's derivation path "cannot be covered by the
packet's own test suite" and that closing it "means extracting the census and baseline
arithmetic into pure functions." Both halves were wrong. `load_authorized_examples` and
`evaluate_arm` are already separable seams; replacing them with fixtures drives the real
derivation code. The limitation is corrected forward, and I said plainly in the chat that I
had handed Codex a restructuring decision that should never have been a decision at all.

### 3. Supplied the mutation measurement, and found three degenerate fixtures

Fourteen cases over the derivation path, two passes, identical results, zero bad anchors, with
the byte-identity tripwire test deselected *and the deselection asserted* — the harness aborts
if the word "deselected" does not appear, which is the rule Session 85 bought after
`pytest --deselect` silently ignored a mistyped node id twice.

Against Codex's returned state: **10 caught, 4 survivors.**

| | breakage | verdict |
|---|---|---|
| A | trajectory-census guard neutered | caught |
| B | exactly-152-examples guard neutered | caught |
| C | matched C1/S class-census guard neutered | caught |
| D | zero-OOD guard neutered | caught |
| E | fit-names-the-current-trainer binding neutered | caught |
| F | majority-class accuracy: `max` → `min` | **survived** |
| G | majority class: `max` → `min` | **survived** |
| H | empirical-prior cross-entropy sign flipped | caught |
| I | paired S−C1 difference reversed | caught |
| J | sample SD: Bessel correction removed | caught |
| K | OOD counts hard-wired to zero | caught |
| L | proportions denominator hard-coded to 152 | caught |
| M | per-suite row filter removed | **survived** |
| N | paired loop truncated to two seeds | **survived** |

All five guards Codex targeted are genuinely caught. The four survivors trace to three
fixtures:

- **F and G — a uniform class census.** One example per class makes `max` and `min`
  indistinguishable in both baselines. The assertion `majority_class == "healthy"` was pinning
  dictionary iteration order under a four-way tie, not the selector.
- **N — a constant paired difference.** Every seed got the same 0.02, so the mean equals the
  constant and the sample standard deviation is exactly zero regardless of how many seeds are
  in the table. **This one is my own gap, not Codex's**: my Session-85 repair replaced a
  hard-coded `range(5)` with the contract's declared seed set precisely so the count came from
  the contract, and I never wrote the test that pins it. The existing test that does assert the
  seed list reads a *static tracked file*, which cannot move when the code that wrote it moves.
- **M — a loader stub returning its own count.** The stub ignored the rows it was handed, so
  the production code that separates each suite's rows was never exercised. Scope stated
  honestly: this is a coverage gap, not a live defect — with real rows, deleting that filter
  gives each arm 304 examples instead of 152, and the guard one line later refuses loudly.

### 4. Repaired the fixtures; production code untouched

Three changes, all inside the test file:

1. Class counts became **1 / 2 / 3 / 4** — unequal and matched across suites, with `sensor` as
   the majority and positioned neither first nor last in the mapping, so the assertion pins the
   selector rather than an ordering accident.
2. The evaluation stub's suite offset now **varies with the seed**, giving five distinct
   differences, plus an explicit assertion that the paired table names exactly the contract's
   declared seeds — the cardinality pin that was missing.
3. The loader fixture carries **152 real rows per suite in one list**, and its stub returns one
   example per row handed in. The negative case now removes a row instead of editing a count,
   so it drives the production filter.

`analyze_dev_fit.py` is byte-identical, so no artifact regeneration was required and the
tracked result is untouched. I verified that the analyzer's recorded code identity does not
name any test file rather than assuming it.

**Re-swept: 14 cases, 14 caught, 0 survivors, both passes identical.**

### 5. Audited my own instrument before trusting the perfect score

Session 85 produced two consecutive "perfect" mutation results that were both artifacts of a
broken harness, and both pointed toward my own repairs looking complete. So I treated 14/14 as
suspicious and ran a negative control: two semantically inert edits to the analyzer. Both
survived, which is what a discriminating harness must do. The verification is a *different*
observation from the one that motivated the check — which is the specific lesson last session
cost me.

## Challenges and how they were overcome

- **My own scratch harness does not survive between sessions**, which is why Codex could not
  re-measure and why the six-survivor question stayed open. I rebuilt it from the rules
  recorded in my context summary rather than from memory of the code. Those rules — assert the
  deselection, whole-line anchors, no `-x`, clear the bytecode cache, restore in a `finally`
  and re-verify the digest, run twice and require agreement — are all scar tissue from real
  faults, and every one of them earned its place again this session.
- **Comparing the two README versions initially looked like a 123 KB rewrite.** It was not: I
  had compared a stored (LF) version against a working-tree (CRLF) version, which makes every
  line differ. This project has hit the line-ending trap in four separate files now; the fix is
  always to compare like with like and to say which rendering a digest refers to.
- **I had the wrong full hash for the previous README version** in my carried notes and got an
  empty result. I took the real hash from the commit rather than from my summary — which is
  the standing rule about never quoting a figure from a summary when a primary record exists.

## Important decisions

1. **Approve the public correction unchanged.** Verified additive, historically accurate, and
   the right form under the playbook.
2. **Concede the refactor question in plain language.** Codex's reading of its own module was
   better than mine. Recording that clearly matters more than recording it gently.
3. **Repair rather than block.** Nothing found changes a published number; all three are test
   fixtures. This continues the turn the last two sessions made — measure, repair, hand back
   with an explicit approval, and reserve blocking for something that moves a result.
4. **Report that the test count did not grow.** I added no tests; I made three existing ones
   able to fail. A repair that adds no count looks like nothing happened, and a growing count
   looks like defects were found. Neither is what this was, so I said so first.
5. **Leave the Live-Run README untouched.** No artifact finished, no phase closed. The log is
   lean by design and Codex had just appended to it.

## Insights gained

- **A test can execute a line without being able to fail on it, and a uniform fixture is the
  purest form of that.** Four equal classes make "largest" and "smallest" the same answer. The
  test ran the baseline arithmetic, asserted a value, passed — and could not have caught the
  code computing the opposite of what it claims. The general move: for every fixture, ask what
  the code under test is supposed to *distinguish*, then check the fixture actually differs
  along that axis.
- **The defect landed one layer below the repair again — but this time inside the repair I
  asked someone else to make.** Codex's tests were the right idea, correctly targeted, and
  three of their fixtures were degenerate. Seven consecutive rounds have had this shape. It is
  no longer an observation about luck; it is where to look first.
- **A reviewer who declines to invent a number leaves the right thing undone.** Codex could
  have quoted a plausible mutation score and nobody would have checked. It said explicitly that
  it had not measured, which is what made the gap visible enough for me to close. The honest
  omission was more useful than a confident number would have been.
- **My own gap was the one I was least likely to find.** Case N exists because a repair *I*
  made in Session 85 — deriving the seed count from the contract instead of hard-coding it —
  was never given a test. I found it only because the sweep was aimed at someone else's work
  and happened to cross my own.

## Files created or updated

Created:

- `agents/Claude/Session Summaries/HumanReport86.md`

Updated:

- `Reproducibility Packet/tests/test_dev_fit_analysis.py` — three fixture repairs
  (blob `c7b0a09371a86bb402dfbcdd1f9e33604f228552`)
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — my Session-86 turn, `+180 / −0`, single hunk at the physical tail
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

Reviewed, approved and **left unchanged**:

- `README.md` (root, public) — blob `a544f9d25f75f850b4a11bb061039be8bcac39b1`
- `Reproducibility Packet/scripts/analyze_dev_fit.py` — blob `31381b18...`
- `Reproducibility Packet/results/dev_fit/dev_fit_analysis.json` — blob `0d00b5ca...`
- `Reproducibility Packet/results/dev_fit/dev_fit_result.json` — blob `d4cefb61...`
- `Reproducibility Packet/README.md` — blob `eb4a58e4...`

## Verification

```text
mutation sweep, Codex's state        14 cases | 10 caught | 4 SURVIVORS | 0 bad anchors
mutation sweep, state returned       14 cases | 14 caught | 0 survivors | 0 bad anchors
                                     both passes identical; restore digest re-verified;
                                     tripwire deselected and the deselection ASSERTED
negative control                     2 semantically inert edits, both SURVIVED
analysis focused                     35 passed (count unchanged; no test added)
trainer + contract + analysis        177 passed under python -O, expected warning only
FULL PACKET SUITE                    1,551 passed in 115.64 s  (Codex S85: 1,551 — no change)
compileall                           clean
git diff --check                     clean (expected autocrlf notices only)
README additivity                    662 bytes inserted, 0 removed (prefix/suffix measured)
README history claim                 verified against 388f55c and ba95c0e primary blobs
Codex's S85 transcript append        single tail hunk @@ -23249,0 +23250,98 @@, additions only
my transcript append                 single tail hunk @@ -23347,0 +23348,180 @@, additions only
FITS 0 | CHECKPOINTS 0 | GENERATION 0 | ROLLOUTS 0
lifetime Protocol-P physical execution unchanged at 278
REAL-DATA TOUCHES                    ZERO of every kind.  PILOT / VAL / TEST: 0
config/config.json                   absent
```

## Transcript-order monitoring

No recurrence, so no note was added to the monitoring chat — the standing duty is to flag
recurrences, not to log clean sessions. Verified at the Git level rather than assumed: Codex's
Session-85 commit touches the shared transcript as a single hunk of 98 added lines and zero
removed, landing after my Session-85 header at the then-physical tail, and it touches the
monitoring file not at all. My own append is likewise a single tail hunk, 180 added, zero
removed.

## Next steps

1. **Codex approves or contests `test_dev_fit_analysis.py` at blob `c7b0a093...`.** If it
   approves, every Gate-4 development-fit review loop is closed.
2. **The Slot-9 capacity ladder for the structurally sensed suite is then the real next step.**
   The first fit found that suite scoring slightly *worse* than the conventional one on its own
   training data at a fixed 39,594 parameters — which is a statement about network size, not
   about sensors, and the ladder is the instrument that was planned in advance to settle it.
   Nothing about that is authorized yet; it needs design and review first.
3. **The seed-spread finding still awaits the Gate-6 sample-size decision.** Run-to-run spread
   across random seeds is roughly three times the effect the study is designed to detect. That
   belongs in the confirmatory design before anything is frozen.
4. Every later gate stays exactly where it is: no reserved-split reads, no threshold selection,
   no configuration freeze, no confirmatory claim.
