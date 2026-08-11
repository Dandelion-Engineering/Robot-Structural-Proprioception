# Human Report — Claude Session 122

**Current date and time:** 2026-08-11 14:12 PDT

---

## Summary

This session did one thing and did it carefully: it **published the public account of the rung-2
result** that three previous sessions had deliberately deferred, and handed the exact published
bytes to Codex for review.

That deferral had a named trigger, and the trigger fired. In my Session 121 I said the heartbeat
would not be written until Codex approved the packet-runbook state — because publishing a status
the project has not finished checking says more than the project knows. Codex's Session 121
approved Git blob `f5e677c8…` of `Reproducibility Packet/README.md` exactly as I returned it,
closing the last open loop in the project. So the condition was met, and the entry went out.

The entry is the first public statement of what the larger network actually produced, and it is
not comfortable reading. That is the point of it.

---

## What was accomplished

### 1. The chat tail was read before anything was written

Codex's Session-121 turn resolved all three things I had explicitly handed over rather than
decided unilaterally:

- **Finding BN accepted** — it independently reproduced the per-class non-zero counts and agreed
  the corrected paragraph states the record exactly.
- **Finding BO accepted, including the out-of-scope Step-28 repair.** It ran its own AST/source
  audit, found the single `EQUIVALENCE_ARMS` definition, and ruled that correcting Step 30 while
  leaving its explicit Step-28 parallel false would have made the runbook internally
  inconsistent. I had flagged that repair as a deviation from the round's scope and offered to
  withdraw it; it stays.
- **Finding BP accepted** as useful runbook precision rather than clutter.
- **The `roughly 12×` figure stays unchanged.** I had measured its provenance, deliberately not
  edited it, and handed the call over. Codex ruled that `roughly` plus the explicit per-step unit
  already carries the boundary and that another clause would add bulk without correcting a false
  claim. I accept that without contest.

**No disagreement is open between the agents.**

### 2. The closed state was authenticated against the object, not the report

`git hash-object` on `Reproducibility Packet/README.md` returns `f5e677c8…` and the working tree
is clean, so the bytes Codex approved are the bytes on disk. I did not take that from its report.

### 3. Every figure the public entry would carry was re-derived from primary artifacts

I wrote a small read-only script that opens the tracked analysis artifact, **refuses unless its
raw SHA-256 equals `604d7272…`**, and recomputes from the artifact's own fields, importing no
project module:

```text
rung-2 non-zero F1 counts    healthy 0 / actuator 6 / sensor 10 / structure 0
rung-1 anchor non-zero       healthy 8 / actuator 10 / sensor 10 / structure 10
only zero anchor cells       C1 seed 1 healthy; C1 seed 3 healthy
majority-baseline arms       C1 seeds 0 and 4; S seeds 0 and 3
paired macro sign            recorded {negative 2, positive 2, zero 1}; re-derived independently
                             from the five raw per-seed differences, same result
```

The run counters came from the run record itself (`fits_attempted` 12 = 2 equivalence + 10
rung-2, `rollouts_spent` 0, `generation_runs` 0, `non_dev_reads` 0, exit `X_RUNG2_OK`,
`elapsed_s` 1272.094…), the 304-row census from its own `row_disclosure` field, the equivalence
verdicts from the equivalence artifact (`weights_bit_identical` and `loss_history_bit_identical`
both true on both arms), and rung 1's `39,594` parameters from the frozen design. **Nothing in
the published entry came from memory.**

### 4. The public entry was written and published

One entry, appended to the root `README.md` running log. It carries the two jointly applied
section-5.4 sentences **verbatim as quotations**, with the degeneracy observation in the same
paragraph and immediately after them, so a reader cannot get one without the other.

Around them: the run facts; the equivalence result stated as what it physically is; the read
described as re-scoring twelve checkpoints from digest-authenticated bytes under exact equality;
the design's own advance warning that `OBJECTIVE_REDUCED` is *not* a learning signal, placed
**before** the zeros rather than after them; the zeros themselves; and the efficiency finding
hedged exactly as the runbook hedges it.

**Deliberately absent:** any cause, any trend across the two rungs, anything about C1 versus S,
any capacity or threshold choice, any generalization claim, and any `because` / `therefore` /
`confirms` attached to either licensed sentence.

### 5. The state was handed to Codex with an explicit approval

```text
README.md   (repository root, public Live-Run README)
Git blob (filtered)   964231a49d6b94230697cf9a03ad4e9f540b7fd1
canonical LF sha256   f4002198ea8a2d21cc69914b20891a79029dfc39cdba71b6c57c246e285eb513
                      149,954 B / 210 LF / 0 CR
working-tree raw      0c2c2f19… (150,164 B / 210 LF / 210 CR)
git diff --numstat    +2 / -0        deleted lines: ZERO
```

---

## Challenges, and how they were handled

**The one that actually cost me something.** My first read-back script crashed reading
`arms[].classification.per_class_f1`. That path is not the shape of the `arms[]` rows — it is the
*template string* the anchor rows carry in their `per_class_f1_field`, naming where their values
came from. This is the exact conflation my own continuity file warns about after Session 119
(*"read the field, do not remember it"*), and I walked into it anyway one session after writing
the warning.

It cost about thirty seconds, and the only reason it cost that little is that it **failed loudly
with a `KeyError`** instead of quietly reading something plausible. I read the actual record
shape and repaired the script. The transferable version: *a warning you wrote yourself is not a
guard; the guard is the code that crashes.*

**The measurement trap next door.** The public README is CRLF on disk under `core.autocrlf=true`
and is pinned by no `.gitattributes`, so there are **three** digests available for it and only
one is the committed identity. I published the filtered blob as the identity, and disclosed the
canonical-LF and raw working-tree digests beside it with the reason they differ — so Codex
reproduces the right one rather than discovering a phantom mismatch. This project has been bitten
by that family of confusion repeatedly.

**Verifying the prohibition mechanically rather than by reading.** The forbidden words are
forbidden *as attachments to the licensed sentences*, but the entry legitimately needs to name
them in order to tell a reader they are forbidden. Rather than eyeball it, I flattened the entry
to a single line and searched for every forbidden term. Three hits: all three inside the sentence
that names them as forbidden. One hit for "trend": inside the sentence that refuses to draw one.

---

## Important decisions

1. **Publish now.** The named trigger fired; deferring further would have been the defect, not
   the caution.
2. **One entry, not two.** The runbook closing and the result are the same event from a
   stranger's point of view.
3. **Put the warning before the zeros.** The design's `OBJECTIVE_REDUCED` caveat is what stops
   the status sentence being read as a result. Ordering is the mechanism.
4. **State the equivalence result physically** — bit-identical weights and loss history — rather
   than as "PASS", which means nothing to a public reader.
5. **Keep the inconvenient efficiency finding in.** The larger network costs roughly 12× per step
   while carrying 5.5× the parameters. It is a real result, it cuts against convenience, and it
   is the kind of thing that determines whether work like this can run on hardware ordinary
   people own.
6. **Do not open a new scientific lane in this session.** With this closed, nothing scientific is
   open anywhere in the project. Choosing what comes next is a joint decision, so I asked rather
   than acted.

---

## The question I put to Codex

The project now has **no open scientific lane**. Rung 2 is spent, C7 is spent, Stage 1 is
finished as scoped, and capacity / probability / abstention are validation-owned and undecided
while validation stays shut. I named three candidate directions and asked for its reading before
starting any of them:

1. **Phase-3 work that can legitimately start early** — I am default writer for the Technical
   Report and the Accessible Piece, and both can begin against the existing record.
2. **The Slot-8 verification artifact** — a named completion requirement, not a freeze blocker,
   explicitly meant to be paced into the project rather than assembled at the end.
3. **Something on the freeze path proper** — which, as I read the order, is not mine to open
   unilaterally.

My stated inclination is **(2) then (1)**, because Slot 8 is the one outstanding item whose
absence would actually block completion and whose design gets harder the longer it waits. I did
not start it, because whichever we pick will shape several sessions.

---

## Insights gained

- **A deferral with a named trigger is a real instrument.** Sessions 118 through 121 each checked
  the heartbeat triggers and each declined to publish, for a stated reason, with the condition
  written down. This session the condition was met and the entry went out without anyone having
  to reconstruct why it had been waiting.
- **The ordering of an honest paragraph is load-bearing.** "The check passed" followed by "the
  check is deliberately weak" reads as a result with a caveat. Reversed, it reads as what it is.
- **The strongest contrast in the record is `structure`, not "four non-zero values."** Eight of
  ten anchors carry four non-zero per-class values, not ten — the correction I made last session.
  What *is* unanimous is that every anchor is non-zero on `structure` and every rung-2 arm is
  exactly zero there. The weaker claim was the one that was false.

---

## Files created or updated

- **`README.md`** (repository root, public Live-Run README) — one appended running-log entry;
  `+2/-0`, zero deleted lines; blob `964231a4…`. **Open review round, on Codex.**
- **`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`**
  — appended my Session-122 turn: the confirmation of Codex's approval against the object, the
  published state and its three digests, what the entry says and what it deliberately omits, the
  re-derivation table, my explicit approval, and the open question. `+123/-0`, prior
  `d4a05457…`, post `386b1433…`, 0 CR added, prefix asserted byte-identical.
- **`agents/Claude/README.md`** — current-state lead of the Live-Run README bullet updated in
  place under the file's own maintenance rule (no session paragraph appended).
- **`agents/Claude/Session Summaries/HumanReport122.md`** — this report.
- **`agents/Claude/Summary of Only Necessary Context.md`** — completely rewritten for Session 123.

Scratchpad only, not committed: the read-back script, the prefix-asserting append routine.

---

## Resource spend

**Zero of everything.** Zero fits, zero checkpoints, zero rollouts, zero generation runs, zero
analyzer or C7 invocations, zero plan-mode invocations, and zero pilot / validation / test reads.
The only files opened were tracked artifacts and the frozen design. Checkpoint count unchanged at
67. Nothing this session selects a rung, a capacity or a threshold.

---

## Next steps

1. **Codex reviews `README.md` at blob `964231a4…`.** If it edits or blocks, the owner re-review
   is mine.
2. **Codex answers the direction question.** Until it does, I have no scientific lane to open.
3. **Preserve every boundary this session did not move:** no retry authority, no cause, no rung
   trend, no C1-versus-S conclusion, no later-role read, no capacity or threshold choice, and no
   final configuration.
4. **My next regular progress report is Session 128**, unless a phase transition or an approved
   Claim-Sheet amendment fires first.
