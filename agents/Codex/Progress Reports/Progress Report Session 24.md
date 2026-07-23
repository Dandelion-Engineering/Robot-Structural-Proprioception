# Progress Report — Codex Session 24

**Report date:** 2026-07-22

**Phase:** Phase 2 — Execution

**Audience:** Project director

## The short version

Since my Session-16 report, the project has moved from a contact-enabled experiment that was unsafe and reference-unstable to a bounded, five-second-safe development task with a clear separation between **information** and **control**.

That distinction now drives the project:

- The strain gauges add strong diagnostic information about structural faults on this task.
- The structural recovery actions screened so far do not turn that information advantage into source-specific tracking improvement.
- The actuator fault has real recoverable tracking headroom, but the measured difference between the two sensor suites' current recovery commands is small on the tested development conditions.
- The newest probability screen preserves a **5.07-percentage-point** sampled difference, below the 10-point development bar, but first review corrected an overclaim: six sampled probabilities do not close a continuous response or the wider calibrated-authorization problem.

The configuration remains unfrozen. These are development screens that are shaping a valid experiment, not a research result.

## How the experiment changed

The Session-16 contact pilot failed for useful reasons. Its reference stopped being trustworthy after the scheduled decision, the robot re-contacted the plane repeatedly, and the five-second trace crossed the unchanged joint-angle safety limit. The team did not relax the limits to make the run pass.

The redesigned task now uses low-authority feedback from deployable encoder observations, makes one diagnosis at a declared time, holds that decision, and produces one brief post-decision contact episode. All four physical source conditions stayed inside the unchanged safety envelope for the required five-second horizon. This created a credible development fixture for asking two separate questions:

1. Does a sensor suite know what went wrong?
2. Does acting on that knowledge improve tracking?

Keeping those questions separate prevents a diagnostic win from being reported as a control win.

## What the information screen found

With disjoint noisy development roles, the structural-sensing suite reached **0.995 macro-F1** across the four classes, compared with **0.704** for the conventional suite. Macro-F1 computes an F1 score—the balance between precision and recall—for each class and then weights the classes equally ([scikit-learn documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)). The largest difference was structural-fault recall: **100% for the structural suite versus 8.3% for the conventional suite**. Healthy false-alarm rates were 2.1% and 4.2%, respectively.

That is a strong information result on the current development fixture. It is not yet validation-sized and does not establish a final sensor comparison.

The old structural torque-derating action failed separately: even when handed the correct diagnosis, it made five-second tracking **18.6% worse**. This is why detection, attribution, permission to act, and the outcome of acting are now kept as distinct gates.

## What the control screens found

### Structural recovery is blocked on this task

A tracking-directed inverse-stiffness action family initially appeared promising, improving structural-fault tracking by roughly 19–20% without a safety incident. The healthy robot improved slightly more under the same multiplier. The action was therefore a generic nominal-controller retune, not source-specific structural recovery, and it was blocked.

A follow-on headroom screen explained the problem. Across the tested structural stiffness losses, the no-action tracking deficit never reached the development gate; at the most severe losses, tracking became slightly better even while strain rose sharply. The gauges still reveal the structural change, but this bounded task does not provide the tracking loss needed to demonstrate recovery from it.

### The actuator fault has headroom

The headroom screen did find a recoverable actuator condition. Review then caught a units error: the screen had compared a healthy-relative **deficit** with a degraded-relative **reduction** bar as if they had the same denominator. Correcting the conversion moved the advancing condition from 50% to **25% remaining actuator gain**.

This is a good example of why the two-agent same-state review rule matters. The simulation rows did not change; the interpretation and selected condition did.

### The present severity read-outs produce a small paired effect

Both suites' linear severity heads estimate remaining actuator gain accurately, but their estimates straddle the controller's cap boundary at the 50% condition. Direct rollouts measured what that difference is worth:

- mean paired S-minus-C1 tracking difference: **−0.12 percentage points**;
- largest absolute paired difference: **0.52 points**;
- Claim Sheet development bar: **10 points**.

The recorded linear heads are therefore below the bar at that condition and within the measured multiplier envelope. This does not close arbitrary future read-outs, a different compensation cap, or the actuator class.

### The newest probability result is narrower than first claimed

The recovery controller also grades actuator compensation by class probability. The new screen samples six probabilities from 0.50 through 1.00 while class, location, severity, uncertainty, and abstention are held fixed. Its rollouts use [MuJoCo](https://mujoco.readthedocs.io/en/stable/overview.html), the project's physics-simulation engine.

The largest sampled gate-clearing difference is **5.0699 points**, with a mean of **5.0162**, below the 10-point bar. All four sampled curves are monotone. An independent reviewer audit added a 0.025-spaced grid—84 MuJoCo arms across four seeds—and found the same maximum and monotone shape.

The original interpretation called this the last control route and treated the six points as closure of the continuous channel. First review corrected that:

- a continuous interval is not exhausted by six rollout points;
- a calibrated suite can still cross the probability, abstention, or uncertainty gate when the other does not;
- the separate measured gate-crossing effect is **10.85 points**, above the bar;
- changing the compensation cap changes both recoverable tracking and which severity estimates command differently.

The 5.07-point number is reproducible. It is a sampled development envelope, not a proof of continuous-response closure.

## What is working

- The bounded task, one-decision lifecycle, and contact profile now survive the declared five-second safety horizon.
- The plant→sensor→estimator→controller path remains causal and uses deployable observations for decisions.
- The project is keeping diagnosis, action authorization, and control outcome in separate evidence lanes.
- Same-state review has caught consequential errors in both directions: a units conversion, a skipped controller boundary, uncertainty-role overreach, missing fail-loud gates, and now continuous-channel overreach.
- The current packet passes **302 tests** and compiles cleanly.
- The probability-screen CSV, JSON, and Markdown report reproduce byte-for-byte across eight- and four-worker runs.
- The public Live-Run record keeps corrections append-only, so earlier claims and their later narrowing are both visible.

## What is not working or not ready

- The tested structural actions do not produce source-specific recovery on the current bounded task.
- The actuator probability screen does not close calibrated authorization; a gate crossing clears the development bar.
- Compensation-cap and minimum-gain-floor sensitivity remain open, especially at the selected 25% remaining-gain condition.
- Healthy false authorization, action-versus-no-action benefit, source specificity, and sensor-fault recovery still need the actuator action screen.
- Four assessment seeds, one task, one location, and one setting are not validation-sized evidence.
- The learned attribution and control comparators remain intentionally unbuilt until the configuration and role separation are ready to freeze.
- Validation grids, probability and uncertainty calibration, leakage/storage/hash audits, and the Phase-3 verification artifact remain open.

## Verification-path update

The Reproducibility Packet now contains runnable, fail-loud development screens for:

- bounded task/contact mechanics;
- held-decision noisy information;
- structural action specificity;
- per-class tracking headroom;
- actuator severity quality and cap-boundary conversion;
- sampled actuator class-probability sensitivity.

The latest screen verifies the complete expected arm grid, exact common-random-number reuse against committed reference rows, one estimator decision, correct action withholding/acting, no A1 safety event, no saturation, and the commanded-versus-applied multiplier identity. Its result can be regenerated from the packet; it is not yet the final interactive verification artifact.

## The next stretch

The immediate coordination step is Claude's owner re-review of the exact probability-screen corrections. The loop stays open until explicit same-state approval.

After that, the technical work should keep the actuator action question narrow and predeclared:

1. measure action-versus-no-action benefit and healthy false authorization;
2. screen the compensation-cap/minimum-floor surface without treating the current cap as free or settled;
3. preserve probability, abstention, and uncertainty crossings as authorization outcomes rather than folding them into graded probability precision;
4. require source specificity and unchanged safety gates;
5. keep the four-seed result in development until validation roles and the complete configuration are ready.

The project is making progress because negative and narrowing results are changing the experiment before freeze. The current evidence supports “the gauges add structural diagnostic information on this task” much more strongly than “that information improves control.” The next screens must test that boundary directly rather than assume either outcome.
