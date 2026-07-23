# Progress Report — Session 24 (Phase 2, mid-execution)

**From:** Claude · **Date:** 2026-07-22 · **Project:** Robot Structural Proprioception

*A director update, not a technical paper. If any sentence sends you to look something up, that's my failure — every leaned-on term has a plain explanation and a link. Meant to be read start to finish in one sitting. It picks up where my session-16 report left off.*

---

## The one-paragraph version

Since my last report we stopped building the apparatus and started getting **answers** — and the answers are pointing somewhere specific and, I think, genuinely interesting. The strain sensors work. They work *dramatically* well at one thing: noticing when a link goes soft. On that fault the strain-equipped robot catches **100%** of cases where the conventional robot catches **8%**. That is not a marginal edge; the conventional robot is essentially blind there. And then we asked the second question — *does knowing that help the robot do its job?* — and the answer, so far, is **no, because that particular fault doesn't hurt the robot's job in the first place.** A softening link makes the arm's tracking *slightly better*, not worse. Meanwhile the faults that genuinely do degrade performance — a weakening motor, a lying joint sensor — are ones the conventional robot already detects perfectly well on its own. We have now checked **four separate ways** the extra strain information could still convert into better control on those faults, and all four are closed. This is converging on an outcome we **wrote down in advance** as a legitimate result: *the extra sensing improves diagnosis but not control*. I want to be plain that this is a real finding and not a failure, and equally plain that it isn't final — the design still isn't frozen, and there are named things left to check.

---

## A 20-second refresher

We're testing whether a few cheap **strain sensors** (they feel how much the arm is bending) give a robot information a normal robot doesn't have — enough to tell apart three kinds of trouble: a link going **soft**, a motor going **weak**, or a joint sensor **lying** — and whether knowing which one actually helps the robot keep doing its job. A clean "no" is a real, publishable result. Every setting is locked *in advance*, a practice called [preregistration](https://en.wikipedia.org/wiki/Preregistration_(science)), so nobody can move the finish line after seeing the race.

---

## The idea I most want to teach you this session: seeing something is not the same as being able to do something about it

This is the whole shape of what we found, and it's worth getting in your bones because it will show up in the final write-up.

There are two completely different questions you can ask about a sensor:

1. **Can it tell?** — Does the signal contain enough information to distinguish what happened? This is an *information* question.
2. **Does it help?** — Given that you can tell, can you act on it in a way that makes the outcome better? This is a *control* question.

It is very tempting to assume the second follows from the first. It doesn't, and our project is now a clean example of why. Picture a car with a sensor that reliably detects a small scratch on the paint. The sensor is excellent. The information is real. But there is no steering input that responds to a scratch — knowing about it changes nothing you can *do*. The information is genuine and the control value is zero.

That is very close to what we measured. When we weaken the arm's link stiffness, the strain signature grows enormously — at the most severe setting the peak strain is **13.5 times** the healthy level, a signal you could not miss. And at that exact same setting, the arm's tracking error is **5% lower than healthy** — the arm does its job slightly *better*. There is nothing for a controller to fix. The strain sensors are reading a real, large, unmistakable change in the body that simply has no cost attached to it on this task.

Meanwhile the faults that *do* cost something — a motor down to a quarter of its strength (23% worse tracking), a joint sensor with a constant offset (16% worse) — are exactly the ones the conventional robot detects perfectly on its own, because the motor command is something it already knows and can compare against.

So the honest summary of where the evidence points is this sentence, which I expect to be near the center of the final paper:

> **Where the strain sensors have exclusive information, there is no control headroom; where there is control headroom, the conventional sensors already have the information.**

That is a real, specific, checkable claim — and it is a much more interesting one than "the sensors didn't work," which is not what happened.

---

## What's been done since the last report

Last time the machine was built but nothing was answered. Since then, in rough order:

- **The strain suite's information advantage was confirmed properly** — under realistic noise, with a decision made once and held (no peeking, no retries). Strain suite: **99.5%** four-way accuracy. Conventional suite: **70.4%**, and only **8.3%** on structural faults. This is the strongest positive result the project has.
- **The obvious recovery action was tried and it failed** — stiffening the command in response to a detected structural fault. It improved tracking on the *healthy* robot slightly more than on the faulted one, which means it was a generic tuning improvement wearing a diagnosis costume. We blocked it. This is the kind of thing that would quietly become a false claim if nobody checked whether the "fix" was actually specific to the fault.
- **We measured where the headroom actually is** (Codex's screen, which I independently reproduced and, in doing so, found and fixed a units error in its threshold). Structural faults: no headroom at any severity. Motor and sensor faults: real headroom.
- **Then we spent four sessions closing every route by which strain could still win on the faults that do have headroom.** Detection — closed, both suites detect them. Classification — closed, both classify them. Severity accuracy — closed, and the conventional suite is if anything slightly *better*. And this session: the class-probability channel — closed.

---

## What was unexpected

**Two things, and both were corrections to my own work.**

The first: last session I claimed a result was "closed for any possible read-out." Codex reviewed it and said that was overreach. It was right, and the counterexample was sitting inside my own data — I had swept a range of controller responses and found the outcome barely moved across it, but the range I swept wasn't the whole range the system can actually reach. Extend it to the true endpoints and the movement is above our threshold, not below it.

This produced the second thing I want to teach you, because it's a genuinely useful idea:

> **A sweep across a range *you chose* gives you an envelope. A sweep across a range the *system's own constants* close gives you a reachable set. They can be the same table of numbers and mean very different things.**

An envelope says "across the values I tried, nothing much happened." A reachable set says "the machine cannot go outside these values, and across all of them nothing much happened." The second is a far stronger claim, and you're only entitled to it when you can point at the specific constants doing the closing.

This session I got to use that immediately. The channel I screened turned out to be closed at both ends by two numbers already in the controller: it refuses to act below 50% confidence, and it never commands more than double compensation. So the sweep genuinely covers everything the machine can do — I could make the stronger claim, and, more importantly, I could *say why I was entitled to it*. Getting corrected on Monday and applying the correction on Tuesday is the collaboration working the way it's supposed to.

And a third, smaller one, on the same theme: I nearly shipped a units error in this session's own screen. I was about to compare the channel's span against our 10-point bar using a quantity that isn't the one the bar is written in. It understates the real number by about 6.5%. Caught it before handing off. Same error class I'd caught in Codex's work three sessions ago, which is a useful reminder that the discipline has to point inward too.

---

## What's working

- **The cross-review is doing real work.** Three consecutive sessions where one agent found a substantive defect in the other's work: Codex's threshold units (mine, S21), my severity grid (Codex's catch, S23), and my overreach plus two integrity gaps (Codex's catch, S24). None of these were cosmetic. Each would have put a wrong sentence in the final paper.
- **The reproducibility packet is genuinely healthy.** 248 tests passing before this session's work, all green, and every screen re-runs to bit-identical results on a different worker count.
- **The pre-registration is holding.** The outcome we're converging on — "improves diagnosis, not control" — is one of the four we wrote down *before* running anything. That's the difference between a result and a rationalization.

---

## What isn't working

- **The design freeze is still the bottleneck, and it's the same bottleneck as session 16.** The learned "diagnosis brain" — the part that would let the robot *name* a fault — still isn't built, because training it honestly requires frozen settings and confirmatory data that don't exist yet. I will not build it on unfrozen settings; that would be the exact leak the whole design exists to prevent.
- **Everything so far is one small condition.** One task, one contact setup, one fault location, one severity per class, held out over sensor noise only. That is enough to *close* routes, which is what we've been doing. It is not enough to make a confirmatory claim, and I keep saying so in every artifact.
- **The compensation cap is leaving performance on the table, and we now know how much.** At the motor fault we selected, fully restoring the arm would need a 4× correction; the controller is capped at 2×. It recovers **57.5%** of what's theoretically recoverable. That's a design decision worth revisiting — but raising the cap re-opens a route we just closed, so it's a genuine trade rather than free money. That's flagged for the next round.
- **Still awaiting your Claim Sheet review** (`director_requests.md`, entry 1). It is explicitly non-blocking and we have kept working — but it's open, and this is where I'm supposed to say so.

---

## The verification artifact

No change this session. The Slot 8 hands-on artifact — the thing that will let you check the result yourself without reading the technical report — still depends on the frozen data layout. I'd rather report "nothing new" than manufacture an update.

---

## What's next

1. **Codex's actuator action screen** — does the recovery action help at all, and does it fire wrongly on a healthy robot? That's the remaining piece of the control story, and this session's work removed one term from its design.
2. **Getting to a freeze.** With four channels closed, the list of things that must be settled before we can generate confirmatory data is shorter and much more concrete than it was at session 16. That's the real progress this stretch bought.
3. **Then, and only then, the learned head** — on frozen settings, on data generated after the freeze.

If the pattern holds, the project's result will be a careful, well-evidenced negative on the control question paired with a strong positive on the information question. That's a genuinely useful thing to publish: it tells the next person which half of this idea is worth their time.

I'll write the next progress report at my session 32, or sooner if a phase closes or the contract gets amended.

— Claude
