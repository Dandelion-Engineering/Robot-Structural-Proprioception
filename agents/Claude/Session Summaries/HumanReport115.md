# Claude — Human Report, Session 115

**Date and time:** 2026-08-11 00:44 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. My next regular progress report is Session 120, unless a phase
transition or an approved Claim-Sheet amendment fires one sooner.

---

## Summary

Two things happened this session. I closed the review loop Codex opened on the public log entry I
wrote last session, and I built step 3 of the rung-2 sequence — the executable that will actually
fit the larger network, and the 142 tests that measure it. Nothing was trained, nothing was
selected, and no result of any kind was produced. The executable exists; running it is a separate
permission that has not been given.

The part of the session I think is worth the director's attention is not the code. It is that a
tool I built to check my own tests found a real hole in them, and that the same tool, while doing
so, briefly did something it should not have been able to do.

### What was accomplished

**1. The public-log review loop is closed.** Codex made two precision corrections to my Session-114
entry on the public README: it changed "five further joint approvals" to "five further gated
steps," and it changed "eleven deliberate defects" to "eleven deliberate wiring mutations — nine
faults and two harmless controls." I re-opened the file rather than reading its report and agreeing
with it, verified the change is exactly one line and that nothing else in a 144 KB file moved, and
kept both corrections. Both are right. My own sentence had called all eleven cases defects and then
explained two paragraphs later that two of them were harmless, which is a contradiction inside one
sentence; and "gated steps" is checkable against something that exists, where "joint approvals" was
not. I explicitly approved Codex's exact bytes, so both agents now approve the same state.

I noticed one thing I chose not to act on and said so rather than staying quiet: Codex's inserted
em dashes are unspaced where the document's dominant style is spaced. There are four pre-existing
unspaced em dashes in older entries, so there is precedent, and a round-trip between two agents to
change whitespace is not worth what it costs.

**2. Step 3 of the rung-2 sequence is built.** Two new files:

- `Reproducibility Packet/scripts/utils/rung2_escalation.py` — 89,132 bytes, Git blob `735f8dee`
- `Reproducibility Packet/tests/test_rung2_escalation.py` — 89,321 bytes, Git blob `7cefcb63`, 142 tests

What the executable is for, in plain terms: the project already has an approved program that fits
the *small* network, and it cannot fit the large one — its only network-construction line names the
small one by name. So the fitting loop has to exist a second time. The obvious danger is that the
second copy quietly differs from the first, and then any difference we measure between the small
and the large network is partly a difference between two programs rather than between two
architectures.

The frozen design's answer, which this executable implements as its actual structure rather than as
a promise, is that there is **one** loop, and what varies is a *factory* handed to it — a small
argument that says which network to build. The ten measured runs pass the large-network factory.
The two verification runs pass the small-network factory and are required to reproduce two existing
approved results **bit for bit**. Because both go through the identical code, a verification that
passes really does certify the path the measurements take.

I checked that this can actually hold before handing it over, rather than discovering it at
execution time: fitting through the new loop with the small-network factory reproduces the approved
program's own output exactly — every weight identical, every per-epoch loss value identical — even
with the machine's random-number state deliberately disturbed first.

**3. I measured my own tests, and they had a hole.** The project's standing practice is to break
the code on purpose, one change at a time, and check that the tests notice. I ran 23 such changes,
twice, with identical results both times.

Twenty of them were real faults and all twenty were caught. Three were deliberate harmless changes
and all three correctly survived — which is what shows the instrument is discriminating rather than
simply alarmed at everything.

But one real fault survived the first run of that measurement, and it is the finding of the session.
I changed the line that hands the run's seed to the network factory so that it always handed over
seed zero. Every test still passed. The reason is uncomfortable and general: my reproducibility
tests ran the same seed twice and compared, so pinning both runs to the same wrong seed left them
agreeing perfectly; and the one test that uses a *specific* seed happens to use zero. The
consequence of that fault reaching a real run would have been ten results claiming to come from five
different starting points while actually sharing one — quietly destroying the five-seed structure
the whole comparison rests on, with a completely green test suite. I closed it with two independent
tests rather than one.

### The challenge, and how it was handled

One of my twenty-three deliberate faults removes the guard that stops the program writing into the
directory holding the project's ten approved trained models and their sole provenance record. The
test that catches that fault worked by aiming the program at the **real** protected directory and
checking nothing appeared there. It caught the fault — but the broken version of the program, before
failing the test, wrote four small refusal files into a new subdirectory of that protected tree.

Nothing was damaged. The four files record zero of everything; the ten model files and both approved
documents were untouched, and I re-verified both documents' checksums against their approved values
before doing anything else. I removed the leftover directory.

The lesson is more interesting than the incident. **A test that checks a safety guard by pointing a
real destructive path at it is only safe while the guard is present** — and "the guard is absent" is
precisely the condition the measurement exists to create. The check and the thing it protects were
the same object. I split the test in two: one version calls the guard directly on the real protected
path, where no write is reachable even if the guard is gone; the other drives the whole program
against a *simulated* protected directory in a temporary folder, so a broken version writes
somewhere harmless while the assertion still fires. Re-measured afterwards: the fault is still
caught, and the real directory is untouched.

I flagged the same exposure to Codex, because if any other measurement harness in this project
points a real destructive path at a guard, it has the same problem.

### Decisions I made

- **No "output directory is dirty" refusal in this executable.** Its predecessor needed one because
  ten of its runs shared a directory; this one has a single configuration and claims a fresh
  directory that must not already exist, so there is nothing an earlier attempt could have left
  behind. I pinned the deliberate absence with a test, so re-adding it later would be a decision
  rather than a copy-paste, and I handed the call to Codex to overrule.
- **A run that completes but whose training objective did not improve is a completed run, not a
  failed one.** The frozen design gives those two outcomes different sentences and different rows in
  its pre-registered interpretation, so I treated them as deliberately separable and pinned that
  separation with a test. Also handed to Codex.
- **The interpretation functions are defined in the executable and never called by it.** The rules
  that turn the raw record into a finding belong to a later, separately reviewed script; putting the
  definitions here means there is only ever one definition of each. I verified by inspecting the
  program's own call graph, not by reading, that the executable calls none of them.
- **One helper is a deliberate copy.** The approved program's refusal-file writer is hard-wired to
  its own directory name and cannot be edited, because editing it would change a recorded identity
  and invalidate the project's ability to re-verify its own existing results. So this module carries
  a near-identical copy, and a test drives both writers with the same input and requires the written
  bytes to be identical and the paths to differ in exactly one component.

### Reasoning paths explored

The main one worth recording is the choice of what the verification runs compare against. It would
have been easier to have the new program verify itself — fit twice and check the two agree. That
proves the program is deterministic and proves nothing about whether it matches the approved one.
The design's requirement, which I kept, is that it must reproduce two *existing* approved results
that were produced months of sessions ago by different code. That is a comparison whose two sides
come from genuinely different places, which is the property the project has repeatedly found to be
the one that matters.

### Insights gained

- Two tests that both pass can be blind in exactly the same way. My reproducibility tests compared
  a seed against itself, so a fault that replaced the seed everywhere was invisible to all of them
  at once. Redundancy is not independence.
- A safety check cannot protect the thing it brackets while it is the thing being removed. This is
  the same shape as an earlier finding in this project about a check that ran after an expensive
  operation, one level further out.

### Files created or updated

- `Reproducibility Packet/scripts/utils/rung2_escalation.py` — **new**, the step-3 executable
- `Reproducibility Packet/tests/test_rung2_escalation.py` — **new**, 142 tests
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — one appended turn, `+198/-0`, 1,954,669 → 1,966,069 bytes
- `agents/Claude/README.md` — the rung-2 bullet updated in place, `+1/-1`
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten
- `agents/Claude/Session Summaries/HumanReport115.md` — this report
- Removed: `Reproducibility Packet/results/dev_fit/nested/` — four zero-count refusal files written by a deliberately broken program during the measurement described above; untracked, unapproved, and not evidence of any authorized run

The root `README.md` was **not** changed. I re-read its playbook in full and judged that a build
session whose artifact has not yet been reviewed is not a finished artifact, a phase close, or a
noteworthy event. The project's own precedent agrees: no public entry was logged when the previous
executable was built.

### Verification

```text
new test file, normal         142 passed in 3.58 s
new test file, python -O      142 passed, 1 expected pytest warning
whole packet suite          2,004 passed in 151.88 s   (1,863 before + these 142)
mutation measurement           20 real faults caught, 3 controls survived, 0 bad anchors,
                               two passes identical, file bytes restored and re-verified
```

### Resources spent

Zero fits, zero checkpoints, zero rollouts, zero data generation, zero analyzer invocations, and
zero reads of the pilot, validation or test splits. No manifest, sensor file, label payload or
trained-model file was opened at any point. Every measurement above ran on synthetic tensors and
synthetic training examples. Plan mode was exercised three times into a scratch directory outside
the repository to check it produces identical bytes regardless of destination; **the gated plan
action of step 4 has not been taken and no plan artifact exists anywhere in the repository.**
Lifetime totals are unchanged: 278 rollouts, 13 fits.

### Next steps

1. **Codex reviews the step-3 executable and its tests.** Two judgment calls are explicitly handed
   to it, listed above. If it edits either file, closing that loop is mine.
2. **After that loop closes — and only then — step 4:** run plan mode for real, and have both agents
   review the artifact it writes.
3. Steps 5, 6 and 7 remain behind their own separate gates: the two-half execution authorization,
   the read-only analyzer, and the exact-state review that must precede any interpretation.
4. My next regular progress report is Session 120.
