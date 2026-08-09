# Claude Human Report — Session 102

**Date and time:** 2026-08-09 08:29 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. The project lifetime Protocol-P total remains **278**.

**Fits:** 0. **Checkpoint writes:** 0. **Data generation:** 0. **Plan artifacts published:** 0.
**C7 invocations:** 0. **Artifacts written:** 0. **Pilot / validation / test reads:** 0.

**Real-data touches, all reads:** `manifest.csv` and the 304 authorized development rows; the
fifty checkpoints named by the terminal sweep record, opened to hash their bytes; and of those,
the ten approved anchor `.pt` files also loaded and scored in one forward pass each. A forward
pass under `no_grad` is not a fit.

**Progress-report session:** no. My next regular progress report is Session 104, unless a phase
transition or an approved written Claim Sheet amendment fires sooner.

---

## Summary

This session was a review. Codex built invariant **C7** — the new read-only analysis script that
turns the completed capacity sweep into the pre-declared descriptive read — and handed it to me
for independent review at two exact file states. I reviewed it, found **two defects**, repaired
both, added three tests, and handed an edited state back with my explicit approval. The loop is
open on Codex.

The headline is the first finding, and it is the same shape as finding AU three sessions ago:
**the reader as handed over could not have completed the read it exists to perform.** Not because
the science was wrong, and not because the model was wrong — because two kinds of arm in the same
record are written by two different programs, and one of those programs rounds its numbers before
it writes them. The reader compared both kinds the same way, so it would have refused the first
approved anchor it reached, reporting what looks like a corrupted checkpoint.

I proved that from the published artifacts alone before touching any data, then drove the real
function against the real state to watch it refuse, then repaired it and drove it again to watch
it accept.

**I did not compute the section-5 descriptive read.** No headroom, no pair constraint, no curve
shape, no crossing point, no paired range, no `m(c)`, no `s(c)` and no derived label for the
completed sweep. `derive_analysis` was never called against the real state. That interpretation is
pre-registered as prose in the frozen design and is applied jointly, at a later gate, after C7's
code loop closes and after a separate authorization to run it — three gates, in that order.

---

## What was accomplished

### 1. Finding AV — the two arm kinds are persisted in different numeric domains

The terminal sweep record carries fifty arms. Forty are new (`COMPLETED`) and ten are the
already-approved 32-channel anchors (`REUSED`). C7's `evaluate_arm_context` re-loads each
checkpoint, recomputes its classification scores through the approved metric definition, and
requires the recomputation to equal what the record stores — exactly.

That is right for the forty new arms and unsatisfiable for the ten anchors, because the two kinds
reach the record through different writers:

| arm kind | written by | numeric domain |
|---|---|---|
| `COMPLETED` | the sweep executable's `curve_arm_document` | the raw float, unrounded |
| `REUSED` | the approved first-fit analysis, `dev_fit_analysis.json` | `round(x, 12)` — the whole report goes through `rounded()` |

**Measured from the two published artifacts, with no data read and no model loaded.** Every
per-class F1 is a `2·TP / (2·TP + FP + FN)` rational over 152 examples, so the denominator is a
positive integer at most 304. I searched that space for the unique rational whose twelve-decimal
rounding is the published value, and compared that rational's float with what is published:

```text
per-class F1 values whose exact rational differs from the persisted float   32 of 40
anchors whose exact macro-F1 differs from the persisted macro-F1            10 of 10
new arms whose macro_f1 renders with MORE than twelve decimals              40 of 40
```

So the exact comparison is satisfiable for every new arm and for no anchor. Arms are evaluated in
`(channels, suite, seed)` order, so a real run would have re-scored the twenty arms at 16 and 24
channels and then refused at the first 32-channel anchor with *"a recomputed checkpoint score
differs from the terminal record"*.

**Then I drove it rather than resting on the arithmetic.** I loaded the 304 authorized development
rows and the one approved `dev_fit_C1_seed0.pt`, built the arm through Codex's own validator, and
called Codex's own function:

```text
RESULT: evaluate_arm_context REFUSED -> a recomputed checkpoint score differs from the
                                        terminal record
raw == stored (macro_f1)                 False
rounded(raw) == stored (macro_f1)        True
rounded(raw) == stored (accuracy)        True
rounded(raw) == stored (per-class)       True
stored is already at the 12-dp boundary  True
```

The recomputation is correct in every particular. It disagrees only about which domain the stored
number lives in.

**The repair: compare in the domain the value was persisted in, and assert both directions.** A
new function `require_recomputed_scores_match` keeps exact equality for new arms — that is the
strongest check available there and I did not weaken it — and, for a reused anchor, takes the
recomputation to the approved analyzer's own twelve-decimal boundary using that file's `rounded`
function, imported rather than restated. It *also* requires the stored anchor value to be at that
boundary, so that if the approved analysis ever stopped rounding, this would fail loudly instead
of quietly becoming a comparison of a value with itself.

I deliberately did **not** round both sides. That was the smaller edit, and it would have thrown
away a real check on forty arms to fix a problem that exists on ten.

### 2. Finding AW — a second network construction site, in the one file its guard cannot see

The frozen design's invariant **C5** says the rung-1 parameter band stays enforced for every arm
and that no flag may turn it off. The sweep module implements that by having exactly one place
where the network is constructed, and an AST test asserts that `enforce_rung1_band=True` occurs
**exactly once** in that module.

C7 constructed its own network directly, with its own `enforce_rung1_band=True`. That test parses
the sweep module and nothing else, so a second construction site in a different file is entirely
outside its reach: the sweep suite stays green while two definitions of the network under review
drift apart. It also skipped the capacity-point and seed validation that the shared constructor
performs.

Repaired to call the shared `build_network`, moved above the `try` block so a channels/seed
refusal propagates as itself rather than being relabelled *"a capacity checkpoint cannot be
loaded"*. The class is no longer imported or referenced anywhere in the reader.

### 3. Why the test suite could not catch either one — the part I think matters most

Both defects sat under twenty-one passing tests, and in both cases the fixture was degenerate
along exactly the axis under test:

- The one test that drives the scoring path uses a two-example fake batch and asserts against
  `accuracy = 1.0`, `macro_f1 = 0.5`, and per-class values of `1.0` and `0.0`. **Every one of
  those numbers is exact at twelve decimals**, so the fixture cannot tell the two persistence
  domains apart. It is also a new arm, so the anchor branch is never entered at all.
- The test that binds reused anchors to the approved analysis builds the synthetic approved rows
  *from* the synthetic record rows, so both sides come from one source and the boundary can never
  appear between them.

This is the Session-86 lesson recurring almost verbatim: a fixture repaired along the measured
axis stayed degenerate along one nobody named. So I added three tests, and made the
non-degeneracy an **explicit assertion** rather than a property of the numbers I happened to pick:
one test asserts that rounding actually moves the fixture, one drives the anchor/new-arm
distinction in four directions, and one pins that the reader adds no second construction site.

**Four-case two-state mutation sweep**, each case run twice with identical results, every write to
the production file restored in a `finally` with the restore digest-verified:

```text
M1  restore the exact comparison for both arm kinds (the handed-over behaviour)   CAUGHT
M2  round BOTH sides                                                             CAUGHT
M3  drop the both-directions boundary assertion                                   CAUGHT
M4  restore the second construction site                                          CAUGHT
```

Each was caught by the test that names it, not merely by the suite. M1 is the negative control
that matters: it reproduces exactly what was handed to me, and the new test goes red.

### 4. Sufficiency check on the real exact state, stopping before the read

The Session-101 discipline applied again: when a read is fenced off, check that it *could* be
computed rather than computing it. I drove C7's whole authentication chain against the real
approved documents and stopped before the derivation. Thirteen checks, all passing:

```text
the three inputs parse; the result, plan and anchor canonical digests are the approved ones
validate_envelope accepts the real state and sources BAR = 0.05 and s(32) = 0.149635726834
validate_arms returns fifty normalized arms: ten REUSED, forty COMPLETED
load_development_context returns 152 + 152 authorized development rows and the shared context
all fifty checkpoints resolve inside their namespace; 50 of 50 digests match the record
the repaired comparison accepts 10 of 10 reused anchors -- it refused 10 of 10 before
```

I also checked the one number the reader hard-refuses on. Recomputing the anchor's paired sample
standard deviation from the record's own values and rounding to twelve decimals reproduces the
approved published figure exactly (`0.1496357268341403` against a published `0.149635726834`, with
`3.6e-13` of margin to the nearest rounding boundary). That check is sound and I kept it.

### 5. Two things measured and recorded rather than raised

1. **`paired_range_exceeds_anchor_sd` is `false` when the paired range is `null`.** The frozen
   interpretation table reads that `false` as "the difference did not move by more than the
   anchor's own seed spread", which is not what an empty eligible subsequence means. It is
   unreachable in practice, because the reader refuses unless the anchor point is unconstrained
   and therefore always eligible. Recorded because the branch exists.
2. **The run root is not required to be named after the run label.** The design makes that binding
   structural for the *executable*; the reader only requires the terminal artifact to sit directly
   in the supplied root, and then authenticates every byte it reads by digest. Nothing is unsound.
   Stated in the transcript with its reasoning so Codex can overrule the reasoning and not only the
   observation.

---

## Challenges, and how they were handled

**The main one was not finding the defect — it was not spending the pre-registration to find it.**
The whole point of the frozen design's section 5 is that the interpretation is fixed *before*
anyone sees the curve. A reviewer who "just checks the numbers are sane" spends that and cannot
give it back. So every measurement this session was designed to stop short of the read: the
rational reconstruction uses only the anchor values the design already publishes; the drive of the
broken function uses one anchor arm; the sufficiency check calls everything except the derivation.
That constraint made the review harder and is the reason the first proof is arithmetic rather than
empirical.

**A self-correction worth recording.** My first repair introduced two em dashes into a file Codex
had written as pure ASCII. I caught it by measuring the returned bytes rather than by reading them
— the check that reports `ascii False` is worth more than the intention to type carefully — and
replaced them before finalizing. Same family as the transcript writer's ASCII gate, which exists
for the same reason.

---

## Reasoning paths explored, and what was rejected

- **Round both sides.** Rejected. It fixes ten arms by giving up a stronger check on forty. The
  domain difference is a fact about two writers, so the comparison should know about both writers,
  not average over them.
- **Add a tenth identity entry / a new guard for the anchor domain.** Rejected as over-building.
  The rounding already has exactly one definition in this project, in the approved analyzer; the
  right move is to import it, which is what the design says about every other shared definition.
- **Raise AW and leave it to Codex.** Rejected. The reviewer may edit, the repair is two lines, and
  leaving a second construction site in place while the loop is open is the state in which someone
  changes one of them.
- **Run C7 end to end to see whether anything else breaks.** Rejected outright. That is the read,
  and it is gated. The sufficiency check is the honest substitute and it found nothing further.

---

## Insights gained

- **A green suite is a statement about the states it enters.** Twenty-one tests passed against a
  reader that could not have read the artifact it was written for. This project has now recorded
  that sentence three times — for the driver, for the sweep executable, and now for the reader.
- **A number's domain is part of its identity, and a writer is where a domain is decided.** The
  project already knew this for file digests (canonical for tracked text, raw for binary). Finding
  AV is the same rule one level down: a *value* must be compared in the domain of the program that
  persisted it, not the domain of the program that recomputes it.
- **A guard pinned by an AST test is pinned in one file.** Widening the code without widening the
  test's domain leaves a guard that looks enforced and is not.
- **The cheapest decisive measurement was arithmetic.** Reconstructing exact rationals from
  published twelve-decimal values settled the whole finding before a single byte of data was read.
  Worth reaching for first when the alternative touches a fenced-off resource.

---

## Files created or updated

**Reviewed, repaired and returned (open on Codex for owner re-review):**

```text
Reproducibility Packet/scripts/analyze_capacity_sweep.py
  Git blob                 b9043fa266dc7c35a6acdb240216ae0ec3337f6e
  canonical/raw SHA-256    7eca4016d7ffb73c15ec1e35642e5f6e1ecb95a7c6757e72cc875cf79f87ffbe
  44,600 bytes / 1,088 lines / LF / pure ASCII / no BOM
  (Codex's handoff state, superseded: 5dcc0947 / c33e21f5...fa35fe27)

Reproducibility Packet/tests/test_capacity_sweep_analysis.py
  Git blob                 a81d35c952fba158f647a64b9cd13bad0c301c93
  canonical/raw SHA-256    bd8c36316b4be433cac0000ef2597137cb35b68b0f5407c7b992764d9976d229
  29,957 bytes / 805 lines / LF / pure ASCII / no BOM   24 tests (21 + 3)
  (Codex's handoff state, superseded: 5e4497fd / 1d95cdc9...05842586)
```

**Appended (never overwritten):**

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — one turn, `+257 / −0`, a single tail hunk, all seven writer gates passed, header declared
  `08:26 PDT` against a write at `08:26:38 PDT`.

**Closeout:**

- `agents/Claude/Session Summaries/HumanReport102.md` (this file)
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

**Deliberately unchanged:**

- The root Live-Run `README.md`. The heartbeat check ran and the answer was no: an open review
  round is work in progress, which the lean public log is explicitly not for, and the banner date
  is already current. **Not even the banner date was advanced** — "Last updated" tracks the public
  state, and advancing it on a session a stranger cannot see tells that stranger something happened
  when nothing public did.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md`. **No recurrence, verified at
  the Git level rather than assumed:** Codex's Session-101 commit touches the Phase-2 transcript as
  a single tail hunk, additions only, and touches the monitoring file not at all; my own append is
  likewise a single tail hunk with additions only. The duty is to flag recurrences, so a clean
  session adds no note.
- `agents/Claude/references.md`. No external source was read this session.
- Every approved artifact: both run roots, both consumed plans, all 55 local checkpoints, the
  sweep executable, its tests, the frozen design, the approved ledger and the approved first-fit
  analysis. Nothing was regenerated, moved or deleted.

**Verification of the returned state**

```text
C7 tests, normal                          24 passed  (21 + 3)
capacity executable + C7, normal         241 passed
capacity executable + C7, python -O      241 passed; expected pytest warning
full packet suite                      1,792 passed
compileall                                 clean
production AST                            27/27 functions documented; zero assert guards
working tree                              clean before and after, apart from this session's files
```

---

## Next steps

1. **Codex owns the next turn:** the owner re-review of `b9043fa2` / `a81d35c9`. It should re-open
   both findings rather than wave them through — AV changes a comparison it wrote deliberately, and
   if it would rather bind the anchor domain another way, that is a real disagreement and better
   had now than after the read.
2. **When that loop closes**, C7 execution is still its own gate: an exact command, inputs, output
   destination and a joint authorization, followed by an exact-state review of what it wrote.
3. **Only then** is the frozen section 5.4 interpretation applied, jointly, to the exact reviewed
   state. Nothing about capacity selection, thresholds, Stage 2, config materialization,
   generation, rollouts, or any pilot/validation/test read is licensed before that, and section 5.4
   itself licenses none of them either.
4. **Standing and unblocked:** the Phase-3 packet obligation I recorded and did not fix — the
   packet's own README does not mention the capacity sweep at all, and the git-ignored checkpoints
   have no documented clean-machine recovery path. Both belong to Phase-3 assembly and neither
   belongs inside a review session.
5. **Director:** nothing is blocked on Randy. `director_requests.md` entry 1 (the Claim Sheet
   review) remains open and non-blocking.
