# Progress Report — Phase 0 Close

**For:** Randy (director) · **From:** Claude · **Date:** 2026-07-16 · **Trigger:** Phase 0 → Phase 1 transition

Hi Randy — this is the first progress report on *Robot Structural Proprioception*. It's written to be read straight through, no jargon walls; anything you're not expected to already know, I explain and link. It marks the moment the project crossed from the reading phase into the planning phase.

---

## The one-paragraph version

The two agents (Codex and I) have each finished an independent survey of the research field your idea lives in, compared notes, and agreed on the sharpest small question the idea can be boiled down to. I've now drafted the project's **contract** — the document that pins down exactly what we're testing and what would count as success, failure, or an in-between result — and handed it to Codex to review. Nothing is blocked, nothing needs you right now, and there's a clean honest question on the table. Below is what that question is, why it's interesting, and what happens next.

## The idea, in plain terms

Almost every robot runs on a fixed factory model of its own body — a built-in assumption about exactly how long its arms are, how stiff, how strong its motors are, what its sensors read. Real bodies don't stay fixed. Parts wear, bolts loosen, things heat up and go slightly soft, motors weaken, and the sensors themselves drift and get noisy. When that happens, a robot that keeps trusting its original model can quietly become inaccurate or unsafe — even though it's still physically capable of doing the job.

People handle this effortlessly because we have a dense, built-in sense of our own bodies — **proprioception**, the sense of where your limbs are and what they're doing without looking ([short explainer](https://en.wikipedia.org/wiki/Proprioception)). Your nervous system is constantly fusing signals from skin, muscles, tendons, and joints into an up-to-date picture of the body you actually have right now, not the one you had last year.

Your seed idea was: what if a robot had something analogous — not skin, but a sense of its own **internal structure**? Aerospace structures are already wired up with sensors that measure strain (how much a material is stretching), curvature (how much a beam is bending), and vibration. The question is whether feeding a robot that kind of internal signal lets it do three things a normal robot can't do well:

1. **Notice** that its body or its sensors have changed.
2. **Tell what** changed — was it the *structure* (a limb went soft), an *actuator* (a motor weakened), or the *sensor itself* (a reading went bad)?
3. **Keep working** — adapt and preserve as much capability as possible, instead of treating every deviation as a total failure.

The middle one — telling *what* changed — turns out to be the crux, and I'll come back to why.

## What we found in the reading phase

Both agents searched the published research independently (on purpose — two independent readings surface more than one merged one), then compared. The headline finding is encouraging for the project: **this specific question sits in a gap between six different research communities, and none of them has occupied the whole thing.** Very briefly, each community owns one piece:

- **Robot self-modeling** — robots that learn a model of their own body from experience and notice when it's wrong ([Bongard et al., 2006](https://doi.org/10.1126/science.1133687)). But they *trust their sensors* and blame every mismatch on the body.
- **Rapid adaptation** — robots that adjust within a fraction of a second after something changes ([Cully et al., 2015](https://doi.org/10.1038/nature14422)). But they lump every kind of change into one internal signal that isn't designed to say *what* changed.
- **Online system identification** — continuously re-estimating the robot's physics. But there's a proven mathematical result ([Wensing et al., 2024](https://doi.org/10.1177/02783649241258215)) that some structural changes are *invisible* to a robot's normal joint sensors — no amount of cleverness recovers them from those measurements alone.
- **Structural health monitoring** — the aerospace/civil-engineering field that reads strain and vibration to find damage. But it stops at "damage detected"; it never closes the loop to *controlling* the machine.
- **Soft-robot sensing** — robots with sensing built into their bodies, but used to figure out their *shape*, not their *health*.
- **Sensor-fault diagnosis** — the field that worries about bad sensors, but which famously can't cleanly tell a broken *sensor* apart from a genuinely changed *machine*.

The gap that unites all six is what we're calling **source attribution**: when something shifts, was it the structure, the actuator, or the sensor? That "invisible to normal sensors" result is the key — it's the reason extra structural sensing *might* genuinely add information a normal robot can't get, because strain sensors measure the bending *between* the joints that normal sensors are blind to. That's the bet the project tests.

## Where the project stands right now

We've agreed to boil your broad idea down to the smallest experiment that can actually answer it:

> On a small simulated robot arm with slightly bendy links, do a few strain/curvature sensors help it tell apart three kinds of change — a link going soft (structure), a motor weakening (actuator), and a joint sensor going bad (sensor) — better than a robot with only conventional sensors? And if it diagnoses better, does it actually *recover* better?

A few deliberate choices behind that:

- **It all runs in simulation**, on the Dandelion desktop. We're not building a physical sensor. We're testing whether the *information* such a sensor could provide is worth the trouble — the cheap way to find out before anyone spends money on hardware.
- **The comparison is rigged to be fair.** The tempting mistake is to compare a fancy structural robot against a deliberately dumb normal robot and declare victory. Instead we hold *everything* constant — same robot, same "brain," same faults — and change *only* the sensors. Any advantage then has to come from the sensor information itself, not from a better algorithm. We even give the conventional robot the richest sensor set an affordable real robot could plausibly have, so the bar for "structural sensing helps" is honest.
- **A "no" is a real result.** If the conventional robot does just as well, that's a genuine, publishable finding — it tells robot builders *not* to spend money and weight on structural sensing for this kind of problem. We've written the success and failure definitions down *in advance* so we can't move the goalposts after seeing results. (This is a core Dandelion discipline: [pre-registration](https://en.wikipedia.org/wiki/Preregistration_(science)), deciding what counts as success before you look.)

## What's newly designed (and something you'll get to try)

Part of the contract is a commitment to build you a **hands-on way to check the result yourself**, without reading the technical report. As designed this session, it's a side-by-side demo: you pick a change from a menu — *"soften link 2," "weaken motor 1," "throw off sensor 1"* — and watch two robots do the same task at once, one using conventional sensors and one using structural sensors. A live readout shows each robot's guess about what went wrong (and how confident it is, including an honest "I'm not sure"), plus how well each is still tracking the task. You'll be able to *see* whether the structural robot figures out the problem faster and recovers better — or whether they look the same, which would be the honest negative. This gets built gradually as the project runs, not slapped together at the end.

## What isn't working / what needs you

Nothing is blocked, and there are **no open requests for you** right now — I have not had to create the `director_requests.md` file yet because nothing so far requires your login, identity, or a purchase. The one genuine *technical* uncertainty ahead is whether our chosen physics simulator ([MuJoCo](https://mujoco.org)) can produce believable strain signals for a fairly stiff robot link. Stiff metal barely bends, so the strain numbers may come out tiny and noisy in simulation. Codex's very first job in the next phase is a focused test of exactly this, with a clear pass/fail bar; if MuJoCo can't do it cleanly, we have a well-understood backup ([PyElastica](https://github.com/GazzolaLab/PyElastica), a tool built specifically for bendy rods). I'm flagging it here so it's on your radar as the main thing that could force a course-correction — but it's a normal, planned-for risk, not a problem.

## What's next

- **Codex** reviews the Claim Sheet, and runs the make-or-break simulation feasibility test.
- **I** build the parts that inject realistic sensor problems (drift, temperature effects, noise) and the scoring system that measures who wins, and — once Codex and I agree the contract — I write the plain-language companion version of it and a short "study guide" to keep you fluent in the concepts as we go.
- Then real building begins (Phase 2).

The pace is deliberately unhurried — the whole point of how Dandelion works is that short honest sessions stack up over time. This one closed the reading phase and put a clean contract on the table. More soon.

— Claude
