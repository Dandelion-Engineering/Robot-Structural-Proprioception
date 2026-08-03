# Progress Report — Codex, Session 64

**Date:** 2026-08-03
**Covers:** my Sessions 57–64 (previous report: Session 56)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The measuring program described in my last report has now run. In Session 57 I
executed its approved 135-simulation plan once. It took 4,432 seconds inside the
executor — about 74 minutes — and returned the pre-registered middle case: some
structural-damage levels were detectable, and some were not.

That result was real, but it was not yet portable across the project.

The four contexts in the screen quietly contained two different payload weights:
an unloaded arm and an arm carrying 50 grams at its tip. The strain-based damage
signal at 50 grams was roughly half the unloaded signal, while the noise floor it
had to beat barely moved. The project reserves six other payload weights that the
screen never measured. So the honest boundary is not “the method detects this much
damage.” It is “the method detects this much damage at the two lightest payloads we
tested.”

The last several sessions built the follow-up needed to measure that dependency.
Both agents have approved the exact measurement design and the two code seams that
let payload mass reach the simulator and the results key. This session I built and
verified the executable itself. Claude has not reviewed that executable yet, so it
is not approved and nothing has run. The official zero-rollout plan has not even
been produced.

That distinction is the present state: **the earlier screen is executed evidence;
the payload extension is an approved design plus a reviewer-pending build.**

---

## The idea behind the follow-up

If we ran each payload with unrelated sensor noise, a difference between two
weights could be caused by the body, the noise draw, or both. The extension instead
uses **common random numbers**: the same eight sensor identities are reused at every
mass, so the random part is held fixed and the physical body is the thing that
changes. This is a standard variance-reduction idea — compare two systems under the
same random draws so their difference is easier to interpret. ([Variance reduction,
including common random numbers](https://en.wikipedia.org/wiki/Variance_reduction).)

That choice also turns a software check into a real one. After all seven healthy
payload blocks run, the executable compares the healthy coefficient vectors within
each shared identity. If payload mass never reached the simulator, the common-noise
design would produce identical vectors. The executable requires all 168 cross-mass
comparisons to be distinct before it is allowed to run a single non-anchor damage
ladder.

The cost of this clarity is that identity can no longer distinguish physical
bodies. A 25-gram run and a 200-gram run deliberately share the same sensor identity.
Payload mass therefore has to be part of the results key itself. That sounds small,
but it is the difference between 126 physical bodies and 18 collapsed key slots.
The current ledger would refuse the collision loudly rather than silently accept a
wrong measurement, but the experiment still could not complete without the fix.

---

## What happened across these eight sessions

### Sessions 57–58: run once, then reproduce before interpreting

Session 57 executed the approved screen exactly once: 135 physical simulations,
147 logical result rows after the intended reuses, and no confirmatory data. I
reviewed the persisted result immediately and approved its exact bytes. Claude then
re-derived the result independently instead of trusting the producing program.

The outcome was `CASE_B`: a middle boundary rather than “everything works” or
“nothing works.” The selected probe was 0.10 newtons with a 0.25 ramp fraction.
The result remains development-only. It did not freeze `config.json`, create
confirmatory identities, or authorize dataset regeneration.

### Sessions 58–61: the result had two missing readings

The first missing reading was **role coverage**. The protocol required a count of
how many structural severities reserved for development, pilot, validation, and
test were actually detectable, but the executed driver did not compute it. The
zero-rollout analyzer we reviewed afterward gave counts of **0 / 0 / 1 / 1**.
Development — the split from which a model would learn — retains no detectable
structural severity at this probe. That is a genuine non-transfer result, not a
test failure and not permission to invent a new training claim.

The second missing reading was payload conditioning. The screen already contained
the balanced unloaded-versus-50-gram comparison; nobody had asked it the question.
Reading that contrast cost no new simulation and showed the roughly twofold signal
attenuation. We built and cross-reviewed an analyzer so the finding was reproduced
from the persisted screen rather than carried as an impression.

### Sessions 60–61: our mutation-testing ritual needed repair

Mutation testing deliberately breaks a guard and asks whether the tests notice.
([Mutation testing](https://en.wikipedia.org/wiki/Mutation_testing).) We found that
Python bytecode caching could make a fast sweep execute the previous mutation while
reporting the verdict under the current one. The dangerous failure was a false
all-clear: calling a guard tested when the test had never exercised it.

The corrected ritual now uses a fresh isolated packet copy for every mutation,
disables bytecode writes, clears every `__pycache__`, runs the whole focused suite
without `-x`, and repeats the complete sweep twice. The final executable state in
this session caught all 17 selected decision-bearing mutations in both passes, with
identical verdicts.

### Sessions 62–63: make the expensive follow-up prospective

Claude drafted the payload-boundary extension; I reviewed it against the existing
plant, result key, stage order, and decision authority. The review changed several
load-bearing parts before any extension measurement existed:

- the design now holds random identity fixed across masses rather than moving it;
- plan mode costs zero rollouts and is separated from execute mode;
- a dead payload override is caught before any non-anchor damage ladder;
- every result row carries both physical keys used by its difference;
- reduced mass coverage preserves diagnostics but licenses no Claim Sheet option;
- the outcome classifier is ordered, exhaustive, and uses one rule for the
  payload-capped option in both relevant branches.

Claude and I approved the same frozen document at the end of Session 63. That
approval authorized construction only — not plan mode and not execution.

### Sessions 63–64: build the three prerequisites

I added payload mass to the generator override and to the physical result key.
Claude’s review found the adjacent producer gap: the key could hold a mass, but the
only row-to-key path did not pass it. Claude fixed that additively; I re-reviewed and
approved the exact state this session. The generator and results seams are now
jointly approved.

I then built the third prerequisite, the extension executable. It has its own
X-stage ledger and its own 126-physical / 532-logical census rather than forcing
those objects through Protocol P’s A/B/C vocabulary. Its default is zero-rollout
plan mode. Execute mode requires a separately authorized plan digest, recomputes
the whole plan before the replay can run, performs the anchor first, runs all
non-anchor healthy blocks next, checks payload liveness, and only then opens the
remaining ladders.

The current executable and test blobs are owner-approved by me and are now with
Claude for first review. They are not a jointly approved prerequisite yet.

---

## Where things actually stand

**Working and closed:**

- The 135-rollout Protocol-P screen ran once and its exact result is approved by
  both agents.
- The role-coverage and payload-conditioning reads are approved zero-rollout
  analyses of that persisted result.
- The payload-boundary extension document is approved and frozen.
- The generator and physical-key seams are jointly approved.
- The full packet suite passes **1,172 tests**; the new focused suite passes 36
  tests normally and under optimized Python, where decision-bearing `assert`
  statements would disappear.
- Lifetime Protocol-P-related physical execution remains **151 rollouts**. This
  eight-session stretch added no physical execution after Session 57.

**Still open or unresolved:**

- Six payload masses remain unmeasured.
- The physical mechanism behind the attenuation remains unidentified. The model
  has no gravity, and the 0.8-Hz probe is far below the lowest measured structural
  mode, so sag and resonance are not explanations.
- Development retains no detectable structural severity at the selected probe.
- Claude’s exact-state review of the new executable and tests is open.
- The official plan artifact does not exist. The replay gate and extension have
  not run. `config/config.json` remains absent.
- Claude’s Session-64 progress report has two narrow reviewer edits awaiting
  Claude’s same-state approval; those edits change no scientific state.
- The Claim Sheet review in `director_requests.md` remains open and non-blocking.
  Nothing in this stretch requires a new action from you.

**Verification artifact:** no change. The director-facing hands-on artifact still
belongs with the later confirmatory result; producing a development-screen demo now
would risk making an unfrozen boundary look final.

---

## What happens next

1. Claude reviews the executable and tests against the frozen extension, not only
   against their passing suite. Any edit returns to me for genuine re-review.
2. Only after both agents approve the same executable bytes does Step 2 close.
3. Plan mode may then run once at zero rollout cost. Both agents read that exact
   plan artifact.
4. A separate joint authorization must name the plan’s canonical digest before
   the ordinary-path replay or payload extension may spend a rollout.
5. The extension then runs once in its pre-registered order. Its result informs —
   but does not itself make — the later Claim Sheet amendment decision.

The important posture is unchanged: the project found that a real result depended
on a variable the first design did not settle. We preserved the result at its true
scope, stopped before building conclusions on top of it, and made the follow-up
harder to fool before paying for it.

— Codex
