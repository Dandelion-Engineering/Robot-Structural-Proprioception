# Progress Report — Claude, Session 144

**Written:** 2026-08-16 16:16 PDT
**Covers:** my Sessions 137 through 144
**Previous report:** `Progress Report Session 136.md` (covered S129–S136)

---

## The short version

Eight sessions ago I had just started writing the code that will one day connect this
project's demo screen to a real scientific result. That code is now roughly half built and
the finished half is approved by both agents.

But the half that is built is not the thing worth your attention in this stretch. Three
other things are.

**One: we built the obvious fix, measured that it would have destroyed three finished
experiments, and threw it away.** Codex found a real hole in my code, agreed with me about
where the repair belonged, and I went and built the repair exactly there. Then I measured
what it did. It broke 52 tests and — much worse — it made two finished analysis programs
refuse to read three completed runs that this project is not allowed to re-run. I reverted
the whole thing and rebuilt the fix somewhere else. That is the single most useful hour of
the eight sessions, and it is entirely a story about measuring something we both already
agreed on.

**Two: a test suite of mine passed 341 times for the wrong reason, and the thing that caught
it was the same instrument that caught the last one.** In session 138 I discovered that my
tests would have stayed green on a version of my code that accepted a four-thousand-character
filename where it should have accepted 255. This is the second consecutive report in which I
have had to tell you that. I want to explain why it keeps happening rather than promise it
won't.

**Three: the process change you directed is written down and has not had to fire yet.** The
review method now has a defined ending — a ladder that says what happens when two agents
reach the round limit still disagreeing. Codex and I reconciled it, I wrote it into the
playbook, and in the eight sessions since, four separate reviews have closed without needing
it. That is the outcome you'd want, though it does mean the mechanism itself is still
untested in anger.

**And one honest thing that is neither good nor bad, just true: I have spent eight
consecutive sessions without running a single scientific measurement.** Zero simulations,
zero training runs, zero reads of reserved data. There is a good reason and I'll give it,
but you should hear the number first rather than find it buried.

---

## Background, so the rest reads cleanly

You have seen most of this before; skip ahead if it is familiar.

**What we are building right now.** Slot 8 of our Claim Sheet is a promise we made before
doing the work: when this project produces a result, we will also produce something *you* can
put your hands on to check it, without reading the technical report. Ours is an interactive
screen — pick one of several body-change cases, scrub a timeline, watch the simulated arm
move and see what each of the two competing sensor setups concluded.

That screen exists and works. Today every number on it is invented by the packet, and each
picture says so in red. The work of the last eight sessions is the **connection**: the code
path by which a real, already-established result could reach that screen. Not the result —
the plumbing.

**Why the plumbing is this careful.** Because the demo must never be the place where a result
is *discovered*. If the screen's first run were also the first time anyone looked at the
held-out data, every safeguard this project maintains would have been quietly routed around
by a picture. So the connection is built to refuse: it opens only files that a separately
reviewed document names in advance, and it checks each one against a fingerprint recorded in
that document before it interprets a single byte of it.

**What a "fingerprint" means here.** We use [SHA-256](https://en.wikipedia.org/wiki/SHA-2), a
standard cryptographic hash: run a file through it and you get a 64-character string that
changes completely if any byte of the file changes. It is the ordinary tool for "is this the
same file I was promised?"

---

## The thing worth your attention: a repair we built and then undid

### What Codex found

My code checked each file's fingerprint before using it. Codex looked at *how* and found the
gap.

The packet has an older, already-approved piece of code for loading scientific data. It works
like this: open the file, compute its fingerprint, compare it to the expected one — and then,
if it matches, **open the file again** to actually read the contents.

Those two opens are the problem. Between them, the file on disk can change. The version you
fingerprinted and the version you used are not guaranteed to be the same version. The security
literature has a name for this shape and a catalogue entry:
[time-of-check to time-of-use](https://cwe.mitre.org/data/definitions/367.html), CWE-367. It is
one of the classic ways a check that looks airtight turns out to be decorative.

Codex demonstrated it rather than describing it: a payload swapped between the two opens was
accepted, and its values were handed back as authenticated. My chain inherited the flaw for
free, because I was calling that older code.

### Where the repair obviously belonged

Both of us agreed: fix it in the two utility files that own the rule. One open, one read,
fingerprint the bytes you actually have in your hand. Codex formally accepted widening the
review's scope to cover those two files. That is a considered agreement between two reviewers,
in writing, before any code was touched.

So I built it.

### What the measurement said

Then I ran the tests. **52 failed, 25 more errored.**

The reason is a mechanism this project built on purpose, quite a while ago, and I had
forgotten how far it reached. When we run a real training job here, the program records a
fingerprint of *every source file that participated in it* — a "code identity." Later, when a
read-only analysis program goes to interpret the results of that run, it re-computes those
fingerprints and refuses to proceed if any of them changed. The point is to make it impossible
to quietly rewrite the code that produced a result and then reinterpret the result as though
nothing happened.

Those two utility files are in the list. They are two of the eight files whose fingerprints are
recorded inside three separate already-approved documents: a training ledger, a model-size sweep
plan, and a second-architecture escalation plan.

So my correct, agreed, well-motivated repair had this consequence: **two finished analysis
programs would have refused to read three completed runs.** Those three runs cost real compute,
were authorized exactly once each, and this project has no authority to re-run them. The
permissions are spent. A retry would need a fresh plan and fresh joint authorization, and none
is being sought.

I reverted every byte of it and verified all four affected files were bit-for-bit identical to
Codex's own recorded baseline.

### Where the repair actually went

Into a **new file** that no recorded identity contains. It reuses every rule from the closed
utilities — it even inherits from the old loader class rather than reimplementing it — and
restates only the mechanical business of reading. Tests hold the new code equal to the old code
wherever they overlap, so the two cannot drift apart.

And I added a test whose entire job is to make a future session hit this wall in a cheap place:
it reads the three approved documents, extracts the recorded fingerprints of those two files,
and fails if either file has changed. Someone six months from now who thinks "these two modules
have duplicated logic, let me tidy that up" gets a failing test with the reason attached instead
of three unreadable runs.

### Why I'm telling you this at length

Because the part that went right is not the fix. Both agents had already reasoned their way to
the right-looking answer and signed off on it. **The only thing that stopped it was building it
and measuring it.** A review is two smart readers agreeing; it is not a measurement, and this
stretch produced a clean example of the difference.

---

## The second thing: my tests keep passing for the wrong reason

### What happened in session 138

I finished a piece of the connection code and its test suite: 341 tests, all green, green again
under a stricter interpreter mode, and green as part of the packet's full 2,578-test run.

Before handing it over I ran a **mutation control**. The idea is simple and slightly
adversarial: deliberately damage your own code in a specific way, then check that your test
suite goes red. If your tests stay green, they were not actually testing that thing.
[Mutation testing](https://en.wikipedia.org/wiki/Mutation_testing) is a real and fairly old
technique; it is not widely used because it is expensive, and it is exactly the kind of expense
this project can afford because we are not in a hurry.

Twenty-five deliberate faults. Twenty-four caught. One survived.

The survivor: I raised a length limit in my code from 255 characters to 4,096. Every test
stayed green.

The reason is worth understanding, because it is subtle and it is a mistake anyone would make.
My tests were written to say things like "a name one character over the limit must be rejected."
That reads as careful. But "one character over the limit" is computed *from the limit* — so when
I moved the limit, the test inputs moved with it. The suite was faithfully testing the
*relationship*, which was never in doubt. It was testing nothing at all about the *value*, which
is the only part a human reviewer cannot check by reading the code.

255 is not arbitrary. It is the maximum filename length on essentially every filesystem this
packet could land on. **341 green tests would have stayed green on a module that accepted a
four-thousand-character filename** — which would fail on a stranger's machine, which is precisely
the failure our reproducibility standard exists to prevent.

I rewrote every length in those tests as a literal number, and added one test that pins both
limits to 255 and 250 with the reason attached.

### Why I am not promising it won't recur

Because it already has, in a different costume. **The mutation sweep has now changed my tests
rather than confirming them on six consecutive builds.** Session 136: four tests asserted a word
that also appeared in a later check, so deleting the code under test left the suite green.
Session 138: the limits above. Session 142: a test that fired before both operations it was
meant to separate. Session 143: two more tests measuring nothing.

Six for six is not a run of bad luck; it is a property of how tests get written. A test is
written by the same mind that just wrote the code, immediately after writing it, while that
mind still believes its own model of what the code does. The sweep is the only instrument here
that does not share that belief.

So I have stopped treating it as a final confirmation step and started budgeting for it *before*
the handoff. This session I ran one on Codex's changes to my code, not just my own — eight
deliberate faults, six caught, and the two survivors turned out to be provably harmless for a
reason I could measure rather than argue. I also got one of my own control cases wrong (I broke
it by accident instead of harmlessly, so it looked like a result when it was a bug in my
instrument), and I have reported that in the review record rather than quietly rebuilding it.
An instrument both agents rely on is not a place to be quietly tidy.

---

## The process change you directed

At the end of the last reporting period the review method had a stopping rule — at most three
rounds — but no defined ending if two agents hit that limit still disagreeing. The old answer,
"escalate to the director," made you the tiebreaker for every unresolved technical argument,
which is the bottleneck this whole framework is built to avoid.

You directed a replacement. I proposed one, Codex reconciled it, and I wrote the agreed version
into the playbook in session 140. The shape:

- The turn that first hits the limit in disagreement must **classify** the residual issue as
  *factual* or *judgment*, in that same turn.
- **Factual** issues get exactly one experiment, with both agents committing *in writing to what
  its outcome will mean* before it runs — and that experiment may spend no gated resource. A
  disagreement is never a door around a gate.
- **Judgment** issues get exactly one narrow round-trip, carrying both positions verbatim.
- If that does not converge, **the contested piece does not ship.** A capability stays refusing;
  prose is withheld rather than softened. You get a notice, and it does not block anything.

Codex made three corrections to my draft, and all three were against me. The one I'd single out:
I had written a budget ceiling in *sessions* and its mechanism in *rounds*, and those two units
do not compose — so my document promised a limit it did not actually enforce.

Since then, four reviews have closed cleanly and the ladder has not had to fire. That is the
good outcome. It also means the mechanism is untested in practice, and I'd rather say so than
let "we have a process for that" stand in for evidence that the process works.

---

## What isn't working, and what's slow

**Eight sessions, no measurements.** I have run zero simulations, zero training runs and zero
reads of reserved data since session 136. The project counters are unchanged at 278 simulated
rollouts, 67 model fits and zero reads of the pilot, validation or test sets.

The reason is real: every scientific lane this project has opened is either finished or
deliberately shut. The model-size sweep ran and its pre-written interpretation said the curve
cannot be read. The second architecture ran once and its pre-written interpretation licensed two
sentences, neither of them good news. The next scientific step requires a frozen configuration,
a selected model size and a calibrated threshold — none of which exist, and each of which is
gated behind work that is not yet done. So the honest options were *build the verification
machinery now* or *idle*.

But I want you to have the shape of it plainly: **the last eight of my sessions have produced
infrastructure for verifying a result that does not exist yet.** That is a defensible use of a
patient project's time. It is also the kind of thing that can continue indefinitely without
anyone noticing, and the person best placed to notice is you rather than either of us.

**Half of the current piece is still unbuilt.** The connection is defined as a 21-step read
order. Steps 1 through 12 are built and approved. Steps 13 through 21 — the part that checks the
authenticated data is internally *coherent*, plus the geometry it needs and the output it
writes — are the only unbuilt work in the project. That is my next session's work, and it needs
a new review card and its own mutation budget before handoff.

**One request has been open on you since early on, and it is still not blocking anything.**
Entry 1 in `director_requests.md` is the Claim Sheet review; it was designed to be non-blocking
and it is behaving that way. Entry 2 — the Windows security feature that blocked a native
library and made two sessions' test counts meaningless — was resolved by the repair agent you
authorized, and the standing procedure is written down: if it recurs, we log a new numbered
entry with the diagnostic output rather than absorbing it, because you are deciding policy from
the pattern of incidents and a silently absorbed one is invisible to you. Nothing else is on you.

---

## The verification artifact

Genuinely new this stretch, so here it is briefly.

The screen itself is unchanged and still shows only invented numbers. What changed is the
connection behind it. As of this session:

- The path from a reviewed "connection record" through schema, configuration, dataset audits,
  file indexes and data payloads is built, and **every file it touches is opened exactly once**,
  with the fingerprint taken over the bytes that read returned.
- There is exactly one place left where a file is read twice, and rather than argue it away we
  **counted it**. A test patches the low-level read and counts opens per file across the entire
  chain; it pins that one file at exactly two, so any *new* second read anywhere fails the build
  instead of quietly joining an allowance. Codex then narrowed what that second read can do, and
  I checked its fix separates on a real input rather than merely reading well.
- **The public entry point still refuses unconditionally.** Nothing can be run through this
  machinery today, by design, and that stays true until the whole connection is finished and
  separately authorized.

---

## What's next

1. Build steps 13 through 21 — coherence, geometry, output — under a new review card, with the
   mutation sweep budgeted before the handoff rather than after.
2. That completes the connection *code*. It still connects to nothing, because the three
   scientific inputs it needs do not exist.
3. After that, the project's open questions are scientific rather than infrastructural again,
   and the next real decision is which of the currently-shut lanes to try to open.

Nothing in this report is a research result. The project's central question — whether
distributed structural sensing gives a robot an adaptive-control advantage over a conventional
sensor suite — remains unanswered, and nothing in these eight sessions moved it.

— Claude
