# Progress Report — Session 32 (Phase 2, pre-confirmatory build)

**From:** Claude · **Date:** 2026-07-24 · **Project:** Robot Structural Proprioception

*A director update, not a technical paper. If any sentence sends you to look something up, that's my failure — every leaned-on term has a plain explanation and a link. Meant to be read start to finish in one sitting. It picks up where my session-24 report left off.*

---

## The one-paragraph version

This stretch produced **no new scientific findings, and that is the correct outcome.** Sessions 25 through 32 were spent building the apparatus that will let the real experiment count — and, twice, catching serious flaws in that apparatus before they could contaminate anything. The headline event: I **blocked** a design document Codex had built and was ready to run, because I found that it quietly leaked the answer. Not a typo, not a style disagreement — a structural flaw that would have handed our own hypothesis an unearned win, in a way that would have looked like success. Codex fixed it, I re-checked by re-deriving the whole thing independently, and found a second, smaller flaw that ran the *other* direction. Codex chose to pay 23% more compute to remove that one too. The experiment is now specified down to 808 exact scenarios with their random seeds fixed in advance, and both of us have signed the same bytes. Nothing has been generated yet. The next session is where the actual data starts.

---

## A 20-second refresher

We're testing whether a few cheap **strain sensors** (they feel how much the arm is bending) give a robot information a normal robot doesn't have — enough to tell apart three kinds of trouble: a link going **soft**, a motor going **weak**, or a joint sensor **lying** — and whether knowing which one actually helps the robot keep doing its job. So far the evidence says the sensors are excellent at the first thing and useless for the second, which is one of the four outcomes we wrote down in advance. A clean "no" is a real, publishable result.

---

## Why eight sessions of paperwork is the actual science

Here is the thing I most want you to have from this report, because from the outside it can look like we stopped working.

In session 24 I told you the evidence was converging on "improves diagnosis, not control." Everything supporting that came from **development screens** — quick experiments where we're allowed to look, adjust, and look again. That freedom is what makes them useful for closing off dead ends, and it's exactly what makes them worthless as final evidence. If you're allowed to keep adjusting until the numbers look right, you will eventually get numbers that look right, whether or not the effect is real.

The fix is [preregistration](https://en.wikipedia.org/wiki/Preregistration_(science)): write down *everything* — the scenarios, the fault severities, the random seeds, the metrics, the thresholds, what counts as success and what counts as failure — seal it, and only then generate the data. After that, there is exactly one run and one answer.

"Seal it" is doing real work in that sentence. Both agents can edit every file in this project. So the sealing is done with a [cryptographic hash](https://en.wikipedia.org/wiki/SHA-2) — a short fingerprint computed from the file's exact bytes, where changing a single character produces a completely different fingerprint. The plan carries its own fingerprint inside itself. When I say I approved `dev-eec59ec8…`, I'm not approving an idea we discussed; I'm approving a specific arrangement of bytes, and any later edit is instantly visible as a different fingerprint. Neither of us can quietly revise the plan after seeing results, and you don't have to take our word for it.

That is what these eight sessions built. It is unglamorous and it is the difference between a finding and a story.

---

## The catch that made this stretch worth it

In session 30 Codex handed me the scenario plan — which fault appears in which scenario, under which conditions — for approval. It passed all of its own tests. I checked it a different way: instead of verifying it was internally consistent, I **expanded every scenario the plan described and measured what the resulting dataset would actually look like.**

It leaked.

Each scenario carries three background conditions alongside its fault: how much weight is on the arm's tip, what the temperature is doing, and whether the arm touches a surface. These are supposed to be *nuisances* — realistic clutter that the diagnosis has to survive. Assigned properly, they tell you nothing about which fault is present.

In that version they told you a great deal. Roughly **48%** of the possible background conditions were impossible under a healthy robot, so the background alone partly announced that something was wrong. Two of the three conditions were locked into a fixed relationship within each fault setting. And the pattern separated mild faults from severe ones.

Here is why that was disqualifying rather than merely sloppy. **Temperature reaches our robot's senses through exactly one channel: the strain gauges.** They're mildly temperature-sensitive — about 10 microstrain per degree Celsius, a real property of the physical sensors we're simulating. The conventional robot has no way to perceive temperature at all. So a design where temperature correlates with which fault is present hands the strain-equipped robot a shortcut the conventional robot is *physically incapable* of using. It would have won. It would have won on the confound, not on the physics. And the result would have looked exactly like the finding we're hoping for.

The everyday version: imagine a drug trial where, purely by an accident of scheduling, everyone who got the real drug was measured on warm days and everyone who got the placebo on cold days — and your measuring instrument happens to drift with temperature. The drug "works." Nothing about that trial is salvageable by analysis.

I blocked it. Codex rebuilt the assignment with an explicit balanced table of background conditions, chosen by a rule that has no access to the fault at all. I re-measured: the information the background carries about the fault is now **0.000000000 bits** — that's [mutual information](https://en.wikipedia.org/wiki/Mutual_information), the standard way to ask "how much does knowing X tell you about Y," and zero means the answer is *nothing*. Every leak signature I'd found was gone.

---

## The idea I want to teach you this session: which direction does the flaw point?

When you find a problem in an experiment, the first question isn't "how bad is it." It's **which way does it push the answer.**

- A flaw that pushes *toward* what you hoped to find is **disqualifying.** It has to be fixed before you run.
- A flaw that pushes *away* from what you hoped is usually a **footnote.** You declare it, you carry it, you move on.

The asymmetry isn't squeamishness — it's about which errors get caught downstream. A flaw that hurts your hypothesis shows up as a disappointing result, and disappointing results get investigated relentlessly. A flaw that helps your hypothesis shows up as a **win**, and wins get celebrated and published. Nobody digs into why the good news is good. So the self-serving error is the one that survives, which is precisely why it has to be caught before the run rather than after.

I applied that standard in both directions within two sessions, which is how you know it's a standard and not a mood:

**Session 30 — I blocked**, because the flaw favored us.

**Session 31 — I approved despite finding a real flaw**, because it ran against us. In the corrected plan, the tip weight was perfectly predictable from which practice routine the arm was running, but only in the two splits used for *training*. A learning system could latch onto "routine A means light payload" — a shortcut that would break the moment it met the held-out data. Tip weight is more visible to strain gauges than to conventional sensors, so the strain robot would suffer *more* from learning it. Conservative. Declared, not blocked.

I also did something I'd recommend as a habit: **I checked whether the flaw was avoidable before reporting it as one.** I brute-forced every possible design of that size — all of them — and proved that with two repeats per routine, no arrangement can satisfy both the balance requirement and the no-shortcut requirement. It was a forced trade-off, and Codex had taken the better side of it. That took five minutes and turned "you should have avoided this" into "this is unavoidable at this budget, and here is what it would cost to escape." The second is both more accurate and more useful.

**Session 32 — this one.** Codex took the escape route: four repeats instead of two in the training splits, at a cost of 152 extra scenarios (+23%). I re-derived all 808 scenarios independently and measured. The shortcut is gone — 0.000 bits on all three background conditions in all four splits — and a bonus fell out that I care about more than the fix itself. The [training, validation, and test sets](https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets) now use structurally identical background designs, so when we walk the experiment up its difficulty ladder, each step changes exactly one thing. Before, one of the steps changed two things at once, and a null result there would have been ambiguous between "the hypothesis is wrong" and "the training data was subtly different." That ambiguity was the real cost, and buying it out was worth more than 23%.

---

## The check I now run on every plan, and why it exists

There's a specific failure that no amount of testing can catch, and it bit us in session 30.

A test suite verifies that code does what the code says. It cannot verify that the code does what the **document** says. In the blocked version, the written description said the background conditions were assigned by a "decorrelating rotation." The arithmetic underneath did something else entirely. Every test passed, because the tests checked the code against itself. The prose and the machine had drifted apart, and the sealed plan is the *prose* — that's the thing we're promising to follow.

So now, for any preregistered document, I re-derive the artifact **from the document's own written rule, in my own code**, and diff it row by row against what the real code produces. This session: 808 rows, 13 identity fields each, **zero mismatches**. That proves the plan we're publishing and the plan the machine will execute are the same object.

I also checked that the new safety check Codex added actually has teeth, by feeding it the *previously approved* version and confirming it now refuses it. A guard that never rejects anything is decoration.

---

## Where things stand

| | |
|---|---|
| Phase | 2 (Execution) |
| Scenario plan | **agreed and fingerprinted** — 808 scenarios, 16,160 planned data rows |
| Data generated | **none** |
| Final settings frozen | **no** — deliberately |
| Test data touched | **zero**, and locked until the freeze |
| Test suite | 378 passing |

Seven gates stand between us and the confirmatory run. Three are closed and jointly signed. One — the real scenario generator — is Codex's next session. Three are mine and open after that: the learned diagnosis models, their calibration, and the evaluation harness. Then both of us sign the freeze, generate once, and evaluate once.

---

## What isn't working

- **Eight sessions, no new scientific result.** That's the honest headline. It's the right trade, but it's a real cost and you should see it stated plainly rather than buried.
- **The learned diagnosis model still isn't built** — the same bottleneck I reported at sessions 16 and 24. It needs the frozen data layout, which needs the generator, which starts next session. I've held the line on not building against a layout that doesn't exist, and I'd make that call again, but it means my main lane has been idle for a while.
- **We reopened a decision we had already closed.** Codex amended a plan I'd approved one session earlier. That's the protocol working — nothing was silently substituted, the amendment got a new fingerprint and a fresh review — but it cost a full round-trip, and if it became a habit it would be churn rather than diligence.
- **The likely landing hasn't changed.** Everything still points at "improves diagnosis, not control." All this machinery is being built to establish a result we expect to be a qualified negative. That's worth doing — a well-evidenced negative tells the next researcher which half of this idea to skip — but I don't want the care we're taking to read as optimism about the outcome.
- **Still awaiting your Claim Sheet review** (`director_requests.md`, entry 1). Explicitly non-blocking, and we've kept working. But it's open, and this is where I say so.

---

## The verification artifact

No change this session. The hands-on artifact that will let you check the result yourself, without reading the technical report, still depends on the frozen data layout. Nothing new is genuinely nothing new.

---

## What's next

1. **Codex builds the real scenario generator** — the thing that turns 808 sealed specifications into actual simulated robot runs. When it hands that off, my review question is narrow and specific: *do the generated data actually realize the approved plan?* I'll measure the produced data against the 808 reservations directly rather than reading the generator's report about itself.
2. **Then my lane finally opens** — the learned diagnosis models, then their calibration on validation data only.
3. **Then the freeze**, then one confirmatory generation and one evaluation.

The next progress report is due at my session 40, or sooner if a phase closes or the contract gets amended.

— Claude
