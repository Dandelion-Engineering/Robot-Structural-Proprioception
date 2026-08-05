# Claude — Human Report, Session 77

**Date and time:** 2026-08-05 04:36 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.

---

## Summary

Amendment A2 came into force between my last session and this one — Codex approved the exact
two-file state I had approved in Session 76, and the review loop closed. That mattered for
what I did next: A2 was the last written gate standing in front of **Gate 4**, my own lane,
which is where the project's headline method lives. After four consecutive sessions whose
only output was a narrowing of our own claims — correct sessions, but I had written down a
warning to myself that a fifth would mean we were polishing instead of moving — this session
built something.

**The project's first learned model now exists.** It is untrained, and by design it is not
permitted to answer.

## What I did first: confirmed A2 rather than assuming it

Codex's Session-76 report says the amendment is in force. I checked three things against
primary sources rather than against the report:

1. The accessible-sheet blob it approved is byte-for-byte the one it approved in Session 75
   (`203aab77…` both times) — so nothing moved in the file I did not touch.
2. Its quoted numbers re-derive from the persisted artifact rather than from my draft: mean
   per-cell Q95 `0.4165464356091794` at 0.000 kg and `0.3990021149047824` at 0.050 kg, ratio
   `0.9578814768`. Exact.
3. Its public README entry states **both** load-bearing halves — that the contract changed
   *and* that not one success bar moved. That is the half a reader is most easily misled
   about, and it is there.

The amendment fires two duties: a progress report and a public log entry. Both belong to the
agent whose session writes the approving turn, which was Codex, and Codex did both. Writing a
second progress report here would have been padding rather than compliance, so I did not. My
next regular progress report remains Session 80.

## The main work: Gate 4, rung 1

The Claim Sheet's Slot 9 pre-commits the project to a **model-capacity ladder** — start with
the smallest model that could plausibly work, and escalate only for a stated reason. Rung 1 is
"a compact recurrent or temporal-convolutional estimator, roughly ten thousand to a hundred
thousand parameters." That rung has been described in our code as *specified, not built* since
Session 9. It is now built:

`Reproducibility Packet/scripts/utils/attribution_net.py`, with 64 tests in
`Reproducibility Packet/tests/test_attribution_net.py`.

```text
parameters        39,594          inside Slot 9's rung-1 band, and the constructor
                                  REFUSES a configuration outside it
receptive field   1,023 samples   covers the whole proposed 768-sample window
throughput        4,072 windows/s on the project GPU, peak 283 MiB of 16 GB (1.8%)
                  449 windows/s on the CPU — no GPU is required by the packet
```

The size is a decision, not a limitation. Dandelion's efficiency standard says the smallest
sufficient solution is the one that ships, and Slot 9 already named the compute story as
*breadth* — many seeds and conditions — rather than one large network. At 1.8% of the graphics
card's memory, five training seeds across four sensor suites is trivially affordable, which is
the number that makes the pre-registered statistics possible at all.

### The four properties I built in and then measured

Each is a way the whole experiment could fail quietly rather than loudly.

**1. The network is identical for every sensor suite.** The conventional robot (C1) and the
structurally-sensed robot (S) get the same architecture with the same parameter count; the
suite enters only through which input columns are marked valid. If the model could shrink
with the suite, then any advantage we later measure for S is confounded with model capacity —
"the better robot had the bigger brain" — which is the exact thing the Claim Sheet holds the
algorithm fixed to avoid.

**2. It cannot see forward in time, and the normalization cannot either.** This is the one I
think is easiest to get wrong and impossible to notice. The ordinary way to normalize this
kind of network averages across the time axis, which lets a window's later samples influence
its earlier features. No shape changes. Nothing errors. The estimator is simply no longer
causal, and our claim that it only ever reads the past is false. The normalization here is
per-timestep, and the test **measures** causality by nudging one instant of input and
confirming no earlier output moved — with a companion test showing that the ordinary
normalization *fails* that same check, so the check cannot be passing merely because the
nudge was too small to see.

**3. An untrained network is not allowed to answer.** Freshly built, its internal values are
random and carry no information about anything. It therefore declines: it abstains, splits its
four-way probability evenly, reports no location, and reports its severity uncertainty as
infinite. Weights become usable only through a call that **requires** a written record of
where they came from. Reporting the argmax of random initialization would be fabrication with
a confidence number attached to it.

**4. The decision thresholds are not the model's to set.** When to abstain and when to declare
a change both default to "always abstain, never flag." Those operating points belong to the
validation stage (Gate 5), fit on a healthy calibration set. This is the same discipline our
interpretable detector already follows: a development pilot may not hand a deployed rung its
operating point.

One related refusal is worth naming because it costs us something. The network emits a raw
uncertainty scale, and it would be easy to report that as the severity uncertainty. Session 24
measured that an in-sample scale of exactly that kind understates the true predictive error by
**5.72×** for suite S. So the module exposes it under a deliberately awkward name and reports
infinity until Gate 5 calibrates it properly.

## Two real defects found by running it

**The estimator was relocating the caller's network.** PyTorch moves a model between processor
and graphics card *in place*. My first version adopted the network it was handed, so building a
GPU estimator from a network a CPU estimator already held moved both — and, worse than the
crash that revealed it, the two estimators then shared weights, so loading trained weights into
one reached into the other. That is precisely the paired C1-versus-S and multi-seed usage this
rung exists for. It was caught only because my GPU test happened to build *two* estimators from
one network; a single-estimator test would have stayed green forever. Fixed, with two tests
pinning it.

**Processor and graphics card did not agree, and the cause was a default.** Measured across
four seeds on the same weights and the same input:

```text
PyTorch's default setting          max difference 8.842e-05 on the class probabilities
the setting turned off             max difference 5.960e-08
```

Eight parts in a hundred thousand is three orders of magnitude below our 0.05 success bar, so
it would never have changed a headline. It would have made two things false that we do rely
on: that a saved result reproduces on someone else's machine, and that a paired C1-versus-S
difference is a difference in *sensing* rather than partly in which device each arm ran on. At
forty thousand parameters the fix costs nothing measurable, so the module now pins the setting
for every forward pass and restores it afterward rather than mutating the whole program's
numerics.

## Verification

```text
focused suite         64 passed
full packet suite     1,370 passed in 132.81 s   (was 1,306; +64, no regressions)
compileall            clean
mutation sweep        15 injected defects | 15 caught | 0 survivors
                      anchor verified green before and after; original restored and re-checked
real-data wire check  one delivered development observation, read-only, no fitting:
                      768-step past-only window -> network -> validated output contract.
                      Valid fraction 0.991175 — the mask stream is live even on a healthy row.
rollouts              0.  No plan mode, no execute mode, no replay gate, no generation.
config/config.json    still absent
```

The mutation sweep is the part I would point at if someone asked whether the 64 tests are
worth anything. A green suite proves nothing on its own; the sweep breaks the code fifteen
different ways — a time-mixing normalization, non-causal padding, letting an untrained model
answer, dropping the provenance requirement, sharing weights between estimators, making the
precision fix a no-op, an off-by-one in the location decode — and every one of them turns the
suite red.

## Two things I did not decide alone

I put both to Codex rather than proceeding on my own reading.

**Is training this model on the existing development data authorized?** I did not train. The
case for yes: A2 explicitly retired the expectation that the development dataset would be
regenerated, so it is no longer slated for replacement, and A2's own list of what it does not
authorize does not mention model fitting. The case for its own gate: both agents' notes have
said "read this data, do not build on it" since Session 33, and a trained checkpoint is a
thing built *on* it. My proposal is that development-only fitting is allowed, carrying the same
"development only, ineligible for confirmatory analysis" authority string our other development
measurements carry, with pilot, validation and test untouched. Codex rules.

**A contradiction between two of our own documents.** Our estimator module says the learned
rungs are trained *after* the configuration freeze. The governing freeze decision says the
freeze comes *after* model implementation and validation-only threshold selection. Those cannot
both be true, and the direction matters: one has Gate 4 waiting on the freeze, the other has the
freeze waiting on Gate 4. I believe the gate decision governs and the module docstring is stale
— you cannot select thresholds on validation data to freeze if the model that produces them does
not exist yet. I have not edited either, because it is a claim about sequencing rather than a
typo, and the freeze plan is Codex's.

## Reasoning I want on the record

I came into this session expecting to spend it on A2's aftermath. The honest read of the state
was that A2's aftermath was already handled, competently, by the other agent, and that four
consecutive sessions of mine had produced no forward motion. I had left myself an explicit
instruction about that. Acting on it meant choosing the largest unblocked thing in my lane
rather than the most defensible small thing, and then holding it to the same standard we hold
everything else: measure the properties, do not assert them; break the tests deliberately to
see whether they notice; refuse to let the new thing answer questions it has not earned.

The thing I am least sure about is the requirements pin. I pinned PyTorch's base version
rather than the exact CUDA build our machine used, so a reader without a graphics card can
still install and run the whole packet. That trades a little reproducibility exactness for a
lot of accessibility, which is the direction Dandelion's mission points, but it is a judgment
call and I flagged it for Codex to overrule if it disagrees.

## Files created or updated

- `Reproducibility Packet/scripts/utils/attribution_net.py` — **new**, Gate-4 rung 1
- `Reproducibility Packet/tests/test_attribution_net.py` — **new**, 64 tests
- `Reproducibility Packet/requirements.txt` — PyTorch pinned, with the measured device-agreement numbers
- `Reproducibility Packet/README.md` — requirements note, test-coverage sentence, license row, and two stale sentences corrected
- `README.md` (root, public) — one milestone entry
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — the Session-77 handoff (`+199/−0`)
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md` — clean check plus independent verification of Codex's Session-76 byte event
- `agents/Claude/Session Summaries/HumanReport77.md` — this report
- `agents/Claude/README.md` — workspace index
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten resume state

## Next steps

1. Codex reviews the two new files; the review cycle is open at `5dc30c06` / `591d9031`.
2. Codex rules on development-only training authorization and on the freeze-order contradiction.
3. If training is authorized: the trainer script, with the five seeds, the matched suite loop,
   and the checkpoint provenance record — still development-only, still zero rollouts.
4. Gate 5 (calibration, abstention, out-of-distribution) is next in my lane after that, and it
   is the stage that turns the raw uncertainty head into something we are allowed to report.
5. Unchanged and still blocked: assignment replacement, dataset regeneration, the final
   configuration freeze, any pilot/validation/test generation, all confirmatory work, and any
   second payload measurement.
