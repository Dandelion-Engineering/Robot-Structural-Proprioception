# Claude — Human Report, Session 96

**Date and time:** 2026-08-08 08:31 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Plan artifacts added to the packet: 0. Data generated: 0. Pilot / validation / test reads: 0.** No plan mode was run at all this session. The full packet test suite reads two approved development documents (`dev_fit_result.json`, `dev_fit_analysis.json`) through its fixtures; no delivered observation payload and no approved `.pt` checkpoint was opened. Every write my mutation harness made was to the sweep module itself, restored in a `finally` with the restoration verified by digest.

**Progress-report session:** **yes** — this is my regular session-96 report, covering my Sessions 89–96. It is written in addition to the normal session work at `agents/Claude/Progress Reports/Progress Report Session 96.md`. No phase transition and no Claim-Sheet amendment occurred.

---

## Summary in one paragraph

Codex ruled my Session-95 finding AT in, implemented the sibling analyzer check I had
recommended, and handed back two blobs for genuine re-review. I opened both, drove the repair
rather than reading it, and **approved `capacity_sweep.py` at `61d4fb97` unchanged** — the
executable's loop is closed at a state both agents name. I contested nothing. An eight-case
mutation sweep over the repair found **two coverage gaps**, neither of them a live defect: the
digest-shape guard was deletable in silence, and the choice of the *text* hashing domain over
the raw one was unpinned — and that second one fails only on the fresh clone the
Reproducibility Packet exists to serve, which no test running in this tree can see. I closed
both **with tests only, changing no production line**, so my edit cannot move a byte of the
plan the next session must regenerate. The test file is returned at `8e97f6a9` for Codex's
approval.

---

## What I approved, and what I checked before approving it

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  blob 61d4fb97c2d87606134cbf0a1e1c4458e4997cd6
  canonical/raw d91db2effbdc05001eebd3838eee19852f4fd7b4e90f684543f224a1e45f821e
  96,715 B / 2,259 lines / LF / no BOM
  *** APPROVED UNCHANGED.  Codex had already approved these bytes, so both approvals name
      the same state and the EXECUTABLE loop is CLOSED. ***
```

The diff from my Session-94 state is +43 lines in one function plus one call site. I did not
take any of it on trust:

1. **The guard sits above every spend.** Read at source rather than inferred: in
   `_execute_mode`, `require_authorized_plan` is called before `claim_run_root`, before
   `load_dev_examples`, and before either fit loop; `require_authorized_plan` rebuilds
   `plan_document()` and requires exact equality, so the analyzer comparison runs at the
   planning boundary and again at the authorization boundary. There is no second entry into
   execute mode that bypasses it.
2. **The hashing domain agrees structurally, not coincidentally.** Codex's guard calls
   `code_identity`, and `analyze_dev_fit.analysis_code_identity()` — the function that
   produced the recorded `4caa2938…` — calls the *same* `code_identity` out of the same
   `dev_fit_contract`. One definition consumed twice, not two copies that currently agree.
   That distinction is precisely what separated this from finding AS, and it is why I did not
   raise AS again here.
3. **C3's cardinality is untouched and the import surface is now completely bound.** I
   enumerated the sweep's project-local imports: `attribution_net`, `dev_fit_contract`,
   `dev_fit_trainer`, `protocol_p`, `analyze_dev_fit`. Three are inside the eight C3 compares
   entry-by-entry against the approved ledger; `capacity_sweep.py` is the one permitted
   addition; `analyze_dev_fit.py` is now covered by the sibling check. **`protocol_p.py` is
   the one project module in neither set** — recorded, not raised, because it neither fits nor
   scores an arm (which is what design section 7.1's binding requirement names) and because
   it is covered twice anyway: a pre-plan change to `canonical_text_sha256` moves every
   recorded digest and C3 refuses, and a post-plan change to `canonical_json` makes the
   rebuilt plan differ from the stored one and the equality check refuses.

## The thing I went looking for and decided is NOT a finding

The approved analysis artifact carries nine identity entries; eight are the same labels the
ledger carries; nothing in the executable compares those two eights. **I measured them: no
disagreement, all eight byte-identical.**

I did not ask for a guard, and the reason is the distinction AT itself turned on. **AT was
live** — the plan's bytes could stay identical while an unbound file on disk moved underneath
them. **This is two frozen documents whose exact canonical digests the plan already binds** as
`approved_analysis_sha256` and `approved_fit_ledger_sha256`. Given those bytes the property is
fixed, and a property of bound bytes that has been measured once does not also need a runtime
check. Adding one would be the cargo-cult version of AT — the ritual of the previous finding
applied where its mechanism does not exist. I stated that reasoning in the chat so Codex can
overrule the reasoning and not only the code.

## What the mutation sweep found

Eight mutations of `capacity_sweep.py`, the focused suite run per case, original restored in a
`finally` and the restoration verified by digest. Against Codex's 207 tests: **six caught, two
survived, both negative controls surviving** (so the harness is not simply reporting red).

```text
M1  delete the plan_document() guard call            CAUGHT (1 test)
M2  neuter the comparison to `or True`               CAUGHT (2 tests)
M3  delete the isinstance/hex64 shape guard          *** SURVIVED all 207 ***
M4  hash dev_fit_trainer instead of the analyzer     CAUGHT (17 failed, 13 errors)
M5  swap code_identity() for a raw sha256            *** SURVIVED all 207 ***
M6  point the field path at dev_fit_trainer.py       CAUGHT (17 failed, 13 errors)
NC1 reword one docstring word                        survived (control)
NC2 rename a local variable                          survived (control)
```

**M3 is a message defect, not a hole.** The value comparison one line below refuses every
malformed record anyway, so nothing gets through. What is lost is that the operator is told
the analyzer *moved* when in fact the artifact's own ledger is *unreadable* — and the guard
that distinguishes those two is deletable in silence. Requirement (s) says drive the gate and
assert the REASON; six parametrized cases now do, including the correct digest upper-cased,
which a value check alone still refuses but with the wrong sentence.

**M5 is the one worth the session.** Codex chose the text domain and that choice is correct;
nothing pinned it. Measured this session:

```text
git check-attr text eol -- .../analyze_dev_fit.py     both UNSPECIFIED
git config core.autocrlf                              true
analyze_dev_fit.py in this working tree               0 CRLF pairs, 634 LF
  raw == canonical                                    4caa2938…   <- why M5 survives here
the same module materialized with CRLF (a fresh clone)
  canonical                                           4caa2938…   unchanged
  raw                                                 3e06846a…   DIFFERENT
```

The root `.gitattributes` states in its own comment that this repository is developed with
`core.autocrlf=true` and that an unpinned text file materializes as CRLF in a fresh clone;
`.py` files are not pinned. So a raw-domain guard passes here and **refuses a legitimate plan
on the Windows clone the Reproducibility Packet exists to serve** — the one environment no
test that only ever runs in this tree can see. The new test writes a CRLF materialization into
`tmp_path`, points `__file__` at it, asserts the guard accepts it, and asserts up front that
the two byte-strings actually differ so the case cannot go inert if this tree's line endings
ever change.

Re-swept after the additions: **8 / 8, both controls still surviving, production digest
`d91db2ef…` unchanged before and after.**

## Why tests only

The plan's `code_identity` binds `capacity_sweep.py`; it does not bind the test file. Editing
tests therefore **cannot** move the plan's bytes, while any production edit would have
invalidated the regeneration the next session has to do. That asymmetry is what made adding
two tests cheap here and what made me refuse to touch production for a message improvement. It
is the same reasoning as lesson 142, applied in the direction that says *don't* edit.

```text
Reproducibility Packet/tests/test_capacity_sweep.py
  blob 8e97f6a94a3c5ac12e6ac85376913c9104424725
  canonical/raw 61f700fb4b6c51df495cdfca1c0fa0b5aacb3d9021c0c04e3cee2a72746b99e0
  86,984 B / 2,121 lines / LF / no BOM / pure ASCII / 214 tests / +59 / -0
  *** RETURNED FOR CODEX'S APPROVAL — the loop is open on this file only. ***
```

## Sequencing: why I did not re-plan

Codex set the order — close the executable review at the same state, then one zero-fit re-plan
at `stage1-run-1`, then a fresh two-agent review of the plan's exact bytes, then a *separate*
joint authorization for the 42 fits. I did not re-plan inside a session that returned an open
test blob. I told Codex in the chat that because `capacity_sweep.py` is byte-identical to what
it approved, approving `8e97f6a9` unchanged lets the re-plan follow immediately, including in
that same session.

## Verification

```text
FULL PACKET SUITE   1,765 passed in 164.10 s   (1,758 + the 7 I added)
FOCUSED ROUTE A     214 passed;  214 passed again under python -O
MUTATION SWEEP      8 cases, 8/8 matching expectation, 2 negative controls surviving,
                    restore verified by digest inside a finally
compileall          clean.   git diff --check   clean
PRODUCTION BLOBS    capacity_sweep 61d4fb97, design b45efa47, analyze_dev_fit 31381b18,
                    dev_fit_trainer caa00418, dev_fit_contract bd2c0d08,
                    attribution_net c4fa3c63, plan d2584d28: ALL UNCHANGED
PACKET ARTIFACTS    ONE capacity_sweep_plan.json, still the superseded d2584d28.  NO result,
                    NO equivalence, NO .pt outside results/dev_fit.  config/config.json
                    still ABSENT.
FITS 0 | CHECKPOINTS 0 | GENERATION 0 | ROLLOUTS 0 | NEW PLAN ARTIFACTS 0
REAL DATA           zero beyond the suite's two tracked fixtures.  PILOT / VAL / TEST: 0.
                    LIFETIME PROTOCOL-P ROLLOUTS UNCHANGED AT 278.
TIMESTAMP           read from the shell clock immediately before the transcript write.
```

## Transcript hard gate

```text
pre-write bytes       1,645,051
pre-write lines       26,391
pre-write SHA-256     fa7705076769614eb697d2ff25fd140d38deb69e7b511d918bb4841010b6ca67
                      *** EQUALS the digest Codex published at the end of its S95, which
                          independently confirms the transcript was untouched between
                          sessions. ***
appended bytes        9,235   (pure ASCII, LF only)
post-write bytes      1,654,286
post-write lines      26,544
post-write SHA-256    57e4c67e70d22b494d5aef5f4cdfd5bef043bbbfced18878b64d5b319a37b87d
header unique at      line 26,393, after the 26,391-line boundary
prefix retained       byte-identical under fa770507…
physically last       Claude
Git level             +153 / -0, one tail hunk
```

**One honest note on my own writer.** Its gate 5 — "this agent is physically last" — compared
the stripped tail against `-- Claude`, but this transcript's convention ends every turn with a
`---` separator *after* the signature, so the gate reported FATAL on a correct append that had
already been written. Gates 1–4 and 6 had passed inside the writer against the real on-disk
bytes; I verified all six by hand afterwards rather than re-appending, which would have
duplicated the message. **The lesson is narrow and worth keeping: a gate written against a
remembered file convention will fire on the convention rather than on the condition, and a
writer whose checks run *after* the write must be safe to fail — mine was, but only by
accident of ordering.** No content was lost, nothing was written twice, and the file's CRLF
count is unchanged at 19,456.

## Cross-review

I read Codex's `HumanReport95.md` in full, its Session-95 chat turn, and the two blobs it
returned. Its report is accurate against everything I independently checked: the diff is what
it describes, the guard is where it says, the old plan is refused with the message it quotes,
and the plan artifact is untouched at `d2584d28`. I confirmed rather than assumed its claim
that deleting the `plan_document()` call makes the post-plan test fail — that is my M1, and it
does. I also confirm its acceptance of my Session-95 invocation correction. Nothing in its
report needed a correction carried forward, so no review cycle opened on it beyond the
artifact loop already running.

I read the four concluded chat summaries and the `Transcript Order Monitoring` active thread.
No reply is owed there: Codex recorded no recurrence in its Session 95, and the thread's last
turn is mine from Session 83.

## Files created or updated

Created:

- `agents/Claude/Session Summaries/HumanReport96.md` — this report.
- `agents/Claude/Progress Reports/Progress Report Session 96.md` — the regular session-96
  progress report, covering my Sessions 89–96, at the Accessible-Piece bar.

Updated:

- `Reproducibility Packet/tests/test_capacity_sweep.py` — two tests added (+59 / −0), one of
  them parametrized six ways. No production line touched.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — append-only
  approval of the executable, the two coverage findings, and the handoff.
- `README.md` (root, Live-Run) — one running-log entry. The previous entry announced a plan
  awaiting a second review; that plan is now superseded, and the log is append-only, so the
  correction propagates forward as a new dated entry rather than editing the old one.
- `agents/Claude/README.md` — navigation and the Session-96 entry.
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py` — approved at `61d4fb97`.
- `Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json` — the superseded
  plan, preserved as the visible state that produced AT. Regeneration is the next session's
  act, not mine.
- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` — frozen design, verified
  untouched at `b45efa47` by the module's own `design_digest()` check.
- `director_requests.md` — no new director-only blocker. Entry 1 remains open and
  non-blocking.
- `.gitignore` files — reviewed against this session's diff; the session lock, environments,
  caches and generated payloads are already covered. No update required.

## Decisions I made this session

1. **Approve the executable unchanged rather than fold my two findings into it.** Neither
   finding is a live defect, and a production edit would have invalidated the re-plan. Tests
   were the whole cost.
2. **Do not raise the analysis-vs-ledger eight.** Measured identical, and structurally
   unnecessary because both documents' exact bytes are already bound. Stated the reasoning
   out loud so it can be overruled.
3. **Record `protocol_p.py` as out of section 7.1's scope rather than raise it.** It neither
   fits nor scores an arm, and both directions of change are already refused elsewhere.
4. **Do not re-plan.** Codex's ordering is right and the sequencing call is its own.
5. **Correct a twenty-three-session self-contradiction in my own summary rather than carry it
   again.** While running the obligation grep I now prescribe as lesson 151, I found that the
   payload-boundary extension's pointer has read *"CODEX OWES THE SECOND READ"* through **every
   rewrite from S73 to S95**, while the Order line in the same file records that Codex
   completed that read in its Session 72 and that Step 5 has since run to completion and been
   jointly approved. Nothing was blocked by it — the extension is fully spent — but a future
   session reading only the pointers would have believed a review was outstanding. Fixed, with
   the history of the error kept in place. **The mechanism is worth more than the fix: a status
   clause about what the *other* agent owes is the one most likely to rot, because nothing in
   my own work ever forces me back to it.** That is lesson 151, and it is the third time
   (S80, S93, S96) that grepping my own summary found something reading it did not.
6. **Append a Live-Run entry despite Codex declining one in its Session 95.** Its judgment was
   reasonable for a session that only reopened a review; mine is that the log's most recent
   entry now publicly describes a plan state that is no longer true, and an append-only log
   corrects that forward.

## Next steps

1. **Codex reviews `8e97f6a9` and explicitly approves or edits it.** If it approves unchanged,
   the pair closes at the same state.
2. **One zero-fit re-plan** at `stage1-run-1`, run from `Reproducibility Packet/scripts/` with
   `--output-dir ../results/capacity_sweep`, replacing the superseded artifact.
3. **Both agents independently review the regenerated plan's exact bytes.**
4. **Step 4 remains a separate joint authorization** naming that plan's digest. No fit may run
   before it exists.
5. **Then the C7 read-only analysis script**, which imports the section-5 pure functions that
   already exist in `capacity_sweep.py` rather than redefining them.
6. My next regular progress report is **Session 104**, unless a phase transition or an
   approved Claim-Sheet amendment fires sooner.

— Claude
