# Claude — Human Report, Session 84

**Date and time:** 2026-08-06 08:31 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278.**
**Progress-report session:** no. My next regular progress report is Session **88**.

---

## The short version

Two things happened this session, and the second one is the one that matters.

1. The trainer's review loop **closed**. Codex's Session-83 state came back with two findings
   against my Session-83 state; I reproduced both against my own bytes, found one more,
   decided it was a disclosure rather than a block, and approved Codex's exact blobs. Both
   agents have now approved the same bytes, so the executable gate is open.

2. **The ten development fits ran.** Ten models trained, zero simulation spent, and the
   project has its first learned-model numbers after eighty-three sessions without one.

The result is more interesting than "it trained." It learns — comfortably above baseline —
and the most useful thing it produced is a warning about the *experiment*, not about the
robot: the run-to-run variation caused purely by the random starting seed is roughly three
times the size of the effect the study is designed to detect. That surfaced before any of
the reserved comparison data has been touched, which is the cheapest possible moment to
learn it.

---

## What I did, in order

### 1. Owner re-review of Codex's trainer state

Codex returned `dev_fit_trainer.py` at `caa00418` and its tests at `cbc4064f`, with two
findings against my Session-83 state.

**Finding U — reproduced, accepted.** Codex's claim was that my new refusal artifact
(`dev_fit_output_refused.json`, added in my Session 83 so a stale-directory refusal could
not overwrite the record binding checkpoints to their provenance) sat *outside* the
cleanliness guard as well as outside the protected namespace. So a directory holding only
that artifact was accepted as clean, the run fell through to the missing-data exit, and the
directory ended with two contradictory terminal records.

I did not take that on report. I wrote my own blob back out of git into the package so its
relative imports resolved, drove **both** blobs in one process across four staged
directories, and read the directory back each time:

```text
                              guard      main()   files afterwards
MINE   b9d7bb6f  refusal only ACCEPTED   rc=4     refusal + dev_fit_result.json (X_DATA_MISSING)
CODEX  caa00418  refusal only REFUSED    rc=6     refusal only
```

Exactly as reported. The repair is right and the mutation sweep confirms both halves of it
are load-bearing.

**Finding V — reproduced, accepted.** A docstring still carried the superseded sentence
saying equal post-onset lead makes excitation "the only thing that differs" between the two
development trajectories — the overstatement Codex narrowed in Session 82 and I accepted
then. `git cat-file -p b9d7bb6f | grep excitation` returns exactly one line; Codex's blob
returns zero. Correct finding, correct scope, documentation only.

**The thing I went looking for and did not find.** Codex's repair makes the refusal artifact
*both* the guard's trigger and the refusal's write target — which is precisely the collision
my own Session-83 Finding S was about. I expected a recurrence. I measured instead of
assuming, and there isn't one: the refusal document's persisted content is invariant
(`authority`, `exit`, `reason_class`, `fits_run: 0` — the stale list goes to stdout and never
to the file), so a second refusal overwrites the first with the same four keys and nothing is
lost. I am recording that I looked and came up empty, because the pull to narrate a seventh
consecutive "defect one layer below the repair" round is strong and would have been false.

### 2. Finding W — mine, and disclosed rather than blocked

Widening the same probe did surface something real. Because the refusal reports through the
name whose occupancy triggers it, an *unwritable* occupant of that one name turns a named
terminal exit into an uncaught traceback. Two artifact names crossed with three occupant
kinds, both blobs:

```text
occupant of dev_fit_output_refused.json      MINE      CODEX
   ordinary file                             rc=4      rc=6
   read-only file                            rc=4      UNCAUGHT PermissionError
   directory                                 rc=4      UNCAUGHT PermissionError
occupant of dev_fit_result.json              rc=6      rc=6  (all three kinds)
```

Read the halves against each other: an unwritable *result* artifact refuses cleanly every
time, because the refusal writes a different name. Only the name that is simultaneously
trigger and target can kill the refusal.

**I disclosed this rather than blocking on it, and I want the reasoning on the record because
the choice favours me.** Nothing is destroyed in any crashing cell — the original bytes
survive, so this is Finding S's *shape* without Finding S's *harm*. It is unreachable from
the authorized invocation, which runs into a fresh directory. And it is a member of a class
Codex has already ruled on: limitation 116's forty loud foreign-exception escapes, which it
ruled in Session 80 stay open and disclosed. Blocking would have cost another full round on
these two files and deferred the first learned-model number again — which is exactly why I
handed Codex the ruling instead of taking it, and said so in the chat.

I also measured the fix so the ruling is cheap to make: a one-line change (skip the refusal
write when the artifact is already present) **survives the entire focused suite**, which
says both that the fix breaks nothing and that the current behaviour is unpinned coverage.

### 3. Verification, then approval

```text
Finding-U reproduction   both blobs in ONE process, 4 staged cases each, directory read back
Finding-W grid           2 artifact names x 3 occupant kinds x 2 blobs, main() driven
mutation sweep           15 cases | 14 CAUGHT | 1 survivor (the W fix) | 0 bad anchors
                         | both passes identical | restore digest re-verified
focused suite            49 passed;  under python -O  49 passed + expected warning
FULL PACKET SUITE        1,516 passed in 119.96 s — no regression
compileall clean         git diff --check clean
production plan          X_PLAN_OK, 10 arms, diagnostic [1000, 1768), ordinary [900, 1668)
```

The diagnostic window is still exactly Protocol P's pre-registered `[1000, 1768)`, which is
the whole justification for the derived window policy. **I approved `caa00418` / `cbc4064f`.
Both agents have now approved the same bytes; the loop is closed.**

### 4. The ten development fits

Codex's Session-83 report wrote its half of the authorization explicitly ("only after that
closure may the ten predeclared development-only C1/S fits run in a new output directory");
I wrote mine in the chat before running anything, because my own Session-81 lesson says a
closed review loop is not by itself an authorization. Both halves exist in writing.

```text
X_FIT_OK   10 arms   0 rollouts   0 generation   device cpu, all settings defaults
census     both trajectories, both suites, 76 rows each — 152 examples per arm
artifact   results/dev_fit/dev_fit_result.json, 33,193 B, 10 distinct checkpoint digests,
           0 drive-letter paths, 0 backslashes, no repo or user name (checked, not assumed)
```

---

## What the fits actually showed

### The reported loss is not a learning signal

Seven of the ten arms report a **negative** final loss. That is not a defect and not learning
either: the composite loss includes a Gaussian negative-log-likelihood term carrying
`+ log_scale`, which is unbounded below. Decomposed in-sample:

```text
                class      loc      sev      ood     total
C1 (5 seeds)    0.434    0.514   -1.162    0.023   -0.190
S  (5 seeds)    0.557    0.557   -1.116    0.017   +0.016
```

The severity term is what makes the totals negative and it is also the term that varies most
between arms — so a reader handed only `final_loss` would be ranking arms by how confident
the severity head became. `final_loss` and `loss_history` are exactly what the persisted
artifact carries. I proposed to Codex that the artifact persist the four terms separately;
I did not make the change, because that is a schema we both just approved.

### It learns

In-sample, against the arm's own label census (`healthy 8 / structure 16 / actuator 32 /
sensor 96` of 152):

```text
                     C1        S      baseline
class cross-entropy  0.434   0.557    1.010   (empirical prior)
accuracy             0.870   0.817    0.632   (majority class)
macro-F1             0.682   0.650    —
```

Both suites clear both baselines, so the rung-1 implementation optimizes and the whole data
path works end to end. **This is in-sample fit, not generalization** — which under the
contract's bound 5 is all a development fit is permitted to be.

Before reading any direction into C1 versus S I checked that S's extra channels actually
arrive, because "S is worse" and "S's gauges never reached the network" look identical in a
metric. They arrive: the four gauge rows carry real magnitude for S and are exactly zero in
both the value and mask halves for C1.

### The finding worth acting on — the seed spread swamps the effect

Paired by seed, which is the pairing the confirmatory design uses:

```text
seed      0        1        2        3        4      mean     sd
C1     0.640    0.631    0.829    0.487    0.824    0.682
S      0.715    0.670    0.590    0.591    0.684    0.650
S-C1  +0.075   +0.039   -0.239   +0.104   -0.140   -0.032   0.150
```

The pre-declared success bar is **≥0.05 absolute macro-F1** over **≥5 seeds**. Here the
paired difference has a standard deviation of **0.150** across five seeds — three times the
effect the bar asks us to resolve. C1's own spread across seeds is 0.343.

I want to be careful about what this does and does not say. It is in-sample, at 20 epochs on
152 examples, at one capacity rung, with no early stopping, and in-sample spread is not
held-out spread. But it is the first direct look at how much this architecture moves with its
seed alone, and it belongs in the Gate-6 sample-size conversation rather than being noted and
dropped.

### The direction is against the hypothesis, and rung 1 cannot settle that

Per-class F1, paired S−C1: healthy **+0.100**, structure **−0.069**, actuator **−0.108**,
sensor **−0.052**. The structurally-sensed suite fits its own training set slightly worse on
three of four classes.

I do not think that is a statement about information, and the reason is in the design: S is
C1 plus four gauge channels at a **fixed 39,594 parameters** — strictly more input, identically
much capacity. The project's own efficiency standard already names this case (a null from an
undersized model is evidence about the model, not proof the signal is absent), and Slot 9's
capacity ladder is the instrument built for it. The honest reading is that the ladder must be
climbed for S before any C1-versus-S conclusion is drawn.

---

## Challenges, and how they were handled

**The pull to find a seventh consecutive "one layer below" defect.** Six consecutive rounds
have had the defect sitting beneath the repair, and I have written that down as a search
strategy rather than an observation. It works — it found Finding W. It also produced a
hypothesis (a Finding-S recurrence in the new refusal write) that measurement falsified, and
the disciplined outcome was to say so rather than to keep hunting for a framing that made the
round look sharper.

**A choice that favoured me.** Approving rather than blocking unblocked the fits and ended a
seven-session drought. That is precisely the shape the project's own rule covers: measure how
much it favours you, say so, and hand the decision to the reviewer. I did all three.

**I fabricated a timestamp.** The header on my second chat turn reads 08:52 PDT; the shell
said 08:29. I typed the time from estimate rather than reading it. Dated entries are corrected
forward rather than edited here, so the bad stamp stays with a correction note beside it. It
matters beyond tidiness: a reader comparing that stamp against this report would have seen a
turn timed *after* the report describing it and reasonably concluded the transcript order had
broken again. It had not.

---

## Decisions I made

- **Disclose Finding W rather than block on it**, and hand Codex the ruling — consistent with
  its own Session-80 ruling on the same class, and stated together with the fact that the
  choice favours me.
- **Do not edit the approved bytes to fix Finding W or the loss-reporting issue.** Both are
  proposals to Codex. Editing would have reopened a loop that had just closed.
- **Run the fits on CPU at every default setting.** It is the reproducible choice for an
  outside reader without a CUDA machine, and the smallest sufficient one — the whole run cost
  about a minute.
- **Report the training diagnostic as a probe, not an artifact.** The decomposition,
  accuracies and per-class F1 are not in the tracked document; they live in this report and
  the chat until something commits them. Committing them is the natural next piece of work.

---

## Files created or updated

- `Reproducibility Packet/results/dev_fit/dev_fit_result.json` — **new**, tracked. The ten
  arms, their provenance, censuses and loss histories.
- `Reproducibility Packet/results/dev_fit/dev_fit_*_seed*.pt` — ten checkpoints, git-ignored
  by the packet's own rule; the result document above is their sole provenance record.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — three appends,
  `+292/−0`: the approval turn, the fit-results turn, and the timestamp correction.
- `README.md` — Live-Run log entry for the closed loop and the first trained models; banner
  date to 2026-08-06.
- `agents/Claude/Session Summaries/HumanReport84.md` — this report.
- `agents/Claude/README.md` — workspace index refreshed.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

No source or test file was edited this session. `dev_fit_trainer.py` and its tests stand at
Codex's `caa00418` / `cbc4064f`; the dev-fit contract stands untouched at `bd2c0d08` /
`fbd941b5`, verified at those blobs.

---

## Next steps

1. **Codex rules on Finding W** (close the trigger/target collision, or leave it disclosed)
   and on whether the result artifact should persist the four loss terms separately.
2. **Commit the training diagnostic.** The numbers above come from a scratchpad probe. If
   they are going to be quoted anywhere, they need a script and its tests inside the packet.
3. **Climb the capacity ladder for S.** Rung 1 cannot settle the C1-versus-S question, and
   this session's per-class result is the first concrete evidence for that.
4. **Take the seed-spread finding into the Gate-6 sample-size decision** before the
   confirmatory design is frozen.
5. Still blocked and unchanged: pilot, validation and test outcome reads; new generation;
   the final `config.json` freeze; every confirmatory claim.

The project has a learned-model number for the first time. It is a development number, it is
in-sample, and the most valuable thing in it is a caution about the experiment rather than a
result about the robot — which is roughly what a development fit is supposed to produce.
