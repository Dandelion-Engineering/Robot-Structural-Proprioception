# Progress Report — Claude, Session 136

**Written:** 2026-08-14 15:52 PDT
**Covers:** my Sessions 129 through 136
**Previous report:** `Progress Report Session 128.md` (covered S121–S128)

---

## The short version

Eight sessions ago the demo screen for this project existed but was wired to nothing —
it could draw a robot, a timeline and a diagnosis, but every number on it was invented
by the packet. Since then I have built the figure set that proves the screen works,
written the contract that will one day connect it to a real result, spent five sessions
arguing that contract into a shape neither of us could break, and — this session —
started building the code that enforces it.

Two things in this stretch are worth your attention more than the code is.

The first is that **you changed how we review things, and it worked immediately.** The
old loop had no stopping rule, and it produced a seven-round design review. Under the
new rule the same disagreement closed in one round. I will show you the number below,
because it is the clearest evidence in this project that a process change did something.

The second is that **a test suite of mine passed 209 times for the wrong reason and I
only found out because I tried to break my own code on purpose.** That is the most
useful thing that happened this session and I want to explain it properly, because it is
the kind of failure that does not announce itself.

---

## A little background, so the rest reads cleanly

**What the "verification artifact" is.** Slot 8 of our Claim Sheet is a promise we made
before doing the work: that when this project produces a result, we will also produce
something *you* can put your hands on to check it, without reading the technical report.
For this project that is an interactive screen — a menu of body-change cases, a picture
of the simulated arm, a timeline, and what each of the two competing methods concluded.

**Why it is not connected to anything yet.** Deliberately. The screen must never be the
place where a result is *discovered*; it can only be the place where a result already
established elsewhere is *displayed*. If the demo's first run were also the first time
anyone looked at the held-out data, then every safeguard this project maintains —
deciding what counts as success before looking, using each dataset once, leaving the
final test split untouched — would have been quietly routed around by a picture. So the
screen is currently wired to a synthetic fixture that is labelled, on screen, as
fabricated.

**What a "connection record" is.** It is the document that will one day connect the
screen to a real result. Think of it as a numbered manifest: it names every single file
the screen is allowed to open, and the fingerprint each of those files must have. The
program checks the manifest against reality and refuses if anything disagrees. It cannot
go looking for files, cannot fill in a blank, and cannot open anything the manifest does
not name. If you would like the general idea behind fingerprinting a file this way, the
mechanism is a
[cryptographic hash](https://en.wikipedia.org/wiki/Cryptographic_hash_function): a short
string computed from a file's exact contents, where changing one byte changes the
string completely.

---

## Where the project stands

Still **Phase 2 (execution)**, and the honest headline has not changed: **the scientific
question is not answered and no result exists.** The final configuration is not frozen,
no model capacity has been selected, no thresholds have been calibrated, and the
`pilot`, `val` and `test` datasets have never been read — not once, in any session, by
either agent. That last number is the one I would check first if I were you, and it is
zero.

What *has* moved is the verification lane. Of its four steps:

| step | what it is | state |
|---|---|---|
| 1 | the design of the screen | closed, both agents approved |
| 2 | the screen itself and its tests | closed, both agents approved |
| 3 | the fixture figures a reader can look at today | closed, both agents approved |
| 4 | connecting a real result | design closed; the code is now half-built |

Step 4 is itself split into six pieces. The first — its design — closed today. The
second — building the code — is what I started this session. The remaining four are all
blocked on scientific work that has not happened yet, and that blocking is the point,
not an obstacle.

---

## What has been done since the last report

**Sessions 129 and 130 finished the screen.** I built the ten-file figure set that a
reader can open today: four body-change cases, each rendered at 300 dots per inch, with
the exact fixture seed recorded so anyone can regenerate them byte for byte.

One detail from that fixture matters more than it looks. When you build a synthetic
demo, the tempting mistake is to make the method you are hoping wins look good in every
panel. I deliberately did the opposite: of the four cases, one favours the structural
method, one favours the conventional baseline, and two are exact ties — including one
where the two methods produce *identical* tracking numbers but reach *different*
conclusions. A demo whose every panel flattered our own hypothesis would be the exact
misreading this whole design exists to prevent.

**Sessions 131 through 135 were the connection-record design.** This was five sessions
of two agents trying to break one document, and the honest accounting is that every
round found something real:

- the fixture we planned to check the robot's geometry against turned out to be
  incoherent for that purpose — its "how the arm is bent" data and its "where the
  arm's tip ended up" data are generated by two unrelated processes, so it can check
  storage and refusals but cannot check geometry;
- the design would have required a *test* to create a file named `config.json` inside
  the project — and that filename is our own token for "the configuration is frozen and
  the confirmatory work may begin." A test must not be the thing that manufactures the
  project's authority to proceed;
- and the fix for that, mine, quietly lost a guarantee: it proved the *rules* accept a
  frozen configuration without proving the *program* does. An implementation that
  refused every real configuration would have passed the whole test list.

**Session 136 — this one — built the first half of the code**, and handed it to Codex
for review.

---

## The process change, and the number

Your new review method arrived on 2026-08-14. Before it, an artifact review had no
stopping rule: the reviewer found a problem, the owner fixed it, the owner found a
problem in the fix, and so on. That is how the connection-record design reached round
seven. Every round found something real, which is exactly what made it hard to see that
the process was failing.

The new rule adds three things: a **Review Card** written before review begins, naming
what is being reviewed and what would count as a blocking problem; **one complete
findings list in round one** instead of serial discovery; and **at most three
round-trips**, with the explicit note that the limit never forces an approval.

The effect on my own behaviour was immediate and I can name it precisely. Codex handed
me a repair. I found a genuine gap in that repair. Under the old loop I would have
written it up as a new finding and handed it back — which is one more round. Under the
new one, the card told me I was the *owner* and this was my half of a round-trip, so the
obvious move was to fix it inside the state I approve and say exactly what I changed.
Same technical content, one fewer round. **The review closed in one round-trip instead
of an eighth.**

I also found a defect in the new machinery on its first use, which is worth reporting
because it is the kind that hides. The Review Card named the document under review by
its fingerprint — and the fingerprint it named **did not exist**. It shared its first
eight characters with the real one, which is exactly the width everything in this
project quotes. Nothing but asking the version-control system directly would have caught
it. Codex and I now name every reviewed state three ways and check each identifier
against the repository before the card governs anything.

---

## The thing that went wrong this session, and why I am glad it did

This session I wrote about 59,000 characters of contract code and about 50,000
characters of tests for it. All 209 tests passed on the first run.

That is not reassuring; it is a reason to check. So I did what this project always does
after writing tests: I broke the code on purpose, 44 different ways, and required the
tests to catch each break. The technique is called
[mutation testing](https://en.wikipedia.org/wiki/Mutation_testing), and the idea is
simple — a test that stays green when you delete the rule it claims to check was never
checking that rule.

**Five of the 44 breaks went unnoticed, and four of them were my own tests passing for
the wrong reason.**

Here is the clearest one. The contract refuses a manifest that ends with a stray
newline character. My test broke the file that way and then checked that the refusal
message contained the word "newline". But a *later*, different rule also refuses that
file, and *its* message happens to say "no trailing newline" too. So when I deleted the
newline rule entirely, the file was still refused, the message still contained the word,
and the test still passed. The rule could have been removed from the program without a
single test noticing.

Three others had the same shape. The fifth was different: a guard that no valid input
can ever reach, which I had left in as a second line of defence — and a guard nothing
can break is a guard nothing checks, so I now exercise it directly.

I want to be straightforward about what this means. My tests were wrong in a way that
made them *look* stronger than they were, and no amount of re-reading them would have
found it — only running the experiment did. This project has learned some version of
that lesson several times now, and each time it arrives from a slightly different
direction. After the fixes, all 42 real breaks are caught, two deliberately harmless
changes still pass (which is how I know the instrument is not just reporting everything
as caught), and the whole sweep gives identical results run twice.

---

## What is working

- **The refuse-first discipline.** The program's default answer is no. It authenticates
  before it interprets, and it interprets before it opens anything. Every path it will
  ever touch has to be named in advance, with a fingerprint.
- **Splitting big builds into reviewable pieces.** I deliberately did not hand Codex the
  whole adapter this session. Half of it, bounded, with an explicit statement that the
  step does not close until both halves are reviewed.
- **The two of us finding real things in each other's work.** Not one round in the last
  eight sessions was ceremonial.

## What is not working, or at least not yet

- **The scientific lanes are all spent or shut.** Everything that could be measured
  under the current approved plan has been measured. Real progress now needs the
  configuration freeze, and that needs decisions that are not mine alone.
- **Review is where nearly all of my time goes.** Five of these eight sessions produced
  no code at all — they produced a better document. I think that was right for a
  document that governs what may open the held-out data, and I also think it is a cost
  worth you seeing plainly rather than buried.
- **One open request to you, unchanged.** Entry 1 in `director_requests.md` — your
  review of the Claim Sheet — is still awaiting a reply. It is explicitly non-blocking
  and we have kept working; I mention it only so it does not vanish. Entry 2, the
  Windows security block that made our test suite temporarily unmeasurable, was resolved
  by the repair agent you authorized, and the standing procedure it produced is now
  part of how we work.

## The verification artifact, since there is genuinely something new

There is something you can look at today, and it is worth being precise about what it
is and is not.

`Reproducibility Packet/results/verification_fixture/` holds ten files: four rendered
cases plus the machine-readable scenes behind them. Every one is labelled, on the image
itself, **"SYNTHETIC — NOT A RESULT."** That label is not modesty. Every number in those
pictures was fabricated by the packet on purpose, and none of them came from the
simulated robot.

What they demonstrate is that the surface works: the menu, the timeline, the arm
drawing, the two methods' conclusions side by side, and the honest handling of the
awkward cases — a method that abstains, a method that is confidently wrong, and a case
where the two methods are literally indistinguishable. When a real result exists, the
same code will draw it, and the label will change to say which result, from which
dataset, established when.

## What the next stretch of work looks like

1. Codex reviews the contract I handed over today. If it holds, I build the second half:
   the part that actually opens files — configuration, dataset audits, the per-case data,
   the geometry check — plus a purpose-built synthetic fixture that is coherent enough to
   check the geometry against, which the existing one is not.
2. That build closes step 4b. It authorizes nothing further; a built tool is not a
   permission.
3. Everything after that waits on the science: the configuration freeze, the capacity
   choice, the threshold calibration, and a real result to display.

I would rather this lane arrive late and unable to fabricate anything than arrive early
and be the place a result quietly came from.

---

*Counters, for the record: 278 simulated rollouts, 67 model fits, 67 saved checkpoints,
and zero reads of the pilot, validation or test data — across the whole project, both
agents, every session.*
