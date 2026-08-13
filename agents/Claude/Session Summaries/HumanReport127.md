# Human Report — Claude Session 127

**Current date and time:** 2026-08-13 12:11 PDT

## Summary

This was the fifth round of review on the Slot-8 verification-artifact design — the document that
specifies the director's hands-on verification path. It is still the only open review loop in the
project, and it is mine to own.

Codex's Session-126 review of my Session-126 state kept all four of my repairs and raised one
finding of its own, **CM**: a sentence in my rationale for finding CI claimed that no code in the
packet writes a `controller_logs` payload, and that was false. This session I re-opened that
finding and drove it against the source rather than taking Codex's word for it. The claim is
correct — `scripts/build_data_contract_fixture.py` does write a synthetic controller role, copying
the plant record's own timestamps. I accepted CM in full and kept Codex's replacement wording
unedited.

I then found two things of my own in the state Codex returned:

- **CO** — Codex's edit removed the clause that made its own appeal to the design's section-1.2
  test valid, leaving the conclusion without its premise. Restored as a single clause; non-blocking
  and I said so.
- **CN** — the load-bearing one, and it is the shape that has been recurring: **a rule stated
  generally and then enumerated partially, with the tests pointed at the enumeration.** The
  `X_WINDOW_UNSUPPORTED` refusal said an arm's tracking block must be a valid call to the live
  tracking metric, then listed four ways it could fail; invariant V15 told the future build round
  to "assert the four refusal shapes". I drove the live function and found that a scene satisfying
  every one of those four checks is still refused in at least two more ways. So the enumeration was
  a partial re-implementation of a function the packet already owns. Repaired by making scene
  construction *call* the function instead of re-deriving its preconditions.

The design is back on Codex at Git blob `0753d4ed`, which I explicitly approved. Step 1 of the
Slot-8 sequence remains open; no module, fixture, figure or real-result connection is authorized.

**This session spent zero fits, zero rollouts, zero checkpoints, zero generation runs, zero
analyzer invocations, and zero pilot, validation or test reads.**

## What was accomplished

### 1. The handoff was authenticated before it was reviewed

The Phase-2 transcript's first 2,160,843 bytes reproduce Codex's declared pre-append digest
`0a35151d…` exactly; its append is 5,738 bytes carrying 101 LF and zero CR; the transcript's total
CR count is 19,709 before and after, unchanged; and Codex's Session-126 turn was physically last.
The design on disk reproduced Codex's declared reviewer state to the byte: blob `c674c022`,
raw == canonical `9e9abda3…`, 57,121 B / 767 LF / 0 CR, non-ASCII confined to U+2013 and U+2014.

Nothing in the review started until those matched. This is the discipline the project arrived at
after a transcript-order fault recurred three times: the whole prior file travels as an asserted
prefix, not as a context block.

### 2. Finding CM was reproduced at source and accepted in full

Codex's claim was specific and falsifiable, so I checked it rather than agreeing with it:

- `scripts/build_data_contract_fixture.py` defines `_controller_payload`, which writes
  `"t_s": np.asarray(record.t_s, ...)` — the plant record's own time array, copied verbatim into
  the controller role.
- A grep across every script in the packet confirms it is the only place a `controller_logs`
  writer is created at all.
- `utils/assignment_generator.py` records `roles_intentionally_pending_gate4_fit` as exactly
  `["estimator_outputs", "controller_logs"]` — so the absence of a *production* writer is a
  declared state, not an oversight.
- `validate_role_payload` requires `controller_logs.step` to be a contiguous 0-based grid and
  `t_s` to be strictly increasing, and never compares `t_s` to anything in the plant record.

My sentence had collapsed "no production writer has fixed the convention" into "no code writes the
role". The first is true and is the reason the design should not freeze a timestamp equality; the
second is simply false. Codex's replacement is also the stronger argument, because it rests on what
the schema and role contract *promise* rather than on a prediction about future code. I kept it
word for word.

### 3. Finding CO — a restored clause

Codex's edited paragraph ends: "…would bake an equality into this scene contract that neither the
schema nor the role contract promises. That is exactly what section 1.2's design test names as a
defect."

Section 1.2's test is narrower than that sentence implies. It says that when the scientific inputs
finally exist, *connecting them must not require a rewrite of the scene schema or either renderer*.
Baking in the equality is not itself the defect; it is a defect **because** connecting a faithful
production logger would then require editing this contract. That intermediate step was the clause
the edit had removed, and without it the conclusion floats. I restored it as one clause, changed
nothing else in the paragraph, and told Codex in the transcript that I would equally accept
dropping the appeal to 1.2 instead — this is a precision repair, not a disagreement.

### 4. Finding CN — the rule that enumerated part of a function it should have called

This is the substantive finding of the session, and it is my finding CE seen one level further out.

CE (Session 125) established that the fixture must produce a valid call to `utils.metrics.j_5s` —
the tracking metric the Technical Report will report and the verification figure's third panel will
draw — and that a scene which is not a valid call must be refused at construction with
`X_WINDOW_UNSUPPORTED` rather than reaching a renderer. That repair was right and survives.

What the document then did was *list* the ways such a call can fail: a non-uniform or
non-increasing grid, a non-finite sample, an onset that is not exactly on a control sample, and a
grid that ends before the analysis window closes. Invariant V15 said, in as many words, "Tests also
assert the four refusal shapes." A build round reading that implements those four checks.

I drove the live function instead of reasoning about it. On a uniform, strictly increasing 500 Hz
grid with finite traces and an on-sample onset — every one of the four named checks satisfied:

```text
window_s = 0.001 (shorter than one control interval)
    four named checks pass: True
    live j_5s: REFUSED  "the analysis window contains fewer than two control samples"
window_s = 0.0
    four named checks pass: True
    live j_5s: REFUSED  "window_s must be positive"
window_s = -1.0
    four named checks pass: True
    live j_5s: REFUSED  "window_s must be positive"
one-sample grid
    four named checks: NOT EVALUABLE — the uniformity check has no interval to test
    live j_5s: REFUSED  "window_s must be positive"
control: window_s = 5.0, onset 0.010     ACCEPTED, finite value
control: two-sample grid, window = 1 dt  ACCEPTED, finite value
```

Nothing in the scene table constrains the window length; it is carried as a bare scalar sourced
"from fixture or authenticated config". So a fixture could set it to zero, construction would
accept the scene, the tracking panel would pin its shaded band to a zero-width window, and the
refusal would arrive later — from a test, or from a renderer — instead of from the construction
step the design assigned it to.

The deeper problem is not the missing cases. It is that a list of a live function's preconditions
is a **second definition of a fact that function already owns**, which is the duplication the
design's own property 1 forbids by name, and which drifts the moment the function changes.

**The repair.** Scene construction now establishes validity by *calling* `j_5s` and refusing on
whatever it raises, rather than re-deriving its preconditions. The exit-code table says so and
marks its list as "include, and are not limited to". Section 4.4 gains a bullet carrying the driven
evidence and the reasoning — delegating costs one trapezoid over arrays the scene already holds,
opens no file, and cannot fall behind a later change to the metric. V15 now requires a test that
construction *delegates*, and asserts six refusal shapes individually: the original four plus the
two I drove, which are in the list precisely because each passes every other check in it and is
caught only by the call.

### 5. Three checks that found nothing, recorded so they are not re-spent

- **The design requires the two arms of a scene to share one exact time grid. I checked that a real
  pair can satisfy that, including the awkward case.** The assignment generator builds the C1 and S
  rows of a pair from a single reservation and compares trajectory and every seed field one by one,
  so both arms run the same trajectory for the same duration. And the online rollout loop contains
  no early exit: it runs its full step count regardless of safety flags, so a fault-tripped arm
  cannot come back shorter than its partner and silently break the pairing.
- **A schema cross-reference I suspected was a mislabel is correct.** Schema section D is titled
  "Labels, estimator outputs, controller logs", so the design legitimately cites D for both the
  truth block and the decision block.
- **The mechanical counts are clean on the finished bytes.** The nineteen invariants appear once
  each as headings and in order, the prose count that names them still matches, the property
  lead-in says "Eight" over a mechanically enumerated one-through-eight, and the exit-code table
  has thirteen rows with no code appearing in prose without a row.

### 6. Exact state returned, and the sweep over the finished bytes

```text
owner Git blob              0753d4ed5523ba57de6e848a3682bf5184ff4128
raw == canonical SHA-256    98e20ae11bf2ed112b584d3ea9f1c1302380489440dcff239f9154dc719b27ba
bytes / LF / CR             59,495 / 790 / 0
final newline / BOM         yes / no
non-ASCII                   U+2013 and U+2014 only
LF pinned by                packet .gitattributes `protocol/*.md text eol=lf`; git check-attr
                            reports eol: lf, and the filtered and --no-filters hashes agree
owner delta from reviewer   +34 / -11, git diff --check clean
```

All eleven deleted lines attribute to the four blocks I deliberately rewrote — the status line and
its closing sentences, property 3's section-1.2 sentence, the `X_WINDOW_UNSUPPORTED` row, and V15 —
with zero unattributed, verified from the diff rather than from memory.

My chat append is `+149/-0`, prior transcript `0012d6ae…` at 2,166,581 bytes, post `8a8b25d2…` at
2,175,950 bytes, zero CR added, with the entire prior byte sequence asserted identical by the
routine that wrote it.

## Challenges and how they were handled

### Accepting a correction without accepting it on authority

CM told me one of my own sentences was false. The temptation in a fifth review round is to accept a
narrow wording correction quickly and move on — it costs nothing and it keeps the loop converging.
I have a standing lesson against exactly that: a reviewer being right is not the same statement as
a reviewer's set being complete. So I reproduced the writer, grepped for others, read the
generator's declaration and read the role validator, and only then accepted. The check also paid
for itself twice over: it is what put me inside `role_contract.py` and `metrics.py` in the same
session, which is where CN came from.

### Knowing when a precision repair is worth a round and when it is not

CO is a single restored clause in a rationale paragraph. It changes no rule. Raising it risks
another review round over prose. I raised it anyway, but marked it explicitly non-blocking in the
transcript and offered Codex the alternative fix — because an argument whose premise has been
deleted is exactly the kind of thing a later build round reads, cannot follow, and quietly ignores.

### Not planting a fresh instance of the defect I found last session

My Session-126 finding CL was a stale count sitting beside a list it did not enumerate. My first
draft of the CN repair wrote "the four shapes named just above" and "every one of the other four
checks" — two new counts beside two lists. I caught them in the mechanical sweep of the finished
bytes and removed both numerals. This is the third session running that a mechanical pass over my
own finished work caught something a reading had missed.

## Important decisions

1. **Accepted CM in full, unedited, after reproducing it at source.** The rule it narrows is
   unchanged, and Codex's version of the argument is the better one.
2. **Repaired CN by delegation rather than by extending the list.** Adding the two missing cases
   would have fixed the symptom and left the duplication in place. Calling the function is the
   repair that cannot rot.
3. **Kept the four original refusal shapes as individually asserted tests** rather than replacing
   them with the delegation test alone. They are the regression cases the last two rounds paid for.
4. **Left the public Live-Run README untouched.** An open internal review round is none of its
   three triggers, which is the same call I made in Sessions 123 through 126 and the same one Codex
   made in its Session 126.
5. **Did not open a second work lane.** The direction is settled — Slot 8 first, then the Technical
   Report, then the Accessible Piece — and step 1 is not closed.
6. **Appended nothing to the transcript-order monitoring thread.** The check was clean; a clean
   check belongs in this report, not in that file.

## Reasoning paths explored

**I considered approving Codex's bytes unchanged.** Its edit was correct and the loop is five
rounds deep. Rejected: the CN gap is in the part of the document that tells the build round what to
implement, and this design exists specifically so that the eventual demo cannot be built the cheap
way. A gap in the instruction is the most expensive kind of gap here.

**I considered repairing CN by simply adding the two missing preconditions to the list.** Rejected
for the reason above — the list would still be a partial copy of a live function, and the next
person to change `j_5s` would have no reason to look here.

**I considered whether construction calling `j_5s` violates the design's own rule that a renderer
opens no scientific input.** It does not: the call is a pure function over arrays the scene already
carries, opens nothing, and costs one trapezoidal integral. Section 4.7 adds no dependency, since
the invariants already require a test to call the same function.

**I looked for a defect in the requirement that both arms share one exact time grid**, on the
theory that the CI shape — a rule strict enough to refuse the real data it is written for — might
recur there. It does not: pairs are built from one reservation with identical trajectory and seeds,
and the rollout loop has no early exit. Recorded as a null result so the next session does not
re-spend it.

## Insights gained

**The recurring defect in this document has a shape, and it has now appeared four times.** CA, CE,
CI and CN are all the same failure: *a rule stated in general terms and then discharged by a
partial enumeration*, where the enumeration is what the implementation will actually follow. CA
enumerated the JSON values that could be written and omitted the schema's own defaults. CE required
a valid metric call without requiring the fixture to produce one. CI enumerated an equality the
real system does not satisfy. CN enumerated four of a function's preconditions and told the tests
that was the set. The general question that finds this class is: **when this document names a fact
that some other object already owns, does it point at that object, or does it copy it?**

**The most useful question this round was "who owns this fact?"** — the companion to last session's
"which panel draws this?". A document that copies a fact takes on the obligation to keep the copy
current, and nothing in the project enforces that. A document that points at the owner cannot go
stale.

**The loop is still converging, and CN is smaller than CI was.** CI would have refused every real
scene; CN would have let an invalid scene through to a test or a renderer instead of refusing it at
construction. Both are real, but the blast radius is shrinking each round, which is what a
converging review looks like.

## Files created or updated

- `Reproducibility Packet/protocol/slot8-verification-artifact-v0.1.md` — **updated** (+34/-11).
  Blob `0753d4ed`, raw == canonical `98e20ae1…`, 59,495 B / 790 LF / 0 CR. The CN repair (exit-code
  row, a new section-4.4 bullet, V15), the CO clause restoration, and the status line.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — **appended** (+149/-0), the Session-127 owner re-review turn.
- `agents/Claude/README.md` — **updated**, the Slot-8 line's state and review history.
- `agents/Claude/Session Summaries/HumanReport127.md` — **created** (this file).
- `agents/Claude/Summary of Only Necessary Context.md` — **rewritten** for Session 128.

Read at source and not modified: `Reproducibility Packet/scripts/utils/metrics.py`,
`utils/role_contract.py`, `utils/assignment_generator.py`, `utils/online_loop.py`,
`scripts/build_data_contract_fixture.py`, `schema/schema-v1.0.md`.

## Next steps

1. **Codex's fifth-round review of blob `0753d4ed` is the next thing that happens.** If it approves
   those exact bytes, step 1 of the Slot-8 sequence closes.
2. **If step 1 closes, step 2 is mine and is authorized**: the scene module
   (`Reproducibility Packet/scripts/utils/verification_scene.py`), the renderer
   (`scripts/render_verification_scene.py`), the synthetic fixture, and the test suite carrying all
   nineteen invariants. Neither file exists yet — the design-first decision is why no code has been
   written across five sessions.
3. **If Codex edits or blocks instead, the owner re-review is mine again and comes first.**
4. My next regular progress report is **Session 128**, unless a phase transition or an approved
   Claim-Sheet amendment fires one sooner.

## Boundary — what this session did not spend

Zero fits, checkpoints, rollouts, generation runs, plan invocations, analyzer invocations and C7
invocations. Zero pilot, validation and test reads — the final test split remains at zero identities
and zero payloads. No real data payload or role index was opened. No MuJoCo model was built and no
rollout was stepped. No capacity, rung, width, probability threshold, abstention threshold or
configuration was selected. No closed lane was reopened. The `j_5s` probe ran in a scratch directory
outside the repository against fabricated arrays. The checkpoint count was not re-read because no
fit ran and nothing this round depends on it; it stands at 67 as last measured.
