# Progress Report — Session 16 (Phase 2, mid-execution)

**From:** Claude · **Date:** 2026-07-21 · **Project:** Robot Structural Proprioception

*A director update, not a technical paper. If any sentence sends you to look something up, that's my failure — every leaned-on term has a plain explanation and a link. Meant to be read start to finish in one sitting. It picks up where my session-8 report left off.*

---

## The one-paragraph version

Since my last report the apparatus went from "three-and-a-half of four stages built, but untrained and unrun" to a **complete relay that runs end to end as one wired machine** — the simulated arm moves, imperfect sensors report, a diagnosis socket decides, and a recovery controller acts on that decision — with the whole control chain now pinned by an automated test, so the trained "diagnosis brain" can later drop into a socket whose behavior is already locked down. Along the way we solved the problem I flagged last time as the project's live risk: the useful signal was **nearly invisible** — buried roughly 90× under the sensor noise — and we found a gentle, honest way to make it stand out (this is the thing I most want to teach you this session). We also got our **first concrete hint of where strain sensing might actually earn its place**: in a pilot run, the strain-equipped robot reliably noticed a *softening link* that the conventional robot was completely blind to. I'm going to be careful with that sentence, because it's the most encouraging thing we've seen and therefore the easiest to overread. **There is still no result.** What we have is a far more complete and far more honest machine, one genuinely promising early signal, and the same discipline holding firm: the part that would let the robot *name* a fault still isn't built, because the data needed to train it honestly doesn't exist until we freeze the design — and freezing the design is still the bottleneck.

---

## A 20-second refresher

We're testing whether a few cheap **strain sensors** (they feel how much the arm is bending) give a robot information a normal robot doesn't have — enough to tell apart three kinds of trouble: a link going **soft**, a motor going **weak**, or a joint sensor **lying** — and whether knowing which one actually helps the robot keep doing its job. A clean "no" is a real, publishable result. Every setting is locked *in advance* so nobody can move the finish line after seeing the race.

---

## Where the project stands right now

Last time I described the system as a relay: **arm physics → sensors → diagnosis → controller**, with three-and-a-half of the four stages built but nothing trained or run. The headline change since then is that **all four stages now exist and are wired into one continuous machine**, and the seam between "decide" and "act" — the part that used to be a promise — is now real code with a test standing guard over it.

Concretely:

- **Arm physics → sensors → diagnosis-socket → recovery controller** all connect and run one control step at a time, with no ability to peek at the future (the honesty property I described last time still holds and is re-verified).
- The **recovery controller** — Codex's stage, the "what do I do about it" behavior — now exists and plugs into the socket I'd built for it. When the diagnosis is confident a *motor* is weak, it compensates at that joint; when it suspects a *structural* change, it eases off globally; when the diagnosis only says "something's off" without naming it, the controller correctly does **nothing** drastic. That last point matters: a robot that yanks itself around every time it's merely *unsure* is more dangerous than the fault.
- I built a **shared test that drives this whole chain end to end** and checks that each of those behaviors actually happens through the real machinery, not just in theory. That test is now the guardrail: the trained brain, when it arrives, drops into a socket whose control behavior is already fixed and verified.

So the relay is now four-of-four stages built and connected — but the **middle is still deliberately hollow**. The piece that *names* the fault (soft vs. weak vs. lying) is still not built, for exactly the honest reason from last time, which I'll return to at the end.

---

## The idea I most want to teach you this session: how we made an almost-invisible signal visible

Last time I named the project's biggest live risk in plain terms: the whole thing only works if the strain sensors can actually *see* the fault. This session's most important conceptual work was confronting that head-on — and the finding was worse than we feared before it got better.

**The problem: the signal was tiny.** When a link softens slightly, the extra bending it produces during ordinary motion is genuinely small — small enough that it sits roughly **90 times below** what a single noisy sensor reading can resolve. Passively "listening harder" doesn't rescue it: if the thing you're listening for is quieter than the hiss, more listening just gives you more hiss. If that were the whole story, the project would be over — strain sensing couldn't help because it couldn't even *detect* the change.

**The fix is a genuinely lovely old idea, and it's the thing I want you to walk away understanding.** Instead of waiting passively for the fault to reveal itself, the robot gives its own arm a **gentle, rhythmic nudge** — a tiny push at the tip, on and off at a fixed, known rhythm (about 0.8 times per second). Then, when it reads the strain sensors, it pays attention *only to the part of the signal that wiggles at exactly that rhythm, in step with the nudge*. Here's why that works: random sensor noise doesn't care about our rhythm, so when you average the in-rhythm part over a full cycle, the noise drifts toward zero — but the arm's real response *is* locked to the rhythm, so it adds up instead of cancelling. You've effectively told the sensor "ignore everything except the answer to the specific question I'm asking, at the specific beat I'm asking it." This is exactly the trick physicists use to pull impossibly faint signals out of loud noise; the instrument that does it is called a [lock-in amplifier](https://en.wikipedia.org/wiki/Lock-in_amplifier), and it's a workhorse of the physics lab.

**And crucially, the nudge is gentle enough to be safe.** The push we settled on is about **0.05 newtons** — roughly the weight of a US nickel resting on the fingertip — applied for a single ~1.25-second cycle. We checked (Codex's mechanics work) that this clears the "now the signal is visible" bar with comfortable margin *and* stays well inside the arm's safety envelope: it doesn't overspeed a joint, over-bend a link, or push the arm outside its safe reach. So the answer to last time's biggest worry is: **yes, in the clean case the signal can be made visible, and made visible safely, without a heroic shove.**

I want to be honest about the ledger here, because this is where honesty earns its keep:

- That "comfortable margin" is measured in the **clean, idealized** version of the signal. When we then ran the same idea on *realistic, noisy* sensor readings — the version a real robot would actually see — the strain suite still caught the faults it was supposed to (in the pilot, it correctly flagged the target fault the large majority of the time), but the margin is thinner and the settings that make it work still need to be pinned down on a **larger, fairer sample** than a pilot provides. I'll say more under "what isn't working."
- Everything in this section is about the first rung of the ladder — **noticing a change** — not yet about **naming** it. Getting the arm to reliably say "*this* is a soft link and not a weak motor" is the trained-brain job that still waits on the freeze.

---

## The first real hint of where strain might actually help — stated carefully

Here's the encouraging part, and I'm going to fence it properly.

In the noisy pilot, we compared the **strain-equipped** robot against the **conventional** robot on the same faults. For a weak motor or a lying sensor, both robots could tell something had changed — those faults leave fingerprints an ordinary sensor suite can pick up. But for a **softening link**, the conventional robot was essentially **blind**: in the matched comparison, its ability to catch that fault bottomed out at zero, while the strain-equipped robot caught it reliably. That is *exactly* the shape of result the whole project is betting on — extra bodily sensing revealing a kind of change that conventional sensing structurally cannot feel, because a soft link deforms the body without necessarily disturbing the motor currents or joint angles a normal robot watches.

Now the fences, because this is the easiest place in the project to fool ourselves:

1. This is **detection** ("something structural changed"), not the full four-way **naming** the headline result requires. Naming still needs the trained brain and the frozen dataset.
2. It's a **pilot**, on a small sample, with settings we have explicitly *not* frozen. It is a hypothesis sharpening into focus, **not** a confirmed result. The confirmatory run is precisely what will decide whether this hint survives contact with a fair, pre-registered test.
3. The very thing that makes it exciting — that conventional sensing scores zero here — is also a reminder of how the honest negative could still arrive: if a trained model turns out to squeeze the same information out of the conventional suite after all, or if the advantage evaporates under harder noise.

So: the most promising thing we've seen, held at exactly arm's length until the frozen experiment can confirm or kill it.

---

## Safety got its own careful workout this session

My actual hands-on work this session was reviewing a piece of Codex's safety machinery, and it's worth a sentence because it shows the standard in motion. We're adding the ability to simulate the arm's fingertip **touching a surface** — because a real robot that's diagnosing itself while also bumping into the world needs its safety limits to account for contact forces, not just its own motion. Codex built a careful screen that finds the gentlest contact setup producing one brief, bounded touch in every scenario while never tripping a safety limit, and explicitly refused to let an open-loop safety check masquerade as a real result. My job was to **independently reproduce it** — I re-ran the whole thing from my own code, drove the simulated arm myself, and confirmed every number matched to eleven decimal places, that the "no-contact control" case genuinely produces no contact, and that the one disqualified setting really does misbehave the way the screen says. It all held up, and I approved it. This is the two-agent review discipline you've seen before, doing its quiet job: nothing enters the record until the other agent has rebuilt it and agreed.

---

## What's working

- **The full relay runs as one honest machine.** All four stages connect and step forward in real time without peeking at the future, and the decide→act seam is now real and test-guarded. The trained brain has a fixed, verified socket to land in.
- **The signal-visibility problem has a credible, safe answer.** The gentle rhythmic-nudge idea lifts the fault signature above the noise in the clean case with margin to spare, without any unsafe shove — directly answering last report's biggest open worry.
- **We have a real hint, not just apparatus.** The strain suite noticing a structural change that conventional sensing can't is the first evidence pointing at *where* the payoff would come from, if it's real.
- **The honesty machinery keeps earning its place.** Independent reproduction caught nothing to fix this session — but only because it was actually done, from scratch, rather than assumed.
- **Still inside every constraint.** Free, open-source software on the one desktop; nothing spent; nothing needing your accounts.

## What isn't working yet / what's genuinely still open

- **The central question is still 100% open.** I'll keep saying this until it isn't true: we have a machine and a promising hint, not a finding. Strain sensing has not been *shown* to help. A clean negative is still entirely possible.
- **We still can't train the "naming" brain — on purpose.** Everything past "notice a change" — naming the fault, sizing it, and proving strain helps — waits on freezing the design and then generating the labeled data. Same line I refused to cross last time; still refusing.
- **Freezing the design is still the bottleneck, and the pilot has made the remaining list sharper, not shorter.** We now know precisely what's left to pin: the diagnostic settings need calibrating on a **much larger healthy sample** (the pilot's "false-alarm rate" rested on a single event in ~50 runs — far too thin to trust), plus the fault-severity grid, a few safety constants, and the new contact profile. We are deliberately refusing to freeze a *partial* design, because once frozen it's permanent — so this is careful, not slow-for-its-own-sake.
- **The margin under realistic noise is real but not yet nailed down.** The clean-case comfort shrinks under honest noise, and the settings that recover it need to prove themselves on a fair sample before we'd stake anything on them.
- **Nothing is blocked on you right now.** The Claim Sheet is still logged for your review whenever you'd like it (non-blocking). No new asks this session.

## What's next

- **Me:** my next real build is the trained "naming" brain (the learned attribution model, plus a contrasting design borrowed from a robotics method called [Rapid Motor Adaptation](https://arxiv.org/abs/2107.04034)) — and it stays on the shelf until the design freezes and real data exists. Until then my lane is keeping the diagnosis front and the scoring machinery honest and ready. When the data is real, I also build the automated anti-cheating tests that make the honesty checkable on the actual files.
- **Codex:** the matched contact-enabled comparison and the evaluation-sized controller test — the pieces that turn "the machine runs" into "here's how much better, with honest error bars."
- **Toward the freeze:** the larger calibration runs that turn the pilot's hint into a pinned-down design, then locking everything in a single unchangeable file and generating the real dataset. That freeze is still the gate to the first genuine results.
- **For you, eventually:** the hands-on demo the contract commits us to — pick a fault from a menu, watch a conventional robot and a strain-equipped one both try to diagnose it and keep working, side by side. It still doesn't exist (it's Phase 2/3), but every stage it needs now runs, and the decide→act seam it depends on is built and verified. That, plus the second pass of your study guide, is how Phase 3 will hand the finished work back to you.

I'll write the next progress report at my session 24, or sooner if a phase closes or the contract gets amended.

— Claude
