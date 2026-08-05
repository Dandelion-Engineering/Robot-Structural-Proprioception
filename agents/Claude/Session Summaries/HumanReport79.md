# Claude — Human Report, Session 79

**Date and time:** 2026-08-05 12:33 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.

---

## Summary

This session was an owner re-review, and it did what an owner re-review is for. Codex
reviewed the development-only fitting contract I submitted in Session 78, found four real
defects, repaired them, and handed the repaired bytes back for my genuine re-review. I
reproduced all four of its findings against my own blob before touching anything, kept
every line of its repair, and then found **two behavioural defects sitting one layer below
two of those repairs**, plus **four guards — two of Codex's, two of my own — that no test
could make fail**. I fixed all six, added nine tests, and returned a state I explicitly
approve. The loop stays open; Codex owns the next turn.

I deliberately did **not** build the trainer this session, which was the next item in
Codex's sequencing and is gated on this loop closing.

No model was trained. No checkpoint, result or dataset was written. **No real data was
read at all this session** — not even the manifest. Zero rollouts.

## 1. What the review found

### The four findings I was handed, all reproduced

I drove both blobs in a single process — mine written out of git by `cat-file` into the
package so its relative imports resolve, then deleted — because a claim and its
demonstration are separate artifacts and a reviewer's finding reached by reading is not the
same evidence as one reached by running.

| State | My Session-78 blob | Codex's repair |
|---|---|---|
| duplicate `(C1,0)` appended to the exact ten-fit plan | accepted | refused |
| empty caller-built row batch | accepted | refused |
| `dev/C0` caller-built batch | accepted | refused |
| `dev/C1` rows for a nominal `S` fit | could not express the check | refused |
| data root name containing a newline | accepted | refused |
| census sentence, 1 selected + 1 withheld dev row | "1 withheld as non-dev" | "0 non-dev, 1 unmatched-suite dev" |

All four are real and all four repairs close the state they were written for. I contested
nothing.

### Finding A — the repair does not deliver the property it was written for

Codex's fourth finding was that a newline in the data root name turns the record's promised
single traceable line into two lines. The diagnosis is exact. The repair refuses ASCII
control characters — and Python's own definition of a line boundary is wider than ASCII.

I enumerated **every codepoint**: 1,112,064 of them (surrogates excluded). Three values
were accepted as bare names and still split the record into two lines — `U+0085` NEL,
`U+2028` LINE SEPARATOR, `U+2029` PARAGRAPH SEPARATOR. None is exotic; a directory name may
legally contain any of them on either host, and this field is read from a real directory.

The fix is not a fourth character added to a list. The routine exists to make a promise
true, so it now **ends by asserting that promise** — the value must be a single line by
Python's own reckoning. That covers the three, covers the seven ASCII boundaries the
control rule already caught, and covers whatever a future interpreter decides is a line
boundary. After the repair the count is **zero**.

Both rules are kept, and I checked that neither is decoration: `\t` and `\x7f` are
single-line values only the control rule refuses; `U+2028` is a control-free value only the
single-line rule refuses. A test drives each direction.

### Finding B — two guards in one module disagreed about what a training seed is

The completed-fit plan decides membership by set equality over tuples. Python's equality
does not agree with this module's own idea of a seed: `("C1", True) == ("C1", 1)` with an
equal hash, and `("S", 4.0) == ("S", 4)`. Measured: the ten-fit plan with a bool substituted
for the integer `1`, and with a float substituted for `4`, were both **certified as complete
matched plans** — while the module's seed check refuses a bool outright and says so in its
message. An unhashable entry, meanwhile, died inside `set()` with a foreign `TypeError`
rather than this module's own refusal.

The consequence is small; the disagreement is not. A contract that says two things about
one quantity is the shape that reaches a write-up unnoticed. Closed by checking each entry's
shape before the set arithmetic — deliberately shape only, not membership, so the "outside
the predeclared plan" branch that Codex's own test drives stays reachable.

### Four guards nothing could make fail

The mutation sweep against Codex's returned state found four survivors. Three are coverage
rather than broken behaviour, and I said so plainly rather than letting a count speak:

- Codex's control rule could drop its `DEL` half — no test drove `DEL`.
- Codex's expected-suite validation could be deleted — every test passed a real suite.
- **My own** requested-suite validation in the selector could be deleted — nothing ever
  asked for an unauthorized suite.
- **My own** authority check could be weakened from equality to containment and the whole
  suite stayed green. This is the one I would not have found by reading: a containment test
  accepts a record that has wrapped the mandated authority string in text of its own,
  including text that contradicts it, while passing every other check in the file. The
  contract's fourth bound says the checkpoint carries the *exact* authority.

## 2. A harness fault of my own, and it is new

My first sweep reported four **bad anchors** — patterns that matched nothing. The cause:
the file is **mixed-EOL**, 401 Windows line endings and 65 Unix ones, because the two agents
write different conventions into one working tree. Session 78's harness rule — encode each
pattern in the target file's own newline convention — *assumes the file has one*. Every
multi-line pattern spanning the boundary failed silently.

It cost nothing only because the harness reports an absent anchor as a **failure and never
as a skip**. Had it skipped them, four cases would have dropped out of a sweep I then quoted
as complete. The anchor is now a pattern accepting either convention at every line break.
I am recording this as a property of how we work rather than an accident of one file: my
resume notes already carry the same warning about the shared chat transcript, and this is
the second file where it bites.

## 3. Decisions I made, and the reasoning

**I blocked rather than approved.** Codex had just been right about four things, which is
exactly the condition under which its repair is hardest to review honestly. This is now the
fifth consecutive round in this project where the next defect lived one layer below the
repair that had just landed — it is no longer a coincidence, it is where I look first.

**I kept every line of the repair.** The diff is pure insertion — `+57/−0` and `+141/−0`,
zero deletions — so nothing of Codex's work was quietly rewritten while I added to it.

**I did not build the trainer.** Codex's sequencing puts it after this loop closes, and I
followed that rather than deviating. Two reasons beyond deference: it would have been built
against bytes I was in the middle of contesting, and reviewing a trainer in the same turn as
the contract that grounds it merges two loops that are cleaner apart. I named in the chat
exactly what I will build the moment the loop closes, so no design work is lost.

**I left two of Codex's weak test assertions alone and said so in the open** rather than
editing them quietly. They match a word that appears at two different refusal sites; they
pass and they are not wrong. I added assertions on the phrase unique to each site beside
them. Silently tightening a reviewer's test is how a disagreement gets buried instead of
settled.

## 4. Verification

```text
both-blob probe          5 cases x 2 blobs in one process; all four findings reproduced
codepoint enumeration    1,112,064 enumerated; 3 leaks before the fix, 0 after
mutation sweep           52 cases | 52 CAUGHT | 0 survivors | 0 bad anchors
                         both passes identical | restore byte-IDENTICAL
                         (Codex's state under the same sweep: 41 caught, 4 survivors)
focused suite            67 passed (was 58); under python -O, 67 passed
FULL PACKET SUITE        1,441 passed in 126.39 s (Codex's 1,432 + 9; no regressions)
compileall               clean
real-data touches        NONE — no manifest read, no .npz opened
fits / checkpoints / generation    0 / 0 / 0
config/config.json       absent
physical rollouts        0
```

Transcript integrity: the Phase-2 transcript was 1,343,389 bytes / 21,045 lines before my
append. Five assertions passed inside the writer — the prior bytes survive as a
byte-identical prefix under their own SHA-256, my header occurs exactly once, it occurs
after the recorded boundary, Claude is physically last — and the Git diff is `+171/−0`.
I also verified Codex's Session-78 append at the Git level: `+108/−0`, header unique,
correct chronological order. No violation, so no monitoring-chat entry was needed.

The public Live-Run README heartbeat check ran and the log was **deliberately left
untouched**: nothing finished this session. The contract loop is open and the model is still
untrained. Logging an unreviewed module would be logging work in progress, which that log
is explicitly not for.

## 5. Files created or updated

- `Reproducibility Packet/scripts/utils/dev_fit_contract.py` — the single-line
  post-condition and the plan-entry shape check, with both measurements written into the
  docstrings (blob `2448ad4d`)
- `Reproducibility Packet/tests/test_dev_fit_contract.py` — nine tests: the derived
  line-boundary universe, the two-rules-each-live pair, the seed-type agreement, malformed
  plan entries, the expected-suite validation, the unique-phrase suite refusals, the
  selector's suite validation, authority equality-not-containment, and the record's
  single-line property (blob `2aa5f762`)
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — my Session-79 turn: the reproduction table, both findings, the sweep, the harness fault,
  and the explicit approval of my returned state
- `agents/Claude/Session Summaries/HumanReport79.md` — this report
- `agents/Claude/README.md` — workspace index refreshed
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for the next session

## 6. Next steps

1. **Codex owns the next turn**: genuinely re-review `2448ad4d` / `2aa5f762` and either
   approve those exact bytes or edit and hand back.
2. **When that loop closes, I build the trainer** against the approved contract — the
   deterministic-precision context around both the forward and backward pass, the ten
   predeclared `(suite, seed)` arms, the row check at the point of consumption, and one
   provenance record per checkpoint.
3. **No development fit may run** before the trainer's own review closes, and any fit is
   limited to the already-delivered 304-row development partition.
4. Pilot, validation, test, the final `config.json` freeze, new data generation and all
   confirmatory work remain blocked behind their own later decisions.
5. My next regular progress report is **Session 80**.

## 7. One honest note about the shape of this session

This session moved a contract module, not a result. The measurement that would answer the
project's question still has not run, and my recent sessions have been instrument and
contract work rather than measurement — I am deliberately not attaching a precise count to
that, because a historical figure quoted from memory is exactly the kind of claim this
project has already had to retract once. What is measured is this session: zero rollouts,
no data read, no model trained.

What I would say in its defence is narrower than "review is valuable". It is this: every
round of this loop, including this one, has found something a reader could check and would
have cared about. The authority check that could be weakened to containment would have let a
development-only checkpoint carry a note *contradicting* its own authority into a
downstream artifact. That is the failure this project exists to avoid — a number that looks
finished and is not. The question I keep asking is whether the next round will still be
buying that, and the honest answer is that when a round finds only coverage and no
behaviour, it is time to close, not to hunt for one more.
