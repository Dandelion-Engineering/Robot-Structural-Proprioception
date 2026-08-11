# Progress Report — Claude, Session 120

**Written:** 2026-08-11 10:12 PDT
**Covers:** my Sessions 113 through 120
**Phase:** 2 (Execution)
**Previous report:** `Progress Report Session 112.md` (covered S105–S112)

---

## The short version

Over these eight sessions I built a second, larger, structurally different neural network for
the robot's self-diagnosis problem, ran it, and measured what it learned.

It learned less than the smaller one. On two of the four categories it was supposed to
distinguish, it learned nothing at all — a score of exactly zero, on every one of the ten runs.
Four of those ten runs performed exactly as well as a system that ignores its inputs entirely
and answers `sensor` to every question.

**And the most important thing in this report is that we had written down, in advance, that this
exact outcome could sneak past our success check.** It did. The check said "passed." The
pre-written warning next to it said, in effect, *"if this check passes, do not conclude the
network learned anything."* Both are now in the record, side by side, because that is what we
committed to before we knew which way it would go.

That is the session stretch: a null result we can trust, produced by a process that was built to
be trustworthy before the answer existed.

---

## What you need to know to follow this

Three ideas, and then the rest reads plainly.

**1. The four categories, and why "zero" means something specific.**
The network's job is to look at a window of the robot's sensor readings and say what is going
on: nothing wrong (`healthy`), a motor problem (`actuator`), a sensor problem (`sensor`), or a
structural problem (`structure`). We score it with something called
[F1](https://en.wikipedia.org/wiki/F-score), which combines two questions — when it says
`structure`, is it right? and does it find the structural cases that are there? — into a single
number between 0 and 1. An F1 of exactly 0 on a category does not mean "did poorly." It means
the network **never once** correctly identified that category.

**2. The majority-class baseline, which is the bar that matters here.**
Our 152 development examples are not evenly split: 96 are `sensor`, 32 `actuator`, 16
`structure`, 8 `healthy`. So a system that always answers `sensor` — no learning, no sensors,
just a fixed answer — gets 63.2% of them right. That number is the floor. Four of our ten runs
landed exactly on it, to six decimal places. Not near it. On it.

**3. Why we built a different network at all.**
The first network ("rung 1") reads its input the way you'd scan a long strip of tape — a stack of
[dilated convolutions](https://en.wikipedia.org/wiki/Convolutional_neural_network) that can see
1,023 samples back at once, but treats the whole window in one shot. The second ("rung 2") reads
it the way you'd read a sentence — a [recurrent network
(GRU)](https://en.wikipedia.org/wiki/Gated_recurrent_unit) that walks through the window step by
step, carrying a running memory, plus an attention layer that decides which moments mattered.
It has 219,018 adjustable parameters against rung 1's 39,594 — about 5.5 times as many.

The point was never "bigger is better." It was that the earlier capacity work left an honest
open question — *would a network with more capacity, or a different way of handling time, find
something the first one couldn't?* — and the only way to answer it was to build one and look.

---

## Where the project stands

Phase 2, execution. The capacity ladder for the diagnosis network now has **two rungs on it,
both fitted, both measured**. That is the concrete thing these eight sessions produced.

What is deliberately *not* concluded: we have not selected which network to use, have not set any
decision threshold, have not established anything about how either network performs on data it
has not seen, and have not said anything about the project's actual research question (whether
the structural-sensing suite beats the conventional one). Every one of those remains locked
behind its own gate, and this work opened none of them.

The shared configuration file that freezes the experiment's settings is still unfrozen, and the
untouched `test` data has still never been read — zero identities, zero payloads, every session,
without exception.

---

## What got done, session by session

The stretch has a clean shape: design, build, review, run, read, interpret — with an explicit
review round between every pair of steps, and neither agent allowed to move alone.

- **S113–S114 — the network itself.** Built the rung-2 architecture and 71 tests for it. Every
  figure in the design document was *rebuilt from the constructed network* rather than copied out
  of the design — parameter count, receptive field, layer census. Codex reviewed and we closed on
  the same bytes.
- **S115 — the runner.** The program that actually performs the twelve fits, plus 142 tests.
  Jointly approved in a single round, which was unusual enough to note.
- **S116 — the plan.** The runner first emits a plan: every arm it will fit, every file it will
  write, every input digest it will check, written to disk *before* anything expensive runs. I
  audited that plan with 132 checks plus a 23-of-23 mutation control; Codex audited it separately
  with its own 107-check instrument. Approved.
- **S117 — the run.** I ran 44 pre-authorization checks and issued my half of a two-part
  execution authorization; Codex issued the other half and ran it. **12 fits, 1,274.6 seconds,
  zero physical simulations.** Exit code `X_RUNG2_OK`.
- **S118 — the reader.** A separate, read-only program whose only job is to re-open the run's
  output, re-score all twelve saved networks from scratch, demand exact agreement with what was
  recorded, and then compute the summary. 103 tests. Codex approved my exact bytes with no edit.
- **S119 — the read, and the finding.** The reader ran once, in 11.97 seconds. I then audited its
  output with a 165-check instrument that shares no code with it. And that is where the
  degeneracy surfaced.
- **S120 — the interpretation, jointly.** Codex ran its own 853-check audit and approved the same
  bytes. I re-derived both interpretation conditions from scratch this session — 40 checks, plus a
  ten-mutant control — and we each applied the same two pre-written sentences. I then wrote the
  two new runbook steps into the reproducibility packet so an outsider can repeat all of it.

---

## What was found that we did not expect

**The rung-2 network scored zero on `healthy` and zero on `structure`, on all ten runs.**

Six of the ten found *something* — a non-zero score on `actuator` — and the other four found
nothing at all beyond answering `sensor` to everything. By contrast, the ten rung-1 runs carried
in the same document each have four non-zero category scores. The bigger network is not a
slightly worse version of the smaller one. On two categories it is a different thing entirely.

**Three things are true about this, and I want to be precise about each:**

*It is not a bookkeeping error.* The reader reloaded every one of the twelve saved networks from
their verified bytes and re-scored them from the raw data, then required **exact** equality with
the recorded numbers. That equality held ten times out of ten. The zeros are what the networks
actually produce.

*It is not a failure of the run.* We wrote three failure branches in advance — the fitting loop
failing to reproduce its reference, the run stopping early, and the training objective failing to
go down. None of them happened. Reading the failure path as "or anything else that looks
disappointing" would make the exercise of writing it in advance pointless.

*It is exactly the hazard we pre-declared.* This is the part worth your attention. The check we
used to confirm the run worked asks whether the training objective went down. But that objective
is a sum of several terms, one of which is a measure of how well the network estimates fault
*severity*. **The design document says, in writing, before any of this ran, that this term can
drag the total down without classification improving at all — and that passing this check is
therefore explicitly not evidence of learning.** All ten runs reduced the objective. All ten
also failed to learn two categories. The warning we wrote was not hypothetical.

**A second, smaller finding, and a real one for a company whose whole strategy is
affordability:** rung 2 carries 5.5× the parameters but costs roughly **12× per training step**.
A recurrent network's timesteps must be computed one after another; they cannot be spread across
processor cores the way the convolution stack can. On the hardware this project actually has —
one desktop — the architecture that *looks* like a modest step up the ladder is the expensive
one. That goes in the technical report as a finding, not a footnote.

---

## What's working

**The pre-registration is working, and this stretch is the proof.** Writing down what each
possible outcome would license — before any of it ran — meant that when a weak check passed, we
were not free to describe it as a success. The sentences we are permitted to say were fixed in
advance, and they are narrow: that a second rung exists and was fitted, and that the paired
comparison did not point the same way across the five random seeds. Nothing more. Both agents
applied that same pair independently, from the raw record, without either of us being able to
widen it.

**The two-agent review is working, and it keeps finding real things.** Not one artifact in this
stretch passed on the first look. And in both S119 and S120, my own audit instrument was wrong
before it was right — three times in S119, once this session. That is the point of building a
second instrument that shares no code with the first: it has to be able to be wrong in its own
way. An audit that passes on the first try usually has not been calibrated.

**Nothing expensive has been spent twice.** Every costly action in this project — the run, the
read — required two separate written authorizations and was structurally impossible to repeat,
because the destination directory is claimed exclusively and consumed. Three such destinations
are now spent. No retry has been taken and none is authorized.

---

## What isn't working

**We do not know why the network failed on those two categories, and we deliberately have not
guessed.** Capacity, training protocol, optimization, the data itself — any of these could be
the cause, and attaching one without measuring it would be exactly the kind of story-telling
this structure exists to prevent. The observation is recorded as what it is; the explanation is
future work with its own design and its own review.

**The class imbalance is a live suspect but an unexamined one.** Eight `healthy` examples out of
152 is very few to learn from. That is an obvious hypothesis and it is *not* in the record as a
conclusion, because nothing in this run tested it.

**The reproducibility packet has a disclosed hole.** The trained networks themselves — 67 files
now — are too large to commit and are not in the repository. Someone downloading the packet can
re-check every tracked record against every other, but cannot re-drive the reading steps without
those files. That is written into the packet as a limitation rather than papered over.

**One director-only item is still open, and it is the same one:** `director_requests.md` entry 1,
your review of the Claim Sheet, logged at Phase 1 close. It is non-blocking by design and nothing
is waiting on it. The reading path is still the same and still short: start with
`Accessible Claim Sheet.md`.

---

## The verification artifact

No change to report. The Slot 8 verification artifact — the hands-on thing built so you can
check the result yourself without reading the technical report — is still scheduled for the
confirmatory stage, and nothing this stretch touched it. I would rather tell you that than
manufacture an update.

What *did* change on your behalf is the reproducibility packet's runbook: it now carries two new
steps covering the rung-2 run and its reading, with the exact commands, the exact file digests,
and — under a heading that says what it is for — the zero-scores finding written out in full,
placed so that a reader cannot encounter the licensed sentences without also encountering it.
That edit is with Codex for review as I write this.

---

## What's next

The immediate next stretch is small and mostly administrative: close the review round on those
runbook steps, and then decide together whether the public project log gets an entry for this
result. My own view, already on the record, is that it should — the result is now jointly
interpreted and closed, and a public log that carries a plan but not the run it produced is
falling behind the work.

After that the open question is what rung 2's zeros mean, and the honest answer is that we do not
yet know what the right next experiment is. It is not automatically "try a third architecture."
It might be a much narrower question about the class imbalance, or about whether the training
objective's severity term should be weighted differently, or whether the window of sensor data we
feed the network is the right one. Whatever it turns out to be, it will be designed and reviewed
before it is run, and it will not be selected by trying things until one of them looks better —
that is protocol selection, and the contract forbids it.

Nothing about the project's central question has been answered by this stretch, and nothing about
it has been foreclosed either. What we have is a second rung on the ladder, an honest measurement
of what it does, and a record that a stranger could check.
