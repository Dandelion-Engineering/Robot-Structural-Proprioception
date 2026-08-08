# Claude — Human Report, Session 93

**Date and time:** 2026-08-07 20:28 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Plan artifacts: 0. Data generated: 0. Pilot / validation / test reads: 0.** This session did not read a tracked results file at all.

**Progress-report session:** no. My next regular progress report is Session 96; no phase transition and no Claim-Sheet amendment occurred this session.

---

## Summary in one paragraph

Codex's Session 92 reviewed the capacity-sweep executable I handed over, blocked it on six
findings, repaired them itself, and handed back an edited state for my approval. This session is
the owner half of that loop. I re-opened both files rather than reading the diff alone, drove all
six of Codex's repairs adversarially from my own side, and accepted every diagnosis and every
implementation unchanged — they were correct, and two of them found failure modes my own mutation
sweep structurally could not see. The re-review then found three more things, one of which is a
genuine violation of the design's own invariant C1: the rule "this program must never write into
the approved checkpoint directory" was enforced in one of the program's two modes and not the
other, so `--mode plan` pointed at that directory wrote a file into it. All three are repaired,
each with a test that drives the guard rather than watching its consequence, and the state is
handed back to Codex. The full packet suite is green at 1,753 tests. Nothing ran against the real
data: no plan artifact, no fit, no checkpoint, no rollout.

---

## What this session was for, in plain terms

The project's diagnosis model has been trained exactly once, at one network size, and the result
was awkward: the sensor suite with *more* information fitted slightly worse. Nobody thinks that
settles anything, because both suites got the same-size network — the richer one had more to
represent and no more room to represent it in. The capacity sweep is the pre-registered
measurement that asks whether size was the constraint, by retraining at five widths.

That measurement is not authorized to run yet. What exists is the program that will run it, and
the project's rule is that a program of this consequence gets read by the other agent before it is
allowed anywhere near the data. Codex read it, found six real problems, fixed them, and gave it
back. My job this session was to genuinely re-read the result rather than nod at it — because the
review cycle only works if the owner comes back, and a rubber-stamp is worse than no second pass
at all, since it produces the *appearance* of two independent reads.

---

## What was accomplished

### 1. Verified the handed-back state before reviewing it

Both reviewer blobs match the digests Codex recorded exactly — module
`9059bccb…` / canonical `c3c1b3dc…`, tests `42e22a70…` / canonical `aa250c9b…`, both LF, no BOM,
raw identical to canonical. The frozen design document is untouched at blob `b45efa47…` /
canonical `05109d97…`. Codex's session touched only those two files plus its own workspace and the
transcript; every production blob (`dev_fit_trainer.py`, `dev_fit_contract.py`,
`attribution_net.py`, `analyze_dev_fit.py`, both approved results JSON, both READMEs) is unchanged.

### 2. Drove all six of Codex's findings rather than reading them

Each was checked by making the program do the thing, not by reading the patch:

- **C10 as an identity gate.** A complete run document is accepted; replacing one required
  completed arm with a duplicate of another while holding the count at forty is refused; a
  duplicated equivalence arm is refused; a single unattempted arm is refused. Codex's underlying
  point is right and worth carrying: a complete scientific sweep is a fixed set of *named* arms,
  not fifty rows carrying acceptable status words.
- **The refusal filename.** A refusal document written with a fixed identifier lands at a file
  named for that identifier and the payload agrees; forcing a second write redraws the identifier
  and the earlier refusal's bytes are still on disk afterwards.
- **Structurally complete terminals.** The run now starts with all fifty curve arms and both
  equivalence arms present and marked unattempted, replaced in place as work happens, so an early
  refusal can no longer make the downstream arms simply vanish from the record.
- **Partial equivalence state.** I traced the failure unwind rather than the success path,
  including the case Codex did not name: if both comparisons pass but the artifact write fails,
  the run exits as an equivalence failure while the arms read as passed — and the completeness gate
  still refuses that terminal, because the forty curve arms are unattempted. No hole.
- **The plan's provenance surface.** The four added fields are rebuilt and compared by equality
  along with the whole plan, so they extend the existing gate instead of adding a second one.
- **Authenticated checkpoint bytes.** The hash-and-compare runs before the fit counter advances
  and before the file is loaded, and the load consumes the same authenticated bytes rather than
  re-reading the path — so a mismatch spends zero fits and writes zero files.

### 3. Found and repaired three things the reviewer pass did not cover

**AO — invariant C1 was enforced per-mode instead of per-executable.** The design says the
executable "must refuse to write into `results/dev_fit`." The guard had exactly one call site, in
execute mode, so `--base-dir` was checked and plan mode's `--output-dir` was not. Reproduced with
the packet root redirected into a temp tree, so nothing went near the real directory: plan mode
pointed at the protected path exited 3 and left `capacity_sweep_plan.json` sitting inside it. The
easiest route there is the *refusal* branch — a plan that could not even be built writing itself
into the one directory the module may not touch. Repaired by giving plan mode the same guard
before its first write, under the same named exit; the protected directory now gains nothing and
the exit code is 10.

**AP — the equivalence checkpoint filename had two definitions.** The plan declares where each
compatibility checkpoint will be written; the gate that writes it built the same name from its own
copy of the literal. Nothing compared the two, so an edit to either would have left the plan
promising a path the run never produces. Repaired into one definition that both sides consume,
with a test that asserts the files the gate physically wrote *equal* the names the plan declares —
the existing test counted two files in the right directory, which any two files would satisfy.

**AQ — a comment claimed an assertion the code does not make.** The forty-two-fit budget was
described as "asserted on every exit"; it is stated and recorded, and there is no run-time check
anywhere. I deliberately did **not** add one: the budget is an arithmetic property of the two arm
lists the program iterates, not a limit it enforces, and a new refusal path would be a new design
surface under review for an unreachable condition. What actually keeps the constant honest is an
existing test that pins it to the arm counts by equality. I rewrote the comment to say exactly
that.

### 4. Measured the tests rather than trusting them

An eleven-case mutation sweep plus three negative controls, under the harness rules my Session 92
had to learn the hard way — inherited environment, asserted green baseline, controls carrying an
expected-survivor set, no early exit, caches cleared per case, restore verified by digest in a
`finally`, explicit newline handling on every write, and two passes required to agree.

```text
baseline               green
negative controls      3 / 3 SURVIVED  -> the harness is capable of the word "survived"
passes                 agree
applied / caught       14 / 11
real survivors         none
restore                both files digest-identical to the pre-sweep bytes
```

Four of the eleven cases attack **Codex's** repairs, not mine. A passing suite is not evidence that
a specific guard is load-bearing; breaking the guard and watching the suite go red is.

---

## Decisions I made, and why

1. **I edited and handed back rather than approving.** The review cycle allows the owner to
   approve a reviewer's state outright, and the temptation with a strong reviewer pass is to do
   exactly that. But AO is a real invariant violation with a reproduction, and approving around it
   would have made both agents' approvals name a state that violates the design both agents froze.
2. **`X_FORBIDDEN_BASE` covers plan mode too, rather than a new exit.** The reason the exit
   persists no artifact is that every sink is under the supplied destination — which is equally
   true of plan mode's output directory. One exit, one reason. This also makes Codex's own Session
   92 docstring narrowing *more* accurate rather than contradicting it.
3. **I did not add a budget assertion.** Smallest sufficient: the honest fix for a comment that
   overstates the code is to correct the comment, not to grow the code until the comment is true.
4. **I left the public Live-Run README untouched.** No artifact loop closed, no phase moved, and
   the log is lean by design. The heartbeat check happened; the answer was "nothing to log."
5. **I named where I think this loop should end.** Two rounds, both finding new measured defects
   one structural layer apart, so the escalation trigger has not fired and should not be read as
   close-by-count. But I told Codex in the chat that if its next pass finds only coverage, it
   should close — that is the Session 71 heuristic, and stating it in advance is cheaper than
   arguing about it at round four.

---

## Challenges, and how they were handled

- **The reviewer state was good, which is its own hazard.** Six correct findings with correct
  repairs and 199 passing tests is exactly the condition under which an owner re-review becomes
  ceremonial. The thing that broke it open was asking a question the reviewer's frame did not
  contain — Codex audited the *consumers of each guard*, so I audited the *call sites of each
  guard*, and the one guard with a single call site in a two-mode program was the finding.
- **Demonstrating the C1 violation without committing it.** A faithful reproduction writes into
  the protected directory, which is the thing the invariant exists to prevent. I redirected the
  module's own idea of where the packet root is into a temp tree, which makes the guard evaluate
  against a fake protected directory and leaves the real one untouched. The permanent test uses
  the real path but a subdirectory of it, asserts the parent's listing is unchanged, and cleans up
  in a `finally` — the same discipline the execute-mode test earned in Session 92.
- **Not reopening what is settled.** Three of Codex's repairs touch code I wrote and would have
  written differently in places. Preference is not a finding. I checked whether each
  implementation is *correct and defensible*, not whether it is the one I would have chosen, and
  said so explicitly rather than editing around it.

---

## Files created or updated

Created:

- `agents/Claude/Session Summaries/HumanReport93.md` (this file)

Updated:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py` — plan-mode invariant-C1 guard, one
  definition of the equivalence checkpoint name, corrected budget comment, widened module and
  `require_permitted_base` docstrings. **+63 / −18** against Codex's reviewer state.
- `Reproducibility Packet/tests/test_capacity_sweep.py` — three tests: plan mode refuses a
  protected output directory and leaves it unchanged; the gate writes at exactly the names the plan
  declares; the equivalence checkpoint name has one definition and validates its inputs.
  **+91 / −0**.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — my Session 93 owner re-review turn.
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

Reviewed and deliberately unchanged:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` (frozen; the module's own digest
  check still passes against it)
- every approved result JSON and every production module
- `README.md` (the public Live-Run README) and `Reproducibility Packet/README.md`
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — no append-order recurrence this session, so nothing to report
- `.gitignore` and `Reproducibility Packet/.gitignore` — already cover the session lock, bytecode
  and caches, temporary directories and future checkpoints; no change needed

---

## Verification

```text
new-file suite        202 passed in 3.84 s   (199 before + 3 new)
full packet suite   1,753 passed in 128.33 s (1,750 before + 3 new)
compileall            clean
git diff --check      clean
mutation sweep        11 / 11 real cases caught, 3 / 3 negative controls survived,
                      two passes agree, both files restored by digest
handed-back state     module blob 9a1d11a7… / canonical d4db0665…, 93,920 B / 2,198 lines
                      tests  blob 2a043f99… / canonical 81e6e1e5…, 77,253 B / 1,896 lines
                      both LF, no BOM, raw == canonical
frozen design         b45efa47… / 05109d97… UNCHANGED
production blobs      ALL UNCHANGED
packet artifacts      no sweep plan, result or equivalence JSON anywhere in the packet;
                      config/config.json still absent
transcript append     six gates passed: ASCII clean, prior 1,590,311-byte prefix retained
                      byte-identical under its own SHA-256, header unique at line 25,405
                      after the 25,404-line boundary, Claude physically last, +218 / −0
FITS 0 | CHECKPOINTS 0 | PLAN ARTIFACTS 0 | GENERATION 0 | ROLLOUTS 0
REAL-DATA TOUCHES     zero of every kind. No manifest, no .npz, no checkpoint, no
                      regeneration, and no read of a tracked results file.
                      PILOT / VAL / TEST: 0. Lifetime rollout total stays 278.
```

Every plan artifact and synthetic checkpoint this session produced lives under a pytest temporary
directory or a `tempfile.TemporaryDirectory`. Plan mode has still never been run into the packet.

---

## Cross-review

I read Codex's `HumanReport92.md` in full and the work it points to — the reviewer edits to both
files, and its Session 92 turn in the Phase 2 transcript. Its account is accurate against the
repository: the blobs, digests, line counts and deltas it reports all check out, and the two
adversarial reproductions it recorded (`C10_DUPLICATE_ACCEPTED`, `REFUSAL_UUID_MATCH False`) I
reproduced independently before its repairs and confirmed refused after them.

One thing I want on the record in Codex's favour, since this thread has mostly recorded the
opposite direction: its judgment not to extend my 36/36 mutation number to its own edited bytes
was correct and is the right general rule. A mutation score belongs to the exact state it was
measured on, and inheriting it across an edit is how a stale measurement becomes a false claim.

---

## Next steps

1. **Codex owner-reviews module blob `9a1d11a7…` and test blob `2a043f99…`.** If it approves those
   exact bytes, the executable review loop closes.
2. Only then: **one deterministic zero-fit plan run**, reviewed as its own artifact.
3. The two equivalence fits and forty curve fits need a **later, separate joint authorization**
   naming the approved plan's digest.
4. The read-only analysis script the design requires is a separate build after the executable's
   loop closes.
5. Still blocked and unchanged: any pilot / validation / test read, any threshold, any capacity
   selection, Stage 2, the final `config/config.json`, any generation, and every rollout.

— Claude
