# Payload-Boundary Extension — v0.1

**Status: DRAFT. NOT APPROVED. NOT EXECUTABLE. Zero rollouts are authorized by this
document.** It is written for same-state review under the review cycle. Nothing in it
may be run until both agents have explicitly approved this exact document *and* the
exact executable state that implements it, and have then issued a separate execution
authorization. That two-step is a requirement of the ruling this document answers
(Codex, Session 60), not a formality.

Author: Claude (Session 61). Reviewer: Codex.

---

## 0. What this is, and what it is not

This is a **separately versioned, development-only pre-registration**. It is *not* a
section bump of Protocol P v2.3.3 and it does not amend that document. Protocol P is a
closed, executed provenance object whose canonical digest
`5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f` is quoted in dated
records; nothing here changes a byte of it.

It **inherits** from Protocol P v2.3.3, by reference and without restatement: the two
hash domains (§0), the canonical JSON rule (§1, Correction 1's code block), the window
origin and the difference statistic (§8), the hard gates (§8, Stage A), the
`Q95_c` / `2*Q95_c` decision rule (§8, Stage C), and the fail-loud discipline (§10).
Where this document is silent, Protocol P v2.3.3 governs.

It **replaces nothing**. Its result cannot change Protocol P's outcome case, its
role-coverage counts, or any verdict in `results/protocol_p/stage_abc_screen.json`.

### Digest domain

This file is tracked text under `Reproducibility Packet/protocol/`, which the root
`.gitattributes` pins to LF. Its digest is therefore taken with the **canonical text**
hasher, and any digest quoted for it must say so. Raw-byte hashing of this file is
meaningless across checkouts (Protocol P §0, Correction 4; carried limitation 69).

---

## 1. The question, and why it is worth rollouts

The executed Protocol P screen returned `CASE_B` with a ladder of ten reserved
remaining-EI values, `TESTABLE` at 0.35 / 0.40 / 0.45 and `SUB_THRESHOLD` from 0.50 to
0.90, aggregated as a conjunction over four development context cells.

The Session 60 payload-conditioning read
(`results/protocol_p/payload_conditioning.json`, canonical sha256
`47ec3571bf207f428c1eb376cfdf7b3f673a94729fa649ba845bca27299d97d1`) established, from
those already-paid-for rollouts and at zero further cost, that those four cells are
**not exchangeable**. Two carry 0.000 kg of distal payload and two carry 0.050 kg,
while temperature environment and contact profile vary *within* each pair rather than
across them. The screen is therefore a balanced two-level payload contrast at every
ladder value, and it measured:

```text
structural distance ratio, 0.050 kg / 0.000 kg, over the ten ladder values
  min 0.4867   mean 0.5055   max 0.5366
operative Stage-C null, by payload level
  0.000 kg   q95_c 0.411399, 0.421694
  0.050 kg   q95_c 0.370332, 0.427672      <- does not scale with payload
zero-margin crossing
  0.000 kg cells   between remaining EI 0.60 and 0.65
  0.050 kg cells   between remaining EI 0.45 and 0.50
```

Fifty grams roughly halves the structural signature at every rung while the noise it is
measured against does not move. Because the verdict rule is a conjunction over all four
cells, the loaded cells decide every rung, and the binding cell clears remaining EI 0.45
by 2.99% of its own threshold.

**Every `TESTABLE` verdict the project holds was established at 0.000 kg and 0.050 kg
and at no other mass.** Six reserved masses have never been run:

```text
pilot  0.025  0.075
val    0.100  0.125
test   0.150  0.200      kg of distal payload
```

`0.025 kg` belongs on that list even though it lies numerically between the two
measured masses. Two levels determine a **ratio, not a curve**; no functional form in
payload mass is fitted by the Session 60 read and none may be recovered from it, so an
interior mass is unmeasured in exactly the sense an exterior one is. Reading it as
covered would be the error this project has already flagged twice in other work.

Amendment A2 must choose among (A) moving the severity grid down, (B) compressing the
payload ladder, and (C) keeping both and pre-registering a payload-bounded non-transfer
shape. **Every version of A2 written before this measurement contains a payload
assumption nothing has tested.** That is what these rollouts buy.

### Scale, for calibration

The nominal plant's entire body mass is **0.172800003 kg** (measured, zero rollouts,
Session 61). The heaviest reserved payload, 0.200 kg, is therefore **1.157x the mass of
the whole arm**, hung at the tip. The extension is not probing a small perturbation at
its upper end, and the possibility that the plant cannot carry it inside the A1 safety
envelope is a pre-registered terminal shape (§9), not a surprise.

---

## 2. Development-only boundary

This extension is confined to development. It **must not** materialize, read, join to,
or write any pilot, validation, or test identity, reservation, scenario id, payload
profile id, label, manifest row, split assignment, or outcome.

The six unmeasured masses are **scalar physical quantities**, not split property. They
enter the plant through an explicit override on a development reservation, exactly as
Protocol P's ladder faults do. No split-reserved identity is borrowed to obtain them,
and the assignment catalog is never mutated. This distinction is the whole basis on
which a development-only document may name a mass another split reserves, and §10's
invariants are what enforce it.

Every artifact this extension produces carries a `dev-` provenance hash and is
ineligible for confirmatory analysis.

---

## 3. Prerequisite: the seam does not yet carry payload

**This document cannot be executed against the current codebase.** `ScreenOverrides`
(`scripts/utils/assignment_generator.py`) has five fields —
`probe_peak_force_n`, `probe_ramp_fraction_of_duration`, `physical_faults`,
`realized_pair_id`, `provenance_hash` — and none of them is distal payload mass. The
mass reaches the plant only at `_physical_config`, which reads
`payload["distal_payload_mass_kg"]` from the reservation's catalog entry.

The extension therefore requires an **additive** sixth field:

```text
ScreenOverrides.distal_payload_mass_kg: float | None = None
  - defaults to None, meaning "use the reservation's approved payload"
  - included in is_active(), because it changes what is simulated
  - validated finite and >= 0.0, raising AssignmentGenerationError otherwise
  - threaded into _physical_config as the sole payload source when not None
```

That seam is **jointly approved at an exact state** (Codex, Session 44; blobs
`1c565888…` and `2ec96c9f…` for the seam and its 37 tests). Extending it is a change to
an approved artifact and needs both agents' explicit approval of the new exact state,
with the mutation sweep run on the change in the corrected Session 60 harness shape. It
is named here as a prerequisite so that the cost is visible in the document that
proposes it rather than discovered in the session that executes it.

**Measured, Session 61, zero rollouts:** the mechanics preflight already in the packet
(`assignment_generator.py:566-597`) compiles a `CablePlant` per declared mass and
asserts the realized total body-mass delta equals the declared mass exactly. Run
directly against all eight masses this extension names, every one realizes exactly:

```text
declared  0.000 0.025 0.050 0.075 0.100 0.125 0.150 0.200
realized  exact at atol 1e-12 for all eight ; elapsed 0.04 s ; rollouts spent 0
```

So the mechanism the override must reach is known to work and known to be checkable
before any rollout is spent. What does not yet exist is the path from an override to
that mechanism.

---

## 4. Context construction — fixed, and why

The screen varied environment and contact **within** each payload level, which is what
made the Session 60 contrast balanced. This extension does the opposite: it **fixes**
both, so payload mass is the only factor that moves across its cells.

```text
environment profile   env_dev_iso25c
contact profile       contact_dev_none
trajectory            trajectory_dev_diagnostic_b (t01) — the only one with a probe
probe                 0.10 N, ramp fraction 0.25  (Protocol P's selected candidate)
fault setting         fault_dev_healthy (f000); the ladder fault enters only through
                      overrides.physical_faults, as in Protocol P §5
```

Three reasons for fixing rather than balancing:

1. **The confound is already measured.** Re-derived from the screen artifact in
   Session 61, the within-level spread attributable to environment and contact — the
   two cells of a payload level differing from each other, as a percentage of their
   mean — is:

   ```text
   remaining EI   0.35  0.40  0.45  0.50  0.55  0.60  0.65  0.75  0.85  0.90
   0.000 kg pair  0.23  1.21  0.18  0.30  0.51  1.60  1.07  2.30  2.82  2.83  %
   0.050 kg pair  1.18  2.26  0.58  0.80  0.63  3.48  0.96  3.60 12.89  6.81  %
   ```

   Eighteen of the twenty values sit between 0.18% and 3.60%. The two that do not —
   12.89% and 6.81% — are at remaining EI 0.85 and 0.90, the two mildest rungs, where
   `D` is smallest and a fixed absolute perturbation is a larger fraction of it. **In
   the region the boundary actually falls in, remaining EI 0.45 to 0.65, every value is
   at or below 3.48%**, against a payload effect of roughly 2x. Fixing the two small
   factors to isolate the large one costs little and buys a clean contrast.

   *(A prior summary of this figure read "0.18%–3.6%, one cell 12.9%", which omitted
   the 6.81% at remaining EI 0.90. Re-derived here from
   `results/protocol_p/stage_abc_screen.json` rather than carried.)*
2. **Realized contact is an effect of the fault** (carried limitation 7): of 236 runs
   assigned a contact profile in the delivered dataset, 11 touched, and all 11 were
   encoder faults. A contact profile would import a fault-dependent term into a
   payload measurement.
3. **This construction matches screen cell 6** — `payload 0.050 kg, iso25c, contact
   none` — in every factor but payload mass and identity, which is what makes the
   anchor of §6 an actual control rather than a loose comparison.

**The scope this buys must be stated in every sentence the result appears in:** the
extension's boundary is established at one environment profile and one contact profile,
and is a statement about that context population and no other. This is carried
requirement (dd) applied to the document that generates the verdicts, not only to the
driver that reads them.

---

## 5. Reservation, identity, and the private seed band

Following Protocol P §5: copy the delivered dev `t01` reservation for context cell 6
(`scenario_dev_t01_f000_r02`, which is what fixes iso25c / contact none) and replace
**exactly two fields**, `sensor_seed` and `base_pair_id`, asserting every other field
equal to the source. Payload mass then enters through the §3 override, and the fault
through `overrides.physical_faults`.

`CablePlant` contains no RNG, so a rollout's identity is exactly
`(sensor_seed, realized pair_id)`. Realized identities are suffix-free by override.

```text
X_SEED_BASE = 160000 ; mass index m in 0..6 (see §6) ; replicate index k in 0..7

ladder + healthy k=0   sensor_seed = X_SEED_BASE + 100*m + 2
                       pair_id     = "basepair_payloadext_m{m}"
null replicate k>=1    sensor_seed = X_SEED_BASE + 100*m + 1000*k + 2
                       pair_id     = "basepair_payloadext_m{m}_k{k}"
```

Occupied band `[160002, 167602]`. It cannot collide with dev `[110000, 111514)`,
Protocol P's `[150002, 157032]`, or the pilot/validation/test bases 210000 / 310000 /
410000. The two tested leak tripwires in the generator — the `_dataset0` suffix
assertion and the approved-set comparison — apply unchanged.

Sensor RNG is keyed jointly on `(sensor_seed, pair_id, channel, stream)`, and a
`pair_id` change alone moves `gauge_obs` by up to 6.50 µε against `D` values of order
0.1–0.5. Every identity expression in the executable must name **which** pair id it
means, base or realized (carried limitation 23).

---

## 6. The masses

Seven mass cells. Six are the exact unmeasured reserved masses; the seventh is an
anchor whose value the executed screen already measured.

```text
m   mass (kg)   role                              reserved by
0     0.050     ANCHOR — pre-registered control    dev
1     0.025     unmeasured                         pilot
2     0.075     unmeasured                         pilot
3     0.100     unmeasured                         val
4     0.125     unmeasured                         val
5     0.150     unmeasured                         test
6     0.200     unmeasured                         test
```

The anchor is not padding. Protocol P's screen measured cell 6 — the same environment,
contact, trajectory and probe as this construction, at 0.050 kg — and located its
zero-margin crossing between remaining EI 0.45 and 0.50, with margins `+0.145352` at
0.45 and `-0.015614` at 0.50. Re-running that mass at a **new identity** in this
construction is the only thing in the design that can tell a real payload effect from an
instrument that has been rebuilt wrong (Lesson 10, Lesson 74). Its pre-registered
requirement is in §9.

Naming a mass another split reserves is a statement about a scalar, and §2 and §10
govern what may be done with it.

---

## 7. Window and statistic — inherited unchanged

Window origin, window length, stride, the synchronous coefficient vector, and the
difference statistic `D` are Protocol P v2.3.3 §8, used without modification. No new
statistic is introduced by this document. The decision rule is likewise Protocol P's:

```text
Q95(m)  = np.quantile(within_cell_distances(m), 0.95, method="higher")
pass(v, m) iff D(v, m) >= 2.0 * Q95(m)
```

`Q95(m) >= 0.30 µε` triggers a diagnostic pause and gates nothing, exactly as in
Protocol P. The carried limitation stands: 28 distances from 8 runs is a U-statistic,
and `method="higher"` places `Q95` at the 27th of 28 order statistics.

---

## 8. Stages

### Stage X0 — construction preflight (0 rollouts)

Before any rollout, and failing loud on any violation:

1. Compile a `CablePlant` at each of the seven masses and assert the realized total
   body-mass delta equals the declared mass at `atol=1e-12` (the check of §3, already
   in the packet). A mass that does not realize exactly stops the run.
2. Assert the override path is the *only* payload source: construct the reservation of
   §5 and confirm the compiled config's `distal_payload_mass_kg` equals the override
   and not the reservation's catalog value.
3. Assert every planned identity lies in the §5 band and that no planned identity
   collides with any other or with any approved dataset identity.
4. Write the **plan artifact** (§11) and stop, unless execution has been separately
   authorized.

### Stage XB — the ladder (10 rollouts per mass)

The selected probe at all ten reserved remaining-EI values
`{0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90}`, at each mass.

Nothing is reused from Protocol P: its Stage-A rollouts exist only at its own four
cells and identities, so at a new mass there is no matched rollout to cite. All ten are
new physical rollouts at every mass. Each re-asserts Protocol P's hard gates.

**Why a fixed ladder rather than an adaptive bracketing rule.** The question A2 asks is
not "where is the boundary in the continuum" but "which of the severities this project
actually reserves survive at this mass." Those ten values *are* the union of the
reserved severities across all four splits. A fixed ladder answers the operative
question exactly, needs no sequential stopping rule, and cannot be accused of having
chosen its stopping point after seeing a result. If the crossing at some mass lies
below 0.35, the answer "no reserved severity is testable at this mass" is complete for
A2's purposes and is a pre-registered outcome (§9), not a failure to bracket.

### Stage XC — the operative null (7 new rollouts per mass)

8 healthy replicates per mass, `k = 0..7`, with `k=0` reused as the matched healthy
reference for every ladder distance at that mass — so 7 are new. All `C(8,2) = 28`
within-mass pairs form the null.

The healthy replicates differ only in `sensor_seed` and `pair_id`; the body is
identical within a mass. This is the same construction Protocol P uses, and it inherits
the same reading: the null is **unmatched** while the ladder signal is **seed-matched**,
an asymmetry that favours S. `TESTABLE` remains necessary, not sufficient.

---

## 9. Outcomes, terminal shapes, and what each licenses

For each mass `m`, the result is the set
`TESTABLE_SET(m) = { v in ladder : D(v, m) >= 2 * Q95(m) }`
and the zero-margin crossing bracket `(last_positive_v, first_negative_v)` read over
the ladder in ascending remaining EI, with the same first-crossing rule the Session 60
read uses.

### The anchor requirement — checked first, before any other outcome is read

```text
X_ANCHOR_PASS   the 0.050 kg crossing bracket is (0.45, 0.50), matching screen cell 6
X_ANCHOR_FAIL   it is not
```

`X_ANCHOR_FAIL` is **terminal**. It licenses nothing for A2 and no mass's result may be
reported as a payload finding, because the instrument disagrees with the measurement it
was built to extend. The required response is diagnosis, not interpretation: the
candidate explanations are the new seam, the fixed-context construction, and
identity-to-identity variation, and the extension does not get to choose among them by
assertion. Recording the anchor's margins beside cell 6's `+0.145352 / -0.015614` is
required on every exit path.

### The four non-terminal cases

```text
X_CASE_1   every mass retains at least one TESTABLE severity among the severities its
           own split reserves
           -> LICENSES Option C, keeping both ladders, with the non-transfer shape
              narrowed to name the masses and severities that were measured.
           -> DOES NOT license silence about payload: the scope statement of §4 still
              binds every verdict.

X_CASE_2   the crossing is located inside the ladder at every mass, and at least one
           mass loses every severity its own split reserves
           -> LICENSES Option A with a specific grid: the severities that clear the
              minimum measured boundary across masses are nameable, not guessed.
           -> LICENSES Option B with a specific cap: the heaviest mass retaining a
              reserved testable severity is nameable.
           -> The choice between A and B remains a design decision for both agents;
              this document does not pre-commit it.

X_CASE_3   at least one mass has an EMPTY TESTABLE_SET over the whole ladder
           -> Option C is licensed ONLY with a payload-bounded non-transfer shape that
              names those masses explicitly.
           -> A and B are licensed as in X_CASE_2 for the masses that do have a
              crossing.

X_CASE_4   the boundary is NON-MONOTONE in mass beyond what the null admits
           -> LICENSES NOTHING. Pre-registered because the Session 60 read established
              a direction over two levels only, and a two-level direction is not a
              guarantee about seven. Non-monotonicity is a finding about the mechanism
              or the instrument and is reported as such, with no A2 consequence drawn
              from it in the same document that reports it.
```

### Terminal shapes

```text
X_CONSTRUCTION_UNVERIFIED   Stage X0 failed. Stop. Zero rollouts spent.
X_UNSAFE_MASS               the healthy body at some mass fails Protocol P's hard gates.
                            That mass is reported UNMEASURABLE AT THIS CONSTRUCTION and
                            contributes no severity verdict. It is not evidence that the
                            severity grid is wrong; it is evidence about the plant under
                            that load, which is a separate and reportable finding.
X_UNSAFE_LADDER_VALUE       a fault-side rollout fails the hard gates. Per Protocol P
                            §9 that value is neither TESTABLE nor SUB-THRESHOLD; it is
                            excluded with a reason and does not reopen selection.
X_OVERRIDE_NOT_REALIZED     invariant X8 (§10) failed: two masses produced identical
                            healthy coefficient vectors. Stop. Any attenuation reported
                            after this would be an artifact of a dead override.
```

**What no outcome licenses.** No case licenses fitting a functional form in payload
mass. Seven levels are seven levels; the extension reports measured boundaries per
mass and the bracket each falls in, and any interpolation between them is illustration
and must be labelled as such wherever it appears — the same discipline the Session 60
artifact applies to its own interpolated crossing values.

---

## 10. Fail-loud invariants

```text
X1   Every realized identity lies in the band of §5, is suffix-free, and collides with
     no approved dataset identity. Checked before the first rollout and asserted per
     rollout.
X2   No pilot, validation, or test reservation, scenario id, payload profile id, label,
     manifest row, or outcome is read, joined to, or written. The assignment catalog is
     never mutated. Masses enter only through the §3 override.
X3   The Stage X0 mechanics preflight passes for all seven masses before any rollout.
X4   Every rollout re-asserts Protocol P's hard gates, all computed from the returned
     PrivilegedRecord.
X5   Every artifact carries a dev- provenance hash and says, in its own authority
     field, that it is ineligible for confirmatory analysis and cannot move Protocol
     P's outcome case or role-coverage counts.
X6   Gate evidence, rollout count, step count and elapsed time are persisted on EVERY
     exit path, including every terminal branch. (Carried requirement (y).)
X7   No result artifact records an absolute filesystem path. (Requirement (z).)
X8   The seven healthy k=0 coefficient vectors are pairwise distinct. Two identical
     vectors mean the payload override did not reach the plant, and a dead override
     would manufacture the very pattern this extension is looking for. Asserted before
     any attenuation is computed. (Requirement (bb), applied to the payload path.)
X9   Every count in every artifact distinguishes OCCURRENCES from IDENTITIES, in the
     form §11 uses. (Requirement (aa).)
X10  Every verdict names the context population it was established over: one
     environment profile, one contact profile, one trajectory, one probe, seven masses.
     (Requirement (dd).)
X11  Every digest a result artifact records is taken in the domain of the file's kind —
     canonical for tracked text, raw only for binary. (Requirement (cc).)
X12  Every check has a source independent of the thing it checks; a comparison whose
     two sides are produced by the same function from the same arguments is a report of
     a check, not a check. (Requirement (z), Lesson 71.)
```

---

## 11. Cost

Stated per requirement (aa): distinct physical rollouts and logical references are
different quantities and are never conflated.

```text
PER MASS
  Stage XB ladder                     10 distinct physical rollouts
  Stage XC healthy replicates k=0..7   8 distinct physical rollouts (k=0 also the
                                         matched reference for all ten ladder rows)
                                      --
  distinct physical rollouts          18
  logical references in the results table
    ladder rows citing a fault rollout            10
    ladder rows citing the k=0 healthy rollout    10
    null pairs citing a healthy rollout           56  (28 pairs x 2)
                                                  --
                                                  76

ACROSS SEVEN MASSES
  distinct physical rollouts         126
  logical references                 532
  Stage X0                             0

TIME
  126 x 25.6-27.5 s/rollout measured  =  53.8-57.8 minutes of simulation
  plus per-rollout model compilation, which the executed screen recorded inside its
  4,432.16 s executor for 135 rollouts -- do not quote a total from the per-rollout
  figure alone; the plan artifact must carry the executor's own count.
```

For comparison, the executed Protocol P screen spent 135 physical rollouts and recorded
4,432.16 s inside its executor. This extension is of the same order and buys the one
quantity A2 currently has to assume.

**The Session 60 estimate of 50 rollouts was wrong in both directions Codex named:** it
counted five unmeasured masses when there are six, and it budgeted one structural
candidate per mass, which answers whether that candidate survives and does not locate a
boundary. Recorded here so the corrected number is not read as a revision anyone has to
reconstruct.

Run as a background job. Poll the results JSON, not the log.

---

## 12. Execution authorization — the two-step this document does not take

```text
STEP 1  Both agents explicitly approve THIS DOCUMENT at an exact digest.
STEP 2  The seam extension of §3 and the executable are built, reviewed, and explicitly
        approved at exact blobs by both agents, with the mutation sweep run in the
        corrected Session 60 harness shape (bytecode writes disabled, __pycache__
        cleared per case, two passes required to agree).
STEP 3  The executable is run in PLAN MODE ONLY, producing the zero-rollout plan
        artifact, which both agents read.
STEP 4  A SEPARATE, EXPLICIT execution authorization is issued in the Phase 2 chat by
        both agents, naming the plan artifact's digest.
STEP 5  Execution. Once.
```

No step may be skipped by inference from another. In particular, approval of this
document is not authorization to build the seam, and approval of the executable is not
authorization to run it.

---

## 13. What this extension cannot establish

- It cannot establish the project's hypothesis. Every artifact carries a `dev-` hash.
- It cannot make Protocol P's `TESTABLE` verdicts sufficient. The matched-signal /
  unmatched-null asymmetry that favours S is inherited along with the statistic.
- It cannot speak about any environment profile, contact profile, trajectory, or probe
  other than the ones §4 fixes.
- It cannot speak about any mass other than the seven of §6, and it fits no curve
  through them.
- It cannot, by itself, choose A2's option. It supplies the measurement each option
  currently assumes; the choice remains a joint decision made after the read.
