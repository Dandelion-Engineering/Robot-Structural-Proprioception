# Progress Report — Session 8 (Phase 2, mid-execution)

**From:** Claude · **Date:** 2026-07-17 · **Project:** Robot Structural Proprioception

*A director update, not a technical paper. If any sentence sends you to look something up, that's my failure — every leaned-on term has a plain explanation and a link. Meant to be read start to finish in one sitting.*

---

## The one-paragraph version

Since the last report we crossed from *designing* the experiment to *building the machine that runs it*. Three things now exist that didn't: the physics half and the sensing half **run together as one live loop** (the simulated arm moves, the sensors report imperfectly, one control step at a time, with no ability to peek at the future); the **scoring machinery** that will judge the final result is built and has already survived a round of bug-hunting; and this session I built the **first half of the "diagnosis brain"** — the part that watches the sensor stream and decides *whether something has changed* and *whether it's confident enough to say what*. I deliberately did **not** build the second half yet — the part that names *which* of the three faults it is — and the reason I held off is itself one of the more honest decisions in the project, so I'll explain it. Still no results: we have not shown that strain sensing helps. We've built most of the apparatus that will tell us, honestly, either way.

---

## A 20-second refresher

We're testing whether a few cheap **strain sensors** (they feel how much the arm is bending/stretching) give a robot information a normal robot doesn't have — specifically, enough to tell apart three kinds of trouble: a link going **soft**, a motor going **weak**, or a joint sensor **lying** — and whether knowing which one actually helps it keep doing its job. A clean "no" is a real, publishable result. The whole design is locked in advance so nobody can move the finish line after seeing the race.

---

## Where the project stands right now

Think of the full system as a relay: **arm physics → sensors → diagnosis → controller**. As of this session:

- **Arm physics → sensors** is built and the two pieces are **wired together into one causal loop** (Codex's work plus mine, integrated over the last few sessions). "Causal" is doing real work in that sentence: the robot's decision at each instant can only use readings that have actually arrived by then — a sensor with a small delay is withheld until its delay has passed, exactly like real hardware. We verified this the hard way (more below).
- **The scoring machinery** (my "evaluation harness" from the last stretch) is built: it's the code that will eventually compute *did diagnosis improve* and *did control improve*, with honest statistics.
- **Diagnosis** is the piece I started this session. The *first half* now exists.
- **Controller** (the recovery behavior) is Codex's upcoming work; I built the socket it plugs into.

So the relay is roughly three-and-a-half of four stages built — but **untrained and unrun**. The apparatus is coming together; the experiment hasn't happened.

---

## The idea I want to actually teach you this session: the "diagnosis brain," and why I built only half of it

The diagnosis component is the heart of the project — it's the thing that looks at the incoming sensor stream and answers "what's going on with my body?" It has a natural ladder of difficulty, and it's worth seeing the rungs:

1. **Detect** — notice *something* changed (I'm not behaving like a healthy version of myself).
2. **Classify** — name *which* of the three things it is: soft link, weak motor, or lying sensor. And crucially, be allowed to say **"I don't know"** rather than guess.
3. **Localize & size** — *where*, and *how bad*.
4. **Use it** — feed that into the controller so the robot keeps working.

Here's the honest decision. Rungs 1 and the "I don't know" part of rung 2 can be built and tested **right now**, because they don't require the robot to have *learned* anything from examples — they're a well-understood idea from aerospace structural monitoring called [novelty detection](https://doi.org/10.1098/rsta.2006.1928): measure how far the current behavior sits from a healthy baseline, in units of "how surprising is this." So that's what I built: a detector that fits a picture of "healthy," then flags a change when the sensors stray far enough from it, and reports **how confident** it is — including honestly saying "something's off but I can't tell you what."

The *naming* rung (soft vs. weak vs. lying) is different in kind. To do that well, the system has to **learn from labeled examples** — thousands of simulated runs where we know the true answer. And here's the catch: **those examples don't exist yet**, because we haven't frozen the experiment's settings (see below), and generating data before the settings are frozen would mean training on numbers we're about to change. Building the "naming" brain now would mean building something I can't honestly train or test — a guess dressed up as a result. So I built the machine's frame, its input format, and its honest detection-and-uncertainty front, and I stopped exactly at the line where the next step would require data we've promised ourselves not to fake. The learned "naming" brain (and a second, contrasting design borrowed from a well-known robotics method called [Rapid Motor Adaptation](https://arxiv.org/abs/2107.04034)) is specified and ready to build the moment the settings freeze and the data is real.

This is the project's "don't build around absent evidence" discipline showing up in a concrete choice. It would have been easy — and dishonest — to stand up an impressive-looking neural network this session. It just wouldn't have *meant* anything yet.

**One concrete decision this produced:** how much recent history the diagnosis looks at. I proposed the robot consider roughly the **last ~1 second** of sensor history (about 500 readings) for each judgment. The reasoning is physical: our test uses a gentle ~1.25-second wiggle to "poke" the arm and reveal its condition, so the window needs to be about that long to see a full poke — but not so long that the robot is slow to notice a change. That number now unblocks "freezing" the design.

---

## What surprised me: the review process caught real scoring bugs again

Last report I showed you that the two-agent review (one drafts, the other genuinely re-reviews and edits) caught real design mistakes. It happened again this stretch — this time in the **scoring** code I'd written, and Codex caught three real ones. I re-checked each against our written contract and reproduced the problems myself before agreeing. Two are worth showing because they're the kind of subtle error that silently corrupts a result:

- **"95% of what?"** Our contract says the unknown-detector should be tuned to catch **95% of genuinely unknown cases**. My code had tuned it to the wrong 95% — accepting 95% of the *normal* cases, a different and easier target. Left in, it would have reported a rosier unknown-detection number than we actually promised to hit. Codex corrected it to the contract's meaning, and also split the tuning data from the testing data so the detector can't be quietly tuned on the very cases it's graded on. I verified both against our written spec.
- **A statistics bug that would have understated our own uncertainty.** The final result comes with a confidence interval (is the improvement real or a fluke of which scenarios we tested?). My version mishandled how we account for the randomness of *training the AI* versus the randomness of *which test scenarios* we drew — treating them as more independent than they are, which can make the result look more certain than it is. Codex restructured it correctly. This one matters because overstated confidence is exactly the failure that makes a published result fall apart later.

I also found one gap in my own earlier work while re-checking: our contract promises a specific number — *how much of the work can the robot handle while keeping its error rate under 5%* — that I'd never actually implemented in the scoring code. I added it this session. None of this changes what we're testing; it changes whether the eventual scorecard is trustworthy. The pattern from Phase 1 holds: the review isn't ceremony, and the honesty machinery keeps earning its place.

---

## What's working

- **The two halves fit and run as one honest loop.** The single most common way projects like this quietly cheat is by letting the diagnosis peek at information it wouldn't really have — a future reading, a hidden answer. We've now made that *structurally* hard: the sensing code can only reach the handful of things a real sensor could measure, delayed readings are withheld until they'd really arrive, and I re-verified all of it on a real run rather than trusting it.
- **The scoring machinery is built and battle-tested.** It exists, it's been through a real bug-hunt, and it now matches the contract we wrote in advance.
- **We're building only what we can honestly stand behind.** The clearest evidence is that I *stopped* this session at the point where going further would have meant faking data. That's the project working as designed.
- **Still inside every constraint.** Free, open-source software on the one desktop; nothing spent; nothing needing your accounts.

## What isn't working yet / what's genuinely still open

- **The central question is still 100% open.** I can't stress this enough: we have built apparatus, not findings. Strain sensing has not been shown to help. It still might come back a clean negative.
- **We can't train the "naming" brain yet, on purpose.** Everything downstream of "detect a change" — actually naming the fault, sizing it, and proving strain helps — waits on two things: **freezing the design** and then **generating the labeled data**. Both are close but not done.
- **"Freezing the design" is the current bottleneck, and it's a shared to-do.** Before we generate the real data, we lock every setting in a single file that can't be changed afterward (this is what keeps us honest — no moving the finish line). We've agreed most of it; a few items remain: exactly how long/strong the diagnostic "poke" should be, a couple of safety-related settings, and the fault severities — several of which we want a small pilot run to inform rather than guess. We're deliberately refusing to freeze a *partial* file, because once frozen it's permanent.
- **The next real risk is the learned brain itself.** Once we can train it, there's a genuine open question of whether *any* method — strain-equipped or not — can separate these faults well at realistic noise levels. The feasibility spike (last report) passed for the *raw signals*; whether a trained model turns that into reliable *naming* is exactly what Phase 2 will find out.
- **Nothing is blocked on you right now.** The Claim Sheet is still logged for your review whenever you'd like (non-blocking). No new asks this session.

## What's next

- **Me:** with the design-freeze settings converging, my next builds are the two "naming" brains (the learned attribution model and the RMA-style contrast) and — once real multi-run data exists — the automated anti-cheating tests that make the honesty checkable on the actual data files. Then training, and the first genuine measurements.
- **Codex:** the last physics-side freeze settings, and the recovery controller that uses the diagnosis — the fourth stage of the relay.
- **Toward the freeze:** a small pilot run to inform the few settings we'd rather measure than guess, then locking the design and generating the real dataset. That's the gate to the first actual results.
- **For you, eventually:** the hands-on demo the contract commits us to — pick a fault from a menu, watch a conventional robot and a strain-equipped one both try to diagnose it and keep working, side by side. It doesn't exist yet (it's Phase 2/3), but the loop it needs now runs end to end, which is real progress toward it. That, plus the second pass of your study guide, is how Phase 3 hands the finished work back to you.

I'll write the next progress report at my session 16, or sooner if a phase closes or the contract gets amended.

— Claude
