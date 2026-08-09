# Progress Report — Claude, Session 104

**Date:** 2026-08-09 16:26 PDT
**Covers:** my Sessions 97–104 (previous report: Session 96)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The last report ended with a program that was written but had never been run against real
data, and a hole in it that had just been found and closed. These eight sessions ran it.

The capacity sweep — the measurement that trains the same experiment at five different
network sizes to find out whether the network being too small was why the first result came
out the way it did — **executed, produced fifty trained models, and has now been read.**

The reading is the part worth your attention, and it is not the shape anyone expected:

> **The interpretation for this measurement was written and frozen back in Session 88, before
> a single one of these fifty models existed. It contains six rows. Each row says: if you see
> *this*, you may say *that*, and you may not say *this other thing*. When we applied it to
> the finished numbers, exactly one row matched — and the sentence it licenses is that the
> curve does not have a readable shape. No trend statement of any kind is permitted.**

That is a real outcome, not a failure to get one. The instrument reported its own limit
instead of producing a confident answer it could not support. And there is a specific detail
underneath it that I think is the most valuable thing this project has produced so far about
its own method — I get to it below.

Nothing has been spent on the reserved data. Still zero simulation rollouts beyond the 278
already on the books, zero reads of the pilot, validation or final-test sets, no chosen
network size, no threshold, and no final configuration.

## The one idea you need: what pre-registration actually buys

Most of what has looked like bureaucracy in this project comes down to one idea, and this
report is the first time it has paid out visibly.

When you run an experiment, you get numbers. Then you have to say what the numbers mean. The
trap is that those two steps happen in the same head, in that order — so the meaning gets
chosen *after* the numbers are visible, and people are extraordinarily good at finding a
reading that flatters what they were hoping for, without any dishonesty at all. This is not a
character flaw; it is well documented and has a name, and the standard fix is called
**pre-registration**: you write down what each possible outcome will mean *before* you can
see which one you got. ([A plain overview of pre-registration and why it works.](https://www.cos.io/initiatives/prereg))

In Session 88 I wrote that document for this measurement. It is a six-row table. Each row
names an exactly-defined observation — not a vibe, an observation a program can compute — and
then says, in plain prose, what may be said if that observation occurs and what may not.
Codex reviewed it. It was frozen. Then, sixteen sessions later, the numbers arrived and we
applied the table to them mechanically.

## What the reading came out to be

Exactly one row matched. What it licenses, verbatim:

> the paired curve does not have a readable shape at five points and five seeds

and it explicitly forbids **any trend statement**.

In ordinary language: we trained the experiment at five network sizes, five random restarts
each. If network size mattered in a simple way, the difference between the two sensor suites
would move in some direction as the network got bigger — up, down, or flat. It doesn't do
any of those. It goes up and down. At five sizes and five restarts, that is not enough
resolution to call a shape, and the frozen table says so and forbids us from pretending
otherwise.

The five per-size numbers themselves are real, audited, exact, and published in the artifact.
We may quote them. We may not connect them into a line.

## The near-miss, which is the actual finding

Here is the detail I would most like you to take away from this report.

One of the six rows — one that did **not** match — would have licensed this sentence:
*"across this band, the difference did not move by more than the anchor's own seed spread."*
That is a comfortable, reasonable-sounding sentence. It is very close to what someone
eyeballing these numbers would say. I believe it is the sentence that would have been written
if the interpretation had been chosen after seeing the curve.

It fails **two of its three conditions, independently**. The curve's shape is not
flat-or-declining, and the spread comparison comes out the opposite way from what that row
requires. Either failure alone blocks it.

So: the pre-registration blocked, twice over, precisely the sentence that hindsight would
have produced. It did not block it because someone was being careful in the moment — it
blocked it because the choosing had already happened sixteen sessions earlier, in a document
that could not know what it was going to block. **That is the whole argument for the method,
and this is the first time in this project it has been demonstrated rather than asserted.**

## What these eight sessions actually did

**Sessions 97–99 — hardening before spending.** The program had never touched real data. Three
sessions of adversarial review and mutation testing went into it first: deliberately breaking
the program in specific ways and checking that the test suite notices. A test suite that
passes on a broken program is worse than no test suite, because it produces confidence.

**Session 100 — the authorization, and a failure of my own.** Running the sweep required both
agents to separately, explicitly authorize the exact command, on the exact code, against the
exact inputs, writing to one exact destination. I issued my half. I also, in the same session,
put a timestamp on a message that was sixteen minutes in the future — because I stamped the
header while *drafting* and never re-read the clock at the moment of *writing*. That matters
because those timestamps are how you audit the order our sessions happened in. I built a gate
that now refuses any message whose header time disagrees with the clock at the moment the
bytes move. It has held every time since. (There is a postscript to this below.)

**Sessions 101–102 — the run happened, and then the reader was built and broken.** The sweep
ran: forty new models trained, ten existing ones reused, forty-two checkpoint files written,
zero simulation. Then the *reader* — the separate, read-only program that turns those fifty
models into the descriptive numbers — went through review, and I found two real defects in
it. The important one: the ten reused models and the forty new ones stored their scores in
**different numeric precisions**, and the reader demanded exact equality across both. It
would have refused to complete the read it exists to perform — on every single run, for a
reason that had nothing to do with the science. Both defects were repaired and both repairs
survived deliberate attempts to break them.

**Session 103 — the last checks before the spend.** Thirty-nine checks that all sit *below*
the spend, run *before* authorizing rather than in exchange for authorizing. That distinction
is a rule this project bought with a real failure: a check that runs after a spend is a cost,
not a check.

**Session 104 (this one) — the independent audit, and the reading.** Codex ran the reader
once and approved its own output. My job was the other half: an independent audit of the
exact bytes. Seventy-three checks, none of which imported the program that produced the file —
because auditing a computed file by re-running the program that computed it proves nothing.
Every number was re-derived from the frozen design's own text. All fifty model files were
re-fingerprinted from disk. Then twelve deliberately damaged copies were run through the same
audit under a scratch directory, and every one was caught by the specific check that names
the damage. Only then did agreement count as evidence. The audit found nothing wrong. Both
agents now approve the same bytes, and the interpretation was applied.

## What was unexpected

**That the answer would be "the instrument can't read this."** I expected one of two shapes:
the difference closes as the network grows (suggesting the first result was partly a
size artifact), or it doesn't (suggesting it wasn't). The actual outcome is a third thing —
five sizes and five restarts are not enough to distinguish those two stories. That is
genuinely useful information about the design, and it is information we would not have if the
table had been written afterwards, because afterwards there would have been a story.

**That the saturation guard never engaged.** The design contained a safeguard against a known
trap: with only 152 training examples, a big enough network memorizes them perfectly, both
sensor suites hit a ceiling, and the difference between them collapses to zero for reasons
that have nothing to do with information. The guard watches for that. It never fired — no
size in this range was anywhere near that ceiling. So the domain was fully readable and the
read still came out unreadable. The limit is resolution, not saturation.

## What is working

- **The two-agent review loop is still finding real things.** Every round in this stretch
  found something, and Codex's forward correction this session caught an error of mine before
  it cost anything (I stated a directory had three entries; it has four — I had listed the
  things I was thinking about and called it a census).
- **The mutation discipline.** Nothing gets believed here because it passed a test. It gets
  believed after the test is shown to fail on a deliberately broken version. That has now
  caught defects in the executable, in the reader, in the test fixtures, and in my own audit
  probes.
- **The spend ledger.** Every session states exactly what it consumed. Across 104 of my
  sessions the reserved comparison data has been read zero times.

## What is not working, honestly

- **This measurement did not answer the question it was designed to answer.** It answered a
  narrower one: whether five widths and five seeds can resolve the shape. They cannot.
  Whether to spend more on this axis is now an open decision rather than an implied one, and
  the frozen design explicitly forbids treating this reading as permission for it.
- **The cost-to-science ratio in this stretch is poor and I want to say so plainly.** Eight
  sessions produced one 89,150-byte JSON file and one sentence of licensed interpretation.
  The rigor is real and I would not trade it away, but a director looking at eight sessions
  of my time is entitled to notice that most of it went into establishing that a measurement
  could be trusted rather than into making measurements.
- **Three Phase-3 assembly items are open** and none of them blocks anything right now: the
  Reproducibility Packet's README does not mention the capacity sweep at all; the fifty-five
  saved model files are deliberately not stored in the repository and have no documented
  recovery path for someone starting from a clean machine; and analyzer output files carry a
  "boundary" block whose zero-counts describe the *reader* rather than the *run*, which needs
  its scope named wherever it gets quoted.
- **A safeguard of mine had quietly expired.** The timestamp gate from Session 100 lived in an
  untracked scratch directory, and untracked scratch does not survive a session. I found out
  this session by going to use it and finding it gone. I rebuilt it from my own notes before
  writing anything and all three of this session's messages passed it — but a control that
  lives outside version control is a control that expires, and this one survived on the
  strength of a prose description rather than an artifact.
- **`director_requests.md` has nothing new for you.** No director-only blocker was hit in
  these eight sessions.

## The verification artifact

No change this stretch. The Slot 8 artifact — the thing built so you can check the result
yourself without reading the technical report — is not affected by a development-only
descriptive read, and I did not manufacture an update for it.

## What happens next

1. **Codex owes its half of the interpretation.** Applying the frozen table is a joint act;
   I posted mine and asked for its reading. If it reads the row set differently, that gets
   settled before either of us writes another line about this curve.
2. **The next step after that is genuinely undecided,** which is the correct state to be in.
   Going to bigger networks, or more restarts, or more sizes, each needs its own reviewed
   document and its own joint authorization. Nothing in this reading licenses any of them.
3. **Nothing downstream has moved.** The final configuration is still unfrozen, the reserved
   data is still unread, and the project's central question — whether structural sensing adds
   information beyond a conventional sensor suite — is still open and still unanswered.
