# Progress Report — Claude, Session 72

**Date:** 2026-08-04
**Covers:** my Sessions 65–72 (previous report: Session 64)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

Last report ended with a decision: before we could interpret the experiment we had
already run, we needed one more measurement — how the result changes with the weight the
robot arm is carrying. We had written the plan for that measurement as a frozen document,
and Codex had just built the program that would carry it out.

This report covers what happened to that program.

**It went through eight full rounds of adversarial review between the two agents, and
every single round found something real.** Then, this session, the review closed and the
program did the one thing it was allowed to do: it wrote out the complete measurement
plan, in full, at a cost of **zero simulation time**. That plan document now exists, I
have read it and checked its numbers independently, and it is waiting on Codex's own
read before either of us may authorize the measurement itself.

The honest headline for you is two-sided, and I want both halves in the same breath:

- **What we bought.** The program that will record roughly an hour of irreplaceable
  simulation now cannot lose that record, cannot quietly write your machine's folder
  names into a public results file, and cannot silently reuse one experiment as another.
  Each of those was a real, demonstrated failure at some point in the last eight rounds.
- **What it cost.** Eight of my sessions and eight of Codex's went into a program rather
  than into science. Zero simulations ran. The lifetime total is still **151**, exactly
  where it was at the last report.

I think the trade was worth it, and I will show you the specific failures so you can
judge that for yourself rather than take my word. I will also flag the point at which I
think it stopped being obviously worth it, because I do not think that point is nowhere.

---

## The one idea you need for the rest of this report

Everything below turns on a distinction that sounds pedantic and is not:

> **The experiment is the simulation. The *result* is the file the program writes down.**

We are going to spend about an hour of computer time running 127 physics simulations of
a flexible robot arm carrying seven different weights. That hour is not repeatable in any
cheap sense — and more importantly, this project's entire promise is that a stranger can
check our work. A stranger cannot check a simulation that has already finished. They can
only check **the file it left behind**.

So the file is the deliverable, and the program that writes it is the instrument. If the
program writes the file wrong, or crashes before writing it, or writes it correctly but
with something in it that we cannot publish, the hour is spent and the result is gone. In
that light, "we spent eight sessions hardening a file-writer" reads a bit differently.

Two smaller ideas you will want:

**Pre-registration.** We write down what we are going to measure, and what would count as
success or failure, *before* we run it — so we cannot look at the data and then decide
what we were testing. This is standard practice in fields that have been burned by the
alternative; the [Center for Open Science](https://www.cos.io/initiatives/prereg) has a
short explanation. The plan document this session produced is the pre-registration made
machine-readable.

**Mutation testing.** The way we check that our *tests* are real. You deliberately break
a line of the program and see whether any test complains. If none does, that line was
never actually being checked — the tests were watching, but not at that spot.
[Wikipedia has a good overview.](https://en.wikipedia.org/wiki/Mutation_testing) This is
the instrument that found most of what follows, and it is why several rounds report
"nothing was broken, but nothing was watching either."

---

## What happened, round by round

The two agents alternated. One would hand over a state it explicitly approved; the other
would review it, find something, fix it, and hand it back. Eight complete round-trips.
Here is what each one actually found, in plain terms.

**Round 1 (my Session 65) — three failures in the part of the program no test had ever
entered.** Before the measurement starts, the program is supposed to re-run one
already-completed simulation and check it comes back byte-for-byte identical — proof the
instrument still behaves. It was asking for the *wrong* completed simulation: someone had
re-typed a run's name by hand and typed a neighbour's. Every attempt to execute would
have failed that check. Worse, when that check fails the program is supposed to write
down what happened and how much simulation it had spent — and instead it crashed on a
programming error and wrote nothing, losing exactly the record the check exists to
produce. Third: one class of error could escape mid-run and discard the evidence of every
simulation already spent, up to about an hour of it.

All three lived in the program's *exit paths* — the code that runs when something has
gone wrong. That is not a coincidence. Testing a normal function is cheap; testing "what
does the program write when it dies at step 94 of 127" is expensive, so nobody writes
those tests, and those are precisely the paths whose whole job is to preserve evidence.

**Rounds 2–4 (Sessions 65–66) — six more, including one that was a genuine surprise to
me.** The program has two rules that are each obviously correct: *always write down what
happened*, and *never put a machine-specific file path into a published record*. The
second is enforced by a guard that refuses. Everywhere the two rules do not meet, both
look right. Where they meet — a failure record that has to quote a filename — the
prohibition fired *while writing the record* and destroyed it. Nobody had ever written
the two rules down as a pair.

**Round 5 (my Session 67) — the fix for a class, instead of another example.** The
program cleans machine paths out of error messages by recognising a list of path
spellings. The guard that later refuses a bad record asks a different question, using the
operating system's own path parser. Those two disagree on inputs nobody had thought to
write down, and *every* disagreement destroys a record. Two spellings had already been
added in two consecutive sessions — each a correct fix to a real bug, and each one an
example rather than a rule, so the class stayed open both times.

The fix was to stop enumerating: make the cleaner *end by asserting the guard's own
question*, then check it by brute force. I generated 37,448 different message strings in
0.27 seconds and found **1,358 counterexamples** that three sessions of careful reading
had not found. Two of my own first attempts at the fix were also wrong, and the same
enumeration caught both in under a second.

**Rounds 6–8 (Sessions 68–71) — the same class, one layer further out each time.** A
repair that stopped a path being published turned out to make the *whole error message*
discardable. A rule that handled Windows drive letters handled a narrower alphabet than
the program's own documentation claimed. A path with a space in it — `C:\Program Files\…`
— slipped through, because the rule stopped at the first space.

Then the one I would single out. Round 7 found a **complete machine path published
intact**, and the reason is genuinely interesting: `https://host/folder/file` and
`\\host\share\file` are, to a pattern-matcher, *the same shape*. A URL and a Windows
network path are lexically indistinguishable. Every "clever" rule we had written to tell
them apart was secretly a decision about which names count as web addresses, with the
criterion left implicit — and the implicit criterion was "anything followed by a colon."
Stated out loud, neither of us would have agreed to that. Buried in a pattern, it
survived three rounds of review.

The honest fix was to stop being clever: **write the list of protected names down, put it
in a named constant, and disclose what falls off the end.** Codex then found that my
version of that fix recognised each name as a *suffix* of a longer word, so
`reasonhttps://host/…` was still protected. That is now closed.

**Round 8 (my Session 71) — the first round that found no broken behaviour at all.** I
could not find anything the program did wrong. What I found instead was that the list of
protected names — which is now the entire decision — had **nothing checking it**. Both
tests covering it were written to loop over the list itself, which means they simply
follow whatever the list says. I deleted names from it and the whole test suite stayed
green; I *added* a name and the suite stayed green while a complete machine path started
being published again. Adding a name is an ordinary future edit ("let's also protect
`ws`"), and it silently reopens the exact hole we had spent three rounds closing.

I want to be careful about how that round is described, because I was careful about it at
the time: **not one of my eighteen new tests failed against the state I was reviewing.**
They are coverage, not defects. Eighteen new tests look like eighteen new problems to
anyone reading quickly, and I said so at the top of my handoff rather than let the count
speak for itself.

Codex reviewed that round, agreed, and approved. **The loop closed at eight rounds.**

---

## Then the program did its job

With the review closed, exactly one thing became authorized: run the program in **plan
mode**, which spends no simulation at all and writes out the complete measurement plan.

I ran it this session. It produced a 5,386-byte document holding:

- the **seven payload weights** (0.025 kg to 0.200 kg) and which role each one is
  reserved for;
- the **ten damage levels** to be tested at each weight;
- the **eight random identities** reused across all seven weights, so that a difference
  between weights is a difference in *weight* and not in random noise (this is
  [common random numbers](https://en.wikipedia.org/wiki/Variance_reduction), a standard
  variance-reduction trick);
- **126 distinct simulations** plus one verification re-run — every cost, including the
  cost of every possible early stop, fixed in advance;
- and the **anchor**: which of the earlier experiment's ten results this new run must
  reproduce for us to believe the rebuilt instrument at all. Nine of the ten are
  required; one is deliberately excluded because the original missed its threshold by
  2.1%, and requiring a new run to reproduce a 2.1% margin is requiring it to reproduce
  noise.

**It cost nothing.** Three consecutive runs took 0.38, 0.36 and 0.37 seconds. A single
simulation takes about 26 seconds. The program does build eight copies of the robot's
body — to confirm each weight actually reaches the physics model — but it steps none of
them, and the clock proves it.

**I checked it rather than reading it.** The plan publishes a
[SHA-256](https://en.wikipedia.org/wiki/SHA-2) fingerprint identifying all 126 planned
robot bodies. Rather than trust the program that computed it, I rebuilt all 126 from the
plan document's *own published fields* with separate code, and re-derived the
fingerprint: identical. Every cost, every threshold, the anchor split, and the identity
scheme all re-derived the same way. I also scanned all 285 strings in the file for
machine paths with a matcher written from scratch for the purpose: zero, and not a single
backslash anywhere in the file.

One more property, which matters more than it sounds: I ran the plan three times — twice
here, once from a complete copy of the project at a totally different folder path — and
got **byte-identical files** all three times. The fingerprint identifies the *document*,
not the copy. That is what makes it safe for the next step, where both of us sign an
authorization that names that exact fingerprint.

---

## What isn't working, and what I would want you to push back on

**The obvious one: eight of my sessions produced no science.** Sessions 65 through 71
went entirely into one program. Some of that is unambiguously good — the round-1 failures
would have cost real simulation time and produced no record. But by rounds 7 and 8 we
were reviewing a **text-cleaning routine**: the code that strips folder names out of
error messages. That is a long way from robot proprioception, and I do not want to
present it as though it were the same thing.

My honest defence is narrow: that routine is the thing standing between an hour of
simulation and a publishable file, and it published a complete machine path as recently
as round 7. My honest concession is that a project with a deadline would have stopped
around round 5, accepted a disclosed limitation, and moved on. We do not have a deadline,
which is the strategy working as designed — but it is worth you knowing that the strategy
has a cost and this is what the cost looks like.

**The trigger that was supposed to stop this never fired, and it was right not to.** We
have a rule: escalate to you when a round re-argues something already settled. Not one of
the eight rounds did — every round accepted the previous round's findings in full and
blocked on new, measured evidence, each time one structural layer below the last. So the
rule held. But eight rounds is the longest loop this project has had, and if the next
review round on the plan document also finds only coverage rather than defects, I have
written into my own notes to **close it rather than hunt for a ninth**.

**Still waiting on you, and still not blocking anything:** `director_requests.md` entry 1
— the Claim Sheet review — remains unanswered from Phase 1. It is explicitly
non-blocking and the agents have kept working, so this is a note rather than a request.
Nothing else is waiting on you.

**One documentation wrinkle I chose not to fix.** The frozen plan document says in one
place that "the plan artifact must carry the executor's own count" of elapsed time. A
plan spends no simulation and has no executor, so there is nothing to carry; the
requirement is discharged in the *results* file, where it belongs. I read it as a slip of
the word "plan" for "result", and I have recorded it rather than proposing a version bump
of a frozen document over a wording slip. Codex may disagree, and if it does, its version
wins rather than trading another round.

---

## The verification artifact

No change this session, and I am not going to manufacture one. Your hands-on verification
path (Claim Sheet Slot 8) is still where it was: it lives inside the Reproducibility
Packet and gets built as the measurements that feed it arrive. This session produced a
plan, not a result, so there is nothing new for you to hold.

What I will say is that the plan document is, unexpectedly, a small piece of verification
infrastructure in its own right. Everything in it re-derives from its own contents — I
demonstrated that this session with independent code. If you ever want to check that we
did not quietly change the experiment after seeing its results, that file plus its
fingerprint is how you would do it.

---

## What is next

1. **Codex reads the plan document independently.** That is the next turn, and it is
   required — the frozen document says the plan is "read by both agents", not one.
2. **A separate joint authorization** naming the plan's exact fingerprint, and explicitly
   authorizing one verification re-run. Neither agent may issue this alone, and I was
   careful this session not to write anything that could be read as half of it.
3. **The measurement itself.** 127 simulations, 53–58 minutes, run as a background job.
   It stops early and writes down what it has if the instrument disagrees with the earlier
   experiment, or if the payload weight turns out not to reach the physics at all.
4. **Amendment A2** — the Claim Sheet change this whole detour exists to inform — is
   still undrafted and still blocked. It is blocked on the measurement, which is the
   correct order: A2 currently has to *assume* the answer this measurement will supply.

If the next two steps go smoothly, the next report should be able to tell you what
happens to the robot's structural signal as you hang more weight on the end of its arm —
which is the question this eight-session detour was for.
