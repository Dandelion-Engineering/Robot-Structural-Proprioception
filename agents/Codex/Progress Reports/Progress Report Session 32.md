# Progress Report — Codex Session 32

**Report date:** 2026-07-24

**Phase:** Phase 2 — Integration and Reproducibility Build

**Audience:** Project director

## The short version

Since my Session-24 report, the project has stopped searching through more
development recovery actions and built the machinery for the experiment we
actually promised to run.

Three things now matter most:

- The final actuator-action screen blocked. It found real recoverable actuator
  tracking error, but the safe controller setting missed the predeclared
  source-specific margin and stronger settings crossed the unchanged safety
  limits.
- The machine-readable schema, draft/final configuration lifecycle,
  role-separated storage, and full 808-reservation experiment plan have passed
  independent same-state review.
- The approved plan is now embedded in the still-draft configuration, and its
  real dev/pilot/validation C1-versus-S base dataset has been generated and
  independently audited. Test remains untouched.

This is a major reproducibility milestone, not a research result. No learned
model has been fit to these data, no validation threshold has been selected,
the final `config.json` does not exist, and the one-shot test set has not been
materialized.

## Why the plan came before the data

A preregistration records a study plan before data collection or analysis so
later results can be compared with the intentions that existed beforehand
([OSF overview](https://help.osf.io/article/330-welcome-to-registrations)).
Our repository version is executable: the plan names every trajectory, fault,
background condition, split, and random-number identity, then hashes its own
canonical contents.

The hash is a fingerprint, not a claim that the plan is scientifically good.
SHA-256 is defined by the
[NIST Secure Hash Standard](https://csrc.nist.gov/files/pubs/fips/180-4/final/docs/fips180-4.pdf);
here it lets both agents prove they reviewed the same bytes. Scientific quality
still came from trying to break the plan before generation.

That distinction paid off twice.

First review found that payload and temperature had become locked together in
a way that leaked fault identity. Temperature reaches deployable observations
only through the strain gauges, so the flaw would have handed a shortcut to the
very suite being tested. The assignment was blocked before any data existed.

After that leak was fixed, review found a smaller training-only alias between
trajectory and payload. It could not manufacture an S-over-C1 win, but it could
make a null result harder to interpret. Development and pilot repeats were
therefore increased from 76 to 152 reservations each. The total plan grew from
656 to 808 reservations, every fault now sees all eight background-condition
cells, and every trajectory varies payload, temperature, and contact.

## What was built since Session 24

### The development action lane closed honestly

The source-specific actuator action screen used separate tuning and assessment
roles. Its safe cap-3 controller reduced actuator-fault tracking error by
16.58%, but falsely applying the same diagnosis to a healthy plant improved
tracking by 8.32%. The remaining 8.25-point source-specific margin missed the
10-point gate. Stronger cap-4 and cap-5 actions produced more raw recovery but
crossed the unchanged A1 safety envelope.

The bounded inverse-gain family therefore blocked. That result helped end the
sequence of small action screens and redirect effort to the agreed experiment.
It is still a development result, not a final comparison of sensor suites.

### Configuration now has a real lifecycle

The Phase-2 readiness review separated two states that had previously been too
easy to blur:

1. a versioned `dev-*` draft used while models and thresholds are selected; and
2. one immutable final `config.json`, created only before untouched
   confirmatory generation.

The draft refuses confirmatory callers. It stays self-hashed, records open
gates, and cannot masquerade as the final file merely because its JSON is
well-formed.

### Storage now enforces the information boundary

The packet now writes a path-free identity manifest, separate plant,
observation, label, estimator-output, and controller-log roles, plus exact
per-file hashes. A deployable loader can open one observation suite only; it
cannot receive a plant path, label path, identity manifest, oracle, or sibling
suite root.

A synthetic fixture proved every role and join before real generation. Draft
lifecycle checks reject test rows, and supervised joins expose only an
observation plus its target on dev/pilot/validation.

### The approved plan now drives the real simulator

The generator uses [MuJoCo](https://mujoco.readthedocs.io/en/stable/overview.html)
for the selected cable/rod plant and adds the pieces the approved plan requires:

- an exact distal point mass with corrected center of mass and inertia;
- split-owned temperature profiles;
- time-windowed endpoint contact without widening the single allowed
  collision pair;
- structural and actuator components in the plant;
- sensor bias, drift, and dropout only in the observation path; and
- compound plant-plus-sensor cases with the full component list retained
  outside deployable observations.

Before generation, all eight declared payload masses are compiled and checked.
The generator then builds 472 approved non-test reservations: 152 development,
152 pilot, and 168 validation. The primary C1/S manifest contains 944 rows.
Dataset identities use training seed zero; the five model-fit seeds do not
appear until those five models really exist.

## What the closing audit establishes

The independent audit does not trust a report written by the generator. It
reloads every payload through the hash-checking role loaders, re-derives the
approved reservation set, and compares the manifest field by field.

It checks:

- 472 approved reservation pairs and 944 manifest rows;
- 944 plant payloads and 944 labels;
- 472 C1 observations and 472 S observations;
- byte-identical privileged plant truth within every matched pair;
- bitwise-identical shared C1/S channels within every pair;
- every one of the eight declared payload masses;
- exact split counts; and
- zero test identity or payload rows.

The full packet test suite now contains 397 passing tests. The generated
numeric data live under the ignored local `data/` root and are rebuilt by the
runbook rather than committed as multi-gigabyte repository objects.

## What surprised us

The most important finding in this interval was not a model score. It was that
an apparently balanced experiment plan could still encode the answer through
background conditions. The first assignment looked reasonable in prose and
passed simpler count checks. Expanding it and measuring the realized design
revealed the leak.

The second surprise was constructive: paying a 23% generation-cost increase
made development, pilot, and validation share the same per-trajectory
background design. That makes the pilot-to-validation rung easier to interpret.
The later validation-to-test rung still changes from a half fraction to the
complete factorial per trajectory; that limitation is recorded in advance.

I also stopped and restarted the full data build after noticing that my first
preflight checked the six research-owned masses before generation but compiled
the two test-owned scalar masses later. No test identity had been created, and
the physics implementation was correct, but the approved wording required all
eight mass values to be checked first. The partial local output was discarded
and regenerated from zero under the stricter order.

## What is working

- Two-agent same-state review is catching design flaws before results exist.
- The approved assignment, parent draft, current draft, and generated roles
  have explicit, reproducible identities.
- The generator cannot accept a test split from its CLI, and the independent
  draft lifecycle refuses test rows again.
- All real roles are written through the reviewed role builders and reloaded
  through exact indexes and payload hashes.
- Shared plant truth and shared observation channels are measured rather than
  assumed.
- The runbook now takes a reader from contract validation through real base-role
  generation and independent audit.

## What is not working or not ready

- Gate 2 is not declared complete until the generated base-role state receives
  same-state review and the later estimator/controller roles exist.
- The learned attribution head and RMA comparator remain unbuilt.
- No five-seed model fit, validation calibration, abstention threshold, OOD
  threshold, or action-authorization rate exists.
- The confirmatory controller protocol and final evaluation driver remain open.
- Final `config.json` is absent.
- Test identities and payloads remain unmaterialized.
- No Phase-3 interactive verification artifact exists yet.
- The current development evidence still supports “structural sensing improves
  diagnosis on this task” more strongly than “it improves control,” but the
  approved multi-setting comparison has not yet been fit or evaluated.

There is no open director-only request.

## Verification-path update

The packet's verification path now includes:

1. strict draft-config and assignment validation;
2. a synthetic complete-role fixture;
3. the real assignment-driven base-role generator;
4. a smoke-only truncation mode that labels itself non-research;
5. an independent full on-disk role/identity/CRN audit; and
6. the full regression suite.

This is genuinely new verification infrastructure. It is not yet the final
interactive artifact promised for Phase 3.

## The next stretch

The immediate next step is Claude's independent review of the embedded
assignment, generator, manifest, and on-disk audit.

If that state passes:

1. Gate 4 fits the matched C0/C1/S learned and interpretable models under the
   five preregistered training seeds and shared capacity rules.
2. Gate 5 uses validation only to select calibration, abstention, OOD, and
   action-authorization thresholds.
3. Gate 6 freezes the exact confirmatory controller protocol.
4. Gate 7 builds and reviews the evaluation driver and final test manifest.
5. Only then is immutable `config.json` created and the untouched test
   identities and payloads materialized.

The project remains in Phase 2. The central result is still open, and the
correct next move is to fit the approved non-test data—not to infer an answer
from the generator or from the earlier development screens.
