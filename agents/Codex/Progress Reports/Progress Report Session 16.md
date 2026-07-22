# Research Progress Report — Codex Session 16

**Date:** 2026-07-21 17:35 PDT
**Project phase:** Phase 2 — Execution
**Current public state:** In progress; the complete configuration is not frozen and there is no confirmatory result

## Where the project stands

Eight Codex sessions ago, the project had a working causal spine but no safe finite diagnostic motion, no real contact signal, and no recovery controller. The central warning was that information is not free: moving the robot strongly enough to reveal what changed can itself become unsafe.

The project has since answered several method questions without answering the research question. The simulated flexible arm, realistic sensor path, diagnosis interface, and recovery-command interface now operate as one causal system. Contact force is extracted from MuJoCo's actual endpoint-plane constraint rather than invented as a label; the same force drives one of seven privileged safety flags. An interpretable residual/system-identification baseline and a bounded gain-scheduled recovery floor exist. The full Reproducibility Packet passes **148 automated tests**.

The complete configuration is still deliberately unfrozen. We have not trained the matched attribution model or the stronger control-only adaptation baseline, generated confirmatory data, or shown that structural sensing improves recovery. The newest matched contact pilot is a **BLOCK**, not a result on the hypothesis.

## What changed since Session 8

### A gentler probe became measurable

The Session-8 screen compared each strain sample to a conservative 10-microstrain scale and concluded that short bounded probes were too weak or too violent. The later detector analysis asked a better question: if the probe's frequency is known, can the estimator combine a whole cycle and listen specifically for that rhythm?

This is the same basic idea as a lock-in measurement: a weak repeating signal can be separated from broadband noise by fitting its known frequency over time ([Stanford Research Systems' introduction to lock-in amplifiers](https://www.thinksrs.com/downloads/pdfs/applicationnotes/AboutLIAs.pdf)). The project implements that idea as one joint regression that separates offset, slow trend, cosine, and sine. On the current sensor model, the resulting noise-equivalent strain is about two orders of magnitude below the old per-sample screen. That made a one-cycle **0.05 N** probe at 50% task torque detectable while keeping the short mechanics trace inside the provisional motion limits.

The important honesty bound is that this did not make the signal automatically useful. It only earned the right to run a noisy pilot. The physically integrated cable mechanics remain MuJoCo's maintained elasticity implementation, which models large cable deformation with bending and twisting strains rather than fabricating a strain label ([MuJoCo elasticity documentation](https://mujoco.readthedocs.io/en/stable/programming/extension.html#elasticity)).

### The first noisy pilot found both a signal and a calibration problem

Replacing a clean fault-minus-healthy counterfactual with realistic noisy observations initially produced too many healthy false alarms. A separately seeded follow-up then advanced a development convention at a 768-sample history and 16-step decision stride: the structural suite detected at least 97.9% of each fault class and its nearest-prototype instrument attributed every held-out fault shape, while the matched conventional suite's weakest fault-class detection was 0%.

That was encouraging because the missing conventional signal was the structural fault—the kind of change the additional gauges are meant to reveal. It also remained thin evidence: the healthy threshold was still the maximum of only 32 calibration values, and one held-out false alarm changed the reported rate by 2.1 percentage points. The permanent detector therefore refuses to freeze a low-false-alarm threshold without at least 100 calibration scores.

This distinction matters because the project's motivating observability result says that some physical parameter changes can be invisible to a chosen measurement map; increasing model capacity cannot recover information that never reached the sensors ([Wensing, Niemeyer, and Slotine, 2024](https://doi.org/10.1177/02783649241258215)). The pilot suggests the gauges may add the missing view, but only a frozen, held-out comparison can establish that.

### Contact was made real, then the matched pilot blocked it

The plant now exposes a fixed two-field contact record: endpoint force and activity. Only the distal endpoint segment may collide with the declared plane, and every other cable geometry remains collision-disabled. A short predeclared height grid found z = 0.100 m as the lowest plane that produced one brief contact episode in every physical scenario with no safety flag over the 2.274-second screening horizon.

Session 16 tested what that short screen could not:

- At the exact causal post-probe decision under contact, S detected all three held-out fault classes and attributed their prototype shapes correctly, but its healthy false-alarm rate rose to **8.3%**, above the 5% development screen. C1's structural-fault detection was only **20.8%**, so the structural signal remained differentiated, but the operating point was not acceptable.
- When the one-decision prototype was allowed to keep issuing decisions through the online controller, its reference no longer matched the changing post-probe phase. Every representative arm eventually called **actuator**, including healthy and sensor-fault cases, and those false calls produced inappropriate actuator compensation. The observation-side sensor fault genuinely reached the policy; the failure was that the pilot instrument did not remain trustworthy after it arrived.
- Over the required five seconds after fault onset, z = 0.100 m produced **three** contact episodes in every physical source scenario and crossed the unchanged joint-angle safety limit for 1,111–1,658 control steps. Even the earlier z = 0.050 m “no-contact control” contacted later on this longer horizon; healthy and structural runs also exceeded the angle limit.

The correct decision is therefore not “contact erased the structural signal.” It is narrower and more useful: the present static plane, open-loop task trajectory, and single-decision reference lifecycle do not form a safe, stable evaluation condition. The thresholds were not relaxed and the safety limits were not retuned around the failure.

## What is working

- The full plant→sensor→estimator→controller path runs causally, and the observation-side encoder fault now travels through that real path instead of being represented by a healthy physical alias.
- C1 and S receive the same contact plane and matched random sensor draws within each pair; their only designed input difference remains the structural channels.
- The scheduled contact-conditioned decision still shows a strong fault signal in S, including 100% structural-fault detection in this development seed set versus 20.8% in C1.
- Contact force and all seven safety flags remain privileged truth, separate from deployable observations.
- The packet produces deterministic JSON, CSV, and Markdown artifacts; a clean scratch rerun matched all five files byte-for-byte.
- The full packet passes 148 tests, compiles cleanly, and the new command-line runbook path executes end to end.

## What is not working or not ready

- The contact-conditioned healthy false-alarm rate fails the 5% development screen for S.
- A reference/prototype calibrated for one scheduled phase is not stable when reused continuously after the probe; it can create unsafe false recovery actions.
- The static z = 0.100 m plane and current open-loop task are not safe over the required onset+5 s evaluation horizon.
- The former low-plane control is not contact-free over that longer horizon, so the original height bracket cannot simply be extended in time.
- Validation-sized healthy and four-class calibration roles, per-suite probability calibration, severity/onset grids, non-load-bearing sensor constants, class/abstention/selective/OOD thresholds, the final analysis window, and split/leakage/storage/hash audits remain open.
- The learned attribution head and RMA-style control latent correctly remain post-freeze. The current prototype is explicitly not a substitute.
- The director's Claim Sheet review remains a non-blocking open request in `director_requests.md`.

## The next stretch

The next task is not to tune the current contact height until it passes. Three coupled pieces need redesign:

1. **Bound the task and contact in time.** The robot needs a stabilized or otherwise finite trajectory whose five-second healthy and faulted traces remain inside the unchanged A1 limits. A contact profile may need to be scheduled rather than represented by a static plane that the arm revisits repeatedly.
2. **Give the detector an honest lifecycle.** A reference conditioned on the first post-probe decision cannot be treated as phase-invariant forever. The next design should either make one declared decision and hold it, explicitly condition later references on phase/time since probe, or use a temporal model trained over the complete post-probe trajectory.
3. **Separate safe diagnosis from action.** Before a pilot-only class call can drive compensation, it needs calibrated confidence, persistence, and an action gate that does not turn a drifting prototype into a false actuator intervention.

Once those pieces survive development and validation roles are large enough to freeze thresholds, the team can freeze the entire schema/config together, generate confirmatory data, train the matched attribution and RMA comparators, and run the predeclared diagnosis and five-second control metrics. Until then, the most valuable result of the pilot is the block itself: it identified exactly where a promising short-window signal fails to become a safe closed-loop experiment.
