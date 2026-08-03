# Progress Report — Claude, Session 64

**Date:** 2026-08-03
**Covers:** my Sessions 57–64 (previous report: Session 56)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

Last report ended with a finished measuring program that had run zero of its 168
simulations. Since then it **ran**. Codex executed it in its Session 57 — 135
simulations, about 74 minutes of computer time — and it produced a real,
pre-registered result.

Then the result turned out to be conditional on something nobody had looked at.

Not wrong. Conditional. The number the screen produced is true of the exact
conditions it was measured in, and one of those conditions is **how heavy an
object the robot arm is holding**. I found that in Session 60, by reading a
contrast that was already sitting inside the finished experiment — it cost zero
new simulation time. Adding 50 grams to the arm's tip cuts the damage signal
roughly in half, while the background noise the signal has to beat does not move
at all.

The project uses seven other payload weights that this experiment never touched,
and three of its four data groups reserve at least one of them. So the honest
statement of where we are is: **we measured the boundary of what this method can
detect, and we measured it at the two lightest weights out of eight.**

The last four of my sessions have gone into designing the follow-up measurement
that fixes that — carefully, because it costs about an hour of simulation and
because getting it wrong would waste both the hour and the trust in the number
it produces. That design is now agreed by both agents. It has not run yet.

---

## The one idea you need for the rest of this report

The robot in our simulation is a two-link flexible arm. Buried in it are four
virtual **strain gauges** — sensors that measure how much the material is being
stretched or bent. ([Strain gauge, Wikipedia](https://en.wikipedia.org/wiki/Strain_gauge).)
That is the "structural proprioception" the whole project is about: can a robot
feel its own body deforming, and does that tell it something its ordinary sensors
cannot?

The screen we ran asks a narrower question: **if we weaken one of the arm's links,
how weak does it have to get before the strain gauges can tell?** We weaken the
link by a percentage — "remaining stiffness 0.50" means the link is half as stiff
as it should be — and we look for the weakest damage the gauges can still pick out
of the noise.

The answer the screen gave, at the arm's two lightest payloads:

- Unloaded, the gauges can detect damage down to about **40% stiffness loss**.
- Carrying 50 grams, only down to about **55% stiffness loss**.

Fifty grams. On an arm whose entire body weighs 173 grams.

---

## What happened, session by session

**Sessions 57–59 — the screen ran, and then we audited it three times.**
Codex executed the 135 simulations. I then re-derived every number in the result
from the raw output using instruments that share no code with the program that
produced it — the discipline being that if you check a producer with the
producer's own code, you have measured agreement, not correctness.

Every number reproduced. But the audit found something the tests could not:
one whole section of the pre-registered protocol had **no implementation at
all**. The document promised a "role-coverage" count — how many of the damage
levels reserved for each data group are actually detectable — and nothing in the
program computed it. Nobody had checked the specification against the outputs,
because everyone was checking the outputs against each other.

I built that missing piece at zero simulation cost. It says: of the damage levels
reserved for the four data groups, **development gets 0 detectable, pilot 0,
validation 1, test 1**. That matters because development is the group the models
train on. We are asking a model to learn a signature that, at the selected probe,
is not measurable in its own training data.

**Session 60 — the tool that certifies our other tools was broken.**
Both agents use a technique called **mutation testing** to decide whether a safety
check is real: you deliberately break one line of the code, re-run the tests, and
if no test fails, that line was never being checked by anything.
([Mutation testing, Wikipedia](https://en.wikipedia.org/wiki/Mutation_testing).)

Ours was giving false answers in both directions. The cause was mundane and nasty:
Python caches compiled code and decides whether the cache is stale by comparing
file size and modification time — and time to a resolution of **one whole second**.
Every one of our broken versions happened to be exactly the same size as the last,
and when the tests ran in under a second, consecutive runs landed in the same
second. Python quietly executed the *previous* broken version and we recorded the
verdict against the current one.

The dangerous direction is not the false alarm. It is the false all-clear: the
tool reporting that a safety check is real when no test touches it — inside the
exact ritual we perform in order to be sure. The fix is two lines. But it had been
wrong for nine sessions, so every "this guard is verified" claim from that stretch
had to be re-checked. I re-ran the ones that mattered; they held.

**Session 60, same session — the payload finding.**
The screen ran its damage ladder in four different environmental conditions, and
the design document calls those four "replicates," as though they were
interchangeable. They are not. Two of them carry a 50-gram payload and two do
not — a clean, balanced comparison that had been sitting inside a finished,
paid-for experiment for three sessions, unread.

The ratio is remarkably steady: across all ten damage levels, the payload
multiplies the damage signal by 0.49–0.54. The noise floor it competes against
moves by essentially nothing. Signal falls; noise does not; the detection boundary
moves.

**Two things I deliberately did not conclude, and want on the record.** Two
weights give you a *ratio*, not a *curve*. I cannot multiply 0.5 out to 200 grams
and claim to know anything. And the *mechanism* is unidentified — I checked the
two obvious explanations in Session 62 and killed both:

- It is not the payload sagging the arm. Our simulation has **gravity switched
  off**. I discovered this by trying to measure the sag and getting exactly zero
  at every weight including 200 grams. So the payload is pure rotational
  inertia — resistance to being accelerated, not a hanging load.
  ([Moment of inertia, Wikipedia](https://en.wikipedia.org/wiki/Moment_of_inertia).)
- It is not resonance. Our diagnostic probe wiggles the arm at 0.8 Hz; the arm's
  slowest natural vibration is around 77 Hz, roughly 97 times faster. Nothing is
  being driven near a resonance.
  ([Normal modes, Wikipedia](https://en.wikipedia.org/wiki/Normal_mode).)

So we have a real, repeatable, sizeable effect and no explanation for it. I would
rather report that than let a plausible-sounding mechanism into a document
unmeasured.

**Sessions 61–64 — designing the follow-up.**
The obvious response is "just measure the other six weights." The design took four
sessions and seven review rounds, and I think the rounds were worth it. A sample
of what they caught:

- My first draft gave each of the seven weights its own random sensor noise. Codex
  pointed out that this makes my own safety check useless: I had written a check
  requiring the seven results to be *different from each other* as proof the weight
  setting was actually reaching the simulator — and giving each its own random seed
  makes them different for free. The check would pass in exactly the situation it
  existed to catch. The fix is to hold the randomness identical across weights, so
  a setting that fails to take effect produces *identical* output, which is
  refusable. ([Common random numbers is the standard name for this
  trick](https://en.wikipedia.org/wiki/Variance_reduction).)
- Fixing that broke the results key. Our results table identifies each simulation
  partly by its sensor identity — which was fine while every weight had its own.
  Make the identities identical and the key can no longer tell a 25-gram run from
  a 200-gram run. The current ledger would refuse the second weight loudly about
  nine simulations in, rather than quietly filing one as the other, but the
  follow-up still cannot run until payload mass is part of the key.
- In Session 63 I found a defect in Codex's own correction. The rules that say what
  the result licenses us to conclude had been tightened in one branch and left
  loose in the neighbouring one. I enumerated all 19,448 possible outcomes and
  found 3,185 in which **deleting a result would have licensed a bolder
  conclusion**. That is the sharpest test I have for a rule of this kind, and it is
  now written into the document.
- This session (64) I reviewed Codex's first piece of construction and found that
  the payload weight could be stored in the results table but there was no way to
  *put* it there — the only code path that builds those entries dropped it. The
  planned 126 simulations would have collapsed to 18 slots. Fixed, with a test
  that fails if it ever regresses.

---

## Where things actually stand

**Working:**
- The screen ran and its result is agreed by both agents. Total simulation spent
  on the whole project to date: **151 rollouts**. The screen itself recorded
  4,432 seconds — about 74 minutes — inside its executor; the other 16 rollouts do
  not have one carried aggregate time, so I am not inventing a project-wide total.
- Every finding above cost **zero** new simulation. All of it came from reading
  data we already had, or from reasoning checked against the source code.
- The automated test suite is at 1,136 tests, all passing.
- The review process is finding real defects at a steady rate, in both agents'
  work, including in corrections to earlier corrections.

**Not working, or unresolved:**
- **Six of eight payload weights are unmeasured**, and the design's ability to
  generalize across weights depends on them.
- **The mechanism of the payload effect is unknown.**
- **The development group has no detectable structural damage level** at the
  selected probe, which is a problem for the training stage that comes next.
- **The follow-up measurement has not run.** It needs about an hour of simulation
  and one more piece of code, which is the immediate next task.
- **Nothing else is blocked on you.** The one open item in `director_requests.md`
  is still your review of the Claim Sheet, which is deliberately non-blocking —
  the agents have kept working the whole time.

**On the verification artifact** (the hands-on thing you will use to check the
result yourself): no change this stretch, and I am not going to manufacture one.
It is paced to arrive with the confirmatory results, not before them.

---

## What is next

1. Build the program that runs the payload measurement, and review it the same
   way we reviewed the last one.
2. Run it in two stages: a zero-cost planning pass first, then — as a separately
   authorized decision — the real one, about 53–58 minutes.
3. Read the result, then choose between three pre-registered options for how the
   project handles payload weight. The document already pins which result licenses
   which choice, so that decision cannot be made after seeing the data in a way
   that flatters us.
4. Write the formal amendment to the Claim Sheet, regenerate the dataset, and get
   back to the actual models.

The honest framing of this stretch: we found that our headline measurement has a
hidden dependency, and we stopped to measure the dependency instead of writing it
up as though it were not there. That is slower. I think it is the right call, and
if you disagree, it is your call to make — this is the kind of judgment the
progress report exists to hand you.

— Claude
