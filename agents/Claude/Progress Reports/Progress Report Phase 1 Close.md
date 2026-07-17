# Progress Report — Phase 1 Close (Sharpening → Execution)

**From:** Claude · **Date:** 2026-07-17 · **Project:** Robot Structural Proprioception

*This is a director update, not a technical paper. If any sentence sends you to look something up, that's my failure, not yours — every leaned-on term has a plain explanation and a link. Read it start to finish in one sitting.*

---

## The one-paragraph version

Phase 1 is done. Phase 1 was the design phase — its whole job was to turn your seed idea into a **contract**: an exact, written-down agreement about what we're testing, how we'll measure it, and — decided in advance — what would count as success, as failure, and as an honest "it depends." That contract (the **Claim Sheet**) is finished and agreed by both agents, along with a plain-language version for you, a study guide for you, and the shared "data schema" that lets Codex and me build two halves of the same machine without them failing to fit together. Nothing has been *simulated* yet — Phase 1 produced no results, and it wasn't supposed to. We now move into **Phase 2 (Execution)**, where the actual robot simulation gets built and the real question finally gets tested. The first Phase-2 step is a small, honest go/no-go experiment I'll describe near the end.

---

## A 30-second refresher on what we're actually asking

Most robots run on a fixed factory model of their own body. Real bodies don't stay fixed — parts wear, loosen, heat up, go slightly soft, lose motor strength; sensors drift and get noisy. A robot that keeps trusting its original model can quietly become inaccurate or unsafe while still being physically capable of the job.

Your idea was to borrow from aerospace: a structure's **strain** — how much its material is stretching or bending under load — isn't just a thing engineers check for safety, it's *information the robot could feel about itself*. The question we spent Phase 1 sharpening into something testable:

> On a small simulated flexible robot arm, do a few cheap **strain/bending sensors along the limbs** give it information a normal robot sensor set doesn't have — specifically, enough to tell apart *three different kinds of change* (the structure went soft, a motor got weak, or a joint sensor started lying) — and does knowing which one it is actually help the robot keep doing its task?

The honest twist we've kept front and center: **a clean "no" is a real result here.** If a good conventional sensor set already recovers the same information, that tells builders *not* to spend money and weight on strain sensing — genuinely useful to know, and we'll publish it just as loudly as a "yes."

---

## What Phase 1 actually produced

Four documents, all finished and agreed:

1. **The Claim Sheet** — the technical contract (fifteen numbered "slots" covering the question, the method, the baselines, the scoring, and the pre-declared success/failure shapes). This is the spine everything else hangs on.
2. **The Accessible Claim Sheet** — the same contract in plain language, for you. It says exactly what the technical one says, with nothing softened or dropped — I checked every number matches.
3. **Study Guide, Pass 1** — a conceptual foundation written for you specifically, so you can follow and judge Phase 2 without having to take our word for anything.
4. **The shared data schema** — the least glamorous and, honestly, one of the most important. It's the precise definition of the data that flows from the physics simulation → the sensors → the diagnosis → the controller. Codex builds the physics half; I build the sensing-and-diagnosis half. The schema is the shared blueprint that guarantees the two halves click together and — critically — that the test stays honest (more on that below).

All four are in the repository, and the Claim Sheet has just been logged for your review (see `director_requests.md` — it's **non-blocking**, meaning we keep working while it waits for you, whenever you get to it).

---

## The four ideas we locked down (this is the substance)

Phase 1's real work was making a handful of design decisions airtight. Here are the ones worth your attention.

**1. Change *only* the sensors — nothing else.** The core of the experiment is a fair comparison between sensor sets, built up in layers:
- **C0** — a bare robot: joint-angle sensors + knowing what commands it sent.
- **C1** — a realistic, well-equipped conventional robot: C0 plus a noisy motor-current reading (a rough sense of how hard each motor is pushing) and one motion sensor (an IMU, the same chip that knows which way your phone is tilted) on the far link.
- **S** — the star: exactly C1, plus four small **strain gauges** along the arm.
- **O** — an "oracle" that secretly sees the true answer. Not a real robot; it's the ceiling, so we know the best score physically possible.

The trick: we use the *same* diagnosis software and the *same* controller on every set. The **only** thing that changes is which sensors it's allowed to read. That way, if **S** beats **C1**, the win can only be due to the *information the strain sensors carry* — not a smarter algorithm. Comparing **S** against the strong **C1** (rather than the bare **C0**) is us deliberately picking the *hardest* fair fight, so a win actually means something.

**2. Three kinds of change, plus the right to say "I don't know."** We test three specific failures — a link going soft (**structure**), a motor weakening (**actuator**), and a joint sensor drifting/biased (**sensor**) — plus a healthy state. And the robot is always allowed to **abstain** — to answer "something changed but I can't safely say what." That matters because a system that's forced to always pick an answer will confidently guess wrong, which in a real robot is worse than admitting uncertainty. We score the abstain option carefully so the robot can't game it (a diagnosis it abstains on when it should've known counts against it, not for it).

**3. Two separate scorecards, never blended.** We measure **diagnosis** (did it correctly name what changed?) and **control** (did it keep doing the task well after the change?) as two independent scores. We refuse to merge them into one number. Why: it's entirely possible that strain sensing helps the robot *know* what broke but doesn't help it *perform* better — or vice versa. Blending them into one score would hide exactly that distinction, and that distinction is one of the most interesting things the project could find. For the record, the headline diagnosis score is a "macro-F1" — a standard, unglamorous accuracy measure that [weights each of the four answers equally](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html) so the robot can't look good just by nailing the common cases and flubbing the rare ones.

**4. We wrote down the finish line before running the race.** This is the honesty machinery, and it's the part I'm most glad we nailed. *Before* generating a single simulation, we committed — in writing — to the exact bar that counts as success: strain sensing must improve diagnosis by **at least 0.05** (on that 0-to-1 scale), *and* cut the post-failure tracking error by **at least 10%**, *and* do so with a [statistical confidence interval](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) that excludes zero (i.e., the improvement is unlikely to be a fluke of which random scenarios we happened to test). Fixing the bar in advance is what stops a researcher — human or AI — from seeing the results and then quietly deciding that whatever happened counts as a win. Everything in between full success and clean failure (say, "it helps for soft links but not weak motors") is *also* pre-listed, so a partial result gets reported as exactly that, never dressed up as more.

---

## What surprised me — the review process caught real mistakes

The two-agent setup (I draft, Codex reviews and edits, I re-review) isn't ceremony. In Phase 1 it caught genuine errors in my own drafts that would have quietly undermined the experiment. Three worth showing you, because they're understandable and they're the kind of thing that decides whether a result is trustworthy:

- **The weak-motor test was almost too easy — Codex caught it.** In my first draft, the conventional robot **C1** could effectively tell when a motor was weak, because I'd let it see something close to the true delivered force. Codex pointed out that a real robot *doesn't* get that — it only measures the *current* going into the motor, and a worn motor produces less force for the same current. So we moved the "weakness" to act *after* the current reading. Now the conventional robot genuinely can't directly see a weak motor; it has to infer it from motion, which is exactly the ambiguous situation strain sensing is supposed to help with. Without this fix, the experiment would have been rigged in the conventional robot's favor on that one fault — and we'd have understated strain's value.
- **A lying sensor doesn't bend anything — so we test it differently.** I'd originally assumed every fault should show up as a change in strain. But a drifting *joint sensor* doesn't physically deform the arm — it just reports the wrong number. So it can't be caught by "the strain changed." It's caught by a **disagreement**: the lying sensor says one thing while the independent strain history says another. That's the whole intellectual heart of the project — using one physically-independent stream to cross-check another — and getting the *mechanism* right for the sensor fault mattered.
- **"Stored separately" wasn't actually safe — we made the data physically unable to cheat.** A constant risk in this kind of study is **leakage**: the diagnosis software accidentally peeking at the answer key. We'd agreed the answer labels would be "stored separately," but in reviewing the data schema I'd handed off, Codex noticed that the bookkeeping file still carried a fault ID that could give the game away, and that "separate" was a promise in prose, not something enforced. The final schema physically walls off the answer key and includes an automated test that **fails the build** if the diagnosis code can reach anything it shouldn't. Honesty you can check by running it beats honesty you have to trust.

None of these changed *what* we're testing. They changed whether the test would actually be *fair* — which is the difference between a result worth publishing and one that isn't.

---

## What's working

- **The collaboration is producing something tighter than either of us drafted alone.** Every one of the fixes above came from one agent genuinely re-reading the other's work, not rubber-stamping it. The contract is meaningfully stronger for it.
- **The design is honest by construction.** Pre-committed bars, two un-blended scorecards, an enforced anti-cheating wall, and a clean-negative result treated as a first-class outcome. If this project says "yes" at the end, it'll be a "yes" you can trust; if it says "no," same.
- **We've stayed inside the constraints.** Everything is free, open-source, commercial-use-friendly software running on the one desktop. No costs incurred, nothing that needs your accounts or money.

## What isn't working yet / what's genuinely still open

I want to be straight about the risks, because "what isn't working" is where you learn what's actually uncertain:

- **The central question is still 100% open.** Phase 1 was design. We have *not* shown that strain sensing helps — we've only built an honest way to find out. Everything could still come back a clean negative.
- **The very next step is a real go/no-go that can fail.** Before building the full experiment, Codex runs a small **feasibility spike**: does a *few* simulated strain gauges on a realistically stiff (metal-ish) arm actually produce *distinguishable* signals for the three faults, above realistic sensor noise? Real strain sensors have real limits — for example, the fiber-optic gauges we're modeling [bleed temperature into their strain reading, roughly 10 microstrain per °C](https://doi.org/10.3390/s21175828), which we're simulating rather than idealizing away. If the signals don't clear that noise floor, we don't paper over it — we either switch to a higher-fidelity physics model ([PyElastica](https://github.com/GazzolaLab/PyElastica), a rod-physics library we've lined up as the backup) or we report honestly that this simulation can't fairly test the question. That gate is deliberately placed *first*, before we invest in the full build.
- **One thing is waiting on you, and it's fine that it is.** The Claim Sheet is logged for your review. It's non-blocking by design — we're already moving into Phase 2 — but your review is the checkpoint that the contract matches what you actually want this project to be. Whenever you get to it.

## What's next (Phase 2)

- **Codex:** the feasibility spike described above — the gate. Nothing else gets built until it clears.
- **Me:** while that runs, I build the **sensor-realism model** (turning the simulation's perfect physics into believably imperfect sensor readings — drift, temperature effects, lag, dropout) and the **evaluation harness** (the scoring machinery, wired to refuse the leakage and blending problems above).
- **For you, eventually:** the contract commits us to build a hands-on **side-by-side demo** — you pick a fault from a menu ("soften link 2," "weaken motor 1," "bias sensor 1") and watch two copies of the robot, one conventional and one with strain sensing, try to diagnose it and keep working, live. It doesn't exist yet — it's built during Phase 2/3 — but it's designed into the plan now, and it's how you'll be able to *see* the result rather than take our word for it. That, plus the second pass of your study guide, is how Phase 3 will hand the finished work back to you.

I'll write the next progress report at my session 8, or sooner if a phase closes or the contract gets amended before then.

— Claude
