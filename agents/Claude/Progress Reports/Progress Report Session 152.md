# Progress Report — Claude, Session 152

**Written:** 2026-08-17 18:35 PDT
**Covers:** my Sessions 145 through 152
**Previous report:** `Progress Report Session 144.md` (covered S137–S144)

---

## The short version

Eight sessions ago the program that will connect this project's demonstration screen to a
real scientific result was about half written. It is now most of the way through — twenty of
its twenty-one steps exist — and this session it did something it had never been able to do
before: **it assembled a complete menu and showed three different kinds of body change side
by side.** Until today the demo could only ever have shown one panel, because the fixture
data we are allowed to build did not contain enough kinds of change to fill a menu.

That is the visible progress. Three other things in this stretch matter more.

**One: Codex has now found something real in four consecutive reviews of my work, and the
last three were not about my code being wrong.** They were about my *evidence* being wrong —
tests that passed for a reason that had nothing to do with what they claimed to prove. I
think this is the single most interesting pattern of the stretch and most of this report is
about it.

**Two: the same defect turned up twice in one review, in two completely different places, and
neither Codex nor I noticed they were the same defect until I sat down to repair them.** I
have written down the general form so that next time we can go looking for the family instead
of the instance.

**Three: none of these eight sessions produced any new science, and I want to say that
plainly.** No simulation was run, no model was trained, no measurement was taken. Every one
of them was infrastructure — the machinery that will let you check the result yourself. The
counters that track our scientific spending have not moved since Session 117.

---

## Where the project stands

The project is still in Phase 2, execution. The scientific question — whether a robot can use
distributed measurements of its own structure to notice and adapt to changes in its own body
— is not being answered right now, and has not been since Session 117, because every path to
answering it is deliberately closed behind a gate that has not been opened.

What is being built instead is **Slot 8**: your verification path. The Claim Sheet committed
us, before any of the work began, to building a specific thing whose only job is to let you
check the result without reading the technical report. In this project that thing is an
interactive screen: a menu of body changes, and for each one, a side-by-side comparison of
what the two competing approaches concluded.

The screen itself has existed since Session 130 and is connected to nothing — every number
on it is openly fabricated fixture data, and it says so. What I have been building for the
last dozen sessions is the piece that will one day connect it to real results: an "adapter"
that reads a reviewed document naming every scientific file the screen is allowed to open,
checks that every one of those files is exactly the file the document names, and only then
builds the picture.

That adapter's specification is a fixed list of **twenty-one steps in a fixed order**. Steps
one through twelve were finished and approved earlier. This stretch built steps thirteen
through twenty. One step remains.

### Why the order is fixed, and why that turns out to matter

Every step in the list either establishes a fact or checks a relationship between facts
earlier steps established. Because the order is fixed, a step written later is allowed to
*assume* everything the earlier steps proved.

That is the whole design, and it is also where three of the four review findings in this
stretch came from. When I test one step in isolation, I have to hand it a starting state —
and that state must be one the earlier steps could actually have produced. If it is not, then
the test proves something about a situation the program can never be in.

That sounds abstract, so here is what it actually looked like.

---

## What was found that I did not expect

### The evidence was wrong three times running, and the code was right all three times

In Session 150, Codex reviewed step 19 and reported that my tests handed it a starting state
the program refuses five steps earlier. My verdicts were right; my *reasons* were worthless.
In Session 151 I repaired that — and Codex reviewed the repair and found it still incomplete.
In this session I repaired it again, and I expect the honest thing to say is that I do not
know for certain that this one is complete either.

Here is the concrete shape. The adapter checks that a data set's records all agree about
which configuration produced them. To test one late step, I need to hand it a state
describing a *different* configuration. So my test helper edits the configuration identity —
and it has to edit **every copy of it**, in every document, or it produces a state that is
internally contradictory in a way the program would have caught long before.

Session 150's helper moved four copies. Codex measured that eight relationships broke.
Session 151's helper moved eleven copies. Codex measured that seven more relationships
*still* broke — a recomputed head-count of the data set, two audit documents' copies of that
head-count, the record's own twenty-field echo of each data row, and eight index files.
Session 152's helper moves all of them, and the helper now refuses to return a state in which
any of **eighteen** stated relationships is broken.

**The thing I got wrong twice in a row is not arithmetic.** It is that I wrote a
post-condition — a rule the helper checks on its own output — and then wrote in its failure
message that it recognised *every* state the program can be in, when it only recognised the
ones I had thought of. The repair this time was to make the check say exactly what it covers
and, separately, to write down what it deliberately does **not** cover and why.

### A safety net that could only ever catch the previous accident

When I widened the check in Session 151 I also added what scientists call a
[negative control](https://en.wikipedia.org/wiki/Scientific_control): I reconstructed the
*old*, broken helper as an input and required the new check to catch it. That felt rigorous.
It was not.

The old helper's defect was already covered by the new rules — of course it was caught. What
the control could not tell me is whether the new check would catch the mistake I had just
made *this* time. And it did not, because I had not made that mistake yet when I wrote the
control.

So the rule I have written down is: **when a review widens a check, the state that was
shipped this time becomes a second control, kept forever beside the first.** Measured here:
the Session-150 version breaks 11 of the 18 relationships and the Session-151 version breaks
7 of them, and only the second is a witness for anything this session added. Both controls
now live in the test file permanently.

### Two findings that were one finding

Codex's second finding this round was in real production code, not in a test. The step that
assembles the final picture was being handed a label — "this data is development-only" versus
"this data is final" — as a separate argument, and it stamped that label onto every panel
without ever checking it against the reviewed document.

So a caller could have handed it the label "FINAL" over development data, and the resulting
screen would have carried a *final results* banner over data generated during development.
That is precisely the confusion the whole design exists to prevent.

I measured how far the forgery would have travelled before anything noticed: the scene
validator **accepted it**, and so did the version claiming to be private test-fixture data.
Nothing after the assembly step can see the disagreement, because by that point the label is
the only statement of the fact left in the object.

The repair is three lines: require the supplied label to be the reviewed document's own
authority, before a single panel is built.

**What I did not see until I was repairing both:** this is the same defect as the test-helper
one. In both cases a value arrived *beside* the thing being checked instead of being derived
*from* it. The test helper took a configuration identity as a string; it now derives that
identity from the document, and the parameter is gone. That is the stronger of the two
repairs, because deleting the seam beats guarding it.

---

## What is working

**The review discipline is doing its job, expensively and correctly.** Four consecutive
reviews, four real findings, none contested by me after I drove each one at source myself.
Twice my own measurement came out *wider* than what Codex reported — this session I found
that the broken state also violated a policy rule Codex had not enumerated. That is what the
two-agent arrangement is supposed to produce, and it is producing it.

**The demo menu now exists.** This is the first session in which the program can assemble a
complete verification bundle. The gate it had to pass requires the menu to contain at least
one structural change, one actuator change and one sensor change — because a menu that cannot
show a reader all three side by side cannot support the comparison the artifact exists to let
them make.

Session 151 measured that no menu our fixture data could build would pass that gate, and
wrote the boundary down instead of hiding it. **The repair was a fixture, never a relaxation
of the rule.** This session built three additional synthetic pairs carrying the three
required kinds of change, and the accept path — plus two identity checks that had never been
reachable — is now driven end to end.

**The step count.** Twenty of twenty-one read-order steps built. The remaining one writes the
finished bundle to disk, and it was blocked until this session for exactly the reason above:
you cannot test writing a bundle until something can build one.

---

## What is not working

**Eight sessions, no science.** Between Sessions 145 and 152 I ran no simulation, trained no
model, and took no measurement. Every counter is where it was in Session 117: 278 physical
simulation rollouts, 67 model fits, and zero reads of the pilot, validation or test data.
This is by design — those paths are gated behind decisions that have not been made — but it
is eight sessions of building the instrument rather than using it, and you should know that
is where the time went.

**I keep shipping incomplete post-conditions.** Twice in a row now, the thing Codex found was
a check of mine that claimed more than it verified. I do not think this is carelessness; I
think it is that a rule about "every relationship the earlier steps established" is a claim
about code I did not write and am not currently reading. The repair I have adopted — call the
function that *owns* the rule rather than restate it — closed part of it this session, and I
expect it to close more of it next time.

**One blocker is still yours.** `director_requests.md` entry 1, the Claim Sheet review, is
still awaiting your reply. It has been non-blocking the whole time and remains so — we have
kept working — but it is the one open item on your side. Nothing else is waiting on you.

---

## What is next

1. **Step 21** — writing the finished bundle to disk. Unblocked for the first time this
   session, because its accept path needs a bundle that passes the gate and now there is one.
2. The remaining verification work on the adapter: an observer that proves the program opens
   exactly the files it is allowed to open and no others, and the last of the acceptance
   tests.
3. Wiring the command-line entry point, which currently refuses every invocation
   unconditionally and correctly.
4. A [mutation sweep](https://en.wikipedia.org/wiki/Mutation_testing) over the finished pair
   of files — deliberately breaking the program in dozens of small ways and requiring the
   test suite to notice each one. This has changed my tests on three consecutive builds, so
   it is budgeted as real work rather than a confirmation step.
5. Only then: the review card, the review chat, and handing the whole of it to Codex.

After that, the adapter is finished as a *program*. It will still be connected to nothing,
and it will stay that way until the configuration freeze, the model-capacity choice, the
threshold calibration and the established result all exist. Those are the gates that make the
scientific answer possible, and none of them has opened yet.

---

## A note on the verification artifact

There is something genuinely new to report on it this session, which is why it appears here:
for the first time, the program can produce the complete object the screen draws. What it
produces is still entirely synthetic and openly labelled as such — three fabricated body
changes over fabricated data, assembled to prove the assembly works. No real result has been
read, and reading one requires authorizations that do not exist.

The distance from here to a screen showing you a real result is not code. It is the four
gates listed above.
