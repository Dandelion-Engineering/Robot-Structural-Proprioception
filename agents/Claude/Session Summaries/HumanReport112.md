# Claude — Human Report, Session 112

**Date and time:** 2026-08-10 18:14 PDT
**Phase:** Phase 2 — Execution
**Progress-report session:** **Yes.** Session 112 is a regular per-agent progress-report session. The report was written *in addition* to normal session work and is at `agents/Claude/Progress Reports/Progress Report Session 112.md`, covering my Sessions 105–112. My next regular is Session 120.

---

## Summary

Three pieces of work: the owner re-review that the review cycle put on me, the regular progress report, and the continuity-file split Codex approved in its Session 111.

**The owner re-review is the session's substance.** In my Session 111 I returned a zero-resource design for Slot 9's rung 2 — one named recurrent-plus-attention estimator to climb the model-capacity ladder. Codex reviewed it in its Session 111, found seven design-state defects, repaired them directly in the still-unapproved draft, and explicitly approved its own reviewer state at Git blob `1f65ab5f…`. Because the reviewer changed the bytes, the loop stayed open and the next act was mine: genuinely re-open that exact state, review both the feedback and the edits, and either explicitly approve or edit and hand back.

I re-opened it, reproduced its identity before reading a word of it, **accepted all seven repairs**, and found **two more defects, which I repaired**. So the loop is still open and it is now on Codex again, at a new state I explicitly approve: blob `404c9f1f…`.

**Nothing was spent.** No fit, no checkpoint, no generation, no rollout, no plan action, no analyzer invocation, no pilot/validation/test read. The session touched no real project data at all — no manifest, no `.npz`, no label payload, and not one byte of any `.pt` checkpoint. It read exactly two tracked JSON artifacts and wrote to neither. Rollouts remain 278; the fit counter remains 13.

---

## What I accepted, and the two places I did more than agree

Codex's seven repairs were: correcting which Claim Sheet slot is the authority for this action; making the attention parameterization exact; separating size-band admissibility from architecture identity; narrowing an over-claiming label; replacing an overlapping interpretation table with an ordered partition; repairing an impossible refusal-persistence promise; and binding the new checkpoints to their own producer identity.

All seven are correct and I did not contest any of them. On two, I went looking for an **independent second mechanism**, because a finding you can only restate is a finding you have conceded rather than accepted.

**On repair 2 — the attention specification.** Codex found that an implementer using PyTorch's stock `nn.MultiheadAttention` would build 228,330 parameters against the declared 219,018, because the stock module silently adds an output projection. I reproduced both counts by construction, and the silent addition is exactly one `H → H` projection, 9,312 parameters.

The second mechanism changes which invariant turns out to be load-bearing: **228,330 sits comfortably inside the declared parameter band of `[100,001 – 1,000,000]`.** So the section the design spends a page on — enforcing the rung's band with no override, no flag, no escape hatch — would have accepted the wrong architecture without complaint. The only thing that refuses it is a single clause requiring the exact count. Which means the returned document was not merely *under-specified*: it was **internally unsatisfiable**, because a faithful implementer would have had to either change the count or weaken the invariant, and the second of those is the direction things drift.

**On repair 4 — the over-claiming label.** Codex narrowed an arm's status from `LEARNED` to `OBJECTIVE_REDUCED`, because the training objective contains a severity term whose scale can pull the total down without classification improving. The second mechanism is in my own text, four lines below the label I chose: **rung 1 reached the lower synthetic loss of the two.** I put that number in the document *because* it was the inconvenient direction — and then labelled the gate with a word that would have licensed reading it as rung 1 having learned more. The counterexample and the overclaiming label were four lines apart in a document I wrote in one sitting.

---

## The two findings I raised, and why each was worth a repair rather than a note

### BI — a specification true of the right implementation and also of the wrong one

The design said parameter creation happens "inside `fork_rng(...)` after `manual_seed(seed)`" — and never said the *seeding* happens inside the fork. Rung 1 does it inside. I drove both orders on synthetic tensors:

```text
seed INSIDE the fork    caller's global CPU RNG state after construction   UNCHANGED
seed BEFORE the fork    caller's global CPU RNG state after construction   MUTATED
both orders                                                    219,018 parameters
```

That third line is what made it a repair. **The parameter-count invariant — the one a builder checks first — cannot tell the two orders apart.** The invariant that catches it is one clause at the end of a thirteen-item list. So the document's most-read guard is blind to it and its least-read guard is the whole defence. This is Codex's own repair-2 defect class (a construction detail left to the implementer's reading, where one reading silently violates a declared property) arriving *in the sentence repair 2 added*. The order is now part of the specification, with the two source lines cited and with the document itself saying which invariant does and does not catch it.

### BJ — the document forbade the field it requires

§5.3 reads *"No trend, slope or direction across rungs."* §5.2 requires the analyzer to persist a signed rung-2-minus-rung-1 difference per suite per seed, **plus its per-suite mean**. Under the plainest reading of that prohibition, the document instructs a builder both to persist a field and not to. A contract a builder resolves by guessing is a contract with a hole in it.

The resolution was already ours and neither of us invoked it: Stage 1 settled this exact tension — its five per-point means are persisted and quotable, and a line through them is forbidden. The prohibition is on *asserting* a direction, not on *persisting* the primitive. That distinction is now explicit, along with the fact that no interpretation row licenses any sentence about that field at all.

**The reusable instrument:** read an emit-prohibition against the persist-requirements in the section above it. Both were written to be strict, and they were written against each other.

---

## What I drove

A 78-check probe that builds the architecture **from the document's prose alone**. It imports no rung-2 code, because none exists — only the two approved stem components the design says rung 2 must import, read-only.

```text
A   the approved constants the design derives from    RUNG1_MAX measured at 100,000, so the
                                                      derived rung-2 floor of 100,001 is exact;
                                                      rung 1 re-measured at 39,594 / RF 1,023
B   the selected configuration, CONSTRUCTED           219,018
C   the seven-term component ledger, term by term     all seven exact, sum 219,018
D   all seven grid rows, TWICE each — analytically    7/7 counts, 7/7 stem receptive fields,
    and by construction                               7/7 band verdicts
E   the nn.MultiheadAttention counterfactual          37,248 vs 27,936 → 228,330
F   the module-type census, both rungs                9/8/1/5 and 19/4/10, all exact
G   suite-agnosticism under a masked gauge block      219,018 → 219,018, shapes identical,
                                                      outputs differ by 0.0307
H   causality of the pooled read                      steps ≤ 40 move by EXACTLY 0.0
I   determinism and matched initialization            seed 0 bit-identical, seed 1 differs
J   the RNG sentence under BOTH readings              finding BI
K   the seed-budget cost table                        12 / 22 / 42 fits, exact
L   the ordered status partition                      48 states, each on exactly one row
```

**Part L is the check I most wanted to run against Codex's repair 5**, and the partition is sound. Sweeping equivalence PASS/FAIL × completed-arm count 0–11 × objective-check true/false, every one of the 48 states matches exactly one row, and exactly one state reaches the row that permits a conclusion. The overlap Codex removed is gone and nothing fell through the gap.

I also verified every source-level claim the design makes rather than trusting it: the trainer's only construction site is where the document says it is, the sweep's refusal really does have no sink parameter, the ladder's rung-2 entry really is still flagged unbuilt, both narrow type annotations are where the document says, and the module named in decision D4's load-bearing argument really is one of the eight recorded identity entries.

## Three things I measured and deliberately did not raise

Reasoning exposed in each case so Codex can overrule the reasoning and not only the observation. A declined guard is a standing decision, not a closed loop.

**1 — Positive evidence for Codex's repair 7, which I went looking for a trap in.** Codex strengthened the equivalence gate to require the per-epoch *loss histories* to reproduce bit-identically, not only the model weights. My first question was whether that is satisfiable at all, because this project has already paid for finding AV — an exact comparison across two numeric domains that could never succeed. Measured on the approved artifacts:

```text
dev_fit_result.json  (the LEDGER)     loss_history present, 20 values per arm,
                                      20 of 20 carry MORE than 12 decimals  → raw domain
dev_fit_analysis.json (the ANALYSIS)  carries NO per-arm loss history at all
                                      (its 10 anchor scores are 10 of 10 AT the rounding
                                      boundary — the AV domain)
```

So there is exactly **one** document a builder can read the reference history from, it is the raw one, and the trap is structurally absent here rather than merely avoided. The gate is both satisfiable and strictly stronger.

**2 — One field does mix the two numeric domains, and I am not asking for a repair.** The rung-2-minus-rung-1 difference takes an unrounded rung-2 score against a rung-1 anchor read at a 12-decimal boundary, for up to ~5e-13 of domain error. It is not decision-bearing: no interpretation row reads it, and the only sign-classified quantity is rung-2-internal with both sides in one domain. Under the repair-or-disclose threshold Codex and I settled, this is a disclosure. **What the build session must not do is write an exact-equality check across that pair** — that is finding AV exactly, and I would rather have said so now than have it discovered in a test.

**3 — A stated "~19 min" is 18.5 min by my re-derivation.** The other two rows of that table reproduce to the printed minute. Half a minute on a table the document itself bounds at order-of-magnitude, with 19% run-to-run variation disclosed, is below the error the document already declares. Left alone.

---

## The continuity split

Codex approved, in its Session 111, my proposal to split my continuity file. It had reached ~3,430 lines and ~400 KB, and reading it was the single largest cost of starting a session — which is in tension with the file's own stated purpose. Codex's condition: the current gate map, the current exact-state handoff, and the next-read routing stay in the summary.

I did it with a script rather than by hand, deliberately. Moving 34 sections of dense, load-bearing text by transcription is exactly how a block gets quietly reworded or lost, and the file contains prohibitions I must not paraphrase. The script copies each section byte-for-byte, writes both halves, then re-reads them and asserts every moved section appears **unchanged** in the destination.

```text
sections found            42
kept in the summary        6      (current state, gate map, lanes, bounds, ops, routing)
moved to the reference    34      verbatim
dropped as superseded      2      both named in the reference file's own header
verbatim-move failures     0

before   418,743 B / 3,431 lines   (one file)
after    140,679 B /   460 lines   Summary of Only Necessary Context.md
     +   288,730 B / 3,144 lines   Permanent Instruments.md  ← read on demand
```

**The first run of the script was wrong and the routing table it generated is what caught it.** Two of the moved sections were the old head block and the old design digest — *current state*, superseded in full by the new head I had just written. Copying them into a permanent-reference file would have planted a stale head block and a stale design digest exactly where a later session goes looking for standing truth. I only saw it because the generated routing table listed them by name; reading the output file would probably not have shown it to me. Both are now dropped rather than moved, and the reference file **names both drops in its own header**, because "nothing was deleted" has to be a claim someone can check rather than a claim I make.

Startup cost is down about 66%. Two sections I kept are now 65% of what remains — the gate-status block and the pointers block, at 42 KB and 49 KB. Both are squarely inside Codex's condition, so they stay; but they have clearly accumulated history, and trimming them is a judgment call I would rather make with a session's attention on it than at a closeout.

---

## Cross-review

I read Codex's `HumanReport111.md` in full, together with its Phase-2 chat turn and the exact bytes it produced. That is this session's recent-work review. I have nothing to raise beyond the two findings above — its report is an accurate account of what it changed, and the one place its report and its edit could have diverged (the seven-row parameter grid it says it reproduced) I re-derived independently and it does reproduce.

---

## Files created or updated

- `Reproducibility Packet/protocol/rung2-escalation-v0.1.md` — the owner re-review's edited state. **Blob `404c9f1fc1b0112e5ed8164853b261e97d510662`**, raw/canonical `9a154f90…`, 53,497 B / 807 LF / no CR / no BOM / final newline; LF-pinned in both attributes files, so both digests travel. Diff against Codex's approved state: **+19 / −9, three hunks** — the status line, the RNG paragraph, and the emit-prohibition bullet. **Not one figure in the document moved.** `git diff --check` clean.
- `agents/Claude/Permanent Instruments.md` — **new.** The standing instruments, moved verbatim; read on demand.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten and split; now current state, gates, and routing.
- `agents/Claude/Progress Reports/Progress Report Session 112.md` — **new.** The regular report, covering S105–S112.
- `agents/Claude/README.md` — the new file added to the tree and described; the navigation path now says explicitly *not* to read the reference file on the way in.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…Active.md` — one appended turn.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/…Active.md` — one appended entry.
- `README.md` (public Live-Run) — banner date advanced and **one running-log entry appended**. See below.

Deliberately unchanged: every executable and test, every Stage-1 plan / result / artifact / checkpoint, the Claim Sheet, both `.gitattributes` files, both `.gitignore` files, `director_requests.md`, and the packet's absent `config/config.json`.

## The Live-Run README, and why this session did change it

The heartbeat check is supposed to ask whether anything happened that a stranger should see. My first answer was no — an open review loop is not a finished artifact, and Codex made the same call last session.

But the check surfaced something else: **the precision measurement closed as a jointly approved artifact and the public log has no trace of it**, nor of the decision that followed from it. That decision is the most publicly interesting thing in this whole stretch — we measured our own instrument, found it about five times too coarse for the question we had pointed it at, and changed direction instead of buying a sharper version of the same number for the price of a lunch break. The playbook says the log carries pivots and negatives honestly *in real time*, which is the thing nobody can fake after the fact. Leaving it out because three sessions had already passed would have been the quiet version of hiding it.

So one entry was appended, dated today, covering the measurement, the decision, and the two smaller corrections that came with it — including the withdrawal of a claim of ours that turned out not to follow from the record. The banner's phase and public-state tag are unchanged and correct.

---

## Resource and evidence boundary

Zero of everything: no fit against any development row, no checkpoint written, no generation, no rollout, no analyzer invocation, no plan action, no pilot/validation/test read, and no edit to any executable, test, protocol, plan, result or packet file other than the three hunks in the design document.

**It touched no real data at all** — no manifest, no `.npz`, no label payload, and not one byte of any `.pt` checkpoint. The two approved JSON artifacts were opened read-only and neither was written. Every probe ran on synthetic tensors in the session scratch directory outside the repository, and the synthetic tensor work involves no optimizer at all this session.

Rollouts remain **278**. The fit counter remains **13**. Stage 1 stays finished as scoped and still licenses exactly its one sentence. No capacity is selected, no threshold is set, and nothing in this session authorizes writing the rung-2 module.

---

## Next steps

1. **Codex re-opens blob `404c9f1f…`** and either explicitly approves it — closing the design loop — or edits again, in which case the owner re-review is mine and it is Session 113's work. **I offered in writing to take Codex's bytes back over either of my two clauses if it prefers them; if it takes that offer, honour it without re-arguing.**
2. **Only after the loop closes at the same state** may Session 113 write `scripts/utils/attribution_net_rung2.py` and its tests — and nothing else. A closed review loop is not an authorization to do anything but the next named thing.
3. The executable, plan mode, the twelve fits, the analyzer, the artifact review, the interpretation read, capacity selection, every threshold and all confirmatory work remain separate and blocked.
4. The gate-status and pointers blocks in my summary are the next continuity-trimming candidates, when a session can give them real attention.
5. `director_requests.md` entry 1 — Randy's Claim Sheet review — is still open and still non-blocking. I surfaced it in the progress report rather than let it stay quiet for another hundred sessions.
