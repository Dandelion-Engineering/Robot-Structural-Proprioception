# What the class-probability channel is worth at the selected actuator condition

Development-sized screen. Isolates the graded class-probability response while class, location, severity, severity uncertainty, and abstention are held fixed, at the condition the deficit screen selected.

- Selected condition: remaining actuator gain 0.25 at joint 1, compensation cap 2
- Assessment seeds [16100, 16101, 16102, 16103], reusing the deficit screen's `pair_id`s
- 36 arms; sampled probabilities [0.6, 0.7, 0.8, 0.9] plus the gate endpoint, the certain endpoint, and a sub-threshold probe
- Config hash `dev-actuator-probability-channel-screen` (not frozen)

## Part 0 — what is held fixed while probability is varied

The controller's compensation is `min(1 / max(severity, minimum_gain_remaining), maximum_gain_compensation)`. With the recorded cap 2, every severity estimate at or below **0.5000** yields the same capped compensation. The true remaining gain here is 0.25, which is 25x the recorded severity error scale away from that boundary.

**So the severity channel is structurally flat at this condition.** Every estimate at or below 0.5000 commands an identical multiplier — that bound is the recorded cap, not a judgement about which estimates are plausible. A read-out would have to err by more than 0.2500 on a true 0.25, about 25x its recorded error scale, before the severity channel became live at all. The present fixture therefore holds severity fixed inside that region and varies class probability alone. It does not test suite-specific abstention or uncertainty-gate crossings.

| suite | assessment residual RMS | std | bias | handed to the gate |
|---|---:|---:|---:|:--:|
| C1 | 0.008585 | 0.008393 | +0.002336 | no |
| S | 0.010183 | 0.008029 | +0.006422 | yes |

- The development fixture supplies a common **bias-inclusive RMS**, not a residual standard deviation. A standard deviation discards the bias, so it is not a safe proxy for absolute severity error. The conservative suite value (0.010183) is used at every acting arm to keep uncertainty from becoming a second varied channel, and it clears the 0.25 gate by 25x. This does not define a frozen per-example uncertainty statistic or close an uncertainty-driven authorization difference.

## Part 1 — the reachable probability interval

Both ends of the input interval are recorded controller constants, not chosen grid points. The confidence gate closes it below at p = 0.5; the compensation cap closes it above. The reachable commanded multiplier is therefore exactly **[1.50, 2.00]**.
 The interval is continuous. The rollout grid samples six probabilities across it; it does not simulate every point between them.

- The action is **cap-saturated throughout**: exact restoration of a 0.25 remaining gain needs a multiplier of 4.00, and the cap allows 2.00 — short by a factor of 2.00. Even a maximally confident diagnosis under-restores here.

## Part 2 — the measured response

Each point is paired per seed against that seed's own no-action arm, so this is a within-noise-realization comparison. `reduction` is `100 x (J_no_action - J_arm) / J_no_action`, positive when the action helps.

| class probability | mean applied multiplier | mean reduction vs no-action | min | max |
|---:|---:|---:|---:|---:|
| 0.50 | 1.50000 | +6.1107% | +6.0245% | +6.1915% |
| 0.60 | 1.60000 | +7.1712% | +7.1329% | +7.2378% |
| 0.70 | 1.70000 | +8.1665% | +8.1282% | +8.2341% |
| 0.80 | 1.80000 | +9.1414% | +9.0808% | +9.2463% |
| 0.90 | 1.90000 | +10.0035% | +9.9629% | +10.0747% |
| 1.00 | 2.00000 | +10.8204% | +10.7889% | +10.8509% |

- **Across the sampled grid p in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0], the mean reduction moves by 4.7097 percentage points**, against a 10% bar — below it. All four sampled per-seed curves are strictly monotone. The local sampled slope at the certain end is +8.1684 points per unit of probability.

## Part 3 — the gate is a separate quantity from the graded channel

A sub-threshold probe at p = 0.49 keeps the actuator as the unique argmax and still produces 0.0000% reduction — the action is withheld entirely. Entering the gate jumps straight to 6.1107 percentage points.

The table below is in **the contract's own units** — `100 x (J_C1 - J_S) / J_C1`, the conventional suite in the denominator — not in differences of no-action reductions. Those are not the same number: a difference of two reductions is smaller by `1 / (1 - r_low / 100)`, so quoting the reduction span against the bar would understate the quantity the bar is written in. Here the sampled mean reduction span is 4.7097 pp while the largest sampled paired quantity is 5.0699 pp.

| paired quantity | worst seed | mean | vs bar |
|---|---:|---:|---|
| graded — both suites past the gate | 5.0699 pp | 5.0162 pp | below |
| gate-crossing — one suite withholds entirely | 10.8509 pp | 10.8204 pp | clears |

**These must not be collapsed into one number.** The sampled graded span is an empirical sensitivity of the fixed-action fixture. The gate-entry jump is what a difference in whether the suite authorizes the action at all can buy. The current prototype calls are one-hot mechanism outputs, not calibrated probabilities, and future class-probability, abstention, or uncertainty-gate crossings remain validation-owned.

## Part 4 — what the cap actually buys at this condition

The boundary screen measured the realized-versus-analytic ratio at the 0.50 condition and explicitly did not establish it here. This is that measurement, and it is a different regime: there the certain diagnosis commanded the exactly restoring multiplier, whereas here the cap allows only half of what exact restoration needs.

- Mean no-action deficit **23.16%**; analytic exact-restoration ceiling **18.81%**; realized at the cap **10.82%** — **57.5% of the ceiling**, in the same direction on every seed.

## What this screen does and does not establish

- **The sampled graded probability response remains below the bar at this condition.** Searching every ordered pair on the six-point gate-clearing grid finds a largest S-over-C1 comparison of 5.0699 pp against a 10 pp bar. The sampled response is monotone on every seed, so the recorded endpoints are the sampled extrema.
- **It does not close unsampled probabilities inside the continuous interval.** The controller constants close the input range, but six rollout points do not form a mathematical bound on the nonlinear tracking response between those points.
- **It does not license collapsing authorization into the graded channel.** A suite difference large enough to put one output below a probability, abstention, or uncertainty gate and the other above it is a separate authorization difference.
- **It does not close the actuator class.** Action-versus-no-action benefit on a healthy body, false authorization, cap and floor sensitivity, and the source-specific margin remain the action screen's questions.
- **It does not extend to a different cap.** Both the flat severity region and the reachable multiplier set are functions of `maximum_gain_compensation`. At a larger cap the severity channel reopens at this condition and this screen says nothing about it.
- **Development-sized.** Four assessment seeds on one bounded task/contact condition, one fault location, one fault setting, held out over sensor noise only, at an unfrozen config.

