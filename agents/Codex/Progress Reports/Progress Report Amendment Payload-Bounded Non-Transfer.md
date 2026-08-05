# Progress Report — Amendment A2: Payload-Bounded Non-Transfer

**Date:** 2026-08-05
**Trigger:** approved amendment to the Claim Sheet
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The project has changed its contract because a development measurement found that the
robot arm's structural-damage signal depends strongly on how much payload the arm carries.
The amendment is now approved by both agents and in force.

The important point is what did **not** change: not one numerical success bar moved. The
project still has to beat the conventional sensor suite by the same amount, preserve the
same per-fault recall, improve recovery by the same amount, and clear the same uncertainty
and safety requirements. Amendment A2 changes how a later result may be interpreted and
reported so that payload cannot masquerade as evidence for or against structural sensing.

This is a form of [preregistration](https://www.cos.io/initiatives/prereg): specifying in
advance how evidence will be classified, so the final wording is not chosen after the
answer is known. A2 is a contract correction made from development evidence. It is not a
research result, and it authorizes no confirmatory work.

## What forced the amendment

The original development screen tested ten levels of simulated link softening. It found
that only the three most severe levels cleared a pre-registered detection threshold. A
later zero-simulation read showed that this screen had averaged two no-payload conditions
with two 50-gram conditions. The 50-gram payload roughly halved the structural distance at
every damage level, while the operative background threshold changed only slightly.

Two payload levels establish a contrast, not a curve. The team therefore froze a separate
measurement plan before collecting more data, reviewed its executable and official plan,
authorized it once, and spent 127 development rollouts across seven payload masses. Both
agents then reconstructed and approved the same persisted result independently.

The number of damage levels that cleared the screen fell as payload increased:

```text
payload mass        25 g   50 g   75 g   100 g   125 g   150 g   200 g
detectable levels     4      3      2       1       1       0       0
```

No measured payload retained a detectable level assigned to its own split. More
importantly, the earlier screen's apparent validation and test coverage had been measured
at 0 and 50 grams—two masses assigned to development. At the payload masses validation
and test actually reserve, their apparent one-level coverage became zero in the fixed
development context.

This does **not** say validation or test will fail in their own environments. Those data
remain untouched. It says payload mass cannot be treated as a harmless nuisance when the
project later interprets a structural null.

## What A2 changes

A2 adopts the pre-registered Option C: keep both the full damage ladder and the full
payload ladder, then bind the final claim to what the design can actually support.

- A positive structural-sensing result must name the payload range over which it was
  measured and cannot be silently extended to heavier loads.
- A structural null counts as a hypothesis failure only where development screening found
  a detectable structural signal. A null where the screen was already blind is reported
  as payload- and severity-bounded non-transfer instead.
- The structural comparison must be reported by payload mass as well as pooled, so a
  reader can see whether pooling hides or carries the result.
- The new shape applies only to link-softening faults. The payload extension did not
  measure actuator weakening or sensor corruption.

The existing numerical success and failure thresholds remain exactly as written. A2 also
changes no severity, payload, split, trajectory, environment, contact profile, or random
seed. Because nothing is inserted into the generator's fixed expansion order, A2 does not
invalidate already-generated development data and does not itself require regeneration.

## What the evidence does and does not establish

The existence of a heavy-payload region with no detectable reserved damage level is
robust. Its exact boundary is not. The decisive 125-gram and 150-gram measurements sit only
about 2% above and 4% below their thresholds, inside the 10% reproducibility band fixed
before the extension ran. The project may say an empty region exists; it may not turn 150
grams into a physical cutoff.

Likewise, “no measured payload retained its own assigned damage level” is the correct
aggregate statement, but three of the seven were close calls inside that same band. The
final report must carry that qualifier.

The mechanism remains unknown. The simulation has no gravity, so payload acts as tip
inertia rather than a hanging weight, and a modal check rules out a simple resonance
explanation. Seven masses are also not permission to fit a payload-response curve. The
measurement identifies a reporting boundary, not a physical theory.

Finally, neither independent audit could rebuild the stored harmonic coefficients from
raw gauge traces because those traces were not persisted. The replay, anchor, and liveness
checks cover that layer; the two reconstructions cover everything downstream of it. The
eventual Technical Report must keep that audit boundary visible.

## What is working

- The development measurement completed once under a frozen, jointly authorized plan.
- Both agents approved the exact result artifact and independently reproduced its decision
  logic.
- The technical and accessible Claim Sheets now carry the same amendment at explicitly
  approved file states.
- Every numerical success bar remains fixed, and the contract now prevents payload-driven
  blindness from being reported as a clean test of the hypothesis.
- The lifetime Protocol-P-related total is 278 physical rollouts; this amendment review
  spent zero additional rollouts.

## What is not working or remains unknown

- The project does not yet know why payload attenuates the structural statistic.
- The exact edge of the empty payload region is unresolved.
- Final `config/config.json` is still absent, and the configuration remains unfrozen.
- Pilot, validation, and test data remain ungenerated and unread. There is no confirmatory
  result.
- The director's non-blocking Phase-1 Claim Sheet review remains open in
  `director_requests.md`; no new director action is required by A2.

**Verification artifact:** no change. The payload measurement and its audit improve the
development record, but they are not the Claim Sheet's eventual hands-on result
demonstration.

## What happens next

A2 closes an interpretation gate; it does not open an execution gate. Any replacement of
the assignment, dataset supersession or regeneration, final configuration materialization,
pilot/validation/test generation, confirmatory work, Protocol P change, or second payload
measurement requires its own later explicit authorization.

The next project step is therefore a separately reviewed decision about what downstream
work is actually needed before configuration freeze. Until that decision is made, the
correct state is deliberately quiet: the amendment is in force, the success bars are
unchanged, and the untouched data stay untouched.

— Codex
