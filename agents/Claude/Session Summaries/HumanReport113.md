# Claude — Human Report, Session 113

**Date and time:** 2026-08-10 20:29 PDT

**Phase:** Phase 2 — Execution.

**Progress-report session:** No. My last regular was Session 112 (covering S105–S112); my next
regular is **Session 120**, unless a phase transition or an approved written Claim-Sheet
amendment fires one sooner. Neither happened this session.

---

## Summary

Two things happened. A loop that Codex opened on me closed, and **the second rung of the
project's model-capacity ladder now exists as code** — the first new architecture this project
has built since Session 77.

The design for that rung was frozen at the end of last session: both agents approved the exact
same bytes of `rung2-escalation-v0.1.md`, which closed a two-round review and authorized exactly
one thing — writing the architecture module and its tests, and nothing else. This session did
that. `attribution_net_rung2.py` and `test_attribution_net_rung2.py` now exist, 69 tests pass
against them, the full 1,861-test packet suite is green, and both files are handed to Codex for
review at named digests. **Nothing was fitted.** No training run, no checkpoint, no simulation,
no reserved data read. The module deliberately contains no training loop at all; that is a
separate build under a separate authorization, two gates further along.

The other item was Codex's correction to a sentence I put on the public log last session. I had
written that a sharper version of an earlier measurement was "a lunch break away." Codex checked
that against the approved timing record and it does not hold: the honest projection is about 740
additional training runs and roughly 2.15 hours, with real uncertainty in both the seed count and
the time. It appended a dated correction rather than editing my entry, and I re-derived every
figure in it independently before approving. It was right, and the way I got it wrong is worth
recording: that same log entry *also* contains a careful withdrawal of a different over-confident
timing claim. I audited the careful sentence and not the loose one, four paragraphs apart, in a
document I wrote in one sitting.

The most useful technical result of the session was not the module. It was what a mutation sweep
found in **my own tests** for it, described below.

## What was accomplished

### 1. Owner re-review of the public README correction — closed

Codex's correction was checked against the closed precision note rather than against Codex's
summary of it. Every figure reproduced: 740 additional fits is `(79 − 5) × 5 widths × 2 suites`;
2.15 hours is `740 × 10.4665 s`; the 47–162 seed range is the note's own interval row; and the
"can err in either direction" qualification is faithful to the note's explicit rule that the cost
rate is directionless. I approved the exact bytes. That loop is closed with both agents on the
same state.

I recorded one measurement without acting on it, with the reasoning exposed so Codex can overrule
the reasoning and not just the conclusion. Four terms occur exactly once in the entire public
README and all four are in the new correction: *point estimate*, *dispersion interval*,
*in-sample*, and *rung-2 architecture* as a bare noun the reader has never been introduced to.
The public log is written at the plain-language bar; its neighbouring entries say "training
runs" and "tens of repeats rather than five." I did not edit it, for two reasons: the entry is
committed and published, and the log is append-only by rule; and a third dated entry restating a
correction in plainer words is the playbook's own "bloated log" failure mode for no reader gain.
So the correction propagates forward instead — the next public entry is mine, and it has to
introduce rung 2 in plain words rather than inherit that vocabulary.

### 2. The rung-2 module, built to the approved design

`Reproducibility Packet/scripts/utils/attribution_net_rung2.py`, Git blob `ca192af0`, 18,043
bytes. `RecurrentAttentionAttributionNet`: a causal convolutional stem of four residual blocks →
a per-timestep channel normalization → a two-layer unidirectional GRU → a single-query four-head
attention pool over every timestep → one fusion projection → the same four output heads rung 1
has. 219,018 parameters, 5.53× rung 1's 39,594.

Every figure the approved design declares was **rebuilt from the constructed module** rather than
transcribed:

- the seven-term parameter ledger, term by term — 2,368 + 66,560 + 128 + 102,528 + 27,936 +
  18,528 + 970 — summing to exactly 219,018, with a check that the terms account for the whole
  network and nothing is uncounted;
- all seven rows of the design's selection grid, parameter counts *and* stem receptive fields,
  including the 82,778-parameter row the band refuses by name;
- the `nn.MultiheadAttention` counterfactual at 228,330 parameters — and the fact that **228,330
  is inside the declared band**, so the band check would happily admit the wrong attention block
  and only an exact-count assertion refuses it;
- the module-type census: rung 2 has 9 convolutions, 8 linear layers, 1 two-layer GRU and 5
  normalizations, against rung 1's 19 / 4 / 0 / 10. Rung 2 is deeper in the recurrent path and
  shallower in the convolutional one, which is why no write-up may use the bare word "deeper";
- strict causality, measured by perturbation rather than read off the diagram: perturbing every
  input after step 24 moved the recurrent features at steps ≤ 24 by **exactly 0.0**;
- construction determinism; capacity identical with the gauge channels masked; and that the
  approved estimator wrapper accepts a rung-2 network with no edit at all.

### 3. The mutation sweep, and the finding it produced about my own tests

I do not trust a test suite I have only read, so the tests were measured: 21 deliberately broken
versions of the module, each run against the full suite, twice, with the file's bytes restored
and re-verified afterwards.

**The first run caught 14 and left 6 survivors — and 4 of those were real.** A version that fuses
the attention context with *itself* instead of with the recurrent state passed everything. So did
one with the two fusion inputs swapped. So did one where the normalization stage is built,
counted in the parameter ledger, and then simply never applied. And so did one where the entire
attention block is constructed, counted, and **dead** — the heads reading the recurrent state
directly.

All four are the same defect, and naming it is the point: **my tests pinned what the network is
made of and never pinned how the pieces are wired together.** Every one of those broken versions
has the right parameter count, the right shapes, the right determinism and passes the causality
check. A review centred on the parameter ledger — which is exactly the review this design invites,
because the ledger is its most conspicuous artifact — is structurally blind to all four.

I closed them with three tests, and the third is a general instrument rather than a patch for the
three specific mutants: **every parameter the network constructs must receive a non-zero gradient
from its own forward pass.** A stage that is built and never applied is precisely a stage whose
gradient never arrives, so one assertion covers every tensor at once and will catch the next
unwired stage nobody has thought of yet.

I then wrote a 21st mutation against my own new work. One of my tests asserts that the rung-2
parameter band's floor equals rung 1's ceiling plus one — "derived, never retyped," as the design
puts it. But retyping it as the literal `100_001` is not a behaviour change, so no equality
assertion can see it, and yet that is exactly the edit that silently unbinds the two bands so a
later change to rung 1's constant leaves rung 2's floor stranded. "Derived" is a property of the
expression, so the instrument has to be the source: a check that the right-hand side really is
`RUNG1_MAX_PARAMETERS + 1`.

**Final state: 19 of 19 real mutations caught. Both negative controls — a docstring word and a
comment — correctly survived, which is what shows the sweep is not simply failing on everything.
Two passes, identical results, zero bad anchors.**

## Challenges, and how they were resolved

**The design says "the eight gauge columns" and the schema says four.** My first test asserted 8
and went red immediately. Both are right: the gauge channel is four columns of the sensor
registry, and each arrives at the network twice — once as a value and once as a validity flag —
so it is eight columns of the input tensor. The test now says so in a comment rather than leaving
the next reader to rediscover it. Small, but it is the kind of thing that becomes an imagined
contradiction three sessions later.

**A method that does not exist.** My first draft of the wrapper test called `estimator.estimate(...)`;
the interface method is `update(...)`. It failed loudly and immediately, which is the point — but
it is a reminder that a test written from memory of an interface is a test of my memory.

**The chat-append tool was gone for the seventh time.** It lives in an untracked session scratch
directory and does not survive a session. It was rebuilt from the durable gate list in my
permanent-instruments file, at full strength including the permissive header recognizer and the
Windows timezone detail — the sixth consecutive faithful rebuild, and the reason it stays faithful
is a correction made several sessions ago that every improvement gets written back into the block
that owns the lesson rather than left in that session's own notes.

## Decisions I made

- **No entry on the public README this session.** The playbook allows entries only when an
  outward-facing artifact is finished, a phase closes, or something genuinely noteworthy happens.
  A newly written internal module in an *open* review round is none of the three, and publishing
  an unreviewed module as public status would tell a stranger more than the project knows. I
  re-read the playbook rather than reasoning from memory, as I have each session.
- **No `receptive_field` attribute on the rung-2 network**, only `stem_receptive_field`. Rung 1's
  property names how far back its final feature can see; here the GRU and the attention pool each
  span the whole window, so "31" would be a false name for a true number. A test pins the absence,
  and I flagged the call to Codex rather than deciding it silently.
- **I did not edit the three approved modules**, for any of the three cosmetic reasons that came
  up while building — including leaving the capacity ladder's rung-2 entry still reading
  "not built." Those files are inside recorded code identities, and a one-word edit to a comment
  would cost the project its ability to re-verify its own fitted record. Each is pinned as a
  disclosed limitation with its own test.

## Insights

The transferable one is the defect class the sweep exposed. **A parameter count is a statement
about composition, not about wiring, and a design whose most conspicuous artifact is a parameter
ledger invites a review that cannot see the difference.** Four independent ways of mis-wiring this
network all produce the declared 219,018 parameters, the declared shapes and the declared
causality. What separates a correct network from those four is not any property of its parts; it
is which part feeds which. Reconstruction tests answer that for the paths you thought of, and a
gradient-reach assertion answers it for the ones you did not.

A second, smaller one: this session's chat-append tool measured the transcript's prior state at
1,928,013 bytes with digest `3694fd8e…`, and that is **byte-for-byte the post-write digest Codex
independently recorded at the end of its own last session**. I proposed that cross-check as a
convention last session and Codex accepted it; this is its first operation as an agreement rather
than a coincidence. It is a stronger ordering check than a timestamp, because a header can be
misdated and a physical tail can be reconstructed, but two agents' independent measurements of the
same transcript state cannot agree by accident.

## Files created or updated

**Created:**
- `Reproducibility Packet/scripts/utils/attribution_net_rung2.py` — blob `ca192af0`, sha256
  `59333b48…`, 18,043 B / 362 LF / no CR / no BOM.
- `Reproducibility Packet/tests/test_attribution_net_rung2.py` — blob `52809287`, sha256
  `b7c62b59…`, 35,697 B / 874 LF / pure ASCII. 69 tests.
- `agents/Claude/Session Summaries/HumanReport113.md` — this report.

**Updated:**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — one appended turn,
  `+153/−0`, all seven writer gates passing.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/… - Active.md` — one appended turn,
  `+35/−0`, recording no order violation and the digest convention taking effect.
- `agents/Claude/README.md` — the rung-2 bullet rewritten in place (2,798 → 1,903 characters),
  per the maintenance rule that a bullet is pruned to purpose-not-content when next touched.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten, as every session.

**Deliberately unchanged:** the public `README.md` (heartbeat checked, no trigger met); the three
approved modules inside recorded code identities; and every fitted artifact.

## Resource spend

**Zero of everything measurable.** No fit, no checkpoint, no simulation rollout, no data
generation, no plan action, no analysis invocation, and no read of pilot, validation or test data.
No project data was touched at all — no manifest, no `.npz`, no label payload, not one byte of any
saved model. Lifetime rollouts remain **278**; lifetime fits remain **13**. The test suite and the
mutation sweep run entirely on synthetic tensors.

## Next steps

1. **Codex reviews the two new files** (`ca192af0` / `52809287`). If it approves them unchanged,
   step 2 of the rung-2 sequence closes and step 3 — the executable that actually fits — becomes
   authorized. If it edits, the owner re-review is mine and it is next session's first job.
2. **Do not write `rung2_escalation.py` before that loop closes.** A closed review loop is not an
   authorization, and this project has a standing lesson about exactly that.
3. Everything else in the project remains where it was: the Stage-1 capacity measurement is
   finished and jointly approved, no capacity or threshold has been selected, validation and test
   data remain untouched, and the final configuration remains unfrozen by design.
