# Claude — Human Report, Session 95

**Date and time:** 2026-08-08 04:22 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Plan artifacts added to the packet: 0. Data generated: 0. Pilot / validation / test reads: 0.** The plan runs I made for verification read no data root at all. The full packet test suite reads two approved development documents (`dev_fit_result.json`, `dev_fit_analysis.json`) through its fixtures; no delivered observation payload and no approved `.pt` checkpoint was opened.

**Progress-report session:** no. My next regular progress report is Session 96; no phase transition and no Claim-Sheet amendment occurred this session.

---

## Summary in one paragraph

Codex closed the executable review loop last session and then ran the first real act it
unlocked: it produced the project's official **plan** for the capacity sweep — a single
13,786-byte document that names, in advance and in full, every one of the 42 model fits the
experiment is allowed to make, every file it is allowed to write, and the exact version of
every piece of code that will produce the numbers. Producing that plan costs nothing; its
whole purpose is to be checked before anything expensive happens. My job this session was the
independent second read of it. I rebuilt every claim the document makes from sources outside
the program that wrote it, and all 59 of my checks passed; I also reproduced the document
twice from scratch and confirmed it is byte-for-byte what the approved program emits, so it
was not edited after it was written. Then I found one thing the plan does *not* bind, and
measured that the gap is real rather than theoretical: the module that decides which training
examples every arm sees and computes every arm's headline score is not covered by any check
the program itself runs, and I demonstrated that changing it leaves the plan's bytes
identical. I approved everything I verified but deliberately withheld the approval that would
close this gate, and handed the ruling to Codex. Nothing was executed.

---

## What a "plan" is, and why it gets its own review gate

The capacity sweep is the most expensive single action this project has queued: 42 model fits,
each irreversible in the sense that it consumes real compute and writes real files. The design
we froze earlier does not let that happen in one step. It splits it into five separate gates,
each of which has to be passed and reviewed on its own:

1. freeze the design — done;
2. build the program and its tests, and review them to a state both agents approve — done last
   session;
3. **run the program in "plan mode", which spends nothing, and review the document it writes —
   this session;**
4. a separate joint authorization to actually spend the 42 fits — not yet;
5. review the exact result, and only then apply the pre-registered interpretation.

Plan mode exists so that the whole shape of the experiment can be argued about while it is
still free to change. The document it writes is a promise: *these* 42 fits, at *these* network
sizes, with *these* random seeds, writing to *these* file names, using code with *these* exact
fingerprints. When gate 4 eventually opens, the authorization will name this document by its
cryptographic digest, and the program will refuse to run against any other. So the plan is the
last cheap place to catch a problem, and the first expensive one to carry a problem forward.

---

## How I read it

The rule I hold myself to on a second read is that I must not check the document against the
program that produced it, because a program and its own output agree by construction. Every
expectation has to come from somewhere else. So I rebuilt each claim from the frozen design's
own text, from the approved records of the earlier ten fits, from the assignment and
configuration files, and from the source files on disk — and wrote it as a standalone audit
script that does not import the sweep program at all.

Fifty-nine checks, all passing. In plain terms, I confirmed that:

- the document is exactly the bytes Codex published, in strict canonical form, pure ASCII,
  with no stray line endings and no hidden numbers that JSON cannot represent;
- every fingerprint it records — of the frozen design, of the approved earlier results, of the
  data assignment, of the draft configuration — recomputes correctly from the actual file it
  claims to describe, rather than merely being internally consistent;
- the experiment's shape is right: ten already-completed runs reused and marked read-only, forty
  genuinely new runs covering four network widths times two sensor suites times five random
  seeds with no duplicates and none secretly re-doing the already-completed size, plus the two
  special "did we break anything" runs;
- those two special runs point at exactly the right earlier results to compare against;
- all 44 files it promises to write live inside one folder named after this run, none of them
  escape upward, and no path on this machine — no drive letter, no username, no folder name —
  is written into the document anywhere;
- the budget is 42 fits and 42 saved models and zero of everything else, and 42 is the sum of
  the arms actually listed rather than a number typed in;
- the training recipe is character-for-character the same recipe the earlier approved fits
  used, including the two carefully derived time windows;
- the network sizes it reports match the table in the frozen design at every width;
- it emits no conclusion, no verdict, no recommendation of any kind — which the design
  explicitly forbids at this stage;
- and the two statistics it carries from the earlier analysis resolve through the field names
  the document itself supplies, so I retrieved them rather than compared them to a number I
  remembered.

Then I ran the program in plan mode twice, into two different scratch folders, and compared.
Both, and the published document, are byte-identical. That confirms two separate things: the
design's requirement that the document not depend on where it is written is genuinely met, and
the published document really is the program's output rather than something edited afterwards.

**One small correction.** The command Codex published for reproducing the plan does not run as
written — it names the wrong starting directory for the way the program is packaged. The
document itself is unaffected, but a reproducibility packet whose published command fails is a
problem, so I worked out the invocation that does work and recorded it. Per our convention I
did not edit Codex's report; corrections travel forwards into the next document that needs
them.

---

## What I found: the module nothing checks

The frozen design says two things that turn out not to meet in the middle.

Section 3 requires the sweep program to **import** its scoring function from an existing,
separately approved script (`analyze_dev_fit.py`) rather than write its own — a good rule,
because a second definition of the headline metric in one project is a second version of the
quantity the whole study is about. Section 7.1 requires the plan to record the fingerprint of
"the network module and every module that fits or scores the arms."

The program in fact leans on that script for three things: the scoring function, the list of
fault categories the scoring is over, and — this is the load-bearing one — the routine that
**loads the training examples every one of the 42 arms is fitted on**. The plan records nine
code fingerprints. That script is not one of them. Its digest, and even its name, appear
nowhere in the document's 13,786 bytes.

The information is not actually missing. The plan does record the fingerprint of the earlier
*analysis artifact*, and that artifact in turn records the script's fingerprint — which is
identical to the script on disk today. So the chain exists, one hop away, through a document
the plan already binds. What is missing is any moment at which the program compares the two.

I did not want to assert "the gate would not notice" without measuring it, so I built a small
harness that changes the script, regenerates the plan, and compares the bytes, restoring the
original afterwards and verifying the restoration by digest. Three cases:

| change made to the scoring/loading script | did the plan change? | did the tests catch it? |
|---|---|---|
| headline score changed from the average of the per-category scores to the maximum | **no — byte-identical** | one test caught it |
| each suite's training rows loaded in reverse order | **no — byte-identical** | **nothing caught it** |
| one word changed in a comment (control) | no — byte-identical | nothing caught it (correct) |

The first change would move the reported score of all 42 arms. The second would fit every arm
on a different batch of data. Neither is visible to the plan, and therefore neither is visible
to the check that gate 4 will run before spending the fits.

One methodological note, because it nearly produced a wrong answer: there is a test in the
suite that fails for *any* byte change to that script, including a comment. Left in, it reports
every mutation as caught and the measurement says nothing. Its own docstring warns about this —
a warning written by an earlier session of mine after exactly that mistake — so I excluded it
and confirmed the exclusion took effect by counting the collected tests, which the same
docstring also warns about. The control surviving is what tells me the harness is measuring
something real.

**I have been careful not to inflate this.** There is genuine residual protection. The design
includes an equivalence check that re-runs two of the already-completed fits through the new
code path and demands bit-identical results before the forty new ones start. That check *would*
catch the data-loading change — but only after spending two of the 42 fits, and it would not
catch the scoring change at all, because it compares model weights and training losses, and the
headline score is neither.

---

## The judgment, and why I did not simply approve

The document's bytes are correct. Everything I could check passed. But the gap is in the
*binding the plan exists to provide*, and closing this gate is precisely what turns the
document into the thing a spending authorization will name. So approving it would mean signing
off on an identity guarantee I had just demonstrated has a hole in it.

Blocking the plan on its own would also be wrong, because the plan faithfully reflects a
program both of us approved; the gap is upstream of the document. So I did the thing that fits
the actual situation: I explicitly approved everything I verified, explicitly withheld the
approval that closes the gate, and handed Codex the ruling with two named repairs and my
recommendation.

My recommended repair is small and, importantly, does not collide with an existing invariant.
The obvious fix — add a tenth fingerprint — is actually forbidden by one of the program's own
rules, which permits exactly one addition to the historical set. The fix that works instead is
a comparison: check the fingerprint already recorded in the artifact the plan already binds
against the script actually being imported, and refuse if they differ. That adds nothing to the
fingerprint list, leaves the existing rule untouched, and converts a paper guarantee into a
mechanism. Its cost is one free regeneration of the plan.

I also wrote down where this contradicts something I said last session. In Session 94 I
recorded a rule of thumb that after the plan exists, a cosmetic-looking gap in this file should
be carried forward rather than repaired. I do not think that covers this one, and rather than
quietly exempting myself I stated the difference: last session's item was a duplicated piece of
text whose two copies agreed; this one is invisible to the authorization gate and one of its
two failure modes survives every behavioural test in the relevant files. If Codex judges
otherwise, I said explicitly that I will take the ruling and approve rather than trade another
round — but that the gap would then have to be carried as a numbered limitation for the
technical report, since the frozen design cannot be amended to record it.

---

## Verification

```text
full packet test suite        1,755 passed in 135.05 s
independent plan audit        59 / 59 checks passed (rebuilt from the design, the approved
                              ledger and analysis, the assignment, the draft config and the
                              tracked sources -- the sweep module is never imported)
plan reproduction             2 scratch destinations + the published artifact, all three
                              byte-identical at 740d5db9..., cmp clean
mutation harness              3 cases, original restored in a finally and the restore
                              verified by digest, tripwire deselection confirmed by the
                              collected count (239 -> 238 + 1 deselected), negative control
                              SURVIVED
production blobs unchanged    capacity_sweep.py 937ab73c, test_capacity_sweep.py 0a8f8b71,
                              design b45efa47, dev_fit_trainer caa00418, dev_fit_contract
                              bd2c0d08, attribution_net c4fa3c63, analyze_dev_fit 31381b18,
                              dev_fit_result d4cefb61, dev_fit_analysis 0d00b5ca, plan
                              d2584d28, packet README eb4a58e4
git status                    clean before and after every probe
no sweep execution            no capacity_sweep_result.json, no capacity_sweep_equivalence
                              .json, no .pt outside results/dev_fit; config/config.json
                              still absent
fits 0 | checkpoints 0 | rollouts 0 | generation 0 | packet plan artifacts still 1
timestamp                     read from the shell clock immediately before the transcript
                              write, not estimated while drafting
```

---

## Transcript hard gate

One append-only turn, six gates passed:

```text
pre-write     1,626,311 B   26,076 lines   sha256 f2781d5999cb24a2...
post-write    1,639,880 B   26,289 lines   sha256 f4cc6efc14ff259b...
header        line 26,078, unique, after the 26,076-line boundary
numstat       +213 / -0
last agent    Claude
```

The pre-write digest equals the post-write digest Codex published at the end of its Session 94,
which independently confirms the transcript was untouched between sessions. **Monitoring
thread: no note added, because there is no recurrence** — Codex's Session-94 commit touches the
transcript as a single tail hunk of +158/-0 and does not touch the monitoring file at all,
verified at the git level rather than assumed.

---

## Files created or updated

Created:

- `agents/Claude/Session Summaries/HumanReport95.md` — this report.

Updated:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — one append-only turn: the 59-check audit, the reproduction measurement, the invocation
  correction, finding AT with its mutation table, and the withheld gate approval.
- `agents/Claude/README.md` — Session-95 navigation.
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten resume state.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json` — the artifact under
  review; I did not edit it, and an edit would have been the wrong instrument here.
- `Reproducibility Packet/scripts/utils/capacity_sweep.py`, `tests/test_capacity_sweep.py`,
  `protocol/capacity-escalation-v0.1.md`, `scripts/analyze_dev_fit.py`, both READMEs,
  `.gitattributes`, `.gitignore`.
- Root `README.md` — heartbeat checked, nothing added and the banner not advanced. Codex
  already logged the executable closure and the plan in its Session 94, and my session opened a
  review round rather than finishing anything a stranger can see. **Eighth consecutive session
  of mine that correctly added nothing.**

---

## Decisions I made this session

1. **Audit from outside the producer.** Every expectation rebuilt from the design, the approved
   records or the tracked sources; the sweep module is never imported by the audit script.
2. **Measure the reproduction rather than trust the digest.** Two plan runs into two scratch
   destinations; this is what distinguishes "the digest matches" from "the program produces
   these bytes".
3. **Raise AT, and measure it before raising it.** A claim that a gate cannot see something is
   worth nothing until the mutation is run and the bytes compared.
4. **State the residual coverage honestly.** The equivalence check does cover the data-loading
   half, at a cost of two fits. Saying so is what keeps the finding at its real size.
5. **Withhold the gate-closing approval rather than block the artifact.** The document is
   faithful; the gap is upstream of it. Blocking the plan alone would be aimed at the wrong
   object.
6. **Record where this contradicts my own Session-94 rule of thumb**, so Codex can overrule the
   reasoning and not only the code.
7. **No public log entry.** An open review round is work in progress, which the lean log is
   explicitly not for.

---

## Cross-review

I read Codex's `HumanReport94.md` in full, both of its Session-94 transcript turns, and the
artifact it produced. Its independent audit of the plan is accurate as far as it goes and its
severity judgment on my Session-94 finding matches mine. Two corrections travel forward: the
published reproduction command does not run as written, and its audit — like mine, at first —
treated the nine code fingerprints as complete when the design's own words ask for the module
that scores the arms. Its bookkeeping correction of my Session-94 round count is accepted: my
report said round three and my transcript turn said round four for the same state, and the turn
was right.

---

## Next steps

1. Codex rules on AT: the sibling identity check, the governance alternative, or a disclosure.
2. Under either ruling, Step 3 closes with both agents approving the same plan bytes — the
   current ones if AT is ruled disclosed, or a regenerated document if the check goes in.
3. Step 4 remains a separate joint authorization naming the approved plan's digest. No fit may
   run before it.
4. The read-only analysis script, every later-role read, Stage 2, the final configuration
   freeze, generation and all rollouts remain separately blocked.

— Claude
