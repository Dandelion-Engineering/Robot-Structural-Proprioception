# Claude — Human Report, Session 81

**Date and time:** 2026-08-05 20:31 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278.**
**Progress-report session:** no. My last regular was Session 80; my next regular is **Session 88**. No phase transition and no approved Claim-Sheet amendment fired this session.

---

## Summary

Two things happened this session, and the second one only became possible because of the first.

**The dev-fit contract loop closed at round four.** This is the small module that decides
what a development-only training run is allowed to read, and what every saved model must
be able to say about where it came from. It has been through four full adversarial review
rounds across Sessions 78–81, and every one of those rounds found something real. This
session I re-opened Codex's repaired state, reproduced its finding against my own bytes
rather than taking it on report, verified the repair was actually guarded rather than
merely present, hunted for a further defect with a deliberately different instrument, and
then **approved Codex's exact bytes**. Both agents have now explicitly approved the same
state, which is what closes a loop under our review cycle. It does not reopen.

**Then I built the trainer.** With the contract closed, Codex's Session-77 sequencing says
the training executable is next, so I wrote it: `utils/dev_fit_trainer.py` plus its test
file, 15 tests, all green, no regressions anywhere in the packet (1,482 tests pass, up
from 1,467). **Nothing has been trained.** The trainer has its own review to pass before
a single development fit is authorized to run, and I have not run one.

For the director, in plain terms: the project spent four sessions writing and re-reviewing
a rulebook, and this session the rulebook was finished and the thing that has to obey it
was built. The honest caveat from my Session-80 progress report still stands and I restate
it below rather than let it quietly disappear now that there is forward motion.

## What I did, in order

### 1. Verified the state before trusting it

Working tree clean; the two files on disk hashed to exactly the blobs Codex approved
(`bd2c0d08` / `fbd941b5`). I check this every session because "verify the live git state
before trusting continuity" is a lesson this project bought the hard way.

### 2. Reproduced Codex's Finding F against my own blob

Codex's finding was that I had deleted a validation call from the producer as redundant,
and that it was **not** redundant when two fields of one entry are malformed at the same
time. I did not accept that on the strength of its report. I wrote my own Session-80 blob
back out of git into the package as a sibling module — so its relative imports resolved —
and drove both versions in a single process, then deleted the temporary file.

Both halves reproduced against my bytes:

- a path-shaped label paired with a bad value had its **whole path quoted** in the refusal
  message, by a guard that exists specifically to never do that; and
- a mapping with mixed key types escaped as a foreign `TypeError` from `sorted()`.

Under Codex's repaired state both are refused cleanly and the message names only the final
component. I also added a case Codex did not have — an **integer** key — and confirmed its
repair covers it, because the rule is stated once as a type predicate rather than as a list
of spellings. **Its diagnosis was right and mine was wrong**, and I said so plainly in the
chat rather than softening it.

### 3. Caught a fault in my own instrument

My reproduction probe had an automatic leak detector — does the secret path appear in the
refusal message — and it reported **no leak on the very cell that leaks**. The message is
rendered with Python's `repr`, which escapes each backslash, so the literal path string is
genuinely absent from a message that plainly displays the path. I only caught it by reading
the output instead of trusting the flag.

This is the Session-80 lesson arriving one level down. Last session I learned that a probe
inherits the shape of the finding that motivated it. This session: an *automatic verdict*
inherits the shape of the **rendering** its author had in mind. Every later probe this
session used a marker token that survives any escaping.

### 4. Proved the repair was guarded, not just present

A line that is correct but that no test would notice being deleted is not protected. A
seven-case mutation sweep at the mandatory harness shape — bytecode caches cleared, no
early exit, line-ending-agnostic anchors because the file genuinely mixes CRLF and LF,
restore verified, whole sweep run twice — returned **7 caught, 0 survivors, both passes
identical, restore byte-identical.** Codex's claim that both call sites are non-vacuous in
both directions is now measured rather than asserted.

One case in my first run came back as an anchor failure because I had truncated an anchor
mid-statement. The harness reported it as a **failure rather than skipping it**, which is
precisely the rule that exists for it, and I fixed the anchor and re-ran.

### 5. Built the instrument for the *class*, not the instance

Codex's finding is a class: in a consumer over a multi-field object, one field's refusal
can render or crash before a sibling field has been validated. My Session-80 grid drove one
hostile value at a time and could not construct that state by shape. So I built the
cross-field grid — every multi-field consumer in the module, two hostile fields at once,
32 cells, reporting three verdicts including one nothing had looked for: *does the refusal
disclose the value hidden in the other field*.

**Codex's repair is total over the object it repaired.** Thirteen cross-field cells, zero
escapes, zero disclosures. I want that recorded because for five consecutive rounds the
answer had been "there is another defect one layer below," and here there is not. Saying so
accurately matters more when the accurate answer is the less dramatic one.

### 6. Finding G — measured, disclosed, and deliberately not blocking

The grid did find one real accept, and it is in a different part of the record. The
provenance record enforces "no machine path in this document" on its data-root field —
strictly, with a documented rationale, upheld by Codex's own earlier ruling — and enforces
nothing but "non-empty string" on the neighbouring free-text field that lands in the *same*
document. Five cells demonstrate a filesystem path travelling all the way into the record's
canonical JSON.

**I chose not to block the loop on it, and I want the reasoning on the record.** I checked
each of the five bounds rather than asserting: it cannot let a fit read withheld data,
cannot let a development artifact pass as confirmatory, cannot corrupt an identity, and
cannot break the record's one-line property. Its worst case is a hygiene violation inside
an artifact that is ineligible for the real analysis by construction. Weighed against a
fifth round on one module, holding the loop open for it is not a trade I think this project
should make.

I also did the measurement that decides the *repair*, so Codex is not ruling blind. The
obvious fix — refuse anything containing a drive letter — **false-positives on the module's
own legitimate output**: its real sentence contains `t:` and `d:`, from the words "split:"
and "selected:". That is exactly a defect this project already paid for in Session 70. The
sentence contains no path separator at all, so the safe total rule is "single line, no `/`,
no `\`", and I offered to implement precisely that in one turn if Codex rules it should be
closed in the module. **Meanwhile the trainer I then built makes the state unreachable in
practice** — it passes the census's own sentence and nothing else, and a test pins it.

### 7. Built the trainer

`Reproducibility Packet/scripts/utils/dev_fit_trainer.py`. It fits the rung-1 network once
per `(suite, seed)` arm of the ten-arm predeclared plan. What it is built around:

- **The determinism context wraps forward *and* backward**, not just the forward pass. The
  GPU's default reduced-precision mode applies to the convolution *backward* kernels too,
  so a context covering inference alone would leave gradients computed at a precision the
  context was opened to prevent — and a paired C1-vs-S difference would carry a hardware
  flag inside it.
- **The arms come from the contract's plan**, not from a loop the trainer writes.
- **The role check runs where rows are consumed**, not only where they were selected,
  because a caller can build a row list itself and that is the path no filter guards.
- **Every saved model gets a validated provenance record** — checkpoint digest in the raw
  domain, code identity in the canonical-text domain, built by the contract's own function
  rather than hand-assembled.
- **A comparison cannot be reported over an incomplete plan.**
- **Two inputs are required with no default**: the data root, and the window origin. The
  window origin is a pre-registration-adjacent decision, and a default would have made that
  decision quietly inside a development script. Requiring it keeps the choice visible and
  records it in the result.
- **A refusal's message is never persisted.** It can quote a caller-supplied string, and
  our standards forbid a result artifact recording an absolute path. Rather than build a
  scrubber — the accept side of a scrubber is where damage is invisible, and we spent five
  sessions on exactly that in the payload work — the artifact records only which check
  refused and the exception class. The message goes to the operator's screen and nowhere.
- **Every terminal exit is named, writes an artifact, and has a test that drives that exit
  and reads back what it wrote.** The exit paths of a program are the region no test enters,
  and this project has been bitten there four times.

## Challenges, and how they were resolved

**My own probe under-reported the leak it was written to find.** Resolved by reading the
raw output instead of the verdict, then rebuilding every subsequent probe around a marker
that survives escaping. Recorded as a lesson rather than quietly fixed.

**A bad mutation anchor.** The harness caught it because the rules say an ambiguous or
absent anchor is a failure, never a skip. Fixed and re-run; the discipline paid for itself
in the same session it was applied.

**Two test-fixture mismatches with the real storage contract.** My synthetic manifest gave
the two suites of one pair different group identifiers, which the manifest audit correctly
refuses because paired rows must agree on every identity field. Fixed the fixture rather
than the check — the check was right. A second, smaller one: I had imported three schema
constants from the wrong module.

**A docstring that claimed more than its test asserted.** My full-fit test's docstring said
"and the loss falls," which it does not check. I removed the claim rather than leave a test
overstating itself — a test that describes an assertion it does not make is how a false
belief enters the record.

## Decisions I made, and why

1. **Approve and close rather than open round five.** The finding I had was real but not
   bound-permeable, and four rounds on one module was already the cost I flagged to the
   director last session.
2. **Disclose Finding G with its repair pre-measured**, so the ruling costs Codex one
   sentence and me one turn, instead of a round of discovery each.
3. **Refuse the obvious repair for Finding G on measured grounds**, and say why in the same
   turn, so nobody re-derives the Session-70 trap.
4. **Make the window origin a required input rather than choosing it.** Late in a long
   session is the wrong moment to make a pre-registration-adjacent decision.
5. **Never persist a refusal message**, instead of building a second scrubber.

## Insights worth keeping

**An automatic verdict inherits the shape of the rendering its author imagined.** The
Session-80 version of this lesson was about probes inheriting the shape of findings. The
sharper version: a detector that searches for a *value* will miss that value the moment
anything between it and the output re-renders it.

**"One function over" is sometimes the honest answer, and it is less flattering than "one
layer below."** Five rounds running, the defect sat structurally beneath the last repair.
This round it did not — the repair was total over its object, and the new finding sits
beside it in a different field. Reporting that accurately mattered because the inaccurate
version would have flattered me, the reviewer.

**A closed loop is not permission.** The contract closing does not authorize a fit; the
trainer's own review does. I wrote that into the chat, the module docstring, and here,
because it is exactly the inference a future session under time pressure would make.

## Files created or updated

**Created**
- `Reproducibility Packet/scripts/utils/dev_fit_trainer.py` — the development-only trainer.
- `Reproducibility Packet/tests/test_dev_fit_trainer.py` — 15 tests; every terminal exit driven and its artifact read back.

**Updated**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — my Session-81 turn, `+225/−0`, additions only.
- `README.md` — one lean running-log entry, `+2/−0`. The banner was already current at 2026-08-05 and was not touched.
- `agents/Claude/Session Summaries/HumanReport81.md` — this report.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 82.

**Approved unchanged, not edited** (the loop closes on *these* exact bytes)
- `Reproducibility Packet/scripts/utils/dev_fit_contract.py` — `bd2c0d08…`
- `Reproducibility Packet/tests/test_dev_fit_contract.py` — `fbd941b5…`

## Verification

```text
two-blob reproduction   5 cases x 2 blobs in one process; my S80 blob written out of git
                        into the package, then deleted.  Both halves of Finding F reproduced.
cross-field grid        32 cells, three verdicts reported (in-domain / foreign / disclosed)
mutation sweep          7 cases | 7 CAUGHT | 0 survivors | 0 anchor failures | two passes
                        identical | restore byte-identical
focused contract suite  93 passed
new trainer suite       15 passed
FULL PACKET SUITE       1,482 passed in 116.60 s  (was 1,467 — +15, no regressions)
compileall              clean
REAL-DATA TOUCHES       NONE.  No manifest read, no .npz opened, no checkpoint written.
FITS / CHECKPOINTS      0 / 0    generation 0    config/config.json still absent
ROLLOUTS THIS SESSION   0        lifetime Protocol-P-related total remains 278
```

## Next steps

1. **Codex re-reviews the trainer.** It is unreviewed and therefore not authorized to run.
2. **Codex rules on Finding G** — close it in the contract module (I implement in one turn)
   or leave the field free-text and rely on the trainer deriving it.
3. **Then, and only then, the ten development fits run** — the first moment this project
   produces a number about whether the model learns anything at all.
4. After that: calibration and threshold work (Gate 5), which is mine and which may only
   touch validation once Gate 4 closes.

## The honest caveat, restated rather than dropped

My Session-80 progress report said that if Sessions 81–88 did not produce a number about
whether the model learns, the concern would stop being a caveat and become the result. This
session did not produce that number either — it closed the rulebook and built the thing
that will produce it. That is real forward motion and I am not going to dress it up as more
than that. **Five of my sessions have now gone into one contract module and its trainer,
and the model still has not been trained.** The next block is short and irreversible:
one review, then the fits. If it stretches again, the director should read that as the
finding it is, and I have written the handoff so that the next session cannot mistake an
open loop for permission or a closed one for a result.

— Claude
