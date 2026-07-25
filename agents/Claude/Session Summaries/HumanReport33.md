# Human Report — Claude Session 33

**Current date and time:** 2026-07-24 18:31 PDT
**Phase:** Phase 2 — Execution (integration and pre-confirmatory build)
**Session role:** Exact-state review of Codex's Gate-2 generator and the first real generated dataset
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Session decision:** `APPROVE_GATE2_GENERATOR_BASE_ROLES` (no review-target edits) **plus** a new
self-imposed gate, `BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK`

---

## Summary

### What I was handed

Codex's Session 32 embedded our jointly approved Gate-3 assignment into the still-draft
configuration, built the real assignment-driven MuJoCo generator, and produced the project's
**first real research dataset** — 472 development/pilot/validation reservations, 944 manifest
rows across the matched C1 and S sensor suites, 3.7 GB on local disk (ignored by git). It asked
me to review the exact tracked state and the generated data and answer with an approval token or
an artifact-specific block.

I approved it. The implementation is correct and I could not break it where it counts. But the
more valuable part of the session was not the verdict — it was measuring, for the first time,
what the *physics* in that data actually contains. Two findings came back, and the first one
changes what I do next.

### The verdict on the artifact: approved

I deliberately did not audit through Codex's auditor. The whole point of an independent review is
to reach the same conclusion by a different route, so I re-derived all 472 authorized reservations
**from the assignment document's own written expansion rule**, never importing the code that
generates them, and diffed my derivation against the on-disk manifest row by row.

```text
derived from prose            472    (dev 152 / pilot 152 / val 168)
manifest rows on disk         944    (C1 472 / S 472)
scenario ids only in either     0 / 0
field mismatches, 9 fields      0    across all 944 rows
seeds 1888, collisions          0
pair_ids 472 unique; run_ids 944 unique
train_seed values            {0};   config_hash single value
test rows                       0
```

Leakage, measured on the delivered manifest rather than on the design: the mutual information
between the fault setting and the context cell — and between the fault and each of payload,
environment, and contact individually — is **0.0000000000 bits in all three splits**. No known
fault tuple is reused across any split pair. Suite masking is exact: I scanned all 472 C1
payloads and none leaks a single finite or valid strain-gauge sample. Temperature realizes its
prescribed profile analytically across all six environments. Every fault family leaves a
measurable physical trace — zero dead runs out of 396. The full packet suite passes 397 tests.

I also tried to break Codex's new approval wrapper, which is the subtlest piece of this handoff.
It correctly refused eight of nine tampering attempts I threw at it, and the generator refused
every request that included the test split.

### Finding 1 — the structural fault signal falls below our own detection bar at every severity we reserved

This is the finding that matters, and I got it wrong on the first pass before getting it right.

The project's strain gauges exist to give the structural-sensing suite information about
*structural* damage that the conventional suite cannot get. My first measurement compared the
delivered data against the 10-microstrain floor from the Phase-0 feasibility spike and looked
alarming. Then I checked the history and found that we had **deliberately superseded that floor**
in Sessions 9–11: a 1.0 N diagnostic probe was rejected as unsafe (it violated the joint-angle
limit), and we replaced the per-sample floor with a synchronous-detection floor of 0.405
microstrain and a required 2× margin, then selected the 0.05 N probe against that bar with a
bracketed grid. I had nearly reported a carefully litigated decision as a defect.

So I re-measured with the project's actual operative statistic — and validated my instrument
first, because the whole finding rests on it. Our safe-probe screen recorded an
actuator-versus-healthy value of 0.898 microstrain at the selected condition; my pipeline brackets
that (0.729 at remaining gain 0.50, 1.089 at 0.25). The instrument reproduces the screen.

The structural numbers, at the severities the approved assignment actually reserves:

```text
remaining EI   distance    margin    where it is reserved
    0.90        0.0544      0.13x    validation
    0.85        0.0864      0.21x    pilot
    0.75        0.1614      0.40x    development
    0.60        0.3267      0.81x    pilot
    0.50        0.4873      1.20x    development
    0.40        0.7266      1.79x    validation
                                     floor 0.405; required 2.0x = 0.810
```

**Every reserved structural severity is below the bar.** And it degrades with payload, meaning it
is worse in validation and worse still in test:

```text
payload      rem EI 0.90    rem EI 0.40
 0.000 kg       0.13x          1.78x
 0.100 kg       0.07x          0.81x
 0.125 kg       0.06x          0.76x
 0.200 kg       0.05x          0.64x
```

The screen that justified the 0.05 N probe cleared its bar with a *structural* value of 1.015
microstrain at remaining EI 0.50 under a different excitation. Four of the six structural
severities we reserved — 0.60, 0.75, 0.85, 0.90 — are **milder than the only severity at which
the probe amplitude was ever validated**, and under the assignment's own trajectories and payloads
even the two severe ones fall short.

What this does and does not mean matters. It bounds the *interpretable* detector rung. The learned
models I am about to build read the raw sensor tensor and may extract more than a single-frequency
harmonic statistic; that is genuinely untested. So this is not a prediction that the hypothesis
fails. It is a warning that if I fit models on this data and the structural-sensing suite fails to
beat the conventional one, **we will not be able to tell hypothesis failure from method failure** —
and separating those two is precisely what the Claim Sheet's pre-declared failure shapes exist to
do. Our own validation screen says this condition should clear 2×; the delivered data does not.
The scientific standard's stop-or-go rule applies: diagnose before proceeding.

**What I proposed instead of a block on Codex.** I am not asking for regeneration and I did not
block the artifact — the generator faithfully implements a design *we jointly approved*, and I
approved it twice without ever measuring what physics it would produce. That miss is mine. Instead
I imposed a gate on my own next step: before building the Gate-4 capacity ladder, I run a cheap
structure-versus-healthy separability check on the **development split only**, for both suites, at
both development severities. If the structural suite separates structure where the conventional
one cannot, the design is sound and this becomes a recorded limitation on the mild end of the
grid. If neither separates, we amend the severity grid — and possibly the probe amplitude within
the safety envelope — **before** validation or test data are spent. Development data alone can
answer this, which is exactly what a development split is for.

### Finding 2 — the contact confound is nearly inert, and where it fires it is caused by the fault

The design gives every run one of three context axes: payload, temperature, and whether the arm's
tip briefly touches a surface. Measuring all 472 runs:

```text
runs assigned a contact profile        236
runs that actually touched the plane    11   (4.7%)
  development 0/76   pilot 11/76   validation 0/84
contact-active steps                   243
scheduled contact-window steps     104,800
duty cycle inside the windows        0.232%
```

In development and validation, the contact label has **zero physical consequence** — the
three-axis context design realizes as two axes there.

The sharper part: I pulled the fault identity of the eleven touching runs from the label payloads
rather than inferring it from run numbering. **Every contact event in the entire dataset occurs in
an encoder bias or encoder drift run** — 7 of 16 bias runs, 4 of 16 drift runs, and 0 of 44
healthy, structural, actuator, or dropout runs. The mechanism is clean: bias and drift corrupt the
measured joint angle, so the controller drives the true joint past its target, the tip descends
further, and it reaches the plane. Dropout does not shift the mean, so it never touches.

That makes contact an **effect of the fault rather than an independent confound**, and a contact
event at 2.6–3.0 N is loudest in the strain-gauge channel that only the structural suite carries.
The information between the fault and the *assigned* contact label is exactly zero, which is what
we designed and verified. The information between the fault and contact *actually occurring* is
not. The bias runs in the direction that favours our own hypothesis — the direction that does not
announce itself in a disappointing result later.

Today the exposure is contained: eleven pilot runs, and pilot feeds neither model fitting nor
calibration nor the headline comparison. The reason to raise it now is the test split, whose
contact window is 2.2 seconds against pilot's 0.6, at the heaviest payloads, generated once after
the configuration freezes and never inspected. If the coupling reappears there at a higher rate it
lands directly in the confirmatory result with no chance to see it first.

### Smaller notes I passed to Codex

Four non-blocking items: the binding validator accepts a self-consistently re-hashed assignment
when its optional pinning argument is omitted (both shipped command-line tools do pin it, so this
is defense-in-depth, not a live hole); the generator hard-codes the control timestep in three
places instead of reading it from the bound configuration; roughly 1.4 GB of the 3.7 GB dataset is
a byte-identical duplicate because plant traces are written once per suite; and the deliberately
discarded partial generation run is recorded in the reports and the chat but not inside the
Reproducibility Packet, where the standards want exclusions preserved.

## Challenges and how they were resolved

**I nearly reported a settled decision as a defect.** My first framing measured the delivered data
against the Phase-0 10-microstrain floor and concluded the probe was 20× too weak. Checking the
history showed that floor had been deliberately replaced, and that 1.0 N had been rejected on
safety grounds after real analysis. Had I sent that, I would have re-litigated a decision the team
made carefully and burned Codex's next session on a non-issue. The fix was to find the *operative*
bar and validate my instrument against a number the team had already published, before claiming
anything.

**My first measurement of the fault signature was confounded.** Comparing fault runs against
healthy runs in the delivered data gave ≈0.8 microstrain for *every* fault family at *every*
severity — suspiciously flat. A signature independent of fault magnitude is not the fault. Each
reservation carries its own sensor seed, the controller reads noisy encoders, and the closed loop
amplifies that into a different physical trajectory, so I was measuring run-to-run noise. I
re-ran with identical seeds varying only the fault, which isolated the real effect and revealed
the clean monotone severity trend the delivered data had hidden.

**Establishing that a claim was real before making it.** For the contact finding, my run-numbering
arithmetic said the touching runs were all encoder faults. That is exactly the kind of inference
that produced a false positive in my previous session, so I re-derived the fault identity from the
label payloads on disk instead. It confirmed the claim — but the claim would not have been worth
making on the arithmetic alone.

## Decisions I made

1. **Approve the artifact rather than block it.** The finding is about the approved design, not
   about Codex's implementation of it. Blocking the generator would have been blocking the wrong
   object and would have implied a defect that is not there.
2. **Impose the gate on my own next step instead.** `BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK`
   keeps the project from walking into a manufactured method failure without stalling Codex or
   demanding regeneration on evidence that does not yet justify it.
3. **Do not propose an amendment yet.** Both findings point at the same lever — excitation and
   severity — and the separability check on development data will say whether an amendment is
   needed and what it should change. Proposing one now would be guessing.
4. **Raise Finding 2 without acting on it.** The contact coupling is contained today; what it
   needs is to be on the record before the test contact profile is inherited unexamined.

## Reasoning paths explored

I considered blocking the Gate-2 handoff outright on the grounds that data unable to demonstrate
the effect should not be accepted. I rejected that: the review cycle's question is whether the
artifact is what it claims to be, and it is. I also considered treating Finding 1 as a plain
recorded limitation and proceeding to Gate 4 as planned. I rejected that too — the failure-shape
taxonomy in Slots 11–13 is the whole reason we distinguish a clean negative from a broken
experiment, and running the fits without first checking separability would forfeit that
distinction at the exact moment it matters.

## Insights gained

The one worth keeping: **a design review that reads the design cannot find what the design does.**
I reviewed this assignment twice and measured its label distributions to ten decimal places — the
context leak, the parity residual, the seed hygiene — and every one of those measurements was
correct. None of them could see that the third context axis fires on 4.7% of the runs that
declare it, or that the structural signal sits below our own bar. That only became visible when
real physics existed to measure. The lesson generalizes to the remaining gates: a pre-registration
is a claim about data, and it stays unverified until data exist to check it against.

The second: **the reviewer's yardstick needs the same audit as the artifact.** I used a superseded
floor and got a dramatic wrong answer, then used a confounded pairing and got a flat wrong answer.
Both looked like findings. Validating my instrument against a number the team had already
published is what separated the real result from the two false ones.

## Files created or updated

**Created**
- `agents/Claude/Session Summaries/HumanReport33.md` (this report)

**Updated**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my Session-33 review turn (+220 / −0 lines, verified physically last)
- `README.md` — one lean running-log entry for the review outcome
- `agents/Claude/README.md` — workspace index through Session 33
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten

**Deliberately unchanged**
- Every review-target file — approval was given with no edits, as the review cycle requires
- `Reproducibility Packet/config.json` — still absent
- `Claim Sheet.md` / `Accessible Claim Sheet.md` — no amendment written
- `agents/Claude/references.md` — no external source read this session
- `director_requests.md` — no director-only dependency arose
- The transcript-order monitoring thread — Codex's Session-32 append was clean (+178 / −0, both
  headers after my Session-32 turn, Codex physically last), the eleventh consecutive clean append,
  so per the standing agreement I flag only on recurrence

## Verification performed

```text
tracked file digests reproduced          6 / 6
approved assignment byte-unchanged       76255a80...514ae
independent prose re-derivation          944 / 944 rows, 0 field mismatches
realized fault-context leakage           0.0000000000 bits, all splits, all axes
cross-split fault-tuple reuse            0
C1 gauge-channel leakage                 0 / 472 payloads
temperature profile realization          max deviation 2.3e-3 C
fault families with zero effect          0 / 396 runs
full packet test suite                   397 passed in 9.79 s
adversarial wrapper tampering refused    8 / 9 (the ninth is the noted default)
generator test-split requests refused    3 / 3
transcript append                        +220 / -0, physically last
```

## Next steps

1. **Run the structural separability check on the development split** — both suites, both
   development severities, interpretable rung plus a small learned probe. This answers Finding 1
   and unblocks or amends Gate 4.
2. **Depending on that answer:** either proceed to the Gate-4 capacity ladder with a recorded
   limitation, or write a Claim-Sheet amendment covering excitation amplitude and the structural
   severity grid, and run it through the review cycle before validation or test data are consumed.
3. **Fold Finding 2 into whatever that amendment decides** — specifically, choose the test contact
   profile deliberately rather than inheriting it.
4. **Gate 5 calibration** remains queued behind Gate 4 and touches validation only.
5. `config.json` stays absent until Gates 2–7 close.

## Claim boundaries

This session produced no research result. It did not fit a model, select a threshold, authorize a
recovery action, evaluate the conventional-versus-structural comparison, materialize any test
identity or payload, freeze the configuration, or close Phase 2. Finding 1 bounds the
interpretable detector rung only and does not predict the headline outcome. The central question —
whether distributed structural sensing gives a robot an adaptive advantage — remains open and
unanswered.
