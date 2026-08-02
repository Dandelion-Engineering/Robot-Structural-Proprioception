# Progress Report — Codex Session 56

**Report date:** 2026-08-01

**Covers:** Codex Sessions 49–56

**Phase:** Phase 2 — Integration and Reproducibility Build

**Audience:** Project director

## The short version

Eight Codex sessions ago, the project had just run Protocol P's cheapest stage: a sensor-only diagnostic that measures how much two healthy readings differ when only the sensor identity changes. The stages that actually exercise the simulated robot were still unwritten.

Those stages now have a jointly approved program. It has not been run.

The program's plan contains:

```text
9 admissible probe candidates
180 logical result rows
168 physical simulations
12 rows that reuse an earlier simulation
```

That distinction matters. A result row is a line in the final analysis table; a physical simulation is a body that actually ran. Twelve rows reuse measurements already paid for. The program now preserves that physical-versus-logical distinction, records every executed body once with its complete safety evidence, and refuses to turn an unsafe run into a scientific result.

This session closed review of the final pre-execution code addition: a check that independently derives the damage-start time from the approved trajectory document immediately before each simulation. It exists because an earlier check compared two objects built from the same caller-supplied value and therefore could not detect that the shared value was wrong.

One packet-runbook sentence remains in owner re-review after a precision edit. The 168 screen simulations remain unrun and unauthorized. The final configuration is unfrozen, and the confirmatory test split remains untouched.

## Where the project stands

Protocol P is a development screen. It asks whether structural damage produces a safe, measurable signal under a pre-declared diagnostic probe before the project commits to its final data-generation configuration.

Its current state is:

- the specification is jointly approved;
- the generator seam is jointly approved;
- a one-row replay has repeatedly reproduced its retained reference exactly;
- Stage 0 ran once and its result is jointly approved;
- the shared construction and provenance layers are jointly approved;
- the Stage-A/B/C driver and results layer are jointly approved;
- the document-derived onset check and its 37 new tests are approved by both code author and reviewer at the same exact states;
- packet README Step 25 documents the zero-rollout plan, with one reviewer wording edit awaiting owner re-review; and
- Stages A, B and C have never run.

This is substantial measuring infrastructure, not a research answer. Stage 0 is the only completed screen stage, and it has no simulated mechanics. Nothing yet establishes whether the structural signal is detectable at any severity.

## What changed since Session 48

### The first measurement reached exact-state approval

Stage 0's `0.400881` microstrain figure was independently re-derived and its artifact reached same-state approval. The review also narrowed how its identity may be described: the cryptographic fingerprint binds the run's inputs and output shape, not its measured values. It is provenance, not a tamper seal over the numbers.

Cryptographic hashes are useful here because they identify exact bytes. The relevant public standard is NIST's [Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final). A hash can only protect the object actually included in the hash expression; the project now states that boundary explicitly.

### Shared Protocol-P rules were extracted once

The text-hashing rules, exact protocol and assignment pins, canonical serialization, and common failure type moved into a small standard-library-only module. This removed MuJoCo from Stage 0's import path and gave the replay gate, Stage 0, and the Stage-A/B/C driver one shared authority.

The construction layer then made every physical screen request fail loudly unless it carries the right stage, context cell, source reservation, identity, severity, probe, and fault-onset fields. The permanent plant test separately proves the simulated link changes from nominal to softened at the correct step.

This separation is deliberate. One check answers, “Did we request the body the protocol names?” The other answers, “Does the simulator actually switch that body at the named instant?” Neither implies the other.

### Reuse provenance was settled before implementation

The protocol lists 180 logical rows but budgets only 168 physical simulations. Twelve rows reuse a selected Stage-A measurement in later stages.

The first naive implementation path could have created a new stage-specific fingerprint for each reused row. Those fingerprints would look valid even though the corresponding bodies never ran. The settled rule is simpler:

> The simulation that physically ran owns the provenance stamp. Every logical reuse points back to that immutable origin; it never mints a replacement.

This is now enforced in both directions. The physical ledger contains 168 distinct stamps on the clean path; the analysis table contains 180 provenance references, twelve of which repeat an origin.

### A green suite missed two whole-program failures

Claude's first driver implementation passed 906 tests. Whole-program stand-in executions still revealed two dangerous states:

1. If one candidate was dropped by a safety gate and another survived, the program spent 73 stand-in simulations and then called all 73 “unplanned.”
2. Stage B and Stage C computed safety reports but did not use them when building scientific verdicts, so an actuator-saturating ladder value could be labelled measurable and an unsafe healthy replicate could enter the baseline.

The result file also omitted the safety evidence needed to audit those failures afterward.

The corrected state preserves every simulation it spends, on normal and terminal paths, with its safety report, step count, runtime, exact request, and provenance. Unsafe Stage-B values cannot receive a scientific case, and an unsafe Stage-C healthy reference cannot enter the null distribution.

The lesson is not that automated tests failed. It is that unit-level green tests and whole-program state coverage answer different questions. The fix was to add discriminating end-to-end driver states without spending a real simulation.

### The damage-onset check became genuinely independent

Protocol P exists partly because an earlier prototype could have softened the body from step 0 instead of the declared step 500 while still passing every later safety gate.

The construction layer's original runtime comparison could not detect a wrong onset if both the built tuple and its expected tuple were created from the same wrong onset argument. Session 56 added the missing pre-registered helper and a new driver-level check whose expected onset comes directly from the approved trajectory document.

The distinction was demonstrated rather than inferred:

```text
real override bundle built at onset 0
old same-input construction comparison     accepted
new document-derived comparison            refused before execution
```

The test also proves the rollout executor is never called after the refusal.

This is a small example of why pre-registration matters. The Center for Open Science's [preregistration overview](https://www.cos.io/initiatives/prereg) describes the general purpose: separate decisions made before seeing results from choices made after. Here, the benefit appears one layer earlier—the written plan gives the code an independent source against which to check the request it is about to run.

### The runbook now exposes a zero-cost audit path

Packet README Step 25 lets an outside reader build and inspect the complete Stage-A/B/C plan without running a simulation. My independent run completed in 0.287 seconds and reproduced:

```text
9 candidates / 180 rows / 168 simulations / 12 reuses
fault onset 500
measurement window [1000, 1768)
results = null
```

The artifact now records the config as `config/draft-config-v0.1.json`, not as a full `C:\Users\...` path from the machine that produced it.

I made one wording correction in the runbook: the table has 180 provenance references comprising 168 distinct stamps, not “180 stamps” in the identity sense. Claude must reopen and explicitly approve that exact reviewer-edited state before the runbook loop closes.

## What surprised me

### The hardest bugs were relation bugs

Most of the consequential findings were not wrong constants or syntax errors. They were mismatches between two objects that were individually plausible:

- logical rows versus physical simulations;
- a safety report versus the verdict that should consume it;
- a constructed fault tuple versus the document that should authorize its onset;
- a result row versus the physical ledger entry that measured it; and
- a readable input path versus a portable scientific artifact.

Local checks can prove each object is well formed while the relation between them is wrong. The driver now tests those relations at the boundary where the objects meet.

### A deliberately redundant check can be honest

The new helper explicitly refuses unknown condition names, and the builder it calls independently refuses them too. Removing the helper's line would change only which error message appears.

Normally one authority is preferable. I approved keeping this line because the pre-registered code sketch places the refusal inside the named helper, the condition tuple is imported rather than copied, and the documentation/tests plainly mark the line as non-load-bearing. Redundancy is dangerous when it is mistaken for independent protection; it is manageable when its limited purpose is explicit.

### The cost record needed the same physical-versus-official distinction

Claude's Session-56 progress report originally said Protocol P had spent one simulation total. Cross-review found that the project has one official replay result but four physical replay-gate executions: the original Session-45 result, two Session-46 implementation-verification runs, and one Session-51 regression run after an import edit.

The distinction changes no result and no Stage-A/B/C boundary. It matters because a cost record should count physical executions even when two were deliberately induced verification runs rather than official scientific results. I corrected Claude's report directly and returned the reviewer-edited exact state for owner re-review.

## What is working

- The Protocol-P specification and every executable layer through the Stage-A/B/C driver are jointly approved.
- Physical and logical rollout accounting are separated explicitly.
- Every executed body has one audit record with complete safety and provenance evidence.
- Unsafe Stage-B and Stage-C states fail closed before a scientific case or operative null exists.
- The structural onset is independently checked against the approved trajectory document before every physical screen run.
- Plan mode is the safe CLI default and runs zero simulations.
- The full packet suite passes **975 tests**.
- The zero-rollout plan artifact contains no absolute machine path.
- Stage 0 remains the only completed screen stage.
- The final config lifecycle still blocks confirmatory work.

## What is not working or not ready

- Packet README Step 25 awaits Claude's same-state re-review after one precision edit.
- Claude's Session-56 progress report awaits owner re-review after the replay-count correction.
- The one-row replay has not yet been rerun immediately before the prospective screen.
- No explicit decision authorizes the 168 Stage-A/B/C simulations.
- The central structural-detectability screen has no result.
- Amendment A2 is not written or approved.
- Replacement assignment/config lineage and coherent regeneration remain downstream.
- Gates 4–7 and the final immutable `config.json` remain open.
- The Phase-3 interactive verification artifact does not yet exist.
- The confirmatory test split remains deliberately untouched.

Nothing in this session requires a new director decision. The execution decision remains an agent review gate under the approved protocol.

## Verification-path update

The project now has three complementary pre-measurement checks:

1. **Replay gate:** rebuild one retained physical row and compare every watched value and filesystem scope.
2. **Stage 0:** reproduce the sensor-only healthy-difference diagnostic with no plant rollout.
3. **Plan mode:** verify every Stage-A/B/C input pin, timing derivation, row count, reuse count, and provenance shape while running zero simulations.

I accepted the proposal to run the one-row replay once more in the dedicated execution round immediately before measurement. That future round should authorize the replay check explicitly, review its PASS, and only then make the separate decision on the 168 screen simulations.

This is still pre-confirmatory infrastructure. The eventual director verification artifact remains a Phase-3 deliverable.

## The next stretch

The gated order is:

1. Claude reopens packet README blob `9c9fa7f03de8b000580704330755f232cfdb8ef1` and progress-report blob `39c592422639b84005a2dd7d9539171be541a84c`, explicitly approving each unchanged or returning a new state.
2. The agents enter a separate execution-authorization round.
3. Explicitly authorize and run the one-row replay gate immediately before measurement, then review its result.
4. Decide whether to authorize the 168 Stage-A/B/C simulations.
5. If authorized, run the screen once under the approved driver and review the result artifact before any downstream interpretation.
6. Only after that result loop closes: write Amendment A2, produce replacement assignment/config lineage, regenerate coherently, close Gates 4–7, freeze one immutable config, and materialize the confirmatory split once.

The current headline remains deliberately narrow: **the development screen is now executable and independently reviewed, but the experiment that could establish structural detectability has not run.**
