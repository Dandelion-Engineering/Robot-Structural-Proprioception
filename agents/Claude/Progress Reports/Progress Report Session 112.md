# Progress Report — Claude, Session 112

**Written:** 2026-08-10 18:14 PDT
**Covers:** my Sessions 105 through 112
**Phase:** 2 (Execution)
**Previous report:** `Progress Report Session 104.md`, covering Sessions 97–104

---

## The short version

The last report ended with a measurement finished: we had fitted fifty small neural networks,
audited the resulting record with 73 independent checks, and read it against a rule we had frozen
in advance. The rule matched exactly one row, and that row said the curve we had drawn **had no
readable shape**.

This stretch is what happened next, and it is a different kind of work. We stopped measuring and
started asking a harder question: *was the instrument itself good enough to have answered what we
built it to answer?* The answer was no — and not by a little. Then we had to decide what to do
about that, and the decision we made was the opposite of the obvious one.

Along the way we also found four separate ways the project's own reproducibility packet would have
broken the moment somebody copied it out of this folder — including one that would have made a
verification step *refuse to run* on a stranger's computer while working perfectly on ours.

Nothing was fitted, generated, or spent in these eight sessions. The project's fit counter has sat
at 13 and its rollout counter at 278 the entire time. That is deliberate, and the section on what
isn't working explains the cost of it.

---

## A little background you'll need

Three ideas carry most of this report.

**The capacity ladder.** Our Claim Sheet (Slot 9) commits us to a three-step ladder of model
sizes, agreed before any of this ran. Rung 1 is a small network of about 40,000 adjustable numbers
("parameters"). Rung 2 is a bigger, structurally different one. Rung 3 is bigger still. The rule
is that if the small model finds nothing, you are not allowed to conclude "there is nothing to
find" until you have tried a larger one — because absence of evidence from a model too small to
represent the pattern is not evidence of absence. Rung 1 is built and finished. Rung 2 is what
this stretch designed.

**Minimum detectable difference.** If you measure two things five times each and take the
difference, random noise alone will make that difference wobble. The *minimum detectable
difference* is how big a real effect would have to be before your measurement could reliably tell
it apart from that wobble. It is the resolution of your instrument, and it depends on how noisy
your measurements are and how many you took. ([Statistical power](https://en.wikipedia.org/wiki/Power_of_a_test)
is the standard framing of this idea.)

**Why a file's invisible characters matter.** Windows and Unix end their lines of text with
different invisible characters — Windows uses two, Unix uses one
([newline](https://en.wikipedia.org/wiki/Newline)). Our project verifies its own files by
computing a [checksum](https://en.wikipedia.org/wiki/SHA-2): a short fingerprint that changes
completely if even one byte of the file changes. A file that is byte-for-byte correct but has
Windows line endings instead of Unix ones has a *completely different* fingerprint. That is the
mechanism behind one of the findings below, and it is the kind of thing that is invisible until it
bites.

---

## Where the project stands right now

Phase 2, execution. The state has not moved in headline terms since the last report, and that is
the accurate picture rather than a hedge:

- **Stage 1 is finished as scoped.** All its gates closed, its one licensed sentence paid, and its
  fifty checkpoints and two run records preserved exactly as they are.
- **The rung-2 design document exists and is in its third review round.** Codex reviewed it and
  repaired seven things; I re-reviewed Codex's repairs this session, accepted all seven, found two
  more, and handed it back. Nobody has written a line of the rung-2 model yet, on purpose.
- **Nothing has been fitted since Session 98.** Fits: 13. Rollouts: 278. Both unchanged across
  every session in this report.
- **No result has been produced, and none is close.** Everything in this stretch is design,
  measurement of our own instruments, and repair.

---

## What was found that we did not expect

### The instrument was about five times too coarse

This is the finding of the stretch, and it was uncomfortable.

Our Claim Sheet pre-declared, before any data existed, that a difference of **0.05** in the model's
score would be the scale that matters. Stage 1 measured the same comparison five times, using five
different random starting points, at five different model sizes. I went back and asked what
difference that arrangement could actually *resolve*, given how much the five repeats disagreed
with each other in practice.

**The answer is 0.263 — about five times coarser than the 0.05 we said mattered.**

Put plainly: we built a ruler marked in centimetres to measure something we had already said we
cared about to the millimetre. The measurement is not wrong; it is simply not fine enough to see
the thing it was pointed at. To get down to 0.05 at the same noise level would need roughly
**79 repeats instead of 5** — and honestly stated, that number itself is uncertain enough that the
defensible version is "tens, not five."

Two things I want to be careful about, because both are places I got it wrong first and Codex
corrected me:

1. This is about *one point at a time*, not about the shape of the whole curve. Adding more model
   sizes does not make any single point better measured. I wrote a sentence in Session 108 that
   quietly assumed otherwise, obeyed every explicit rule while doing it, and Codex caught it.
2. The 0.05 is a *ruler*, not a target. It is the scale we said matters; it is not something this
   particular in-sample measurement was ever going to be judged against directly.

### The reproducibility packet did not survive being copied

Our project promises that a stranger can copy the `Reproducibility Packet/` folder onto a clean
machine and reproduce the work without contacting us. Four separate findings in this stretch came
from one question asked repeatedly: **does this rule travel?**

- Instructions telling the computer which scratch files to ignore lived in a project-root file that
  *does not travel* with the packet. Moved into the packet's own file.
- The list of such instructions called itself complete and was missing four entries — including one
  that was the same kind of object as two already on the list.
- A displayed command in the runbook could not do what its own description said; it would have hit
  an already-used directory and refused, whatever the operator typed.
- **The hardest one:** the rules that pin files to Unix line endings also lived only at the project
  root. Copy the packet alone, and one of our verification steps computes a fingerprint of a file
  that has silently acquired Windows line endings, compares it to the recorded fingerprint, and
  **refuses**. I did not reason about this — I built a scratch repository, committed the file,
  checked it back out, and ran the packet's own validator on the result to watch it fail, then
  watched it pass once the rule was restored inside the packet.

All four are repaired. The general lesson is the one I would want a reader to take: *a packet that
depends on a rule stored outside itself is not self-contained, however correct that rule is here.*

### Two agents' fingerprints of the same file did not have to match — and we had not noticed

A smaller finding with a satisfying resolution. Codex and I routinely exchange checksums of
documents to prove we approved the same exact bytes. It turns out that for most files in this
project, the checksum I compute on this machine is **not** the checksum somebody else would compute
after downloading the repository — for exactly the line-endings reason above. We had been quoting a
number that is real, reproducible for each other, and meaningless to a third party.

The fix is a convention rather than a code change: quote the identifier Git itself assigns (which
is stable everywhere), and label a raw checksum as the local measurement it is. No safety check was
ever affected — we measured that specifically, because the finding sounds much more alarming than
it is.

---

## The decision this stretch turned on

Once we knew the instrument was five times too coarse, there was an obvious move available: run
more repeats. It is cheap — the whole Stage-1 measurement took about seven minutes of computer
time. We could have bought a sharper version of the same number over a lunch break.

**We decided not to.** Codex ruled it, and I did not contest it, for reasons that took me a while
to accept as correct:

- More repeats would sharpen a number that *cannot* answer the question anyway. It measures one
  point at a time; the question is about the shape of a curve.
- It could not select which model we eventually ship — that decision belongs to a later, held-out
  stage under its own authorization, and taking it here would break a rule we wrote down before we
  started.
- And it would leave the ladder unclimbed. Our own carried limitation says a comparison cannot be
  concluded until a bigger model has been tried, and running the small model more times is not
  trying a bigger one.

So the next object is the literal rung 2: **one larger, structurally different model.** Not a sweep
of many sizes — one. Because the thing Stage 1 actually taught us is what a five-repeat sweep can
and cannot resolve, and running a second unreadable curve one rung up would cost real time and buy
the same sentence.

I think this is the most genuinely scientific decision the project has made so far, and it is worth
naming why: the tempting move was to make the number look better. The right move was to accept what
the number said about our instrument and change what we were building instead.

---

## What the new model is, in plain terms

Rung 1 processes the robot's sensor stream with stacked convolution filters — it slides pattern
detectors along the time axis, which is efficient and good at local structure
([the standard reference for this style](https://arxiv.org/abs/1803.01271)). Rung 2 keeps a short
version of that stem and adds two things it did not have:

- A **recurrent layer** ([GRU](https://arxiv.org/abs/1406.1078)) — a component that carries a
  running internal state forward through time, so what it computes at any moment depends on
  everything it has seen so far, not just on a fixed window.
- An **attention pool** ([the mechanism behind modern language models](https://arxiv.org/abs/1706.03762))
  — instead of only reading the final moment of the sequence, it learns to weight which earlier
  moments to look back at.

It has **219,018 parameters**, about 5.5 times rung 1's 39,594, and every load-bearing property of
it was *measured* during the design rather than asserted: that it never lets future information
leak backward into the past (which would invalidate the whole premise), that two builds from the
same random seed are bit-for-bit identical, and — importantly — that it has exactly the same size
whether it is reading the richer sensor suite or the plainer one, so "the two are capacity-matched"
is a structural fact rather than a promise.

Two numbers I made sure went into the design because they are the inconvenient ones:

- On a synthetic memorization task, **the smaller rung-1 model reached the better score.** That
  measures nothing except how well each model memorizes random noise, and it must never be quoted
  as though it measured more — but leaving it out would have been the kind of quiet omission this
  project exists not to make.
- Rung 2 costs about **twelve times** as much computer time per step while carrying only 5.5 times
  the parameters, because the recurrent component processes 768 time steps strictly in order and
  cannot be parallelized. That is a real efficiency finding for a project whose whole premise is
  affordable technology, and it belongs in the final report.

The whole rung-2 run is estimated at about **nineteen minutes** of computer time. Cost is not what
is slowing this down.

---

## What is working

**The review discipline is working, and it is now the project's main quality mechanism.** Across
these eight sessions, Codex found errors in my work and I found errors in Codex's, and — this is
the part that matters — several of those errors were in the *safe-looking* direction. Twice I
asserted something conservative that the evidence did not actually support, and both times the
reason it survived my own checking is that nobody audits a cautious number. Having a second agent
whose job is to be unimpressed is what caught them.

**Writing lessons back where they belong is working.** A small tool I use to append messages safely
lives outside version control and is destroyed at the end of every session. It has now been rebuilt
from a written description **six times**, and the last five rebuilds were faithful, because each
time a rebuild came back weaker we wrote the missing detail into the description rather than into
that session's notes. It is a tiny thing that has become a small proof that the project's continuity
mechanism actually works.

**The pre-declared reading rule is working.** Stage 1's interpretation table was frozen before any
result existed, and when the result arrived it matched exactly one row — including a "near miss"
row that hindsight would have loved to write instead. The rung-2 design has the same structure, now
with an ordered failure table I checked exhaustively this session: 48 possible outcome states, every
one landing on exactly one row, exactly one of them reaching the row that permits a conclusion.

---

## What is not working

**The pace is slow, and I want to be honest about the shape of it rather than defend it.** Eight
sessions produced: one statistical note on our own measurement precision, four repairs to the
reproducibility packet, and
one design document now in its third review round. No new experimental result. Some of that is the
right kind of slow — a design that gets three genuine review rounds is a design that will not need
a fourth after it is built. Some of it is genuinely a cost of the two-agent review structure: every
document takes at least three sessions to close, because the loop is write → review → re-review, and
neither agent may approve their own state.

**The continuity file has become the largest single cost of starting a session.** My working-memory
document had grown to about 3,300 lines and 400 KB, and reading it is the first thing every session
does — which is in tension with the document's own purpose. Codex approved splitting it this
session, and I have done so; the permanent instruments now live in a separate file read on demand.

**One request has been open on you since Session 5, and I should say so plainly rather than let it
go quiet.** `director_requests.md` entry 1 asks for your review of the Claim Sheet — the project's
contract. It is **non-blocking by design** and the agents have never waited on it, which is exactly
why it has now been open for a hundred sessions without anyone mentioning it in a progress report.
It is still worth your time whenever your schedule allows: it is the checkpoint where a course
correction is cheapest, and the reading path built for it starts with `Accessible Claim Sheet.md`
rather than the technical contract. Nothing else is on you, and I would rather say that than
manufacture a request.

**One limitation is disclosed rather than closed, and it is worth your knowing about.** Fifty-five
model checkpoint files are deliberately excluded from the repository because of their size. Our
verification steps authenticate them by fingerprint, which means a stranger on a clean machine
cannot re-run one of the packet's later steps — they can rebuild the models, but a rebuilt model
that differs by a single byte does not reproduce our analysis, it produces a different one. We chose
to state this honestly rather than write a recovery procedure that reads like a guarantee we cannot
make.

---

## The verification artifact

No change to report this stretch. The Slot 8 verification path — the hands-on thing that will let
you check the result without reading the technical report — is unchanged since the last report, and
manufacturing an update for it would be exactly the failure mode the playbook warns about. It will
move when there is a rung-2 result to verify against.

---

## What the next stretch of work looks like

1. **Close the rung-2 design loop.** Codex re-reads the state I handed back today. If it approves
   the same bytes, the design is frozen.
2. **Write the rung-2 model and its tests.** That is the *only* thing a closed design authorizes —
   not the experiment, not the analysis.
3. **Then, as four further separately reviewed steps:** the program that runs the fits; a dry-run
   plan reviewed before anything executes; the twelve fits themselves (about nineteen minutes) under
   an explicit two-agent authorization; and a separate read-only analysis program.
4. **Only then** do we read the result, jointly, against the table that is frozen today.

That is deliberately six or seven sessions of work for nineteen minutes of computation. The reason
is that every one of those separations has already caught something real: it was a review of a
displayed command that found the command could not run, and a review of a reader script that found
it could not have read the very file it existed to read.

---

## One last thing, because I think it is the honest summary

The most important sentence in this report is not about the model. It is this: **we measured our own
instrument, found it was five times too coarse for the question we had pointed it at, and responded
by changing what we were building rather than by making the number look better.**

That is not a result. Nobody will cite it. But if this project eventually produces something worth
believing, it will be because of decisions like that one, and I would rather you saw them happening
than only saw the conclusion.

— Claude
