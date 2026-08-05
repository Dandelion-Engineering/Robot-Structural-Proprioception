# Claude — Human Report, Session 78

**Date and time:** 2026-08-05 09:12 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278.**

---

## Summary

This session did two things. First, it closed my half of the review cycle Codex opened on
the Gate-4 learned attribution rung — accepting Codex's finding and repair in full,
finding one new silent defect *in* that repair, fixing it, and handing the state back.
Second, it built the executable form of the training authorization Codex issued in its
Session 77: the module that decides which data a development-only fit may read, what the
fit plan is, and what every checkpoint must be able to say about itself.

**No model was trained. No checkpoint exists. No data was generated. Zero rollouts.**

---

## 1. The review cycle on the attribution rung

### What Codex found, and why I accepted it

Codex's Session 77 found that PyTorch's `load_state_dict` is not transactional: it can
copy compatible tensors into the live network and *then* raise on a missing key. The
estimator's `attach_trained_weights` sets its provenance string only after a successful
load, so a failed replacement left **mixed weights labelled with the previous run's
identity** — the exact silent state the provenance requirement exists to prevent.

I did not accept this on the report. I drove **both blobs in a single process** from one
common driver — Codex's from the working tree, mine written out of git history — so the
only difference between the two runs is the bytes under test:

| | exception | live tensors moved | provenance afterwards |
|---|---|---|---|
| my Session-77 state | `RuntimeError` | 1 (`input_proj.weight`) | the *old* run's string |
| Codex's repair | `RuntimeError` | 0 | the *old* run's string |

The defect is real, the repair closes it, and Codex's regression test goes red against my
state — which I checked rather than assumed.

### The defect I found in the repair

Codex's fix validates the incoming weights on a deep copy and then does `self.net =
candidate`. That is transactional, and it also **replaces the estimator's network object**.
Anything that captured `estimator.net` before the call is left holding an orphan:

| | `est.net` is the captured object | an optimizer step on the captured params moves `est.net` |
|---|---|---|
| my Session-77 state | yes | yes |
| Codex's repair | no | no |

The order that produces this is ordinary, and it is the order the trainer I am about to
write will use: build the estimator, build the optimizer over `est.net.parameters()`,
then resume from a checkpoint. After that, every optimizer step trains a module the
estimator does not read. There is no exception, the loss falls, and the estimator's
weights never move.

It is the same *class* as the defect Codex found — a silent mislabel — pointed the other
way: Codex's made the weights disagree with the provenance; this makes the trainer
disagree with the estimator.

**The fix keeps both properties.** Validation still happens on a deep copy, so nothing
touches the live network until the whole state dictionary and the device transfer have
succeeded; the install then writes the validated tensors *into* the live network instead
of replacing it. The second load cannot fail partway — the candidate is a deep copy, and
a strict load neither adds keys nor changes shapes, so the two agree by construction — and
the docstring carries that argument rather than leaving it implicit.

Three tests were added, and the report names which one is the evidence: the **optimizer**
test, because it names the consequence rather than the identity. The other two pin the
identity on the success and refusal paths.

This is the fourth consecutive round in this project where the defect lived one layer
below the layer being repaired. That pattern is now the first place I look after any fix
lands, and it is why I looked here.

### Two rulings, both accepted, both acted on

Codex ruled that **fitting the rung on the already-delivered `dev` partition is authorized
as development evidence** (it reads persisted rows and generates nothing), under five
narrow bounds; and that the **Config Freeze Readiness Review governs the ordering** —
model implementation and dev fitting come *before* the final `config.json` freeze, not
after, because the frozen configuration has to contain model and threshold choices that
cannot exist before the model does.

I raised the second contradiction in my Session 77 and believed my own docstring was the
stale side. Codex agreed, so the docstring was corrected forward. **A second instance
existed** and I went looking rather than assuming there was only one: `scripts/utils/__init__.py`
carried the same "trained post-config-freeze" claim. Both are corrected, and the correction
keeps the part of the old sentence that was right — training on data that does not exist
would be fabrication, which is why a fit is authorized only against an already-delivered
partition.

---

## 2. `utils/dev_fit_contract.py` — the authorization, made executable

Codex's ruling names four things to build and review: the trainer, the checkpoint/result
schema, the data-role refusal, and the seed/suite plan. **I built the last three and
deliberately not the trainer.** The reason is that refusals have to be reviewable on their
own: a role check buried inside a training loop is only exercised by running the loop, and
this project has repeatedly found that a program's exit paths are the region no test
enters. Everything in the new module is a pure function over data a test can construct, so
every state a refusal exists to catch can be built directly.

What it enforces:

- **Which rows.** `dev` rows of the matched suites only; a caller-assembled list is
  re-checked at the point of *consumption*, because that is the path no filter guards. An
  empty selection is refused rather than returned. Every selection carries a census that
  states its own denominator — how many rows existed, how they split, how many were
  withheld — so no downstream number is reported over an undisclosed base.
- **Which fits.** Five explicitly named training seeds and two matched suites, crossed
  into a ten-fit plan. An unbalanced set is refused, because a paired C1-vs-S comparison
  is only paired if both arms ran the same seeds. `C0` is refused outright: no C0
  observations were ever generated.
- **What a checkpoint must say.** The exact development-only authority string, the data
  root's bare name, the manifest / configuration / assignment digests, the suite, the
  seed, the identity of the code that did the training, the checkpoint digest, and the
  row disclosure. Every rendering of the record validates before it is produced, so a
  record cannot refuse to describe itself while agreeing to be written to a file.
- **What it cannot do.** The module imports neither MuJoCo nor PyTorch — checked in a
  fresh interpreter, because this one has already imported both. It therefore cannot
  simulate anything, which is bound 2 in import form.

It was wired against the real delivered dataset in a **read-only** check: 944 manifest
rows, 304 `dev` (152 C1 + 152 S), 640 withheld, one configuration hash across all 304.
No `.npz` was opened, no model was built on a delivered row, nothing was written.

---

## 3. Three defects in my own new work, all found by mutation

The first mutation sweep over my own module came back **20 of 23**, and I am reporting
that rather than only the clean second run.

1. **The suite filter was never exercised.** My fixture had `dev` rows in C1 and S only,
   so deleting the filter entirely left the test green — the fixture already had the
   property the filter establishes. Closed by adding a `dev`/C0 row and asserting it is
   withheld while the census still counts it.
2. **One of the two renderings could skip validation** and nothing noticed, because the
   only invalid-record test went through the other one.
3. **Half of my own path predicate was dead code.** I wrote the "is this a bare name"
   check as a conjunction over both path flavours. Dropping the POSIX half survived the
   suite, so I enumerated 3,564 strings: 1,009 that the Windows parser refuses and the
   POSIX parser accepts, and **zero** the other way. The POSIX half rejected nothing, so
   it was deleted rather than left looking authoritative, with the measurement recorded
   in the docstring.

And one the grid caught while the tests were being written: `..` is a *bare name* to
Python's path library, and joining it to a root walks up the tree. It is now refused by an
explicitly named, equality-pinned list, because that is a decision about names rather than
a property of any shape.

---

## 4. One instrument fault of my own

I took the blob hashes of every file I had touched **while a mutation sweep was still
running in the background**, and one of them was the hash of a *mutant* rather than of my
work. I caught it because the sweep's own restore digest and `git hash-object` disagreed
afterwards; nothing downstream used the bad number, and every hash reported this session
was retaken with nothing else running and confirmed stable across two calls.

This is precisely the "concurrent writer" residual I named in Session 73 as the one thing
no measurement can close — arriving in the place I had not thought to apply it. **A
mutation sweep is a writer, and any measurement of the repository taken while one runs is
a measurement of a mutant.**

It also surfaced a real fault in both sweep harnesses: they restored the file with a
text-mode write, which on Windows translates every line ending, so their "restored
identical" check was comparing a converted file against its own converted digest. Both
harnesses now read and write bytes and encode each case pattern in the target file's own
newline convention.

---

## 5. Verification

```text
attribution_net mutation sweep   17 cases | 17 CAUGHT | 0 survivors | both passes identical
                                 restore byte-identical
dev_fit_contract mutation sweep  23 cases | 23 CAUGHT | 0 survivors | both passes identical
                                 restore byte-identical (first pass 20/23; see section 3)
focused suites                   test_attribution_net.py 68 passed (was 65)
                                 test_dev_fit_contract.py 56 passed (new)
FULL PACKET SUITE                1,430 passed in 125.33 s (Codex's 1,371 + 3 + 56)
compileall                       clean
real-data touches                one read of manifest.csv; no .npz opened
rollouts                         0
config/config.json               absent
```

---

## 6. Files created or updated

- `Reproducibility Packet/scripts/utils/attribution_net.py` — identity-preserving
  transactional install (blob `c4fa3c63`)
- `Reproducibility Packet/tests/test_attribution_net.py` — three tests for the identity
  property and its consequence (blob `5a401ca1`)
- `Reproducibility Packet/scripts/utils/dev_fit_contract.py` — **new** (blob `73e5e743`)
- `Reproducibility Packet/tests/test_dev_fit_contract.py` — **new**, 56 tests (blob `3959ff28`)
- `Reproducibility Packet/scripts/utils/estimator.py` — freeze-order correction (blob `b2abf463`)
- `Reproducibility Packet/scripts/utils/__init__.py` — second freeze-order instance
  corrected; `attribution_net` added to the module index (blob `04647db4`)
- `Reproducibility Packet/README.md` — the new module and the corrected ordering (blob `ebef72fe`)
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — my Session-78
  turn, `+262/−0`
- `agents/Claude/Session Summaries/HumanReport78.md` — this report
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — updated

**Root `README.md` (the public live-run page): checked, deliberately unchanged.** The
heartbeat rule is that an entry belongs on the log when something is *finished*. The
review loop is still open, the new module is unreviewed, and Codex had already posted the
scope correction covering the training authorization hours earlier. Logging an unreviewed
module would be logging work in progress, which the log is explicitly not for.

**`.gitignore`: checked, no change needed.** It already covers the virtual environment,
the local dataset, caches, and the three session locks.

---

## 7. Next steps

1. **Codex owns the next turn.** Two loops are open: the attribution rung at
   `c4fa3c63` / `5a401ca1`, and the new dev-fit contract at `73e5e743` / `3959ff28`,
   which has never been reviewed.
2. **Four choices in the new module are flagged for Codex to rule on or overrule** —
   where the shared authority string should live, refusing a frozen-looking configuration
   hash, comparing the assignment digest for equality rather than shape, and requiring the
   data root to be a bare name rather than a path.
3. **The trainer is my next session's work**, and it will consume the plan and the
   provenance record rather than re-deciding either. No fit may run until both loops close.
4. Pilot, validation, test, the final configuration freeze, further payload measurement,
   and all confirmatory work remain blocked.
5. My next regular progress report is **Session 80**.
