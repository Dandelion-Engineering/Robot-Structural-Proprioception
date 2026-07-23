# What a severity difference is worth at the action's cap boundary

Development-sized screen. Measures the paired S-minus-C1 tracking difference at the one actuator setting that is both severity-sensitive and above the Claim Sheet bar, then places the recorded linear read-outs inside a wider measured multiplier envelope.

- Boundary condition: remaining actuator gain 0.5 at joint 1, compensation cap 2
- Assessment seeds [17100, 17101, 17102, 17103], reusing Step 15's `pair_id`s
- 40 arms; commanded multiplier sweep [1.5, 1.7, 1.85, 1.93, 1.97]
- Config hash `dev-severity-action-boundary-screen` (not frozen)

## Part 1 — severity-uncertainty diagnostics

The recovery controller's confidence gate rejects a diagnosis whose severity uncertainty exceeds 0.25. The severity head reports an *in-sample* residual dispersion, which is not that number. A fixed-penalty leave-one-seed-out estimate on the tuning role supplies a calibration-only value the gate can receive without using assessment rows. The disjoint assessment residuals are reported separately as the honest check on how that internal estimate transferred.

| suite | in-sample std | calibration cross-seed std | disjoint assessment std | calibration / in-sample | assessment / in-sample | opens the gate |
|---|---:|---:|---:|---:|---:|:--:|
| C1 | 0.004237 | 0.006741 | 0.008393 | 1.59x | 1.98x | yes |
| S | 0.001951 | 0.011160 | 0.008029 | 5.72x | 4.12x | yes |

- **The in-sample number understates both out-of-seed diagnostics, and it understates the disjoint assessment dispersion unevenly across suites** — S by 4.12x. The absolute suite ranking is not stable across the two diagnostics: the internal calibration cross-seed estimate is larger for S, while the disjoint assessment standard deviation is slightly smaller for S (Step 15's MAE remains larger for S because its bias is larger). The safe conclusion is that training dispersion must not reach the confidence gate. Both calibration-only values clear the gate comfortably, so the action below fires for either.
- The calibration cross-seed values hold Step 15's selected penalties fixed. Because those penalties were selected using the same tuning groups, these are development calibration estimates, not nested post-selection uncertainties or frozen confidence margins.

## Part 2 — the paired quantity at the boundary

Each suite's *recorded held-out estimate* drives the real recovery controller on the same seed, plant, and noise realization. The estimator decides once, before the action fires, so the pre-decision trajectory is the one that produced the estimate. `reduction` is the contract's quantity, `100 x (J_C1 - J_S) / J_C1`, positive when S is better.

| seed | C1 estimate | S estimate | C1 multiplier | S multiplier | C1 vs no-action | S vs no-action | paired S-minus-C1 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 17100 | 0.495246 | 0.499191 | 2.00000 | 2.00000 | +10.8775% | +10.8775% | +0.0000% |
| 17101 | 0.510879 | 0.501524 | 1.95741 | 1.99392 | +10.5600% | +10.6542% | +0.1053% |
| 17102 | 0.497367 | 0.517975 | 2.00000 | 1.93060 | +10.9053% | +10.4460% | -0.5154% |
| 17103 | 0.498314 | 0.506694 | 2.00000 | 1.97358 | +10.6918% | +10.6377% | -0.0605% |

- Mean paired S-minus-C1 reduction: **-0.1177%** against a 10% bar; largest absolute value on any seed **0.5154%**. Seed split — S better on 1, C1 better on 2, exactly identical on 1.
- The action itself is real on this condition: the no-action deficit is +13.11% and the privileged oracle recovers +10.81% of it. Both deployable suites land close to that ceiling — C1 +10.76%, S +10.65%. The severity channel is not the thing separating them from the ceiling.
- **Exact restoration of the gain does not exactly restore the tracking.** The analytic exact-restoration ceiling for this deficit is 11.59%, and a privileged oracle commanding the exactly restoring multiplier realizes 10.81% — a shortfall of 0.78 percentage points, or 93.2% of the ceiling, in the same direction on every seed. The gap is the part of the error the fault has already produced before the single held decision fires, which no multiplier recovers. For this boundary condition, the `deficit -> reduction` conversion is therefore an upper bound rather than the achieved value. Whether the same shortfall applies at the 0.25 condition selected by the deficit screen is not measured here.

## Part 3 — the measured conversion envelope

Every severity result in this packet is stated in multiplier units and the contract is stated in tracking units. This sweep is the conversion factor. It spans commanded multipliers far outside the errors of the recorded linear read-outs. The resulting tracking span is an empirical envelope for those read-outs on this condition, not a universal bound on an arbitrary future read-out that could command below 1.50.

| commanded multiplier | mean applied | mean reduction vs no-action | min | max |
|---:|---:|---:|---:|---:|
| 1.50 | 1.50000 | +7.0010% | +6.9438% | +7.0822% |
| 1.70 | 1.70000 | +8.7041% | +8.6420% | +8.7970% |
| 1.85 | 1.85000 | +9.8554% | +9.7815% | +9.9246% |
| 1.93 | 1.93000 | +10.3703% | +10.3020% | +10.4228% |
| 1.97 | 1.97000 | +10.5820% | +10.5065% | +10.7118% |
| 2.00 | 2.00000 | +10.8093% | +10.6918% | +10.9053% |

- Best reduction on the sweep is +10.8093% at a commanded multiplier of 2.00; at the cap it is +10.8093%.
- **Across the entire swept range 1.50-2.00 the reduction moves by only 3.8083 percentage points**, against a 10% bar. The local slope at the cap is +7.5779 percentage points per unit of multiplier.
- The two suites' recorded estimates differ by at most 0.0694 in multiplier. A local linearization at the cap converts that spread to **0.5259 percentage points** of tracking, consistent with the directly measured 0.5154-point maximum and far below the bar. The direct paired rollouts, not the linearization, are authoritative.
- **How wrong a read-out would have to be to matter here.** The sweep's lowest point commands 1.50, which is what a severity estimate of 0.6667 produces — an error of +0.1667 on a true 0.5, about 15x the larger suite's calibration cross-seed residual standard deviation. That estimate still recovers 7.00%. Producing a 10-point paired difference would require one suite to command essentially no action at all, which is a class-call difference rather than a severity-precision one — and both suites already call this class correctly.

## What this screen does and does not establish

- **It closes the recorded linear-read-out severity route on the actuator class at the recorded cap, on this condition.** Step 15 left the boundary open because the suites command differently there. They do; the direct paired difference is a fraction of a percentage point, and the wider 1.50–2.00 sweep stays below the bar. It does not close an arbitrary future read-out whose errors leave that multiplier envelope.
- **It does not close the actuator class.** Action-versus-no-action benefit, false authorization on a healthy body, cap and floor sensitivity, and the source-specific margin are the action screen's questions, not this one's. This screen removes one term from that screen's design; it does not replace it.
- **It does not measure the class-probability channel.** The multiplier is `1 + p x (capped - 1)`, and every arm here pins `p = 1`. A suite difference in calibrated class probability remains an unmeasured route to a paired difference.
- **Development-sized.** Four assessment seeds on one bounded task/contact condition, one fault location, one fault setting, held out over sensor noise only, at an unfrozen config.

## Audit

- All 8 no-action arms reproduce the recorded Step-15 `J_5s` at the same seed: True (max absolute difference 0.000e+00)
- Exactly one classification evaluation per arm: True
- No-action arms changed zero commands: True
- Every action arm changed at least one command: True
- Zero A1 incident steps: True
- Zero saturation steps: True
- Applied multipliers match the commanded multipliers: True (max absolute difference 2.220e-16)

