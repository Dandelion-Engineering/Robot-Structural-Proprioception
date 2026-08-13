# Progress Report — Claude, Session 128

**Written:** 2026-08-13 14:44 PDT
**Covers:** my Sessions 121 through 128
**Previous report:** `Progress Report Session 120.md` (covering Sessions 113–120)

---

## The short version

Eight sessions ago I finished the last piece of science this project had authority to do. Since
then I have built exactly one thing, and for six of those eight sessions it was **a document with
no code underneath it** — a specification for the demo you will eventually use to check this
project's result with your own eyes, argued over line by line with Codex until neither of us could
find another hole in it.

This session the code finally exists. You can now run one command and get a working, animated,
side-by-side comparison of two robots — except that every number in it is fabricated on purpose,
and the screen says so in large red letters.

That sounds like a strange thing to celebrate. This report is mostly about why it isn't.

---

## Where the project stands

Phase 2 (Execution) is still open. Nothing scientific has moved since Session 120, and that is by
design rather than by drift: every remaining scientific lane in this project is either **finished**
or **deliberately shut**.

- The **rung-2 capacity experiment** ran, was read, was interpreted under the exact two sentences
  we pre-registered before running it, and is spent. There is no retry authority and none is
  being sought.
- **Choosing a model size, a confidence threshold, or an abstention threshold** all live behind
  Gate 5, which requires touching the validation data — and validation stays untouched until
  Gate 4 closes.
- The **final configuration file** that would name a real run is deliberately not frozen yet.
- The **held-out test data remains completely untouched**: zero files read, zero rows opened.

So the honest description of the last eight sessions is: the science is parked exactly where the
plan says it should be parked, and I have been building the thing that has to exist before any of
it can be shown to anyone.

---

## What Slot 8 is, and why it needed six sessions of argument

Every Dandelion project promises you a **verification path** — a hands-on artifact that lets you
check the result yourself without reading the technical report end to end. In this project's
contract that promise is "Slot 8", and what it commits us to is specific: a small interactive demo
where you pick a body change from a short menu ("soften link 2 by 30%", "weaken actuator 1", "bias
encoder 1") and watch two copies of the robot run the same task at once — one using the
conventional sensor suite, one using the structural sensor suite. A live panel shows each copy's
diagnosis and confidence and its tracking error. You see directly whether the structural robot
names the right cause sooner and tracks better — **or whether the two are indistinguishable, which
is the honest negative shown as a result.**

Here is the problem I ran into in Session 123. That demo needs four things. Three of them do not
exist yet:

| what the demo needs | where it is |
|---|---|
| a frozen configuration naming the run being shown | deliberately absent — a gate we chose to keep shut |
| a chosen model size and its trained weights | undecided; nothing has been selected |
| calibrated confidence and abstention thresholds | undecided, and they live behind the validation gate |
| something that draws the picture | does not exist |

Only the fourth is available today. And a demo built now would have to either invent the first
three or **silently adopt whatever our development records happen to contain**.

The second of those is the dangerous one, and it is worth being blunt about why. Our development
record contains a result where **all ten trained models scored exactly zero on two of the four
fault categories** — they never once correctly identified a "healthy" case or a "structure" case.
That is a real and honestly recorded development finding, not a scandal; it is in the packet, and
it is public in the project's running log. But a development record wrapped in a finished-looking
demo reads to a non-specialist as *the project's result*. If someone opened a polished animated
comparison and saw those numbers presented as an outcome, they would be misled, and it would be
our fault.

**So the design's entire purpose is to make that misrepresentation structurally impossible rather
than merely discouraged.** Not "we'll remember not to do that" — impossible, in the sense that the
code refuses.

---

## What was actually built this session

Two program files and two test files, about 4,200 lines together.

- **The scene contract.** One data structure that describes exactly one side-by-side comparison:
  the two robot bodies over time, each one's diagnosis history, each one's tracking error against
  the same reference, and a provenance block saying where every number came from.
- **The synthetic fixture.** A generator that fabricates four complete cases from a seed, entirely
  analytically. Its tracking traces are smooth mathematical curves, its probabilities are round
  numbers, its onset is at a round time. It is not trying to look real, and a fixture that looked
  real would be a defect.
- **The two surfaces.** An interactive window with a radio-button menu, a timeline slider and a
  play/pause button; and a scripted path that writes 300-DPI figures for the eventual reports.
  Both call **the same painting function** — which matters more than it sounds, and I come back to
  it below.
- **144 tests**, one named for each of the nineteen invariants the design commits to, plus the
  refusal cases.

Every scene the code can currently produce carries a red banner reading **SYNTHETIC — NOT A
RESULT**, a line reading *"A synthetic fixture is not evidence: every number on this screen was
fabricated by the packet"*, and the sentence *"This demo does not answer the project's research
question."* The banner is drawn **into the image**, not into a caption — because a caption is
separable from the picture the moment someone copies it into a slide.

The path that would read real data exists in the code and **refuses before it opens a single
file**, because the authorization that would make it work does not exist. A test asserts that no
input currently in this packet can produce a "development" or "final" label. The day either
becomes possible, that test goes red — which is the point. It forces a deliberate decision instead
of a quiet one.

---

## What was unexpected

**Three of the four cases I'd have written naively were wrong, and testing found them.**

The one I want to tell you about is from Session 125, because it is the cleanest example of why
this project reviews things the way it does.

The demo shows a tracking-error graph with a shaded band over the five seconds after the fault —
the window our headline metric integrates over. I specified that the demo's shaded band and the
report's published number must be *the same quantity*, because if they drift apart, the picture
and the number disagree and nobody notices.

Then I actually ran our metric function on a perfectly ordinary fabricated trace: a thousand
samples at 100 Hz starting at zero, with a deliberately round fault onset at 5.0 seconds. **It was
refused.** That grid ends at 9.99 seconds, and a 5-second window starting at 5.0 needs a sample at
10.0. Off by one sample.

The consequence, had nobody checked: the demo's shaded band would have extended past the end of
the data it was drawn over, and the metric would never have been called in the only round that can
call it — the picture and the number disagreeing in exactly the way the rule existed to prevent.

Codex found the mirror-image mistake in Session 126, and I found its twin in Session 127: I had
written down *four* of that function's preconditions and pointed the implementation at my list. Two
more existed that my list missed. **Copying a fact that another piece of code already owns creates
a second definition that nothing keeps in sync.** The fix was to stop copying: the code now simply
*calls* the metric function and refuses on whatever it refuses on. A test monkey-patches that
function to raise an error no design document has ever mentioned, and requires the refusal to come
through carrying that exact error — so if a future session replaces the call with a checklist
again, the test fails and says why.

**The second unexpected thing is smaller but I liked it.** The design requires the interactive view
and the published still to be "the same comparison". The obvious way to build that is two code
paths that both draw the same thing — and the first time they diverge, the divergence is silent and
lands in a published figure. So the interactive window doesn't draw anything itself: it calls the
same painting function the figure script calls, and displays the result. Sameness is a single
source rather than a promise maintained by hand.

---

## What isn't working

**MuJoCo is broken on the agents' desktop, and it isn't our doing.**

[MuJoCo](https://mujoco.org/) is the physics engine this whole project's simulated robot runs on.
As of this session, Python on that machine cannot load it at all:

> `ImportError: DLL load failed while importing _functions: An Application Control policy has
> blocked this file.`

That is a Windows security policy — [Smart App Control / WDAC](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/appcontrol)
— deciding that one of MuJoCo's binary files is not allowed to run. Nothing in the project changed;
the interpreter simply cannot open the file any more.

The practical effect: 28 of the packet's test files can't even load, and a 29th fails inside the
same import. **That means the packet's usual full-test-suite count cannot be measured while this
holds**, and I am not going to quote a smaller number as though it were the whole suite. What I can
honestly report is 1,328 tests passing, 1 failing and 28 files failing to load, with every one of
those 29 failures traced to that single blocked file.

This is logged as entry 2 in `director_requests.md`, because only you can change a machine security
policy. **It is not blocking the current work** — the Slot 8 code deliberately imports neither
MuJoCo nor PyTorch, so that it will open on an ordinary laptop for anyone who downloads the packet
— and its own 144 tests run green. But it will block the next time anything needs to simulate the
robot.

**The other thing that isn't finished:** the code I built this session is under review by Codex
right now. Until that closes, no figures get written into the packet and no runbook step gets
added. That's the sequencing the design set for itself, and it has already earned its keep.

---

## The verification artifact — where it actually is

There is genuinely something new to report this time, which there hasn't been since this lane
opened.

| step | state |
|---|---|
| 1. design reviewed and frozen | **closed, both agents approved the same bytes** (Session 127) |
| 2. code, fixture, both surfaces, 19 invariants tested | **built this session, under review by Codex** |
| 3. generate the figure set, add the runbook step | not started; blocked until step 2 closes |
| 4. connect a real result | a separate design, review and joint authorization; not granted by any of the above |

One measured detail worth having: the whole four-case figure set renders in **1.7 seconds**, and it
is byte-for-byte identical when rendered twice. That determinism is what lets a figure in a report
be traced back to the exact scene that produced it.

---

## What the next stretch looks like

1. Codex reviews the code and tests against the frozen design. If it edits or blocks, the re-review
   is mine and comes first — that is how every loop in this project closes.
2. Once it closes: generate the fixture figure set into the packet, and add the runbook step so a
   stranger who downloads the packet can reproduce it with one command.
3. Then — and only then — the question of connecting a **real** result becomes live, and it needs
   its own design, its own review and its own authorization. It also needs the three inputs that
   don't exist yet, which puts it downstream of the capacity and threshold decisions.

I want to be straight about the shape of the last eight sessions: **they produced no science.** They
produced the thing that determines whether the science, when it exists, can be shown to you
honestly. Six review rounds ran on a document with no code against it, and every round found
something real — a demo that could not have been written to disk, a resolution check that would
have gone red on a correct figure, a clock rule that would have rejected every real recording the
day we connected one. Those are all defects that would otherwise have been found by a future
session with a deadline, or not at all.

That was the trade. I think it was the right one, and this is the report where you get to disagree
with me about it.
