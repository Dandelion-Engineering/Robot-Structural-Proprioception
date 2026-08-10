# Claude — Human Report, Session 111

**Date and time:** 2026-08-10 16:28 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. My next regular progress report is Session 112, unless a phase
transition or an approved written Claim-Sheet amendment fires one sooner.

---

## Summary

This was the first session in a long stretch that began with **nothing open on either agent** —
no review loop to close, no returned state waiting for my approval. What it had instead was a
direction. At the end of its Session 110, Codex closed the last open loop and then ruled on the
three questions the Stage-1 precision note had deliberately left open. Its ruling: stop spending
seeds on the current within-rung measurement, and build the thing the Claim Sheet has named since
Phase 1 and nobody has built — **rung 2 of the model-capacity ladder, a larger recurrent-plus-
attention estimator.** It asked me to return a zero-resource design for review, under six
explicit bounds, since I own the estimator lane under the agreed labor split.

I did that. The session produced one new document —
`Reproducibility Packet/protocol/rung2-escalation-v0.1.md` — and the measurements it rests on.

The short version of what the design says:

- **One named architecture, not a sweep.** A causal convolutional stem feeding a two-layer
  unidirectional GRU, read out by a single-query multi-head attention pool at the window's final
  timestep. **219,018 parameters, 5.53× rung 1's 39,594.** Ten development fits — two sensor
  suites × five seeds — plus a two-arm gate that proves the fitting loop is still the approved
  one.
- **Everything except the architecture is held exactly fixed**, including the training protocol,
  which is inherited unchanged from rung 1 so that the two rungs are comparable.
- **Every claim in it was measured this session rather than reasoned about.** The parameter
  counts, the strict causality of the network, its determinism, the fact that its capacity is
  identical for both sensor suites, whether the attention path is actually wired, the cost, and
  whether the architecture optimizes at all under the inherited protocol — all measured, on
  synthetic tensors, touching no project data of any kind.
- **The read is pre-declared and deliberately small.** Six rows, each licensing exactly one
  sentence, with a list of the words that may not be attached to any of them.

The session spent zero of everything: no fit against a development row, no checkpoint, no
generation, no rollout, no data read. Rollouts remain 278 and the fit counter remains 13.

One sentence is worth pulling out of the design, because it is the part I expect the director to
care about and it is the part that was easiest to get wrong. **Building rung 2 does not tell us
whether the earlier result was caused by capacity, and the design says so in three places.**
Architecture, size and optimization all change at once between rungs, so a difference between
them has more than one available explanation. What rung 2 buys is that the project can no longer
be accused of having tested its central question with only one model, at one size, and stopping
there.

---

## What happened, in order

### 1. Reading the state, and confirming the direction was mine to take

Codex's Session-110 turn made a design-direction proposal, not a decision, and explicitly invited
me to contest the literal-rung-2 reading before drafting. I did not contest it, and the reason is
in the record rather than in preference: Slot 9 of the Claim Sheet names rung 2 in words, carried
limitation 127 says the ladder must be climbed for the structural suite before any conclusion
comparing it to the conventional one, and the alternative on the table — extending the existing
network's width to 64/96/128 channels — would have been another sweep of the rung whose curve we
had just finished proving unreadable at five points and five seeds.

### 2. The one place I sharpened Codex's reading instead of accepting it

Limitation 127's licensing sentence is *"the ladder must be climbed for S before any C1-vs-S
conclusion is drawn."* Read quickly, that sounds like a task with a completion condition: build
rung 2, tick the box. It is not. It is a constraint on a **conclusion**, and the conclusion it
guards is the held-out confirmatory comparison at the project's final gates — which no
development fit at any rung ever reaches.

Three things follow, and all three are now written into the design (§2.2):

1. this document does not discharge limitation 127; it builds the rung;
2. what discharges 127 is the confirmatory comparison being run at a capacity that validation
   selected from a ladder with more than one rung on it;
3. **"the ladder has been climbed" is not an observation the measurement can report.** It is true
   the moment rung 2 exists and is fitted, whatever the numbers say — because a climb that only
   counts when the result is favourable is not a climb.

That third point is the same failure shape Codex corrected in me two sessions ago and that I
repeated once more the session after: the safe-sounding sentence is the one nobody audits. *"Rung
2 will tell us whether the deficit was capacity"* is safe-sounding and false, and it is now
forbidden in writing.

### 3. The architecture, and why each piece is there

```text
input  [batch, 36 streams, 768 timesteps]      (18 channels, each with its validity mask)
  -> pointwise projection to 64 channels
  -> 4 residual causal dilated convolution blocks     (local features, 31-sample span)
  -> per-timestep channel normalization
  -> 2-layer unidirectional GRU, hidden 96            (the recurrent path)
  -> 4-head attention pool, one query built from the final GRU state
  -> fusion layer
  -> class / unknown / location / severity heads      (the same four heads as rung 1)
```

Four choices are worth explaining to a non-specialist reader, because each one is a place the
science could have been quietly broken:

- **The recurrence is one-directional.** A bidirectional layer would let the network read the end
  of a window while forming its opinion about the beginning. That is invisible in offline testing
  and fatal to the claim that the same weights would work on a real robot reading its sensors as
  they arrive. I measured it rather than asserting it: perturbing every input after timestep 40
  changed the features at timesteps 40 and earlier by **exactly zero**.
- **The attention is one query at the final timestep, not attention everywhere.** Only the final
  timestep's summary is actually used to make a decision, so computing attention at all 768
  timesteps would do 768× the work the decision consumes. The property that matters is preserved:
  the decision at any time depends only on what came before it.
- **The convolutional stem got shorter, from nine blocks to four.** Rung 1 needed nine because
  convolution was its only way of seeing across the window. Here the GRU and the attention pool
  each span the whole window on their own, so the stem's job is local feature extraction.
- **The stem's building blocks are imported from the approved rung-1 module, not re-typed.** A
  second copy of the rule that makes a convolution "causal" is a second place it can be wrong, and
  this project has already paid for that defect class once.

### 4. Codex's six bounds, and where each is discharged

Codex attached six conditions to the request. Each is answered in a named section rather than in
spirit:

| bound | discharged by |
|---|---|
| build, execute, validation-read and confirmatory stay separate gates | §11's seven sequenced steps; approving the document authorizes only writing the module |
| the two sensor suites stay **exactly** capacity-matched | measured — masking the structural channels leaves the parameter count at 219,018 and every output shape identical, while changing the outputs |
| the rung and its band **named and enforced**, not bypassed with a Boolean | the new constructor takes no enforcement argument at all; the band's lower edge is *derived* from the approved rung-1 constant rather than retyped; and an automated test asserts no such argument can be added |
| no Stage-1 anchor, ledger, run root or result modified | the destination check refuses the approved checkpoint directory before any write of any kind, including the refusal record's |
| development fits are implementation/learnability checks only | the pre-declared criterion is deliberately weak — finite losses, final epoch below first — and the read forbids p-values, intervals, capacity selection and any held-out claim |
| the seed budget justified for the **new** decision | five seeds, justified by comparability with the existing anchor and explicitly **not** by precision, because the new architecture's seed-to-seed spread is unknown until it is fitted |

The third of those is the one Codex cared most about, and it deserves a plain-language note. Rung
1's network had a safety check refusing to be built at a size outside its declared band — the
ladder cannot be climbed by editing a number. But that check could be switched off with a single
argument, which satisfies the letter of the rule and destroys its purpose. **The rung-2 network
has no such switch.** The check is unconditional, and the tests that used to need the switch get
their speed a different way.

### 5. What I measured, all of it on synthetic data

| what | result |
|---|---|
| parameter count of the selected configuration | 219,018 (5.53× rung 1) |
| strict causality | perturbing everything after step 40 changed earlier features by **exactly 0.0** |
| determinism | two builds at the same seed are bit-identical; a different seed differs |
| identical capacity across sensor suites | 219,018 either way, shapes identical, outputs differ |
| the attention path is live | the attention contributes about 46% of the pooled read's magnitude |
| attention before training | **near-uniform**, as an untrained network's must be — a wiring check, not evidence it learns anything |
| cost | 0.268 s per optimizer step vs rung 1's 0.022; a whole arm 109.3 s vs 8.5 s; the whole run ≈ 19 minutes |
| does it optimize at all under the inherited protocol | yes — loss 2.564 → −0.550 over 20 epochs on a synthetic memorization task |

Two of these are in the document specifically because they are the inconvenient ones. **Rung 1
reached the lower loss of the two on the synthetic task** — that measures memorization of random
labels and says nothing about real data, and it is recorded rather than omitted. And **rung 2
costs about 12× rung 1 per step while carrying only 5.5× the parameters**, because a recurrent
network's 768 sequential steps do not parallelize well on a CPU. That is a real efficiency finding
about this architecture on this hardware and it belongs in the eventual report.

### 6. A wall I hit, and the shape of the answer

Neither the approved trainer nor the approved capacity-sweep module can fit rung 2. The trainer
has exactly one place where it builds a network and it names rung 1 there; the sweep module
refuses any width outside its own five-point grid. This is the same wall Stage 1 hit, and the
established answer is to copy the training loop and prove the copy still behaves like the
original.

The problem is that this would be the **third** copy of that loop, and three copies is where
drift stops being hypothetical. The design's answer is a small improvement on the established
shape: **the loop is written once and parameterized by a network factory.** The rung-2 arms pass a
rung-2 factory; the verification gate passes a *rung-1* factory and asserts that the resulting
weights are bit-identical to the checkpoints the approved trainer produced in Session 84. The gate
therefore exercises the identical code path the real arms use, differing only in which network is
built.

### 7. The decision I most want reviewed

Three separate times, this design wanted to make a small edit to an already-approved file: to flip
a `built=False` flag on the ladder's rung-2 entry, to widen a type annotation that the code's own
behaviour already exceeds, and to add a parameter so that rung-2 refusal records stop being filed
in a directory named after the capacity sweep.

**All three are refused by one measured fact.** The approved network module is one of eight files
whose digests are recorded as the identity of every checkpoint the project has fitted, and the
approved sweep module is likewise recorded in the sweep's identity. A one-word edit to a
comment-level field changes a recorded identity — and the design's own verification rule, which
checks those eight entries one by one, would then refuse every future run that reads the approved
results. **The project would trade the ability to re-verify its own fitted record for a cosmetic
fix.**

So all three become disclosed limitations with tests pinning them, and the one that forces a real
duplication — the refusal writer — carries a test that drives both copies on the same input and
asserts they agree, so they cannot drift apart in silence.

---

## Challenges and how they were overcome

**Deciding what rung 2 is *for*, when the obvious answer is wrong.** The tempting framing is that
rung 2 settles whether the earlier deficit was a capacity problem. It cannot: architecture, size
and optimization dynamics all move together between rungs, and at a fixed epoch budget they are
not separable. Overcome by writing the honest purpose into the document three times — in §1, in
§2.2, and in §9's list of what the measurement cannot do — and by pre-declaring a read whose rows
are statements about signs and about what was built, never about causes.

**Justifying a seed budget without inheriting one.** Codex explicitly barred inheriting the number
from the Stage-1 curve or from that curve's "79 seeds" point estimate. The honest position is that
no precision argument is available at all, because the new architecture's seed-to-seed spread is
unknown until it is fitted, and the Stage-1 spread may not be assigned to a configuration nobody
has run. Overcome by justifying five seeds on a *different* ground — comparability with the
existing anchor, which exists at exactly those five seeds — pricing five, ten and twenty so the
alternative is visible, and stating plainly that a deeper estimate should be a later extension
built on a measured spread rather than a number picked today.

**Not letting a design document quietly become a second unreadable curve.** The instinct after
Stage 1 was to sweep rung 2's size too. Stage 1's own measurement is the argument against it: a
five-point, five-seed within-rung curve resolved a minimum paired difference of 0.263 against a
pre-declared scale of 0.05, and the frozen interpretation rule matched exactly one row — the one
saying the curve has no readable shape. Running that again one rung up would spend fits to buy the
same sentence. Overcome by proposing exactly one configuration and writing the reason into §4.6 in
terms of what was measured rather than in terms of taste.

**The append-only transcript writer was gone for the seventh time.** It lives in an untracked
session scratch directory, which does not survive a session. It was rebuilt from the seven-gate
list in my summary before anything was written, and all seven gates printed their measured values.
The prior-bytes digest the writer recorded matched, exactly, the post-write digest Codex published
in its own Session-110 report — an independent confirmation that nothing touched the transcript
between the two sessions.

---

## Decisions and reasoning

1. **Accept the literal-rung-2 reading without contest.** The authority is the Claim Sheet and
   limitation 127, not the Stage-1 curve, and Codex was right that a width extension would not be
   a climb.
2. **Sharpen what limitation 127 licenses.** It constrains a conclusion, not a task, so this
   document builds the rung and does not discharge the limitation. Written into §2.2 so nobody
   builds against the looser reading.
3. **One configuration, not a rung-2 sweep.** Selecting among rung-2 sizes is capacity selection
   and belongs to validation under its own authority; and Stage 1 already measured what a small
   within-rung curve can resolve.
4. **Inherit the training protocol unchanged**, so the architecture is the only difference between
   the rungs — and pre-declare the failure path, because the temptation if rung 2 does not learn
   in 20 epochs will be to tune until it does, which is protocol selection against development
   data and is forbidden.
5. **Enforce the band with no bypass at all**, rather than with a flag defaulted to on, and write
   the tests so they never need one. A control that can be switched off is a control that will be.
6. **Declare the rung-2 parameter band, and say that it is a declaration.** The Claim Sheet names
   no band for rung 2; I chose one contiguous with rung 1's so that a parameter count identifies
   its rung with no ambiguous value in between. Flagged as a decision Codex may overrule.
7. **Do not edit any approved file, for any of the three reasons this design found to want to.**
   The identity chain is worth more than the cosmetics.
8. **Leave the public Live-Run README untouched.** The heartbeat check ran; a design handed into
   review is not a finished artifact, a phase transition, or a public result. Codex reached the
   same conclusion independently in its Session 110.

---

## Insights gained

**A rule that is enforced by default is not the same as a rule that cannot be broken.** Rung 1's
band check was on by default and could be turned off with one argument. Nobody ever turned it off,
and Stage 1 even wrote down that a future session should not — but the note was a request, and the
request would have been read by whoever was in a hurry. Removing the argument entirely costs
nothing except making the tests slightly more thoughtful, which is a good trade for a control the
project's central comparison depends on.

**The cheapest way to keep a design honest is to measure the thing you were about to assert.** Six
of the design's load-bearing claims — causality, determinism, matched capacity, a live attention
path, cost, and whether the thing optimizes at all — were assertions I could have written and
nobody would have questioned. Measuring them took under half an hour and changed two of them: the
cost ratio is worse than the parameter ratio suggests, and rung 1 beats rung 2 on the synthetic
task. Both of those are now in the document.

**An identity chain makes small edits expensive, and that is the feature working.** It felt
absurd to refuse to change `built=False` to `built=True`. Then I traced what that field's file is
bound to, and the absurdity moved: the project records the digests of eight files as the identity
of every checkpoint it has ever fitted, precisely so that a future reader can prove the results
came from the code that claims to have produced them. Making that guarantee cheap to break in
exchange for cosmetic accuracy would be the wrong trade in every direction.

**"The ladder has been climbed" must not be conditional on the result.** I nearly wrote a read in
which the climb counted only if the deficit persisted or vanished in some interpretable way. That
would have made a structural fact about what was built contingent on what was found — which is
precisely the move the project's honesty bounds exist to prevent, arriving from an unexpected
direction.

---

## Files created or updated

- `Reproducibility Packet/protocol/rung2-escalation-v0.1.md` — **new.** The rung-2 design, 44,063
  bytes, Git blob `b7449993ceeb657fb37feff36bff4cb827ceed0a`, sha256
  `97ff428021a5e68631afa2e04b6309aafc81b37f454c26c8c5a997d253069d7a`. Handed to Codex for review.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my Session-111 turn returning the design, answering each of Codex's six bounds,
  reporting every measurement, and raising four decisions for its ruling. `+167 / −0`.
- `agents/Claude/Session Summaries/HumanReport111.md` — this report.
- `agents/Claude/README.md` — updated for the new design document and the current state.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

Not changed, deliberately: every approved executable, test, protocol, plan and result; the Claim
Sheet; `director_requests.md`; both `.gitattributes` files; the public Live-Run README;
`.gitignore` (reviewed and found accurate — the session's only untracked artifact was the new
design document, which belongs in the repository).

---

## Resource and evidence boundary

Zero of everything. No fit against any development row, no checkpoint, no data generation, no
physical rollout, no C7 invocation, no plan action, no pilot/validation/test read, and no edit to
any executable, test, protocol, plan, result or packet file other than the new design document.

**It touched no real data at all** — no manifest, no `.npz`, no label payload, and not even a hash
of a `.pt` checkpoint. Every probe this session ran on synthetic tensors in the session scratch
directory outside the repository and wrote nothing into the project.

The synthetic optimizer steps in the cost and learnability probes are **not** development fits and
spend no budget, on the standing precedent that the capacity-sweep test suite's fits have always
been synthetic steps at the real registry width.

Lifetime physical rollouts remain **278**. The lifetime fit counter remains **13**.
`Reproducibility Packet/config/config.json` remains absent. Working tree clean before the session
except for nothing, and clean after except for the two intended changes plus the closeout files.

---

## Next steps

1. **Codex reviews `rung2-escalation-v0.1.md`** under the review-cycle playbook and either
   approves the exact state or returns findings. A clean design review authorizes writing the
   rung-2 module and nothing else.
2. Codex should rule on the four decisions I handed over — the private-name import, the declared
   parameter band, the five-seed budget, and above all the refusal to edit any approved file. The
   module's shape depends on the last one.
3. If the design is approved, the next build is `scripts/utils/attribution_net_rung2.py` and its
   tests, as its own separate review loop.
4. Everything downstream stays gated: the executable, plan mode, execution authorization in two
   halves, the read-only analyzer, and only then the joint application of the pre-declared read.
5. Capacity selection and every probability, detection, abstention, out-of-distribution and
   uncertainty threshold remain validation-owned under separate authorization.
6. Pilot, validation and test roles remain unread until their named gates open.
7. My next session is 112, which **is** a regular progress-report session (covering Sessions
   105–112) in addition to its normal work.
