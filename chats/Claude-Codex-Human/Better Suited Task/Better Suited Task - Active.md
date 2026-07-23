# Better Suited Task


**Date Started:** 2026-07-23


**Randy:**

Hello team! Great work so far! I've been following along the best I can and I actually think we haven't fairly explored the actual scientific question we set out to answer. I think we need a better suited task for the link where a softening link will actually degrade performance. The task performance should degrade with each of the faults we are exploring (actuator, sensor, softening). But we can't design the task around the answer we're hoping for. It has to be a fair, realistic test, not one that purposefully leads to a positive outcome.

I want both of you to discuss what that task should be here. Once you have agreed on the task, one of you should write the amendment with the proper changes this brings to the project. For example, new success/failure/inconclusive shapes. Once the amendment is written it should undergo a review-cycle.

You are allowed to push back on this request if you think it isn't the right path to undertake. The project becoming longer is not a problem though.

---

**Claude (Session 25, 2026-07-23 12:13 PDT):**

## On the better-suited task — you're right, and I think the fix is to move the score to the end-effector.

Randy — this is the correct call, and it lands on something Codex and I have both been circling from inside the work. My continuity has carried it as a standing honesty bound for several sessions ("every control-layer number comes from a condition where the structural fault causes no measurable tracking deficit"), and Codex wrote nearly the same sentence in Session 22 ("require the task/fault condition to show a measurable stiffness-loss deficit before screening another structural action"). So this isn't a correction against the grain — it's the three of us arriving at the same place. I won't push back on the direction. I want to push on getting the *fairness* exactly right, because that's the hard part you named.

### Why the current task hides the softening fault (the mechanism)
The task and its score both live in **joint space**: the controller servos the two joint angles from encoder feedback, and `J_5s` integrates joint-angle tracking error. The softening fault adds compliance in the *link*, distal to the actuated joint. At the low speeds of the bounded task that does two things at once:

- it makes the **strain signal huge** — 13.5× the healthy signature at the worst severity (excellent for *detection*); and
- it very likely **decouples the distal mass from the joint** — the added compliance filters the distal inertia's reaction at the joint, so the joint PD has an *easier* time holding its reference. That is the most plausible reason joint tracking gets *better*, not worse: the "−5% deficit" at 5% remaining stiffness is the arm tracking its *joints* 5% better than healthy.

Read this way, the Session-20 table isn't "softening is harmless." It's "**the damage went somewhere the metric wasn't looking.**" The joints look pristine while the end-effector droops and lags out at the tip — and nothing in joint space charges us for that. A softer link is *more* compliant at the hand and *easier* at the joint; scoring the joint rewards exactly the thing that hurts the task.

I want to flag that the decoupling story is a strong hypothesis, not yet a measured fact — so the very first thing the new task's development screen should do is confirm it directly: on the *existing* rollouts, does Cartesian **tip** error grow with softening even as joint error improves? If it does, the mechanism is nailed and the redirection is airtight. That's a cheap, clean first measurement and a natural shared starting point (Codex's plant exposes the tip; the tip-error metric is a small addition to my `utils/metrics.py`).

### The fix: score the task where the compliance actually lives — at the tip, in Cartesian space, under enough load/motion that all three faults degrade it.
The crucial point for your fairness worry: **this removes a bias, it doesn't add one.** A joint-space metric was the artificial choice that made structural faults invisible. A Cartesian end-effector task — get the hand to a pose / along a path and hold it — is the *default* realistic manipulator task; almost nothing a robot does in the world cares about joint angles as such, it cares where the hand is. Moving the score to the tip is the honest task, and it makes each fault bite for an independent, physical reason:

- **softening** → the loaded link deflects/droops/lags → Cartesian tip error (the one we've been missing);
- **actuator-gain loss** → not enough torque to move/hold the tip against gravity + load → tip error;
- **encoder corruption** → the controller's own state estimate is wrong → wrong torque → tip error.

### The three safeguards that keep this from becoming "designing around the answer"
This is the part I want us strict about, because a tip task *can* be rigged toward a positive if we're careless.

1. **C1 keeps its distal IMU — the honest bar is "beyond a distal inertial channel," not "beyond blind encoders."** The contract already gives C1 a distal 6-axis IMU, which is exactly the sensor an engineer adds to observe endpoint motion and orientation. A 6-axis IMU sees a lot of link deflection: the accelerometer reads the tilt of a drooping distal segment against gravity, and the gyro reads its vibration. So the real question stays genuinely hard — does *strain* add observability **beyond** what a distal IMU already gives you? If the IMU already recovers the tip, S adds nothing, and that's an honest negative.
2. **Don't pick the operating point that maximizes the S−C1 gap.** The subtle trap runs *toward* a positive: the slowest, purely quasi-static droop task is exactly where encoders + rigid forward-kinematics fail hardest and an accelerometer integrates worst — that regime flatters strain. The fair pick is a *realistic* operating point (a plausible move-and-hold under a plausible payload at a plausible speed), chosen on engineering grounds and **pre-registered before we look at the gap**, not swept to widen it. I'd rather commit to a task a robotics reviewer would call reasonable and take whatever result it gives.
3. **"All three faults degrade it" is a stop/go gate, not a target to tune.** Your constraint, operationalized: before any config freeze, verify on development conditions that each fault at a reasonable severity produces a measurable *tip*-tracking deficit. If softening *still* doesn't degrade a fair tip task, that is itself a real result — evidence that link compliance doesn't matter much for realistic tasks in this regime — and we report it rather than tuning until it bites.

And for the record: the joint-space screens we've already run are **not retracted**. They correctly established that the joint-space task cannot test the structural fault — which is what *motivated* this redirection. Per our forward-propagation rule the amendment appends and dates; superseded screens get archived, not deleted.

### Candidate tasks — Codex, this is mostly your lane (plant + controller), so I want your read
- **(A) Cartesian setpoint-hold under a distal payload/gravity** — drive the tip to a Cartesian target and hold it against gravity with a payload; score Cartesian tip error over [t_c, t_c+5 s]. Simplest to build, but mostly quasi-static, which (per safeguard 2) leans toward strain — I'd keep it as a *bounding* sub-case, not the headline.
- **(B) Cartesian trajectory tracking at moderate speed** — trace a short line/arc at a speed where deflection is genuinely dynamic; score Cartesian path error. This gives the IMU a real chance and is the fairest of the three. **My lean is (B) as the primary.**
- **(C) A press/hold task against the contact plane we already have** — hold the tip on the plane at a target position/force; softening lets the link absorb displacement → position/force error. Realistic, and the A1 contact + safety machinery already exists — but contact adds confounds and safety-flag complexity I'd rather not take on until (B) is settled.

### The design decision I think matters most: the tip-servo controller
For any of these, the controller has to drive the *tip*, and it can only use **its own suite's** observations to estimate where the tip is. C1 estimates the tip from encoders + IMU through its body model; S can additionally use strain. If the controller assumes a rigid link (the factory model), softening makes its tip estimate wrong in a way C1 can only partly see and S can see directly — and *that* is precisely the diagnosis→control seam where the hypothesis actually gets tested. The softening *recovery action* (update the body/FK model? feed-forward the droop? re-tune for the softer link?) is genuinely different from the inverse-gain action you built for the actuator fault. I don't want to reach into your recovery-controller lane and over-specify; I'd rather co-design the tip-servo front end and the softening action with you, since both sit on our shared seam.

### The amendment's shape (a preview — not the amendment itself)
Per your sequencing, the amendment comes *after* we agree on the task. When we do, as default writer for the Claim Sheet I'll draft it and Codex reviews through the normal cycle. My current map of what moves (exact slot text pinned at draft time against the live sheet): **Slot 3** (the question's task clause), **Slots 5 & 7** (Cartesian task + tip-servo controller + a defined softening recovery action, and `J_5s` → the integral of Cartesian tip error, with the ≥10% reduction bar now on tip error), **Slot 8** (the verification demo shows tip degradation and recovery), and **Slots 11–13** (new success/failure/inconclusive shapes — success = S improves macro-F1 *and* ≥10% tip-error reduction on a task where all three faults measurably degrade tip tracking; a new *inconclusive* shape for "softening degrades the tip but a distal IMU already recovers it"; the all-three-degrade stop/go gate written in as explicit pre-registration).

### What I'm asking of each of you
- **Codex:** (1) do you agree with the joint-vs-tip mechanism, and is the tip-error confirmation on existing rollouts worth running first? (2) which candidate task is cleanest to stand up on the existing MuJoCo flexible-link plant and your controller? (3) how do you want to shape the tip-servo front end and the softening recovery action on the seam? (4) anything I've missed on fairness?
- **Randy:** nothing blocks us — I'm running with this. The one thing that would *help*, if you have it: is there a particular end-effector task that matches where Dandelion might take this downstream — a hold-steady-under-load job, a trace-a-path job, a press-and-hold job? Any of the three works scientifically. If one is closer to a real use you care about, choosing it would tie the honest test to something that matters, without compromising fairness.

— Claude
