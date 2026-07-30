# Progress Report — Codex Session 48

**Report date:** 2026-07-30

**Covers:** Codex Sessions 41–48

**Phase:** Phase 2 — Integration and Reproducibility Build

**Audience:** Project director

## The short version

Eight Codex sessions ago, Protocol P was a detailed but still non-executable plan for
checking whether the structural-fault settings in this project are measurable under a
safe, pre-declared probe.

It is now an exact, jointly approved specification with an approved generator seam, a
bit-for-bit replay of one retained development row, and its first executed measurement.
That first measurement is deliberately modest: it contains no simulated robot and no
fault. It asks how much the four-gauge difference statistic moves when only the sensor
identity changes.

The result is:

```text
100 paired healthy sensor draws
95th percentile, method="higher"   0.400881 microstrain
prior fixed-trace cell range       0.3176–0.4251 microstrain
```

The value falls inside the broad pre-registered range, but near its upper end: it exceeds
three of the four earlier cell values and is only 5.7% below the maximum. That is limited
corroboration, not agreement with the physics, not a detection threshold, and not
evidence that structural sensing helps.

The artifact itself passed my independent review unchanged. Its review loop is still
open for one procedural reason: the owner handed it off without explicitly approving
the exact file. Project rules do not let me infer approval from creation, a self-audit,
or silence. Stages A, B, and C remain unauthorized until that explicit approval lands.

The final configuration remains unfrozen. No confirmatory test identity or payload
exists.

## Why so much work preceded one small number

Protocol P is a development-only instrument check. Before spending 168 additional
simulated rollouts on a structural-severity ladder, the project needs to know that:

- it can reproduce a known retained row exactly;
- the new screen-only controls actually reach the physical plant and sensor path;
- the simulated link softens at the declared step rather than from the beginning;
- every result is bound to the exact protocol, assignment, draft config, and command;
- a screen run cannot write into the retained dataset;
- the statistic and null are fixed before seeing the deciding values; and
- the result cannot be mistaken for confirmatory evidence.

This is the practical value of pre-registration: it separates decisions made before a
measurement from interpretations made afterward. The
[Center for Open Science](https://www.cos.io/initiatives/prereg) describes the same
general discipline.

Across Sessions 41–48, most findings were not about the high-level scientific question.
They were about places where precise-looking code or prose could have measured a
different object from the one the protocol named.

## What changed since Session 40

### The specification became an exact tracked artifact

Sessions 41–43 took Protocol P through three exact-state versions. The final approved
file is `protocol-p-v2.3.3.md`.

Those reviews found several executability defects:

- text fingerprints and binary payload fingerprints were being treated as if they had
  the same line-ending rules;
- an undefined abbreviation had acquired two incompatible meanings, one descriptive
  and one verdict-bearing;
- the Stage-0 identity expression named one payload and hashed another;
- a seed-base constant was declared but bypassed by repeated literals;
- one fault-onset expression used an unbound timestep name; and
- the plant-timing invariant could not be checked at the place the text first assigned
  it.

None changed the intended science. All could have changed what an implementation did or
what a reader believed had authority.

The project uses SHA-256 fingerprints to identify exact files and canonical states. This
is identity, not secrecy; the underlying standard is NIST's
[Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).

### The fault-timing boundary became a permanent test

The plant now has a permanent regression test proving that the structural model remains
nominal through step 499 and switches at step 500. That test matters because the
screen's safety checks had large margins and could still pass if the link were softened
from the start. Correct construction and physical admissibility are separate questions;
one cannot stand in for the other.

### The generator seam reached joint approval

The approved screen-only seam can change probe peak, ramp fraction, physical fault, and
screen identity without altering the approved assignment or ordinary generation path.
Its tests verify the values at the real plant-construction site and through both sensor
paths.

An early test suite missed a particularly dangerous wiring defect: the lower-level
helper accepted the override correctly, but the caller could forget to forward it. In
that state, results would record the candidate we believed we ran while the plant
received the delivered default. Deliberately injecting that fault turned the missing
test from a theoretical concern into a measured one.

### One retained row replayed exactly

The replay gate rebuilt one existing development reservation and compared it with the
retained references:

```text
identity fields                       20 / 20 equal
privileged plant payload fields       20 / 20 equal
structural observation entries        38 / 38 equal
matched missing-value positions       531
watched filesystem changes            0
```

That is a one-row construction positive control. It does not generalize to the other
471 retained reservations and says nothing about fault detectability.

Review then found that the first replay gate could still print PASS after observing a
watched-file change and could miss a newly created repository-top-level file. Both
paths were corrected and verified through the real command line, not only through
direct helper calls.

### Stage 0 was wired, reviewed, and run

Stage 0 computes one scalar per pair:

```text
D = the length of the difference between two four-gauge harmonic-coefficient vectors
```

Each vector has eight entries: cosine and sine coefficients from each of four gauges.
The same zero mechanical strain and linear thermal profile are used on both sides; only
the sensor seed changes. One hundred pairs consume seeds 0 through 199 exactly once.

The implementation review took three rounds because each round found a different
evidence problem:

1. the first implementation stamped the bound config hash but constructed its sensor
   model from independent defaults;
2. three command-line pins duplicated bound timing values without checking equality;
3. a test described a binding-bypassed state as constructible end to end; and
4. another test reimplemented the production binding arithmetic instead of calling the
   binding gate.

The final implementation state is jointly approved. Claude explicitly approved it
before executing the one authorized Stage-0 run.

## What Stage 0 found

The written artifact contains 100 finite distances:

```text
mean                    0.278734 microstrain
population standard dev 0.074773 microstrain
minimum                 0.114994 microstrain
median                  0.279701 microstrain
maximum                 0.569876 microstrain
95th percentile         0.400881 microstrain
```

I independently parsed the file with duplicate-key rejection; recomputed its mean,
population standard deviation, extrema, median, and `higher` 95th percentile; and
reconstructed its `dev-` identity from the embedded canonical string. I also reproduced
the protocol digest, assignment digest, assignment self-hash, draft-config self-hash,
and production assignment/config binding.

Four observations exceed the reported percentile and five are at or above it. That
small distinction corrected one sentence in the director-facing report but does not
change the statistic.

### What the number means

The earlier fixed-trace exercise held one healthy simulated plant trace fixed in each
of four cells and re-read it under different sensor identities. Its per-cell 95th
percentiles were:

```text
0.3176   0.3555   0.3854   0.4251 microstrain
```

Stage 0's `0.400881` is inside that range. This is the one corroboration Protocol P
declared.

The honest boundary is just as important:

- it is conditional on one pair id, window length, thermal profile, sensor model, and
  difference operation;
- the fixed-trace values are four conditional diagnostics, not a population reference;
- Stage 0 has no plant, mechanics, or fault;
- it sets no threshold and gates no decision; and
- the later Stage-C per-cell nulls, not Stage 0, govern the development screen.

The public running log initially called `0.401` a floor below which damage is invisible
and called an input-binding check a safety gate. I added an append-only correction:
`0.401` is not a detection threshold, and configuration identity is not physical safety.
The old entry remains visible, as the public-history rule requires.

## What surprised me

### A correct artifact can still have an open review loop

Claude's result turn was detailed and self-critical. It recomputed the artifact's main
statistics and identity and clearly requested review. It did not, however, explicitly
say that Claude approved the exact artifact.

That sounds procedural until the alternative is considered. If creation or careful
description counted as approval, an owner could hand off a state it did not endorse and
the reviewer could unknowingly close the loop. The rule that both agents approve the
same bytes exists precisely to prevent that ambiguity.

I approved the artifact unchanged and returned it for one explicit owner approval.

### The run time was promised and then lost

The prior handoff said the first-run elapsed time would be recorded when Stage 0 ran. It
was not recorded in the artifact, transcript result, or report. The number cannot be
reconstructed honestly from commit timestamps.

This does not affect the measurement or violate Protocol P, which does not bind runtime.
It is still a documentation miss. The right response is not to run the stage a second
time merely to manufacture a first-run number. The packet runbook should say that the
first-run elapsed time was not captured unless a later, separately authorized
reproduction is timed and labeled as such.

## What is working

- Protocol P v2.3.3 is jointly approved at one exact digest.
- The structural-onset test, generator seam, replay gate, and Stage-0 implementation
  have closed same-state review loops.
- One retained development row has passed an exact replay gate.
- Stage 0 has run once and its artifact passes independent identity and statistic audit.
- The packet suite passes **595 tests**.
- The root public record corrects overclaims forward instead of silently rewriting them.
- The final config lifecycle still refuses confirmatory work.
- The test split remains untouched.

## What is not working or not ready

- The Stage-0 result review is still open pending the owner's explicit approval of the
  unchanged artifact.
- Claude's Session-48 progress report is in a small reviewer-edited loop for three
  evidence-boundary corrections.
- The first-run Stage-0 wall clock was not captured.
- The Stage-A/B/C driver does not exist and is unauthorized.
- The central development screen has not measured structural detectability.
- Amendment A2 is not written or approved.
- The existing 472-reservation non-test dataset is pre-amendment and must not be
  relabeled under a new design.
- Gate-4 models, calibration, controller authorization, the final evaluation driver,
  final `config.json`, and confirmatory materialization remain open.
- The project hypothesis has not been answered.

Nothing is blocked on a new director decision. The existing Claim Sheet review request
remains non-blocking.

## Verification-path update

The reproducibility path now has two complementary controls:

1. **Replay:** one retained plant-bearing development row rebuilds exactly with no
   filesystem residue.
2. **Stage 0:** a clean checkout can reproduce the sensor-only difference diagnostic
   without the retained dataset or MuJoCo.

Stage 0's runbook step should be added only after its result artifact reaches explicit
same-state approval. The first-run runtime must be labeled as not captured.

This is still pre-confirmatory infrastructure. The Phase-3 director verification
artifact does not yet exist.

## The next stretch

The gated order is:

1. Claude explicitly approves or edits-and-returns the unchanged Stage-0 result
   artifact.
2. Claude owner-reviews the three corrections to its Session-48 progress report.
3. After result closure, Claude adds the Stage-0 packet runbook step.
4. Claude implements the Stage-A/B/C driver against the already-recorded construction,
   identity, safety, and no-persistence requirements and hands it off unrun.
5. Codex reviews that driver and its real-output-root tests.
6. Only after same-state implementation approval may Stage A run; Stages B and C remain
   sequentially gated behind it.
7. Both agents review the terminal Protocol-P result before any written Amendment A2,
   replacement assignment, dataset regeneration, or final config freeze.

The current headline is intentionally narrow: **the measuring path now has one reviewed
sensor-only diagnostic, but the development experiment that could test structural
detectability has not begun.**
