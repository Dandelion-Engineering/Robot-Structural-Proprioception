# Progress Report — Claude, Session 96

**Date:** 2026-08-08 08:31 PDT
**Covers:** my Sessions 89–96 (previous report: Session 88)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The last report ended with a *design* for the next measurement — the "capacity sweep," which
trains the same experiment at five different network sizes to find out whether the network
being small is why the first result came out the way it did. Since then that design was
frozen, the program that executes it was written, it went through four more rounds of
adversarial review, and it produced its first output.

Then the first output found something nobody was looking for.

> **The plan our program writes before spending anything — the document that is supposed to
> pin down exactly what will happen — did not actually pin down one of the programs that
> would do the work. The module that grades every answer, and that loads every training
> example, was named nowhere in it. I changed how that module grades, regenerated the plan,
> and the plan came out byte-for-byte identical.**

That hole had been open since the design was written. It is now closed: there is a check
that refuses to plan, and refuses to authorize a run, if the grading module on disk is not
the exact one the approved results were produced with. Codex ruled the finding in, wrote the
repair, and I approved it this session after trying to break it.

The honest other half is the same as last time, and it is getting heavier. **Eight more
sessions, zero simulations, zero models trained.** The lifetime simulation total is still
**278**, where it has sat since early August. The last new scientific numbers this project
produced came out of my Session 84 — twelve of my sessions ago.

---

## The one idea you need: what it means for a plan to "bind" a program

This is the concept the whole report turns on, and it is not complicated once it is named.

Everything expensive in this project is **pre-registered** — written down in advance, in a
document both agents approve, before any of it runs. ([Pre-registration](https://www.cos.io/initiatives/prereg)
is a standard scientific practice: you commit to what you will do and what will count as
success *before* you see the answer, so you cannot quietly change the question after the
fact.) Our version of that document is called the plan. Running "plan mode" costs nothing —
no training, no simulation — and produces a single file describing exactly what the real run
would do: which 42 models get trained, at which sizes, with which random seeds, reading which
data.

For that document to be worth anything, it has to name not only *what* will be done but *which
exact code* will do it. Otherwise you could approve a plan on Monday, quietly change the
program on Tuesday, and run something different on Wednesday under Monday's approval.

The way it names the code is a **fingerprint**. Every file gets run through
[SHA-256](https://en.wikipedia.org/wiki/SHA-2), a function that turns any file into a
64-character string, where changing a single character anywhere in the file changes the
string completely and unpredictably. The plan records those fingerprints. Before any spending
happens, the program re-fingerprints the files on disk and refuses if anything moved.

That machinery was in place. It covered nine files.

**It did not cover the tenth.**

## The finding: the grader was never fingerprinted

The capacity-sweep program does not do everything itself. It borrows two jobs from a module
written earlier in the project, `analyze_dev_fit.py`:

- it **loads** every training example the 42 models will learn from, and
- it **scores** every model's answer — the accuracy number each of the 42 results is
  ultimately judged by.

Those are not peripheral jobs. They are the two ends of the measurement. And that file was in
none of the nine fingerprints. The plan reached its identity in one indirect hop — a different
approved document happens to record it — but *nothing ever compared the two*. A record you
never check is a note in a drawer.

**I did not want to report "the gate would not see it" as an argument, so I measured it.** I
made three changes to the grading module, regenerated the plan after each one, and compared
the bytes. The original was restored afterwards and the restoration verified by fingerprint.

| Change made to the grading module | Did the plan notice? | Did the test suite notice? |
|---|---|---|
| Score computed as the best category instead of the average across categories | **No** — byte-identical plan | 1 test caught it |
| Every training example loaded in reverse order | **No** — byte-identical plan | **None.** All 238 tests passed |
| One word changed in a comment (control) | No — as expected | None — as expected |

The middle row is the one that matters. Reversing the order examples are loaded in is not a
cosmetic change; it changes what each model actually learns from. It sailed through the plan
gate *and* through every behavioural test the project has for that code path.

The first row explains the score in plainer terms. The project's headline accuracy measure is
[macro-F1](https://en.wikipedia.org/wiki/F-score), which averages performance across all four
fault categories so that doing well on the common ones cannot hide doing badly on the rare
ones. Replacing that average with "whichever category you did best on" would inflate every
number in the study. The plan would not have blinked.

There was one partial protection, and I want to be accurate about it rather than dramatic. The
sweep begins by re-training two models it already has, to check the new code reproduces the
old results exactly. That check would have caught the reversed-loading change — but only
*after* spending two of the 42 training runs on it, and it would not have caught the scoring
change at all, because it compares model weights rather than scores.

## The repair, and why the obvious version of it was wrong

The obvious fix is to add the grading module as a tenth fingerprint. That fix is not available.
An existing rule — one both agents approved months of sessions ago — requires the sweep's
fingerprint list to be *exactly* the eight files the original models were trained with, plus
exactly one new file: the sweep program itself. A tenth entry makes the program refuse its own
identity.

So the repair goes beside the list rather than inside it. The approved results document
already records the grading module's fingerprint; the plan already binds that document. The
new check simply *compares those two things* — the fingerprint the approved document recorded
against the fingerprint of the module actually loaded — and refuses if they differ. It runs
once when the plan is written and again when a real run is authorized. Nothing about the
existing rule changes.

I recommended that shape; Codex ruled the finding in, implemented it, and handed it back. This
session I approved it unchanged, after checking the things I would not take on trust: that the
check sits above every point where the program could spend anything, that the two fingerprints
being compared are produced by the same function rather than by two copies of a convention
that happen to agree today, and that the file-count rule really is untouched.

## What else these eight sessions did

Briefly, because the finding above is the story:

- **Sessions 89–91** finished tearing apart the sweep design. Three more real defects,
  including one I want to name because it is the same shape as the big one: the design claimed
  that re-using an authorization would be "recorded rather than silently presented as a new
  authorization," and there was no mechanism behind that sentence. Two runs under the same
  label would write into two unrelated directories and nothing would notice. The design was
  frozen on the fifth round.
- **Session 92** wrote the program and its tests. Notably, my first attempt at the tool I use
  to check my own tests was itself broken and reported false results; the corrected version
  found five real gaps, four of them in tests I had just written.
- **Sessions 93–94** were two more review rounds, six defects from Codex and three from me,
  all real, all repaired. The loop closed.
- **Session 95** ran the plan for the first time, audited it against 59 independent checks
  rebuilt from the frozen design rather than from the program — and found the hole above.

## The tool I keep leaning on, and why

Nearly every defect above was found the same way: by
[mutation testing](https://en.wikipedia.org/wiki/Mutation_testing). The idea is simple and a
little adversarial. Tests are supposed to fail when the code is wrong — so deliberately break
the code, in a specific realistic way, and check that some test actually goes red. If nothing
goes red, the tests were never checking that thing; they were only keeping you company.

Every sweep I run includes at least one **negative control** — a change that *should* be
invisible, like rewording a comment. If a control comes back "caught," the harness is broken
rather than the code, and the whole run is worthless. That is not hypothetical caution: my
first harness in Session 92 failed exactly that way.

## The small thing this session that is actually a Dandelion standard

My review of Codex's repair found two things its tests did not pin down. Neither is a live
defect — the code is correct — so I changed no program code and added tests instead. One is
worth explaining because it is about our own promise rather than about this experiment.

Windows and Unix mark the end of a line
[differently](https://en.wikipedia.org/wiki/Newline): Windows uses two characters, Unix one.
Git converts between them when files are checked out, and this repository is configured to do
exactly that. So the same file has different raw bytes on this machine than it will on a
stranger's fresh copy — and therefore a different naive fingerprint.

Our fingerprinting function already handles this: it normalizes line endings before hashing,
so the fingerprint describes the *document* rather than the copy. Codex used the correct
function. But nothing in the test suite would have noticed if someone later replaced it with
the naive one — because on this machine the two agree. On a fresh Windows copy they do not:
I measured the divergence. The naive version would refuse a perfectly legitimate plan on
every clone somebody else makes.

That matters more than it sounds like, because the Reproducibility Packet's entire promise is
that a stranger can copy it to a clean machine and re-run our result without contacting us.
A check that only works on our computer quietly breaks that promise. The new test materializes
the file the way a fresh clone would and asserts the check still accepts it.

## What is working

- **The adversarial review process keeps finding real things, and it found this one before any
  money was spent.** Every round in this stretch found a genuine defect. Nothing was
  ceremonial.
- **Plan mode costs nothing, which is why this was cheap.** Regenerating the plan is free, so
  discovering a flaw in it costs one session rather than 42 training runs.
- **The measurement discipline holds.** I did not report "the gate would miss this" as an
  opinion. I mutated the code and compared bytes, with controls, with the original restored
  and the restoration verified.

## What is not working

- **The rate.** Twelve of my sessions have now passed since the project last produced a new
  scientific number. Eight of them are in this report. Everything in that time was
  infrastructure and review — real, load-bearing infrastructure, but not science.
- **I said last time I would name where the cost stops being obviously worth it, so here it
  is.** The finding this stretch produced (the unbound grader) is exactly the kind of thing
  that justifies the process — it would have invalidated all 42 results and nobody would have
  known. The 2-of-8 coverage gaps I found this session are much smaller, and they are the
  signal I am watching. **If the next round finds only that shape again, I will say the loop
  has reached diminishing returns rather than run another one on principle.** I want that
  written down before the round rather than after it.
- **Nothing is blocked on you.** The one open item in `director_requests.md` is still entry 1,
  the Claim Sheet review, which is explicitly non-blocking and has been since Phase 1.

## The verification artifact

No update. The Slot 8 artifact — the hands-on thing that will let you check the result
yourself — has not moved this stretch, and I am not going to manufacture progress on it. It
is paced to arrive with the results it is meant to let you verify.

## What happens next

1. Codex reviews and approves the two tests I added. If it approves them unchanged, the
   program is closed at a state both agents have signed.
2. **One free re-plan.** The repair changed the sweep program, which changed its fingerprint,
   which means the existing plan is now correctly rejected as "written by a different code
   state." A new plan gets generated — still zero training runs — and both agents review its
   exact bytes.
3. **Then, and only then, a separate joint authorization to actually spend the 42 training
   runs.** That authorization does not exist yet and cannot be implied by anything above.
4. After the runs, a read-only analysis script turns the 42 results into the answer to the
   question this whole stretch has been building toward: **does the comparison between the
   two sensor suites change as the network gets bigger?**

Still blocked, unchanged: every capacity training run, every reserved-data read (pilot,
validation and test remain entirely untouched), the final configuration freeze, and every
confirmatory claim.

— Claude
