# Accessible Claim Sheet — Robot Structural Proprioception

## What this document is

This is the **plain-language companion to the project's contract.** The contract itself — the technical [`Claim Sheet.md`](Claim%20Sheet.md) — is written for the two AI agents doing the work, so it is dense and exact. This document carries **the same commitments, in ordinary language**, so you (the director) can hold the whole contract in your head without decoding the technical version. It is not a summary and it is not softened: every promise, every number, every success-and-failure line means exactly what it means in the technical sheet. If the two ever disagree, that is a bug — they are kept in sync.

It follows the technical sheet's structure: an orientation section, a one-line "contract at a glance," and then the same **fifteen numbered slots**, so you can read either document alone or move between them slot-for-slot. Where a term appears that you are not expected to already know, it is explained and given a link to a credible source you can check.

---

## The question, in ordinary language

Most robots run on a **fixed factory model of their own body** — a stored description of exactly how long each limb is, how heavy, how stiff, how its motors respond. The controller trusts that model completely. But real bodies do not stay fixed. Parts wear and loosen, joints heat up and develop friction or backlash, a limb takes a knock and goes slightly soft, a motor weakens; and the sensors that watch all of this slowly **drift** and go noisy. A robot that keeps trusting its original model can quietly become inaccurate — or unsafe — even while it is still perfectly capable, mechanically, of doing the job.

Humans cope with exactly this problem because we have a **dense, distributed sense of our own bodies**: signals from skin, muscles, tendons, joints, and the balance organs, all continuously updating an internal sense of what our body is doing and what shape it is in. Robots have almost nothing comparable. They have joint-angle sensors, motor readings, maybe a camera and one motion sensor — but no continuous, spread-out stream of information about the mechanical state of their own structure.

This project asks a narrow, concrete version of the big question in the seed: if we give a robot a stream of **internal structural sensing** — measurements of *strain and curvature* (how much its own limbs are bending and stretching under load, the same quantities aerospace structures are already wired to report) taken at a few points along its limbs — does that let it do three things a conventional robot sensor suite cannot do as well?

1. **Notice** that its body, or one of its sensors, has changed.
2. **Tell what** changed — the structure itself, an actuator (a motor/drive), or the sensor that is supposed to be watching.
3. **Keep** as much useful capability as possible after the change, instead of failing or, worse, carrying on confidently while wrong.

The entire project runs **in simulation.** We are not building a physical sensor. We are testing whether the *information* such a sensor could provide is valuable enough to justify deeper research. That distinction is the whole point of the project, and it is worth holding onto: a "no" here is a real, useful answer.

---

## The story so far, and what a win or a loss would mean

**The prior rung — what the field has already figured out.** Six separate research communities each own one piece of this puzzle, and — this is the key finding from both agents' Phase 0 literature surveys — **none of them owns the whole thing:**

- **Robot self-modeling** can teach a robot to learn and revise a model of its own body from experience (the founding demonstration is [Bongard, Zykov & Lipson, 2006](https://doi.org/10.1126/science.1133687), a robot that re-figures-out its own shape and recovers after losing a limb) — but it senses the body through joints or cameras and **trusts its sensors**, blaming every surprise on the body.
- **Rapid adaptation** methods can compensate for a changed body in a fraction of a second — the leading example is [RMA, "Rapid Motor Adaptation," Kumar et al., 2021](https://arxiv.org/abs/2107.04034) — but they compress *every* kind of change into a single control signal that is not built to say *what* changed.
- **Online system identification** re-estimates the robot's physics as it runs, but a formal 2024 result ([Wensing, Niemeyer & Slotine](https://doi.org/10.1177/02783649241258215)) proves that some structural changes are **invisible in principle** to joint-only measurements — there is a genuine blind spot no amount of clever math can fix from that data alone.
- **Structural health monitoring** — the aerospace/civil-engineering field that reads strain and vibration to find cracks and damage ([Farrar & Worden, 2007](https://doi.org/10.1098/rsta.2006.1928)) — reads exactly the signals we care about, but **stops before the control loop**: it detects damage, it does not fly the plane afterward.
- **Soft-robot and tactile proprioception** already put distributed sensing *inside* robots — impressively, [Wang et al., 2024](https://doi.org/10.1038/s41467-024-54327-6) have a soft robot that predicts its own shape and treats the mismatch as a touch — but they use it to estimate *shape and external contact*, not internal *health*.
- **Sensor-fault diagnosis** worries about whether the sensors themselves are lying, but its core tool — flagging "the measurement disagrees with the model" — by itself **cannot say whether the sensor moved or the body moved.**

**The current rung — what this project tests.** Lay those six side by side and one gap sits unoccupied in the middle: **source attribution.** When the relationship between what the robot commands, what its sensors report, and how it actually moves shifts, distributed structural sensing might supply the missing *extra, physically independent view* that lets the robot separate a **structural** change from an **actuator** change from a **sensor** change — with honest uncertainty about which — and then act on it. This project runs the **smallest controlled experiment that can tell whether that extra information is really there and really useful.** On a small simulated bendy two-joint arm: does adding a few local strain/curvature channels to an otherwise-matched conventional sensor suite improve the robot's ability to correctly name which of three change types just happened — a link going soft, a motor weakening, or a joint sensor being corrupted — under realistic sensor imperfections, and does any improvement in naming the cause translate into the arm actually recovering the task better?

**What a win would mean.** Success is a hands-on demonstration that a few cheap structural channels carry cause-separating information a rich conventional suite does not — and that this buys **measurably better recovery**. That would be real evidence that affordable robots could extend their own safe, useful life by sensing their own structure.

**What a loss would mean.** Failure is a **clean negative**: a well-matched conventional suite recovers the same information and the same performance, so the structural hardware is not worth adding for this task. This is genuinely valuable in the other direction — it tells robot builders *not* to spend cost, weight, and complexity on structural sensing where ordinary sensors already suffice. **A clean negative here is a result, not a disappointment.** And the in-between outcomes (structural sensing helps for some change types but not others, or helps you *diagnose* without helping you *recover*) are all spelled out in advance below, so a partial win can never be dressed up as a full one.

---

## Contract at a glance

| | |
|---|---|
| **What we build** | A small simulated **two-joint robot arm whose links bend** (modeled as flexible beams, not rigid bars) with **four fixed "virtual strain gauges"** along the limbs, plus ordinary robot sensors. All in simulation, on one desktop computer. |
| **What we vary (the one knob)** | Four nested **sensor suites**, from lean to rich: **C0** = joint-angle sensors + the motor commands · **C1** = C0 + a noisy motor-current reading (turned into a rough estimate of effort) + one motion sensor (IMU) on the far link — the richest set of *onboard* sensors a cheap real robot plausibly already carries · **S** = C1 + the four structural strain/curvature gauges · **O** = a privileged "oracle" that can see the simulator's hidden true state (an unbeatable ceiling, never something a real robot could have). |
| **What we compare against** | The matched conventional suites **C0 and C1** (same brain, structural sensors removed); a simple, interpretable estimator (a transparent floor); a strong learning-based adapter in the style of RMA (the tough competitor); and the oracle (the ceiling). |
| **What counts as success** | Suite **S** beats the best conventional suite **C1** on **both** layers at once: it names the cause **at least 5 points better** (on a standard four-way accuracy score, with the uncertainty range excluding "no difference," and without meaningfully hurting any single cause) **and** it recovers the task **at least 10% better** in the five seconds after a change (uncertainty range again excluding "no difference," with no loss of safety) — all under realistic sensor imperfections. Both layers are required. |
| **What counts as failure** | The matched conventional suite **C1**, given the same short adaptation time, recovers the same cause-naming *and* the same recovery — **S** adds no reliable margin. (A clean, publishable negative.) |

The fifteen slots below make every one of these commitments exact and explain the terms.

---

## Slot 1 — What we're building and what it senses

The project lives at the boundary where **robot control** meets **structural sensing.** The thing we build is deliberately small: a **two-link robot arm** whose links are modeled not as rigid bars but as **flexible beams** — slender parts that measurably bend under load. This matters because it makes "strain" a *real, physical* quantity in the simulation, not a label we paint on. The arm starts moving in a flat plane; we only add twisting on one link if the simpler flat version can't tell two change-signatures apart (the feasibility spike in Slot 9 decides this).

The robot can draw on four kinds of signal, all generated inside the simulator with believable noise and drift (Slot 7 details the imperfections):

- **Joint-angle sensors (encoders)** — where each joint thinks it is, and how fast it's moving.
- **Actuator channels** — the commands sent to the motors, always; and in the richer suites, a *noisy motor-current reading* converted into a rough torque (effort) estimate using the motor's nominal factory spec. Crucially, the actuator-weakening fault happens **after** this reading is taken — so the conventional suite is *not* simply handed the answer to "did the motor weaken?"
- **One motion sensor (IMU)** — a six-axis inertial measurement (the same kind of accelerometer-plus-gyroscope in your phone) mounted on the far link. External cameras and direct "true delivered torque" sensing are kept out of the deployable suites — they're reserved for labels or the oracle, never quietly slipped in.
- **The distributed structural "virtual gauges"** — four fixed measurement stations, two per link, each reporting local bending strain/curvature. Their positions are fixed *before* any learning happens and held fixed for the comparison (so we can't cheat by tuning them on the test). These stand in for what an embedded **fiber-optic strain array** (see Slot 7) could measure on a future real robot.

One more fact worth knowing: **the data does not exist yet, so we generate it ourselves.** Both surveys found that no freely-licensed dataset exists that carries all of this at once — robot commands, joint sensing, distributed structural measurements, several kinds of fault, *and* the downstream control. So the project builds its own simulated benchmark and publishes the code that generates it. That gap is itself part of why the project is naturally simulation-first.

## Slot 2 — The problem, stated so it can be answered

Each existing tool falls short in one specific way: self-models trust their sensors; fast-adaptation methods blur all causes into one signal; joint-only system-ID has that proven blind spot; structural health monitoring stops before control; soft-robot sensing reads shape, not health; and fault diagnosis can't cleanly separate "the sensor lied" from "the body changed." So the concrete problem is an **information** question before it is a control question:

> On a small simulated bendy arm, do a few **local strain/curvature measurements add cause-separating information beyond a matched conventional sensor history** — enough to detect and *tell apart* a link going soft (a **structural** change), a motor weakening (an **actuator** change), and a joint sensor being corrupted (a **sensor** change), under realistic sensor imperfections — and does any resulting improvement in naming the cause translate into **better recovery of the task**?

The experiment is deliberately built so that the **sensor suite is the only thing that changes** between comparisons; the robot, the estimating "brain," the controller, the faults, and the motions are all held identical. That is what lets us attribute any measured advantage to *the information the sensors carry*, and not to a difference in the software reading them.

## Slot 3 — The one sentence we could claim if it works

> **In a compliant (bendy) robot, a small set of physically-grounded local structural measurements provides cause-separating information about body, actuator, and sensor changes that a matched conventional sensor suite cannot recover — and this advantage in naming the cause translates into faster or safer recovery.**

The claim is deliberately narrow. It is *not* "a robot can sense strain" (already known), *not* "a robot can adapt after damage" (already known), and *not* a grand claim that the robot "understands its body." It is the **extra-information** claim, with the recovery clause attached so the word *advantage* is actually earned. Its honest alternatives — it works for some change types but not others, or it improves diagnosis without improving recovery, or it fails outright — are all pre-declared in Slots 11–13, so we can only assert the claim as strongly as the evidence supports.

## Slot 4 — The boundaries we work inside

- **Simulation only.** No physical parts, no robot hardware, no paid datasets, no paid services, no lab equipment. The simulated sensors must represent quantities a *future* real system could plausibly measure, but we are not producing a manufacturable sensor.
- **One desktop, free tools only.** Everything runs on the shared Dandelion desktop (Slot 10), using only free, open-source software whose licenses permit commercial use. Anything with unclear licensing is treated as off-limits until the question is settled.
- **"Smallest sufficient" applies to the final answer, not the search.** The version we would eventually ship is the smallest one that meets the success bar — but that does *not* mean we stop searching early. A "no signal" from an undersized model is evidence about *that model*, not proof the signal is absent; Slot 9 commits us to scaling up the search when warranted.
- **Excitation-vs-safety tension is real.** To identify what changed, a robot needs *informative motion* — but the vigorous motions that best reveal structural signatures are exactly the ones a possibly-damaged robot should avoid. The experiment has to respect this rather than assume rich, safe motion is free.
- **Honest evaluation.** We split training and testing data by *whole runs and whole fault settings* (never by chopping one run into train/test pieces, which would let the model cheat); we keep realistic sensor imperfections in rather than idealizing them away; we put environmental confounds in both healthy and faulty data; and we record every excluded run with its reason.
- **Licensing.** Released code is **MIT**-licensed (very permissive); released writing is **CC BY 4.0** (free to reuse with attribution). All software dependencies permit commercial use. No restrictive-license exception is needed right now; if one ever is, it will be named along with the limits it creates.

## Slot 5 — How we'll actually do it

The core method is a **matched sensor-suite ablation** — a fancy name for a simple, honest idea: run *the exact same estimating brain and controller* on each sensor suite (C0, then C1, then S, with the oracle O as a ceiling), and ask what the added structural channels in S buy over the strongest conventional suite C1. Because only the sensors change, any advantage is attributable to information, not to a smarter algorithm.

**The three change types (mapping onto the three "causes"):**
- **Structure** — a section of a link goes soft (localized stiffness loss).
- **Actuator** — a joint's drive weakens, and — importantly — this happens *downstream* of the motor-current reading, so the conventional suite doesn't get the answer for free.
- **Sensor** — a joint's encoder starts lying (bias, drift, or dropout).

Each is applied one at a time first; then at least one **held-out "compound" case** (two changes at once) is reserved as a surprise generalization test. A **healthy** (nothing-wrong) case is always present, and the robot is always allowed to **abstain** — to answer "I'm not sure" — because forcing a guess on every run would overstate what it actually learned.

**What we compare (including the strong competitors, not just weak ones):**
- The **matched brain** (a compact temporal neural network) run identically on C0, C1, and S — the main vehicle for the comparison.
- A **simple, interpretable estimator** — a transparent floor, so a win isn't just "a bigger black box beat a smaller one."
- An **RMA-style adapter** — the *strong* competitor: it gets the same conventional sensor history but optimizes an internal control signal, not labeled cause-naming. This directly tests the deflationary possibility that "ordinary sensors plus fast adaptation already recover whatever structural sensing was supposed to add."
- An **oracle controller** that is simply *told* the true fault — the ceiling, never a fair baseline.
- [Intelligent Trial-and-Error](https://doi.org/10.1038/nature14422) (a famous "recover like an animal" method) is included only as a **recovery reference point**, not a matched competitor, because it plays by different computational rules.

**Getting the robot to reveal itself (excitation).** A family of ordinary task motions, run two ways: an *ordinary-motion-only* condition (does normal movement already carry enough information?) and a *short, safe diagnostic wiggle* condition (a brief, bounded probing motion). Exactly how much probing to allow is a detail deliberately left for early Phase 2.

**Recovery.** The controller is reconfigured based on the robot's *estimated* fault, and compared against a control-only adapter that gets the same history but no explicit "name the cause" objective — so we can tell whether *knowing what changed* helps beyond simply *adapting to* it.

**Checking the signals are real.** The strain/curvature values from the main simulator are cross-checked against an **independent physics calculation** (a textbook beam calculation or a Cosserat-rod model — Slot 9), plus refinement and noise sweeps. This guards against the embarrassing failure where the "structural channel" turns out to be a disguised copy of the joint angles the conventional suite already had.

Every one of these choices traces back to the Phase 0 surveys and their source ledgers, not to memory.

## Slot 6 — Why it matters and who it helps

Dandelion builds toward **affordable technology for everyday people**, and general-purpose robots are heading into homes and small workplaces — places where no technician will recalibrate them after every knock, wear event, or hot afternoon. If a few cheap embedded structural channels carry cause-separating information, that is a concrete, affordable route to robots that **extend their own safe, useful life**: noticing and adapting to wear, damage, and sensor drift instead of failing — or, worse, carrying on confidently while wrong. And if the result is null or bounded, that is *equally* useful in the other direction: it tells builders *not* to spend cost, weight, and complexity on structural sensing where ordinary sensors already suffice — and, in the bounded case, maps exactly which change types make the extra sensing worth it. Either way the project feeds a possible larger Dandelion program on mechanically self-aware robots, at the mission's bar: the smallest sufficient sensing that runs on hardware people already own.

## Slot 7 — How *we* (the team) will know if it worked

This slot is the **team's** confidence path — the measurements and statistics that tell us whether the claim holds. (Your hands-on path is Slot 8.)

**What we measure it on:** the self-generated simulated benchmark — the bendy two-link arm, the four sensor suites, the three change types plus healthy and a held-out compound case, and the range of motions/payloads/contacts — with the generation code published.

We report **two separate layers of results**, and never blend them into one score (so a diagnosis result is never mistaken for a control result):

**Layer 1 — Did it name the cause correctly?**
- The headline number is **four-way macro-F1** across {healthy, structure, actuator, sensor}. *F1* is a standard accuracy score that balances two errors — false alarms and misses — into one number between 0 (worst) and 1 (best); *macro* means we average it evenly across the four causes so a rare cause counts as much as a common one ([what F1 and macro-averaging mean](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)). On the confirmatory runs, choosing to *abstain* on a known cause counts as an error in this headline number — so the robot cannot inflate its score by refusing the hard cases.
- Per-cause breakdowns and confusion tables, paying special attention to the genuinely hard confusions (structure-vs-actuator, structure-vs-sensor).
- **Detection delay** — how long after a change before it's noticed.
- **Localization error** — when it matters *which* link or joint changed.
- **Calibration** — whether the robot's stated confidence is *honest*: when it says "80% sure," is it right about 80% of the time? Measured with standard scores (Brier, and others) and [reliability diagrams](https://scikit-learn.org/stable/modules/calibration.html).
- **Abstention behavior, measured on its own terms** — how good the "I'm not sure" option is, using risk-vs-coverage curves and a few fixed operating points, plus how well it flags the never-before-seen compound fault as genuinely unknown. Keeping calibration, abstention, and unknown-detection as *separate* measurements follows recent best practice for exactly this kind of "allowed to abstain" system ([Traub et al., 2024](https://papers.nips.cc/paper_files/paper/2024/hash/047c84ec50bd8ea29349b996fc64af4b-Abstract-Conference.html)).
- **Held-out generalization** — performance on severities, motions, payloads, and noise draws it never trained on, plus at least one unseen fault combination.

**Layer 2 — Did it recover the task better?**
- The headline is the **five-second post-change integral of absolute tracking error** — plain-language: over the five seconds right after a change, add up how far off the arm is from where it should be. Lower is better.
- Tracking error before, immediately after, and after adapting; recovery time; how much of healthy performance it gets back; control effort, and any unsafe or constraint-violating excursions.
- And centrally, the **paired difference between S and C1** on identical runs, with an uncertainty range.

**How we keep the statistics honest.** We separate development, pilot, validation, and final-test data by whole runs and whole fault settings. Before we generate the final confirmatory data, we **freeze** everything that could be tuned — gauge positions, model settings, decision thresholds, the analysis window, the full list of scenarios and random seeds — into a versioned configuration. We use at least five independent training runs (seeds) and report **paired 95% confidence intervals** computed by a **[hierarchical bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)** — a standard resampling method for putting an honest uncertainty range on a result, here respecting the nested structure of the data (many scenarios within each seed) and the fact that S and C1 are tested on the *same* scenarios.

**The success numbers, fixed in advance.** "Better than chance" (25% for four causes) is far too weak a bar. For the full success claim we require, set *before* we run any pilot:
- **S improves four-way macro-F1 over C1 by at least 0.05 (5 points) absolute**, with the paired 95% interval excluding zero;
- for **every single cause**, S does not do *worse* than C1 by more than a small **−0.02 margin** (a "non-inferiority" guard — a term from clinical trials meaning "allowed to be no worse than this much" — so an average gain can't hide a regression on one cause);
- **and** S reduces the five-second post-change tracking-error total by **at least 10%**, paired interval excluding zero, with no safety regression.

These are deliberate *design minimums* — the smallest effects we'd consider practically meaningful — chosen before any data. The pilot's only job is to tell us *how many* runs we need to measure such an effect reliably; it is explicitly **not** allowed to choose what counts as success. Anything short of all of the above (helping diagnosis but not control, or only for one change type) is a Slot-13 result, not success.

## Slot 8 — How *you* (the director) can check it yourself

This slot is **your** confidence path — the hands-on thing we commit, before we start, to build so you (and anyone who downloads the reproducibility packet) can verify the result **without reading the technical report end to end.** It lives inside the reproducibility packet and is built gradually, not slapped together at the end.

**The artifact: a small interactive side-by-side demo.** You pick a body change from a short menu — *"soften link 2 by 30%," "weaken actuator 1," "bias encoder 1"* — and watch **two copies of the arm run the same task at once**: one driven by the conventional suite **C1**, one by the structural suite **S**. A live panel shows, for each copy, (a) its current **guess at the cause and its confidence** (or an honest *"not sure"*), and (b) a live **trace of its tracking error**. You see directly whether the structural robot names the right cause **sooner and more often** and **tracks better after the change** — or whether the two are indistinguishable, which is the honest negative shown *as* a result. A scripted version produces the same comparison as a set of high-resolution figures for the reports.

What you do: trigger a few changes, watch which robot correctly says *what* happened and *keeps doing the task*, and watch the confidence/abstain behavior to confirm the system declines to guess when the signals are genuinely ambiguous. Committing to this artifact now also disciplines the whole build — the experiment has to be designed so this comparison is even *possible* to show cleanly. If results change what it should show, we update this slot through the normal amendment process.

## Slot 9 — The build plan (start small, and know when to scale up)

We start with the smallest version that could plausibly work, and commit *in advance* to climbing **two ladders** — model size and physics fidelity — rather than betting on one fixed design.

**The feasibility spike comes first — it is the gate.** Before committing to any particular simulation engine, we build the bendy two-link arm in [MuJoCo](https://github.com/google-deepmind/mujoco) (a fast, free, widely-used physics engine) and test the specific mechanics that can actually represent a *bending beam* — its cable/rod elasticity, and if needed a slender 3-D flexible-solid model. (An important correction from the review: MuJoCo's generic flexible element is mostly a *stretchy line*, not automatically a bending beam or a strain sensor, so the spike has to test the real candidates rather than assume.) The virtual gauges are computed from the simulator's independent deformation coordinates and cross-checked against a textbook beam/Cosserat calculation — never copied from the fault or reconstructed from the corrupted sensor.

**The spike passes only if:** the computed signals are stable as we refine the simulation, and the histories genuinely contain *distinguishable* fault signatures at believable signal-to-noise, **at realistic (metal-like) stiffness** — not just at exaggerated floppiness. For structural and actuator faults, at least one gauge must show a repeatable, above-the-noise response. The sensor (encoder) fault is different by nature: a lying sensor does *not* physically bend the structure, so its signature is a **repeatable disagreement** between the corrupted sensor and the independently-evolved physical/gauge history — that relationship, not a fictitious strain, is what the spike must show. The signals must survive a realistic **fiber-optic strain-sensor noise floor** (see below). If the native candidates can't clear the gate, we fall back to a **[PyElastica](https://github.com/GazzolaLab/PyElastica) Cosserat-rod model** (a well-established way to simulate bending slender rods); full heavy-duty FEM stays offline, for validation only. **No engine is committed until the spike passes.**

- *Fidelity ladder:* native MuJoCo cable/rod (or slender 3-D flex) → PyElastica reduced model (fallback) → offline FEM / independent beam calculation (ground truth, never in the live loop).
- *Model-size ladder:* (1) a compact temporal network (~tens of thousands of parameters) plus the simple baseline; (2) a larger network; (3) an ensemble/probabilistic version for *honest confidence and abstention*. We climb a rung when there's partial signal worth strengthening **or** when a bigger model could plausibly capture a signal a smaller one missed. We stop only when the result holds across the ladder, the hardware ceiling is genuinely reached, or there's a stated *scientific* reason a bigger model wouldn't help — because "a bigger model wouldn't help" is itself a claim that has to be justified, not assumed.

**The hardware ceiling (named):** a single NVIDIA RTX 5060 Ti (16 GB), 32 GB RAM, one 8-core CPU. The models here are far under that ceiling, so our compute story is *breadth* — many faults, severities, seeds, and noise draws run in parallel — rather than one giant network. The ceiling matters most for how much simulation data we can generate, which the spike will size.

## Slot 10 — The computer and software environment

- **Machine:** the dedicated Dandelion AI-agents desktop — Windows 11; AMD Ryzen 7 8700F (8 cores/16 threads); NVIDIA RTX 5060 Ti with 16 GB of video memory; 32 GB RAM; fast local + external SSD storage.
- **Python:** version 3.12 in a project-local environment (`venv`); every Python command uses that environment, never the system default, so the versions stay pinned and reproducible.
- **Core free libraries (all commercial-use-friendly, versions pinned when installed):** MuJoCo (physics), PyElastica (bending-rod validation/fallback), NumPy/SciPy (math), PyTorch (neural networks, GPU-accelerated — GPU availability verified, not assumed), matplotlib (figures at high resolution). Heavy FEM tools, if used at all, run offline for validation only.
- **Portability discipline:** no hard-coded machine-specific paths; all such paths passed in explicitly; outputs written to project-relative locations; shared code in a common module; and the reproducibility packet must run start-to-finish from a fresh install **on a copy of the packet folder alone** — the real test of "someone else can reproduce this."

## Slot 11 — What would count as success

Fixed and pre-declared, **before any pilot or real result is seen:**

> Suite **S** improves held-out four-way macro-F1 over the strongest conventional suite **C1** by **at least 0.05 (5 points) absolute**, with the paired 95% interval excluding zero and no cause doing worse than the small −0.02 margin; **and** S reduces the **five-second post-change tracking-error total by at least 10%**, with its paired 95% interval excluding zero and no increase in unsafe or constraint-violating behavior; **and** both hold **under realistic imperfections** (sensor drift, temperature cross-effects, and held-out severities/motions/payloads). All three conditions are required. A win on diagnosis alone, or only for one change type, or only under idealized sensors, or only on data like the training data, is **not** full success — it is a Slot-13 outcome.

## Slot 12 — What would count as failure

Pre-declared. **A clean failure is a public artifact.** Two distinct failure shapes, and the difference between them matters a great deal:

- **Failure of the hypothesis (the scientifically interesting negative).** The matched conventional suite **C1**, given the same short adaptation, recovers the **same cause-naming and the same recovery** as **S** — no reliable margin — under fair, realistic conditions. Conclusion: for this task and these change types, distributed structural sensing adds nothing beyond a rich conventional suite, and the extra hardware isn't justified. This is reported plainly as the headline result. It is a *real answer*, and it saves other builders the effort.
- **Failure of the method (must be disclosed, never dressed up as a hypothesis result).** The feasibility spike can't produce distinguishable fault signatures at believable signal-to-noise at all, **or** the simulator's "structural channel" turns out to be a disguised echo of the joint angles / secretly leaks the fault. In that case the simulation *cannot fairly test the question*, and we say exactly that — rather than reporting a hollow negative or a fake positive. The fix is the fidelity ladder or an amended plant, **not** a quiet downgrade of the claim.

## Slot 13 — What would count as inconclusive or partial

The "not this, not yet" shapes — pre-declared so a partial win is never reported as a full one:

- **Diagnostic-only.** S names the cause better, but that does **not** turn into better recovery over C1. Useful for monitoring; **not** evidence of a control advantage. (This is exactly why we keep the two result layers separate.)
- **Change-type-specific / bounded.** The benefit shows up only for some change types — say, structural stiffness changes — and not for actuator or sensor faults. This sharply maps *where* structural sensing is worth adding, and is a genuinely useful bounded result.
- **Fragile to real-world imperfections.** A benefit that exists under idealized conditions but **vanishes** under plausible drift, temperature effects, sensor-placement error, or model mismatch — or that turns out to depend on privileged simulator information leaking in. Reported as inconclusive, pending a cleaner test — not as a positive.
- **Only with special probing.** Cause-naming works only under the dedicated diagnostic-wiggle condition and fails under ordinary task motion — a practical caveat on *when* the information is actually available.

## Slot 14 — The minimum we must produce to call it done

The project is complete only when all four required artifacts exist and meet the contract's bar:

1. **Technical Report** (formal, field-facing) — the full rigorous account: the question and its place in the six-community gap; the simulated benchmark and its generation code; the matched C0/C1/S/O comparison with matched model sizes *and* the size sweep; the two result layers with their pre-declared bars; held-out and realistic-imperfection results; the independent validation of the structural signals; every excluded run named with its reason; and the honest headline (positive / bounded / null) at its true strength.
2. **Reproducibility Packet** — self-contained, runs start-to-finish from the packet folder alone on a fresh install; includes the generation and analysis code, configurations, a data-access note, and the **Slot-8 hands-on demo.**
3. **Accessible Piece** — the same work for a general reader, honest and jargon-free (the piece the director shares publicly).
4. **Study Guide** — director-facing, in two passes (one now at Phase 1 close, one at the end under a strict no-spoiler rule).

Plus the **Live-Run README** — the public front page — resolving from its live "in progress" state to an honest concluded landing page that leads with the result and how to check it.

## Slot 15 — Possible ways this could pay off (honest)

- **If it succeeds as scoped:** no *direct* revenue — the immediate value is a research signal (a validated, open reference implementation and benchmark for cheap structural self-sensing) that de-risks a larger program and could seed a reusable, MIT-licensed self-monitoring library other builders adopt. Honest entry: **none identified directly** for the small simulation project itself.
- **If it succeeds and later scales:** a licensable or supported **"structural proprioception" self-monitoring layer** for low-cost robot arms — a module that extends safe service life by detecting and attributing wear/damage/sensor-drift on affordable hardware, squarely in line with Dandelion's affordable-technology mission.
- **If it's a clean negative:** no monetization from the result itself, but real value in the negative — it prevents wasted hardware spend downstream, and there's reputational value in being a team that publishes honest negatives. Not a revenue line, and we won't pretend it is.

---

*A note on staying honest about the framing.* Throughout, the value proposition is **richer information from structural sensing**, not the romantic idea that "the body computes" — a distinction the field itself is careful about ([Müller & Hoffmann, 2017](https://doi.org/10.1162/ARTL_a_00219)). If you ever see the project drifting toward the grander claim, that is a signal to pull it back to the narrow, testable one this contract commits to.

*This document is kept in exact sync with the technical [`Claim Sheet.md`](Claim%20Sheet.md). If the contract is ever amended, this companion is updated in the same session.*
