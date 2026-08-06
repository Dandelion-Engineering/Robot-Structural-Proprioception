# Claude — Human Report, Session 83

**Date and time:** 2026-08-06 04:41 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.
**Progress-report session:** no. My next regular progress report is Session **88**.

---

## Summary

This session was the owner half of a review cycle. In my Session 82 I handed Codex the
development-fit trainer together with a proposed rule for *when* in a run the model is
allowed to look. Codex's Session 82 **approved the rule**, found four defects in the code
around it, repaired them, and handed the state back. My job this session was to check its
four findings against my own bytes rather than take them on report, and then to attack its
repair.

All four findings are real, and I kept all four implementations unchanged. **Two defects sit
one layer below the repair, and both are now closed.** One of them is the more serious kind:
a guard whose whole purpose is to protect a record was, on firing, deleting that record.

The trainer still has not been run. That is deliberate and it remains the honest headline —
see *The clock I am still running against*, at the end.

---

## What Codex approved, and why it matters

The scientific question I put to it was the training window: a model that sees a 768-step
slice of a run has to be told *which* 768 steps, and choosing that number after seeing
results is one of the classic ways a study quietly becomes unfalsifiable.

My Session-82 answer was to make the choice underivable — no command-line option exists —
and to derive it instead from a document both agents approved before the question arose.
Codex checked the derivation against the approved assignment and against Protocol P itself
rather than trusting my arithmetic, and **approved it**:

```text
diagnostic development window   [1000, 1768)   an EXACT reproduction of Protocol P §8
ordinary development window     [ 900, 1668)   the same 500-step post-onset lead
windows per persisted run       1              no unregistered stride
```

It also narrowed one sentence of mine that had overstated the case. I had written that
holding both trajectories at the same time-since-onset makes *excitation the only difference*
between them. That is false — the assignment also gives them different target joints and
different task timing. The defensible claim is the narrower one Codex wrote: the rule removes
an avoidable timing difference without erasing the differences the design deliberately keeps.
I took the correction in full. It is the sort of thing that would have travelled into the
technical report unchallenged.

**This was the one genuinely scientific decision blocking the project, and it is now settled
by both agents.**

---

## Codex's four findings, reproduced against my own bytes

The standing discipline here is that a finding reached by reading a collaborator's message is
not the same evidence as one reached by running it. So I loaded my Session-82 blob and
Codex's repaired blob into a single process — mine written out of Git into the package as a
sibling module and deleted afterwards — and drove the same inputs through both.

Every one of them reproduced:

| what was fed in | my Session-82 code | Codex's repair |
|---|---|---|
| a scheduled trajectory missing from both sensor suites | accepted | refused |
| equal row counts built from **different** simulations | accepted | refused |
| a stored label whose fault-onset moved by one step | accepted | refused |
| a stored label whose fault-onset time moved by half a second | accepted | refused |
| `window_steps = True` | accepted **as a one-step window** | refused |
| a control period of zero | crashed with a division error | refused by name |
| a malformed probe description | crashed inside NumPy | refused by name |

One case is worse than Codex reported it, and it belongs on the record: a control period of
**0.004 seconds instead of 0.002** was *accepted* by my code. It silently halves every
derived step count and produces a schedule that looks entirely reasonable. A wrong-but-plausible
value is the dangerous member of that family; zero merely crashes, which is the safe failure.

---

## Finding S — the guard was deleting the thing it existed to protect

Codex's fourth repair added a guard refusing to start a fit in a directory that already holds
an earlier attempt's output, so a rerun cannot leave a mixed population of old and new model
checkpoints. The reasoning is right and the guard is a good idea.

I ran it. Staged a directory with a prior result document and a prior checkpoint, and started
a fit:

```text
before   dev_fit_result.json  149 bytes, digest a844b691
         dev_fit_C1_seed3.pt  the earlier attempt's model

after    dev_fit_result.json  OVERWRITTEN  — now says "0 fits were run"
         dev_fit_C1_seed3.pt  still there  — now with no record of what it is
```

The checkpoint files store nothing but raw model weights. **The result document is the only
place that records which dataset, which random seed, which sensor suite and which version of
the code produced each one.** Every refusal path in the module writes that filename — so the
guard's own refusal deleted the provenance of the exact checkpoints it was refusing to mix
with, and left behind a document actively contradicting what was on disk. The state after the
refusal is *worse* than the state it refused.

There was a second half. The module's very first exit — the one taken when the operator
forgets to say where the data is — also writes that filename, and it sits **above** the guard.
So that path destroyed the record without the guard running at all.

**The repair.** The check now runs at the top of the program, before anything is written at
all, and its refusal takes a new named ending that writes to a *different* filename —
deliberately outside the set of names it is protecting, so the ending that fires *because*
those names are occupied cannot write to them. Re-measured afterwards: the prior document
survives byte-for-byte in all four cases I constructed, and the refusal is readable at the new
name.

**Why no test caught it.** Codex's test staged a stale checkpoint but no stale result
document — so the directory it refused had nothing to lose. The fixture already had the
property that made the defect invisible. That is the same shape as Session 58's and
limitation 111's, and it is the **sixth consecutive round** in this project where the defect
lived one layer below a repair that had just landed. That pattern is no longer a coincidence;
it is the first place to look after any fix.

---

## Finding T — the right property, named with the wrong container

Codex's first repair upgraded "the two sensor suites are matched" from *equal row counts* to
*equal sets of simulation identities*. That is the correct property. A set, however, throws
away multiplicity:

```text
suite C1 carries simulations   a, a, b
suite S  carries simulations   a, b, b

equal counts        yes
equal SETS          yes    <- what the repair checked
matched pairing     NO     <- two of three rows have no partner
verdict at Codex's state: ACCEPTED
```

Now compared as sorted lists, so multiplicity counts. A genuinely matched population still
passes, and a constructed test pins both sides. Honest scope: the delivered dataset has **zero**
duplicate identities, so this cannot fire against the data we have. It is a guard for the
population the delivered set is not — which is the only population it was ever written for.

---

## Attacking the repair: 23 deliberate corruptions, twice

The instrument here is a mutation sweep: break one safeguard at a time and confirm a test
objects. A safeguard nothing objects to is a safeguard that is not being kept honest.

```text
23 cases | 22 caught | 1 survivor | 0 anchor failures | both passes identical
```

The **first** run had eight survivors, and five of them had a single shared cause worth
naming, because it is a trap that will recur. Codex's repair bound the stored fault-onset in
*two* independent ways — an index and a time. Its test fixture, however, computes the time
*from* the index, so the test moves both at once and **either check alone catches it**. Each
half could therefore be deleted with the whole suite still green. Two conditions written
side by side are two mutually redundant guards until something drives them apart. Closed with
a pair of tests that move exactly one field each, plus a boundary case — the agreement
tolerance could be widened from a **trillionth of a second to a full second** and nothing
noticed.

The same cause explains the rest: a zero control period was the only wrong value ever
supplied, so the rule that pins the period exactly could be weakened to "not zero"; and two
type guards had no state that could fail them. All closed.

**One survivor remains, and it is mine rather than Codex's.** A check I wrote in Session 82 —
that the number of training windows equals the number of runs — survives the focused sweep
*and* the full 1,515-test suite, because the function that builds them appends exactly once
per run and has no path that skips one. The equality is forced by construction. **My own
Session-82 summary described it as a run-time cross-check, and that overstated it.** It stays
as a regression guard against a future edit, but the code now says plainly that it is not
evidence the property was measured.

I also deleted one guard Codex added: a check on the control period inside a helper whose only
three callers all validate that value first. The sweep confirmed it could be removed with the
suite green — an unreachable guard is a branch no test can exercise, which is exactly the
reason I gave in Session 82 for declining to add one elsewhere. I said so explicitly in the
handback and offered to restore it if Codex prefers the symmetry. That is its call, not mine.

---

## Verification

```text
focused trainer tests      48 passed        (Codex's state: 37)
focused under python -O    48 passed
FULL PACKET SUITE          1,515 passed in 121.01 s   (Codex's 1,504; +11, no regressions)
mutation sweep             23 cases | 22 caught | 1 survivor | 0 anchor failures
                           both passes identical; restore digest re-checked
survivor re-checked        against the FULL suite as well: still survives (forced)
compileall / diff hygiene  clean
production plan probe      10 arms planned, 0 fits, 0 rollouts
derived schedule           [1000, 1768) and [900, 1668) — unchanged by my edits
real-data touches          the manifest (304 development rows) and the approved
                           assignment. Zero observation payloads, zero label payloads,
                           zero checkpoints. Pilot / validation / test: zero reads.
fits / checkpoints         0 / 0     generation 0     rollouts 0
```

---

## The transcript-order incident

Codex's Session-82 review message landed in the middle of the shared transcript instead of at
the end, because a patch matched a repeated signature line. Codex caught it itself, retained
the misplaced copy, and appended a dated correction at the true end. My standing monitoring
duty is to verify this at the Git level rather than from the file, and I did: **both writes
were additions only** — `+143/−0` on the technical transcript and `+51/−0` on the monitoring
thread — with nothing deleted, moved or rewritten.

The correction I added is about what a reader is left with rather than about the repair.
The transcript's *chronological* order is now permanently broken in the middle, because dated
entries are never edited. Anyone reconstructing the sequence from line numbers will get it
wrong at line 19,334; the physical end is the authoritative order.

---

## The clock I am still running against

**Seven of my sessions have now gone into this contract module and its trainer, and the model
still has not been trained.** My Session-80 report said that if Sessions 81–88 do not produce
a number, the concern stops being a caveat and becomes the result. That clock is still
running and this session did not stop it.

What is different, and I think genuinely different rather than the same sentence again: **the
scientific blocker is gone.** The window policy was the one decision that needed both agents
to agree on something other than code quality, and Codex approved it. What remains between
here and the first learned-model measurement is one more code review round on two files, with
the loop's own history suggesting it should be a short one — the last round found no
behavioural defect in the reviewer's object, and both defects I found this session were in
code added *during* review rather than in the design.

I said so in the handback: if Codex's re-review finds nothing behavioural, that is the signal
to close rather than to hunt for one more. If it finds something, it will be worth having
found. Either way I would expect Session 84 to close this loop and Session 85 at the latest to
contain the project's first learned-model number.

---

## Files created or updated

| Path | What changed |
|---|---|
| `Reproducibility Packet/scripts/utils/dev_fit_trainer.py` | Findings S and T repaired; one unreachable guard removed; the forced check documented honestly. `+65/−12`. Now blob `b9d7bb6f`. |
| `Reproducibility Packet/tests/test_dev_fit_trainer.py` | 11 tests added: the destruction case, the exit-ordering case, the plan-mode accept side, the multiset case, both halves of the onset binding, the tolerance boundary, the wrong-period case, two shape guards, and the exit-table equality pin. `+291/−3`. Now blob `3a81eecc`. |
| `chats/Claude-Codex/Phase 2 Integration and Config Freeze/...- Active.md` | My Session-83 review turn. `+180/−0`. |
| `chats/Claude-Codex-Human/Transcript Order Monitoring/...- Active.md` | Independent Git-level verification of the append-order recurrence. `+47/−0`. |
| `agents/Claude/Session Summaries/HumanReport83.md` | This report. |
| `agents/Claude/Summary of Only Necessary Context.md` | Rewritten for Session 84. |
| `agents/Claude/README.md` | Refreshed. |

**Not touched:** the public Live-Run README (the loop is open — an open review round is work in
progress, which the lean log is explicitly not for), the packet README, `dev_fit_contract.py`
and its tests (closed and jointly approved), Protocol P, the draft config, and every result
artifact.

---

## Next steps

1. **Codex re-reviews `b9d7bb6f` / `3a81eecc`** and either approves those exact bytes or
   contests them. It also owes a ruling on the deleted control-period guard and on the sixth
   named exit, both of which I flagged as its call.
2. **When and only when both agents approve the same bytes**, the ten development fits run —
   the project's first learned-model measurement.
3. The standing gate is unchanged and literal until then: no fit, no checkpoint, no read of a
   pilot/validation/test outcome, no generation, no rollout.
