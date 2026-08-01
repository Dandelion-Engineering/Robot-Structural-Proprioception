# Progress Report — Claude, Session 56

**Date:** 2026-08-01
**Covers:** my Sessions 49–56 (previous report: Session 48)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

Eight sessions ago I told you the measuring instrument was finished and had
taken its first measurement. That was true, and it is still true — but that
measurement was the *smallest* one in the plan, the one that needs no physics at
all.

Since then, all eight of my sessions have gone into building and checking the
program that runs the **real** measurement — the one that decides whether this
project's central idea is testable. That program now exists, both agents have
signed off on it, and it has run **zero** of its 168 simulations.

I want to be straight with you about that number, because "we built a program
and did not run it" is a sentence that should make a director suspicious. The
honest defence is in the middle of this report: across these eight sessions,
three separate review rounds found real defects in that program, and the worst
of them was sitting in code that 906 automated tests were passing on. Every one
of those defects would have produced a finished-looking result that was quietly
wrong. That is the case for the pace, and if you don't find it convincing,
you should say so — it is your call and not mine.

---

## A one-paragraph refresher

We have a simulated two-link arm. It can break in three ways: a link goes
**soft**, a motor goes **weak**, or a sensor starts **lying**. The question is
whether four [strain gauges](https://en.wikipedia.org/wiki/Strain_gauge) — small
sensors that measure how much the arm's own body is bending — let the arm tell
those three cases apart better than a conventional sensor kit can, and whether
telling them apart better leads to controlling itself better. The arm gives
itself a small deliberate nudge and we read how the gauges answer. Damage should
change the answer. Everything depends on whether the change caused by damage is
bigger than the change caused by everything else.

---

## Where the project stands right now

The whole project is gated on one question we have not yet answered: **is the
damage signal even big enough to see?** If it isn't, then no amount of clever
machine learning downstream matters, and the honest thing to do is say so.

We wrote a pre-registered plan for answering it, called Protocol P. A
[pre-registration](https://www.cos.io/initiatives/prereg) is a public commitment,
made *before* you look, to exactly what you will measure and exactly what each
possible answer will mean. It is what stops a researcher from running twenty
variations and reporting the flattering one. Ours is a 55,000-character document
that both agents approved, and it is frozen — we have not edited it in fourteen
sessions.

The plan has four stages:

| Stage | What it measures | Simulations | Status |
|---|---|---:|---|
| 0 | How much two identical healthy arms differ purely because their *sensors* differ | 0 | **done**, Session 48 |
| A | Nine candidate "nudge" strengths, in four situations, to pick the best one | 108 | not run |
| B | How the signal falls off as the damage gets milder | 40 | not run |
| C | The baseline: how much two *undamaged* arms differ, which is the bar the damage signal has to clear | 32 | not run |

Stages A, B and C are one program. That program is what these eight sessions
built. It totals 168 simulations rather than 180 because twelve of its
measurements are reused — more on that below, because it is the kind of detail
that looks like a discrepancy if nobody explains it.

---

## What has been done since the last report

Roughly in order:

**Sessions 49–50 — checking the first measurement, and checking the checker.**
I verified the Stage 0 result and found something worth knowing: the
cryptographic fingerprint we attach to each result certifies *what went into*
the run, not what came out of it. I proved this the blunt way — I edited a
result value in memory, left the inputs alone, and the fingerprint still
validated. That is not a flaw; it is just not what people assume a fingerprint
does. It now says so in writing, in three places, so that no future sentence of
ours claims the fingerprint "verifies the numbers."

I also found a smaller thing that I think is the more interesting one. Codex had
published a correction to a claim in our public log. The correction was right.
But the claim it withdrew had been published *twice*, and the correction only
named one of them — so a reader who stopped one entry earlier would carry away a
claim we had already retracted. A correction is an artifact, and it inherits
every failure mode an artifact has, including the one it was written to fix.

**Session 51 — building the construction layer.** The part of the program that
builds each simulation's *request* and refuses a wrong one before it runs. 130
new automated checks. I then deliberately damaged my own new code 16 different
ways to see which damage the tests would catch; 15 were caught, and the one that
escaped revealed a real hole in tests I had written that same session.

**Sessions 52–53 — reviewing, and one dry run.** Codex reviewed my work and
blocked it on two findings, both of which I reproduced and both of which were
real. I reviewed its repair and found five guards it had added that no test
actually exercised.

Then I did something cheap that turned out to matter: before writing the program
that executes the plan, I built the *entire* plan once, on paper, in about two
seconds of computer time. That is where the 180-versus-168 problem surfaced.
Every test we had reasoned about one simulation at a time; nothing had ever
looked at the whole set at once. Questions about a whole set — total cost,
duplicates, collisions — are invisible to tests that look at one item, and they
are exactly the questions a program like this gets wrong.

**Sessions 54–55 — building the executor, and being caught.** I wrote the
program, plus 156 automated checks, and handed it over. Codex blocked it on
three findings. **All three were real, and I reproduced every one of them before
changing a line.** They were:

1. If a candidate nudge strength failed a safety check partway through, the
   program threw away every simulation it had already spent on that candidate —
   and then crashed because its own bookkeeping no longer added up. In the case
   I reproduced, 73 simulations were run and all 73 were discarded.
2. The program computed a full safety report for every simulation in all three
   stages, and then *used* it in only one of them. The safety verdict for the
   other two was measured and dropped on the floor. Worse: the reused verdict
   feeds the single most important number in the whole protocol — the baseline
   that everything else is compared against. A damaged arm could have been used
   to build the "undamaged" baseline, and the output would have looked clean.
3. None of that safety evidence was written into the saved result, so no reader
   could have audited either problem from the file afterwards.

**The fact I keep coming back to is this: our full test suite — 906 checks —
was green while two of those three defects were live.** They are not subtle
once pointed at. They were invisible to 156 tests written by me, in the same
session, about the same code. Codex found them by driving the whole program end
to end through states my tests never put it in.

**Session 56 — this one.** Codex approved the corrected program. I then added
the last two pieces of pre-execution work, and found one more thing by accident,
which I'll get to.

---

## What was found that wasn't expected

**A check that cannot fail looks exactly like a check that passes.**

This is the finding I would highlight from this session, because it is the
cleanest example of a pattern that has now recurred four times.

The pre-registration insists that damage must start at a specific moment —
one second into the run — and it says why: an earlier version of our code
accidentally started the damage at the very beginning instead, which meant we
were measuring an arm that had *always* been broken rather than one that broke
partway through. Every safety check still passed, with a wide margin. The result
would have looked completely normal.

So the plan contains a guard: build the damage request, then compare it against
what the plan says it should be. That guard exists in our code. It has tests. It
passes.

It also cannot fail. It compares the thing that was built against a fresh copy
built from *the same inputs by the same function* — so no possible input makes
the two disagree. It is a mirror held up to a mirror.

This session I gave that comparison a second, independent source: a small
function that reads the damage-start time out of the plan document itself, at
the moment of the check, rather than accepting it from whoever is calling. Now
the two sides of the comparison come from different places, and the comparison
can fail. I demonstrated both halves in one run: I built a request with the
damage starting at the wrong moment, showed the old check accepting it, and
showed the new check refusing it.

The pre-registration actually named this function, and its exact form, back when
it was written. It had simply never been implemented under that name — the
behaviour had been split across two other functions. Names in a pre-registration
are part of what was promised, so it now exists as promised.

**The other unexpected thing was smaller and dumber, and I found it by looking
rather than by reasoning.** I ran the program and read its output file, and it
contained the full path of the computer that produced it —
`C:\Users\cresp\...`. That is a machine fingerprint inside a scientific result:
two people running the identical analysis would get files that differ, and the
file would advertise a directory structure on your desktop. The neighbouring
Stage 0 result has no such path. Fixed, and it now records
`config/draft-config-v0.1.json` — which loses nothing, because the file that
matters is identified in the same block by its cryptographic hash.

---

## What's working

- **Adversarial review between the two agents is working, and it is not
  ceremonial.** Across these eight sessions, every single review round found a
  real defect, in both directions. Three consecutive rounds found a real defect
  in the *reviewer's repair*, which is the failure mode you would expect a
  reviewing process to be blind to.
- **Deliberately damaging our own finished code to see whether the tests notice
  it** has now found real gaps in five consecutive sessions. It is cheap and it
  is not optional.
- **The cost discipline is holding.** Total simulation budget spent on this
  entire protocol so far: **one** rollout, as a regression check, in Session 45.
  Everything else — the whole plan, the whole inventory, the whole reuse
  arithmetic, the timing, the 168-simulation cost estimate — has been derived
  without running the simulator at all.
- **The frozen plan has held.** Fourteen sessions without an edit to the
  pre-registration, including through three rounds that found real defects in
  the code implementing it. The defects were in the implementation, not in the
  plan.

---

## What isn't working

**The pace is the honest answer here, and I don't want to dress it up.**

My last report told you eight sessions had produced no measurement. This report
tells you eight more have produced no measurement either. The central experiment
still has not started. If you look at the calendar rather than at the work,
that is sixteen sessions of preparation.

What I can tell you is what those sessions bought. Three review rounds found
eight distinct defects in the executing program, each of which would have
produced a plausible-looking wrong answer rather than an obvious failure. I do
not think any of them would have been caught by running the experiment and
looking at the output, because in every case the output would have looked fine.

What I cannot tell you is that this is the right trade. That is a judgement about
how much a wrong answer costs us versus how much delay costs us, and it is
yours to make. If you want the screen run sooner and the checking thinner, say
so and we will do that — with the reduced confidence written into the record so
the eventual report says what was and wasn't checked.

**Two smaller things that are stuck:**

- **The one open request for you is still open.** `director_requests.md` entry 1
  asks for your review of the Claim Sheet — the project's contract. It is
  explicitly non-blocking and we have kept working, so nothing is waiting on it.
  It has now been open for a long stretch, and I mention it because a request
  nobody mentions is a request that quietly becomes permanent.
- **A large regeneration is queued behind the screen.** The 3.9 GB development
  dataset we generated will be thrown away and rebuilt from scratch once the
  screen's result is in, because a written amendment we have already agreed on
  changes one of the settings that feeds it. That work is real and it is not
  started. It is correctly ordered — regenerating before the screen would be
  regenerating into a plan that might change — but it means the gap between
  "screen finished" and "experiment running" is not zero.

---

## The verification artifact

Nothing new to report on the Slot 8 verification artifact — the thing whose
whole job is to let you check the result yourself without reading the technical
report. It has not been built and this stretch of work did not touch it. I would
rather tell you that than manufacture an update.

What *did* land this session, and is adjacent to it, is a new step in the
packet's runbook (Step 25) that lets any reader — you included — run the screen's
planning pass on their own machine. It takes about a third of a second, runs no
simulations, and prints the entire plan: nine candidate nudge strengths, 180
result rows, 168 simulations, the damage-start step, the measurement window. It
is the cheapest way for someone outside the project to check that our executable
plan matches the arithmetic in our pre-registration.

That step also carries the explanation of why 180 and 168 are both correct.
Twelve result rows reuse a simulation an earlier row already paid for: two of
Stage B's ten damage levels are ones Stage A already measured, and Stage C's
first undamaged replicate in each of four situations is the undamaged run Stage A
already did there. Those twelve rows point at the original run's record rather
than pretending to be new runs. Quote either number alone and a reader is
misled; the runbook now says both.

---

## What's next

1. **The execution decision.** Both agents have approved the program's
   implementation. That is explicitly *not* permission to run it — we separated
   those two decisions on purpose, so that "the code is right" and "spend the
   compute" are not the same signature. The next round is that decision.
2. **Run Stages A, B and C.** 168 simulations, roughly 70–80 minutes of
   compute by our current estimate.
3. **Read the answer.** The protocol pre-commits to what each outcome means, so
   there is no interpretation to negotiate afterwards. The three outcomes are
   roughly: the signal is comfortably visible; the signal is visible only for
   more severe damage; the signal is not visible at all. **The third is a real
   possibility** — my current honest estimate, carried unchanged for many
   sessions, is that the milder damage level fails clearly, and the more severe
   one clears the bar by only about 1.1×, using an estimate that is biased in our
   favour on both sides.
4. **Then the amendment, the regeneration, and the actual experiment.**

If the answer is "not visible," that is a publishable result and not a failed
project — it would say that this particular kind of body sensing, at this scale
of damage, with this kind of nudge, does not carry the information we hoped it
did. We pre-registered that outcome as one of the three precisely so that it
would be reportable rather than embarrassing.

— Claude
