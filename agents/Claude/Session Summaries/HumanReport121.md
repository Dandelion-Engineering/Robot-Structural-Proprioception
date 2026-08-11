# Claude — Human Report, Session 121

**Date and time:** 2026-08-11 12:16 PDT

**Phase:** Phase 2 — Execution (with Phase-3 Reproducibility Packet documentation work)

**Progress-report session:** No. My last regular was Session 120 (covering S113–S120). My next regular is **Session 128**, unless a phase transition or an approved written Claim-Sheet amendment fires one sooner. Neither happened this session.

---

## Summary

### What this session was for

Last session I wrote the two runbook steps that document the rung-2 escalation — the run that put a second architecture on the project's capacity ladder, and the read that interpreted it against rules frozen before any of it existed — into the Reproducibility Packet's README, and handed that state to Codex for review. Codex reviewed it, accepted three judgment calls I had flagged, made one factual repair, and handed it back approved at its own edited state. Because I own that artifact, the review cycle does not close on Codex's approval: I owe a genuine re-review of both the feedback and the edit, and then either an approval of the same bytes or a corrected state handed back.

That re-review is what this session did. It produced an approval of Codex's finding, and **three more defects that neither of us had caught — two of them mine from last session, and one inherited from text both agents approved several sessions ago.** All three are repaired, the state is handed back, and the loop is now in its second round.

### Codex's finding, checked rather than accepted on trust

Codex found that a sentence I wrote in Step 31 was false. I had written that the six rung-2 arms which did not sit at the majority-class baseline "score a non-zero `actuator` F1 and nothing else." I re-derived the whole per-class census from the analysis artifact's own records, importing nothing from the analyzer that produced it:

```text
non-zero per-class F1 across the ten rung-2 arms
  healthy    0 / 10
  actuator   6 / 10
  sensor    10 / 10        <- this is what my sentence denied
  structure  0 / 10
arms sitting exactly at the majority-class baseline   4 / 10
```

Codex is right and my sentence was wrong. I also re-derived the baseline itself from the class census rather than quoting it — answering `sensor` to all 152 development examples on an 8 / 32 / 96 / 16 census gives accuracy 0.631578947368421, a sensor F1 of 0.774193548387097 and a macro-F1 of 0.193548387096774, which is exactly what those four arms carry. **Codex's two edited lines survive in my returned state word for word.** Its three judgment rulings — leave the rung-difference figures named but unprinted, keep the 55→67 checkpoint correction, keep the new boundary paragraph — I accepted without contest.

### The three defects I then found

**BN — the sentence immediately after the one Codex fixed was also false, and also mine.** It said the ten rung-1 anchors "each have four non-zero per-class values." Two of them — C1 seeds 1 and 3 — score zero on `healthy`. Eight have four non-zero values; two have three.

What makes this worth more than a correction is that the contrast the paragraph exists to draw is *stronger* than the sentence I wrote, not weaker. The point of naming the anchors is to show that the rung-2 arms' zeros are not just what this data produces. On `structure`, that contrast is unanimous: **every one of the ten anchors is non-zero, and every one of the ten rung-2 arms is exactly zero.** I rewrote the sentence to lead with the class where the contrast holds without exception and to name the two exceptions on the class where it does not. Precision made the paragraph say more, which is the usual way with this kind of repair.

**BO — a counted falsehood in text both agents had already approved.** Step 30 said the run's equivalence gate "authenticates the ten original `results/dev_fit/` checkpoint files against the tracked ledger." It authenticates two. I traced it at source rather than reasoning about it: the list of equivalence arms is defined exactly once in the project, as `(("C1", 0), ("S", 4))`, and the rung-2 executable imports that same list rather than defining its own; each executable passes the checkpoint directory to exactly one function, the equivalence gate; and that gate's loop runs over those two arms, reading each file's bytes and comparing their SHA-256 against the ledger's digest. The other eight anchors never have their weight files opened at all — they travel document-to-document, by digest and recorded score.

The practical claim in that paragraph survives (a fresh clone lacks the two files, so the command still fails closed), but the count was wrong — and it contradicted a sentence three paragraphs above it in my own step, which correctly says the run "refits the two approved rung-1 checkpoints."

**The same false count is in Step 28**, in the parallel sentence about the Stage-1 executable — and it is the same two arms, because both executables share the one definition. Step 30's paragraph opens by saying the same boundary as Step 28 applies for the same reason, so repairing one and not the other would have left the runbook internally inconsistent as well as wrong. I repaired both, and flagged the Step-28 edit as a deviation from the scope Codex set for this round — the same way I flagged the 55→67 correction last session, on the ground Codex accepted then: a counted, checkable statement that is false should not ship. If Codex reads the scope differently, it can strike that hunk and I will not argue the point.

**BP — a runtime figure a reader cannot check against the packet.** Step 30 said the run took 1,274.6 seconds. That is Codex's external wall-clock measurement and it is true, but the run's own record says `elapsed_s = 1272.094`. A reader who opens the artifact the same paragraph points them at finds a different number with nothing reconciling the two. The gap is start-up: the executable starts its clock inside execute mode, after the interpreter and the (heavy) machine-learning library import. I named both figures and said which is which. This is the softest of the three — the original was not false — and I said so in the handoff.

### What I measured and deliberately did not change

The same paragraph says rung 2 costs "roughly 12× per optimizer step" compared to rung 1. That figure comes from a micro-benchmark recorded in the frozen design, which caps itself in writing — "No figure here may be quoted as a measurement of anything but the order of magnitude" — and which excludes the data loading a real fit does. The README hedges it with "roughly" and links the design in the same step, so it is not false. But its source is not named beside it, and after my BP edit two genuinely measured wall-clock numbers now sit two sentences away, which invites a reader to think this run measured it. **I did not edit it, and I handed the call to Codex** rather than deciding unilaterally in an artifact it is reviewing. This is the project's "record rather than raise" pattern, and it keeps the scope of a review round honest.

## Challenges, and how they were handled

**Three counted falsehoods in one neighbourhood, two of them mine, is a pattern rather than an accident.** All three are the same shape: a sentence written from a correct mental model of the *mechanism* that then states a *count* the mechanism does not support. I knew the equivalence gate refits two arms — I wrote that sentence three paragraphs earlier — and still wrote "the ten" downstream, because "the ten approved anchors" is the phrase this project says most often. The lesson I am carrying forward is narrow enough to be usable: **when prose names a count, the count is a claim and must be measured at its source, even when the surrounding sentence is one you are sure of.** Being sure of the mechanism is exactly what suppresses the check.

**A finding-letter collision, caught late.** Codex's session report labels its finding **BM**, though its chat turn did not use a letter. I had already written my three findings as BM, BN and BO and appended the turn to the transcript. Two different findings sharing a letter would be a real defect in a ledger the project uses to reference findings across sessions. Because the turn was not yet committed and not yet handed over, I corrected it the way this project's own rule allows: I re-asserted the complete prior transcript byte-for-byte as a prefix and rewrote **my own payload only**, renumbering mine to BN, BO and BP and adding a line saying why. No prior turn was touched and nothing was deleted; the append-only rule protects the history, and it is not a licence to publish something I know is wrong. Had this been caught after a commit or a handover, the answer would have been a new appended correction instead.

**A near-miss on the first append.** My first attempt to renumber with a chained text substitution created an intermediate token that the second substitution then matched — a classic ordering bug that would have published a placeholder into the transcript. It was caught because I printed the resulting set of finding letters instead of assuming the replacement had worked. Small, but it is the same discipline that has caught larger things in this project: check the output of your own instrument before publishing it.

## Decisions made

1. **Accepted Codex's diagnosis and implementation in full**, after reproducing the underlying census independently rather than reading its statement and agreeing.
2. **Repaired Step 28 as well as Step 30**, and flagged it as an out-of-scope deviation with the scope call handed to Codex — rather than either leaving a falsehood in a shipping artifact or quietly widening the round.
3. **Did not edit the 12× figure**, and handed the judgment over instead.
4. **Did not append to the public Live-Run README.** The playbook's three triggers are a finished artifact, a phase close, or something genuinely noteworthy. The noteworthy thing — section 5.4 being jointly applied — is precisely what Codex asked be published together with a jointly approved runbook state, and that runbook is now in a second review round *because of defects I found in it*. Publishing now would publish a status the project has not finished checking. This stays a deferral with a named trigger, and the trigger is now Codex's approval of blob `f5e677c8` rather than `9a3a878c`.
5. **Renumbered my own findings** rather than letting a letter collision into the ledger.

## Verification performed

Twenty named checks, each against a primary object and none importing the analyzer whose output was under review: the analysis artifact's digest, byte count and line-ending profile (unchanged); its eleven top-level fields; the ten arms' complete per-class vectors; the four baseline arms by exact equality; the baseline re-derived from the census arithmetic; the ten anchors' zero cells; the paired sign count re-derived from the five per-seed differences (2 negative, 1 zero, 2 positive — unchanged); the rung-2 network constructed and counted at 219,018 parameters with a stem receptive field of 31 and deliberately no whole-network receptive-field attribute; the rung-1 network at 39,594 and 1,023, giving the ratio 5.5316 behind the stated "5.5×"; the frozen design's canonical digest and size; the plan, run and equivalence artifacts' digests and byte counts; the run record's exit code, five budget counters and row disclosure (304 of 944 manifest rows, 152 per suite); the equivalence gate's pass status and its two arms; the run's own elapsed time; the equivalence-arm definition and its single import; each executable's one checkpoint-directory call site; the analyzer's nine arguments, all required with no defaults; the scope of Codex's own commit (+3/−3 on the README and nothing else in the packet); and the full packet test suite at **2,108 passed in 134.19 s**.

## Resource accounting

```text
fits                              0
checkpoints written               0
rollouts                          0
generation runs                   0
simulator invocations             0
production analyzer / C7 runs     0
plan-mode invocations             0
pilot / validation / test reads   0
```

The checkpoint count on disk is unchanged at 67. Nothing this session selected a rung, a capacity or a threshold, attached a cause to the zero-class observation, or added a sentence to what either section 5.4 licenses.

## Files created or updated

- `Reproducibility Packet/README.md` — three repairs (Steps 28, 30 and 31) on top of Codex's edit; returned at Git blob `f5e677c8afdbdfa5c97f3cc53a4a2b92d0a13b9d`, +21/−14 against Codex's reviewer blob, with exactly fourteen deleted lines and no others.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — my Session-121 owner re-review and second-round handoff appended, +156/−0, one tail hunk, no line endings changed.
- `agents/Claude/README.md` — the packet-runbook bullet's current-state lead rewritten for round two; the Live-Run README bullet's lead updated; and the same false anchor claim corrected where it had propagated into my own workspace index.
- `agents/Claude/Session Summaries/HumanReport121.md` — this report.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 122.

**Not modified:** the public root README; the frozen rung-2 design; any architecture, executable or analyzer code or tests; the plan, run, equivalence or analysis artifacts; any checkpoint; the delivered data; any configuration file; and every concluded review loop.

## Next steps

1. **Codex reviews packet README blob `f5e677c8`** and either approves those exact bytes or edits and hands back. Three things need an answer rather than an assumption: whether the Step-28 repair stays (it is outside the round's scope), whether the runtime clarification stays, and whether the 12× figure should have its provenance named inline.
2. **When that loop closes, the public Live-Run README entry is the next act** — one lean entry, and it must carry the zero-class observation beside the two licensed sentences so a reader cannot mistake the passed objective check for classification learning.
3. **The Technical Report still owes two things:** the same adjacency for the zero-class observation, and the story of the capacity-read defect that an earlier public log entry does not tell.
4. **Nothing on the rung-2 lane is scientifically open.** Any attempt to explain the zero-class result — the class imbalance is the obvious suspect and is deliberately not in the record as a conclusion, because nothing in this run tested it — begins as a new reviewed design, not as a continuation.
5. `director_requests.md` entry 1 (Claim Sheet review) remains open and non-blocking.

— Claude
