# Claude — Human Report, Session 89

**Date and time:** 2026-08-07 04:22 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session: 0.** Project lifetime total remains **278**.

**Fits: 0. Checkpoints: 0. Data generated: 0. Pilot / validation / test reads: 0.**

**Progress-report session:** no. My next regular is **Session 96**; no phase transition and no
approved Claim-Sheet amendment fired this session.

---

## Summary

This was an owner re-review session. Codex's Session 88 reviewed the two artifacts I own that
were open — the capacity-escalation design and my own Session-88 progress report — edited both,
and explicitly approved its edited states. Under the review cycle my job was to genuinely
re-open both, re-derive rather than accept, and either approve the same bytes or edit and hand
back.

**I kept every one of Codex's five edits and all five of its rulings, uncontested.** I went
looking for something to push back on and did not find it — the second consecutive session
where that has been the honest outcome. I then found three further defects and repaired them
in place, so both files went back rather than closing.

**The finding that matters is an interaction, not an error.** Two of Codex's repairs are each
correct and each necessary. Together they open a hole neither has alone: removing the machine
path from the sweep's plan document (correct — a physical path and byte-determinism cannot both
be required) also removed the only thing that made two executions two *different* documents.
Since the execution authorization is a digest naming a document, and since the same review's
new retry rule licenses re-running all forty fits after a refusal, a second full spend would
have passed every gate the design names without a second joint authorization. I repaired it
with a one-line `run_label` field that restores single-use authorization without restoring the
contradiction Codex correctly removed.

**Tenth consecutive round in which the defect sat one layer below the repair** — and the first
where the layer below was not code, not logic, but the space between two correct repairs.

## What was accomplished

### 1. Verified Codex's returned state before keeping any of it

The state Codex handed back was confirmed byte-for-byte as reported: blob `e1c8f77c`,
canonical `835e2fc6…`, 47,707 bytes, 774 lines, LF, raw == canonical, no BOM.

I then checked each ruling against something **outside** the document, because checking a
design against its own logic is precisely how last session's defect survived two reviews:

- **The five-width constructor map, rebuilt independently** (no data read): 10,586 / 22,786 /
  39,594 / 61,010 / 87,034 parameters, receptive field 1,023 at every width, the rung-1 band
  guard accepting all five. Codex's table reproduces exactly, and so does my own Session-88
  measurement.
- **`code_identity()` and `require_code_identity()` read rather than assumed.** Neither imposes
  a cardinality, so Codex's Route-A provenance correction — a *ninth* identity entry for the new
  module — is implementable without editing the closed contract file. This was the claim I most
  wanted to be wrong about, because I had written the opposite in my draft. Codex is right: code
  the fit executes belongs in the identity of the fit.
- **`dev_fit_result.json` read**, to confirm the two arms Codex's equivalence gate names —
  `(C1, seed 0)` and `(S, seed 4)` — both exist with 20-epoch loss histories, and that all ten
  approved checkpoints are on disk. The gate's bit-identity comparison is *makeable*, not merely
  specified.
- **`dev_fit_analysis.json` read**, confirming both constants the design sources at run time:
  `claim_sheet_success_bar = 0.05` and `sample_sd_S_minus_C1 = 0.149635726834`.

### 2. Three defects found and repaired in the design

**Finding AA — the authorization hole (the load-bearing one).** Described above. The repair is
a required `run_label` token serialized as the leading component of the plan's logical output
namespace: machine-independent, so byte-determinism across host directories survives verbatim;
run-scoped, so a retry is a different document needing its own joint authorization. §7.2 now
records it alongside the consumed digest so the sequence of authorized runs is reconstructable
from the artifacts alone, and §7.1 carries the full argument under a heading saying why the
field must not be optimized away later.

**Finding AB — the exact call site was still not written down.** Codex's ruling chose the
"new module" route and left the builder to discover what the copied fit loop actually calls. It
calls `_stack`, which is **private**, and which is the batching function — the single place a
retyped copy would most plausibly diverge in a way that changes weights. The design now
tabulates the complete call surface of `fit_one_arm` (lines 942–995), names the one expression
that changes, and makes the import decision explicitly rather than leaving a failed equivalence
gate to discover it. This is my own Session-88 lesson applied to the ruling that lesson
produced; I should have written it when I wrote the lesson.

**Finding AC — a sourced constant whose source was not written down.** `anchor_sample_sd` said
"read from the approved artifact" without naming the field, while `BAR` two subsections earlier
names its path exactly — and the field's name (`paired_macro_f1.sample_sd_S_minus_C1`) is not
guessable from the quantity's. With the literal value sitting in a parenthetical beside it, that
is an invitation to hard-code. Now named to the field, with a refusal specified and the literal
demoted to a reader's convenience the executable may not carry.

### 3. Codex's edits to my progress report — accepted in full, plus two owner changes

Codex struck two sentences of mine that said the capacity sweep would tell us whether the first
result was caused by an undersized network. The design I wrote **in the same session** says
explicitly that it cannot separate width from optimization. That is my own Session-88 lesson —
*a withdrawn claim needs a rule, not an edit* — reappearing inside the report that recorded the
lesson. Second occurrence in the same stretch. Codex was right and I kept the substance whole.

Two changes on top, neither touching that substance:

1. **Register.** The progress report is director-facing at the Accessible-Piece bar. Codex's
   replacement carried "width-dependent trainability under a fixed 20-epoch protocol" and
   "representational capacity" unglossed, in the paragraph a non-specialist reads first. Same
   distinction, plain words.
2. **Two forward-looking statements had gone stale** between Codex's session and mine: the route
   choice is no longer open (ruled), and the training-run count is now forty-two rather than
   forty. The historical sentence is left as the record with a dated parenthetical rather than
   rewritten.

I deliberately did **not** touch the body of the section Codex's edits framed. I re-read it and
it was already careful; the overreach was in the framing sentences only, which is why a
two-sentence excision was the right size of repair.

## Challenges, and how they were handled

**The temptation to approve.** Codex's edits were good, its rulings were sound, and the fastest
path was to approve the same bytes and move on. The review cycle exists precisely because that
is the failure mode. What made the difference was one question: *what else was the deleted field
doing besides the job it was deleted for?* That question found AA, and it generalizes — before
removing a field from a contract, ask what was depending on it existing.

**Deciding what counts as rewriting history.** Codex edited a dated progress report, and I then
edited it further. Progress reports are time capsules; correcting one after the fact is close to
a violation of the project's append-never-overwrite discipline. The line I drew: the report is
in an *open* review cycle and has not been handed to the director as final, so factual
corrections to its forward-looking section are legitimate, but a historical claim about what was
open at the time gets a dated parenthetical rather than a rewrite.

**A near-miss I want recorded.** I initially believed Codex had introduced a defect by deleting
the `TOO_FEW_ELIGIBLE_POINTS` outcome label, which had guarded against reading a "the difference
did not move" statement off a single data point. I worked it through before writing it down and
it is **not** a defect: the anchor at 32 channels is known-eligible by measurement, and the
replacement table's fourth row can only be reached when at least one point above the anchor is
eligible too, so the eligible sequence always has at least two members there. Reported here
rather than in the chat because a finding that dissolves under checking is not a finding — but
it is exactly the kind of thing that gets reported as one when the check is skipped.

## Decisions made

- **Edit and hand back rather than approve.** Three real defects is not a state to close on.
- **`run_label` rather than restoring the path.** Restoring the output root would have re-opened
  the contradiction Codex correctly closed. The field is the minimum object that has both
  properties.
- **Import `_stack` rather than retype it**, and disclose the private cross-module import. The
  alternative is a hand-copied batcher, which is exactly the divergence the equivalence gate
  exists to catch — paying a gate failure to discover it would be a wasted gate.
- **No Live-Run README entry.** Fourth consecutive session of mine adding nothing. An open review
  round on an unfrozen draft is work in progress, and the public log is lean by design.
- **No monitoring-chat note.** Verified at the git level rather than assumed: Codex's Session-88
  commit touches the Phase-2 transcript as a single tail hunk `@@ -24176,3 +24176,122 @@`,
  `+119/−0`, additions only, and touches the monitoring file not at all. No recurrence, so no
  note — the duty there is to flag recurrences.

## Files created or updated

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` — owner re-review; every Codex
  edit and ruling kept, three defects repaired. Returned at blob `51c86f68`, canonical
  `19c6edb3…`, 55,534 bytes / 873 lines / LF / raw == canonical / no BOM, `+113/−14`.
- `agents/Claude/Progress Reports/Progress Report Session 88.md` — Codex's correction accepted in
  full; register restored and two stale forward-looking statements corrected. Returned at blob
  `58276bb4`, canonical `1e359749…`, `+29/−22`. **Not LF-pinned** — a fresh checkout renders CRLF
  and a different raw digest, so the canonical digest is the one to quote.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — one append, `+205/−0`,
  single tail hunk, header unique at line 24,299, prefix byte-identical asserted inside the writer.
- `agents/Claude/Session Summaries/HumanReport89.md` — this report.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.
- `agents/Claude/README.md` — refreshed.

## Verification

```text
full packet suite      1,551 passed in 115.55 s  — count UNCHANGED, because no executable
                       file was touched by either agent this round
git diff --check       clean
constructor map        five widths rebuilt independently; matches Codex and matches my S88
code identity          code_identity() / require_code_identity() read; no cardinality bound,
                       so a ninth entry is expressible
equivalence feasibility  both C9 arms present in the approved ledger with 20-epoch loss
                       histories; all ten checkpoints on disk
FITS 0 | CHECKPOINTS 0 | GENERATION 0 | ROLLOUTS 0 | LIFETIME TOTAL STILL 278
REAL-DATA TOUCHES      reads only, and only of TRACKED results files and source. No manifest,
                       no .npz, no checkpoint, no regeneration. PILOT / VAL / TEST: 0.
config/config.json     absent, as designed
```

## Next steps

1. **Codex's same-state reviewer re-review** of `51c86f68` (design) and `58276bb4` (report). The
   design is not frozen until both agents approve one state, and it is still `v0.1` by Codex's
   own instruction, because it has never been jointly approved.
2. If AA is judged wrong, `run_label` comes out — I said so in the chat and wrote the argument
   into the document so a future session can judge it rather than inherit it.
3. **Then** the Stage-1 executable is written and reviewed. Separate gate.
4. **Then** a zero-fit plan run is produced and reviewed. Separate gate.
5. **Then, and only then,** the forty-two development fits are jointly authorized. Zero rollouts,
   about six minutes of computer time, behind four separate approval gates.
6. After that: the network's confidence calibration (Gate 5) and the evaluation driver (Gate 7).
