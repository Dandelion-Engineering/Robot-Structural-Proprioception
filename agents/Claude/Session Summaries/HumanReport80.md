# Claude — Human Report, Session 80

**Date and time:** 2026-08-05 16:28 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278.**
**Progress-report session:** yes — `agents/Claude/Progress Reports/Progress Report Session 80.md` (covers S73–S80), written in addition to the session's normal work.

---

## Summary

This session was my owner re-review of Codex's Session-79 repair of the development-only
fitting contract, plus my regular progress report.

**Both of Codex's findings are real, I reproduced both against my own superseded blob, and
I kept every predicate and every message of both repairs unchanged.** I did not approve its
exact bytes, because I found one further defect — but I want the shape of that stated
precisely, because it is different from the last five rounds: **Codex's repair is complete
for the thing it repaired.** Measured over 110 hostile-input cells, `DevFitProvenance.
validate()` now has zero foreign exceptions and zero silent accepts. What I found is one
function over, not one layer below.

I edited only this module and its tests and explicitly approved:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py   9d6ecfea816833678fdfa667e956539d75e11ade
Reproducibility Packet/tests/test_dev_fit_contract.py      d4202c8ea07bed623b4515cd39d9b51a4b470199
```

The loop is **open** and Codex owns the turn. No model was fit, no checkpoint written, no
trainer built, no real data read, no rollout spent, and `config.json` remains absent.

## What I did with Codex's two findings

I extracted my own superseded blob (`2448ad4d`) out of git into the package and drove
**both blobs in one process**, so the reproduction was a measurement rather than a
re-telling. All eight of Codex's constructed cases reproduced exactly:

```text
                                    MY 2448ad4d        CODEX 872c6b12
manifest_sha256   = 64hex + LF      ACCEPTED           refused, in-domain
config_hash       = dev-64hex + LF  ACCEPTED           refused, in-domain
checkpoint_sha256 = 64hex + LF      ACCEPTED           refused, in-domain
code digest       = 64hex + LF      ACCEPTED           refused, in-domain
manifest_sha256   = None            TypeError          refused, in-domain
checkpoint_sha256 = None            TypeError          refused, in-domain
code_identity     = list            AttributeError     refused, in-domain
row_disclosure    = None            AttributeError     refused, in-domain
control: well-formed record         accepted           accepted
```

Codex's Finding C is the better of the two and worth recording in plain terms: Python's
`$` anchor may match immediately *before* a final newline, so four fields whose error
messages promise an exact 64-character digest were accepting 65-character, two-line values.
Those are the identities by which a later reader decides which manifest, configuration,
checkpoint and training code a development artifact actually names.

I also checked the one thing its repair made load-bearing: dropping the `^...$` anchors from
the compiled patterns is safe **only** because every call site now uses `fullmatch`. I swept
`fullmatch → match` and `fullmatch → search` at each site; Codex's own new terminal-newline
cases catch all six. The choice is guarded, not merely correct.

## Finding E — the producer silently returns the value the consumer refuses

Codex's Finding D was a *family*: four fields escaping below the module's own exception
boundary. Session 79 taught me to ask what a family is standing in for, and the property
behind this one is stated in Codex's own report — the module defines `DevFitContractError`
so that a fitting-bound violation fails in its own domain. That is a property of the
**module**, not of four fields.

So I enumerated the module: every public entry point crossed with a battery of hostile
values, 140 cells, reporting **both** failure modes rather than only the one I went looking
for. That last clause is the finding's whole provenance — my first version of the probe
printed foreign exceptions only and could not have seen what follows.

```text
BEFORE (Codex 872c6b12)  140 cells | 74 in-domain refusals | 65 FOREIGN | 1 SILENT ACCEPT
AFTER  (mine 9d6ecfea)   140 cells | 100 in-domain refusals | 40 FOREIGN | 0 SILENT ACCEPTS
```

The single silent accept:

```text
code_identity({})                    -> returns {} with NO refusal
DevFitProvenance(code_identity={})   -> "code_identity must name at least the module
                                        that defines the network"
```

The routine that **builds** bound 4's code identity hands back, without a word, the exact
mapping the routine that **audits** it refuses one step later — and the refusal, when it
comes, names the record rather than the call that built it. Everything else about the two
already agreed; I checked, and the label rule and the digest rule were identical in both
places. Only the non-empty rule disagreed.

This is the second time in two sessions that this module has had two guards disagreeing
about one quantity, and both were found the same way: **call both guards on the same value
and compare what they say.** Neither was reachable by reading.

## The repair, and why it is not another matching block

Copying the record's check into the producer closes the instance and leaves two copies of
one rule — which is how these two got out of step in the first place. Instead the rule now
exists **once**, as `require_code_identity`, and both the producer and the consumer call it.
`code_identity()` ends by asserting it as a post-condition, so it cannot hand back a mapping
the record will refuse.

Two smaller repairs travelled with it, both non-vacuous and both swept: `code_identity()`
refuses a non-`Mapping` in its own domain rather than dying in `paths.items()`, and a
non-path **value** now reaches a refusal instead of dying inside `Path()` — `Path(None)`
raises `TypeError` one line *before* the `is_file` guard that exists precisely to refuse a
bad path, so the guard written for the case could never see the most likely instance of it.

## What the sweep caught in my own repair

Adding the post-condition made the in-loop `require_bare_name(label, ...)` redundant:
`require_code_identity` refuses the same label with the same sentence, so deleting the
in-loop copy left the entire focused suite green. **The mutation sweep reported it as a
survivor, which is the only reason I know.** I removed the copy rather than keep it beside a
double-removal sweep case, and the label rule is now swept where it actually lives.

Sixth consecutive round in which something sat one layer below the repair that had just
landed. This time it was below mine.

## What I deliberately did not close, and handed to Codex

Forty foreign escapes remain, all in `require_dev_only`, `select_dev_rows` and
`require_complete_matched_plan`, all of one kind: a caller passes a non-iterable or a list
of the wrong element type and gets `TypeError`/`AttributeError` rather than
`DevFitContractError`.

I left them, and the measurement is the reason: **none of them is permeable.** Every one is
a loud crash, and after this session no bound anywhere in the module is passable by any
value in the battery. Converting loud-in-the-wrong-domain into loud-in-the-right-domain is
decoration unless something depends on the domain, and nothing yet does.

That choice favours me — it is less work — so I measured it, said so in the chat, and handed
Codex the decision rather than taking it. If it wants the module total I will close them
without re-arguing.

## Verification

```text
both-blob probe        8 cases x 2 blobs in ONE process (mine written out of git by
                       cat-file into the package, then DELETED).  8/8 reproduced.
entry-point grid       140 cells, BOTH failure modes reported.  1 silent accept -> 0.
validate() grid        10 fields x 11 values = 110 cells; 0 escapes, 0 accepts, unchanged
                       from Codex's state to mine.
mutation sweep         42 cases | 42 CAUGHT | 0 survivors | 0 bad anchors | both passes
                       identical | restore byte-IDENTICAL.  Case list REBUILT against the
                       edited bytes; the first run of the old list reported 2 bad anchors
                       and 1 survivor, all three real, none of them silently skipped.
focused suite          test_dev_fit_contract.py 92 (was 77); under `python -O` 92 passed
FULL PACKET SUITE      1,466 passed in 128.41 s (Codex's 1,451 + 15, no regressions)
compileall             clean
diff vs Codex's state  source +71/-13 (every deletion a relocation of Codex's own
                       predicates, or the redundant label copy); tests +48/-0
diff --check           clean
transcript append      +169/-0, five assertions passed, header unique at line 21,320
REAL-DATA TOUCHES      NONE.  No manifest read, no .npz opened, no checkpoint written.
FITS / CHECKPOINTS     0 / 0     generation 0     config/config.json absent
ROLLOUTS THIS SESSION  0
```

## Cross-review and transcript monitoring

I read Codex's `HumanReport79.md` and its Phase-2 turn, and both of its findings became the
first thing I reproduced. Its Session-79 transcript append is clean at every level I can
check: the prior blob is an exact byte prefix of the new one under its own SHA-256,
`+100/−0`, its header unique at line 21,220 and physically last, and the last five turns in
correct chronological order (06:13 → 09:05 → 10:12 → 12:32 → 14:10). **No recurrence, so
nothing was added to the monitoring chat** — the duty there is to flag recurrences.

## Live-Run README

Heartbeat check ran; **README deliberately unchanged.** Nothing finished this session — the
contract loop is open and the model is still untrained — and an open review round is work in
progress, which the running log is explicitly not for. The banner is already current
(Phase 2 / In Progress / 2026-08-05).

## Files created or updated

- `Reproducibility Packet/scripts/utils/dev_fit_contract.py` — the shared
  `require_code_identity` rule, the producer's post-condition, and two in-domain refusals.
- `Reproducibility Packet/tests/test_dev_fit_contract.py` — 15 cases: the producer/consumer
  agreement test, the empty-mapping post-condition, six non-mapping cases and seven
  non-path-value cases.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — append-only
  Session-80 review, approval of my own returned state, and handback.
- `agents/Claude/Progress Reports/Progress Report Session 80.md` — the regular progress
  report, covering S73–S80.
- `agents/Claude/Session Summaries/HumanReport80.md` — this report.
- `agents/Claude/README.md` — workspace index refreshed.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten. **A byte-level
  note so a future diff does not look alarming:** git will report this file as
  `+1242/−1177`, i.e. every line changed. It is a line-ending artifact, not a rewrite. The
  committed blob carried CRLF throughout; my rewrite passes through git's clean filter as
  LF, so every line differs at the blob level and this one commit converts the whole file.
  **The real content change, measured after normalising both sides to LF, is `+174/−109`**,
  and the spliced tail was asserted byte-identical at the moment it was written. Nothing was
  lost. This is the same mechanism Codex recorded on the monitoring thread for the
  transcript in its Session 73.

  While rewriting it I also found and corrected a **stale status clause in my own summary**:
  one line said the Session-64 progress report's review loop was OPEN with Codex owing the
  turn, while the Pointers section of the same file said it was CLOSED. The Pointers version
  is right — Codex approved blob `b0ff7496` in its Session 65 (`HumanReport65.md:81-82`),
  which I checked against its primary record rather than trusting either half of my own
  file. The claim had been carried through five consecutive rewrites. It is Lesson 65
  exactly, arriving inside the document whose whole job is to be true, and it surfaced
  because I grepped the file for status words instead of reading it.

## Next steps

1. Codex re-opens and genuinely reviews `9d6ecfea` / `d4202c8e`, and rules on whether the
   remaining forty caller-type escapes should be closed.
2. If it approves them unchanged, the development-fit contract loop closes.
3. **I then build the trainer** — the ten-arm dev fit, its checkpoint writer and its
   provenance record — and hand its exact executable state over *before* any fit runs.
4. No fit may run until the trainer's own review closes. An open loop is not permission, and
   a closed contract loop is not permission either.

The central research measurement still has not run. This session improved the integrity of
the development-only training boundary; it produced no evidence about the hypothesis.
