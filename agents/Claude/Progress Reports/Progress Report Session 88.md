# Progress Report — Claude, Session 88

**Date:** 2026-08-07 00:22 PDT
**Covers:** my Sessions 81–88 (previous report: Session 80)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The last report ended with a neural network that existed but had never been trained. Eight
sessions later, **it has been trained**, and the project has its first learned-model numbers.

Here is the headline, and I want to give you the bad news and the good news in the same
breath, because they are the same fact:

> **When we trained the network on the structural-sensing data (S) and on the conventional
> data (C1), the structural version scored slightly *worse*. And the difference between one
> random starting point and another was three times larger than the difference we are trying
> to detect.**

Neither half of that is a result about sensors. The first half may reflect the network being
too small; it may reflect the network being a size that is simply harder to train well in the
twenty passes over the data we gave it; it may reflect something else about this particular
practice run. **These numbers cannot separate those explanations, and I will not pretend
otherwise** — that distinction is the single most important idea in this report, and I explain
it below. The second half is a warning about the experiment's design that arrived early enough
to be useful.

What I have spent the sessions since doing is designing the measurement that shows *whether
and how* both versions' scores move as the network is made bigger and smaller — and getting
that design torn apart twice, once by Codex and once by me, before anything runs. Note what
that measurement is and is not. It can show that size matters here. It cannot tell us that
being too small is what *caused* the result above. Knowing that the answer moves with size is
still the thing we need next; it is just a smaller claim than the one I first wrote down, and
Codex was right to hold me to the smaller one.

The honest other half, same as last time: **eight sessions, zero simulations.** The lifetime
total is still **278**, exactly where Codex's payload measurement left it. Two of these eight
sessions produced numbers; six were building, reviewing and repairing the machinery that
produced them.

---

## The one idea you need: why "it scored worse" is not a sensor result

Three facts, all measured, and then the one thing they do *not* add up to.

**One.** The network has a fixed size: 39,594 numbers it is allowed to adjust while learning.
Both versions get exactly that size — that is a deliberate fairness property of the
experiment, because a bigger network for S would make any win meaningless.

**Two.** The structural suite S is the conventional suite C1 **plus** four strain-gauge
channels. Not different information — the same information plus more. And I checked that the
gauge channels actually reach the network before reading anything into the result, because "S
is worse" and "S's gauges never arrived" look identical in a score. They arrive.

**Three.** At that fixed size, S fit *worse* than C1 on three of the four fault categories.

Now the thing those three facts do not add up to: **they do not tell us why.** It is entirely
possible for a network to score worse while being fed strictly more real information — more
input at the same fixed capacity is a genuinely harder fitting problem — and that is the
possibility this project's contract anticipated. The Claim Sheet required a "capacity sweep"
from the beginning: a deliberate check of whether the answer changes when you make the model
bigger.

**I want to be careful here, because I was not careful once already.** In an earlier public
log entry I explained this by saying S has to "spread the same capacity over more incoming
information." That is a plausible mechanism. It is also one we have not measured, and Codex
was right to have it struck from the public record. The measured statement is the narrow one:
*S has strictly more input at identical capacity, and it fit worse.* Whether more capacity
changes that is exactly what the sweep is for, and until it runs, the honest reading of "S fit
worse at this size" is: **this number says nothing about sensors either way.** Both of us
wrote that down formally so that no future write-up can quietly turn it into evidence against
the project's hypothesis.

If you want an outside reference for the general shape of the tension — model capacity against
what a model is asked to fit — the textbook version is the
[bias–variance tradeoff](https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff).

---

## The second finding: the seeds move more than the effect

When you train a neural network you have to start it from random numbers. Which random
numbers you use is set by a "seed" — a number you pick so the randomness is repeatable. We
train five times, at seeds 0 through 4, and average.

Here is what the five runs gave us, as the difference between S and C1 (positive means S did
better):

```text
seed        0        1        2        3        4      mean
S − C1  +0.075   +0.039   −0.239   +0.104   −0.140   −0.032
```

Look at the spread. Two runs say S is clearly better. Two say S is clearly worse. The
standard deviation across seeds is **0.150**.

The Claim Sheet — the contract written before any of this — says the project will call the
result a success if S beats C1 by **0.05**. **The noise from the random starting point alone
is three times the size of the effect we are trying to detect.**

That is the most useful thing this stretch produced, and it did not come from a measurement
we designed to find it — it fell out of a routine first fit. It is a warning aimed squarely
at a decision that has not been made yet: how many training runs the *final* confirmatory
experiment needs. Five is very likely not enough. That decision belongs to a later gate, and
this number now sits in the file that gate will read.

Two honest bounds on it, which travel with the number everywhere I write it: this is measured
*in-sample* (on the same data the network trained on), and in-sample spread is not the same
as spread on fresh data. It is not a formal power calculation and must not be reported as
one.

---

## What I actually did, session by session

Sessions 81 through 88 split cleanly into three stretches.

**Sessions 81–84 — building the thing that runs the training, adversarially.** I wrote the
training program; Codex reviewed it and blocked it; I fixed what it found and found more; it
blocked again. Four full rounds. Every round found something real, and every round's finding
sat one structural layer below the previous one. Two examples, because the flavour matters
more than the list:

- Codex found that the program could mix checkpoints from different generations of the code
  and report them as one experiment. Real, and it fixed it.
- I then found that the guard *protecting* against a dirty output directory wrote its refusal
  message into the very file that was the sole record of the checkpoints it was refusing to
  mix with — so the safety check destroyed the evidence it existed to protect.

Somewhere in that stretch we also settled the one genuinely *scientific* decision left open:
which slice of each simulation run the network is allowed to look at. The rule we agreed
derives the window from the approved experiment design rather than accepting it as a
command-line option, and — this is the part that makes it defensible — the rule *reproduces*
the window that the earlier frozen protocol had already pre-registered, rather than competing
with it. There is a test that checks that against the real document.

**Session 84 — it ran.** Ten training runs, two sensor suites × five seeds. Zero simulations
(training reads data that already exists; it runs no physics). That produced the two findings
above.

**Sessions 85–88 — reading it honestly, then designing the follow-up.** Codex built a
read-only analysis program; I reviewed it and found five problems, including a published
file-fingerprint that a fresh download of the repository could not reproduce, and a
hand-copied formula with nothing checking it against the real one. Then two sessions went
into something narrower and, I think, more interesting than it sounds — I will come back to
it under "what was unexpected."

Session 88 (this one) closed that loop and returned the capacity-sweep design.

---

## What was unexpected

**A test can be fixed along the axis you just measured and still be broken along one nobody
named — and the second axis is usually right at the boundary.**

In Session 86 I measured how good our tests actually are by deliberately breaking the program
in fourteen small ways and checking that the tests noticed. Ten of fourteen were caught. The
four misses traced not to missing tests but to *test fixtures that were too simple*: one of
them used four example categories with one item each, so "pick the biggest category" and
"pick the smallest category" gave the same answer and no test could tell them apart. I fixed
all three fixtures. Fourteen of fourteen.

In Session 87, Codex reviewed that repair, corrected one wrong comment of mine — it was
right, I accepted it — and wrote a replacement comment saying the fixture now "pins the
selector rather than an ordering accident."

I measured it. It did not. My repair had made the categories unequal (1, 2, 3, 4), which
killed "biggest versus smallest" — but left them *ascending*, so the biggest was the **last**
one, and "pick the biggest" was still indistinguishable from "just take the last." I broke
the program that exact way and the test suite did not notice.

The fix was to reorder the counts to (1, 2, 4, 3), so the answer is neither the first nor the
last item. Every published number is unchanged; only which category is "the biggest" moves.

Here is the part worth your attention. **The real dataset has the same shape as the broken
fixture.** Our actual label counts are 8, 16, 32, 96 — also peaked on the last category. So
"check it against the real data" would have certified exactly the same accident. When a test
fixture and the real data happen to share a property nobody chose, there is no instrument
anywhere in the project that can see past it, and the fixture is the only place the
distinction can be made at all.

**And this session, the same shape again, one layer lower.** While writing the design for the
capacity sweep, I checked whether the approved training program could actually train a
network of a different size.

**It cannot.** The size is hard-coded at the one value it already used. There is no
command-line option for it and the word does not appear in the file. So the sweep I designed,
and that Codex reviewed in detail and returned five substantive criticisms of, **could not
have been run at all** — and neither of us noticed until I went to write down how it would be
implemented.

Worse, and this is the bit I would defend hardest: one of my own safety rules would have
*blocked the only fix*. I had written a rule saying the reused earlier results must have been
produced by code matching the code producing the new results. But editing the program to add
a size option changes the code's fingerprint — so the rule guaranteeing comparability would
have refused the edit that makes the measurement possible.

The repair is to stop asserting the two are equivalent and **measure it**: before running the
sweep, re-train one network at the original size through the new code and require the
resulting weights to be *bit-for-bit identical* to the approved one. Seven seconds, and it
turns an assumption into a check that fails loudly.

---

## What is working

- **The adversarial review loop is finding real defects at a steady rate and has not once
  degenerated into arguing.** Nine consecutive rounds across these eight sessions, each
  finding something one layer below the last. Every disagreement was settled from source
  within one exchange.
- **The project's first learned model exists, trained, with a complete provenance record** —
  each of the ten trained networks is bound to the exact data, the exact code and the exact
  settings that produced it.
- **Corrections propagate forward rather than backward.** When Codex found that one of my
  earlier public-log entries had been edited in place, it did not revert it; it appended a
  dated note saying an entry had been edited and that the removed claim was never measured. I
  checked that note against the repository's own history before approving it. The record now
  shows the mistake rather than hiding it.
- **Cost discipline is holding.** These eight sessions cost ten training runs of a few seconds
  each and zero simulations.

## What is not working

- **The central question still has no evidence either way.** Does structural sensing beat
  conventional sensing? Eight more sessions, and the honest answer remains: we do not know,
  and nothing we have run yet is allowed to say.
- **Eight sessions produced two sessions' worth of numbers.** I said in the last report that
  I would flag where the review cost stops being obviously worth it. I am not there yet — this
  stretch's rounds each caught something that would have corrupted a result — but the ratio is
  now six-to-two and I am watching it.
- **The seed spread is a real threat to the final experiment** and there is no plan yet for
  how many runs the confirmatory comparison will need. That decision is at a later gate; it
  should not be allowed to arrive unexamined.
- **The one thing that is genuinely stuck is not technical.** `director_requests.md` entry 1 —
  your review of the Claim Sheet — is still open from Session 5. It is non-blocking by design
  and nothing is waiting on it. But it is now the project's longest-standing open item, and
  it is the mechanism that checks the contract still matches what you want. The reading path
  is short and starts with `Accessible Claim Sheet.md`.

## Verification artifact

Nothing new. The Slot 8 verification artifact — the hands-on thing that will let you check the
result yourself without reading the technical report — is still unbuilt and is not due until
the result exists. I am not manufacturing an update on it.

---

## What is next

1. **Codex reviews the capacity-sweep design I returned this session.** One decision in it was
   genuinely open and I handed it over rather than taking it: whether to write a new program
   that imports the approved training pieces, or to edit the approved program itself. The
   first leaves ten existing results' provenance untouched at the cost of a duplicated loop;
   the second is cleaner code and moves a fingerprint that ten files recorded. *(Written
   before the answer existed. Codex has since ruled — the new program, leaving the approved
   one untouched — and the review of the design is still open as this report is handed over.)*
2. **Then the program that runs the sweep is written and reviewed** — a separate gate.
3. **Then a zero-training "plan" run is produced and reviewed** — another separate gate.
4. **Then, and only then, the training runs are authorized jointly** — forty for the curve
   itself, plus two more whose only job is to prove the new program reproduces the old one
   exactly before any new number is trusted. About six minutes of computer time behind four
   separate approval gates, which is the pattern this project has settled into: cheap to run,
   expensive to get right, and never run before both agents agree what it would mean.
5. After that, the network's confidence calibration, and the evaluation driver.

The measurement itself will not answer the project's question, and it will not prove that the
first pattern was caused by a network that was too small. What it will show is whether, and by
how much, the two versions' scores move as the network changes size — everything else about
the training held fixed. That narrower map is the next thing we need, because it tells us what
a later test on fresh data would have to be designed to separate.
