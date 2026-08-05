# Progress Report — Claude, Session 80

**Date:** 2026-08-05 16:28 PDT
**Covers:** my Sessions 73–80 (previous report: Session 72)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The last report ended with a plan and no answer. A measurement had been designed, frozen,
reviewed to death, and written out as a document — but not run.

**It ran.** Codex executed it, I audited it, and it produced a result. That is the first
real news in this report, and I want to give you the answer before anything else:

> **Hanging more weight on the end of the arm suppresses the structural signal, and it
> suppresses it enough that at every one of the seven weights we tested, the damage level
> that weight is supposed to be responsible for testing became undetectable.**

Not *some* weights. All seven. Including the two lightest, which are the ones the earlier
experiment had already covered.

Since then: I wrote the Claim Sheet amendment that records what that means for the
project, both of us approved it, and it is now in force. Then I built the project's
**first learned model** — the neural network whose job is to look at the robot's sensor
history and say what went wrong. It exists, it is reviewed, and it is not allowed to
answer any research question yet.

The honest other half: **eight sessions, zero simulations.** The lifetime total is still
**278**, exactly where Codex's measurement left it. The central question this project
exists to answer — does structural sensing beat conventional sensing — still has no
evidence either way.

---

## The one idea you need: what "the payload boundary" is

The robot in our simulation is a two-link flexible arm. We damage it in three different
ways — the link goes soft, the motor goes weak, or a sensor starts lying — and ask whether
strain gauges bonded to the structure can tell those apart when ordinary robot sensors
cannot.

To ask that question we need the damage to be *detectable at all*. So the project has a
screen: for each level of softening, is the strain signature bigger than the arm's own
natural run-to-run variation? If not, that level is not a fair test of anything.

Last year's screen said the answer was yes for several damage levels. Then, in Session 60,
I noticed something that had been sitting in the completed experiment the whole time: the
screen had only ever run with the arm carrying **two different weights**, and they were the
two lightest of the eight the project reserves. The design document called those cells
"replicates" — as though the weight were noise — and nobody had read them as a variable.

That is the payload boundary: **how heavy can the thing in the robot's hand get before the
structural signal disappears into the noise?** The measurement that just ran was built to
find it.

Two terms you will see below:

- **Pre-registration** — writing down what you will measure and what would count as
  success *before* you look. [The Center for Open Science has a short
  explanation.](https://www.cos.io/initiatives/prereg) Everything in this project's
  measurement path is pre-registered.
- **Development-only evidence** — a result we are allowed to use to build and debug, but
  never to report as a finding. Keeping those two piles separate is most of what this
  report is about in its second half.

---

## What the measurement found

Codex ran it: **127 simulations, 61 minutes** of physics, one of them a verification re-run
proving the instrument still reproduced an already-completed simulation byte for byte. Then
I audited the result artifact — 130 separate checks, rebuilding its numbers from its own
published fields rather than trusting the program that wrote them.

Here is the whole result in one table. `q95` is the arm's natural variation at that weight;
`threshold` is twice that, which is the bar the damage signal has to clear.

| weight (kg) | reserved for | its own damage level detectable? |
|---|---|---|
| 0.025 | pilot | no |
| 0.050 | development | no |
| 0.075 | pilot | no |
| 0.100 | validation | no |
| 0.125 | validation | no |
| 0.150 | held-out test | no |
| 0.200 | held-out test | no |

**Seven for seven.** The formal outcome is what the frozen document calls `X_CASE_EMPTY`:
the set of weights at which the reserved damage is testable is *empty*.

Three things about that, in the order they matter:

**It is a real result, not a broken instrument.** The measurement carried its own positive
control — it had to reproduce nine specific numbers from the earlier experiment before it
was allowed to report anything, and it did.

**The *existence* of the boundary is solid; its *location* is not.** The heaviest weight
misses its bar by a wide margin. But the claim "the boundary sits at 0.150 kg" rests on two
neighbouring measurements that land within about 2–4% of the line — inside the band the
frozen document itself declared too narrow to decide anything. So every sentence anyone
writes about *where* the boundary is has to carry that caveat, and I have pinned that as a
standing constraint on the write-up rather than letting it drift into a clean number.

**We do not know why.** I checked the two obvious mechanisms and both are wrong. The
simulation has **no gravity** — I measured it, and all eight weights deform the arm by
exactly zero at rest — so a payload is added *inertia*, not a hanging load. And the
diagnostic wiggle we use to excite the arm runs about 97 times slower than its lowest
natural vibration mode, so this is not a resonance effect either. The mechanism is
unidentified, and I would rather say that than let a plausible story into a document
unmeasured.

---

## What we did about it

**Amendment A2 is in force.** The Claim Sheet is this project's contract — the document
that says what we are testing and what would count as success — and changing it requires a
written amendment both agents approve. I drafted A2 across Sessions 75–76, Codex edited it,
I made one technical correction, and Codex approved those exact bytes. It records the
payload finding, narrows two sentences that were broader than the evidence, and changes one
design parameter. Crucially, **it does not touch the success bar.** The thing we said we
would have to show to claim a win is exactly what it was in Phase 1.

I want to flag one sentence in it that I sharpened, because it is the kind of thing that
gets written loosely and then quoted forever: an early draft said "no mass retained its own
role." True as an aggregate — and three of the seven missed by so little that a single
well-shaped flip would reverse them. It now reads "no measured mass retained its own
reserved severity, and at three of the seven the margin was inside the instrument's own
reproducibility band." Same finding, honest width.

---

## The first learned model exists

Sessions 77 onward opened **Gate 4**: the matched learned models, which is the part of the
project where the actual hypothesis finally gets tested.

The design has been fixed since Phase 1, and the point of it is fairness. Two identical
neural networks are trained on two sensor packages that differ in exactly one thing:

- **C1** — joint encoders, commanded torques, a motor-current estimate, one inertial sensor.
  A realistic, affordable robot.
- **S** — all of C1, plus four strain gauges bonded to the structure.

Same architecture, same training recipe, same random seeds, same data. If S wins, the win
is attributable to the gauges and to nothing else.

The first rung of that model is now built and reviewed: a **39,594-parameter** causal
temporal convolutional network — small by any modern standard, which is deliberate. It
reads 768 time-steps of sensor history and reaches back over 1,023 of them, and it outputs
four things: what kind of fault, whether it should decline to answer, where, and how badly.

It has **no trained weights**, and it is not permitted to acquire any until a separate
review closes. That is the subject of the last three sessions.

---

## What was unexpected: the same model gives different answers on the CPU and the GPU

This is the finding from this stretch that I would most want you to know about, because it
is small, boring-sounding, and would have quietly undermined the project's central claim.

I trained nothing — I just built the same network twice, with the same weights and the same
input, and ran it on the processor and then on the graphics card. The answers disagreed.

By how much: **0.00008842** on a four-way probability. That is three orders of magnitude
below the 0.05 difference our success bar demands, so it threatens no headline. But it
falsifies two things this project genuinely relies on:

1. that a result we publish reproduces on someone else's machine, and
2. that a difference between the C1 arm and the S arm is a difference in **sensing** —
   rather than partly a difference in which device, or which numerical shortcut, each arm
   happened to run under.

The cause is a speed optimization PyTorch turns on by default, which lets the graphics card
do parts of the arithmetic at reduced precision. ([NVIDIA's explanation of the tradeoff is
here.](https://blogs.nvidia.com/blog/tensorfloat-32-precision-format/)) Turning it off
takes the disagreement to 0.00000006 — the floating-point noise floor.

So the project now has a single named context that every component doing model arithmetic
must run inside, and the eventual Technical Report has to state the setting the numbers
were produced under. It cost one measurement to find and one line of code to fix. It would
have been essentially impossible to find *after* the fact, in a comparison of two trained
models, because it looks exactly like a small real effect.

---

## What isn't working

**Eight of my sessions, and no evidence about the hypothesis.** Codex's measurement is real
science and I audited it; everything I have personally produced since is infrastructure. My
last report made this same admission about a different eight sessions, and I said then that
I did not think the point where it stops being worth it is nowhere. I still think that, and
I am closer to it now than I was.

Here is what the last three of those sessions actually were, so you can judge rather than
take my summary of it. Codex ruled that we *may* train on the already-collected development
data, since training reads existing files and generates nothing new — but under five
explicit limits, including that every checkpoint must be stamped development-only and must
record exactly which data, which configuration, which code and which random seed produced
it. I built the module that enforces those limits. Then:

- Codex reviewed it and found four real defects. I kept every line of its repair and found
  two more one layer beneath.
- Codex reviewed *that* and found two more real defects — including four fields that
  promised an exact 64-character fingerprint and would quietly accept a 65-character one
  with a newline on the end.
- I reviewed *that* this session and found one more: the routine that **builds** a
  checkpoint's code fingerprint would hand back an empty one without a word, while the
  routine that **audits** it refuses exactly that value one step later. Two halves of one
  rule, in one file, disagreeing.

Every one of those was real. None of them is robot proprioception. This is the fourth
consecutive report in which I have had to write a paragraph like this one, and I think the
pattern is now the most important thing in this report: **this project reliably finds real
defects in its own instruments, and reliably does not get to the science.** I do not have a
clean fix to propose. What I have done is set the sequencing so the next block is
irreversibly forward: the contract closes, the trainer gets one review, and then the fits
run.

**Still waiting on you, still not blocking:** `director_requests.md` entry 1 — the Claim
Sheet review from Phase 1 — is unanswered. It is explicitly non-blocking and we have kept
working. Nothing else is waiting on you.

**A known limitation I want on your radar.** The measurement above says the development
data contains **no softening damage severe enough to be detectable** at the weights it
carries. Gate 4 trains the structural-attribution model on exactly that data. That does not
make the training pointless — it can still show the implementation learns, and expose
failure modes — but it does mean a null result from this stretch would be about the *data*,
not about the *hypothesis*, and no write-up may blur the two.

---

## The verification artifact

No change this session, and I am not going to manufacture one. Your hands-on path (Claim
Sheet Slot 8) still lives inside the Reproducibility Packet and gets built as the
measurements that feed it arrive.

The one thing I will point at: the payload result file is checkable without us. Everything
in it re-derives from its own contents, which is a property both Codex and I demonstrated
independently, with separate code, neither importing the program that wrote it. If you ever
want to check that we did not adjust the experiment after seeing its answer, that file plus
its fingerprint is how.

One honesty note on that, because two independent audits sound stronger than they are:
**neither audit reached the raw sensor traces.** Everything downstream of the extracted
signal was recomputed from the file; the step from raw simulated strain to that signal was
not, because the traces are not stored. That step is covered by the byte-for-byte replay
check and by nothing either audit did, and the Technical Report will say so in those words.

---

## What is next

1. **Codex closes the fitting-contract review.** One turn. It owns it.
2. **I build the trainer** — the program that runs the ten development fits (two sensor
   packages × five random seeds) and writes each checkpoint with its full provenance
   stamped on it. It gets one review before any fit runs. I have committed in writing to
   the shape of it already, so that review is about the code and not about the design.
3. **The ten fits run.** Development evidence only: they may show the model learns, and may
   expose failure modes. They may not set a threshold, pick a model size, or become a result.
4. **Then the real sequence**: calibration on validation data, the configuration freeze, and
   the single untouched confirmatory run that answers the project's question.

If the next report cannot tell you whether a small neural network learns anything at all
from four strain gauges, then I will have spent sixteen sessions on plumbing and the
concern I raised above will have stopped being a caveat and become the story.
