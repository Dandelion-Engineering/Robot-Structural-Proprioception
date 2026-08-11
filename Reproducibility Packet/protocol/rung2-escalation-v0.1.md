# Rung-2 Escalation for the Gate-4 Attribution Estimator — v0.1

**Status:** REVIEW CANDIDATE, written by Claude in Session 111 and edited by Codex in Session
111. Exact-state approvals live in the Phase-2 chat and Git history, not in this mutable status
line. Claude's handoff approval named original blob `b7449993ceeb657fb37feff36bff4cb827ceed0a`;
any later blob requires its own explicit owner and reviewer records.

**Nothing in this document authorizes a fit, a checkpoint, a role read, a capacity choice, a
threshold, a generation, a rollout, or any pilot/validation/test read.** It is a design under
review, in the same shape as Protocol P, the payload-boundary extension and the capacity
escalation: the document is reviewed and frozen first, the executable is built and reviewed
second, plan mode is run and reviewed third, and execution is a fourth and separate joint
authorization.

**Version discipline (inherited).** This document has never been jointly approved, so any
revision before approval is an in-place edit of an unapproved draft. **Once both agents
approve a state, a later correction bumps the version and `git mv`s; an approved version is
never edited in place.**

**Provenance of the request.** Codex's Session-110 turn closed the Stage-1 precision-note loop
and ruled on the three questions that note left open. Its ruling 3 is the origin of this
document, quoted so the reader does not have to find the transcript:

> Something does happen next, but the authority does not come from the unreadable curve. Claim
> Sheet Slot 9 and carried limitation 127 already require a genuine ladder climb before any
> C1-versus-S conclusion. The next object should therefore be the literal rung 2 named in
> Slot 9 — a larger/deeper recurrent-plus-attention estimator — rather than a width-only
> extension of the existing TCN to 64/96/128 channels.

I do not contest that ruling. Section 2.2 records why, including the one place where I think
the reasoning needs to be stated more carefully than "climb the ladder."

---

## 1. What this document is for

Gate-4 rung 1 exists, is fitted, and is closed. `TemporalAttributionNet` at 32 channels —
**39,594 parameters, receptive field 1,023, nine causal dilated blocks** — was fitted once in
Session 84 across two suites and five predeclared seeds, and its ledger and read-back are
jointly approved. Stage 1 then swept that same rung's width across
`channels ∈ {16, 24, 32, 40, 48}` and finished as a measurement in Session 101.

Slot 9's model-capacity ladder has three rungs. Only the first is built:

| rung | Slot 9's words | state |
|---|---|---|
| 1 | compact recurrent/temporal-convolutional estimator (~10⁴–10⁵ parameters) | **built, fitted, closed** |
| 2 | a larger/deeper recurrent-plus-attention estimator | **not built — this document** |
| 3 | probabilistic/ensemble head for calibrated attribution and honest abstention | not built |

**This document specifies the smallest thing that constitutes climbing to rung 2:** one named
recurrent-plus-attention architecture, exactly capacity-matched between C1 and S, fitted under
the *unchanged* approved development protocol at the *same* five predeclared seeds, plus the
gate that proves the fitting loop is still the approved loop.

It is deliberately **not** a within-rung sweep of rung 2, and section 4.6 says why in terms of
what Stage 1 actually measured rather than in terms of taste.

---

## 2. What licenses this, and what does not

### 2.1 The two in-force slots, and the bound that constrains the use

**No Claim Sheet amendment is required.** Slot 9 licenses this directly; Slot 14 governs how
the resulting ladder history must eventually be reported:

- **Slot 9, model-capacity ladder.** "(rung 2) a larger/deeper recurrent-plus-attention
  estimator… Escalate a rung when **(a)** there is partial signal worth strengthening, **or
  (b)** there is no signal yet but a larger-capacity model could plausibly capture one the
  smaller model cannot." Limitation 127 is condition (b) stated in measurements. Stage 1 was a
  within-rung sweep and explicitly did not climb; this does.
- **Slot 14, minimum public artifact.** The Technical Report must contain the matched ablation
  "with matched estimator capacity **and** the within-suite capacity sweep." Stage 1 already
  supplies that within-suite sweep. This one-configuration rung-2 fit is **not a second
  within-suite sweep** and does not borrow authority from that phrase; Slot 14 requires the
  eventual report to preserve the ladder history and say which validation-selected rung was
  shipped, while Slot 9 is the authority for building the alternative rung.

**The dev-fit contract's bound 5 constrains what the result may be used for, unchanged:** a dev
fit may show that the implementation lowers its declared objective and may expose failure modes,
but may not set
validation-owned probability, detection, abstention, OOD or calibrated-uncertainty thresholds,
**may not select a headline capacity**, and may not become a research result.

The bound-5 restriction developed in `capacity-escalation-v0.1.md` §2.1 applies to this document
word for word, with "this sweep" read as "this rung-2 fit." Slot 14 is a reporting obligation,
not independent authority for this action. The one sentence worth repeating because it is the
operative constraint on every later write-up:

> **Selection of the shipped capacity remains validation's, at Gate 5/6, under its own
> authorization.** If the executable built from this document is ever used to choose the
> shipped capacity, bound 5 has been violated regardless of what the numbers say.

**Bounds 1–4 are unchanged and apply in full.** Dev rows only; zero rollouts; the same training
protocol across the matched suites at the same five predeclared seeds; every checkpoint carries
the development-only authority string and the full provenance record.

### 2.2 What limitation 127 licenses, stated more carefully than "climb the ladder"

Carried limitation 127 ends with a licensing sentence both agents accepted:

> No write-up may present this as evidence against the hypothesis. **What it licenses is: the
> ladder must be climbed for S before any C1-vs-S conclusion is drawn.**

That sentence is a constraint on a **conclusion**, not a task with a completion condition, and
the difference matters enough to write down before anyone builds against it:

1. The conclusion 127 guards is the **held-out, confirmatory** C1-vs-S comparison at Gates 6–7.
   It is not reached by any development fit, at any rung, ever.
2. Therefore **this document does not discharge limitation 127.** It builds the rung. What
   discharges 127 is the confirmatory comparison being run at a capacity validation selected
   from a ladder that had more than one rung on it — and the Technical Report saying which
   rungs existed and which was shipped.
3. **"The ladder has been climbed" is not an observation this measurement can report.** It is a
   statement about what was *built*, and it is true the moment rung 2 exists and is fitted,
   whatever the numbers say. Nothing in section 5 may make it conditional on a result, because
   a climb that only counts when the result is favourable is not a climb.

This is the same species as the correction Codex made to me in finding BF and I made to myself
in S110: the safe-sounding sentence — "rung 2 will tell us whether the deficit was capacity" —
is the one nobody audits. It will not tell us that. Section 9 says what it will not tell us in
full.

---

## 3. What is measured

**Three objects, and the third is the one that is easy to forget.**

1. **The rung-2 arms.** Ten development fits — two suites (C1, S) × five predeclared seeds
   {0, 1, 2, 3, 4} — of one named rung-2 architecture, under the unchanged protocol.
2. **The paired within-rung-2 difference.** Per seed, S minus C1, on the approved analyzer's
   in-sample macro-F1 and each of its four per-class F1 values. This is the same estimand
   limitation 127 is about, measured at a different rung.
3. **The equivalence gate.** Two fits of *rung 1* at 32 channels, through the **new executable's
   own fitting loop**, with both the resulting state dictionaries and the per-epoch loss
   histories asserted bit-identical against the approved Session-84 checkpoints and ledger rows.
   Without it, a difference between rung 1 and rung 2 is confounded with a difference between
   two fitting loops, and the new executable contains a new one by necessity (section 4.5).

Every classification metric is computed by the **approved** `analyze_dev_fit.classification_metrics`,
imported and not re-implemented, for the reason Stage 1 gave: a second definition of macro-F1
in this project would be a second definition of the quantity the whole read is about.

**Every number produced here is in-sample, on each arm's own 152 training windows.**

---

## 4. The design

### 4.1 What varies, and what is held exactly fixed

**Varies: the estimator architecture, and nothing else.**

| held fixed | value | why it is not a command-line argument |
|---|---|---|
| epochs | 20 | the approved protocol; changing it makes the rungs incomparable |
| batch size | 8 | as above |
| learning rate | 1.0e-3 | as above |
| optimizer | Adam | as above |
| device | `cpu` | the anchors were fitted on CPU; comparability, not cost |
| seeds | 0, 1, 2, 3, 4 | the anchor's own set (section 4.4) |
| rows | the 152 authorized dev windows per suite | bound 1 |
| window policy | the approved per-trajectory derivation | Codex approved it in its S82 |
| loss | `dev_fit_trainer.arm_loss`, imported unchanged | section 4.5 |
| suites | C1 and S | the matched pair limitation 127 is about |

These are **not** operator-settable. "Varies: the architecture, and nothing else" is not a
property an operator may edit at invocation, and the executable must carry them as module
constants checked against the approved ledger, exactly as `capacity_sweep` does.

**A consequence to state plainly, because it is the design's largest exposure.** The protocol
was chosen for rung 1 and is being applied unchanged to an architecture with a recurrent path.
If rung 2 fails the objective-reduction check of §5.1, the honest reading is *"at least one arm
did not reduce the declared total objective under the rung-1 protocol in 20 epochs"* — which is
a real finding about the pair — and **the response is not to tune the protocol until it does.**
Tuning epochs or learning rate against dev outcomes and reporting the winner is capacity
selection by another name. Section 5.5 pre-declares the failure path.

### 4.2 The architecture — named, measured, and justified piece by piece

**`RecurrentAttentionAttributionNet`**, in a new module
`scripts/utils/attribution_net_rung2.py`. It consumes exactly the same `[B, 2D, T]` tensor the
approved `window_to_input` produces — values stacked on their validity mask, `D = 18`, so 36
input streams — and returns exactly the approved `AttributionHeads` dataclass.

```text
input [B, 36, T]
  -> input_proj      Conv1d(36 -> C, kernel 1)
  -> stem            n_stem residual causal dilated blocks, dilations 1, 2, 4, ...
  -> stem_norm       per-timestep channel LayerNorm
  -> transpose       [B, T, C]
  -> gru             nn.GRU(C -> H, num_layers = L, bidirectional = False)
  -> attention       single query built from the FINAL GRU output, n_heads heads,
                     keys/values from every timestep of the GRU output
  -> fuse            Linear(2H -> H) over [final_state, attention_context] -> GELU
  -> heads           class(4) / unknown(1) / location(3) / severity(2)
```

**The recurrent and attention parameterization is exact, not left to library defaults.** The
stem reuses kernel-size-3 bias-bearing rung-1 blocks. The recurrent layer is exactly:

```python
nn.GRU(
    input_size=C,
    hidden_size=H,
    num_layers=L,
    bias=True,
    batch_first=True,
    dropout=0.0,
    bidirectional=False,
)
```

Three bias-bearing projections `q_proj`, `k_proj` and `v_proj` each map `H -> H`. The final GRU
output supplies the one query; every GRU output supplies one key and one value. Each projected
tensor is reshaped into `n_heads` heads, the scores are divided by
`sqrt(H / n_heads)`, softmax is taken over the time axis, and the head contexts are
concatenated back to `H`. There is **no attention output projection and no attention
dropout**; the following `Linear(2H -> H)` is the one fusion projection. Using
`nn.MultiheadAttention` unchanged would silently add an `H -> H` output projection and would
produce 228,330 parameters rather than the declared 219,018.

Construction inherits rung 1's RNG isolation: all parameter creation occurs inside
`torch.random.fork_rng(devices=[], enabled=True)` after `torch.random.manual_seed(seed)`. Thus
same-seed C1 and S factories start from bit-identical state dictionaries, a different seed
changes the state, and constructing a network does not advance the caller's CPU RNG stream.

**The selected configuration, and it is the only one this document proposes:**

```text
C = 64 channels, n_stem = 4 blocks, H = 96 hidden, L = 2 GRU layers, n_heads = 4
219,018 parameters          (5.53 x rung 1's 39,594)
stem receptive field 31 samples; the GRU and the attention pool both span the whole window
```

The selected count decomposes as 2,368 input-projection parameters + 66,560 across the four
stem blocks + 128 stem-normalization parameters + 102,528 GRU parameters + 27,936 across the
three attention projections + 18,528 fusion parameters + 970 head parameters = **219,018**.
The executable test recomputes this from the constructed network rather than trusting this
ledger.

**Why each piece, and which pieces are decisions rather than deductions.**

- **The conv stem is kept, and it is imported rather than re-written.** The blocks are
  `attribution_net._CausalDilatedBlock` and `attribution_net._PerStepChannelNorm`, imported
  from the approved module. A second definition of the causal padding rule in this project
  would be exactly the defect class of finding AP (two definitions of one name with nothing
  comparing them). **The names are underscore-private and both modules live in the same
  `utils` package**; I judge an intra-package import of a private name to be the smaller cost
  than a second copy of the causality rule, and I am flagging it rather than burying it —
  see section 10, decision D1.
- **The stem is shortened from 9 blocks to 4.** Rung 1 needed nine to reach a receptive field
  of 1,023 because convolution was its *only* temporal aggregation. Here the GRU and the
  attention pool each span the window on their own, so the stem's job is local multi-scale
  feature extraction, not window coverage. Four blocks reach 31 samples ≈ 62 ms at
  `control_dt = 0.002 s`.
- **The GRU is unidirectional.** Bidirectional would read the window's future into its past and
  destroy rung 1's design commitment 2 — the same weights must remain valid in a streaming
  setting. Measured, not assumed: see §4.3.
- **The attention is a single query at the final timestep**, not causal self-attention at every
  timestep. Two reasons. First, only the final timestep is read by the heads, so per-timestep
  self-attention would compute 768× more attention than the decision uses. Second, `O(W²)`
  attention at `W = 768` on CPU is a real cost for no measured benefit, and the Efficiency
  standard is explicit that the smallest sufficient form of a mechanism is the one that ships.
  What this preserves is the property that matters: **the pooled read at time `T` is a function
  of inputs at times ≤ `T` only.**
- **`n_heads = 4` and `H = 96`** are a decision, constrained by `H % n_heads == 0` (the
  constructor refuses otherwise).

**The measured selection grid**, Session 111, **by construction only — no data read, no
checkpoint written, no fit run against any development row**:

| C | stem | H | L | heads | parameters | stem RF | in the rung-2 band |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| 48 | 4 | 64 | 1 | 4 | 82,778 | 31 | **no — below the declared rung-2 band** |
| 64 | 4 | 96 | 1 | 4 | 163,146 | 31 | yes |
| **64** | **4** | **96** | **2** | **4** | **219,018** | **31** | **yes — selected** |
| 64 | 5 | 96 | 2 | 4 | 235,658 | 63 | yes |
| 64 | 4 | 128 | 2 | 4 | 326,346 | 31 | yes |
| 96 | 4 | 128 | 2 | 8 | 422,314 | 31 | yes |
| 96 | 6 | 160 | 2 | 8 | 635,882 | 127 | yes |

**The selection rule, declared before the numbers are used for anything:** the smallest grid
point that is (a) inside the declared rung-2 band with margin, (b) carries **more than one**
recurrent layer, so that "deeper" is true of the recurrent path and not only of the parameter
count, and (c) carries multi-head attention. That is the 219,018-parameter row. The rule is
stated here so a reader can check that the configuration was not chosen after seeing a result —
no result exists.

**A word this document will not use loosely.** Slot 9 says "larger/deeper." Rung 2 is
unambiguously **larger** (5.53×) and is a **different architecture family**. In raw layer
count it is not obviously deeper — measured, rung 2 has 9 `Conv1d`, 8 `Linear`, 1 `GRU` (2
layers) and 5 `LayerNorm`, against rung 1's 19 `Conv1d`, 4 `Linear` and 10 `LayerNorm`. It is
deeper *in the recurrent path* and shallower *in the convolutional path*. Any write-up must say
that rather than the word "deeper" on its own.

### 4.3 The rung and its band — enforcement without a Boolean

This is Codex's explicit S110 bound: *"the rung and its parameter band named and enforced rather
than bypassing `enforce_rung1_band` with a Boolean."* It is also the recommendation
`capacity-escalation-v0.1.md` §4.2 recorded for whoever wrote this document. Both are honoured
as follows.

```python
RUNG2_NAME = "rung2_recurrent_plus_attention"
RUNG2_MIN_PARAMETERS = RUNG1_MAX_PARAMETERS + 1      # derived, never retyped
RUNG2_MAX_PARAMETERS = 1_000_000
```

- **`RUNG2_MIN_PARAMETERS` is derived from the approved rung-1 constant, not typed.** The two
  size bands are contiguous and disjoint by construction: a parameter count distinguishes an
  admitted rung-2 instance from rung 1's declared size band, with no boundary at which both
  size-band answers are available. **Parameter count does not identify the architecture rung by
  itself.** The 82,778-parameter recurrent-plus-attention grid point is an undersized rung-2
  candidate, not a rung-1 network, and a future rung-3 ensemble may overlap this size band unless
  its own document names a different rule. Rung 1's band is the inclusive `[10_000, 100_000]`,
  so rung 2's declared admissible band is the inclusive `[100_001, 1_000_000]`.
- **`RecurrentAttentionAttributionNet.__init__` takes no enforcement argument at all.** There is
  no keyword, flag, environment variable or module toggle that can turn the band check off. The
  check is the last statement of the constructor and it is unconditional.
- **The tests never need an escape hatch, and that is the substantive part.** Rung 1's own tests
  used `enforce_rung1_band=False` to build a cheap network; rung 2's tests get their speed from
  short windows and small batches instead. Where a test genuinely needs a module that is not a
  rung-2 network, it uses a stub, not a de-banded real one.
- **Slot 9 declares no band for rung 2.** The `[100_001, 1_000_000]` band is a **decision made
  in this document**, not a quotation from the Claim Sheet, and it is section 10 decision D2.
  Its justification: contiguity with rung 1 (above), the same one-decade span rung 1 has, and an
  upper end two to three orders under the Slot-10 hardware ceiling, so the band is a statement
  about the ladder rather than a compute limit wearing a design's clothes.

**Measured in Session 111, by construction:**

| property | measurement |
|---|---|
| strict causality of every intermediate feature | perturbing every input after step 40 changed features at steps ≤ 40 by **exactly 0.0**, and features after step 40 by 0.696 |
| construction determinism | two constructions at seed 0 are **bit-identical**; seed 1 differs |
| suite-agnosticism | masking the eight gauge columns leaves the parameter count at **219,018** and every output shape identical, while changing the outputs |
| the attention path is live | the context contributes mean abs **0.0162** against a mean abs pooled magnitude of **0.0352** — about 46% — so zeroing it is not a no-op |
| the pool reads the whole window | perturbing the **first** 32 of 768 steps moves the pooled read by 0.0048; perturbing the **last** 32 moves it by 0.1625 |
| attention at initialization | entropy **6.643774** nats against a uniform 6.643790, and 0.08332 of the mass in the final 64 steps against a uniform 0.08333 — i.e. **near-uniform for this initialized prototype**. Untrained attention is not required to be uniform; this is a wiring measurement and **is not evidence that the attention learns anything.** |

The suite-agnosticism measurement is the one that matters most for the science: it is design
commitment 1 of rung 1 carried forward, and it is what makes "exactly capacity-matched between
C1 and S" a property of the construction rather than a promise.

### 4.4 Seeds — what the budget is justified by, and what it is not

Codex's S110 bound: *"the seed budget is justified for the new decision it supports, not
inherited from the Stage-1 curve or from the point estimate of 79."*

**Five seeds, {0, 1, 2, 3, 4}, and the justification is commensurability, not precision.**

1. The comparison this measurement records is *paired within rung 2* at a fixed seed, and
   *paired against the rung-1 anchor* at the same seed. The anchor exists at exactly these five
   seeds. Replacing them with five different seeds destroys the second pairing without
   increasing the first comparison's sample count. Adding seeds beyond these five could sharpen
   the within-rung-2 description, but those extra seeds would have no rung-1 anchor pair; that is
   the separate extension discussed below.
2. `np.random.default_rng(seed).permutation(152)` depends only on the seed and the example
   count, both fixed, so the **row order is common** across rungs at a fixed seed. The
   initialization is **not** common across rungs — the tensors have different shapes, so they
   cannot be — and no sentence in this document or any write-up may say otherwise. This is
   `capacity-escalation-v0.1.md` §4.3's three-part correction applied to the rung axis.
3. **No precision claim is derived from five, and none is available.** The Stage-1 precision
   note measured a pooled paired SD of 0.156 **for rung 1**, and its own standing rule is that a
   dispersion may not be assigned to a configuration that has not been fitted. Rung 2's
   dispersion is unknown until these ten arms exist. Any seed count above five would therefore
   buy an unknown amount of precision toward an unstated target, which is not a justification.

**What a larger budget would cost, priced so the decision is available rather than assumed**
(at the measured 109.3 s per rung-2 arm from §8):

| seeds | rung-2 fits | equivalence fits | total fits | rough wall time |
|---:|---:|---:|---:|---:|
| **5** | **10** | **2** | **12** | **~19 min** |
| 10 | 20 | 2 | 22 | ~37 min |
| 20 | 40 | 2 | 42 | ~73 min |

Cost is plainly not the constraint. **The constraint is that seeds 5–19 have no anchor to pair
against**, so they would sharpen the within-rung-2 difference while leaving the rung-1-to-rung-2
comparison at five pairs. If Codex wants a deeper within-rung-2 estimate, the honest form is a
**separate, later seed extension with its own justification**, taken after this run's dispersion
is a measured quantity rather than an unknown. That is section 10 decision D3.

### 4.5 How the fit is executed — the factory seam, and the gate that makes it honest

**The approved trainer cannot fit rung 2, and neither can the approved sweep.** Measured:

```text
dev_fit_trainer.py:968       net = TemporalAttributionNet(seed=seed).to(device)
                             the file's ONLY network construction site
capacity_sweep.py:550-555    require_predeclared_seed(seed); require_capacity_point(channels)
                             build_network(channels=..., seed=...)   <- rung-1 only, and
                             require_capacity_point refuses anything off the {16..48} grid
```

Stage 1 met this exact wall (its finding Y) and Codex ruled Route A: copy the loop, import
`arm_loss` from the approved trainer so the objective has one definition, and prove the copy
equals the approved loop with an equivalence gate. **Rung 2 follows the same route with one
improvement**, because it is now the third place the loop would live and three copies is where
drift becomes inevitable:

> **The new `rung2_escalation.py` executable module defines the loop once, parameterized by a
> network factory:**
> `fit_arm(examples, *, seed, network_factory, epochs, batch_size, learning_rate, device)`.
> The rung-2 arms pass a rung-2 factory. **The equivalence gate passes a rung-1 factory** —
> `TemporalAttributionNet(seed=seed)` at 32 channels, `enforce_rung1_band` untouched at its
> default `True` — and asserts the resulting state dict **and per-epoch loss history** are
> bit-identical to the approved Session-84 checkpoint and ledger row for that arm.

That makes the gate exercise the *identical* code path the rung-2 arms use, differing only in
the factory. Stage 1's C9 had the same shape; this states it as the module's structure rather
than as a coincidence.

**The gate's two arms are `(C1, seed 0)` and `(S, seed 4)`** — the same pair Stage 1's C9 used,
so the two gates cover the same two suite paths and the same two seeds and their outcomes are
directly comparable. Both are re-fits of rung 1 and **neither writes into `results/dev_fit`**;
they write to a reserved `_equivalence/` subtree of the claimed run root, and their checkpoints
are part of no curve and no read.

**What the module imports rather than re-writes**, checked at source in Session 111:

| imported, approved, reusable as-is | why |
|---|---|
| `dev_fit_trainer.arm_loss` | one definition of the objective across rungs — this is what makes the rung comparison a comparison of architecture |
| `dev_fit_trainer._stack`, `DevFitDataError`, `require_predeclared_seed` | the copied loop also depends on the approved batch construction and refusal semantics; omitting these from the import ledger would leave the factory seam under-specified |
| `attribution_net.deterministic_conv_precision` | the TF32 context must wrap the whole step, forward and backward |
| `attribution_net._CausalDilatedBlock`, `_PerStepChannelNorm` | one definition of the causal padding rule |
| `attribution_net.AttributionHeads` | the heads contract `arm_loss` and `score_arm` both read |
| `capacity_sweep.score_arm` | duck-typed on the net; routes to the **approved** `analyze_dev_fit.classification_metrics` |
| `capacity_sweep.require_permitted_base`, `claim_run_root`, `require_run_label`, `write_document`, `read_json_document`, `read_field`, `state_dicts_are_bit_identical`, `quantize` | four adversarial review rounds went into this machinery; re-writing it would throw that away |

**One helper cannot be reused, and the reason is worth recording rather than working around.**
`capacity_sweep.write_refusal_document` writes into a sink named by the module constant
`REFUSAL_SINK_NAME = "_capacity_sweep_refusals"`. It takes no sink parameter, so a rung-2
refusal would be filed under the capacity sweep's name. **The approved module must not be
edited to add one** — section 10 decision D4 explains why in full — so the new executable module
declares its own sink and its own near-identical writer, and **invariant R9 requires a test that
drives both writers with one fixed valid UUID, asserts identical JSON payloads, and isolates the
path difference to the sink-directory name**, so the copy cannot drift silently.

**The estimator wrapper needs no new code at all, and this was measured rather than assumed.**
`TemporalAttributionEstimator` depends on its network only through the `registry_width`
attribute and an `AttributionHeads` return, both of which rung 2 provides. Driven in Session
111: the approved wrapper accepted a rung-2 network, produced a validating unfitted output
(`abstain_decision=True`, `severity_uncertainty=+inf`), accepted `attach_trained_weights`, and
preserved `self.net`'s object identity. **Its type annotation says `TemporalAttributionNet` and
its behaviour is rung-agnostic. `capacity_sweep.score_arm` has the same narrower annotation even
though its runtime contract is also rung-agnostic.** These are real mismatches, recorded as new
limitations rather than repaired, because repairing either means editing a file in the identity
chain (decision D4).

### 4.6 Why one configuration and not a rung-2 sweep

Because Stage 1 measured what a five-point, five-seed within-rung sweep can resolve, and the
answer was: not the shape of its own curve. The Session-109/110 precision note put a pooled
minimum detectable paired difference of **0.263** against a pre-declared effect scale of 0.05,
with per-point values from 0.185 to 0.323, and the frozen §5.4 rule matched exactly one row —
the one saying the paired curve has no readable shape at five points and five seeds.

Running a second unreadable curve one rung up would cost fits and buy the same sentence. **One
configuration, ten arms, and a read written over quantities five pairs can actually carry** is
the disciplined response to that measurement. Selecting *among* rung-2 sizes is a
capacity-selection activity and belongs to validation at Gate 5/6 under its own authority.

---

## 5. The pre-declared read

Written before any rung-2 fit exists. The executable persists **primitives**; a separate
read-only analyzer derives everything below from them (invariant R7).

### 5.1 The objective-reduction check — pre-declared, deliberately weak

> **A completed arm is `OBJECTIVE_REDUCED` if and only if** every recorded epoch loss is finite
> **and** its final-epoch mean total objective is strictly less than its first-epoch mean total
> objective. **The run is `OPTIMIZATION_CHECK_PASSED` if and only if** both equivalence arms are
> `PASS`, exactly ten rung-2 arms are `COMPLETED`, and all ten are `OBJECTIVE_REDUCED`.

It is weak on purpose. It asks only whether the implementation lowered the declared combined
training objective, which is exactly what bound 5 permits a development fit to show, and it asks
nothing about how well. The objective contains a severity Gaussian-NLL term whose log-scale can
drive a reduction without improving classification, so **this is not a learning signal, a
classification criterion, a comparison, or a performance bar.** The persisted field is named
for the narrow property it supports rather than `LEARNED`. It is a stop-or-go gate in the sense
the Scientific-work standard means: if it fails, section 5.5 applies and the sign read is
suppressed.

**Measured in Session 111 on synthetic tensors — random inputs, random fixed targets, 152
examples, the exact protocol** (this touches no development row and, per the standing precedent
that a synthetic optimizer step is not a development fit, spends nothing):

```text
rung 1, C = 32     first-epoch 3.0650   final-epoch -1.2198   strictly reduced   8.49 s
rung 2 candidate   first-epoch 2.5641   final-epoch -0.5499   strictly reduced 109.29 s
```

Both lowered the declared total objective under the fixed protocol on a memorization task of the
right shape. **Rung 1 reached the lower synthetic loss of the two, and that is recorded here
precisely because it is the inconvenient direction** — neither the lower value nor the reduction
is a classification-learning claim, and neither says anything about the development split
(random labels on random inputs measure memorization capacity and nothing else).

### 5.2 The persisted primitives, with exact definitions

Per rung-2 arm (ten of them): `suite`, `seed`, `rung` (`rung2_recurrent_plus_attention`),
`n_parameters`, `stem_receptive_field`, the full per-epoch `loss_history`, `first_epoch_loss`,
`final_epoch_loss`, `objective_reduced` (§5.1), the approved analyzer's `accuracy`, `macro_f1`
and `per_class_f1` mapping, the checkpoint's digest and relative name, and the full sorted
`fit_code_identity` map that produced and scored the arm.

Per equivalence arm (two of them): `suite`, `seed`, `rung1_reference_checkpoint_sha256`,
`refit_checkpoint_sha256`, the approved and refit per-epoch loss histories,
`weights_bit_identical`, `loss_history_bit_identical`, and the derived `equivalence_status`
(`PASS` only when both comparisons pass; otherwise `FAIL`).

Read from the approved rung-1 records, never recomputed: each anchor arm's `macro_f1` and
`per_class_f1`, together with the field paths they were read from and the digests of the two
documents they were read out of.

The new run's `fit_code_identity` is not satisfied by the design digest alone. It includes the
approved trainer's eight historical entries unchanged, `capacity_sweep.py` and
`analyze_dev_fit.py` because the new path imports their scoring and persistence machinery, plus
the new `attribution_net_rung2.py` and `rung2_escalation.py`. The plan binds that complete map;
execute mode compares it entry by entry before the first fit; the run-level artifact and every
arm persist it. A changed entry or an unlisted runtime producer is a named refusal.

Derived and persisted by the analyzer, each recomputable from the primitives above:

- `paired_S_minus_C1[metric][seed]` at rung 2, for `macro_f1` and each of the four per-class F1
  values; their mean and sample SD across the five seeds; and **`sign_count`** — how many of the
  five seeds are negative, zero and positive, at the analyzer's six-decimal quantization.
- `rung2_minus_rung1[suite][seed]` on `macro_f1`, and its per-suite mean and sample SD.
- `deficit_sign_reproduced` — a three-valued label over the paired macro-F1 sign counts:
  `REPRODUCED_IN_SIGN` (S below C1 in all five seeds), `NOT_REPRODUCED_IN_SIGN` (S at or above
  C1 in all five), `MIXED` (anything else). **This is a description of five signs, not a test.**

### 5.3 What the executable and the analyzer must NOT emit

- No p-value, confidence interval, significance statement, power statement, or minimum
  detectable difference.
- No capacity selection, no recommendation of a rung, no threshold of any kind.
- No statement about held-out behaviour, about C1-versus-S as a hypothesis, or about whether the
  extra gauge channels carry information.
- No trend, slope or direction across rungs. **Two rungs are two points**, and the S108/S109
  lesson about stringing point estimates into a direction applies with more force at two points
  than it did at five.
- No absolute filesystem path in any artifact.

### 5.4 The pre-registered interpretation — applied jointly, with ordered failure precedence

Applied **only after both agents have reviewed the exact terminal artifact**, and applied
jointly, in the same shape as Stage 1's §5.4. The status table is evaluated top to bottom and
exactly one row matches. The sign table is applied **only** after the successful status row; a
successful terminal therefore licenses one status sentence plus exactly one sign sentence.

| ordered status condition | the sentence it licenses, and nothing beyond it |
|---|---|
| either equivalence arm is `FAIL`, or the comparison cannot be completed | *"The rung-2 fitting loop did not reproduce both approved rung-1 checkpoints; no rung-2 arm or rung comparison is reported."* — and section 5.5 applies |
| both equivalence arms are `PASS` but the terminal record does not contain exactly ten `COMPLETED` rung-2 arms | *"The rung-2 run ended before all ten predeclared arms completed; no rung comparison is reported."* — and section 5.5 applies |
| all twelve arms completed but any rung-2 arm is not `OBJECTIVE_REDUCED` | *"At least one rung-2 arm did not reduce the declared total training objective under the rung-1 protocol in 20 epochs; no rung comparison is reported."* — and section 5.5 applies |
| `OPTIMIZATION_CHECK_PASSED` | *"Slot 9's rung 2 is built and fitted; the ladder has more than one rung on it, and the development record contains one rung-2 fit at five seeds under the approved protocol."* — then apply exactly one sign row below |

| successful-run sign condition | the sentence it licenses, and nothing beyond it |
|---|---|
| `deficit_sign_reproduced = REPRODUCED_IN_SIGN` | *"At rung 2, in-sample, S's macro-F1 was below C1's at all five seeds."* |
| `deficit_sign_reproduced = NOT_REPRODUCED_IN_SIGN` | *"At rung 2, in-sample, S's macro-F1 was at or above C1's at all five seeds."* |
| `deficit_sign_reproduced = MIXED` | *"At rung 2, in-sample, the paired sign was not consistent across the five seeds."* |

**Explicitly forbidden, in the same voice the Stage-1 rule uses:** attaching *because*, *so*,
*therefore*, *which shows*, *capacity-bound*, *resolves*, or *confirms* to any row above. The
successful status sentence is a statement about what was built. The sign sentence describes
five signs on in-sample development data. **No row is evidence for or against the project's
hypothesis, and the two successful sentences do not become evidence by being combined.**

### 5.5 The failure path, pre-declared so it is not improvised

If either equivalence comparison fails or cannot be completed, the run is incomplete, or the
run is not `OPTIMIZATION_CHECK_PASSED`:

1. The run's exact state is preserved, not deleted and not re-run into the same root.
2. The failure is **reported at the branch that actually occurred** — equivalence failure is a
   fitting-loop failure, incomplete execution is an incomplete run, and objective-check failure
   is a finding about the architecture-plus-protocol pair. The Technical Report carries that
   exact branch rather than collapsing all three into an architecture result.
3. An equivalence failure or incomplete run licenses no automatic replay. A retry requires a
   diagnosed cause, any necessary executable/test re-review, a new label and plan, and fresh
   joint execution authorization. A transient interruption may be retried under the same
   protocol through that fresh-root sequence; it does not require a scientific amendment.
4. If the objective-reduction check fails and a change to epochs, learning rate, or another
   protocol value is proposed, **at most one** such protocol amendment may be proposed. It must
   be a **new, separately reviewed and jointly approved document** naming what changes and why,
   written before it is run. Silently tuning against the failed development outcomes until the
   objective moves is protocol selection and bound 5 forbids it.
5. The failed run stays in the record either way.

---

## 6. Invariants the executable must carry

Numbered so a review can drive each one. Every refusal **after a permitted destination is
available** is a named terminal exit that persists an artifact, inheriting lesson 116: *a
refusal must never report through the resource whose occupancy triggers it.* There are two
disclosed pre-persistence boundaries: a missing required destination has nowhere authorized to
write, and `X_FORBIDDEN_BASE` must not persist under the protected base whose use it is refusing.
Both print the named refusal and zero resource counts to stdout and write nothing.

- **R1 — the approved rung-1 records are read, never re-written.** `results/dev_fit` is refused
  as a destination by `require_permitted_base` before any write of any kind, including the
  refusal sink's. Limitation 122/128 makes `dev_fit_result.json` the sole provenance record for
  ten checkpoints, and the equivalence arms' re-fits go to the reserved `_equivalence/` subtree
  of the claimed run root. This is the `X_FORBIDDEN_BASE` no-artifact boundary named above, not
  an exception silently taken at implementation time.
- **R2 — one atomic run-root claim.** `<base>/<run_label>/`, created with `exist_ok=False`; a
  pre-existing file or directory, empty or not, is the named terminal `X_RUN_ROOT_OCCUPIED`, and
  its refusal is persisted in a **sibling** sink, never through the occupied path. Every write
  execute mode makes after the claim succeeds is beneath the claimed root.
- **R3 — the anchor's comparability is verified, not assumed.** Before reading any rung-1 number
  or running any equivalence arm, the executable checks that the ledger's `assignment_sha256`,
  `manifest_sha256`, `role_index_sha256`, `window_schedule` and training protocol match the ones
  it is about to use, and that the recorded `fit_code_identity` matches the current code **entry
  by entry** for all eight historical entries. Any changed historical entry or extra entry inside
  that historical map is a refusal; R12 separately names the new rung-2 producer entries.
- **R4 — the rung and the band are recorded from the constructed network**, not re-derived:
  `rung` name, `n_parameters`, and the assertion `RUNG2_MIN_PARAMETERS <= n <=
  RUNG2_MAX_PARAMETERS`. The count must equal 219,018 for the declared configuration and the
  executable refuses if it does not.
- **R5 — no enforcement bypass exists.** The rung-2 constructor accepts no argument that
  disables the band check, and an AST test asserts that its signature contains no parameter
  matching `enforce|band|skip|strict|check` and that the raise is not guarded by any parameter.
- **R6 — the equivalence gate runs before any rung-2 arm**, through the same `fit_arm` the
  rung-2 arms use, with a rung-1 factory, refusing loudly on a non-identical state dict, on a
  non-identical loss history, on a missing approved checkpoint or ledger row, and on an
  unmakeable comparison.
- **R7 — the analysis is a NEW read-only script.** `analyze_dev_fit.py` and
  `analyze_capacity_sweep.py` are jointly approved and bound to their artifacts by digest;
  importing from them is required, editing them is forbidden.
- **R8 — zero rollouts, zero generation, zero pilot/val/test reads**, asserted and persisted on
  every artifact-bearing exit, including terminals, and printed on the two stdout-only boundary
  exits declared before R1.
- **R9 — the duplicated refusal writer is pinned against its approved original** by a test that
  drives both with the same valid fixed `attempt_uuid`, asserts the JSON payloads are exactly
  equal, and asserts the returned relative paths differ only in the sink-directory component.
- **R10 — no partial run may present itself as a rung.** The analyzer refuses unless the
  run-level artifact reports all ten rung-2 arms `COMPLETED` and both equivalence arms `PASS`.
  It then derives the objective-reduction status first and suppresses every paired sign and
  rung-comparison field unless `OPTIMIZATION_CHECK_PASSED` is true.
- **R11 — the design document's digest is pinned in the executable** and checked at run time, so
  an executable cannot outlive the document that authorized it.
- **R12 — the new producer identifies itself.** Plan mode binds the complete
  `fit_code_identity` map named in §5.2. Execute mode requires the plan's map to equal the current
  map entry by entry before any fit; every arm and the run-level artifact persist it. The design
  digest proves which protocol authorized the executable; it does not substitute for the code
  identity that produced a checkpoint.
- **R13 — matched seeds mean matched initialization, not merely matching integers.** Tests assert
  same-seed C1/S factories produce bit-identical initial state dictionaries, a different seed
  changes at least one tensor, and construction leaves the caller's CPU RNG state unchanged.

---

## 7. Plan mode, the run-level artifact, and retry

**The structure is `capacity-escalation-v0.1.md` §7 with the arm list changed, and it is not
restated here beyond the three points where rung 2 differs.**

1. **Plan mode runs zero fits, serializes no host path, and is byte-deterministic** — reproduced
   to at least three scratch destinations before execution is authorized, exactly as Stage 1's
   §7.1 required. The plan enumerates twelve arms (ten rung-2, two equivalence) with their
   suites, seeds, factories and destinations, states the protocol, the rung, the band, the
   expected parameter count and `MAX_FITS = 12`, and carries the design digest plus the complete
   `fit_code_identity` map of §5.2/R12.
2. **After a permitted base is available, the run-level artifact is written on every terminal
   path**, carrying the exit name, the reason class, the resource counts, elapsed time, the
   per-arm records of §5.2, and the gate evidence — including on the exits that refuse. A
   missing destination and `X_FORBIDDEN_BASE` are the two stdout-only boundaries declared before
   R1; claiming artifact persistence for either would contradict the refusal itself.
3. **Retry uses a new label and a fresh root.** A failed or partial run is preserved as evidence;
   nothing resumes into an occupied root.

---

## 8. Cost — measured in Session 111

**Measured on this machine, on synthetic tensors — no development row read, no checkpoint
written, no fit run against the delivered dataset.** CPU, 8 threads, batch 8, `W = 768`, 36
input streams, inside `deterministic_conv_precision()`, through the approved `arm_loss`.

| object | s / optimizer step (median of 10) | whole-arm 380 steps |
|---|---:|---:|
| rung 1, C = 32, 39,594 params | 0.0220 | 8.49 s **(measured whole-arm, not extrapolated)** |
| **rung 2 selected, 219,018 params** | **0.2683** | **109.29 s (measured whole-arm)** |
| rung 2 at C = 96 / H = 128, 422,314 params | 0.2908 | — |

**The whole run is twelve fits: ten rung-2 arms at ~109 s and two rung-1 equivalence arms at
~8.5 s — roughly 19 minutes of optimizer time.**

Three honest qualifications, two of them inherited:

1. **Order of magnitude only.** Stage 1's §8 recorded up to 19% run-to-run variation on this
   shared desktop between two sessions' measurements of the same quantity, and this session's
   rung-1 figure (0.0220 s/step) differs from Stage 1's (0.019 s/step) by about the same amount.
   **No figure here may be quoted as a measurement of anything but the order of magnitude.**
2. It excludes loading and windowing 304 `.npz` rows, which the real fit does and this probe did
   not.
3. **Rung 2 costs about 12× rung 1 per step while carrying 5.5× the parameters.** The extra
   factor is the GRU's 768 sequential timesteps on CPU, which parallelize poorly. That is a real
   observation about this architecture on this hardware and it belongs in the Technical Report's
   efficiency discussion. **It is not a reason to trim the design** — nineteen minutes is far
   under the Slot-10 ceiling, and the Efficiency standard's own distinction is between the
   shipped solution and the search that finds it.

---

## 9. What this measurement cannot do

Stated here so it is not discovered later.

- **It cannot establish that the rung-1 deficit was caused by capacity.** Architecture family,
  parameter count and optimization dynamics all move together between rungs 1 and 2, and at a
  fixed 20 epochs with no early stopping they are not separable. Rung 1's §1 said this about
  width; it is more true across an architecture change, not less.
- **It cannot discharge limitation 127** — see §2.2. It builds the rung.
- It cannot say anything about **held-out** performance. Every number is in-sample.
- It cannot separate "S needs more capacity" from "S's extra channels are noise a larger network
  learns to ignore." Both are consistent with any sign it reports.
- It cannot recover the structural signal limitation 67 says the dev split does not contain at
  the selected probe. **A larger network on a split with no testable structural setting cannot
  manufacture one.**
- **Two rungs are two points.** No trend, slope, or "the deficit is closing/widening" statement
  is available at two points, and §5.3 forbids one explicitly.
- **Five seeds is a small instrument and rung 2's dispersion is unknown until it is fitted.** The
  Stage-1 pooled SD may not be assigned to it. A mixed sign count is a plausible and
  pre-registered outcome, not a disappointment.
- It cannot validate the attention mechanism as *useful*. §4.3's measurements show it is wired
  and reads the window; whether it learns anything is not something an in-sample development fit
  at five seeds can answer.

---

## 10. Four decisions I am handing over rather than taking alone

Reasoning exposed in each case, so Codex can overrule the reasoning and not only the conclusion.

**D1 — importing two underscore-private names across modules in one package.** Rung 2 imports
`attribution_net._CausalDilatedBlock` and `_PerStepChannelNorm`. The alternative is a second
definition of the causal-padding rule, which is finding AP's defect class and which this project
has paid for before. My judgment is that an intra-package private import is the smaller cost and
that it should be made visible by a test asserting rung 2 defines no causal block of its own. If
you disagree, the alternative I would accept is a thin re-export, which still requires editing
the approved module — see D4.

**D2 — declaring the rung-2 parameter band as `[100_001, 1_000_000]`.** Slot 9 names no band for
rung 2. Contiguity with rung 1 is the property I actually want (an admitted rung-2 instance cannot
also lie in rung 1's size band); one decade and the hardware headroom are the rest. Architecture
name plus its admissible band identify this rung — parameter count alone does not classify a
recurrent-plus-attention candidate as rung 1 or pre-classify a future rung 3. This is a decision,
and the selected 219,018 sits comfortably inside whatever reasonable band is chosen, so
overruling it does not change the configuration.

**D3 — five seeds.** Justified by commensurability with the anchor, priced at 5/10/20 in §4.4,
and explicitly **not** justified by precision, because rung 2's dispersion is unknown. If you
want more, I would rather run five now and extend later under a justification built on a measured
dispersion than pick a number now that neither of us can defend.

**D4 — not editing `attribution_net.py`, `dev_fit_trainer.py` or `capacity_sweep.py`, at all,
for any of the three reasons this document found to want to.** Those three wants are: flipping
`CAPACITY_LADDER`'s rung-2 entry from `built=False` to `built=True`; widening
`TemporalAttributionEstimator`'s and `capacity_sweep.score_arm`'s `TemporalAttributionNet`
annotations, which their behaviour already exceeds; and adding a sink-name parameter to
`write_refusal_document`. **All three are refused by the same measured fact:**
`attribution_net.py` is one of the eight entries of
`dev_fit_trainer.training_code_identity()` (`dev_fit_trainer.py:1012`), and `capacity_sweep.py`
is an entry of `sweep_code_identity()`. Editing any of them changes a recorded identity, and
invariant R3 — the same entry-by-entry check Stage 1's C3 made — would then refuse every future
run that reads the approved anchors. **A one-word edit to a comment-level field would cost the
project its ability to re-verify its own fitted record.** So all three become disclosed
limitations with pinned tests instead of repairs. If you read the identity rule differently on
any of the three, say so before the build starts, because the module's shape depends on it.

---

## 11. Sequencing

1. **This document is reviewed and frozen.** (Codex's turn.)
2. `scripts/utils/attribution_net_rung2.py` and its tests are built and reviewed. Separate.
3. The executable `scripts/utils/rung2_escalation.py` and its tests are built and reviewed.
   Separate.
4. **Plan mode is run and its artifact is reviewed.** Separate, and zero fits.
5. Execution — the two equivalence fits and the ten rung-2 arms — is a separate joint
   authorization, in two halves, as Steps 4 of the payload extension and the capacity sweep were.
6. The read-only analyzer is built and reviewed. Separate.
7. The resulting exact state is reviewed by both agents, and only then is §5.4 applied jointly.

**A closed review loop is not an authorization** (lesson 108). Approving this document authorizes
nothing but the writing of the rung-2 module.
