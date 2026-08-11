# Human Report — Claude, Session 117

**Date and time (measured at write):** 2026-08-11 04:20 PDT
**Phase:** 2 (Execution) — open
**Spend this session:** 0 fits · 0 checkpoints · 0 rollouts · 0 generation runs · 0 pilot/validation/test reads · 0 C7 invocations

---

## What this session was

Codex's Session 116 closed step 4: it independently audited the zero-fit plan I wrote last
session with an instrument of its own, found nothing, and approved the exact bytes. It also
accepted my reviewer edit to the public log unchanged, then appended a new public entry of
its own and handed that back to me. And it deliberately did **not** issue a step-5
execution-authorization half, which leaves that half to be earned rather than assumed.

So this session had two jobs. Review the new public entry. Then do the work that has to
happen *before* anyone is allowed to spend twelve training runs, and — if it all holds —
issue my half of that authorization.

Both got done. The public entry took one `+1/-1` edit on a sentence that mis-described what
the review actually was. The pre-authorization ran 44 checks against the real state and
stopped one call short of the first fit. And I went looking for the weakest link in the
whole run and closed it, at zero cost, in a way I think is genuinely better than the
measurement it replaces.

---

## 1. The public entry — one edit

Codex's new running-log entry closed with:

> Independent review reproduced all 107 plan checks and the executable's authorization gate.

Two things wrong, and the second is the one that matters.

**"Reproduced" names the wrong act.** Codex's audit did not re-run my checks. It rebuilt the
expected plan from scratch, without importing the program that wrote the plan, and compared.
That is an *independent instrument*, and its independence is the entire reason it is worth
reporting. "Reproduced" quietly gives that away — it makes the review sound like a replay.

**"All 107" presents one instrument's count as the artifact's total.** There were two audits,
written separately, grouped differently: mine at 132 checks, Codex's at 107. A stranger
reads a definite "all 107" as *the* number of checks that exist on this artifact. I checked
the log's own precedent before editing, because precedent could have cut the other way — and
it cuts both ways honestly. The 2026-08-09 entry names only the reviewer's 73 checks, but
that is because there was only one audit to name. The 2026-08-10 entry describes both sides,
because both sides did something. This is the second case.

The replacement also puts back the part that makes a check count mean anything, which the
original dropped:

> Two separately written audits checked it — 132 by the author, 107 by the reviewer, neither
> borrowing any code from the program that wrote the plan — and both passed, as did a direct
> drive of that program's own authorization gate. The author's audit was calibrated first:
> the plan was damaged in 23 different ways, and each damage had to be caught by the check
> named for it.

One line changed, no line added or removed.

### A measurement correction that lands on me as much as on Codex

Both of us have been publishing this file's *raw working-tree* digest and CR count as if they
identified the artifact. They do not. `core.autocrlf=true` and the root README is pinned in
neither `.gitattributes`, so the file's line endings in a working tree are whatever the last
write left there — and a plain `git checkout -- README.md` rewrites them.

I did exactly that this session, by accident, and then measured it: the file went from
145,850 bytes / 199 carriage returns to 145,859 / 208, **with the tracked content completely
unchanged** — same git blob, same commit, nothing edited. I then checked the tracked side
across four commits and every one has **zero** carriage returns.

Which means a standing note I have been carrying in my own handoff for three sessions —
"the running-log entries end in bare LF while the document is CRLF" — describes a working-tree
artifact and has never been a property of the file as stored. For this file, quote the blob
and the cleaned digest. I have switched to that and said so in the chat.

---

## 2. Step 5's pre-authorization — 44 checks, stopping one call short of the first fit

The rule this follows is one the project bought the hard way: run every check that sits
*below* an expensive irreversible step *before* authorizing it, not in exchange for it, and
name the residual no measurement can close. A check that runs after the spend cannot save the
spend. Section 3 below adds 11 more checks and 14 control cases — 69 measurements in all.

**The authorization gate, driven against the real state (12 checks).** The plan's digest
matches; the base directory I name below is accepted and the protected checkpoint tree is
refused by name; the gate accepts the exact bytes and returns a plan whose run label,
training protocol and design digest all match what the program resolves today. Then the
neighbours — because a gate that accepts everything passes an exact-bytes check identically.
One flipped hex digit: refused. The same bytes sitting at a different path: **accepted**,
which is the document-gate property the code claims. And two semantic mutants — the fit
budget inflated from 12 to 13, and the run label changed — each **authorized under its own
digest**, so the digest comparison could not do the work and only the content checks could
refuse. Both refused.

**The destination (7 checks).** The execution directory does not exist; its parent holds only
the plan folder; the plan sits in a *sibling* of the run root rather than inside it. The
atomic claim itself I drove at a scratch directory only — pointing it at the real base would
have consumed the very directory this authorization exists to open. First claim creates,
second claim refuses.

**Everything else below the spend, against the real state (16 checks).** Parameter count,
arm counts, budget, the program's own fit ceiling; the three approval checks against the real
ledger and analysis; both pinned digests still matching those two files *today*; and all ten
prior checkpoints present on disk with digests equal to the plan's, ten distinct, each
compatibility re-fit pointing at the on-disk digest of its own anchor.

**Code identity (5 checks).** Twelve entries, equal to the plan's, and **every digest
recomputed from the file** rather than read out of the map.

**The last thing before the first fit (4 checks).** Loading the development split through the
approved call: 2.1 seconds, 152 examples per suite, 304 of 944 manifest rows selected,
manifest and assignment digests equal to the plan's pins. This is the check that would
otherwise fail *after* the run directory is claimed — burning the label for nothing. Then I
stopped. No fitting function was called.

---

## 3. The weak link, and closing it for free

This is the part of the session I would defend hardest.

The run's first gate refits two small networks and demands they come out **bit-identical** to
checkpoints produced back in Session 84 by a different program. If they do not match, the run
stops. That gate exists so a later comparison between the small and large networks cannot be
confounded by a difference between two training loops.

The claim that gate rests on factors into two links:

- **Link 1** — the Stage-1 program's fit at 32 channels equals the Session-84 checkpoints.
  This was **measured on real data**, in Codex's Session 100, on the *same two arms*.
- **Link 2** — the new program's fit equals the Stage-1 program's fit. I measured this in
  Session 115, but **only on synthetic examples**.

Link 2 was the soft one, and I do not think it was soft in an obvious way. Bit-identity
measured on one input set does not automatically transfer to another: a difference reachable
only at a different row count, a different final-batch remainder, or a different tensor shape
would never have been exercised by my synthetic fixtures, and the real arms carry 152 rows.
Measuring it properly on real data costs a training run, and no training run is authorized.

So I closed it a different way, at zero cost:

- **The two loop bodies are identical as code**, after normalizing away the two differences
  that are declared by design (which network constructor is called, and one extra guard the
  Stage-1 version needs). Same syntax tree, same digest.
- **Every named thing the shared body uses is literally the same object** in all three
  modules — the batching function, the loss, the precision context, the seed guard, the error
  class, and the numerical libraries themselves.
- **The two network constructors produce bit-identical starting weights** at both of the
  seeds the gate uses: 66 tensors, 39,594 numbers, every one equal.

Same code, same objects, same starting point — so link 2 holds on *any* input, which is
strictly stronger than a measurement on one input set.

**And then the control, because that is the whole lesson of this project.** A comparison that
passes proves nothing until you know it can fail — and specifically, until you know the
normalization step cannot also erase a difference nobody declared. So I damaged the Stage-1
loop twelve different ways, one at a time: the gradient-reset flag, a different optimizer,
the shuffle seed, training mode dropped, evaluation mode dropped, the batch stride, the
epoch average swapped for a median, the seed argument, the non-finite-loss guard, the
learning-rate wiring, the backward pass deleted, the precision context deleted. **All twelve
caught.** Two harmless controls — identical source, and a comment added — both correctly
unaffected.

I also measured where the normalization *is* blind, rather than asserting it is not: inside
the constructor call and inside the one Stage-1-only guard, which are exactly the two
constructs it exists to erase. Both are covered by other instruments, and I named which ones
rather than leaving the gap implicit.

---

## 4. Suites, and one hazard measured

```text
focused rung-2 executable tests   142 passed,   3.54 s
full packet suite               2,005 passed, 126.23 s
```

Codex flagged in Session 115 that a concluded Stage-1 test file still points the Stage-1
program at the real protected checkpoint directory, with cleanup afterwards — safe only while
a guard is present, which is the one condition a mutation sweep removes. Neither of us has
reopened that jointly approved file, and neither should without redirecting it first. What I
could do cheaply was measure the exposure: I re-digested all ten protected checkpoints
**after** running the full suite, and all ten are unchanged. That is not a licence to leave
it — it is evidence that this run's inputs survived today.

---

## 5. My half of the execution authorization

Issued as its own turn, not folded into the review — bundling an authorization into a review
turns a review into a spend.

It names the exact command and every argument (each resolved through the program's own
argument parser and each verified to exist), the plan's digest, the run label, the **base
directory** explicitly — because the destination guard only refuses one specific tree, so the
authorization is worth exactly the base it names — the four relevant file identities, the
budget of 12 training runs / 12 checkpoints / 0 physical rollouts / 0 data generation / 0
reserved-role reads, the projected ~19 minutes and ~10 MB, and the library versions, because
the Session-84 record pins none and the gate is being asked to reproduce that session's
output.

It also states what it does **not** authorize: a retry, a different base, a copied workspace,
the step-6 analyzer, any reserved-role read, any capacity choice or threshold, and any
application of the pre-registered interpretation — which is step 7 and joint.

Five residuals are named, none of them a reason to withhold. The two structural ones are
unchanged from Stage 1 (a replay at a different base, and a concurrent writer, neither of
which any local mechanism can see). The interesting one is honest about the division of
labour: **link 1 above is Codex's measurement, not mine.** If it has moved since Session 100,
the gate catches it after two small fits — about seventeen seconds — and before any large one.
That is exactly where the design put it, and saying so is more useful than pretending I
re-measured it.

**The state is one half of two. Nothing is authorized until Codex issues the second.**

---

## Decisions I made this session

1. **Edit the public entry rather than only flagging it.** The reviewer may edit directly,
   and a one-sentence imprecision in a public log is cheaper to fix than to discuss.
2. **Report both audit counts rather than replacing 107 with 132.** Naming only mine would
   have repeated the same error facing the other way.
3. **Close link 2 statically instead of asking for a fit to measure it.** A fit would have
   been a twelfth of the run's budget spent before the run was authorized, and the static
   argument is stronger than the measurement it replaces because it does not depend on which
   inputs were used.
4. **Drive the atomic directory claim at a scratch base only.** Driving it at the real base
   would have consumed the run root and forced a new label — the guard would have worked
   perfectly and cost us the run.
5. **Load the real development split before authorizing.** It is the last failure that can
   happen after the run directory is claimed, so it is the one most worth moving earlier.
6. **No new public log entry of my own.** I re-read the playbook, as in every session where
   the answer came out no. Issuing an authorization half is not a finished artifact, not a
   phase close, and not a noteworthy event for a stranger — the finished artifact was the
   plan, and Codex already logged it.
7. **No monitoring-chat entry.** The check happened and is recorded below; an entry needs a
   fault or a proposal, and there was neither.

---

## 6. A defect I found in my own continuity file

While rewriting my session-to-session handoff I grepped the finished rewrite for phrases that
assert a position — a habit this project bought the hard way — and found a `← WE ARE HERE`
marker sitting inside the historical narrative of an *earlier* lane, at a step the project
passed in Session 103. It had been carried through **thirteen** of my rewrites after the
position moved, because it reads as punctuation rather than as a claim, so no re-read of the
sentence ever challenged it.

Repaired, and the lesson recorded: a position marker is a status clause and rots like one.
Keep exactly one authority on where the project is — for me that is the block at the top of
the file — and grep the rewrite for every phrase that asserts a position rather than trusting
a read-through. Two other stale status clauses in the same file were tightened the same way.

Three standing lessons were added to my permanent-instruments file: this one, the digest
lesson from section 1 (a digest is only an identity if the thing it digests is the thing that
travels), and the one from section 3 (when a measurement would cost a gated resource, ask
whether the property can be established over the code rather than over one execution of it).

---

## Files created or updated

| Path | What changed |
|---|---|
| `README.md` | reviewer edit, `+1/-1`, one sentence in the 2026-08-11 entry; blob `485d83ce` |
| `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` | my Session-117 turn appended, `+264/-0`, single tail hunk |
| `agents/Claude/Session Summaries/HumanReport117.md` | this report |
| `agents/Claude/Summary of Only Necessary Context.md` | rewritten; three stale status clauses repaired |
| `agents/Claude/Permanent Instruments.md` | three standing lessons appended (180–182) |
| `agents/Claude/README.md` | session pointer updated |

Nothing was written into the Reproducibility Packet. The execution directory
`Reproducibility Packet/results/rung2_escalation/rung2-run-1/` **still does not exist**, which
is the condition the run's first guard requires.

Probe scripts (scratch, not committed): the 44-check pre-authorization probe, the 11-check
static link-2 probe, and its 12-mutation control.

---

## Transcript-order check

Verified at the git level rather than assumed. Codex's Session-116 commit `d28ad3e` touches
the shared transcript as a **single tail hunk**, `@@ -32129,0 +32130,105 @@`, additions only,
and does not touch the monitoring file at all; its public-log change is a single `+1/-0`
insertion. My own append is likewise a single tail hunk, `+264/-0`, with the prefix verified
byte-identical before writing. **No violation, and no open proposal to close.**

The cross-agent digest convention operated for the **fifth** time: the pre-append digest
Codex published in its Session 116 (`73dda967…`) equals the post-write digest I published in
my own Session 116, byte for byte.

---

## What is open, and what happens next

**One review loop is open, and it is on Codex:** the public README at blob `485d83ce` after my
`+1/-1` edit. If Codex edits it, the owner re-review is Codex's, not mine — it owns that entry.

**One authorization half exists of the two step 5 needs, and it is mine.** The next allowed
act in the project is Codex issuing the second half and running the command exactly as
written. Nothing else — not the analyzer, not the interpretation, not a threshold, not a
capacity choice — is authorized by anything that happened today.

If Codex reads the pre-authorization and disagrees with any part of it, the right move is to
say so before running rather than after; an authorization is worth exactly what the gate
reading it is worth, and I would rather rewrite my half than have it treated as scenery.
