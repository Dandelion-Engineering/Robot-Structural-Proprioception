# Claude — Human Report, Session 118

**Date and time:** 2026-08-11 06:38 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. My next regular progress report is Session 120, unless a phase
transition or an approved written Claim-Sheet amendment fires one sooner.

---

## Summary

### What this session was for

The last two sessions ended with a gate at one half of two. My Session 117 issued my half of the
execution authorization for the rung-2 training run; Codex's Session 117 issued the matching half
and then ran it. So this session opened into a project state that had moved further in one night
than it had in the previous ten sessions: **the larger network has now actually been trained, ten
times, and the run's raw record exists.**

That means this session had exactly one substantive job, and the frozen design names it: **step 6
of seven, the read-only analyzer.** The executable that ran deliberately persists only
*primitives* — per-arm loss histories, scores, digests, identities — and computes none of the
comparisons the project actually cares about. A separate program, written after the run but
against an interpretation frozen months earlier, is what turns those primitives into the handful
of derived numbers the pre-registered read is allowed to look at. Building that program was the
work.

Two smaller things came first: closing an open review loop on the public README, and confirming,
as monitor, a transcript fault Codex had reported against itself.

### What was accomplished

**1. The public README banner loop is closed.** Codex caught during its own closeout that the
README's `Last updated` field still said 2026-08-10 while the running log already carried two
2026-08-11 entries, and changed only that field. I reviewed the change against the playbook's
State-A banner rule and against the two Git blobs directly rather than the working tree —
`485d83ce…` → `abeac76c…`, exactly one changed line at `@@ -9 +9 @@`, 208 lines and 145,938 bytes
on both sides, cleaned digest `488c2531…` matching what Codex published. Approved at those exact
bytes. That was the project's one open loop; it is now closed and a new one (mine, on the
analyzer) is open in its place.

**2. The append-order recurrence was verified rather than accepted.** Codex reported that its
first Session-117 transcript append landed at line 19,811 instead of the physical end of file,
that its own assertions caught it before the training run started, and that it repaired the
record append-only. As the agent who holds the monitoring role in that thread, I checked the claim
at the Git level: the commit touches the technical transcript in exactly two hunks at `+277 / −0`,
so nothing was deleted, moved or truncated, the misplaced turn is still readable where it landed,
and the dated correction restates every operative part. I confirmed that in the monitoring thread.

The part I thought was worth writing down is the *cause*. Codex verified one anchor — a long
unique end-of-file block — and then applied a patch whose actual context was a different, repeated
one. **The verified object and the applied object were not the same object.** That is the same
shape as a mistake I retired in my own Session 117, where both agents had been publishing the
README's working-tree digest as if it identified the file when a line-ending filter sits between
the working tree and the thing that travels. Two different failures in two consecutive sessions,
one root: *a verification is only worth something if the thing verified is the thing that
travels.* I stated it once in the monitoring thread so neither of us has to rediscover it.

**3. Step 6 — the analyzer and its tests are built, and handed to Codex for review.**

Two new files:

```text
Reproducibility Packet/scripts/analyze_rung2_escalation.py
  blob 7cf3cc6a720f15fea61dcec670e119a83a67080f
  canonical == raw 8323494348a7a70e2735cf3938a01a273a1f0889ffe75d70435d07d6d291597c
  48,308 B / 1,125 lines

Reproducibility Packet/tests/test_rung2_escalation_analysis.py
  blob a642b3d3d96f0f7d011c5f5ccf407f4c9c1e8825
  canonical == raw 169a3cb2d4314ee0d7d3887a6d421decbbf8ed15950c6145744f18c57baecede
  54,947 B / 1,398 lines / 103 tests
```

What the program does, in plain terms: it opens the run's terminal record and refuses it unless
everything about it lines up with the plan that authorized the run, the frozen design document,
the exact code state running today, the declared twelve-fit budget, and the separate gate-evidence
artifact the run wrote alongside it. It refuses outright if the run is incomplete. It re-reads
every one of the ten approved *previous-generation* numbers from the document they were originally
published in, rather than trusting the copy the new run carried forward. It re-takes all twelve
checkpoint fingerprints from the files still on disk. It reloads the ten new networks and
recomputes their scores from scratch, requiring exact agreement with what the run recorded. Only
then does it derive the small set of comparisons the design pre-registered, and it writes them
once, to a destination that refuses to be overwritten.

**One structural feature is worth a non-specialist's attention.** The design says that if the run
failed a specific weak check — did every one of the ten trained arms actually lower its own
training objective? — then *no comparison may be published at all*. The program derives that
status **first**, and every comparison field is emitted as `null` unless it passes. That ordering
is not a convenience; it is the thing that stops a partially-successful run from quietly producing
a number someone later quotes.

**4. The mutation sweep, and the one thing it caught in my own tests.** A passing test suite is
not evidence that the tests can fail. So I damaged the analyzer twenty-five different ways, one at
a time, and required the suite to go red for each; plus two deliberately harmless changes that had
to stay green. The whole sweep ran twice with identical verdicts, and the file's fingerprint was
verified unchanged afterwards.

**First run: 24 of 25 caught, both harmless controls correctly surviving — and one survivor.**

The survivor is the interesting part. The analyzer checks that the run record and the plan both
name the code state that exists today. I changed the program so that "the code state that exists
today" was read *out of the run record itself* — a comparison of a thing with itself, which is
exactly the class of non-check this project has a written rule against. **It survived my entire
test file.** The reason is worth stating: both of my tests for that property made the record and
the plan *disagree with each other*, and a self-comparison still notices a disagreement. What a
self-comparison stops noticing is the case where every document agrees with every other document
and none of them matches reality — an old run read by a newer program. I closed it with one test
that makes the identity wrong *everywhere at once*, re-ran that case, and it is now caught: 25 of
25, controls still surviving.

That is the honest version of the session's quality claim: my first draft's tests had a real hole,
the sweep found it, and the fix is committed with the finding written down.

**5. Suites.** 103 focused tests pass in 2.05 s, and again under Python's optimized mode. The full
packet suite is **2,108 tests green in 126.88 s** — the previous 2,005 plus exactly these 103.

### Challenges, and how they were handled

**Knowing the answer before writing the program that computes it.** Codex's report already states
that all ten arms reduced their objective. That is a primitive integrity statement and unavoidable
context. But the *comparison* numbers — how the two sensor suites' scores relate at this larger
network size — are precisely what the pre-registered read exists to constrain. I deliberately did
not open those values while writing the analyzer. Everything the program needed to know about the
record's structure came from the executable's source code, not from the record's contents. This
matters because the whole point of freezing an interpretation in advance is defeated if the
program that applies it is shaped around the numbers it will be applied to.

**Deciding how much the analyzer should re-verify.** The design requires deriving from persisted
primitives; it does not require reopening the trained networks and re-scoring them. I put that in
anyway, on the precedent of the equivalent Stage-1 program, because "the record says X" is not a
check until something outside the record produces X. It costs no training and a few seconds. I
flagged it explicitly to Codex as a decision it may rule against.

**A rule that pushes in two directions.** The design says the previous generation's numbers are
*read, never recomputed* — but also that this analyzer must be a new, separate program. So the
anchor path and the new-arm path do opposite things: new arms are re-scored from their weights,
old arms are re-fetched from the document they were published in and compared field for field.
Getting that backwards is not a hypothetical: an earlier session of this project found exactly
that defect in the Stage-1 analyzer, where recomputed values were compared against values that had
passed through a rounding step, and the program could not have completed the read it existed to
perform.

### Important decisions

1. **The design's instruction to import was read as a positive instruction.** Its invariant R7
   says the two already-approved analysis programs must be imported from and must not be edited.
   The easy reading takes only the prohibition and writes a fresh copy of every small validator
   beside the approved ones. I took the whole sentence: the new program imports its validators,
   and its error type is a subclass of the approved program's, so a single error handler still
   covers both.
2. **The published label has two independent derivations.** The one three-valued summary the read
   is allowed to produce is computed from the raw per-seed differences, and then re-derived by a
   different function from the three integer counts the artifact itself publishes. They must
   agree. The point is that a reader holding only the artifact can check the label themselves.
3. **I did not write a runbook step yet, and said so.** The reproducibility packet's runbook has
   no step covering the rung-2 lane at all. Writing the analyzer's step now would document an
   invocation nobody has authorized. I proposed the honest split — one step for the executable and
   plan, writable today; one for the read, after the review — and handed the call to Codex.
4. **No public log entry.** The playbook's triggers are a finished artifact, a phase close, or
   something genuinely noteworthy. A program that has been written but not yet reviewed is none of
   those, and Codex had already declined to log the raw run for the sound reason that its derived
   read does not exist. The banner is current as of today, so nothing there needed touching either.

### Insights gained

- **Redundancy is not independence, and the test for independence is narrower than it looks.** The
  project already had a written rule that a check needs a source independent of the thing it
  checks. What this session added is the *instrument* for proving that rule is satisfied: make the
  value wrong in every document at once. Two documents disagreeing is a weaker probe, and it is
  the one I reached for first.
- **The same root cause produced two unrelated-looking failures in two days.** A digest published
  for the wrong side of a filter, and a patch applied against an anchor other than the one
  verified. Both are "the object you checked is not the object that travels." Naming the shared
  root is cheaper than fixing each instance twice.
- **Writing the reader after the run is safe only because the interpretation was frozen before
  it.** This session is a small, concrete demonstration of why the project's pre-registration
  discipline is more than paperwork: I could build the program freely, in full knowledge that the
  run succeeded, without being able to shape what it is permitted to say.

### Files created or updated

- `Reproducibility Packet/scripts/analyze_rung2_escalation.py` — **new.** The step-6 read-only
  analyzer, blob `7cf3cc6a…`.
- `Reproducibility Packet/tests/test_rung2_escalation_analysis.py` — **new.** 103 tests, blob
  `a642b3d3…`.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — one appended turn, `+164 / −0`, additions only.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — the monitor's confirmation of Codex's report, `+36 / −0`.
- `agents/Claude/Permanent Instruments.md` — standing lessons 183 and 184 added.
- `agents/Claude/Session Summaries/HumanReport118.md` — this report.
- `agents/Claude/README.md` — workspace index refreshed.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 119.
- `README.md` — **reviewed and approved, not edited.** No running-log entry was added.

### Resource accounting

```text
fits                              0
checkpoints                       0
rollouts                          0
generation runs                   0
pilot / validation / test reads   0
analyzer invocations              0
C7 invocations                    0
```

The only real data this session touched was through the test suite's own synthetic fixtures. The
recomputation tests build a freshly initialized, never-trained network in a temporary directory
and score it on four random examples — that is the only way to give the score comparison a
passing case to sit against, and it opens nothing the run produced.

### Next steps

1. **Codex reviews the analyzer and its tests** at the two blobs above and either approves those
   exact bytes or edits and hands back. Nothing downstream can move until that loop closes.
2. **A separate two-part authorization** would then be required to actually run the analyzer
   against the real result — naming the exact input fingerprints, exactly as the training run's
   authorization did.
3. **Step 7** — both agents review the resulting derived artifact — and only then is the frozen
   interpretation applied jointly. That is the moment this project first learns whether its
   pre-written sentences say anything.
4. The runbook question in decision 3 above is open for Codex.
5. Still forbidden and untouched: any capacity or rung selection, any threshold, any generation,
   any rollout, any reserved-data read, and any statement about the two sensor suites beyond the
   single sentence the frozen table will license.
