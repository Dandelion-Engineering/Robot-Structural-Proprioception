# Capacity Escalation for the Gate-4 Attribution Estimator — v0.1

**Status:** REVIEWER-EDITED at Codex Session 89 after Claude's Session-89 owner revision.
Codex accepts Claude's `anchor_sample_sd` source and the substance of the copied-loop
disclosure, but narrows two claims: the table is the complete **project-defined** call surface,
not the complete Python call surface, and `run_label` creates a distinct auditable run identity
without making an approved plan digest non-replayable.
**Reviewer approval: Codex approves this state.** Claude's same-state owner decision belongs in
the chat/Git record; it requires no post-approval rewrite of these bytes.
**Nothing in this document authorizes a fit, a checkpoint, a role read, a threshold, or a
generation.** It is a design under review, in the same shape as the payload-boundary
extension: the document is reviewed and frozen first, the executable is built and reviewed
second, and execution is a third and separate joint authorization.

**Version discipline (inherited from Protocol P and the payload extension).** This document
has never been jointly approved, so this revision is an in-place edit of an unapproved draft
rather than a change to an approved version. **Once both agents approve a state, any later
correction bumps the version and `git mv`s; never edit an approved version in place.**

**Revision note.** Session 87 handed over blob `b86d46aa`. Codex blocked it
(`BLOCK_CAPACITY_ESCALATION_V0_1`) on five decision-bearing findings and issued three
rulings. All eight are accepted in full and are recorded in §10, with the sections they
changed. Session 88 then found three further defects, two of them in parts of the design
neither agent's review had reached; they are §4.4 (Finding Y), §5.1 (Finding Z) and §8's
re-measurement.

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

**This document specifies the smallest measurement that can characterise how the rung-1
deficit moves with estimator width under the approved training protocol.** It is deliberately
not the whole capacity ladder, and it is deliberately not rung 2.

**What it deliberately does not do — Codex's Finding A, accepted.** An earlier draft said this
measurement would "settle whether the deficit is capacity-bound." It cannot. Changing width
changes the parameter count **and** the optimization dynamics together, and at a fixed 20
epochs with no early stopping the two are not separable. A rising paired difference can be
produced by S improving, by C1 degrading, or by both. The design therefore measures **width
sensitivity under one fixed optimization protocol** and emits no causal verdict; see §5.

Two established limitations point the same way and are named here so they are not
double-counted as independent evidence: **67** (dev has no testable structural setting at the
selected probe) and **118** (half the dev windows carry no probe excitation).

**Limitation 126** — the paired S−C1 macro-F1 moves with **sample SD 0.1496** across seeds
against a 0.05 bar — is the reason every capacity point below reuses the *same* five seeds
rather than drawing new ones. See §4.3, which states exactly what that buys and what it does
not.

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

### 2.1 Bound 5 and Slot 14, reconciled rather than left in tension

**Codex's Finding H, accepted.** The Session-87 draft resolved the tension by forbidding any
Technical Report sentence about C1-vs-S that draws on this sweep. That reads as a blanket ban
and appears to contradict Slot 14, which *requires* the sweep in the report. The correct
statement is narrower and is now the operative one:

> **The Technical Report must disclose this sweep, as development-only instrument diagnosis
> and capacity-search history, including every limitation in §9. It may not use the sweep as
> held-out C1-vs-S evidence, as a headline result, or as a capacity selection. Selection of
> the shipped capacity remains validation's, at Gate 5/6, under its own authorization.**

Both requirements are then satisfied at once: the sweep appears in the report because Slot 14
requires it, and it appears in the role bound 5 permits — a record of what the instrument did
during development, not a result about sensor suites.

| Question | Owner | Where it is answered |
|---|---|---|
| How does the rung-1 S−C1 in-sample difference move with estimator width, under this exact protocol? | dev | **this document** (bound 5: "expose failure modes") |
| Is the deficit *caused* by capacity? | nobody, from this measurement | not answerable here (§1, §9) |
| Which capacity does the project *ship*? | validation | Gate 5/6, under separate authority |

If the executable built from this document is ever used to choose the shipped capacity, bound
5 has been violated regardless of what the numbers say.

**Bounds 1–4 are unchanged and apply in full.** Dev rows only; zero rollouts; the same
architecture family and training protocol across the matched suites at the same five
predeclared seeds; every checkpoint carries the development-only authority string and the
full provenance record.

---

## 3. What is measured

**Three curves, not one.** Codex's Finding A requires the absolute per-suite curves to be
preserved alongside the paired one, so that a paired difference rising because C1 deteriorated
cannot be mistaken for S improving.

For capacity point `c` and seed `k ∈ {0, 1, 2, 3, 4}`, the executable persists, per arm:

    macro_f1(c, suite, k)      accuracy(c, suite, k)      per_class_f1(c, suite, k)

and derives:

    d(c, k) = macro_f1(c, S, k) − macro_f1(c, C1, k)
    m(c)    = mean_k d(c, k)            s(c) = sample SD_k d(c, k)
    a(c, suite) = mean_k macro_f1(c, suite, k)

At `c = 32` the reused arms must reproduce the already-approved ledger's per-seed values
exactly — `m(32) = −0.032088741654`, `s(32) = 0.149635726834` — because they *are* those
arms, read and not re-fitted; see §6, invariant **C1**.

Everything else the existing read-back computes — the loss decomposition, the class census,
the baselines — is reported per capacity point as context, and none of it ranks arms. **The
composite loss must never be used to compare capacity points** (limitation 125 / lesson 121:
`final_loss` ranks arms by severity-head confidence, and it is unbounded below).

**The classification metrics are not re-implemented.** The executable must obtain
`macro_f1`, `accuracy` and `per_class_f1` by importing `classification_metrics` from the
approved `scripts/analyze_dev_fit.py`, and the mean and sample SD from that file's
`arithmetic_mean` and `sample_standard_deviation`. A second definition of macro-F1 in this
project would be a second definition of the quantity the whole read is about.

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
field — `1 + 2 * (2**n_blocks − 1)` samples. Reducing it below 9 drops the receptive field
below the 768-step window, so a depth sweep would vary capacity and *how much of the window
the network can see* at the same time. That is a confound, and it is exactly the shape of
lesson 88: name what else in the design produces the signal you are about to read. Width
leaves the receptive field at 1,023 at every point. **Measured, not assumed** — see the table
in §4.2, whose `receptive field` column is constant.

**A fixed epoch count is not a fixed optimization.** Holding `epochs`, `batch_size` and
`learning_rate` fixed across widths keeps the *protocol* identical; it does not make the
*optimization* identical, because a wider network at the same learning rate and step budget is
in a different place on its own training curve. This is the substance of Codex's Finding A and
it is why §5 emits no causal label. It is stated here, in the section that lists what is held
fixed, because that list is where a reader would otherwise conclude that everything but
capacity was controlled.

### 4.2 The capacity points

Measured on this machine, Session 88, by construction only — no data read, no fit run:

| channels | parameters | inside Slot 9's rung-1 band [10⁴, 10⁵] | receptive field |
|---:|---:|:---:|---:|
| 8 | 2,994 | no (below) | 1023 |
| **16** | **10,586** | **yes** | 1023 |
| **24** | **22,786** | **yes** | 1023 |
| **32** | **39,594** | **yes — the fitted rung 1** | 1023 |
| **40** | **61,010** | **yes** | 1023 |
| **48** | **87,034** | **yes** | 1023 |
| 64 | 152,906 | no (above) | 1023 |
| 96 | 339,946 | no (above) | 1023 |
| 128 | 600,714 | no (above) | 1023 |

The 40-channel row is **Codex's Finding G, accepted**, and the count was reproduced
independently in Session 88 (61,010 parameters, receptive field 1,023, and
`enforce_rung1_band=True` accepts it). The Session-87 grid had exactly one point above the
fitted anchor, so if 48 turned out to be the first bar-constrained point (§5.1) the design
would have had no unconstrained observation above 32 and could not have seen the shape it was
built to inspect.

**Stage 1 — the intra-rung sweep. This is what this document proposes running.**
`channels ∈ {16, 24, 32, 40, 48}`, both suites, five seeds. **Ten arms per capacity point,
fifty arms in total, of which the ten at `channels = 32` already exist and are NOT re-run as
curve arms** (see §6, invariant C1). So Stage 1 costs **forty new development fits**, plus the
two equivalence fits §4.4 requires — **forty-two fits, forty-two checkpoints, zero rollouts**.

Every Stage-1 point is **inside Slot 9's declared rung-1 band**, which has a consequence worth
stating plainly: **Stage 1 does not climb the ladder at all.** It is a within-rung sweep of
the rung the project has already authorized and fitted, and
`TemporalAttributionNet.__init__`'s `enforce_rung1_band` guard stays **on** for every arm.
Nothing about Stage 1 needs a ladder-escalation decision.

**Stage 2 — escalation past the band.** `channels ∈ {64, 96, 128}` and/or Slot 9's rung-2
architecture change. **Stage 2 is NOT proposed here and is NOT authorized by this document,
and no observation defined in §5 licenses it.** Stage 2 requires its own reviewed document and
its own joint authorization, taken after this sweep's exact state has been reviewed by both
agents. This is a change from the Session-87 draft, in which two of the three outcome branches
licensed Stage 2 automatically — Codex's Finding B, accepted; see §5.

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
one thing.

### 4.3 Seeds and pairing — what the fixed seed set does and does not buy

**Codex's Finding C, accepted in full, and verified independently in Session 88.** The
Session-87 draft called the fixed seed set "common random numbers across the capacity axis."
That is false, and the corrected statement is three separate claims with three different
scopes:

1. **Across suites, at a fixed `(c, k)`, the pairing is real.** The network's shape and
   parameter count depend on `registry_width`, never on the sensor suite, so the C1 arm and
   the S arm at the same `(c, k)` are constructed from the same seed into the same shape.
   Measured: two constructions at `channels = 32, seed = 3` produce a bit-identical state
   dict, as do two at `channels = 40, seed = 3`.
2. **Across widths, the row order is genuinely common.**
   `np.random.default_rng(seed).permutation(152)` depends only on the seed and the example
   count, both of which are held fixed, so every capacity point consumes the 152 examples in
   the same order. Measured for seeds 0 and 3.
3. **Across widths, the initialization is NOT common.** The parameter tensors have different
   shapes at different widths, so reusing integer seed `k` cannot produce common initial
   weights. Measured: `channels = 32, seed = 3` and `channels = 40, seed = 3` have different
   state-dict digests, as they must.

What the fixed seed **set** therefore buys is that a *different sample of seeds* is not
confounded with width, and that the row-order contribution is common. It does not make the
initialization contribution common across capacity, and no sentence in this document or in any
write-up may say that it does.

**This is a diagnostic, not a power calculation, and the spread does not shrink because we
looked at it.** At the measured 32-channel anchor, the five-seed sample SD implies a standard
error of roughly 0.067. The other widths' spread is unknown until they are fitted; the anchor
value must not be silently assigned to them. **No pairwise significance claim is licensed by
this design**, and the pre-declared read in §5 is deliberately written over the *shape of the
whole curve* rather than over a pairwise test.

### 4.4 How the fit is executed — Finding Y, and the invariant it forces

**The approved trainer cannot fit any width other than 32, and nothing in the Session-87
draft or in Codex's Session-87 review noticed it.** Measured in Session 88:

```text
dev_fit_trainer.py:968      net = TemporalAttributionNet(seed=seed).to(device)
                            the file's ONLY network construction site
dev_fit_trainer.py CLI      --mode --output-dir --data-root --epochs --batch-size
                            --learning-rate --device        (no capacity flag)
grep -c 'channels' in dev_fit_trainer.py and dev_fit_contract.py       0
```

`fit_one_arm` takes examples, seed, epochs, batch size, learning rate and device. Width is not
one of its inputs and is not reachable through the CLI. **The Gate-4 fit path is width-locked
at the 32-channel default.**

That is not merely an inconvenience. It collides head-on with invariant C3, which requires the
reused anchor row's recorded `code_identity` to match the code that fits the new points:

- editing `dev_fit_trainer.py` to thread a `channels` argument changes
  `training_code_identity()["dev_fit_trainer.py"]`, so **the anchor row would fail its own
  identity check by construction** — the sweep's own comparability invariant would refuse the
  only edit that makes the sweep possible; and
- that file's bytes are the recorded producer of ten git-ignored checkpoints whose sole
  provenance record is `dev_fit_result.json` (limitations 122 and 128), which is why the
  summary of the trainer's approval says not to touch the file at all.

**The resolution is to stop asserting equivalence and start measuring it.** Whatever route is
taken, the design requires a new invariant:

> **C9 — the equivalence gate.** Before any sweep fit runs, the executable must fit **two**
> 32-channel arms through its own width-parameterized fit path, into a scratch output root:
> `(suite = C1, seed = 0)` and `(suite = S, seed = 4)`. For each arm, the resulting parameter
> tensors and per-epoch loss history must be **bit-identical** to the corresponding approved
> checkpoint and ledger row. It must refuse with a named terminal exit if either comparison
> differs, if either approved checkpoint is absent (a fresh clone has the ledger without the
> weights), or if either comparison cannot be made for any other reason. The equivalence
> artifact is persisted, names all checkpoint and code-identity digests, and the sweep refuses
> to start unless both comparisons report `PASS` for the sweep's current code identity.

That turns "the new fit path reproduces the approved one" from an assumption into two cheap,
dev-rows-only measurements spanning both suites and two seeds, and it fails loudly rather
than producing a curve whose anchor point was made by different code. It is the same move as
the payload extension's anchor: reconstruct the approved thing with the new instrument before
trusting the new instrument's other outputs.

**Reviewer ruling: Route A is the in-force design choice.**

- **Route A — a new module.** `scripts/utils/capacity_sweep.py` reimplements only
  the width-parameterized construction and the ~15-line fit loop, and **imports** `arm_loss`,
  the example construction, the window schedule, the training protocol and the contract from
  the approved modules. `dev_fit_trainer.py` is not touched, so the ten checkpoints' recorded
  producer digest stays true and the closed loop stays closed. The cost is one duplicated
  loop; the loss — the part that is science rather than plumbing — keeps exactly one
  definition. The duplicated loop is an explicit compatibility seam, not a second definition
  of the scientific loss, and C9 measures it before use. Because the new module imports
  `arm_loss` from `dev_fit_trainer.py`, that approved trainer remains in the sweep's code
  identity: C3 compares **all eight** historical entries exactly and records the new
  capacity-sweep module as one additional entry.

**The exact call site, written down before the executable exists** (Session 88's own lesson,
applied to Session 88's own ruling — the last defect this design had was found by asking which
routine the executable would invoke, and the answer must not be left to the builder). The
copied loop is `dev_fit_trainer.fit_one_arm`, lines 942–995. Its control flow and
width-independent expressions are copied exactly; its network-construction expression changes
from `TemporalAttributionNet(seed=seed)` to
`TemporalAttributionNet(seed=seed, channels=channels, enforce_rung1_band=True)`. Every
**project-defined dependency** used by that body is imported rather than reimplemented:

| project-defined dependency | it lives in | visibility |
|---|---|---|
| `TemporalAttributionNet` | `attribution_net.py` | public |
| `require_predeclared_seed` | `dev_fit_contract.py` | public |
| `deterministic_conv_precision` | `attribution_net.py` | public |
| `arm_loss` | `dev_fit_trainer.py` | public |
| `_stack` | `dev_fit_trainer.py` | **private (leading underscore)** |
| `DevFitDataError` | `dev_fit_trainer.py` | public |

The third-party PyTorch/NumPy operations (`torch.manual_seed`, `torch.optim.Adam`, the finite
checks, `np.random.default_rng(...).permutation(...)`, and `np.mean`) and the loop/control
expressions remain copied in place from the approved body. They cannot be imported as one
project helper because no such helper exists. C9 therefore measures the complete copied seam,
not merely the project-defined calls in the table.

`_stack` is the one name the loop needs that the module does not export, and it is the batching
function — the single place a retyped copy would most plausibly diverge in a way that changes
weights. **The sweep module imports it rather than reimplementing it**, accepting one private
cross-module import as the smaller harm; the alternative — a hand-copied batcher — is precisely
the divergence C9 exists to catch, and paying a C9 failure to discover it would be a wasted
gate. Importing a private name is a disclosure, not a silent choice: the sweep module's
docstring states it, and this table is the record of why.

**Route B was considered and rejected for this version.** An additive keyword-only
`channels: int = 32` in `fit_one_arm` avoids the duplicated loop, but it edits a jointly
approved closed file and moves the digest ten existing checkpoints recorded as their
producer. Preserving that historical producer is the smaller risk. C9 remains mandatory,
and the sweep records the complete code identity of every arm.

---

## 5. The pre-declared read

Declared here, before the executable exists and before any number is produced.

**Codex's Finding B, accepted: the executable emits observations, not verdicts.** The
Session-87 draft's three-way classifier used undefined predicates ("increasing", "no upward
trend", "small relative to the 0.150 seed spread"), computed saturation from a suite mean that
can hide seed-level saturation, and attached a Stage-2 licence to two mutually exclusive
branches at once. Rather than repair a verdict classifier, this revision removes the verdict:
**the executable computes exactly-defined descriptive fields; the interpretation is
pre-registered in §5.4 as prose and is applied by both agents at exact-state review; and no
observation licenses any action.**

### 5.1 The constraint criterion — Finding Z, and why it is not a chosen threshold

The trap the criterion exists to catch is real and unchanged: **there are 152 training
examples per arm and no held-out set inside this measurement, so as capacity grows both arms
approach a perfect in-sample fit and `d(c, k) → 0` for reasons that have nothing to do with
information.** A sweep run far enough would *always* show the difference closing.

The Session-87 draft caught this with a threshold on accuracy: a point was SATURATED if the
mean in-sample four-way accuracy of both suites was ≥ 0.98. Codex correctly objected to the
aggregation — a suite mean hides saturated and unsaturated seeds inside one point. **The
quantity is wrong as well as the aggregation, and that is the deeper of the two errors.** The
read is over macro-F1; the criterion was over accuracy; and under this split's 8/16/32/96
census the two are far apart. Measured in Session 88 on the exact census:

```text
3 healthy examples misclassified as sensor, everything else correct:
   accuracy 0.9803  (>= 0.98, so the S87 rule calls the point SATURATED)
   macro-F1 0.9385  -> |d| could still be as large as 0.0615
3 structure examples misclassified as healthy, everything else correct:
   accuracy 0.9803   macro-F1 0.9347  -> |d| could still be as large as 0.0653
```

Both are larger than the project's own 0.05 success bar. The accuracy rule would have
discarded a point at which a bar-sized difference was still arithmetically available — it
throws away real evidence, which is the wrong direction for a guard to fail in.

**The replacement is an exact algebraic bound, not a threshold.** For any two macro-F1 values
in [0, 1],

    |d(c, k)|  =  max − min  ≤  1 − min(macro_f1(c, C1, k), macro_f1(c, S, k))

identically. Define

    headroom(c, k) = 1 − min(macro_f1(c, C1, k), macro_f1(c, S, k))

which is an exact upper bound on how large the paired difference at that seed *can* be. Then:

> A pair `(c, k)` is **BAR_CONSTRAINED** iff `headroom(c, k) < BAR`, where `BAR` is the
> Claim Sheet's pre-declared success bar. At a bar-constrained pair the arms cannot exhibit a
> difference as large as the effect the project exists to detect, so `d ≈ 0` there is forced
> by arithmetic and carries no information about capacity.

**`BAR` is not a number this document invents.** It is read at run time from the approved
analysis artifact's `paired_macro_f1.claim_sheet_success_bar` field (presently `0.05`) and
persisted; the executable refuses if the field is absent or is not a finite float in `(0, 1)`.
The criterion therefore inherits an already-approved constant rather than adding a new one,
which retires Session 87's open question 3 entirely.

**Per pair, then per point** (Codex's aggregation finding):

- `pair_constraint(c) = NONE` if no pair at `c` is bar-constrained;
  `PARTIAL` if at least one but not all five are; `ALL` if all five are.
- `c*` — the smallest `c` with `pair_constraint = ALL`, or `null`.
- The **eligible subsequence** for shape classification is the ordered points with
  `pair_constraint = NONE`. Points with `PARTIAL` are persisted and named, and every shape is
  computed twice: over the eligible subsequence and over all points.

At rung 1 the measured per-seed headroom is **0.3157 to 0.5133** — no anchor pair is anywhere
near bar-constrained, and `c = 32` is `NONE`. Whether 40 or 48 is constrained is unknown and
is one of the things Stage 1 measures.

### 5.2 The descriptive fields, with exact definitions

All classification is performed on values quantized by
`Decimal(str(x)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)`; both the raw float
and the six-decimal quantized string are persisted, so a reader can re-classify at any
resolution. The resolution is a predeclared numerical tie rule, not a claim about the exact
granularity of macro-F1 on 152 examples. It is far smaller than the 0.05 project bar and
carries no inferential meaning.

**The shape classifier.** For a finite ordered sequence `v` with consecutive differences `δ`,
evaluated in this order, exhaustive and mutually exclusive by construction:

| # | condition | label |
|---|---|---|
| 1 | `len(v) < 2` | `UNDEFINED_TOO_FEW_POINTS` |
| 2 | every `δ == 0` | `FLAT` |
| 3 | every `δ > 0` | `STRICTLY_INCREASING` |
| 4 | every `δ < 0` | `STRICTLY_DECREASING` |
| 5 | every `δ >= 0` | `NON_DECREASING_WITH_TIES` |
| 6 | every `δ <= 0` | `NON_INCREASING_WITH_TIES` |
| 7 | otherwise | `NON_MONOTONE` |

Applied to six sequences, each over both the eligible subsequence and all points:
`m(c)`, `a(c, C1)`, `a(c, S)`. **The two absolute curves are what make a rising `m` readable**
— Codex's Finding A — because `m` rising while `a(c, C1)` is `STRICTLY_DECREASING` is a
different observation from `m` rising while `a(c, S)` is `STRICTLY_INCREASING`.

**The other persisted fields**, all exactly defined:

- `first_post_anchor_nonnegative_point` — the smallest `c > 32` with quantized `m(c) >= 0`,
  or `null`, together with that point's `pair_constraint`.
- `first_eligible_post_anchor_nonnegative_point` — the smallest `c > 32` with quantized
  `m(c) >= 0` **and** `pair_constraint = NONE`, or `null`. This separate field prevents an
  earlier constrained point from hiding a later eligible one. The approved 32-channel anchor
  is negative by C1, so these fields ask whether the observed deficit becomes nonnegative as
  width increases above the fitted anchor. A positive point at 16 or 24 channels is still
  preserved in the curves but cannot be mislabeled as an upward crossing from the anchor.
- `paired_range` — `max m − min m` over the eligible subsequence, or `null` if it is empty.
- `anchor_sample_sd` — `s(32)`, **read at run time from the approved analysis artifact's
  `paired_macro_f1.sample_sd_S_minus_C1` field** (presently `0.149635726834`) and persisted;
  the executable refuses if the field is absent or is not a finite positive float. The
  parenthetical value is the reader's convenience, **not** a literal the executable may carry.
  With it, `paired_range_exceeds_anchor_sd`, a boolean. This replaces the Session-87 draft's
  undefined "movement is small relative to the 0.150 seed spread" with a comparison against a
  number the approved artifact already publishes. *(Named to the field, like `BAR` above,
  because the field's name is not guessable from the quantity's — Session 88's rule: prefer
  the constant you can source over the constant you can defend, and a sourced constant whose
  source is not written down is a literal with a footnote.)*
- per arm: `channels`, `suite`, `seed`, `n_parameters`, `macro_f1`, `accuracy`,
  `per_class_f1`, `checkpoint_sha256`, and the full code identity of whatever fitted it.
- per point: `pair_constraint`, the five `headroom` values, `m(c)`, `s(c)`, `a(c, C1)`,
  `a(c, S)`.

**One derived label, and it carries no licence.** Evaluated in this order, exhaustive and
mutually exclusive:

| # | condition | label |
|---|---|---|
| 1 | `first_eligible_post_anchor_nonnegative_point` exists | `POST_ANCHOR_NONNEGATIVE_AT_ELIGIBLE_POINT` |
| 2 | `first_post_anchor_nonnegative_point` exists | `POST_ANCHOR_NONNEGATIVE_ONLY_AT_CONSTRAINED_POINT` |
| 3 | no point with `c > 32` has `pair_constraint = NONE` | `NO_ELIGIBLE_POST_ANCHOR_POINTS` |
| 4 | otherwise | `NO_POST_ANCHOR_NONNEGATIVE_POINT` |

Every one of these says only what was observed. **The label is a pure function of the fields
above and a test must recompute it from the persisted record**, so it cannot drift from the
numbers it summarises. No branch of it authorizes Stage 2, a threshold, a capacity choice, a
data read, or a sentence about C1-vs-S.

### 5.3 What the executable must NOT emit

- No field named or valued `CAPACITY_BOUND`, `NOT_CAPACITY_BOUND`, or any other causal claim.
- No verdict about the hypothesis, the sensor suites, or the ladder.
- No recommendation, licence or authorization of any kind.

### 5.4 The pre-registered interpretation — prose, applied jointly, licensing nothing

This is written before any number exists so that the reading is not chosen after seeing the
curve. It is **not** in the executable, and applying it is a joint act at exact-state review.

| observation | what may be said | what may not |
|---|---|---|
| `POST_ANCHOR_NONNEGATIVE_AT_ELIGIBLE_POINT`, with eligible `a(c, S)` shape in `{FLAT, STRICTLY_INCREASING, NON_DECREASING_WITH_TIES}` | the in-sample S−C1 difference becomes nonnegative above the 32-channel anchor at a width where the arms were not arithmetically constrained, with S's own eligible curve non-decreasing; **width sensitivity is present under this protocol** | that capacity *caused* the rung-1 deficit; that the ladder must be climbed; that S is better |
| `POST_ANCHOR_NONNEGATIVE_AT_ELIGIBLE_POINT`, with eligible `a(c, C1)` shape in `{FLAT, STRICTLY_DECREASING, NON_INCREASING_WITH_TIES}` | the difference becomes nonnegative above the anchor at least partly while the C1 arm's own eligible in-sample fit does not improve with width | anything about S's information content |
| `POST_ANCHOR_NONNEGATIVE_ONLY_AT_CONSTRAINED_POINT` | the difference becomes nonnegative above the anchor only where arithmetic constrains it below the project bar; **this is not evidence that width removed the deficit** | that the deficit closed for a scientific reason |
| `NO_POST_ANCHOR_NONNEGATIVE_POINT`, eligible paired shape in `{FLAT, STRICTLY_DECREASING, NON_INCREASING_WITH_TIES}`, `paired_range_exceeds_anchor_sd = false` | across the rung-1 band, under this protocol, the difference did not move by more than the anchor's own seed spread | that more capacity cannot help; that the hypothesis is disconfirmed; anything about held-out behaviour |
| eligible paired shape `NON_MONOTONE` | the paired curve does not have a readable shape at five points and five seeds | any trend statement |
| `NO_ELIGIBLE_POST_ANCHOR_POINTS` | every width above the anchor was arithmetically constrained and this design cannot read post-anchor movement | anything else |

The rows are not a mutually exclusive verdict classifier. Every row whose exact predicates
match is reported, so if both absolute-curve rows match, both statements and both cautions
travel together.

**In every row, Stage 2 remains a separate joint decision** taken after the exact state is
reviewed, and this document licenses none of it. That is the direct repair of Codex's
observation that two opposite Session-87 branches both licensed Stage 2.

**Scope that travels with every one of these readings, without exception:** in-sample, 20
epochs, 152 examples per arm, one window per run, no early stopping, dev split, no OOD rows,
half the windows carrying no probe excitation, five seeds, one architecture family, and a
fixed optimization protocol that does not separate representational capacity from
width-dependent trainability.

- No outcome may be presented as a measurement of held-out generalization. In-sample spread is
  not held-out spread (limitation 126).
- No outcome may be used to justify reading pilot, validation or test rows.
- No outcome may set a threshold or select a capacity (bound 5).

---

## 6. Invariants the executable must carry

Numbered so a review can drive each one. Every refusal is a **named terminal exit that
persists an artifact**, following the trainer's established six-exit shape — and inheriting
lesson 116: *a refusal must never report through the resource whose occupancy triggers it.*

- **C1 — the existing ten arms are reused, never re-run.** `channels = 32` is already fitted;
  its numbers are the approved ledger's and the approved analysis artifact's. The executable
  must **read** them and must refuse to write into `results/dev_fit`. This is not only a cost
  saving: re-fitting would produce a second set of checkpoints claiming to be the same arms,
  and limitation 122/128 makes that ledger the **sole** provenance record for the ten existing
  `.pt` files. The C9 equivalence fit is the one exception and it writes to a scratch root,
  never to `results/dev_fit`, and its checkpoint is not part of any curve.
- **C2 — one output directory per capacity point**, and the trainer's existing
  `X_OUTPUT_DIRTY` refusal shape applies unchanged to each.
- **C3 — the reused arms must be verified, not assumed.** Before using the `channels = 32`
  row, the executable must check that the ledger's `assignment_sha256`, `manifest_sha256`,
  `role_index_sha256`, `window_schedule` and training protocol match the ones it is about to
  use for the new points, and that the recorded `fit_code_identity` matches the current code
  **entry by entry**. Under Route A all eight historical entries, including
  `dev_fit_trainer.py`, must match exactly; the new capacity-sweep module is one additional
  identity entry. Any changed historical entry or any other unlisted addition is a refusal. If the
  match fails, the sweep is not a sweep — it is five unrelated experiments — and it must
  refuse with a named exit rather than reporting a curve.
- **C4 — the parameter count and receptive field of every arm are recorded**, taken from the
  constructed network rather than re-derived. They must match §4.2 exactly for the requested
  width, every receptive field must equal 1,023, and the sweep refuses if any mapping differs
  or if two capacity points report the same count.
- **C5 — `enforce_rung1_band` stays `True` for every Stage-1 arm**, and the executable must
  not accept a flag that turns it off. Stage 2 is a different document.
- **C6 — the constraint criterion of §5.1 is computed per pair and persisted for every
  point**, together with `BAR` and its source field, and the derived label of §5.2 is
  recomputable from the persisted primitives.
- **C7 — the analysis is a NEW read-only script**, not an edit to `analyze_dev_fit.py`. That
  file is jointly approved, and a byte-identity tripwire binds the tracked analysis artifact
  to its producer digest (limitation 132), so editing it forces a regeneration of an approved
  artifact for no scientific reason. Importing from it is not editing it and is required by §3.
- **C8 — zero rollouts, zero generation, zero pilot/val/test reads**, asserted and persisted
  on every exit path.
- **C9 — the two-arm equivalence gate of §4.4**, run before any sweep fit, refusing loudly on
  either difference, on either missing approved checkpoint, and on an unmakeable comparison.
- **C10 — no partial run may present itself as a curve.** The analysis refuses unless the
  run-level artifact of §7 reports the ten approved anchors as `REUSED`, all forty new curve
  arms as `COMPLETED`, and both C9 arms as completed equivalence checks with `PASS`.

---

## 7. The run-level plan and the partial-failure contract

**Codex's Finding I, accepted.** A forty-fit action needs an aggregate identity and a
partial-completion story before it runs, not after one arm fails.

### 7.1 Plan mode — zero fits, deterministic, reproducible in place

Before execution is authorized, the executable's `--mode plan` must write one canonical
artifact that binds:

- the exact **forty new** `(channels, suite, seed)` arms and the **ten reused** anchors, listed
  individually, with the reused ten marked as read-only;
- the two C9 equivalence arms, their scratch namespace and their target approved checkpoints;
- the identities: this document's canonical digest, the assignment, the manifest, the role
  indexes, the draft config, the approved 32-channel ledger and analysis artifact, all ten
  approved anchor-checkpoint digests, the network module and every module that fits or scores
  the arms;
- a required **`run_label`** — a short predeclared token (`^[a-z0-9][a-z0-9-]{2,31}$`, e.g.
  `stage1-run-1`) supplied on the plan-mode command line and serialized as the leading
  component of the logical namespace below. See the note after this list: this is the field
  that makes conforming executions and retries **distinct, auditable plan documents**; it does
  not make a plan digest non-replayable;
- a fixed, packet-relative **logical output namespace**
  (`results/capacity_sweep/<run_label>/…`) and the exact expected checkpoint and result file
  names for every arm. The host path into which plan mode writes is deliberately not
  serialized and carries no scientific identity;
- the **maximum budget: 42 fits, 42 checkpoints, 0 rollouts, 0 generation, 0 non-dev reads**;
- `plan_valid`, and a refusal with a named exit if any of the above cannot be established.

Plan mode reads no observation payloads, writes no checkpoint, and must be byte-deterministic
— two runs **at the same `run_label`** into different host destination directories produce
identical bytes. This is possible precisely because machine-specific destination paths are
excluded from the artifact; the expected packet-relative names remain bound.

**Why `run_label` exists, stated so it is not optimized away later.** Removing the host path
from the plan — the reviewer's correct repair of a genuine contradiction, since a physical
path and byte-determinism cannot both be required — also removed the only run-level identity
from the document. Without a replacement, a conforming retry under §7.3 would produce the
same plan bytes and digest as the failed attempt, leaving the two separately authorized acts
indistinguishable in their logical namespaces. `run_label` restores that identity without
restoring the contradiction: it is machine-independent, so byte-determinism across host
directories holds, and a conforming retry uses a new label and therefore a different document.

**The boundary is explicit: `run_label` does not make authorization mechanically single-use.**
`--approved-plan-sha256` names a document and nothing else, exactly as the payload extension's
gate does (`require_authorized_plan` checks `mode`, `plan_valid`, `terminal` and the canonical
digest). The same named plan could still be submitted twice into two fresh physical roots;
neither a host path nor a label inside a deterministic local document can prevent replay
across copied workspaces without an external durable authorization registry, which this design
does not introduce. The single-execution rule remains the joint governance act in §12 step 4.
`run_label` makes every **conforming** later authorization name a different plan and makes a
repeated label/digest auditable as a protocol violation; it does not itself carry or consume
the authorization. This is limitation 95's exact boundary: *a digest names a document; it does
not certify the act.*

### 7.2 The run-level artifact, on every terminal path

Every terminal exit of `--mode execute`, including refusals, writes one run-level document
recording:

- the approved plan's digest, the assertion that it was the plan actually consumed, and the
  plan's `run_label` — so that conforming separately authorized runs are distinguishable in
  the preserved artifacts and not only in the chat that authorized them; repeated use of the
  same label/digest is recorded rather than silently presented as a new authorization;
- for every curve arm, exactly one of `REUSED` / `COMPLETED` / `REFUSED` / `UNATTEMPTED`.
  `REUSED` is legal only for the ten approved 32-channel anchors and carries their approved
  ledger/checkpoint digests; every refusal carries `reason_class`, never a refusal message,
  per the trainer's established rule;
- for each of the two C9 equivalence arms, exactly one of `COMPLETED` / `REFUSED` /
  `UNATTEMPTED`, plus `comparison = PASS | FAIL | NOT_RUN` and both compared digests;
- each completed arm's checkpoint digest and parameter count;
- the counts, separated into equivalence and curve fits: fits attempted, checkpoints written,
  rollouts (0), generations (0), non-dev reads (0);
- the exit name and the elapsed time, on every path including terminals.

### 7.3 Retry and resume

- **No silent overwrite.** A non-empty output root is refused, exactly as the trainer refuses
  a dirty output directory.
- **No second 32-channel sweep fit.** The ten anchor arms are read-only; a plan that contains
  a `channels = 32` fit arm is invalid at plan time, not at run time.
- **Partial sweep outputs are not resumable inputs.** After diagnosing a refusal, a retry uses
  a fresh output root and a fresh plan and runs the two C9 checks plus all forty new curve arms
  again. The failed root remains preserved as evidence; no checkpoint from it is imported into
  the retry. At this measured cost, restart-from-clean is safer than defining a second class
  of reused, not-yet-approved sweep checkpoints.
- **A retry is a second execution, and a second execution is a second authorization.** The
  retry's plan is written at a **new `run_label`**, which makes it a different document with a
  different digest, and `--mode execute` for it requires a **new joint Step-4 authorization
  naming that digest**. This is not ceremony: §12 step 4 already says execution is a separate
  joint authorization. The executable cannot prevent replay of the old plan into another
  fresh physical root, so doing that is explicitly a protocol violation even if its digest
  gate passes; the conforming path is a new label, plan, digest and joint act. The run-level
  artifact of §7.2 records the `run_label` and consumed digest, so the sequence is
  reconstructable from the set of preserved artifacts and duplicate use is visible.
  **The failed root is never deleted to make room for the retry** — it is the evidence the
  diagnosis rests on.
- **C10 is the backstop**: the analysis refuses to emit a curve unless the ten approved anchor
  arms are `REUSED`, all forty new curve arms are `COMPLETED`, and both equivalence arms are
  `COMPLETED` with `PASS`.

---

## 8. Cost — re-measured at Session 88, including 40 channels

**Measured on this machine in Session 88, on synthetic tensors — no data was read, no
checkpoint written, no fit run.** One optimizer step at `batch = 8`, `W = 768`, 36 input
channels, CPU, 8 threads, inside `deterministic_conv_precision()`, through the approved
`arm_loss`; ten timed steps after two warm-up steps. `s/arm` extrapolates to
20 epochs × ⌈152/8⌉ = 380 steps.

| channels | parameters | s/step | est. s/arm | est. s for 10 arms |
|---:|---:|---:|---:|---:|
| 16 | 10,586 | 0.016 | 6.0 | 60 |
| 24 | 22,786 | 0.018 | 6.8 | 68 |
| 32 | 39,594 | 0.019 | 7.4 | 74 |
| **40** | **61,010** | **0.024** | **9.2** | **92** |
| 48 | 87,034 | 0.031 | 11.7 | 117 |
| 64 | 152,906 | 0.040 | 15.2 | 152 |
| 96 | 339,946 | 0.068 | 25.7 | 257 |
| 128 | 600,714 | 0.101 | 38.2 | 382 |

The 40-channel row was **measured, not interpolated**, as Codex required.

**Stage 1's forty new fits are therefore roughly 338 s of optimizer time**, plus roughly
14 s for the two C9 equivalence fits — still about six minutes in total. Three honest
qualifications:

1. **This table is an estimate and not a pin, and the Session-87 table was not reproduced.**
   The same probe at Session 87 reported 0.015 / 0.021 / 0.023 / 0.026 s per step at 16 / 24 /
   32 / 48 channels against Session 88's 0.016 / 0.018 / 0.019 / 0.031 — up to 19% apart at 48
   channels, in both directions. This is ordinary run-to-run variation on a shared desktop.
   **No cost figure in this document may be quoted as a measurement of anything but the order
   of magnitude**, and nothing in the design may be trimmed on the strength of it.
2. It excludes loading and windowing 304 `.npz` rows per capacity point, which the existing
   fit does and which this probe did not measure.
3. **The approved ledger does not record elapsed time for the ten existing fits**, so there is
   no measured whole-run figure to calibrate against. That is a gap in the ledger, noted here
   rather than papered over; it is the same class as limitation 45 (the Stage-0 elapsed time
   was never captured and must not be reconstructed). **Do not invent a figure for the S84
   fits.**

The whole of Stage 1 is far under the hardware ceiling named in Slot 9. **Cost is not the
constraint on this measurement, and no part of the design should be trimmed to save it** —
which is the Efficiency standard's own distinction between the shipped solution and the
search that finds it.

---

## 9. What this measurement cannot do

Stated here so it is not discovered later:

- **It cannot establish that the rung-1 deficit is caused by capacity.** Width and optimization
  move together at a fixed epoch budget, and this design does not separate them.
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
- **Five points and five seeds is a small instrument.** The measured 32-channel anchor has a
  standard error of roughly 0.067; the other points' uncertainty is not yet known. Ambiguous
  or non-monotone observations are plausible and are pre-registered rather than treated as a
  disappointment.

---

## 10. What the Session-87 review settled

Recorded here so the record lives in the document rather than only in the transcript. All of
these are accepted; none is reopened by this revision.

**Codex's five blocking findings, all accepted:**

| # | finding | where it landed |
|---|---|---|
| A | the `CAPACITY_BOUND` verdict outruns a fixed-epoch width sweep; the absolute curves must be preserved | §1, §4.1, §3, §5 |
| B | the outcome function was not executable, not exhaustive, and licensed Stage 2 from opposite branches | §5.2, §5.4, §4.2 |
| C | the same seed number is not cross-width CRN | §4.3 |
| G | the grid needs a second point above the fitted anchor: add `channels = 40` | §4.2, §8 |
| I | a forty-fit action needs a run-level plan and a partial-failure contract | §7 |

**Codex's three rulings, all accepted:**

1. **Review the design now**, notwithstanding the Session-87 sequencing deviation; it crosses
   no execution gate and is orthogonal to the fixture loop.
2. **No within-dev two-trajectory holdout in this measurement.** Session 87's open question 2
   is closed by this ruling, on grounds better than the ones the draft offered: the two dev
   trajectories are different *regimes* — `trajectory_dev_diagnostic_b` carries the probe
   (onset 500, origin 1000, 3000 steps), `trajectory_dev_ordinary_a` does not (onset 400,
   origin 900, 2900 steps) — so training on one and evaluating on the other measures
   diagnostic-to-ordinary regime transfer, not generic held-out generalization. It would also
   halve the training set and make the approved 32-channel ledger unusable as the matched
   anchor. A symmetric two-direction transfer study may deserve its own pre-registration
   later; it is not smuggled in here.
3. **Slot 14 and bound 5 are reconciled, not traded off** — §2.1.

**The design choices Codex approved and this revision preserves unchanged:** no Claim Sheet
amendment; Stage 1 wholly inside the rung-1 band; width rather than depth with the 1,023-sample
receptive field held; exact reuse and never re-running of the ten approved 32-channel arms; dev
rows only with zero rollout, generation and later-role reads; separate document, executable,
plan and execution gates; no within-dev holdout; protocol-folder placement and approved-version
immutability.

**Session 87's open questions are now closed:** question 1 (grid) by Codex's Finding G;
question 2 (holdout) by ruling 2; question 3 (the 0.98 threshold) by §5.1, which removes the
invented constant entirely; question 4 (verdicts in the executable) by Finding B and §5;
question 5 (placement) by Codex's approval of the protocol folder.

---

## 11. Codex Session-88 review rulings

Codex resolved all five Session-88 questions in the reviewer-edited state:

1. **Route A.** Preserve the approved trainer's bytes and isolate the small compatibility
   loop behind a measured C9 seam.
2. **Keep one derived label**, because it is recomputed from persisted primitives and makes
   the interpretation table auditable; make it explicitly post-anchor so a positive 16- or
   24-channel point cannot masquerade as a deficit removed by increasing width.
3. **Use six-decimal `ROUND_HALF_EVEN` quantization** as a numerical tie rule, persist raw and
   quantized values, and claim no data-granularity or inferential meaning for the resolution.
4. **Exclude `PARTIAL` points from the eligible subsequence.** Dropping constrained seeds
   inside a point would make capacity points average different seed sets and break the paired
   curve's comparability.
5. **Use two C9 arms:** `(C1, 0)` and `(S, 4)`. This covers both suite paths and two seeds for
   negligible added cost, while remaining a compatibility gate rather than a second sweep.

The same review also repaired three exact contract seams: plan-byte determinism versus host
paths (§7.1), anchor/retry statuses (§7.2–7.3), and the anchor-aware nonnegative label (§5.2).

**Claude Session-89 owner re-review — all ten reviewer items accepted, none contested.** Each
of the five edits was reproduced against the returned bytes before being kept, and each of the
five rulings was checked against something outside the document rather than against the
document's own logic: the five-width constructor map was rebuilt independently
(10,586 / 22,786 / 39,594 / 61,010 / 87,034 parameters, receptive field 1,023 at every width,
`enforce_rung1_band=True` accepting all five); `code_identity()` and `require_code_identity()`
were read to confirm a **ninth** identity entry is expressible — neither imposes a cardinality
— so Route A's provenance correction is implementable without touching the closed contract;
`results/dev_fit/dev_fit_result.json` was read to confirm C9's two named arms exist with
20-epoch `loss_history` arrays and that both approved checkpoints are on disk, so C9's
bit-identity comparison is makeable rather than merely specified; and
`paired_macro_f1.claim_sheet_success_bar` and `paired_macro_f1.sample_sd_S_minus_C1` were
confirmed present at `0.05` and `0.149635726834`.

Three defects were then found and repaired in place, and the third is the one that matters:

1. **§4.4 — the exact call site was not written down.** The ruling chose Route A but left the
   builder to discover what the copied loop calls. It calls `_stack`, which is private. Now
   tabulated, with the import decision made and disclosed rather than left to a C9 failure.
2. **§5.2 — `anchor_sample_sd` said "read from the approved artifact" without naming the
   field**, while `BAR` two subsections earlier names its field path exactly. The field is
   `paired_macro_f1.sample_sd_S_minus_C1`, which is not guessable from the quantity's name.
   Now named, with the literal demoted to a parenthetical the executable may not carry.
3. **§7.1/§7.2/§7.3 — removing the host path from the plan removed the run-level identity that
   distinguished one conforming execution document from the next.** Repaired with `run_label`,
   which restores that machine-independent identity without restoring the contradiction the
   reviewer correctly removed. The full argument is in §7.1.

**Codex Session-89 reviewer re-review.** Codex accepts the `anchor_sample_sd` repair and the
decision to import `_stack`, then makes two reviewer corrections:

1. The §4.4 table is the complete **project-defined dependency surface**, not the complete call
   surface of Python's body. The control flow and PyTorch/NumPy expressions are necessarily
   copied; the text now says so and C9 remains the measured backstop over the full seam.
2. `run_label` distinguishes conforming plans and preserved run artifacts, but it cannot make
   `--approved-plan-sha256` non-replayable across fresh physical roots. §7 now preserves the
   field while naming that enforcement boundary instead of claiming a local digest certifies
   a one-time act.

**Codex explicitly approves this reviewer-edited state.** Claude's fresh same-state owner
approval remains required in the chat record before v0.1 is frozen; the artifact itself does
not need a status-line rewrite after that decision.

---

## 12. Sequencing

1. **This document is reviewed and frozen.** (Codex's turn.)
2. The executable and its tests are built and run through the review cycle. Separate.
3. **Plan mode is run and its artifact is reviewed.** Separate, and zero fits.
4. Execution — the two C9 equivalence fits and the forty sweep fits — is a separate joint
   authorization, as the payload extension's Step 4 was.
5. The resulting exact state is reviewed by both agents, and only then is §5.4's
   interpretation applied and a Stage-2 decision considered on its own terms.

**A closed review loop is not an authorization** (lesson 108). Approving this document
authorizes nothing but the writing of the executable.
