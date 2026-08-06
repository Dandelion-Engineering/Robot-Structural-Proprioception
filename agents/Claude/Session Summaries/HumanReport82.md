# Claude — Human Report, Session 82

**Date and time:** 2026-08-06 00:25 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.
**Progress-report session:** no. My next regular progress report is Session **88**.

---

## Summary

Codex reviewed the trainer I built last session, blocked it on six executable defects, and
refused to guess at one scientific decision I had left to the operator. This session I
re-opened its exact state, checked all six rather than accepting them on report, preserved
all six, found one defect inside its own repair, and supplied the missing decision.

The missing decision is the one worth explaining, because it is the only genuinely
scientific thing that happened this session.

**The problem.** The model has to be shown a slice of each run — a window — and asked what
is wrong with the robot. Which slice is not a detail. Move it earlier and the fault has not
happened yet; move it later and you may be looking at the arm returning to rest. My Session
81 trainer made the window's starting point a number the operator types at the command line,
with no default, on the reasoning that a default would decide it silently. Codex's objection
was sharper than mine: a number you type is still a number *you chose*, and the delivered
development data contains **two different kinds of run** — one with a small diagnostic
wiggle deliberately applied to the arm, and one without — so no single starting point can be
correct for both. It refused to pick one and handed the question back.

**The answer.** The starting point is now not chosen at all. It is *derived* from the
project's own approved design document, by one rule:

> The window opens a fixed interval after the fault begins, and that interval is the one the
> design document already fixed for that split's diagnostic run.

For the development data that interval is one second. Applying it gives the diagnostic run a
window running from step 1000 to step 1768 — **which is exactly the window Protocol P
already committed to, in writing, before any of this was built.** That is the whole
justification: the rule is not a new decision competing with the pre-registration, it
*reproduces* the pre-registration and then extends it to the run the pre-registration did
not cover. The probe-free run gets steps 900 to 1668 — the same one second after its own
onset — so the two runs are looked at the same distance into the fault, and the only thing
that differs between them is whether the wiggle was applied. That is the comparison this
part of the project exists to make; giving them different intervals would have muddled it.

The rule also turns out to be total: applied to all four data splits it lands inside every
run, with every split reserving exactly one diagnostic trajectory to anchor it. That matters
because the final confirmatory analysis will have to use the same rule, and it now inherits
it rather than needing a second decision later.

**The defect I found in Codex's repair.** Codex had wrapped the training step in a handler
that converts PyTorch's runtime failures — a graphics card running out of memory, say — into
a named, recorded failure rather than a crash. In Python, the class it catches is also the
parent class of the project's own two error types. So the handler was silently swallowing
both of them. Two costs, and I measured both rather than reasoning about them. First, a
violation of one of the project's *bounds* — the rule that a fit may only use five
specifically pre-named random seeds — was being recorded in the result file as "data
missing," with the wrong exit name and the wrong exit code, in the one document whose job is
to say which rule was broken. Second, and reachable on the very first real training run,
this module deliberately never writes an error message into its result file (a decision made
after five sessions of pain in Sessions 66–70), so the message printed to the screen is the
*only* place the diagnosis exists — and the handler was replacing "training loss became
non-finite for seed 3" with a generic sentence. In one case it reported that the training
runtime had failed when no training had been attempted at all. The fix is three lines.

I also fixed something of my own that neither of us had flagged: my Session-81 code recorded
a fingerprint of the design document in every checkpoint, but that fingerprint was a constant
copied into the file — nothing ever compared it against the actual document. It now hashes
the real file, requires the match, and records what it measured. Two other scripts in this
project already do exactly that, so this was a gap rather than an invention.

**Nothing was trained.** The trainer still has not been run against real data, and it may
not be until Codex approves this state. That is the fifth consecutive session in which I can
say honestly that the boundary got safer and the science did not happen. I say more about
that below, because it is the thing the director should be weighing.

## What was accomplished

### 1. Codex's six findings, checked rather than accepted

I preserved every one of them and contested none. What I actually did to each:

- **Finding H (the future-information leak) — reproduced against my own blob.** I wrote my
  Session-81 file out of Git into the package as a sibling module, imported both versions in
  one process, and put a sensor sample one second *after* the decision the model is
  simulating. Under my code it arrived in the training window with the value 12345 and a
  "this is valid" flag. Under Codex's it is absent and marked invalid. I also checked the
  thing an automatic pass/fail would have skipped: that only that one sample was removed
  (7 of 8 survive), because a masking bug that emptied the whole channel would also look
  like a fixed leak. And I read Codex's predicate line by line against the online path it
  claims to reproduce — same test, same tolerance, same handling. It is a transcription,
  not a lookalike. **My diagnosis was wrong and its was right.**
- **Finding I (the trainer described its input instead of enforcing it) — the pins
  re-derived from the delivered files, and the enforcement traced one layer below the
  claim.** All four fingerprints Codex pinned reproduce exactly when I recompute them. More
  importantly, I checked whether the loaders it switched to actually *use* them: they hash
  every individual data file against the pinned index before opening it. The chain is closed
  at every link.
- **Findings J, K, L, M** — read in the executable rather than in the report, and kept. My
  own finding lives inside L's repair.

### 2. The training-window policy, implemented

Stated once, in one function, derived from the approved assignment document. Every number it
produces is recorded in the plan file, in every checkpoint record, and in every failure
document: the fault onset, the interval, the window start and end, the run length the design
implies, whether that run carries a probe, and the fact that each run contributes exactly
one window.

Three additional things the executable now checks rather than asserts:

- **The two sensor suites must be matched.** The whole comparison rests on the claim that the
  gauge-equipped suite and the control suite see the same runs. Since the window depends only
  on which trajectory a run belongs to, the suites are matched exactly when their
  per-trajectory counts are equal — so the trainer counts them and refuses if they are not.
  Delivered development data: 76 and 76 in both suites, for both trajectories.
- **The data file must agree with the design document about its own length.** The window
  schedule comes from the design; the run length comes from the delivered file. A check whose
  two sides come from the same source is not a check.
- **One window per run, verified at run time**, not merely described.

### 3. My Finding N, and the command line closed

The three-line re-raise described above, plus the removal of the window-origin command-line
flag entirely. There is now no value an operator can supply that changes which slice the
model sees. A test pins that the flag is rejected.

## Challenges, and how they were handled

**The temptation to narrow the data.** The easy resolution to Codex's block was to fit only
the diagnostic runs, where a pre-registered window already exists, and call the ordinary runs
out of scope. That would have halved the training set, thrown away the one condition that
isolates what the gauges contribute without a deliberate probe, and forced a matching
narrowing on the final analysis. I did not take it. The harder path — finding a rule that
covers both and happens to reproduce the pre-registered window as a special case — is the one
that leaves the science intact.

**Making sure the new tests are not decorative.** Twelve of the thirty-two tests in this file
are new, and a test that passes for the wrong reason is worse than no test. I ran a mutation
sweep: fifteen deliberate breakages of the source, each run against the whole suite, twice,
with the file restored and re-fingerprinted after every case. **Fifteen breakages, fifteen
caught, no survivors, both passes identical.** Among them: replacing the derived interval with
a chosen number, dropping the onset from the window start, widening the "must land on the
control grid" check, accepting a data split with no diagnostic run, removing the availability
mask that closes Codex's leak, accepting mismatched suite counts, and letting one run
contribute two windows.

**A probe that would have lied to me, avoided.** In Session 81 I was caught by a leak detector
that reported no leak because the value it searched for had been re-rendered on the way to the
output. So this session's leak probe does not only ask "did the bad value disappear?" — it
also asks "did anything *else* disappear?", which is the question that separates a fix from a
mask that eats the channel.

## Important decisions

1. **The window interval is derived, not chosen.** The single most consequential decision of
   the session, and the reason it is defensible is that it lands on a number the project
   pre-registered months of sessions ago rather than on a number I liked.
2. **The probe-free trajectory takes its split's interval.** Holds time-since-fault fixed and
   lets excitation be the only difference.
3. **One window per run.** A sliding set of windows would have multiplied the example count
   without adding independent information, and would have been a second unregistered choice.
   152 examples per arm is a small training set and I am recording it as a limitation rather
   than describing it as anything else.
4. **The window origin is not a command-line input at all.** Stricter than requiring the
   operator to type it.
5. **Only the reachable handler was fixed.** I did not add the same guard to a second handler
   where nothing can trigger it — an unreachable guard is a branch no test can drive, and this
   project has a standing rule against them.
6. **The packet's public README was left alone.** The trainer's entry belongs there when the
   review loop closes, not while it is open.

## Reasoning paths explored

- **Anchoring the window on the fault onset alone** (start exactly at onset). Rejected: it
  puts the onset transient inside the window, and Protocol P's own pre-registered window is
  entirely post-onset. Matching the pre-registration was the stronger constraint.
- **Deriving the onset from the label file rather than the design document.** Rejected, and
  the reason is a real hazard: the fault specification's default onset value is `-1`, so a
  label-derived rule is one data regeneration away from giving healthy and faulted runs
  different windows — which would make the window origin depend on the answer the model is
  supposed to produce. I checked the delivered labels (they currently agree with the design
  document, healthy runs included) and derived from the design document anyway.
- **A single fixed interval for all splits.** Rejected: the design document already fixes a
  different probe offset per split, so a global constant would clip the probe out of the
  window in two of the four splits.

## Insights gained

**A number you type is still a number you chose.** My Session-81 defence of the
command-line window origin was that requiring it prevented a silent default. Codex's
objection is the better one: the operator making a pre-registration-adjacent scientific
choice at invocation time is the problem, and moving it from a default to a prompt does not
solve it. The resolution was to make the value underivable from the command line and
derivable only from a document both agents already approved.

**Python's exception hierarchy is a place where a repair can silently widen.** Both of this
project's error types inherit from the same standard class the repair was written to catch.
Nothing about the repair looked wrong; the defect is entirely in what the language considers
a subclass. This is the second time this family has bitten us and it is worth a standing
note: *a handler that converts one kind of failure into another must be checked against every
type it can actually catch, not against the type it was written for.*

**The strongest justification for a choice is that you did not get to make it.** The window
policy would have been much weaker if I had argued for a good interval. It is strong because
the interval was already fixed, by a document approved before the question arose, and the
rule's job was only to find it.

## Files created or updated

- `Reproducibility Packet/scripts/utils/dev_fit_trainer.py` — the derived training-window
  policy, the matched-census check, the payload/design length cross-check, the measured
  assignment digest, and the Finding-N re-raise. Blob `10054696…`.
- `Reproducibility Packet/tests/test_dev_fit_trainer.py` — 32 tests (was 20), including the
  Protocol-P reproduction test run against the real approved document with no fixture in the
  way. Blob `9e76923c…`.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — the Session-82 review turn, policy proposal and handback (append-only).
- `agents/Claude/Session Summaries/HumanReport82.md` — this report.
- `agents/Claude/README.md` — the trainer's workspace entry brought current.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

## Verification and evidence boundary

```text
two-blob probe        my S81 blob and the reviewer state in ONE process; sibling deleted
digest re-derivation  4 of 4 authorized pins reproduce from the delivered files
loader trace          per-payload hashing confirmed in the source, not accepted on report
mutation sweep        15 cases | 15 CAUGHT | 0 survivors | 0 anchor failures
                      | both passes identical | restore digest re-checked
focused suite         test_dev_fit_trainer.py  32 passed  (Codex's state: 20)
focused under -O      32 passed
FULL PACKET SUITE     1,499 passed in 119.64 s   (Codex's 1,487; +12, no regressions)
compileall            clean
git diff --check      clean
source diff vs Codex  +452 / -94    tests  +437 / -102   (git --numstat)
chat append           +243 / -0, additions only, prefix asserted byte-identical
real-data reads       manifest, approved assignment, draft config/schema, three role
                      indexes, and four development observation+label payloads
pilot / val / test    0 reads of any kind
fits / checkpoints    0 / 0        data generation 0        ROLLOUTS 0
final config.json     absent
```

**One correction I made to my own work before committing, recorded because the project's
standard is that a reported figure is a measured figure.** The first draft of my chat turn
quoted the source and test diff sizes from estimate rather than from `git`. I caught it
while checking what I was about to commit, measured them, and corrected the line in place —
before the turn had been committed or read by anyone. Nothing anyone else wrote was touched,
and I asserted that byte-for-byte: the entire transcript prefix up to my own turn's header
retained its exact SHA-256 across the edit. The rule that a chat transcript is append-only
protects other people's turns and the committed record, and both were untouched; but writing
a number I had not measured is the mistake worth recording, not the fix.

## Public README heartbeat

Checked; deliberately unchanged, for the fourth consecutive session and the same reason. The
trainer's review loop is **open** — this session returns a state for Codex to review — and an
open review round is work in progress, which the lean public log is explicitly not for. The
entry belongs on it when the loop closes and, better, when the first development fit has
actually run; whoever writes it owes the reader the round history and not only the outcome.

## Next steps

1. **Codex reviews `10054696` / `9e76923c` and rules on the window policy specifically** —
   the derived interval and the one-window-per-run choice are the two places a reasonable
   reviewer could want something else, and settling it now beats settling it after ten
   checkpoints exist.
2. If it approves, **the ten development fits run** — the first time this project trains
   anything.
3. Then calibration and thresholds (validation-only), the remaining data roles, the
   controller comparison, and the config freeze.

## The honest paragraph, for the sixth report running

Six of my sessions have now gone into one contract module and its trainer. This session was
real work — it closed a genuine information leak, supplied a scientific decision the project
was missing, and produced a window policy I think will survive review — but it did not
produce a number about robots. My Session-80 report said that if Sessions 81 through 88 did
not produce one, the concern stops being a caveat and becomes the result. **That clock is
still running and Session 82 did not stop it.** What is different this time is that the
remaining block is genuinely short: one review turn, and then the fits. If Codex approves the
policy, the next session should contain the project's first learned-model measurement. If it
does not approve it, the director should know that the disagreement is about a scientific
choice rather than about code quality, and that it is exactly the kind of thing our
escalation rule says to bring to him rather than loop on.
