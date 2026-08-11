# Claude — Human Report, Session 114

**Date and time:** 2026-08-10 22:15 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. My next regular progress report is Session 120, unless a phase
transition or an approved written Claim Sheet amendment fires sooner.

---

## Summary

One thing was open at the start of this session and one thing is closed at the end of it. Codex's
Session 113 reviewed the rung-2 network module I wrote in my Session 113, found no defect in the
production code, found two gaps in my **tests**, added two tests of its own, and handed the state
back. Under this project's review cycle a reviewer's edit does not close the loop — the owner has
to genuinely re-open the artifact, re-review both the feedback and the edits, and either approve
or return something better. That re-review was this session's job, and I did it by measurement
rather than by reading.

**Both of Codex's findings are real, both implementations are kept unchanged, I found no defect in
them, and I have explicitly approved the exact bytes.** Step 2 of the rung-2 sequencing is closed.
That authorizes step 3 — writing the escalation executable and its tests — and nothing else.

### What Codex found, and how I checked it

**Finding BK.** In my Session 113 I closed a mutation sweep with a test asserting that *every*
constructed parameter receives a non-zero gradient from the forward pass. I called it the general
instrument, because it catches — in one statement, for every tensor at once — a component that is
built, counted in the parameter ledger, and then never actually applied. I asked Codex directly
whether that test could miss a stage that is live and receiving gradient but wired contrary to the
design. Codex's answer was yes, with two constructions: traverse the four causal convolution
blocks in reverse, or apply the stem normalization *before* those blocks instead of after. Both
keep all 219,018 parameters, every declared shape, strict causality, and non-zero gradient
everywhere. Neither is the path the frozen design names.

I did not accept that on the argument. I built an eleven-case wiring mutation sweep and ran the
whole thing twice against **both** test states — my incoming file and Codex's reviewer-edited file
— under this project's standing harness rules.

```text
                                        incoming    reviewer
M1  stem traversed in reverse           SURVIVED    CAUGHT
M2  stem_norm applied before the stem   SURVIVED    CAUGHT
M3  fusion operands swapped             CAUGHT      CAUGHT
M4  GELU before the fusion Linear       CAUGHT      CAUGHT
M5  k_proj / v_proj swapped             CAUGHT      CAUGHT
M6  softmax over heads, not time        CAUGHT      CAUGHT
M7  severity columns swapped            CAUGHT      CAUGHT
M8  attention query from the first step CAUGHT      CAUGHT
M9  pooled final state is the first one CAUGHT      CAUGHT
N1  encode local renamed  (control)     SURVIVED    SURVIVED
N2  dilation int-cast     (control)     SURVIVED    SURVIVED
baselines                               69 green    71 green
```

Two passes identical. Zero bad anchors. Module restored to `ca192af0` and tests to `c43d33b`,
both blobs re-verified after the sweep. **Codex's finding is exactly right and exactly two cases
wide in this grid**, and the seven cases that were already caught are what make the result mean
something — they show the sweep is discriminating rather than simply alarmed, and they show the
region my tests *did* cover was genuinely covered. The two harmless controls surviving both states
is the other half of that.

Then I went one step further, because a repair is only load-bearing if the test that was added is
the test that fires. I re-ran M1 and M2 with per-test failure reporting: each produced **exactly
one failure**, and it was Codex's new `test_encode_is_the_declared_stem_norm_gru_path_in_order`
both times. The repair is precisely the thing doing the catching.

The conceptual point is worth keeping, because it is general and I got it half right. Gradient
reach and reconstruction answer different questions. Gradient reach asks *is this component
connected to the answer* and states it once for every tensor at once — that breadth is exactly
what makes it valuable and exactly what makes it blind to position. Reconstruction asks *is this
component in the slot the design named* and can only be written one path at a time. Neither
subsumes the other, and the sweep above is the evidence rather than the assertion: M1 and M2 leave
every parameter gradient-reached.

**Finding BL.** My module and test prologues both said all four disclosed limitations were pinned
by tests. Three were. The fourth — that the approved `capacity_sweep.score_arm` carries a narrow
rung-1 type annotation but a rung-agnostic runtime contract — was enumerated and never driven.
Codex added a test that scores two synthetic examples through the approved function with the real
rung-2 network. I accepted the diagnosis immediately; a claim written down and not driven is the
weaker half of this project's recurring failure mode, and this one sits on the seam the *next*
authorization depends on, since `score_arm` is the approved scorer the step-3 executable is
required to import.

I checked the new test is load-bearing rather than merely present. Editing the approved
identity-bearing file to see the test go red is not available — a one-word edit there changes a
recorded code identity — so I measured it from outside with a forward hook in a throwaway probe:

```text
forward calls through capacity_sweep.score_arm with the rung-2 net   1  (batched, both examples)
score_arm.__annotations__["net"]                                     TemporalAttributionNet
returned mapping                                 {accuracy, macro_f1, per_class_f1}
per_class_f1 keys                                actuator, healthy, sensor, structure
```

The scorer really does drive the rung-2 forward pass, and the annotation really is the narrow one.
Disclosed limitation 3 is now a measured behaviour on the same footing as the other three.

### What I recorded rather than raised

The **order in which the constructor draws its parameters** is pinned by nothing. Swapping the
`k_proj` and `v_proj` construction lines would leave the parameter count, every shape, the module
census and every reconstruction test intact while changing the initial weights. I deliberately did
not raise this as a defect and deliberately did not propose pinning it: the design names an
architecture, not a draw order; nothing is fitted at rung 2 for it to disagree with; and once the
executable exists, the module's own recorded code identity refuses any edit to this file anyway.
Pinning it would freeze a decision the design never made. I recorded it in the chat and here so a
later session does not rediscover it and constrain the module on the strength of the rediscovery.

### Verification

At exactly module blob `ca192af0…` and test blob `c43d33b…`:

```text
focused normal        71 passed in   3.67 s
focused python -O     71 passed, 1 expected pytest assertion warning, in 2.27 s
packet-wide        1,863 passed in 140.01 s
git status         clean; both blobs re-verified after every probe
```

Codex's 1,863 reproduces on my run. The count moved from 1,861 to 1,863 by exactly its two tests.

## Challenges, and how they were handled

**The temptation to agree.** Codex's report was careful, its two findings were plainly correct on
reading, and the fastest honest-looking path was to say so and approve. The review cycle exists
precisely because that path is indistinguishable, from the outside, from the path where the owner
did the work. The sweep cost about two and a half minutes of compute and is the difference between
"I agree with the reviewer" and "I measured the reviewer's claim and here is the grid."

**A carried note of mine turned out to be false, and measurement caught it.** My summary file has
said since Session 105 that the public README had been renormalised and the "log tail is bare LF
while the file is mixed" note was retired as false. Measuring the file before appending showed the
opposite: 205 LF against 199 CR, with the log entries ending in bare LF and the surrounding
document in CRLF. I matched the neighbouring log entry rather than the document, and I have
corrected the note in my summary. This is the standing rule earning its keep — *measure the file
before any append* exists for exactly the session where the remembered fact is wrong.

**Reading a file while a sweep was mutating it.** Partway through the background sweep I read the
test file from the working tree and got the transient swapped-in state rather than the current
one. No harm resulted — I noticed the missing imports immediately, and everything afterwards was
read from Git blobs rather than the working tree — but it is a real hazard of running a
file-swapping harness in the background, and the correct discipline is to read from `git cat-file`
while any sweep is live.

## Decisions I made

1. **Approve both blobs unchanged.** Both findings correct, both implementations correct, both new
   tests measured non-degenerate, no production code touched, all suites green. Step 2 closes.
2. **Do not raise the constructor draw-order observation as a defect.** Recorded instead, with the
   reason, in both the chat and this report.
3. **Write the public log entry now.** My own carried note said the next public entry was mine and
   owed a plain-language introduction of rung 2 — the previous entry used four terms that appear
   exactly once in the whole public README. The module loop closing is the trigger that note named,
   and the running log's own precedent records internal milestones at this granularity.
4. **No Transcript Order Monitoring entry.** I verified at the Git level rather than assuming:
   Codex's Session-113 commit touches the Phase-2 transcript as a single tail hunk
   (`@@ -31268,3 +31268,98 @@`, +95/−0, in a file of 31,270 lines) and does not touch the
   monitoring file at all. No violation and no open proposal to close, so an entry would be a
   journal entry rather than a record. The check is recorded here instead.
5. **Offer step 3 rather than start it.** The loop closed this session; writing the executable is
   authorized but is a full session's work, and I asked Codex in the handoff whether it would
   rather write it.

## Insights

**The instrument I was proudest of last session is the one that got qualified this session, and
that is the correct outcome.** The every-parameter-gradient test is genuinely general and
genuinely valuable; what it is not is complete. A test's breadth and its depth trade against each
other, and the failure mode of a broad instrument is that its breadth reads as coverage. The
counter-discipline that worked here was Codex's: name a concrete wrong implementation that passes
the broad test, then build the narrow instrument that separates them.

**The cross-agent digest convention operated for the second time.** My measured prior digest for
the Phase-2 transcript equalled the post-write digest Codex published in its own Session-113
report, byte for byte, at 1,942,223 bytes. Two agents, two sessions, two independent measurements
of one object, agreeing. It stays non-blocking and its scope is unchanged: an absent prior digest
is not a fault.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my owner re-review and explicit approval (+147/−0; 1,942,223 → 1,950,094 bytes;
  post-write SHA-256 `2566e16f689b6003de115ed42f736e8373793a5b3983e9489f6cab8580bd6db3`).
- `README.md` (root, public Live-Run) — one running-log entry introducing rung 2 in plain words and
  reporting the review (+1/−0; 141,815 → 144,275 bytes). Banner untouched: it already read
  2026-08-10 and the phase has not changed.
- `agents/Claude/Session Summaries/HumanReport114.md` — this report.
- `agents/Claude/README.md` — workspace index refreshed.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 115.

**Deliberately unchanged:** the rung-2 module and its tests (I approved them, I did not edit them),
the frozen rung-2 design, every Stage-1 executable / plan / result / artifact / checkpoint, the C7
analysis and its artifact, the Claim Sheet, both `.gitattributes`, both `.gitignore` files,
`director_requests.md`, and the still-absent final configuration.

## Resource and evidence boundary

Zero fits, zero checkpoints, zero rollouts, zero data generation, zero plan actions, zero C7
invocations, zero analyzer invocations, and zero pilot / validation / test reads. No manifest, no
`.npz`, no label payload and not one byte of any `.pt` was opened. The mutation sweep and both
probes ran on synthetic tensors and synthetic `TrainingExample` objects. No capacity was selected,
no threshold set, and the final configuration remains absent.

Rollouts remain **278**. Lifetime fits remain **13**. Stage 1 remains finished as scoped and still
licenses only its no-readable-shape sentence.

## Next steps

1. **Step 3 is authorized and is the next work:** `Reproducibility Packet/scripts/utils/rung2_escalation.py`
   and `tests/test_rung2_escalation.py`, mine to write and Codex's to review. I offered Codex the
   option of writing it instead; if it declines, I take it in Session 115. Read design section 4.4
   before writing one line of the copied fitting loop.
2. **Nothing else is authorized by this closure.** Plan mode, fits, the analyzer, capacity
   selection, thresholds and the final configuration each remain separately gated, and five joint
   gates stand between today and any rung-2 number.
3. The 55-checkpoint clean-machine recovery/distribution limitation remains open for Phase 3.
4. Director request 1 (Claim Sheet review) is still non-blocking and still awaiting a reply;
   nothing is blocked on it.
