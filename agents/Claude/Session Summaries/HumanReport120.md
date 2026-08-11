# Claude — Human Report, Session 120

**Date and time:** 2026-08-11 10:12 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** **Yes.** This is my eighth session since Session 112, so the regular
cadence fired. `agents/Claude/Progress Reports/Progress Report Session 120.md` is written and
covers S113–S120. It is an addition to this session's work, not a replacement for it.

---

## Summary

Session 119 ended with the rung-2 analysis artifact handed to Codex for the step-7 exact-state
review, and with the interpretation gate untouched. Codex's Session 119 closed that review — it
ran its own 853-check standalone audit, found no defect, and explicitly approved the same bytes I
had approved. It then applied **its half** of the pre-registered section-5.4 interpretation and
stated plainly that mine remained open.

**This session paid the matching half, which closes section 5.4 jointly, and then wrote the
packet-runbook steps that ruling had been waiting on.** Concretely:

1. Re-opened the exact approved artifact and re-derived both interpretation conditions from its
   own primitives with a standalone probe — 40 checks — plus a ten-mutant calibration control.
2. Applied and explicitly approved the exact two frozen sentences. **Section 5.4 is now 2/2 and
   jointly closed.**
3. Wrote **Steps 30 and 31** into the reproducibility packet's runbook, plus two flagged
   factual corrections outside those steps, and handed the state to Codex for one review cycle.
4. Independently confirmed, at the byte level, the transcript-append fault Codex reported against
   itself, and posted that confirmation to the monitoring thread.
5. Wrote the regular progress report.

**Zero fits, zero checkpoints, zero rollouts, zero generation runs, zero non-development reads,
zero analyzer invocations, zero C7 invocations.**

---

## What I did, and why each piece was done the way it was

### 1. The section-5.4 half — re-derived, not recited

The gate's whole value is that both agents reach the same sentence pair independently. Reading a
label out of my own previous session, or accepting the one Codex quoted, would have made my half
a formality. So I re-opened the exact bytes and re-derived both conditions from primitives.

Artifact identity re-measured on disk this session and unchanged: blob
`a2fa857b7df14baefc047bf0b8b4b7a4d87c7b43`, raw SHA-256 `604d7272…6951c`, 40,270 bytes, zero LF,
zero CR, canonical ASCII.

The probe imports nothing from `analyze_rung2_escalation.py` and nothing from any project module.
The two checks that carry the weight are not reads:

- **The ordered status table was re-evaluated here, top to bottom, from primitives** — not read
  off the recorded status name. No equivalence arm is `FAIL` (both `PASS`, both bit-identical in
  weights *and* loss history, each refit checkpoint digest equal to its rung-1 reference); exactly
  ten rung-2 arms, all `COMPLETED`, one per (suite, seed) across five seeds; and every arm's
  `objective_reduced` re-derived from **that arm's own 20-epoch loss history**. Row 4 selects —
  the successful row. Only then did I compare against the artifact's own
  `OPTIMIZATION_CHECK_PASSED` and its three counters against my three counts.
- **The sign label was re-derived twice.** Each paired row's two sides checked to *be* the two
  arms' own `macro_f1` values; each raw difference recomputed as `S - C1`; each `quantized` string
  re-rendered from its own `raw` at six decimals under `ROUND_HALF_EVEN`; then the label derived
  from the counts alone. **Two negative, one zero, two positive — `MIXED`.** That is Codex's count
  exactly, reached independently.

I also drove the sentence pair against the frozen design rather than retyping it: each licensed
sentence must occur **verbatim in its own row and in no other row** of §5.4, and the forbidden-
connective list I check against is read out of §5.4 rather than remembered.

**The two sentences, applied and explicitly approved with nothing attached:**

> Slot 9's rung 2 is built and fitted; the ladder has more than one rung on it, and the
> development record contains one rung-2 fit at five seeds under the approved protocol.

> At rung 2, in-sample, the paired sign was not consistent across the five seeds.

### 2. The calibration control — and the defect it found in my own instrument

All 40 checks passed on the first run. That is a reason for suspicion rather than confidence: an
audit that passes first try has usually not been calibrated, because a second instrument is only
genuinely second if it can be wrong in its own way.

So I built a ten-mutant control — flipped status name, an equivalence `FAIL`, a dropped arm, an
arm whose objective does not reduce, all-negative differences, a substituted `sign_count`, a
substituted label, a paired side detached from its arm, a non-zero `healthy` F1, and one
**design-side** mutant rewording the licensed sign sentence in the frozen document.

**The first control run caught 9 of 10, and the survivor was a real defect in my probe.** Dropping
an arm made it exit non-zero by *raising* — printing nothing at all, discarding every check
already made, so the refusal was indistinguishable from a broken harness. A crash is not a check.
I made the check function print as it goes and guarded the arm lookup. Re-run: **10/10 caught by
the check that names them, unmutated control still green, whole sweep run twice with
byte-identical output.**

There is a smaller one worth recording too. My first path scan of the new README text flagged a
UNC path. It was my own regular expression under-escaped by one level — it was matching a single
backslash, not two. Measured with a `re.escape`-built pattern: zero matches, and the new text
contains no double backslash at all. I chased the flag instead of publishing it.

### 3. The packet-runbook edit — written, and handed over

Codex ruled in its S118 that this would be **one edit carrying two consecutive rung-2 steps**,
written after step 7 so the second step names a jointly reviewed state. Both preconditions were
met before I wrote a line of it.

`Reproducibility Packet/README.md`, blob `9a3a878c862fa0c28de574eec612531a52212dc9`, 118,161
bytes, `git diff --numstat` **+175 / −2**.

**Step 30 — the module, plan and completed run.** The architecture as a different *kind* of
network rather than a wider copy: 219,018 parameters and a stem receptive field of 31, against
rung 1's 39,594 and 1,023 — stated plainly, because the two rungs differ in capacity *and*
temporal reach at once, and that is the first reason nothing here compares them as points on a
curve. Frozen design digest, plan mode, execute mode, the same fail-closed clean-clone boundary
Step 28 carries, three tracked digests, `X_RUNG2_OK`, the 12/12/0/0/0 budget, 1,274.6 s. **The
cost finding got its own paragraph:** 5.5× the parameters, roughly 12× per step, because a GRU's
timesteps do not parallelize on CPU — on the hardware this project actually has, the
cheaper-looking axis of the ladder is not the cheaper axis to climb.

**Step 31 — the read against its pre-registered interpretation.** The nine-argument invocation,
the exclusive-create writer, the tracked digest, then the two licensed sentences quoted verbatim
with the forbidden connectives named. Then the degeneracy observation, under a heading that says
what it is for — *The part a reader must not be allowed to miss* — with all ten arms at F1 = 0 on
`healthy` and `structure`, the four arms at accuracy `0.631579` / macro `0.193548` named by suite
and seed, the 8/32/96/16 census that makes that the majority-class value, the six with a non-zero
`actuator` F1 and nothing else, and the ten anchors with four non-zero values each. Then exactly
three consequences and no more: both sides zero rather than equal; not a recording error (exact
re-score equality across twelve checkpoints); and not the failure path (none of §5.5's three
branches occurred). **No cause is attached.**

### 4. Three judgment calls, each flagged to Codex rather than buried

1. **I named `rung2_minus_rung1` and deliberately did not print its figures.** Step 29 prints its
   five per-point means because those numbers are the subject of the row that matched. Nothing
   licenses a sentence about this block, so printing two means whose only use is the comparison
   the design forbids would put the trap in the runbook and then ask the reader not to fall in it.
   The artifact is tracked; a reader who wants them opens it. I said in the handoff that if Codex
   reads that as under-disclosure rather than restraint, I will print them as record contents with
   the prohibition stated beside them.
2. **Two edits outside the two steps, and they are deviations from Codex's ruling.** The Step-28
   boundary section asserted *"There are 55 of them on the recorded machine"* over a table of every
   `.pt` the project has produced. After the rung-2 run that sentence is false — the packet result
   tree holds **67** — so I corrected the heading, the sentence and the table (+2 rows) and added
   one bullet noting the table is the packet-wide checkpoint boundary and that Step 31 inherits
   Step 29's limitation. I also added one paragraph to **Current boundary**, mirroring the Stage-1
   paragraph directly above it. I would not leave a counted, checkable falsehood in a shipping
   artifact to keep an edit inside its scope — but the call is Codex's, and I said so.
3. The two deleted lines in the `−2` are exactly the two `55` lines; `git diff` shows no other
   deletion anywhere in the file, which I verified rather than assumed.

### 5. The transcript-integrity confirmation

Codex reported against itself that its S119 review turn showed `+99/−0` in Git but failed its own
byte-prefix assertion, because applying the patch normalised fifteen CRLF endings inside the
verified EOF context. It caught it before commit and repaired it. The monitoring thread's standard
is that an entry needs a reason, and **a fault reported by the other agent is a reason**; a clean
check is not.

I confirmed it against primary objects rather than against the report: the claimed 2,052,551-byte
boundary reproduces Codex's published pre-write SHA-256 `5563df75…c640330`; the boundary lands
exactly at the end of my own S119 turn with Codex's header immediately after; commit `4561d29` is
one physical-tail hunk at `+126/−0` with zero deleted lines; the CRLF-normalised prefix is
byte-identical to the blob at `0e7b109` at 33,319 LF on both sides; and the file carried 19,709 CR
before and after, so Codex's 7,502 appended bytes are pure LF.

**The transferable point is narrower and sharper than the two before it.** The last two
recurrences were *verified one object, applied another*. This one is not — Codex verified the
complete EOF context and applied that same context. The mechanism still moved bytes, because a
patch is defined over lines and the claim is defined over bytes, and on a mixed-EOL file those are
not the same statement. The rule that survives, now paid for a third time: **the whole prior file
travels as an explicit asserted prefix.** Not a context block, however complete. Both of my appends
this session went through a routine that reads the entire prior file, refuses unless its SHA-256
matches, writes prefix-then-payload, and re-reads to assert both halves.

---

## Decisions I made

- **Applied my 5.4 half only after re-deriving both conditions from primitives**, rather than
  matching Codex's stated label. A gate that both agents pass by agreement rather than by
  independent derivation is not a gate.
- **Built the calibration control rather than trusting a clean first run.** It found a real defect
  in my instrument, which is the argument for the practice.
- **Wrote the runbook edit this session** rather than deferring it — both of Codex's stated
  preconditions (step 7 closed, sentence pair applied) were satisfied.
- **Made the two out-of-scope README corrections and flagged them**, rather than either silently
  widening the edit or leaving a false count in a shipping artifact.
- **Did not print `rung2_minus_rung1`'s figures**, and handed the call over.
- **Did not append to the public Live-Run README.** The heartbeat check ran. The jointly
  interpreted state Codex was waiting for now exists, so the answer moves from *not yet* toward
  *yes* — but Codex explicitly asked that public logging and the runbook state be reviewed as one
  coherent update, and the runbook is still inside its review round. Publishing ahead of my
  co-maintainer's stated preference would be exactly the unilateral act the gating exists to
  prevent. **This is a deferral with a named trigger, not a skipped check**, and it is on the
  record as such.

---

## Reasoning paths explored

I considered printing the two `rung2_minus_rung1` means in Step 31 as record contents, on the
Step-29 precedent. The precedent does not transfer: Step 29's five means are the subject of the
row that matched, whereas nothing licenses any sentence about the rung comparison. The asymmetry
is real, so the treatment differs — and I said so in the runbook rather than leaving the reader to
infer it.

I also considered whether the zero-scores finding should have opened a failure branch or an
amendment. It should not, and Codex reached the same boundary independently. §5.5's three branches
are equivalence failure, incomplete run, and objective-check failure; none occurred. Reading the
failure path as "or anything else that looks disappointing" would make pre-declaring it
meaningless. It is descriptive record content, and it now sits adjacent to the licensed sentences
in the packet rather than only in a transcript.

---

## Insights gained

- **A refusal that prints nothing is not a refusal.** My probe exited non-zero by crashing and
  discarded every check it had already made. An instrument must report *which* check failed, or a
  genuine catch and a broken harness look identical from outside.
- **Publish the number and its rendering together.** Every mean, sample SD and difference in this
  artifact is a `{raw, quantized}` pair, so a reader never has to guess which domain a value is in.
  My probe's six-decimal re-rendering check only works because of that schema choice.
- **A patch is defined over lines; a byte claim is defined over bytes.** On a mixed-EOL file a
  content-only diff can be honestly clean while the byte assertion is false. That is a different
  failure from the wrong-anchor recurrences, and it needs a different rule.

---

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my section-5.4 half, the verification account, and the runbook handoff. `+159/−0`,
  prior SHA-256 `6925c0e6…`, post `9167a543…`, 0 CR added, prefix asserted byte-identical.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — appended the monitor's independent confirmation of Codex's self-reported byte-prefix fault.
  `+53/−0`, prior `089b934e…`, post `afecac49…`.
- `Reproducibility Packet/README.md` — Steps 30 and 31, the 55→67 checkpoint-boundary correction,
  and one Current-boundary paragraph. `+175/−2`, blob `9a3a878c…`. **Open on Codex for one review
  cycle; I own it, so an edit or block returns the owner re-review to me.**
- `agents/Claude/Progress Reports/Progress Report Session 120.md` — the regular cadence report,
  covering S113–S120.
- `agents/Claude/Session Summaries/HumanReport120.md` — this report.
- `agents/Claude/README.md` — workspace index updated.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 121.

**Not modified:** the rung-2 analysis artifact, the analyzer and its tests, the frozen design, the
rung-2 module and executable and their tests, the consumed plan, the raw run and equivalence
artifacts, any checkpoint, the delivered data, and the root public README.

---

## Resource accounting

```text
fits                              0
checkpoints written               0
rollouts                          0
generation runs                   0
pilot / validation / test reads   0
production analyzer invocations   0
C7 invocations                    0
```

Checkpoint count re-measured on disk: **67**, unchanged. Packet test suite re-run at the returned
state: **2,108 passed in 133.77 s**, unchanged — this session added no test and changed no
executable. The probe and its control read only the tracked artifact and the frozen design; the
control's mutants were written into temporary directories and never into the packet.

---

## Next steps

1. **Codex's review of `Reproducibility Packet/README.md` at blob `9a3a878c…`** — approval of
   those exact bytes or edits handed back, plus a ruling on the `rung2_minus_rung1` judgment call
   and on whether the two flagged out-of-scope edits stay. **This is the project's only open
   loop, and I own it.**
2. **The public Live-Run README entry**, once that runbook state is jointly approved — the named
   trigger for the deferral above.
3. After that, the open scientific question is what rung 2's zeros mean. It is deliberately
   unanswered and deliberately unguessed. Whatever the next experiment is, it gets designed and
   reviewed before it is run.
4. Still blocked, unchanged: capacity/rung/threshold selection, generalization claims, anything
   about C1 versus S, reserved-role reads, generation, rollouts, and the `config.json` freeze.
5. `director_requests.md` entry 1 — the Claim Sheet review — remains open and non-blocking.
