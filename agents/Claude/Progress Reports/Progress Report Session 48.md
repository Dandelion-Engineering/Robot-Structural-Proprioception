# Progress Report — Claude, Session 48

**Date:** 2026-07-30
**Covers:** my Sessions 41–48 (previous report: Session 40)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

My last report to you ended on an uncomfortable note. I told you that eight
sessions had gone by, that we had found eight separate faults in our own
measuring instrument, and that we still had not measured anything.

Since then: the instrument is finished, both agents have signed off on it, and
**as of today it has taken its first measurement.** Two of them, actually. One
of them is a genuinely nice result that I did not expect to get for free.

I also owe you a straight answer about pace, and about the fact that the
project's central experiment still has not started. Both are further down, and
neither is hidden.

---

## A one-paragraph refresher

We have a simulated two-link arm. It can break in three ways: a link goes
**soft**, a motor goes **weak**, or a sensor starts **lying**. The question is
whether four [strain gauges](https://en.wikipedia.org/wiki/Strain_gauge) — small
sensors that measure how much the arm's own body is bending — let the arm tell
those three cases apart better than a conventional sensor kit can, and whether
telling them apart better leads to controlling itself better. The arm gives
itself a small deliberate nudge and we read how the gauges answer. Damage should
change the answer. Everything depends on whether the change from damage is
bigger than the change from everything else.

---

## What "the instrument" was, and why it took so long

Most of the last sixteen sessions went into a single document and the code that
executes it. The document is called **Protocol P**. It is a
[pre-registration](https://www.cos.io/initiatives/prereg): a written commitment,
made *before* the measurement, that says exactly what we will measure, how, with
what settings, and — critically — what result would count as success, failure,
or "we can't tell."

Pre-registration exists because of a well-documented problem in science: if you
decide what counts as a good result *after* you see the data, you will find a
good result whether or not one is there. Writing it down first removes that
freedom from yourself on purpose.

The reason ours took seven rounds of back-and-forth between me and Codex is that
**making a protocol executable is what reveals its defects.** This turned out to
be the single most useful working discovery of the whole project. Every time one
of us sat down to actually *build* what the document described, the building
found something that reading it had not: a term used to mean two different
things, a setting that looked pinned but was computed somewhere else, a
measurement whose starting point was never specified. Reviewing the document
found almost nothing. Executing it found everything.

Protocol P was jointly approved at my Session 43. The specification loop is
closed.

---

## The two measurements

### 1. One run reproduces exactly, from committed files

This one is my favourite result of the last eight sessions, and it was close to
free.

We had generated a batch of simulated runs earlier in the project. The question
nobody had asked: if we take the recorded inputs and run them again today, do we
get **byte-for-byte** the same output?

We built a checker for it. The answer is yes — one run, both the physics record
(20 measured quantities) and the sensor record (38), reproduce exactly.

Why this matters more than it sounds: the check compares today's output against
a file created *before* we made a set of changes to the generator. So passing it
does not only prove the simulation is deterministic. It proves **none of the
changes we made in between disturbed the ordinary path**. We got a regression
test for the whole intervening period out of a check we built for a different
reason.

The honest boundary, which I have insisted appear everywhere this result is
quoted: **it is one run, in one sensor configuration.** We did not regenerate the
whole dataset and we are making no dataset-wide claim.

### 2. Stage 0 — the noise floor, measured today

The first stage of Protocol P asks a narrow question: **how much does our answer
move when nothing is wrong at all?**

If you nudge the arm twice, with nothing broken either time, you do not get
identical readings — sensors have noise, drift, temperature sensitivity,
rounding. So before asking "did damage change the reading," you have to know how
much the reading moves on its own. That is the noise floor. Any damage signal
smaller than it is invisible.

Stage 0 measures this with **no simulated physics at all** — pure sensor
behaviour, 100 paired comparisons. It costs nothing to run and needs no
special hardware or data, which means anyone who downloads our packet can
reproduce it.

The result, in the units the project uses
([microstrain](https://en.wikipedia.org/wiki/Deformation_(engineering)), a
measure of how much a material is stretched):

```text
typical spread (mean)   0.279
the reported figure     0.401     (the 95th percentile — only 5 in 100 exceed it)
```

There was an independent way to check this, and it is the part worth explaining.
Earlier I had measured the same kind of variation using *real simulated physics*
— taking one healthy run and re-reading it through different sensor draws. That
gave four numbers, one per test condition: **0.318, 0.356, 0.385, 0.425**.

Stage 0's purely synthetic 0.401 falls inside that range. Two very different
routes to the same quantity agree. That is real corroboration.

**And here is the qualification I put on the record before anyone quotes it.**
0.401 is not sitting comfortably in the middle of 0.318–0.425. It is **above
three of those four numbers**, with about 6% of headroom to the top. "Inside the
range" is true, and it is exactly what we committed to checking. "Agrees with
the physics-based result" would be a stronger claim than the numbers support,
and I would rather say that myself now than have a reviewer say it later.

---

## What was unexpected

**The reviews kept finding real things — including in each other's fixes.**

The pattern over these eight sessions was not "one agent writes, the other
rubber-stamps." It went: I hand off work, Codex finds a genuine defect and fixes
it, I re-review the fix and find a *second* defect of the same kind in it, Codex
re-reviews my correction and finds two defects in my *evidence*. Three full
rounds on one script.

Today I did the last of those re-reviews, and I want to describe how, because
it is the part I would want you to check me on.

Codex told me two of my tests were unsound. I did not take that on faith. I
rebuilt what we call a mutation sweep: deliberately break the production code in
one specific way, then check whether the test actually turns red. Five cases.

Two of them are the finding:

```text
break the security check  ->  Codex's rewritten test   turns RED    (catches it)
break the security check  ->  my original test         stays GREEN  (blind to it)
```

Same injected fault, same command. Codex's version catches it; mine did not.
That is Codex's criticism **demonstrated rather than argued** — and it is the
right way round, because my test had been *reimplementing* the thing it was
supposed to be checking, so it was only ever agreeing with itself. What stings
slightly is that the warning against exactly that mistake was already written in
my own notes, a few lines above the code where I made it.

I also audited one line Codex added and found the stated reason for it was
wrong — the line is harmless and I kept it, but it does not do what the review
said it does. I recorded that so it does not end up in the final report as a
claim about a safety check that the code does not actually perform.

**This is what I would point to if you asked whether the two-agent review is
doing real work.** It is slow. It is also catching things that would otherwise
have reached the final write-up as false statements.

---

## What's working

- **The pre-registration is done and locked.** Protocol P is a single file with a
  fingerprint; three separate automated tests will fail loudly if even one byte
  of it changes. Nobody can quietly adjust the goalposts, including us.
- **The reproducibility packet is being built as we go**, not assembled at the
  end. Scripts land inside it already portable.
- **Cost discipline held.** Protocol P has a strict budget of expensive
  simulation runs. Across eight sessions we have spent **exactly one**, the one
  that was authorized. Stage 0 cost zero. Every defect described above was found
  without spending budget, by dry-running the analysis before paying for data.

---

## What isn't working

**1. The central experiment still has not started.** Stages A, B, and C — the
ones that actually test whether strain gauges help — are unbuilt and
unauthorized. Stage 0 measures the noise floor; it deliberately decides nothing.

**2. Pace, stated plainly.** This is my second consecutive eight-session report
where the headline experiment did not run. I believe the work was necessary —
every round found something real, and the alternative was measuring with a
broken instrument and finding out afterwards. But I am not going to dress up two
reports in a row of instrument work as fast progress. It isn't.

If it helps calibrate: what is left before the real measurement is the Stage
A/B/C driver, a written amendment we have already agreed on in substance, and a
regeneration of the dataset. That is a handful of sessions, not another sixteen.

**3. The dataset has to be thrown away and rebuilt.** We identified a change to
the experiment design (an amendment we call A2). Because of how the random
seeds are laid out, changing one setting shifts every seed after it — so the
3.9 GB of runs we generated are superseded. They stay on record as a
pre-amendment set, and we regenerate from zero. Nothing is lost scientifically;
it is compute we will spend again.

**4. The odds are not good, and I am not going to soften that.** Our best
current projection says that at the *milder* damage level we plan to test, the
strain signal is likely **too small to detect** — it fails by a wide margin. At
the more severe level it clears the bar by only about 1.1×, and that estimate
was computed with an inflated signal against a deflated threshold, both errors
in the hypothesis's favour.

So a negative result is a live possibility, maybe the likely one. That was
always a legitimate outcome for this project — a clean "no, this doesn't help
enough" is worth publishing, and the pre-registration is what makes it
publishable rather than a disappointment we quietly reframe. Stage C is what
settles it.

**5. Still waiting on you, and still not blocked.** `director_requests.md`
entry 1 — the Claim Sheet review — is open. It is non-blocking by design and we
have kept working. Nothing else needs you.

---

## Verification artifact

No change to report. The Slot 8 artifact — the hands-on thing you will use to
check the result yourself — is still specified and not yet built. It is paced to
follow the real measurement, since what it needs to show depends on what the
measurement finds. I am not manufacturing an update on it.

---

## What's next

1. Codex reviews today's Stage 0 result.
2. I write the packet instructions for it — worth noting that Stage 0, unlike
   our other check, **can** be run by an outside reader on a clean machine with
   no data and no simulator. That is a good thing to be able to say.
3. Build the Stage A/B/C driver — the real measurement — against a checklist
   Codex has already written.
4. Write the A2 amendment, regenerate the dataset from zero, re-audit.
5. Then the models, the calibration, the config freeze, and the confirmatory
   comparison.

---

*Claude, Session 48 — 2026-07-30 11:43 PDT*
