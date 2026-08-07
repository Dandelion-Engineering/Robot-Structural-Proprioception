# Claude — Human Report, Session 90

**Date and time:** 2026-08-07 08:17 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session: 0.** Project lifetime total remains **278**.

**Fits: 0. Checkpoints: 0. Data generated: 0. Pilot / validation / test reads: 0.**

**Progress-report session:** no. My next regular is **Session 96**; no phase transition and no
approved Claim-Sheet amendment fired this session.

---

## What this session was

An owner re-review. Codex had edited my capacity-escalation design in its Session 89, made two
corrections, and approved its own state. My job was to genuinely re-open that document, decide
whether its corrections were right, and either approve those exact bytes or return an edited
state with reasons.

I kept both of Codex's corrections without contest, and found one further defect below them.
The document went back to Codex; the review round is still open.

One loop did close: Codex approved my Session-88 progress report at the exact bytes I had
already approved, so both approvals name the same state and that report is finished.

---

## What Codex had corrected, and why I accepted both

**Its first correction was that I had written an impossible instruction.** My Session-89 design
said that when the new capacity-sweep module copies the trainer's fitting loop, "everything
else in that body must be imported, not retyped," and gave a table of what to import. Codex
pointed out that the table was complete only for the project's *own* functions. The loop also
calls PyTorch and NumPy directly, and its control flow — the nested loops over epochs and
batches — is itself copied. None of that can be imported, because there is no project helper
wrapping it.

I re-read the loop line by line rather than taking this on trust. Codex is right, and the
omission was mine: it had also spotted that my table left out the network class itself. Its
rewritten version names the copied third-party expressions honestly and leans on the
equivalence gate (described below) to catch any divergence across the whole copied region
rather than just the tabulated calls.

**Its second correction was that I had overclaimed what a small field could enforce.** Last
session I added a `run_label` to the execution plan and argued it made an authorization
single-use — that once the agents jointly authorize one execution, the same authorization
could not silently license a second one. Codex's objection: the authorization is a digest of a
document, and the same document can simply be submitted twice.

The check that settled it for me was not the argument but the code the design cites as its
precedent. The existing trainer takes its output directory as a required command-line
argument, and its "don't overwrite an earlier attempt" guard checks *that supplied directory*.
So a second run pointed at a fresh directory passes every gate. Codex is right and I withdrew
the claim.

---

## The defect I found underneath that

Accepting Codex's second correction left something unresolved, and it took the form the last
several rounds of this project have taken: the problem was one layer below the repair.

The design specifies a `run_label` and a project-relative naming scheme for outputs, and then
never says how either relates to the directory the program actually writes into. Three separate
rules depend on that unstated answer — "a non-empty output root is refused," "a retry uses a
fresh output root," and, written by Codex in this very session, the claim that repeated use of
the same label "is recorded rather than silently presented as a new authorization."

That last one is the one that fails. If the output directory is whatever the operator types,
then two executions carrying the same label write their records into two unrelated folders and
nothing ever brings them together. "Recorded" and "auditable" were doing work that no actual
mechanism performs — they described a hope about a diligent reader, not a guard.

The repair costs nothing. The program takes a *base* directory on the command line, as the
trainer does, and writes into a subdirectory named after the label from the plan. The plan
still contains no machine-specific path, so the property Codex correctly protected last session
— that the plan file is byte-identical no matter which machine writes it — is untouched.

What that buys, stated at the width it actually earns:

- A repeat run under the same base collides with the preserved directory of the first and is
  refused by the guard that already exists. The audit claim now names a mechanism.
- "Use a fresh output root" stops being a second thing the operator has to remember and follows
  automatically from using a new label. Two obligations become one.
- The remaining gap narrows from *any fresh directory* to *a different base directory, or a
  copy of the whole workspace*. That gap is real and no local mechanism closes it. But it is
  now a deliberate act that leaves the first run's evidence sitting there unexplained, rather
  than something someone does by accident, and the document says so in those words.

I told Codex plainly what happens if it disagrees: if the output directory should stay a free
operator choice, then the binding comes out — and the audit sentence has to come out with it,
because that sentence is the only thing the binding exists to support.

---

## Two checks worth recording because of what they were checking

**I asked what depended on a fact Codex deleted.** Its edit removed a small annotation from my
table recording that the training loop's row-shuffling does not depend on network width — a
fact that a different section relies on. That question ("before removing something from a
contract, ask what else was depending on it existing") is the lesson I wrote down for myself
last session after two individually correct repairs opened a hole between them. This time I
applied it to someone else's edit. It came back clean: the fact is stated more fully elsewhere,
with its own measurement. Nothing was lost. I recorded the clean result so it is not re-checked
later.

**I verified the equivalence gate's own precondition instead of assuming it.** The design's main
safety mechanism against a mis-copied training loop is to re-fit two of the ten already-approved
configurations through the *new* code and require the resulting weights to match the approved
ones bit for bit. That check is only meaningful if the new, width-parameterized way of building
the network reproduces the old one exactly when set to the old width. I measured it rather than
assuming: identical weights, identical parameter counts, at both of the configurations the gate
uses. Had that not held, the gate would have failed for a reason having nothing to do with the
copied loop, and we would have spent a review round discovering why.

---

## Honest accounting

Nothing was executed this session. No model was trained, no data generated, no simulation run,
and no part of the reserved pilot, validation or test data was touched. The project's lifetime
simulation cost stays at 278 rollouts. The full test suite passes at 1,551 tests — the same
count as the previous three sessions, because no program file has been changed by either agent
in any of them.

This is the fourth consecutive session on this one design document. That is worth saying
plainly rather than burying: two agents have now spent four sessions arguing about a document
that authorizes nothing and produces no science. The counterweight is that every round has
found something real, each one structurally below the last, and the thing being designed is a
forty-two-fit spend that cannot be un-spent. But if the next round finds only wording, that is
the signal to close it rather than to hunt for one more — a heuristic this project earned the
hard way on an earlier eight-round loop, and one I want the next session to actually apply.

The public project README was left untouched. The playbook says entries go in when an artifact
is finished, a phase closes, or something genuinely noteworthy happens for an outside reader.
An open review round is none of those. It goes in the log when the design loop closes — and
whoever writes that entry owes the reader the shape of what these rounds have been finding.

---

## Files created or updated

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` — owner re-review; Codex's two
  corrections kept unchanged, one further defect repaired (the output-root binding in the
  invariant list and in three places in §7), review log extended. Returned at blob
  `b2f650e19a1187360621c60be7f91d544ad9ea40`, canonical SHA-256
  `d7133099cc537d90d76977c581369767cacacc241e2116ff5d18f57d429227ee`, 62,908 bytes / 964 lines,
  LF, no BOM. Delta against Codex's state: +89 / −25.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — my Session-90 turn appended (+131 / −0, single tail hunk, prefix verified byte-identical).
- `agents/Claude/Session Summaries/HumanReport90.md` — this report.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.
- `agents/Claude/README.md` — reviewed and updated.

Not changed, deliberately: the root `README.md` (no trigger), the transcript-order monitoring
chat (no recurrence to flag — verified at the Git level, not assumed), and every executable
file in the packet.

---

## Next steps

1. **Codex re-opens the design at `b2f650e...`** and either approves those exact bytes or
   returns another edited state. If it approves unchanged, v0.1 freezes.
2. **A frozen design authorizes exactly one thing: writing the executable and its tests.** Not
   running it. The plan artifact is a separate review after that, and the execution itself is a
   fourth and separate joint authorization. Four gates, and the design says so in its own text
   so that no future session can compress them.
3. **Nothing else is blocked on the director.** The one open request — the Claim Sheet review
   logged at Phase 1 — remains non-blocking, and the agents have kept working past it as
   designed.
