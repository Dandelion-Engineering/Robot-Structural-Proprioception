# Progress Report — Codex Session 40

**Report date:** 2026-07-29

**Covers:** Codex Sessions 33–40

**Phase:** Phase 2 — Integration and Reproducibility Build

**Audience:** Project director

## The short version

At my Session 32, the project had a reviewed experiment plan and a complete
non-test base dataset. The obvious next move looked like fitting models.

We did not do that.

The first development-only feasibility analysis showed that the delivered
structural settings and excitation did not clear the prerequisite needed for a
fair learned comparison. Rather than fit models to a structural class whose
physical signature might not be measurable, the project stopped and began
designing a bounded repair.

Eight Codex sessions later, that repair is close but still not authorized. We
have a much better pre-registered measurement, a one-row bit-exact replay of
the real generator, and a conservative plan that can end in a narrow positive
or a bounded negative. We have also found several ways that apparently precise
text could have caused the implementation to measure the wrong thing.

The latest one is simple: the proposed structural override forgot to say when
the fault begins. In the actual code, “not specified” means step 0. The
experiment says step 500. Until those agree, the measurement stays blocked.

No final configuration exists. No test identity or payload has been generated.
No Protocol-P statistic exists. That restraint is the most important result of
this interval.

## Why the project stopped before model fitting

The core comparison asks whether four body-strain channels improve diagnosis
beyond a conventional robot sensor suite. Before training a classifier, the
project needs to know that a safe, prospectively chosen probe produces a
repeatable mechanical difference at the structural severities assigned to the
study.

That is an **instrument check**, not the project result. It is analogous to
checking that a scale can resolve the weight difference before comparing two
groups. If the scale cannot resolve it, a classifier score would mix scientific
absence with measurement failure.

The first screen was development-only. It did not inspect the confirmatory test
set and did not establish that structural sensing fails. It established
something narrower: under the delivered excitation and analysis, the current
structural settings did not satisfy the prerequisite separability gate.

That finding triggered the Claim Sheet's amendment process. The repair has
remained text-only because a pre-registration is useful only if the rules are
settled before the deciding measurement. The
[Center for Open Science](https://www.cos.io/initiatives/prereg) describes the
same underlying idea: distinguish planned tests from choices made after seeing
the result.

## What changed since Session 32

### The real generator passed independent hardening

Session 33 reviewed the newly generated dev/pilot/validation base roles and
approved a bounded hardening pass. The generator is tied to the approved
assignment and draft configuration, writes role-separated data, preserves
matched C1/S plant truth and common channels, forbids test materialization, and
passes an independent on-disk audit.

The retained local state still contains:

```text
472 approved non-test reservations
944 C1/S manifest rows
472 byte-identical matched plant pairs
472 bitwise-identical shared-channel pairs
0 test identities or payloads
```

That dataset is pre-amendment development infrastructure, not the final study
under a changed design.

### The first structural repair was too optimistic

Session 34 independently reproduced the development structural-separability
screen and agreed that the scientific direction needed repair. It also blocked
the proposed amendment language because the public claim generalized a
development result beyond the actual estimand.

The correction mattered: a four-cell diagnostic cannot reach a conventional
5% exact sign-test threshold, and a pooled development screen is not evidence
about all splits, all reserved severities, or the final confirmatory question.

### The protocol became more exact one defect at a time

Sessions 35–38 progressively pinned the measurement:

- ordinary and diagnostic probe semantics;
- prospective severity assignment across splits;
- one exact four-gauge statistic rather than an unnamed aggregate;
- exact contact scope and probe-start window;
- a branch-complete candidate selection rule;
- a cellwise healthy null rather than one pooled threshold;
- eight healthy replicates per context cell;
- a conservative finite-sample quantile;
- explicit common-random-number identities;
- safe terminal outcomes that never carry an unsafe choice forward;
- role coverage for dev, pilot, validation, and test; and
- PowerShell-executable commands and fail-loud array-shape guards.

These details are not decorative. Each one removes a choice that could
otherwise be made after looking at the development measurement.

For example, the probe begins one second after the fault. The old analysis
window began at fault onset, so much of it contained no probe. Moving the
window to the configuration-derived probe start was a valid prospective
correction. A response-selected window that happened to maximize the strain
difference was measured and explicitly rejected.

### One exact row now rebuilds bit for bit

Session 39 independently rebuilt one already-delivered healthy development
reservation through the committed assignment, draft config, generator, plant,
and sensor path.

```text
20 / 20 privileged physical arrays matched byte for byte
38 / 38 persisted observation entries matched byte for byte
```

This is strong evidence about that one row and the default generator path. It
is not evidence that all 472 retained reservations were regenerated, and it
does not validate a new override branch that the old generator did not have.

Bit-exact replay is valuable because it turns the generator into a positive
control: if a known row cannot be rebuilt, the new measurement does not start.
The role of a cryptographic hash here is identity, not secrecy. NIST's
[Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)
defines SHA-256; the project uses it as a fingerprint for exact files and
canonical machine-readable states.

## What the latest review found

Claude's Protocol P v2.3 fixes the major problems from the prior version. It
defines a typed, screen-only path for changing probe amplitude, probe ramp,
structural severity, and screen identity without silently editing the approved
assignment. It distinguishes the reservation's base identity from the identity
the sensor random-number streams actually receive. It narrows the replay,
unmatched-row, and gauge-only claims to the evidence they support.

The remaining block is mechanical.

### The structural fault would begin at the wrong time

The direct `FaultSpec` object lists the damage type and severity but omits
`onset_index`. The class default is `-1`. The plant converts that to step 0.

The approved diagnostic trajectory instead introduces the fault at 1.0 second,
or step 500 on the 500 Hz control grid. That difference removes the healthy
pre-change segment and changes the closed-loop history before the probe begins.
It is not a harmless metadata omission.

The correction is small: set the onset explicitly from the trajectory and test
that the fault activates at step 500.

### The provenance guard is still descriptive rather than enforced

The proposed seam requires a nonempty provenance string. A caller could satisfy
that rule by passing the base configuration hash unchanged, even though the
proposal says an altered run cannot carry the base identity.

The proposed new string also does not match the packet's existing hash
lifecycle. It abbreviates SHA-256 to 32 hex characters and inserts descriptive
words after `dev-`; the packet accepts `dev-` plus a full 64-hex digest.

The fix is again local:

- hash one complete canonical protocol specification;
- use the full digest;
- require the derived hash to differ from the base; and
- make any raw file hashes byte-stable across Windows and Unix checkouts.

## What surprised me

The strongest recurring pattern is that a correct high-level idea can fail at
the boundary between two correct pieces of code.

- The generator correctly appends `_dataset0`; the old proposal correctly
  wanted a private screen namespace. Putting them together made the advertised
  leak guard test the wrong identity.
- `FaultSpec` correctly allows a default onset for other callers; the new seam
  correctly accepts a typed `FaultSpec`. Putting them together activates this
  experiment's fault at step 0.
- The provenance object correctly names its sources; the storage contract
  correctly requires a full hash. Putting them together still produces an
  invalid identity unless the formats are reconciled.

This is why executable pre-registration is doing more work than prose review.
The goal is not only to state what we mean. It is to remove every place where
an implementer could reasonably choose something different.

## What is working

- The two-agent review loop continues to find direction-of-error problems
  before decision-bearing simulations run.
- The public and internal records preserve earlier overstatements and add
  forward corrections rather than silently rewriting history.
- Development, pilot, validation, and confirmatory roles remain separate.
- The final config lifecycle still refuses confirmatory materialization.
- The current generator and packet remain green at **399 tests**.
- One real default-path development row has two independent bit-exact replays.
- The new protocol's candidate grid, safe terminal branches, per-cell healthy
  null, common-random-number identities, OOD handling, and role-coverage rules
  now survive review.

## What is not working or not ready

- Protocol P v2.3 is not executable as approved because the fault onset and
  provenance enforcement remain wrong.
- The typed override seam exists only as Claude's scratch prototype; no packet
  implementation has been approved.
- Protocol P has not run. Its Case A/B/C result is unknown.
- The current rough odds put “some severe settings are measurable” and “none
  are measurable under the safe probe” in roughly comparable territory. These
  are estimates, not results.
- A written Amendment A2 does not exist.
- The Claim Sheet and Accessible Claim Sheet have not been amended.
- A replacement exact assignment does not exist.
- The pre-amendment non-test dataset cannot be silently relabeled under a new
  design.
- Gate-4 learned models, validation calibration, controller authorization,
  evaluation driver, final `config.json`, and confirmatory test material remain
  open.
- The Phase-3 verification artifact has no new state to report.

Nothing is blocked on a new director decision. The open Claim Sheet review in
`director_requests.md` remains explicitly non-blocking.

## Verification-path update

The genuinely new verification element since Session 32 is the one-row
default-path replay. It proves that the committed code can reconstruct one
retained development row exactly from its committed authorities and local
reference payload.

The proposed next layer is not approved yet. Once corrected, it will add:

1. a hash-checked local replay reference;
2. exact default-path byte equality;
3. branch-specific tests for every screen override;
4. a fault-onset reach test;
5. lifecycle-valid, base-distinct provenance;
6. explicit no-persistence checks for screen records and labels; and
7. a results-only Protocol-P artifact reviewed before any amendment is written.

That is infrastructure for deciding whether the structural class is measurable.
It is not the final director-facing verification artifact promised for Phase 3.

## The next stretch

The immediate sequence remains deliberately gated:

1. Claude appends one narrow correction for fault onset and provenance and
   explicitly approves that exact state.
2. Codex re-reviews the correction.
3. Only after proposal approval does Claude apply the screen seam and post the
   code diff.
4. Codex reviews the implementation and branch-specific tests.
5. Only after implementation approval does the one-row replay gate run.
6. If it passes, the development-only Protocol-P stages run and produce one
   pre-registered Case A, B, C, or terminal result.
7. Both agents review that result before any written amendment, assignment
   replacement, or regeneration.

The project remains in Phase 2. The correct headline is neither “the structural
idea works” nor “it failed.” It is: **the team is still making the measuring
instrument exact enough that either answer will mean what it says.**
