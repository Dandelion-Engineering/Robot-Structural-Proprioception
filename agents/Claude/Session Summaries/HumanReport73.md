# Claude — Human Report, Session 73

**Date and time:** 2026-08-04 12:32 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **151**.

---

## Summary

Two things happened this session, and the second is the one worth your attention.

The first is procedural and expected: Codex's Session 72 gave the second independent read
that Step 3 of the frozen payload-boundary extension requires, and approved the same plan
bytes I approved. Step 3 is therefore complete, and the next step in the protocol is a
joint execution authorization. **I issued my half of it.** It is not in force — the
protocol says the authorization is issued *by both agents*, so Codex owes the other half,
and nothing may run until that exists. I was careful not to run anything on my half alone.

The second is a finding, and it is the kind that only appears when you go looking at what
you are about to authorize rather than at the document you are about to name.

**The one simulation rollout I am authorizing can be destroyed by a stray file write, and
nothing in the code prevents it.** The replay gate — the check that re-runs one known
simulation and compares it to a stored reference, to prove the ordinary construction path
still behaves the way it did when it was pinned — takes a snapshot of every file in the
packet and at the repository root before its rollout, and another one after, and fails if
*anything* changed. That is a good check: the replay is supposed to write nothing. But by
the time it runs, the rollout has already been spent. So an incidental write — a Python
bytecode cache, a test-runner cache, a log file — would not merely fail a check. It would
convert the single authorized rollout into a terminal failure, and re-running would need a
whole new joint authorization.

Nothing filters that watch list. `__pycache__`, `.pytest_cache`, and the repository root's
own `MUJOCO_LOG.TXT` are all inside it.

I measured the two mechanisms I could name, and both are clean: a plan-mode run (which
imports the same code and compiles eight physics models, so it is the closest thing to the
real run that costs nothing) changed **0 of 3,203 watched files**, and the bytecode risk
is closed by construction rather than by luck — the only lazily-imported module on this
path is already imported at the top of the file that lazily imports it, so no new `.pyc`
can appear inside the window.

What no measurement can close is a **concurrent writer**. Running the packet's own test
suite writes a cache directory inside the packet; if that overlapped the rollout window, it
would burn the rollout. So the authorization carries an operational rule with it: **while
the real run happens, nothing else may touch the packet or the repository root** — no
tests, no second agent session, no editor save. The protocol already said "run it as a
background job and poll the results file, not the console." This session is the reason that
instruction has teeth.

## What I did before authorizing, and why I did it

An authorization for one rollout is worth having only if the rollout is likely to reach the
thing it is being spent on. The replay gate's own code says, in as many words, that every
check which must hold *before* it spends its rollout is reachable at zero cost. I took it
at its word and ran all of them against the real retained dataset:

- all four pinned inputs present and matching their stored fingerprints (the protocol
  document, the assignment document, and the two reference simulation files at 3.2 MB and
  0.93 MB);
- the context binds, and the replay source resolves to exactly one reservation and one
  identity row;
- the two reference files carry exactly the 20 and 38 entries the comparison expects;
- the file-watch list resolves to 3,203 files, far above the floor below which a
  "nothing was written" claim would be certifying an empty set.

Fourteen checks, all passing, in **0.39 seconds** — against 25 to 36 seconds for a single
rollout, so the elapsed time itself is evidence that no simulation hid inside it.

**Two of those checks are ones the gate itself only reaches *after* the rollout is spent,
and I deliberately pulled them forward.** The retained manifest row lookup and the row
comparison sit below the rollout in the code; a duplicated, missing, or disagreeing row
would have been discovered in exchange for the authorized rollout. Run now, they pass. That
is one entire class of failure retired *before* the authorization rather than *after* it.

I said plainly what this does not cover: the rollout's own comparisons — the 20 privileged
simulation fields and 38 observation entries — can only be checked by generating them,
which *is* the rollout. The gate can still legitimately fail there, and if it does, that
means something real: the default construction path moved.

I also refused to name a fingerprint on the assumption that naming it constrains anything.
I drove the authorization gate directly with the committed plan and fourteen neighbouring
states: it accepts the exact document under its own fingerprint and refuses a
one-character-different fingerprint, an upper-case one, a truncated one, an empty one, a
plan marked invalid, a plan marked terminal, an artifact that is not a plan, a plan with a
mass removed, and a foreign plan that records a machine path even when that foreign plan is
named by its *own* correct fingerprint. And I recorded the second layer that makes the one
remaining gap harmless: a content-edited plan named by its own fingerprint does pass the
naming gate, and then dies at the very next check, which rebuilds the plan from scratch and
compares it — **at a cost of zero rollouts**, before the replay gate is ever called.

## One thing I corrected in how we had been writing, not in what we had been doing

Codex and I had both been using the shorthand *"authorizing exactly the one replay
rollout."* Read on its own, that sentence licenses one rollout and nothing else — which
would make the actual execution step, which costs up to 127 rollouts, unrunnable.

Neither of us meant that, and Codex's own next-steps list makes clear it expects the full
run. But the authorization is precisely the document a stranger reads later, so I pinned
the reading rather than leaving it to be reconstructed. The protocol calls the thing being
issued an *execution authorization* and then says it *also* authorizes the replay rollout;
that "also" is additive. The replay gate is called out separately because it is a
precondition run rather than one of the extension's own 126 measurements, and could
otherwise be read as falling outside an "extension execution" authorization.

So my half states exactly what it licenses — one invocation, once, in the fixed stage
order, 0 to 127 rollouts as the protocol's exit table schedules, including the named replay
rollout — and exactly what it does not: a second invocation (a failed run needs a *new*
authorization, not a retry), the pending amendment, the final configuration, or any use of
the result before both agents have audited it. I asked Codex to confirm the same scope in
its half, since two halves that license different things are not a joint authorization.

## Challenges, and how they were handled

**My own transcript-append tool failed, after its checks had passed.** The first attempt
appended the turn correctly and all four of its safety assertions ran and passed — and then
the tool crashed on a type error in its *final print statement*, before it reached the
branch that reports the verdict or restores the file. The turn was on disk and correct, but
I had not seen the verdict, and accepting an unseen verdict is exactly the habit this
project has spent dozens of sessions unlearning. I restored the file and re-appended with
the fixed tool.

That restore is worth recording because it changed the file's **bytes** without changing
its **content**. This repository is developed on Windows with automatic line-ending
conversion and the chat transcripts carry no pin, so restoring from git materialized every
line with Windows endings — taking the file from a mixed 1,232,265 bytes to a uniform
1,237,981 bytes at the same 19,117 lines. Git saw no change at all, before or after; the
stored version is unaffected. **No transcript content was altered, moved, or lost.** I
recorded it in the chat so that if Codex compares against a byte count rather than a line
count, it does not spend a session chasing a phantom. The tool now matches whatever line
ending the file itself uses instead of imposing one.

I also found and fixed a second defect in the same tool: it did not emit the `---` separator
the transcript uses between turns, so the first attempt would have joined my turn to
Codex's without the visual break every other turn in that file has.

## Decisions I made

1. **Issue my half of the authorization rather than wait.** Codex's approval discharged
   Step 3; the next step is mine to take, and holding it back would have cost a full session
   for nothing.
2. **Audit the pre-rollout surface first.** The alternative — authorize now, discover a
   missing manifest row later — costs the rollout and a second authorization round.
3. **Pin the authorization's scope explicitly instead of inheriting the shorthand.** This is
   the document that licenses the largest block of simulation the project has spent; its
   scope should not have to be inferred.
4. **Add nothing to the public log.** Half an authorization licenses nothing and changes no
   public state; the newest entry there is still exactly true. The entry belongs on the log
   when the run has actually happened, and it will owe the reader an honest cost line.
5. **Keep every instrument outside the repository.** All three probes and the append tool
   live in the session scratchpad, so this session added no untracked file to the packet.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` (my Session-73 turn, `+215 / −0`, header at line 19,121, Claude physically last at line 19,332)
- `agents/Claude/README.md`
- `agents/Claude/Session Summaries/HumanReport73.md` (this file)
- `agents/Claude/Summary of Only Necessary Context.md`

No file inside `Reproducibility Packet/` was changed. The plan artifact was read, not
edited.

## Verification

```text
approved blobs, all seven, worktree == the states both agents approved
plan.json  worktree blob == HEAD blob == 04f2bccd   5,386 B   CR 0  LF 0
canonical digest of the parsed plan == 15298da4...030be3
pre-rollout audit          14/14 PASS in 0.39 s
authorization binding      14/14 PASS (require_authorized_plan driven directly)
ephemerality probe         0 added / 0 modified / 0 removed of 3,203 watched files
focused tests              170 passed in 2.70 s
focused under python -O    170 passed (pytest's optimized-assert notice only)
full packet suite        1,306 passed in 121.80 s
compileall                 clean
payload_boundary.json      absent      config/config.json      absent
physical rollouts this session 0   |   project Protocol-P total 151
```

## Cross-review

I read Codex's `HumanReport72.md` and its Session-72 turn in the Phase-2 transcript. Its
independent audit of the plan reaches the same conclusions mine did by a different route —
notably, it rebuilt the anchor from the committed screen result rather than from the
program's constants, and its first key-fingerprint reconstruction failed because it used the
extension-facing word `structure` where the closed schema uses `structural`. That failure is
worth more than the eventual match: it demonstrates the fingerprint is sensitive to the
condition field rather than merely counting masses. I found no correction to propagate
forward. Codex likewise reported reading my Session-72 report and progress report and
finding nothing to carry.

## Next steps

1. **Codex issues its half of the Step-4 authorization**, confirming the same scope. Only
   then is the authorization in force.
2. **Step 5 runs once**, as a background job, with nothing else touching the packet or the
   repository root, polling the result file rather than the console. Budget: up to 127
   rollouts; the executed screen's own record suggests roughly 60–70 minutes of wall clock
   for a full run.
3. **Both agents independently audit the persisted result** before it informs anything.
4. Amendment A2, assignment replacement, the final `config.json`, and all confirmatory work
   remain downstream and blocked.

Next regular progress report: my Session 80, unless a phase transition or an approved
amendment triggers one sooner.
