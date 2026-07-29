# Progress Report — Claude, Session 40

**Date:** 2026-07-29
**Covers:** my Sessions 33–40 (previous report: Session 32)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

Eight sessions ago this project was about to measure something. It still hasn't.
What happened instead is that we found eight separate faults — one per session,
almost exactly — in the **instrument** we were going to measure with. Not in the
robot, not in the physics, not in the science. In the ruler.

That sounds like a bad eight sessions. I want to argue it was the opposite, and
then be honest about the part that genuinely worries me.

---

## First, what the project is actually trying to do

A quick refresher, because the details below only make sense against it.

We have a simulated two-link arm. It can be damaged in three different ways: a
link can go **soft** (structural), a motor can go **weak** (actuator), or a
sensor can start **lying** (encoder bias or drift). The question is whether
adding four [strain gauges](https://en.wikipedia.org/wiki/Strain_gauge) — small
sensors that measure how much the arm's own body is bending — lets the robot
tell those three cases apart better than a conventional sensor kit can, and
whether that better telling-apart translates into better control.

To find out, the arm gives itself a small deliberate nudge — a 1.25-second
gentle push at its own tip, at a known rhythm — and we read how the strain
gauges answer. Damage should change the answer. The whole experiment lives or
dies on one question: **is the change caused by damage bigger than the change
caused by everything else?**

"Everything else" is the instrument. And the instrument turned out to be full of
holes.

---

## The eight faults, in one line each

Each of these was found in a different session, and each one was found the same
way: by trying to write the measurement down precisely enough that a stranger
could run it without asking us anything. That practice —
[pre-registration](https://www.cos.io/initiatives/prereg), writing the analysis
down *before* running it so you can't tune it to your preferred answer — is what
kept surfacing them. Not review. Not reading. **Writing it out.**

1. **The nudge was too weak.** The safety screen that justified the nudge's
   strength used a sharper push shape than the one the data generator actually
   produces. The delivered nudge was about 5.8× weaker than the one we'd
   approved. The shape had never been written into the configuration file, so
   nothing caught it.
2. **The yardstick was measured on a different thing.** The detection bar was
   computed one gauge at a time over a shorter listening window; it was being
   applied to a number that combined four gauges over a longer one. About 8%
   error — small, and in the lax direction.
3. **The yardstick was the wrong *kind* of thing.** It described the spread of a
   *single* measurement; we were applying it to the *difference between two*.
   Related by roughly 1.4×.
4. **And that whole class of yardstick turned out to be void.** The two runs
   being compared deliberately share their random sensor noise — a standard
   variance-reduction trick called
   [common random numbers](https://en.wikipedia.org/wiki/Variance_reduction) —
   so the sensor noise *cancels* from the difference. A sensor-only bar can't
   judge a quantity the sensor noise has already left. The honest response was
   to retire the bar rather than fix it, and measure our own noise from repeated
   healthy runs instead.
5. **The nudge can't be made stronger.** A safety limit already in the plan caps
   it at 0.15 N by arithmetic alone. This matters more than it sounds: "just
   probe harder" is not an option we have.
6. **We were looking at the wrong second and a half.** The rule said to start
   watching when the fault appears. The generator waits a full second *after*
   the fault before nudging. So we watched a second of ordinary motion and
   caught under half the nudge. Fixing it made the damage signal 2.4–3.6× larger
   — the only one of the eight that moved in our favour, which is exactly why it
   got handed to the reviewing agent instead of quietly adopted.
7. **The plan never said how to *build* the thing it measured.** It was extremely
   precise about what to compute and completely silent on how to construct the
   run being computed on. The obvious construction is not the one the real
   generator uses. This is the fault I'm most struck by: precision in one
   dimension reads like precision overall.
8. **The comparison had two variables moving at once.** The damaged run and the
   healthy run we'd been comparing don't just differ in damage — they differ in
   an unrelated roll of the sensor-noise dice, which feeds back through the
   controller and changes how the arm physically moves. So our "damage signal"
   was damage *plus* an unrelated difference. A textbook
   [confound](https://en.wikipedia.org/wiki/Confounding), and I published a
   number built on it before catching it.

---

## The thing I'd most want you to take from this

Look at the direction of the errors.

Faults 1–5 made the project look **worse** than it was. Faults 6 and 8 made it
look **better**. And the two that flattered us were the two that took longest to
find.

That is not a coincidence, and I don't think it's a moral failing either — it's
just how attention works. When a number comes out disappointing you go looking
for what's wrong with it. When it comes out encouraging you write it up. Fault 8
compounded with an incomplete noise measurement, both pointing the same way, and
together they moved which outcome looked most likely. Neither was large alone.

So the working rule now is: **when an error favours you, that's the one to
hunt.** It's the discipline I'd want a stranger auditing this project to be able
to see us applying, and it's why the corrections that hurt us are written into
the public log in the same voice as the ones that help.

---

## What's actually working

**The machinery is faithful.** We can now take the written-down configuration,
rebuild one of the already-generated runs from scratch, and get back a result
identical **to the last bit** — all twenty recorded physical quantities and the
full sensor payload, byte for byte, verified independently by both agents.
[Bit-for-bit reproducibility](https://reproducible-builds.org/) is the standard
a reproducibility packet is supposed to meet, and this project had never
actually demonstrated it. It's now a stop-or-go positive control that runs
*before* the real measurement, so if something later goes wrong there's no
argument about whether the machinery itself was honest.

That finding also paid for itself immediately. Because the pipeline is exactly
deterministic, we discovered we can re-read a stored run through the sensor
model at zero cost — no physics simulation needed. That turned three
measurements that would have cost about an hour of simulation each into free
ones, and produced a design improvement we'd otherwise never have found. Cheap
exact reproduction turned out to be a *measuring instrument*, not just a
confidence check.

**The review loop is doing real work.** Every one of the eight faults above was
either found by writing the protocol out for the other agent, or found *by* the
other agent reading it. This session Codex blocked my protocol for the fourth
time, on nine specific points; I checked every one at the source code before
accepting it, found no defect in any of them, and found that two were **worse**
than Codex had said. One of those is worth naming because it's mine: I had
written that a stray screen run would be caught by a particular safety check.
Under the construction I'd specified in the same paragraph, that check would
have **passed the stray run straight through**. I described a guard by what I
wanted it to check instead of what it checks — the third time I've made that
exact mistake. This time I fed the guard the precise bad input and watched it
fire, rather than describing it.

**Something that had been a promise is now a built thing.** The protocol needed
a way to inject test parameters into the generator that the generator has no
input path for. Previously that was a sentence saying it would be done. This
session I built it and tested it three ways: that it reaches every parameter it
claims to, that it rejects bad values loudly, and — the important one — that
with all overrides switched off it reproduces the delivered run **byte for
byte**. It's a strict extension, not a rewrite. It's still sitting in a scratch
directory awaiting Codex's approval, because it's a change to code Codex owns.

---

## What isn't working

**The honest headline: the answer is still unmeasured, and the odds are roughly
a coin flip — in the unfavourable direction.**

Here's the situation in plain terms. We have ten damage levels to test, from
mild to severe. Our best current estimate says the **mild** ones fail clearly —
their signal is well under the noise. The middle one clears the bar in the
hardest test condition by about 1.11×, which is nothing. And that 1.11× was
computed with a signal we now know is **inflated** (fault 8) against a noise
bar we know is **deflated** (it leaves out part of the noise). Both errors
favour us. Corrected, the middle level is roughly a coin flip.

Which means the two live outcomes are:

- **Only severe damage is detectable.** Then we can still run the experiment,
  but on a narrow slice, and we'd have to report that narrowness prominently.
- **None of it is detectable at a safe nudge strength.** Then we report a
  pre-declared negative: this arm cannot test this question within its own
  safety limits. Not "strain sensing doesn't work" — something narrower and more
  useful: *at this scale, with this excitation budget, the information isn't
  there.*

Both of those are legitimate, pre-declared results. Neither is a failure of the
project. But I want you to hear clearly that the second one is now about as
likely as the first, and that a few sessions ago I'd have told you the first was
ahead. That change is a correction to my own reporting, not new physics.

**We are also four review rounds into one protocol.** Codex has blocked it four
times. Each block was correct and each made it better, but I'm watching the
cost: a protocol that takes five rounds to approve is a protocol whose author
kept mis-specifying it. The counter-argument — the one I actually believe — is
that every round found a real defect that would otherwise have contaminated the
measurement, and the cheapest possible time to find those is before spending 79
minutes of simulation. But if round five doesn't converge, the right move is to
escalate to you rather than loop again, and I'll do that.

**Nothing is blocked on you.** The one open item in
[`director_requests.md`](../../../director_requests.md) is still your review of
the Claim Sheet, which is explicitly non-blocking — the agents keep working
while it's pending. There's no decision waiting on you and nothing you need to
buy, download, or sign up for. This project remains entirely self-contained on
the desktop.

---

## What's next

The immediate path is short and specific:

1. Codex reviews the protocol I posted this session. If it's approved, I apply
   the code change and post the diff for review before anything runs.
2. The measurement itself: 169 simulated runs, about 76 minutes. It starts with
   the reproducibility positive control — if that fails, nothing else runs.
3. That measurement decides which of the three outcomes above we're in, and the
   whole downstream plan branches on it: either we regenerate the dataset around
   what's detectable, or we write up a bounded negative result.

The verification artifact — the hands-on thing you'll eventually use to check
the result yourself — has nothing new this session, so I'm not manufacturing an
update on it. Its shape depends on which branch we land in, which is the right
order: build the demo around the result that exists, not the one we hoped for.

---

## One last thought

I've spent eight sessions finding faults in our own measuring stick and none
measuring the thing we're here to measure. If you're wondering whether that's a
reasonable use of the time, here's the case for it in one sentence: **every one
of those eight faults, if it had survived, would have gone into a public result
that a stranger could check** — and four of them would have made the result look
better than the truth.

The nudge is 1.25 seconds long. Getting the ruler right took eight sessions.
That ratio is uncomfortable, and I think it's also correct.
