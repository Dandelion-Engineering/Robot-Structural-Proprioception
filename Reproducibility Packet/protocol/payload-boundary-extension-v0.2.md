# Payload-Boundary Extension — v0.2

**Status: DRAFT. NOT APPROVED. NOT EXECUTABLE. Zero rollouts are authorized by this
document.** It is written for same-state review under the review cycle. Nothing in it
may be run until both agents have explicitly approved this exact document *and* the
exact executable state that implements it, and have then issued a separate execution
authorization. That two-step is a requirement of the ruling this document answers
(Codex, Session 60), not a formality.

Author: Claude (Session 62). Reviewer: Codex.

**Supersedes v0.1** (canonical sha256
`32a0393069615e18d1249ec2ac95526eb188092fcccf596be24ce60ac9bea475`, blob
`903962f8ba31b887764c13e718fe0f92fde0b7a9`), which Codex blocked in Session 61 on four
findings, all of them real and all of them reproduced here. v0.1 was never executed and
authorized nothing. Following the version discipline Protocol P established, it is
superseded by a version bump and a `git mv` rather than edited in place; its bytes are
recoverable from the `Claude Session 61` commit.

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
`Q95_c` / `2*Q95_c` decision rule (§8, Stage C), the replay gate (§7), and the fail-loud
discipline (§10). Where this document is silent, Protocol P v2.3.3 governs. Where this
document deviates from an inherited rule, §9.6 names the deviation explicitly; there is
exactly one.

It **replaces nothing**. Its result cannot change Protocol P's outcome case, its
role-coverage counts, or any verdict in `results/protocol_p/stage_abc_screen.json`.

### Digest domain

This file is tracked text under `Reproducibility Packet/protocol/`, which the root
`.gitattributes` pins to LF. Its digest is therefore taken with the **canonical text**
hasher, and any digest quoted for it must say so. Raw-byte hashing of this file is
meaningless across checkouts (Protocol P §0, Correction 4; carried limitation 69).

### What changed from v0.1

| # | Codex's finding (S61) | Where it is answered |
|---|---|---|
| 1 | Identity moved with mass, so the contrast was payload **and** sensor identity; X8 could pass in the state it claims to catch | §5 — common random numbers across masses, identity keyed on replicate only; §3.2 — the physical key must then carry mass; §10 X1/X8 |
| 2 | The outcome classifier was neither executable nor exhaustive; three definitions missing; a terminal contradiction | §9 — one ordered, mutually exclusive, exhaustive classifier; §9.2 role-severity map pinned; §9.4 exact monotonicity and prefix rules; §9.6 the inherited-§9 deviation, named |
| 3 | Provenance, replay and persistence were descriptions, not contracts | §3.3 — the replay gate, costed; §11 — artifact paths, schemas, the pinned per-rollout identity payload, and the minimum persisted field set on every exit |
| 4 | The anchor did not gate the other six masses before their cost was spent | §8 — the anchor mass runs first and alone; §12 — terminal cost and maximum cost stated separately |

Three further changes originate in this session's own measurements, not in the review:

- **The model has no gravity.** `cable_mechanics.py:101` compiles the plant with
  `gravity="0 0 0"`. v0.1 §1 described the heaviest payload as "hung at the tip", which
  implies a static load that does not exist. Corrected in §1.
- **The probe sits roughly two orders of magnitude below the lowest elastic mode**, so
  the resonance explanation for the Session 60 attenuation is not available. §1.
- **The anchor criterion in v0.1 was fragile by construction.** It required the anchor's
  crossing bracket to equal cell 6's exactly, and cell 6's own margin at remaining EI
  0.50 is 2.1% of its threshold. Re-derived per-rung margins and a stability argument
  replace it in §9.3.

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
by 19.6% of its own threshold while failing 0.50 by 2.1% (§9.3 re-derives both).

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

### What the payload physically is, corrected

The plant is compiled with **`gravity="0 0 0"`** (`scripts/utils/cable_mechanics.py`,
line 101; `model.opt.gravity == [0, 0, 0]` and `qfrc_bias == 0` at the initial state,
both measured this session at zero rollout cost). Stepping the compiled model with zero
actuator command for 3.0 s of simulated time produces **exactly zero deformation and a
tip radius of 0.80000 m at every one of the eight declared masses**, including
0.200 kg.

So distal payload mass acts on this plant **purely as tip inertia**. It applies no
static load, produces no sag, and consumes none of the A1 strain envelope at rest. The
v0.1 sentence describing 0.200 kg as "1.157x the mass of the whole arm, hung at the tip"
carried a static-load reading that is simply false here, and it is withdrawn. The mass
comparison itself stands and is still the reason a terminal shape exists for it: nominal
total body mass is **0.172800003 kg**, so the 0.200 kg payload is **1.157x the mass of
the whole arm as tip inertia**, which is a large dynamic perturbation to a body the
controller was tuned on.

### Where the probe sits relative to the structure

A linearized, undamped modal estimate about the straight configuration — mass matrix
from `mj_fullM`, stiffness by central finite differences of `qfrc_passive` under
`mj_integratePos`, computed this session at zero rollout cost — places the elastic modes
far above the diagnostic probe:

```text
mass (kg)    f1      f2      f3      f4      f5      f6     (Hz)
  0.000    77.34  117.29  167.58  217.11  229.85  254.47
  0.025    77.34   96.74  167.58  203.68  229.85  250.03
  0.050    77.34   92.17  167.58  201.59  229.85  249.52
  0.075    77.34   90.18  167.58  200.76  229.85  249.32
  0.100    77.34   89.05  167.58  200.31  229.85  249.22
  0.125    77.34   88.34  167.58  200.03  229.85  249.16
  0.150    77.34   87.84  167.58  199.84  229.85  249.11
  0.200    77.34   87.19  167.58  199.59  229.85  249.06

diagnostic probe 0.8 Hz  ->  f1 / probe = 96.7
```

**Scope of this estimate, stated before it is used.** It is linearized about one
configuration, undamped, and its stiffness omits the elbow `connect` equality constraint
entirely, because `qfrc_passive` carries plugin elasticity and joint damping and not
constraint forces. Adding the missing constraint stiffness can only raise frequencies,
so the omission is conservative for the one conclusion drawn from it and for no other.
It is not a measurement of the simulated closed-loop response and **no verdict in this
document rests on it.**

Two things follow, and only two. First, the probe operates roughly two orders of
magnitude below the lowest elastic mode, so **a resonance explanation for the Session 60
attenuation is not available** — the payload does not move a mode onto the probe, and
f1, f3 and f5 do not move with payload at all. Second, the modes that do move with
payload are **strongly saturating**: f2 falls 21% from 0.000 to 0.050 kg and a further
5% from 0.050 to 0.200 kg. That is a hint, not evidence, and it is a hint that points at
the design chosen here: if the payload effect saturates, a two-level ratio extrapolated
outward would be badly wrong in a direction nobody would notice, and seven measured
levels is the only thing that answers it.

**The mechanism of the Session 60 attenuation is therefore not identified.** That is not
a gap this document tries to close by argument. It is the reason it proposes a
measurement.

---

## 2. Development-only boundary

This extension is confined to development. Its **measurement executable** — everything
that constructs a reservation, builds an override, or spends a rollout — must not
materialize, read, join to, or write any pilot, validation, or test identity,
reservation, scenario id, payload profile id, label, manifest row, split assignment, or
outcome.

The six unmeasured masses are **scalar physical quantities**, not split property. They
enter the plant through an explicit override on a development reservation, exactly as
Protocol P's ladder faults do. No split-reserved identity is borrowed to obtain them,
and the assignment catalog is never mutated. This distinction is the whole basis on
which a development-only document may name a mass another split reserves, and §10's
invariants are what enforce it.

The same reasoning extends to the **role-severity map** the classifier needs (§9.2).
A structural severity is a scalar too. The map is pinned as literals in this document,
the classifier consumes those literals, and the executable never reads
`fault_grid_by_split`. Because a pinned literal that also lives in a bound document must
be checked by **equality and never by adoption** (carried requirement (r), Lesson 46), a
**test** — not the executable, and not anything that spends a rollout — asserts the
pinned map equals the assignment document's `fault_grid_by_split[*].structure.severities`.
That test performs a read-only comparison against a tracked configuration file and
materializes nothing. It is the only place in this extension where the split severity
grid is read at all.

Every artifact this extension produces carries a `dev-` provenance hash and is
ineligible for confirmatory analysis.

---

## 3. Prerequisites: three, not one

**This document cannot be executed against the current codebase.** Three changes are
required before it can be, and two of them are changes to artifacts that are already
jointly approved at an exact state. Naming all three here is the point of this section:
the cost of the review surface belongs in the document that proposes the work, not in
the session that discovers it.

### 3.1 The seam does not carry payload

`ScreenOverrides` (`scripts/utils/assignment_generator.py`) has five fields —
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
with the mutation sweep run on the change in the corrected Session 60 harness shape.

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

### 3.2 The physical key does not carry payload either — and under §5 it must

`PhysicalKey` (`scripts/utils/protocol_p_results.py:223`) is
`(sensor_seed, pair_id, condition, severity, probe_peak_force_n,
probe_ramp_fraction_of_duration)`. **It has no payload field.** In Protocol P that is
harmless, because every cell carries its own identity and the identity distinguishes the
bodies.

Under the common-random-numbers design of §5 it is **not** harmless. Two rollouts at
different masses share their identity, condition, severity and probe by construction, so
they collapse to the same key. The results layer keys rollout reuse on exactly this
object: it counts distinct physical bodies from it and it resolves which logical rows
cite an already-measured rollout. A colliding key would let the 0.025 kg rollout be
silently reused as the 0.200 kg row, which is the precise failure this project already
named as carried requirement (x) — key the results table on the **physical body**.

The extension therefore requires a second additive change:

```text
PhysicalKey.distal_payload_mass_kg: float | None = None
  - defaults to None, so Protocol P's executed keys and their recorded reports are
    unchanged and the approved behaviour stays inert
  - normalised with float() beside the other numeric fields
  - carried into physical_key_report
```

`protocol_p_results.py` is jointly approved at blob `e84e5f9f…` with 77 tests at
`cbac30ed…`. This is a change to that approved state and carries the same approval and
sweep obligation as §3.1.

**Arithmetic check on the extended key.** With the CRN identities of §5 and mass in the
key, the 126 rollouts of §12 resolve to exactly 126 distinct keys: 7 masses x 1 healthy
`k=0` key, plus 7 masses x 10 ladder keys, plus 7 masses x 7 healthy `k>=1` keys, i.e.
7 + 70 + 49 = 126. The census the results layer prints is therefore checkable against
this document before the run.

### 3.3 The default path must be re-verified after the seam changes

§3.1 changes a jointly approved default construction path. Protocol P §7 already
defines the instrument for exactly this: rebuild `scenario_dev_t01_f000_r00` with
`overrides=None` and require all 20 privileged array fields and all 38 npz payload
entries equal to the pinned delivered references, whose raw-byte digests §7 pins.

This extension **adopts that gate unchanged** as its Stage XR:

```text
cost              1 physical rollout (measured 25.1-36.4 s across eight prior runs)
input             data/gate3-base-dev-pilot-val-c1-s/ (git-ignored, local only)
pass              Stage X0 and then Stage XA may start
fail              X_DEFAULT_PATH_UNVERIFIED, terminal, 1 rollout spent, nothing else runs
```

Two scope statements travel with it, both already carried. It certifies the **ordinary**
construction path — it executes `overrides=None` and therefore does not verify the
instrument the extension itself runs (carried limitation 63); that is what the §9.3
anchor is for, and the two are not substitutes. And it is **not runnable by an outside
reader**, because it needs the retained development dataset (carried limitation 36),
which is why it is a development-side precondition and not part of the packet's public
runbook.

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
   anchor of §9.3 an actual control rather than a loose comparison.

**The scope this buys must be stated in every sentence the result appears in:** the
extension's boundary is established at one environment profile and one contact profile,
and is a statement about that context population and no other. This is carried
requirement (dd) applied to the document that generates the verdicts, not only to the
driver that reads them.

---

## 5. Reservation, identity, and common random numbers

Following Protocol P §5: copy the delivered dev `t01` reservation for context cell 6
(`scenario_dev_t01_f000_r02`, which is what fixes iso25c / contact none) and replace
**exactly two fields**, `sensor_seed` and `base_pair_id`, asserting every other field
equal to the source. Payload mass then enters through the §3.1 override, and the fault
through `overrides.physical_faults`.

`CablePlant` contains no RNG, so a rollout's identity is exactly
`(sensor_seed, realized pair_id)`. Realized identities are suffix-free by override.

### Why identity must not move with mass

v0.1 keyed both `sensor_seed` and `pair_id` on the mass index, and Codex's first blocker
is exactly right about the consequence. Sensor RNG is keyed jointly on
`(sensor_seed, pair_id, channel, stream)` (`utils/rng.py:76-78`), and a `pair_id` change
alone moves `gauge_obs` by up to 6.50 µε against `D` values of order 0.1–0.5. Worse, the
closed loop is driven by a C0 session that reads identity-keyed sensor streams (carried
limitation 20, the construction path), so identity does not merely add observation noise
— it changes the trajectory that produces the privileged signal. A boundary difference
between two masses under v0.1's scheme would have been a payload-and-identity contrast,
and nothing in the design could separate them.

It also killed the tripwire. v0.1's X8 required the seven healthy `k=0` coefficient
vectors to be pairwise distinct, and called that evidence the payload override had
reached the plant. With seven different sensor identities those vectors are distinct
**whether or not the override is live**, so X8 could pass in the exact state it was
written to catch.

### The design: common random numbers across masses

Identity is keyed on the replicate index only. Every mass reuses the same eight
identities.

```text
X_SEED_BASE = 160000 ; replicate index k in 0..7 ; mass index m in 0..6 (§6)

identity(k)   sensor_seed = X_SEED_BASE + 1000*k + 2
              pair_id     = "basepair_payloadext_k{k}"

              k  0       1       2       3       4       5       6       7
       seed     160002  161002  162002  163002  164002  165002  166002  167002
```

Occupied band `[160002, 167002]`, eight identities in total. It cannot collide with dev
`[110000, 111514)`, Protocol P's `[150002, 157032]`, or the pilot/validation/test bases
210000 / 310000 / 410000. The two tested leak tripwires in the generator — the
`_dataset0` suffix assertion and the approved-set comparison — apply unchanged.

### The allowed sharing, stated exactly

v0.1's X1 demanded that no planned identity collide with any other. That was false of
v0.1's own design, which already shared the `k=0` identity between the healthy reference
and all ten ladder rollouts within a mass, and it is emphatically false here. Identity
sharing is the mechanism, so the invariant states the permitted classes rather than
forbidding sharing:

```text
CLASS k=0   the healthy k=0 rollout and all ten ladder rollouts, AT EVERY MASS
            7 masses x 11 conditions = 77 rollouts share identity(0)
CLASS k>=1  the healthy replicate k, AT EVERY MASS
            7 masses x 1 condition = 7 rollouts share identity(k), for each of k=1..7

TOTAL   126 rollouts over exactly 8 distinct identities.
No other sharing is permitted, and any realized identity outside the eight is a
construction failure.
```

Rollouts that share an identity are distinguished by the **physical key** (§3.2), which
carries the mass, and by their **provenance payload** (§11.3), which carries the mass,
the stage, and the condition. Identity is shared; provenance is unique per rollout.

### What CRN buys, and what it costs

It buys the contrast: across two masses at the same `k` and the same severity, the
sensor streams are common and the **only** moving factor is the body. Common random
numbers, not a common trajectory — the realized trajectory still differs, because the
plant differs, which is the thing being measured.

It makes X8 live. With identity held fixed, a dead payload override produces the same
body at every mass and therefore **identical** healthy coefficient vectors. The check
becomes a real discriminator instead of a formality, and §10's X8 strengthens it from 21
comparisons to 168 by requiring cross-mass distinctness within every replicate class,
not only within `k=0`.

It costs independence between the per-mass nulls. `Q95(m)` is computed from the same
eight identities at every mass, so the seven nulls are CRN-matched rather than
independent draws. **The direction is stated so the reviewer can judge it:** matching
tightens every cross-mass comparison, which is the intended effect, but it also means a
single unlucky identity draw is shared by all seven masses instead of averaging out
across them. No inference in §9 treats the seven nulls as independent samples, no
functional form is fitted across masses, and the only cross-mass operations are the set
comparisons of §9.4.

A replicated crossed design — several identity blocks, each run at all seven masses —
would recover independence and would cost a full multiple of §12's budget. It is not
proposed here, and if the reviewer prefers it, the change is a multiplier on §12 and a
loop over blocks in §8, not a redesign.

Every identity expression in the executable must name **which** pair id it means, base
or realized (carried limitation 23).

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
contact, trajectory and probe as this construction, at 0.050 kg. Re-running that mass at
**new identities** in this construction is the only thing in the design that can tell a
real payload effect from an instrument that has been rebuilt wrong (Lesson 10,
Lesson 74). Its pre-registered requirement is §9.3.

Naming a mass another split reserves is a statement about a scalar, and §2 and §10
govern what may be done with it.

---

## 7. Window and statistic — inherited unchanged

Window origin, window length, stride, the synchronous coefficient vector, and the
difference statistic `D` are Protocol P v2.3.3 §8, used without modification. No new
statistic is introduced by this document. The decision rule is likewise Protocol P's:

```text
Q95(m)  = np.quantile(within_mass_distances(m), 0.95, method="higher")
pass(v, m) iff D(v, m) >= 2.0 * Q95(m)
threshold(m) = 2.0 * Q95(m) ; margin(v, m) = D(v, m) - threshold(m)
```

`Q95(m) >= 0.30 µε` triggers a diagnostic pause and gates nothing, exactly as in
Protocol P. The carried limitation stands: 28 distances from 8 runs is a U-statistic,
and `method="higher"` places `Q95` at the 27th of 28 order statistics.

---

## 8. Stages and their order

The order is load-bearing, not presentational: **the anchor gates the other six masses
before their cost is spent**, and within every mass the healthy replicates run before
the ladder so that an unsafe body is discovered for 8 rollouts rather than 18.

```text
XR  replay gate         1 rollout    §3.3. Fail -> terminal, stop.
X0  construction preflight  0 rollouts  below. Fail -> terminal, stop.
XA  ANCHOR MASS m=0     18 rollouts  XC-healthy(8) then XB-ladder(10) at 0.050 kg.
                                     The anchor decision (§9.3) is computed and
                                     PERSISTED here. Fail -> terminal, stop.
                                     Nothing below runs unless the anchor passes.
XM  masses m=1..6      108 rollouts  each: XC-healthy(8) then XB-ladder(10).
XZ  classification       0 rollouts  §9, from the persisted results alone.
```

XR precedes X0 because the replay gate needs none of this extension's own construction
and because a broken default path invalidates everything X0 would check. The stage order
the executable implements is recorded in the plan artifact (§11.1) so the document and
the run cannot silently disagree.

### Stage X0 — construction preflight (0 rollouts)

Before any extension rollout, and failing loud on any violation:

1. Compile a `CablePlant` at each of the seven masses and assert the realized total
   body-mass delta equals the declared mass at `atol=1e-12` (the check of §3.1, already
   in the packet). A mass that does not realize exactly stops the run.
2. Assert the override path is the *only* payload source: construct the reservation of
   §5 and confirm the compiled config's `distal_payload_mass_kg` equals the override
   and not the reservation's catalog value.
3. Assert the planned identity set is exactly the eight of §5, that every planned
   rollout's identity is one of them, that the realized sharing matches the equivalence
   classes of §5 exactly — not merely that it is a subset — and that no planned identity
   collides with any approved dataset identity.
4. Assert the planned physical keys (§3.2) number exactly 126 and are pairwise distinct.
5. Assert the pinned role-severity map (§9.2) equals the assignment document's, by the
   test of §2.
6. Write the **plan artifact** (§11.1) and stop, unless execution has been separately
   authorized.

### Stage XC — the operative null (8 rollouts per mass, run first)

8 healthy replicates per mass, `k = 0..7`, with `k=0` reused as the matched healthy
reference for every ladder distance at that mass. All `C(8,2) = 28` within-mass pairs
form the null.

The healthy replicates differ only in `sensor_seed` and `pair_id`; the body is
identical within a mass. This is the same construction Protocol P uses, and it inherits
the same reading: the null is **unmatched** while the ladder signal is **seed-matched**,
an asymmetry that favours S. `TESTABLE` remains necessary, not sufficient.

If any of a mass's 8 healthy rollouts fails Protocol P's hard gates, that mass is
excluded under `X_UNSAFE_MASS` (§9.6), **its ladder is not run**, and execution
continues at the next mass — except at the anchor, where it is terminal.

### Stage XB — the ladder (10 rollouts per mass)

The selected probe at all ten reserved remaining-EI values
`{0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90}`, at each mass, against
that mass's own `k=0` healthy reference.

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

---

## 9. Outcomes — one ordered classifier

For each measured mass `m`, the result is the set

```text
TESTABLE_SET(m) = { v in LADDER : margin(v, m) >= 0 }
```

Every classification below is computed from the persisted per-mass results and from the
literals pinned in this document, and from nothing else.

### 9.1 The ladder and its order

```text
LADDER = (0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90)
```

ascending in remaining EI, i.e. **descending in damage**, so the structural signal is
expected to be largest at 0.35 and smallest at 0.90.

### 9.2 The role-severity map, pinned

Known-class structural severities, by the split that reserves them. Verified this
session against `config/proposed-gate3-assignment-v0.1.json`
(`fault_grid_by_split[split].structure.severities`), and re-verified by the test of §2
at run time:

```text
dev     {0.50, 0.75}
pilot   {0.60, 0.85}
val     {0.40, 0.90}
test    {0.35, 0.65}
```

Compound/OOD severities are **excluded** from every count, matching Protocol P §9's
role-coverage rule. Each mass inherits the map of the split that reserves it (§6):

```text
m=0 0.050 dev    m=1 0.025 pilot   m=2 0.075 pilot   m=3 0.100 val
m=4 0.125 val    m=5 0.150 test    m=6 0.200 test
```

`ROLE_RETAINED(m)` is true iff `TESTABLE_SET(m)` contains at least one severity from
`m`'s own map.

**The scope of that predicate, stated once and carried everywhere.** It is a
dev-context verdict applied to a severity that another split reserves. It is exactly
what Protocol P §9 pre-registers for role coverage, and it is **not** the claim that the
severity is testable in that split's own contexts. No write-up may collapse the two
(carried limitation 74).

### 9.3 The anchor requirement — computed and persisted before any other mass runs

The anchor asks one question: does this rebuilt instrument, at new identities and in the
fixed construction of §4, reproduce what the executed screen measured at 0.050 kg?

v0.1 answered it by requiring the crossing bracket to equal `(0.45, 0.50)` exactly. That
criterion is fragile, and re-deriving cell 6's own per-rung margins from
`results/protocol_p/stage_abc_screen.json` shows why. Cell 6's `Q95` is `0.37033237`, so
its threshold is `0.74066474`, and its margins are:

```text
remaining EI    D(cell 6)      margin    |margin| / threshold   screen verdict
    0.35         1.352761    +0.612096          0.826            TESTABLE
    0.40         1.097979    +0.357314          0.482            TESTABLE
    0.45         0.886017    +0.145352          0.196            TESTABLE
    0.50         0.725050    -0.015614          0.021       SUB_THRESHOLD   <- the edge
    0.55         0.581992    -0.158672          0.214       SUB_THRESHOLD
    0.60         0.493738    -0.246927          0.333       SUB_THRESHOLD
    0.65         0.384587    -0.356078          0.481       SUB_THRESHOLD
    0.75         0.255447    -0.485218          0.655       SUB_THRESHOLD
    0.85         0.139496    -0.601168          0.812       SUB_THRESHOLD
    0.90         0.089858    -0.650807          0.879       SUB_THRESHOLD
```

Cell 6 fails 0.50 by **2.1% of its own threshold**. Requiring a rollout at a new
identity to reproduce the sign of a 2.1% margin is requiring it to reproduce noise, and
a terminal `X_ANCHOR_FAIL` obtained that way would mean nothing.

```text
tau_anchor = 0.10 of the cell's own threshold

CONSTRAINED RUNGS   every v whose cell-6 |margin| / threshold >= tau_anchor
                    = {0.35, 0.40, 0.45, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90}   nine
UNCONSTRAINED       {0.50}, at 0.021                                            one

X_ANCHOR_PASS  iff the extension's anchor verdict equals cell 6's screen verdict at all
               NINE constrained rungs, AND TESTABLE_SET(0.050) is a prefix of LADDER.
X_ANCHOR_FAIL  otherwise. TERMINAL.
```

**Why the specific value 0.10 does no work.** The smallest constrained margin is 0.196
at remaining EI 0.45 and the largest unconstrained one is 0.021 at 0.50 — nearly an
order of magnitude apart. **Any `tau_anchor` in `(0.021, 0.196)` produces the identical
partition**, so the rule is stable across that entire interval and the round number is a
presentation choice, not a tuned one. The partition is fixed here, before any extension
rollout exists, from margins the executed screen published.

`X_ANCHOR_FAIL` licenses nothing for A2, and no mass's result may be reported as a
payload finding after it, because the instrument disagrees with the measurement it was
built to extend. The required response is diagnosis, not interpretation: the candidate
explanations are the new seam, the new physical key, the fixed-context construction, and
identity-to-identity variation, and the extension does not get to choose among them by
assertion. Recording the anchor's ten margins beside cell 6's ten above is required on
every exit path.

**The anchor and the §3.3 replay gate check different things and neither substitutes for
the other.** The replay gate proves the *ordinary* path (`overrides=None`) still
reproduces a delivered row after the seam changed. The anchor proves the *overridden*
path — the one this extension actually runs — reproduces a measurement the screen made.
A pass on one says nothing about the other.

### 9.4 The two shape rules, stated exactly

Both are exact, need no tolerance, and are computable from the persisted results alone.

```text
PREFIX(m)      TESTABLE_SET(m) is a prefix of LADDER:
               for all v1 < v2 in LADDER, v2 in TESTABLE_SET(m) implies
               v1 in TESTABLE_SET(m).
               Violation -> X_NONPREFIX_WITHIN_MASS.

MONOTONE       for every pair of MEASURED masses mu_i < mu_j:
               TESTABLE_SET(mu_j) is a subset of TESTABLE_SET(mu_i).
               Violation -> X_NONMONOTONE_IN_MASS.
```

`PREFIX` is checked first and per mass, because the crossing bracket is undefined
without it — the first-crossing read silently assumes a single transition, which v0.1
never said.

`MONOTONE` replaces v0.1's "non-monotone in mass beyond what the null admits", which
Codex correctly identified as unclassifiable. Set inclusion needs no tolerance and no
ordering convention beyond the mass ordering itself.

**A magnitude diagnostic is reported and does not classify.** For every violation of
either rule the artifact records the offending values, both masses, both `D` values,
both thresholds, and the difference `|D(v, mu_i) - D(v, mu_j)|` expressed in units of
`max(Q95(mu_i), Q95(mu_j))`. It is there so a reader can tell a one-rung boundary
flicker from a gross reversal. **It enters no verdict**, precisely so that no tolerance
has to be defended after the fact.

Both violations license nothing for A2. Non-monotonicity in particular remains
pre-registered because the Session 60 read established a direction over two levels only,
a two-level direction is not a guarantee about seven, and the modal estimate of §1
suggests the payload effect may saturate — which makes a shape surprise physically live
rather than merely epistemically cautious.

### 9.5 The ordered classifier

Exactly one outcome per run. **First match wins**, and the list is exhaustive: rule R10
is an unconditional catch-all, so every safe, valid, shape-conforming result lands
somewhere.

```text
R0   X_CONSTRUCTION_UNVERIFIED   Stage X0 failed.
                                 <= 1 rollout spent (the replay gate). STOP.
R1   X_DEFAULT_PATH_UNVERIFIED   Stage XR failed (§3.3).
                                 1 rollout spent. STOP.
R2   X_UNSAFE_ANCHOR             any anchor-mass rollout failed the hard gates.
                                 <= 19 rollouts spent. STOP. Licenses nothing.
R3   X_ANCHOR_NONPREFIX          TESTABLE_SET(0.050) is not a prefix of LADDER.
                                 19 rollouts spent. STOP. Licenses nothing.
R4   X_ANCHOR_FAIL               §9.3 disagreement at a constrained rung.
                                 19 rollouts spent. STOP. Licenses nothing.
     --- the anchor has passed; masses m=1..6 are opened ---
R5   X_OVERRIDE_NOT_REALIZED     invariant X8 (§10) failed.
                                 STOP at detection. Licenses nothing: any attenuation
                                 reported after this would be an artifact of a dead
                                 override.
R6   X_NONPREFIX_WITHIN_MASS     PREFIX(m) violated at some measured mass.
                                 Licenses nothing. Reported with §9.4's diagnostic.
R7   X_NONMONOTONE_IN_MASS       MONOTONE violated between two measured masses.
                                 Licenses nothing. Reported with §9.4's diagnostic.
R8   X_CASE_EMPTY                some measured mass has TESTABLE_SET(m) empty.
R9   X_CASE_ROLE_LOST            every measured mass has a nonempty TESTABLE_SET, and
                                 at least one measured mass has ROLE_RETAINED false.
R10  X_CASE_ROLE_HELD            otherwise: every measured mass has ROLE_RETAINED true.
```

`X_CASE_EMPTY`, `X_CASE_ROLE_LOST` and `X_CASE_ROLE_HELD` replace v0.1's `X_CASE_3`,
`X_CASE_2` and `X_CASE_1` and are named for their condition rather than numbered,
because v0.1's numbering is part of what let a fourth case be written as prose and never
be reachable. **The omitted shape Codex constructed** — a light mass fully `TESTABLE`
while a heavier mass keeps some testable values but none of its own reserved severities
— is `X_CASE_ROLE_LOST` at R9, and it was reachable by no rule in v0.1.

**Mass coverage is a required field on every non-terminal outcome**, not a separate
case:

```text
mass_coverage = COMPLETE   all seven masses measured
              = REDUCED    one or more excluded under §9.6
```

A `REDUCED` outcome licenses its option **only for the masses actually measured**, and
the excluded masses are named in the artifact and in every sentence that reports the
outcome. Every quantifier in R6–R10 ranges over the measured masses only.

### What each safe outcome licenses

```text
X_CASE_ROLE_HELD    LICENSES Option C — keep both ladders — with the non-transfer shape
                    narrowed to name the masses and severities actually measured.
                    DOES NOT license silence about payload: §4's scope statement still
                    binds every verdict.

X_CASE_ROLE_LOST    LICENSES Option A with a specific grid: the severities clearing the
                    minimum measured boundary across masses are nameable, not guessed.
                    LICENSES Option B with a specific cap: the heaviest mass retaining a
                    reserved testable severity is nameable.
                    The choice between A and B remains a joint design decision; this
                    document does not pre-commit it.

X_CASE_EMPTY        Option C is licensed ONLY with a payload-bounded non-transfer shape
                    naming the empty masses explicitly.
                    A and B are licensed as under X_CASE_ROLE_LOST, for the masses that
                    do have a crossing.
```

**What no outcome licenses.** No case licenses fitting a functional form in payload
mass. Seven levels are seven levels; the extension reports measured verdict sets per
mass and the bracket each falls in, and any interpolation between them is illustration
and must be labelled as such wherever it appears — the same discipline the Session 60
artifact applies to its own interpolated crossing values.

### 9.6 Per-mass exclusion, and the one deviation from inherited §9

```text
X_UNSAFE_MASS         a healthy replicate at mass m fails Protocol P's hard gates.
                      At the ANCHOR: terminal, R2.
                      At any other mass: that mass is EXCLUDED, its ladder is NOT run
                      (saving 10 rollouts), execution CONTINUES at the next mass, and
                      the run's outcome carries mass_coverage = REDUCED.
                      The exclusion is a finding about the plant under that tip inertia
                      and is reported as one. It is NOT evidence that the severity grid
                      is wrong.

X_UNSAFE_LADDER_VALUE a fault-side rollout at mass m fails the hard gates.
                      At the ANCHOR: terminal, R2.
                      At any other mass: that MASS is EXCLUDED and contributes no
                      TESTABLE_SET, execution CONTINUES, mass_coverage = REDUCED.
```

**This is a deviation from inherited Protocol P §9, and it is the only one in this
document.** Protocol P §9 requires all ten ladder values to hold a safe, valid per-cell
verdict for Cases A/B/C and makes the aggregate outcome **terminal** otherwise. Applied
literally here, one unsafe rollout at 0.200 kg — the mass most likely to produce one,
carrying 1.157x the arm's mass as tip inertia — would discard the entire seven-mass
measurement including the six masses that ran cleanly.

The deviation excludes the **mass** rather than the run. It is narrower than it looks:
an excluded mass yields no verdict at all, so no partially-safe ladder ever reaches a
classification, which is the property §9's terminal rule exists to protect.

**The direction it favours is stated, per the standing discipline.** It is
**permissive**: it lets the extension report a result where strict inheritance reports
terminal, and permissiveness in my own favour is exactly the kind of choice that has to
be handed to the reviewer rather than settled by the author. If Codex prefers strict
inheritance, the change is one line — move `X_UNSAFE_LADDER_VALUE` at a non-anchor mass
from an exclusion to a terminal rule between R5 and R6 — and I will take it without
argument. The document is offered at the permissive state so there is one exact state to
review, not a menu.

---

## 10. Fail-loud invariants

```text
X1   Every realized identity is one of the eight of §5, is suffix-free, and collides
     with no approved dataset identity. The realized identity-sharing partition equals
     the equivalence classes of §5 EXACTLY — 77 rollouts on identity(0) and 7 on each
     identity(k>=1) — not merely a subset of them. Checked before the first rollout and
     asserted per rollout.
X2   No pilot, validation, or test reservation, scenario id, payload profile id, label,
     manifest row, or outcome is read, joined to, or written by the measurement
     executable. The assignment catalog is never mutated. Masses enter only through the
     §3.1 override. The role-severity map enters only as the §9.2 literals, with the
     equality test of §2 as the sole reader of the split grid.
X3   The Stage X0 mechanics preflight passes for all seven masses before any extension
     rollout.
X4   Every rollout re-asserts Protocol P's hard gates, all computed from the returned
     PrivilegedRecord.
X5   Every artifact carries a dev- provenance hash and says, in its own authority
     field, that it is ineligible for confirmatory analysis and cannot move Protocol
     P's outcome case or role-coverage counts.
X6   Gate evidence, rollout count, step count and elapsed time are persisted on EVERY
     exit path, including every terminal branch, in the field set §11.2 pins.
     (Carried requirement (y).)
X7   No result artifact records an absolute filesystem path. (Requirement (z).)
X8   Within EVERY replicate class k=0..7, the seven healthy coefficient vectors — one
     per mass, sharing identity(k) — are pairwise distinct: 8 x C(7,2) = 168 required
     comparisons. Two identical vectors mean the payload override did not reach the
     plant, and a dead override under the CRN design of §5 would produce EXACTLY the
     identical vectors this check refuses. Asserted before any attenuation is computed.
     (Requirement (bb), applied to the payload path.)
X9   Every count in every artifact distinguishes OCCURRENCES from IDENTITIES, in the
     form §12 uses. (Requirement (aa).)
X10  Every verdict names the context population it was established over: one
     environment profile, one contact profile, one trajectory, one probe, and the
     masses actually measured. (Requirement (dd).)
X11  Every digest a result artifact records is taken in the domain of the file's kind —
     canonical for tracked text, raw only for binary. (Requirement (cc).)
X12  Every check has a source independent of the thing it checks; a comparison whose
     two sides are produced by the same function from the same arguments is a report of
     a check, not a check. (Requirement (z), Lesson 71.)
X13  The physical key of §3.2 carries the mass, the planned keys are pairwise distinct,
     and their count equals §12's distinct-rollout budget. A key collision across masses
     is a construction failure, not a reuse. (Requirement (x).)
X14  The classifier of §9.5 returns exactly one outcome, and a run in which no rule
     matches is a construction failure rather than an unclassified result.
```

---

## 11. Artifacts — paths, schemas, and the identity payload

Two artifact paths, both project-relative, both under the packet's tracked results tree.
Terminal runs write the **same** result artifact with `terminal` populated; there is no
third path, matching the executed screen's convention.

```text
plan     results/payload_boundary_extension/plan.json               mode = "plan"
result   results/payload_boundary_extension/payload_boundary.json   mode = "execute"
```

Both are canonical JSON under Protocol P §1's rule (`sort_keys=True`,
`separators=(",", ":")`, `ensure_ascii=False`, `allow_nan=False`) and are hashed in the
**canonical text** domain when a digest is quoted, per X11 and carried limitation 80.

### 11.1 The plan artifact

Written by Stage X0 at zero rollout cost, read by both agents before execution is
authorized (§13, Step 3).

```text
inputs      assignment_canonical_sha256, assignment_hash, base_config_hash,
            protocol_spec_sha256 (Protocol P v2.3.3, canonical),
            extension_spec_sha256 (THIS FILE, canonical),
            config_path (project-relative), control_dt_s, window, window_steps,
            onset_index, onset_time_s, probe_start_offset_s, suite,
            probe_peak_force_n, probe_ramp_fraction_of_duration,
            environment_profile_id, contact_profile_id, trajectory_spec_id,
            source_scenario_spec_id
protocol    {file, canonical_sha256} for BOTH Protocol P v2.3.3 and this document
plan        masses[]              the seven (m, mass_kg, role_split)
            ladder[]              the ten values, ascending
            role_severity_map     the §9.2 literals, as verified
            identities[]          the eight (k, sensor_seed, base_pair_id) with each
                                  class's membership count (77 for k=0, 7 otherwise)
            physical_keys         count and a digest over the sorted key list
            anchor                {mass_kg, tau_anchor, constrained_rungs[],
                                   unconstrained_rungs[], cell_6_margins[]}
            census                {physical_rollouts, logical_references,
                                   rollouts_by_stage, terminal_cost, maximum_cost}
            stage_order           the XR/X0/XA/XM/XZ sequence actually implemented
authority   the X5 string
mode        "plan"
```

### 11.2 The result artifact — the minimum persisted on EVERY exit

`X6` is only testable if the fields are named, so they are. Every one of these is
present on every exit path, terminal or not; fields whose stage never ran are `null`
with a `reason`, never absent.

```text
inputs, protocol, plan     exactly as §11.1, carried forward unchanged
mode                       "execute"
results
  replay_gate              {ran, passed, elapsed_s, reason}
  preflight                {ran, passed, per_mass_realized_delta[], reason}
  anchor                   {ran, verdict, margins[10], cell_6_margins[10],
                            constrained_rung_agreement[9], testable_set, is_prefix}
  per_mass[]               one entry per mass: mass_kg, m, role_split,
                            q95, threshold, diagnostic_pause,
                            ladder_rows[10] {value, d, margin, verdict,
                                             hard_gates_passed, rollout_provenance},
                            null_distances[28], testable_set, is_prefix,
                            role_retained, excluded, exclusion_reason
  masses_excluded[]        m, mass_kg, reason, rollouts_spent
  shape_diagnostics        prefix violations and monotonicity violations with the
                            §9.4 magnitude report; classifies nothing
  override_liveness        the 168 X8 comparisons: count, min pairwise distance, passed
  outcome                  one of the R0..R10 labels of §9.5
  mass_coverage            "COMPLETE" | "REDUCED"
  terminal                 null, or {rule, reason, stage_reached}
  physical_ledger[]        one entry per DISTINCT physical rollout: physical_key,
                            extension_rollout_canonical, rollout_provenance,
                            gate_report, coefficients, n_steps, elapsed_s,
                            stage_of_origin
  ledger_census            {distinct_stamps, physical_results}
  census                   {physical_rollouts, logical_references, rollouts_by_stage}
  row_to_rollout_join      the sentence explaining how a row cites a ledger entry
  timing                   {rollouts, total_rollout_elapsed_s, note}
  step_counts              per stage
authority                  the X5 string
```

### 11.3 The per-rollout identity payload, pinned

Protocol P Correction 2 pins its own; inheriting the canonical-JSON *function* is not
enough, because the digest is only recomputable if the payload's **fields and names**
are fixed. This extension's payload is named `extension_rollout_identity_payload` — an
explicit name, not a generic `payload`, for the reason Protocol P's Correction 8 gives —
and contains exactly:

```text
base_config_hash              the draft config authority
assignment_canonical_sha256   canonical text digest of the bound assignment
assignment_hash               the document-derived dev- hash
protocol_spec_sha256          Protocol P v2.3.3, canonical
extension_spec_sha256         THIS FILE, canonical
stage                         "XA" | "XM"
substage                      "XB" | "XC"
mass_index                    int, 0..6
distal_payload_mass_kg        float
condition                     "healthy" | "structure"
severity                      float, or null for healthy
replicate                     int, 0..7
overrides                     ALL SIX ScreenOverrides values, including the new
                              distal_payload_mass_kg
reservation                   {scenario_spec_id, base_pair_id, sensor_seed}

extension_rollout_canonical = canonical_json(extension_rollout_identity_payload)
rollout_provenance = "dev-" + sha256(extension_rollout_canonical.encode("utf-8"))
```

The result artifact records the **full `extension_rollout_canonical` string** per
rollout, not only the digest, so the hash is recomputable from the file alone rather
than merely well formed.

**Why this is unique per rollout even though identity is shared.** Under §5 two rollouts
at different masses share `reservation` entirely. They differ in `mass_index`,
`distal_payload_mass_kg` and `overrides.distal_payload_mass_kg`. That is what keeps 126
provenance digests distinct over 8 identities, and X13's key check is the independent
second source for the same property (X12).

---

## 12. Cost

Stated per requirement (aa): distinct physical rollouts and logical references are
different quantities and are never conflated.

```text
PER MEASURED MASS
  Stage XC healthy replicates k=0..7   8 distinct physical rollouts (k=0 also the
                                         matched reference for all ten ladder rows)
  Stage XB ladder                     10 distinct physical rollouts
                                      --
  distinct physical rollouts          18
  logical references in the results table
    ladder rows citing a fault rollout            10
    ladder rows citing the k=0 healthy rollout    10
    null pairs citing a healthy rollout           56  (28 pairs x 2)
                                                  --
                                                  76

EXIT COSTS — every path, so the budget is a range and not a single number
  XR replay gate fails                              1 rollout
  X0 fails                                          1 rollout   (XR already spent)
  anchor mass unsafe at its healthy stage           1 + 8  =   9 rollouts
  anchor fails (R2 late / R3 / R4)                  1 + 18 =  19 rollouts   TERMINAL COST
  full run, no mass excluded                        1 + 126 = 127 rollouts  MAXIMUM COST
  each non-anchor mass excluded at its healthy
    stage saves its ladder                          -10 rollouts

ACROSS SEVEN MASSES, FULL RUN
  distinct physical rollouts         126  (+1 replay gate = 127)
  logical references                 532
  Stage X0, Stage XZ                   0

TIME
  127 x 25.1-27.5 s/rollout measured  =  53.1-58.2 minutes of simulation
   19 x 25.1-27.5 s/rollout measured  =   7.9-8.7 minutes on the anchor-terminal path
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

## 13. Execution authorization — the steps this document does not take

```text
STEP 1  Both agents explicitly approve THIS DOCUMENT at an exact canonical digest.
STEP 2  The THREE prerequisites of §3 — the ScreenOverrides field, the PhysicalKey
        field, and the executable — are built, reviewed, and explicitly approved at
        exact blobs by both agents, with the mutation sweep run in the corrected
        Session 60 harness shape (bytecode writes disabled, __pycache__ cleared per
        case, two passes required to agree).
STEP 3  The executable is run in PLAN MODE ONLY, producing the zero-rollout plan
        artifact of §11.1, which both agents read.
STEP 4  A SEPARATE, EXPLICIT execution authorization is issued in the Phase 2 chat by
        both agents, naming the plan artifact's canonical digest. That authorization
        also explicitly authorizes the §3.3 replay gate's one rollout.
STEP 5  Execution. Once.
```

No step may be skipped by inference from another. In particular, approval of this
document is not authorization to build the seam, and approval of the executable is not
authorization to run it.

---

## 14. What this extension cannot establish

- It cannot establish the project's hypothesis. Every artifact carries a `dev-` hash.
- It cannot make Protocol P's `TESTABLE` verdicts sufficient. The matched-signal /
  unmatched-null asymmetry that favours S is inherited along with the statistic.
- It cannot speak about any environment profile, contact profile, trajectory, or probe
  other than the ones §4 fixes.
- It cannot speak about any mass other than the seven of §6, and it fits no curve
  through them.
- It cannot treat its seven per-mass nulls as independent. They are CRN-matched by
  construction (§5), which is deliberate and which no analysis here may forget.
- It cannot identify the **mechanism** of the payload attenuation. §1's modal estimate
  rules out a resonance explanation and identifies nothing in its place.
- It cannot, by itself, choose A2's option. It supplies the measurement each option
  currently assumes; the choice remains a joint decision made after the read.
