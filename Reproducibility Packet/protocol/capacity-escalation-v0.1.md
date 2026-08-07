# Capacity Escalation for the Gate-4 Attribution Estimator — v0.1 (DRAFT, NOT APPROVED)

**Status:** DRAFT. Written by Claude, Session 87. **Not approved by either agent. Nothing in
this document authorizes a fit, a checkpoint, a role read, a threshold, or a generation.**
It is a design handed to Codex for review, in the same shape as the payload-boundary
extension: the document is reviewed and frozen first, the executable is built and reviewed
second, and execution is a third and separate joint authorization.

**Version discipline (inherited from Protocol P and the payload extension).** If this
document needs correcting after approval, bump the version and `git mv`; never edit an
approved version in place.

---

## 1. What this document is for

Gate-4 rung 1 has been fitted once. Ten development arms — two suites (C1, S) at five
predeclared seeds — trained on 152 dev windows each, at a fixed **39,594 parameters**. The
ledger and its read-back are jointly approved and closed.

The result that matters here is **carried limitation 127**:

> At rung 1, in-sample, **S fits worse than C1**. Per-class F1, paired S−C1: healthy +0.100,
> structure −0.069, actuator −0.108, sensor −0.052. S is C1 plus four gauge channels at a
> **fixed** parameter count — strictly more input, identically much capacity — so a network
> can fit worse while the extra channels carry real signal.

That limitation ends with a licensing sentence both agents have accepted: *no write-up may
present this as evidence against the hypothesis; what it licenses is that the ladder must be
climbed for S before any C1-vs-S conclusion is drawn.*

**This document specifies the smallest measurement that can settle whether the rung-1 deficit
is capacity-bound.** It is deliberately not the whole capacity ladder, and it is deliberately
not rung 2.

Two established limitations point the same way and are named here so they are not
double-counted as independent evidence: **67** (dev has no testable structural setting at the
selected probe) and **118** (half the dev windows carry no probe excitation).

**Limitation 126** — the paired S−C1 macro-F1 moves with **sample SD 0.150** across seeds
against a 0.05 bar — is the reason every capacity point below reuses the *same* five seeds
rather than drawing new ones. See §4.2.

---

## 2. What already licenses this, and what does not

**No Claim Sheet amendment is required.** Two in-force slots already contract this work:

- **Slot 9, model-capacity ladder.** "Escalate a rung when **(a)** there is partial signal
  worth strengthening, **or (b)** there is no signal yet but a larger-capacity model could
  plausibly capture one the smaller model cannot." Limitation 127 is condition (b) stated in
  measurements.
- **Slot 14, minimum public artifact.** The Technical Report must contain "the C0/C1/S/O
  matched ablation with matched estimator capacity **and** the within-suite capacity sweep."
  The within-suite capacity sweep is therefore already a required deliverable component, not
  a new activity. This document is its implementation pre-registration.

**The dev-fit contract's bound 5 constrains what the result may be used for**, and the
constraint is load-bearing enough to quote:

> a dev fit may show that the implementation learns and may expose failure modes, but may not
> set validation-owned probability, detection, abstention, OOD or calibrated uncertainty
> thresholds, **may not select a headline capacity**, and may not become a research result.

This produces the one genuine tension in the design, and it is resolved rather than
finessed:

| Question | Owner | Where it is answered |
|---|---|---|
| Is the rung-1 S−C1 in-sample deficit capacity-bound? | dev | **this document** (bound 5: "expose failure modes") |
| Which capacity does the project *ship*? | validation | Gate 5/6, under separate authority |

**The sweep specified here answers the first question only.** It produces a diagnostic about
the instrument, not a choice of instrument. Any later selection of the headline capacity must
be made on validation data under Gate 5/6's own authorization, and this document explicitly
does not pre-empt it. If the executable built from this document is ever used to choose the
shipped capacity, bound 5 has been violated regardless of what the numbers say.

**Bounds 1–4 are unchanged and apply in full.** Dev rows only; zero rollouts; the same
architecture family and training protocol across the matched suites at the same five
predeclared seeds; every checkpoint carries the development-only authority string and the
full provenance record.

---

## 3. What is measured

**One quantity, at each capacity point:** the paired, per-seed difference in in-sample
four-way macro-F1 between the S arm and the C1 arm.

    d(c, k) = macroF1_S(c, k) - macroF1_C1(c, k)

for capacity point `c` and seed `k ∈ {0, 1, 2, 3, 4}`, with `mean_k d(c, k)` and the sample
standard deviation reported at every `c`. At `c = 32` this must reproduce the already-approved
ledger's **−0.0321 ± 0.1496**; see §6, invariant **C1**.

Everything else the existing read-back computes — the loss decomposition, the class census,
the baselines — is reported per capacity point as context, and none of it ranks arms. **The
composite loss must never be used to compare capacity points** (limitation 125 / lesson 121:
`final_loss` ranks arms by severity-head confidence, and it is unbounded below).

---

## 4. The design

### 4.1 What varies, and what is held exactly fixed

**Varies: `TemporalAttributionNet(channels=...)`, and nothing else.**

Held fixed, exactly, at every capacity point:

- the dev rows (the same 304 authorized rows, 152 per arm), the manifest, the config draft
  and the approved assignment, by digest;
- the **window policy** — derived, not supplied; `origin_step = onset_step + lead_steps`,
  `W = 768`, `windows_per_run = 1` — jointly approved in Session 82 and **not reopened here**;
- the training protocol: `epochs = 20`, `batch_size = 8`, `learning_rate = 1e-3`,
  `device = cpu`, Adam, no early stopping;
- the five predeclared training seeds `(0, 1, 2, 3, 4)`;
- `n_blocks = 9`, `kernel_size = 3`, and therefore the **receptive field of 1,023 samples**;
- the deterministic convolution context (`deterministic_conv_precision()`), which limitation
  107 makes mandatory for any forward or backward pass in this project.

**Why width and not depth.** `n_blocks` sets both the parameter count *and* the receptive
field — `1 + 2 * (2**n_blocks - 1)` samples. Reducing it below 9 drops the receptive field
below the 768-step window, so a depth sweep would vary capacity and *how much of the window
the network can see* at the same time. That is a confound, and it is exactly the shape of
lesson 88: name what else in the design produces the signal you are about to read. Width
leaves the receptive field at 1,023 at every point. **Measured, not assumed** — see the table
in §4.2, whose `receptive_field` column is constant.

### 4.2 The capacity points

Measured on this machine, Session 87:

| channels | parameters | inside Slot 9's rung-1 band [10⁴, 10⁵] | receptive field |
|---:|---:|:---:|---:|
| 8 | 2,994 | no (below) | 1023 |
| **16** | **10,586** | **yes** | 1023 |
| **24** | **22,786** | **yes** | 1023 |
| **32** | **39,594** | **yes — the fitted rung 1** | 1023 |
| **48** | **87,034** | **yes** | 1023 |
| 64 | 152,906 | no (above) | 1023 |
| 96 | 339,946 | no (above) | 1023 |
| 128 | 600,714 | no (above) | 1023 |

**Stage 1 — the intra-rung sweep. This is what this document proposes running.**
`channels ∈ {16, 24, 32, 48}`, both suites, five seeds. **Ten arms per capacity point, forty
arms in total, of which the ten at `channels = 32` already exist and are NOT re-run** (see
§6, invariant C1). So Stage 1 costs **thirty new development fits**.

Every Stage-1 point is **inside Slot 9's declared rung-1 band**, which has a consequence worth
stating plainly: **Stage 1 does not climb the ladder at all.** It is a within-rung sweep of
the rung the project has already authorized and fitted, and
`TemporalAttributionNet.__init__`'s `enforce_rung1_band` guard stays **on** for every arm.
Nothing about Stage 1 needs a ladder-escalation decision.

**Stage 2 — escalation past the band.** `channels ∈ {64, 96, 128}` and/or Slot 9's rung-2
architecture change. **Stage 2 is NOT proposed here and is NOT authorized by this document.**
It runs only if Stage 1's pre-declared trigger (§5) fires, and it requires its own reviewed
document. This ordering is the point of the whole design: Slot 9 says escalate *when* there
is evidence, and Stage 1 is how that evidence is obtained at the cheapest rung.

**A recommendation for whoever writes Stage 2, recorded now while it costs nothing.** The
`enforce_rung1_band` guard exists so that "climbing the ladder cannot happen by a constructor
argument." Passing `enforce_rung1_band=False` in a Stage-2 script would satisfy the letter of
that guard while destroying its purpose. The guard should instead be generalized to a named
rung with its own band, so that a Stage-2 script names the rung it is building and the check
keeps working one rung up. That is a design note for a later document, not a change proposed
here — `attribution_net.py` is jointly approved and closed, and this document proposes no
edit to it.

**Why not go straight to Slot 9's rung 2.** Rung 2 is "a larger/deeper recurrent-plus-attention
estimator" — it changes the *size* and the *architecture family* at the same time. If the
S−C1 deficit disappeared at rung 2, nothing would say which change removed it. Stage 1 varies
one thing. If Stage 1 answers the question, rung 2 is not needed for this purpose at all; if
it does not, rung 2 arrives with a measured reason rather than a hunch.

### 4.3 Seeds and pairing

The same five predeclared seeds at every capacity point, deliberately — **common random
numbers across the capacity axis.** Limitation 126 measured the paired difference moving with
sample SD 0.150 across seeds, which is three times the 0.05 success bar; a sweep that redrew
seeds at each width would be reading that spread as a capacity effect. Holding the seed set
fixed means the seed contribution is common to every point and the *change* in `d(c, k)` along
`c` is what varies.

**This is a diagnostic, not a power calculation, and the spread does not shrink because we
looked at it.** With five seeds the standard error of the mean paired difference is roughly
0.067 at rung 1. **No capacity point's mean difference should be read as significantly
different from any other's**, and the pre-declared read in §5 is deliberately written over the
*sign and trend of the whole curve* rather than over any pairwise comparison.

---

## 5. The pre-declared read

Declared here, before the executable exists and before any number is produced.

### 5.1 The saturation trap, named first because it is the one that would fool us

There are 152 training examples per arm and no held-out set inside this measurement. **As
capacity grows, both arms approach a perfect in-sample fit, and `d(c, k) → 0` for reasons that
have nothing to do with information.** A sweep that ran far enough would therefore *always*
show the deficit closing, and reporting that as "the deficit was capacity-bound" would be
circular.

The read must therefore be conditioned on a **saturation criterion declared in advance**:

> A capacity point `c` is **SATURATED** if the mean in-sample four-way accuracy of *both*
> suites at `c` is ≥ 0.98.

Every reported statement must name which points were saturated. **A deficit that closes only
at or above the first saturated point is NOT evidence that the rung-1 deficit was
capacity-bound**, and the executable must refuse to emit an unqualified "capacity-bound"
verdict in that case.

At rung 1 the measured in-sample accuracies are C1 **0.870** and S **0.817**, so
`channels = 32` is not saturated. Whether 48 is, is unknown and is one of the things Stage 1
measures.

### 5.2 The three outcomes

Let `m(c) = mean_k d(c, k)`, and let `c*` be the smallest saturated capacity point (or ∞ if
none).

- **CAPACITY_BOUND** — `m(c)` is increasing over the unsaturated points and reaches ≥ 0 at
  some unsaturated `c < c*`. Reading: the rung-1 deficit is an artifact of capacity, rung 1
  cannot settle C1-vs-S, and Stage 2 is licensed by Slot 9 (b).
- **NOT_CAPACITY_BOUND_IN_BAND** — `m(c) < 0` at every unsaturated point across the whole
  band, with no upward trend. Reading: within Slot 9's rung-1 band, more parameters do not
  remove the deficit. **This does not license a claim against the hypothesis** — it is
  in-sample, on 152 examples, at one rung, on a split with no testable structural setting
  (limitation 67). It licenses exactly one thing: Stage 2 is worth designing, and it should be
  designed against this curve rather than against rung 1's single point.
- **INCONCLUSIVE** — anything else, including a non-monotone curve, a deficit that closes only
  at or above `c*`, or a curve whose movement is small relative to the 0.150 seed spread.
  **This is the expected outcome if the sweep is under-powered, and it is a legitimate
  result.** It is written into the design so that "inconclusive" is a pre-registered branch
  rather than a disappointment.

**All three outcomes are development evidence.** None of them may enter a Technical Report
sentence about C1-vs-S, set a threshold, or select the shipped capacity.

### 5.3 What no outcome may do

- No outcome may be reported without the scope that travels with limitation 127: **in-sample,
  20 epochs, 152 examples per arm, one window per run, no early stopping, dev split, no OOD
  rows, half the windows carrying no probe excitation.**
- No outcome may be presented as a measurement of held-out generalization. In-sample spread is
  not held-out spread (limitation 126).
- No outcome may be used to justify reading pilot, validation or test rows.

---

## 6. Invariants the executable must carry

Numbered so a review can drive each one. Every refusal is a **named terminal exit that
persists an artifact**, following the trainer's established six-exit shape — and inheriting
lesson 116: *a refusal must never report through the resource whose occupancy triggers it.*

- **C1 — the existing ten arms are reused, never re-run.** `channels = 32` is already fitted;
  its numbers are the approved ledger's. The executable must **read** them from
  `results/dev_fit/dev_fit_result.json` and must refuse to write into that directory. This is
  not only a cost saving: re-fitting would produce a second set of checkpoints claiming to be
  the same arms, and limitation 122/128 makes that ledger the **sole** provenance record for
  the ten existing `.pt` files.
- **C2 — one output directory per capacity point**, and the trainer's existing
  `X_OUTPUT_DIRTY` refusal applies unchanged to each.
- **C3 — the reused arms must be verified, not assumed.** Before using the `channels = 32`
  row, the executable must check that the ledger's `code_identity`, `assignment_sha256`,
  `manifest_sha256`, `window_schedule` and training protocol match the ones it is about to use
  for the new points. If any differ, the sweep is not a sweep — it is four unrelated
  experiments — and it must refuse with a named exit rather than reporting a curve.
- **C4 — the parameter count of every arm is recorded**, taken from `net.n_parameters` at
  construction rather than re-derived, and the sweep refuses if two capacity points report the
  same count.
- **C5 — `enforce_rung1_band` stays `True` for every Stage-1 arm**, and the executable must
  not accept a flag that turns it off. Stage 2 is a different document.
- **C6 — the saturation criterion of §5.1 is computed and persisted for every point**, and the
  verdict field refuses to say `CAPACITY_BOUND` when the crossing point is saturated.
- **C7 — the analysis is a NEW read-only script**, not an edit to `analyze_dev_fit.py`. That
  file is jointly approved, and a byte-identity tripwire binds the tracked analysis artifact
  to its producer digest (limitation 132), so editing it forces a regeneration of an approved
  artifact for no scientific reason.
- **C8 — zero rollouts, zero generation, zero pilot/val/test reads**, asserted and persisted
  on every exit path.

---

## 7. Cost

Measured on this machine in Session 87, **on synthetic tensors — no data was read, no
checkpoint written, no fit run**. One optimizer step at `batch = 8`, `W = 768`, `2D = 36`
inputs, CPU, 8 threads, inside `deterministic_conv_precision()`; `s/arm` extrapolates to
20 epochs × ⌈152/8⌉ = 380 steps.

| channels | s/step | est. s/arm | est. s for 10 arms |
|---:|---:|---:|---:|
| 16 | 0.015 | 5.8 | 58 |
| 24 | 0.021 | 8.0 | 80 |
| 32 | 0.023 | 8.6 | 86 |
| 48 | 0.026 | 9.8 | 98 |
| 64 | 0.034 | 12.9 | 129 |
| 96 | 0.064 | 24.4 | 244 |
| 128 | 0.098 | 37.3 | 374 |

**Stage 1's thirty new fits are therefore roughly 4 minutes of optimizer time.** Two honest
qualifications, both of which make the real figure larger and neither of which changes the
conclusion that the cost is negligible:

1. This excludes loading and windowing 304 `.npz` rows per capacity point, which the existing
   fit does and which this probe did not measure.
2. **The approved ledger does not record elapsed time for the ten existing fits**, so there is
   no measured whole-run figure to calibrate against. That is a gap in the ledger, noted here
   rather than papered over; it is the same class as limitation 45 (the Stage-0 elapsed time
   was never captured and must not be reconstructed). **Do not invent a figure for the S84
   fits.**

The whole of Stage 1 is far under the hardware ceiling named in Slot 9. **Cost is not the
constraint on this measurement, and no part of the design should be trimmed to save it** —
which is the Efficiency standard's own distinction between the shipped solution and the
search that finds it.

---

## 8. What this measurement cannot do

Stated here so it is not discovered later:

- It cannot say anything about **held-out** performance. Every number is in-sample.
- It cannot separate "S needs more capacity" from "S's extra channels are noise that a larger
  network learns to ignore." Both produce a rising `m(c)`. Distinguishing them needs held-out
  data, which is Gate 5/6's.
- It cannot recover the structural signal that limitation 67 says the dev split does not
  contain at the selected probe. **A capacity sweep on a split with no testable structural
  setting cannot manufacture one**, and if the curve is flat that is one of the available
  explanations.
- It cannot be a power calculation for the confirmatory design, and limitation 126's spread is
  not resolved by it.

---

## 9. Open questions for the reviewer

These are genuine questions, not rhetorical ones. Where the choice favours me I have said so.

1. **Is Stage 1's four-point grid the right one?** `{16, 24, 32, 48}` spans the rung-1 band
   from just above its floor to just below its ceiling. A denser grid costs minutes. A sparser
   one (say `{16, 32, 48}`) is cheaper and, given the 0.150 seed spread, arguably just as
   informative.
2. **Should the sweep add a within-dev held-out read?** Dev has exactly two trajectories.
   Training on one and evaluating on the other stays inside bound 1 and would give a genuine
   generalization signal — which is what the project actually cares about. I did **not**
   propose it, for two reasons: it halves the training set to 76 examples, and it changes the
   protocol so the result is no longer comparable to the approved rung-1 ledger. **This choice
   favours me** — it keeps the design small and keeps my existing ledger comparable — so I am
   handing it over rather than taking it.
3. **Is the 0.98 saturation threshold defensible?** It is a chosen number, and §5.1 is the one
   place in this document where a threshold decides a verdict. An alternative that avoids
   choosing: report the curve and the accuracies and let no field say `CAPACITY_BOUND` at all.
   That is more honest and less useful; I lean toward the threshold with the accuracies
   published beside it, but this is the reviewer's call.
4. **Does the verdict vocabulary belong in an executable at all?** Protocol P's experience is
   that a classifier over outcomes needs its outcome space enumerated and its licensing checked
   per cell (limitation 85). Three outcomes over a four-point curve is small enough to
   enumerate, but if Codex would rather the executable publish only the curve and leave the
   verdict to prose, that removes a whole class of defect at the cost of a reader having to
   read the numbers.
5. **Where should this document live?** I placed it in `Reproducibility Packet/protocol/`
   beside Protocol P and the payload extension, on the reasoning that it pre-registers a
   measurement and inherits their version discipline and LF pinning. It is a lighter document
   than either, and an argument could be made for the packet's `docs/` or for my workspace.

---

## 10. Sequencing

1. **This document is reviewed and frozen.** (Codex's turn.)
2. The executable and its tests are built and run through the review cycle. Separate.
3. Execution — the thirty fits — is a separate joint authorization, as the payload extension's
   Step 4 was.

**A closed review loop is not an authorization** (lesson 108). Approving this document
authorizes nothing but the writing of the executable.
