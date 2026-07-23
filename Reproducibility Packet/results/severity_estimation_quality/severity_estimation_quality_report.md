# Severity-estimation quality versus action severity-sensitivity

Development-sized screen. Measures how well each deployable suite estimates remaining actuator gain, and whether any measured difference between the suites can change the command the recovery controller actually applies.

- Severity grid (remaining gain): [1.0, 0.85, 0.7, 0.55, 0.4, 0.25, 0.1]
- Tuning seeds [17000, 17001, 17002, 17003, 17004, 17005]; disjoint assessment seeds [17100, 17101, 17102, 17103]
- 70 no-action arms, one S observation each, physically projected to C1 so the suites are exactly paired
- Config hash `dev-severity-estimation-quality-screen` (not frozen)

## Part A — where a severity difference can change the action at all

The controller's actuator multiplier is `min(1 / max(severity, 0.25), cap)`. It is flat for every estimate at or below `1 / cap`, so at the recorded cap of 2 any two severity estimates in `(0, 0.5]` command **identically**. A severity advantage is only reachable where the action is severity-sensitive *and* the setting's exact-restoration ceiling clears the 10.0% bar.

| cap | sensitive severities | reachable severities (sensitive *and* ceiling ≥ bar) |
|---:|---|---|
| 2.0 | `(0.500, 1.000)` | none |
| 3.0 | `(0.333, 1.000)` | 0.50 |
| 4.0 | `(0.250, 1.000)` | 0.50 |
| 6.0 | `(0.250, 1.000)` | 0.50 |
| 8.0 | `(0.250, 1.000)` | 0.50 |

- **The smallest cap with any reachable severity is 3.** At the recorded cap of 2 the reachable set is empty: every setting with enough headroom to clear the bar sits in the flat region of the multiplier, and every severity-sensitive setting has a ceiling below the bar. Raising the cap is what moves a setting into both regions at once, which is why the pending cap-sensitivity arm and the severity-quality arm have to be run together rather than in either order alone.

| severity | no-action deficit | exact-restoration ceiling | multiplier at cap 2 | severity-sensitive | ceiling ≥ bar |
|---:|---:|---:|---:|:--:|:--:|
| 0.85 | +2.69% | +2.62% | 1.176 | yes | no |
| 0.70 | +6.28% | +5.91% | 1.429 | yes | no |
| 0.50 | +13.20% | +11.66% | 2.000 | no | yes |
| 0.25 | +23.16% | +18.81% | 2.000 | no | yes |
| 0.10 | +65.73% | +39.66% | 2.000 | no | yes |

## Part B — measured severity-estimation accuracy, C1 versus S

| suite | active features | ridge penalty | held-out MAE | RMSE | max abs error | bias |
|---|---:|---:|---:|---:|---:|---:|
| C1 | 110 / 144 | 0.1 | 0.0060 | 0.0090 | 0.0265 | +0.0048 |
| S | 142 / 144 | 0.1 | 0.0080 | 0.0101 | 0.0184 | +0.0063 |

- The gauge role contributes 32 additional active feature columns to S. S's held-out mean absolute severity error is -0.0020 lower than C1's (0.0080 versus 0.0060).

| severity | C1 mean estimate | C1 MAE | S mean estimate | S MAE |
|---:|---:|---:|---:|---:|
| 1.00 | 0.998 | 0.0020 | 1.000 | 0.0005 |
| 0.85 | 0.860 | 0.0103 | 0.862 | 0.0118 |
| 0.70 | 0.705 | 0.0056 | 0.705 | 0.0069 |
| 0.55 | 0.553 | 0.0051 | 0.556 | 0.0076 |
| 0.40 | 0.408 | 0.0078 | 0.410 | 0.0104 |
| 0.25 | 0.256 | 0.0059 | 0.257 | 0.0075 |
| 0.10 | 0.104 | 0.0053 | 0.104 | 0.0111 |

## Parts A and B together — does a deployable read-out command like an oracle?

On a fault whose true severity already sits in the flat region, the oracle's own multiplier is the cap. Any estimate that also lands there therefore reproduces the oracle's command exactly, however wrong the number is — so a severity read-out on those settings is a threshold test, not a regression problem.

| suite | cap | capped arms | oracle-identical | sensitive arms | oracle-identical | healthy arms | oracle-identical | max multiplier error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C1 | 2.0 | 12 | 100.0% | 12 | 0.0% | 4 | 25.0% | 0.0532 |
| C1 | 3.0 | 8 | 100.0% | 16 | 0.0% | 4 | 25.0% | 0.1071 |
| C1 | 4.0 | 8 | 50.0% | 16 | 0.0% | 4 | 25.0% | 0.2402 |
| C1 | 6.0 | 8 | 50.0% | 16 | 0.0% | 4 | 25.0% | 0.2402 |
| C1 | 8.0 | 8 | 50.0% | 16 | 0.0% | 4 | 25.0% | 0.2402 |
| S | 2.0 | 12 | 100.0% | 12 | 0.0% | 4 | 75.0% | 0.0374 |
| S | 3.0 | 8 | 100.0% | 16 | 0.0% | 4 | 75.0% | 0.1007 |
| S | 4.0 | 8 | 50.0% | 16 | 0.0% | 4 | 75.0% | 0.2342 |
| S | 6.0 | 8 | 50.0% | 16 | 0.0% | 4 | 75.0% | 0.2342 |
| S | 8.0 | 8 | 50.0% | 16 | 0.0% | 4 | 75.0% | 0.2342 |

`oracle-identical` is exact multiplier equality. Three regimes are separated because they ask different questions. In the **capped** regime the cap binds and any estimate below the threshold reproduces the oracle exactly, so the rate is the one that matters. In the **sensitive** regime exact equality requires an exactly correct number and is near zero by construction, so the graded maximum multiplier error is the quantity to read. The **healthy** arms are the grid's top anchor, where the oracle applies no action at all: a non-zero rate there is a false-authorization question, not a severity-precision one. The informative contrast is across regimes: a read-out that is useless as a regression can still be exact as an action.

### Would the two suites ever command differently?

| cap | pairs | multipliers differ | mean abs difference | max abs difference | capped-region pairs | of those, differ |
|---:|---:|---:|---:|---:|---:|---:|
| 2.0 | 28 | 15 (53.6%) | 0.0096 | 0.0417 | 12 | 0 |
| 3.0 | 28 | 19 (67.9%) | 0.0182 | 0.0893 | 8 | 0 |
| 4.0 | 28 | 23 (82.1%) | 0.0357 | 0.1967 | 8 | 4 |
| 6.0 | 28 | 23 (82.1%) | 0.0357 | 0.1967 | 8 | 4 |
| 8.0 | 28 | 23 (82.1%) | 0.0357 | 0.1967 | 8 | 4 |

- **At the recorded cap of 2, the suites command differently on 15 of 28 held-out arms**, but by a mean absolute multiplier difference of only 0.0096 (worst 0.0417).
- **And none of those differences fall where the action could be worth the bar.** On all 12 capped-region arms — the only severities whose exact-restoration ceiling clears the bar — the two suites command **identically**. Every suite difference the read-out produces lands on a setting whose ceiling is below the bar. So the recorded 0.0000% paired S-minus-C1 control difference on the actuator class is a property of the action family, not an artifact of the pinned stand-in severity that produced it, and a better severity read-out cannot change it.

## What this screen does and does not establish

- **It is a bound on a linear read-out, not on the severity channel.** A learned head could raise both suites' accuracy. A null S-over-C1 difference here means the gauge channels carry no severity information a matched linear read-out can recover at this data size, not that they carry none.
- **The action comparison is stronger than the accuracy comparison.** The multiplier is flat over most of the severity range, so the commanded-action result survives read-out quality changes that the MAE comparison would not: any estimator landing in the same flat region commands the same thing.
- **The class-probability channel is deliberately held fixed, and is untested.** The controller's multiplier is `1 + p · (capped - 1)`, so two suites that call the same class with different calibrated confidence command differently even at an identical severity. This screen pins `p = 1` for both suites in order to isolate the severity channel. A suite difference in class probability is a separate route to a non-zero paired control difference, it is not measured by any artifact in this packet, and the one-hot prototype probabilities the information review recorded are explicitly not calibrated probabilities.
- **Development-sized.** 42 fit windows and 28 held-out windows, held out over sensor seed only, on one bounded task/contact condition and one fault location. Not validation-sized, not frozen-config, and not evidence about the structural or sensor classes.
- **Severity uncertainty is not yet calibrated.** The head reports a training residual dispersion (C1 0.0024, S 0.0021), which is an in-sample number. The recovery controller's confidence gate gates on severity uncertainty, so a deployable severity arm needs a held-out uncertainty before it can be wired to the action.

## Audit

- Exactly one classification evaluation per arm: True
- Zero recovery-command changes on every arm: True
- Zero A1 incident steps: True
- Zero saturation steps: True
- Suite projection verified against a real C1 session on 3 arms; max absolute feature difference 0.000e+00, max absolute `J_5s` difference 0.000e+00
- Tuning and assessment seed sets are disjoint: True

