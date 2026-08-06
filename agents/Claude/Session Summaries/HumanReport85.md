# Claude — Human Report, Session 85

**Date and time:** 2026-08-06 12:42 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278.**
**Fits run this session:** **0.** Checkpoints written: **0.** Data generated: **0.**
**Progress-report session:** no. My next regular progress report is Session **88**.

---

## Short result

Codex spent its Session 84 auditing the ten development fits I ran in my Session 84, and it
built a new read-only analysis script so the four separate loss terms would survive in a
tracked artifact rather than only in my scratch notes. It then handed me six states and
asked for a genuine owner review.

I did that review. **The fit ledger is correct and I approved it** — I re-hashed all ten
checkpoints, rebuilt every published number from the artifact's own fields, and confirmed
the document contains nothing machine-specific. **Both of Codex's rulings are right and I
took both**, including one where its reasoning was better than mine had been.

The new analysis script is correct code with very little holding it in place. I found five
things, repaired four of them, and handed two decisions back rather than taking them.

**The most useful thing this session produced is not in the packet.** Twice in a row my own
measuring instrument told me the coverage was perfect, and twice it was lying — in a way
that flattered my own work. Catching that took more care than any of the findings did, and
the rule it produced is now written into the code where the next person will hit it.

---

## Work completed

### 1. Owner approval of the first fit ledger

Codex was right that my Session-84 handoff *described* the tracked ledger but never
approved an exact digest, and right that a reviewer's approval cannot supply the owner's.
I approved it explicitly this session:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
```

I verified it with a script that does not import either program that touched it: ten
checkpoint files re-hashed against their recorded digests (10/10), ten distinct digests,
the ten suite/seed keys unique and complete, the class census summing to 152, and zero
backslashes, drive letters, repository names or user names anywhere in the document.

One property I had not previously recorded and which matters: **this file contains no
newline characters at all.** It is compact JSON, so its raw and its canonical digest are
the same number in every checkout on every platform. That turned out to be exactly the
property the file beside it lacks — see Finding A.

### 2. Both of Codex's rulings accepted

**Finding W** (an unreachable refusal path in the trainer can raise instead of exiting
cleanly): Codex ruled it stays disclosed rather than fixed. I accepted, and its argument
is stronger than the one I made in Session 84. Editing the trainer now would leave the
packet unable to reproduce its own tracked ledger from its own current producer — the ten
checkpoints record the trainer's exact bytes as their provenance. The cost of the edit
lands on the provenance record, not on the trainer, and it is larger than the defect. I
also treat Codex's condition as binding: if a future authorization ever allows a reused
output directory, this must be fixed before that runs.

**Finding X** (the ledger stores only the summed loss, which is not a meaningful ranking
number): Codex accepted the substance but declined to rewrite the historical ledger or
re-run the ten arms to change its schema, carrying the fix forward in a new analysis
artifact instead. That is the right shape and the one the project's amendment discipline
asks for.

### 3. Five findings in the new analysis script

**A — the packet's runbook published a digest a reader cannot reproduce.** Step 27 named
the analysis artifact's **raw** SHA-256. That file carries 426 line endings, the path has
no line-ending pin, and this repository converts line endings on checkout — so a stranger
who clones the packet and hashes the file gets a different number than the README tells
them to expect. Measured by materialising the file the way a fresh clone receives it:
14,591 bytes and 426 CRLF pairs against the working tree's 14,165 and none, with a
different digest. The same instrument reproduced a previously recorded measurement for
another artifact exactly, which is my evidence the instrument is right; Git's own warning
says the same thing in its own words. This is the fourth time this project has hit this
class, and the first time inside a runbook instruction, which is worse — the packet's
entire purpose is that an outsider can check it. **The fix is the label, not the file:**
the number Codex published is the canonical digest, and the canonical digest is stable
everywhere. I changed the word, not the artifact, and deliberately did not touch the
line-ending configuration, which is a settled decision.

**B — the loss decomposition was a hand-copy with nothing comparing it to the original.**
The analyzer re-writes the four loss terms so they can be reported separately; the trainer
owns the summed version. The analyzer imports the trainer and then re-types its loss. I
drove both on the same inputs over five random forward passes: they agree to 3.6e-07,
which is floating-point addition order rather than disagreement. So the copy is faithful
today and nothing was checking that it stays faithful. I made the trainer's own value the
analyzer's post-condition, with the measurement and the reason for a non-zero tolerance
written into the code beside the constant.

**C — coverage, measured rather than asserted.** A 22-case mutation sweep over the 591-line
analyzer, against its own ten tests: **7 caught, 15 survived**. The survivors included the
checkpoint-digest verification, both the sign and the scale factor of the severity loss
term, the total itself, and the guard binding the analysis to the current trainer. Nothing
drove the script's main path at all.

**D — a docstring claimed a stability property that measurement denies.** The code rounds
every number before writing it, documented as making the file "hardware-stable". Every
value in the artifact round-trips through that rounding to the *identical* underlying
32-bit float, so two machines that genuinely disagreed would still write two different
numbers. The rounding shortens the printed decimal and nothing more. I rewrote the
docstring to say that and pinned the measurement as a test.

**E — the analysis had no producer binding, though the fit did.** The analyzer refuses a
fit ledger that does not name the current training code. Nothing required a *tracked
analysis artifact* to name the current analyzer. So editing the analyzer without
regenerating left a tracked file whose recorded producer no longer existed — silently, and
it is exactly the failure Codex's own Finding-W ruling refused to create on the fit side. I
added the missing half. It went red the instant I edited the analyzer, which is the point.

I also replaced a hand-typed seed range and two hand-typed counts with values derived from
the contract that defines them. Same numbers today; a renumbered plan would previously have
crashed rather than refused.

### 4. The artifact was regenerated, and exactly one field moved

Regenerating was forced by finding E's new test. A field-by-field comparison of the new
document against Codex's shows **one difference: the analyzer's own digest.** Every measured
quantity — all ten arms, both suite summaries, the paired table, the baselines, the census —
is unchanged. Two regenerations into two separate scratch directories produced byte-identical
files. The run costs 4.2 seconds, reads the 304 already-authorized development rows and the
ten checkpoints, and runs no fit, no simulation and no data generation.

### 5. Two instrument faults of my own — the part of this session worth keeping

After the repairs I re-ran the sweep and got **19 caught, 0 survivors**. Perfect coverage.

It was false. My new producer-binding test compares the artifact's recorded analyzer digest
against the file on disk, so it fails for *any* byte change to that file — it reports every
mutation as caught, no matter how meaningless. It is a tripwire on the file's bytes, not a
test of behaviour. I confirmed this by driving one deliberately irrelevant mutation and
reading which test failed: only that one did.

I deselected it and got **25 caught, 0 survivors** — the same lie a second time. The
deselection had silently not happened. The testing tool ignores a request to skip a test
whose name matches nothing: no warning, no error, exit code zero. I had given it a path in
the wrong form. Both runs had quietly executed the full suite including the tripwire.

The honest number, with the deselection verified, is **25 cases, 16 caught, 9 survivors**.
I then closed the three that were cheaply reachable, ending at **25 cases, 19 caught, 6
survivors**, with both passes identical and the file's digest re-verified after restore.

The harness now refuses to report a verdict unless it can confirm the deselection took
effect — which is the same rule this project already applies to a missing mutation anchor:
*a check that did not happen must be recorded as a failure, never as a skip.* The warning is
also written into the tripwire test's own docstring, where the next person running a sweep
over this file will actually see it.

What makes this worth a section rather than a footnote is the direction of the error. Both
faults produced results that made my own repairs look complete. The only reason either was
caught is that a perfect score is itself suspicious.

---

## Challenges and how they were resolved

- **Distinguishing "this guard is tested" from "the file changed" required auditing my own
  new test.** Resolved by driving a semantically irrelevant mutation and reading which
  single test failed, rather than trusting the aggregate.
- **A silent no-op in a standard tool.** `pytest --deselect` accepts a non-matching node id
  without complaint. Resolved by making the harness assert the deselection appears in the
  output and abort otherwise.
- **My first attempt to write a probe through a shell heredoc failed to parse.** Resolved by
  writing probe files directly rather than piping them through the shell — the same lesson
  this workspace already carries about multi-line scripts.
- **Deciding how much of someone else's module to restructure during review.** Six of the
  surviving mutations sit in code that only executes against the 3.86 GB dataset the packet
  cannot distribute. Closing them means extracting logic into testable pieces. After four
  edits and a regeneration I judged further restructuring to be the kind of scope creep that
  produces new defects, so I disclosed it precisely and handed the decision to Codex.

## Decisions I made, and their reasoning

1. **Approved the fit ledger** — verified independently rather than from my own memory of
   having produced it.
2. **Accepted both rulings without re-arguing them**, including one where Codex's reasoning
   improved on mine. Re-litigating a settled point is this project's named escalation
   trigger.
3. **Repaired rather than blocked.** All five findings were either documentation, a missing
   check, or missing coverage — none changed a published number. Blocking would have cost a
   full round and produced the same bytes.
4. **Fixed the digest by relabelling rather than by changing the line-ending configuration.**
   The configuration decision is settled in this project and the settled position is to
   publish canonical digests. Applying an existing ruling is not the same as making a new one.
5. **Did not touch the public README, deliberately.** Codex edited the body of my dated
   public log entry rather than correcting it forward. The playbook lists rewriting the log
   as a named failure mode and the log is append-only. But **the edited words are mine and
   Codex's replacement is more accurate than what I wrote** — my sentence asserted a
   mechanism nothing had measured. Any move I make there flatters me, so I recorded the
   finding, said plainly that it favours me, and handed the ruling to Codex.

## Insights gained

- **A perfect measurement is a reason to audit the instrument, not to celebrate.** Two
  consecutive instrument faults this session, both producing flawless-looking coverage.
- **A test that reads the thing it checks can become a tripwire on a whole file**, and a
  tripwire destroys the resolution of every other measurement over that file. The test is
  still worth having; it just has to be labelled so the next measurement isn't ruined by it.
- **A digest is only provenance if it identifies the document rather than the copy.** The
  fit ledger is immune to this because it happens to contain no line endings; the analysis
  artifact beside it is not. Same folder, same session, opposite exposure.
- **The strongest repair this session was the one that made a *future* mistake loud**
  rather than fixing a present defect. Nothing was wrong with the tracked analysis when I
  found finding E. The binding exists so that the next edit cannot go unnoticed.

## Files created or updated

Created:
- `agents/Claude/Session Summaries/HumanReport85.md` (this file)

Updated:
- `Reproducibility Packet/scripts/analyze_dev_fit.py` — loss post-condition, contract-derived
  plan values, corrected docstring
- `Reproducibility Packet/tests/test_dev_fit_analysis.py` — 10 tests to 30
- `Reproducibility Packet/results/dev_fit/dev_fit_analysis.json` — regenerated; one field changed
- `Reproducibility Packet/README.md` — Step 27 digest relabelled and qualified
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — one append, +227/−0
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`

Untouched and verified still at their jointly approved bytes: the trainer, the dev-fit
contract, both their test files, the fit ledger, and the root `README.md`.

## Verification

```text
full packet suite                    1,546 passed in 114.73 s   (Codex Session 84: 1,526)
analysis focused                     30 passed   (Codex handed over 10)
trainer + contract + analysis        172 passed under python -O, expected warning only
compileall                           clean
git diff --check                     clean
mutation sweep, state received       22 cases | 7 caught | 15 SURVIVORS | 0 bad anchors
mutation sweep, state returned       25 cases | 19 caught | 6 survivors | 0 bad anchors
                                     both passes identical; restore digest re-verified
ledger verification                  10/10 checkpoint digests re-hashed independently
checkout rendering                   measured into a clean tree, not reasoned about
analysis regeneration                twice, byte-identical
transcript append                    prefix byte-identical, header unique at line 23,024,
                                     Claude physically last, +227/−0
FITS 0 | CHECKPOINTS 0 | GENERATION 0 | ROLLOUTS 0
real-data touches                    the 304 authorized dev rows and ten checkpoints, read
                                     only.  PILOT / VAL / TEST: 0
config/config.json                   absent
```

**Live-Run README heartbeat:** checked, and deliberately no entry. This session closed no
artifact and no phase; it reviewed and repaired one. The public log is lean by design.

**Transcript-order monitoring:** checked at the Git level. Codex's Session-84 append is a
single hunk at the then-physical tail (`+125/−0` at line 22,897) and touches the monitoring
chat not at all. No recurrence, so no note was added — the duty is to flag recurrences.

## Next steps

1. **Codex rules on two things I handed back:** whether to restructure the analyzer so its
   derivation path becomes testable, and what to do about the public log entry that was
   edited in place.
2. **Codex approves or contests the four blobs I returned** (analyzer, its tests, the
   regenerated artifact, the packet README).
3. **Then the capacity ladder.** Rung 1 cannot settle the C1-versus-S question — both suites
   were given networks of exactly the same size — and the paired seed spread found in Session
   84 is a design warning that belongs in the sample-size decision, not in a capacity choice.
   Neither is authorized by anything that happened this session.

Still blocked and unchanged: any read of the pilot, validation or test outcomes; threshold
and calibration work; the final configuration freeze; new data generation; and every
confirmatory claim.
