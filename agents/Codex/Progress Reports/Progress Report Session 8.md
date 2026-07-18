# Research Progress Report — Codex Session 8

**Date:** 2026-07-17 17:03 PDT
**Project phase:** Phase 2 — Execution
**Current public state:** In progress; no confirmatory configuration or research result yet

## Where the project stands

The project now has a working causal spine. A simulated flexible two-link arm advances one control step, produces realistic noisy sensor readings, passes only readings whose latency has elapsed to a diagnosis component, and accepts the next command. The conventional and structural sensor suites run through the same architecture, with hidden simulator truth kept in separate storage and out of the deployable path. The scoring code, uncertainty calculations, diagnosis-output structure, and first honest change detector are also present. The full packet currently passes 80 automated tests.

That is substantial progress, but it is still infrastructure. We have not trained the component that names *which* fault occurred, built the recovery controller, generated confirmatory data, or answered whether structural sensing improves control. Most importantly, this session found that the proposed diagnostic motion is not ready to freeze. The present problem is no longer “can the simulated structure produce measurable strain?” It can. The problem is “can it do so under a short, finite, safety-bounded probe that represents the experiment we actually intend to claim?” The current answer is **not yet**.

## The central lesson so far: information is not free

Robot identification has a basic tension: if the robot moves only in ways that barely load its body, different physical changes can look nearly identical; if it moves aggressively enough to make them separable, that motion may be inappropriate for a robot whose condition is uncertain. This is why the Claim Sheet treated diagnostic excitation as a safety budget from the beginning. The identification literature likewise treats the richness of the commanded motion as a first-class part of what can be learned, rather than a harmless background detail ([BIRDy survey and benchmark](https://doi.org/10.3390/app11094303)).

The earlier mechanics feasibility spike established two honest facts:

- Ordinary joint commands produced structural and actuator gauge differences below the pre-declared 10-microstrain credibility floor.
- A continuous 1 N, 0.8 Hz transverse load pushed those differences above the floor, so MuJoCo’s native cable/rod mechanics were suitable for continued development. MuJoCo’s first-party cable model represents bending and twisting through integrated elastic mechanics, rather than fabricating a strain label ([MuJoCo elasticity documentation](https://mujoco.readthedocs.io/en/stable/programming/extension.html#elasticity)).

That was a valid mechanics-selection result. It was not proof that a short diagnostic action would work. The continuous load had already been moving the plant before the fault arrived. A real post-detection diagnostic would begin after the robot suspects something changed.

## What this session tested

I added a finite “raised-cosine” envelope: the load ramps smoothly from zero, runs for an exact number of cycles, and returns smoothly to zero, with essentially zero net impulse. That prevents the test from hiding a permanent shove inside something called a diagnostic probe. I then reran the selected 17-point plant at the selected 0.1 ms physics step under four matched conditions:

| Condition | Probe budget | Structural signal | Actuator signal | Structure–actuator separation | Mechanics decision |
|---|---:|---:|---:|---:|---|
| Ordinary motion | 1.25 s | 2.17 microstrain | 5.92 microstrain | 5.93 microstrain | BLOCK |
| Continuous feasibility load | 1.25 s post-change view | 10.56 microstrain | 23.36 microstrain | 23.36 microstrain | PASS |
| One-cycle bounded probe | 1.25 s | 8.18 microstrain | 7.84 microstrain | 12.33 microstrain | BLOCK |
| Two-cycle bounded probe | 2.50 s | 8.67 microstrain | 13.38 microstrain | 17.49 microstrain | BLOCK |

The one-cycle probe misses both the structural and actuator floors. The two-cycle probe recovers the actuator signal and the separation between causes, but the structural signal remains below the unchanged floor. Extending the same probe also makes the simulated arm rotate repeatedly rather than behave like a bounded manipulator: the two-cycle healthy run reaches roughly 21 radians of accumulated joint rotation and 38 radians per second.

This is a useful negative method finding. It does not invalidate the selected cable mechanics, and it says nothing yet about whether structural sensing helps the eventual controller. It says the development condition that made the mechanics informative cannot honestly be promoted into a “short safe diagnostic” without redesign.

## A second review found problems before they could harden into the model

Claude built the first diagnosis front: a fixed sensor-history input, a detector that can say “something changed,” calibrated abstention when it cannot name the cause, and a privileged oracle used only as a ceiling. My review found three interface defects and corrected them directly:

1. The supposedly fixed history tensor actually grew during startup, from one row toward the declared window length. It now always has one fixed shape, with unavailable startup rows explicitly masked.
2. Feature slopes used the encoder’s timestamps for every sensor, even though the schema deliberately preserves timing separately for encoders, IMU, current, and gauges. Each channel now uses its own measurement clock.
3. The perfect-information oracle revealed a run’s fault class before the fault’s onset. It now reports healthy before onset and exposes the true class only once the change exists.

These may sound like software details, but they protect the scientific comparison. A changing tensor shape changes the model; the wrong timestamps undermine causal interpretation; and an oracle that knows the future is not a fair ceiling. The project’s formal motivation is that some body changes are invisible from conventional joint measurements alone—model capacity cannot recover information the observation map never contained ([Wensing, Niemeyer, and Slotine, 2024](https://doi.org/10.1177/02783649241258215)). That makes leakage and timing discipline central, not cosmetic.

## What is working

- The selected mechanics, sensor path, online causal loop, estimator-output structure, and evaluation core integrate cleanly.
- Conventional and structural suites preserve matched randomness without letting the conventional suite see hidden gauge values.
- The realistic structural sensor model retains the declared 1-microstrain noise floor and roughly 10-microstrain-per-degree-Celsius temperature cross-sensitivity instead of manufacturing an ideal sensor advantage; the temperature scale is grounded in published fiber-Bragg-grating behavior ([Silveira et al., 2021](https://doi.org/10.3390/s21175828)).
- The evaluation code now enforces the pre-declared five-second tracking window, tie-safe selective prediction, held-out unknown-detection operating points, and crossed pair-by-training-seed uncertainty.
- The full packet passes 80 tests and compiles cleanly.

## What is not working or not ready

- No bounded diagnostic candidate currently clears both the mechanics-information screen and the provisional motion-safety screen.
- The plant still disables environmental contact. Its contact and safety arrays remain zero-width development placeholders, which is unacceptable for pilot or confirmatory data.
- The contact/safety proposal now has explicit semantics—two contact fields and seven safety flags—but the thresholds are provisional and need joint review and implementation.
- `W=512` samples and diagnosis `stride=8` are plausible estimator settings, but remain a pilot-sweep proposal. A 1.02-second history covers most, not all, of one 0.8 Hz cycle.
- Severity/onset grids and several non-load-bearing sensor constants remain open.
- The learned fault-attribution head, strong control-only latent baseline, recovery controller, split/leakage audit against real multi-run storage, and interactive director verification artifact remain future work.
- The agreed Claim Sheet still awaits Randy’s non-blocking review; execution continues while that request is open.

## The next stretch

The next plant-side task is not to make the same sinusoid longer. It is to redesign the diagnostic/controller pair so the arm stays inside an explicit motion envelope while producing usable differential strain. Candidate directions include a closed-loop tip or joint-space probe, lower-amplitude multi-frequency excitation, a short pre-registered pulse sequence, and greater damping or task stabilization. Each candidate must pass two gates together: the unchanged signature floor and the reviewed safety flags. Contact instrumentation must then populate the proposed two-field role so optional endpoint-contact cases can be evaluated rather than represented by empty arrays.

Only after that convergence should the team freeze the complete configuration, run the window/stride pilot sweep, finalize the severity/onset and sensor constants, and generate data for the learned attribution and recovery work. The discipline here is simple: the config freezes when the experiment is ready, not when the file has enough fields to serialize.
