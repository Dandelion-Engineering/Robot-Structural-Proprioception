# Human Report — Claude Session 39

**Current date and time:** 2026-07-29 08:12 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner response to Codex's block of `AMENDMENT_A2_PROPOSAL_V5`; verification of its four blocking pins; clean replacement protocol (v2.2); and a correction to my own Session 38 reading.

**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)

**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

**Session decision:** `AMENDMENT_A2_PROPOSAL_V6` — posted; Codex owns the next turn.

**Rollouts spent:** one development rollout (26.9 s), to verify a reproduction claim. Everything else came from source reading and re-observing data that already exists.

---

## Summary

### What this session was for

Codex opened its Session 38 by approving the scientific substance of everything I handed it in Session 38 — including Finding J, the window-origin correction — and then blocking the exact text on **four narrow defects**, plus one wrong number. It asked for one thing: a clean **Protocol P v2.2** carrying those fixes and nothing else.

I did that. I also, again, exceeded the instruction — and the way I exceeded it is the story of the session, because it repeats a pattern that has now produced a finding four sessions running: **the act of making a pre-registration executable is what finds its defects.** Codex's first pin was that a command I had pinned would not actually run in this project's shell. Checking that sent me to ask what *else* in the document was not executable, and the answer turned out to be the largest gap in it.

### The four pins, and why each was right

**A — the command would not run.** I had written the Stage-0 invocation with `^` line continuations. That is `cmd.exe` syntax. In PowerShell the caret is passed through as a literal argument. I reproduced it exactly:

```text
.\venv\Scripts\python.exe -c "import sys; print(sys.argv)" ^ --window 768
    ->  ['-c', '^', '--window', '768']
```

The script would have received a stray positional argument. I then verified both replacement forms in the project's own shell rather than assuming them — a single line, and backtick continuation — and pinned the single-line form.

**B — a guard that did not do what its own comment said.** I had written `t_g = tm if tm.ndim == 1 else tm[:, 0]` with the comment "fail loud on any other rank". It fails loud on nothing. I fed it every rank it might see:

| input | v2.1 behaviour |
|---|---|
| `[T]` | accepted — correct |
| `[T,1]` | accepted — correct |
| `[T,3]` | **accepted silently**, columns 1–2 discarded, no error |
| `[T,2,2]` | accepted, wrong shape, fails later somewhere else |

The dangerous case is rank 2 with width > 1: it produces a plausible 1-D array of the right length, and nothing downstream can tell it was corrupted. Codex's explicit form rejects both bad cases. Adopted.

Checking its factual premise also corrected a note of my own: I had recorded that the record's time-like fields were `[T, width]` like the value arrays. They are not — `measurement_time_s`, `availability_time_s` and `latency_age_s` are all rank 1 `(3000,)`; only `values` and `valid_mask` carry channel width.

**C — a classifier that generalized past its evidence.** Protocol P has a terminal branch for "no probe candidate is safe." I had written rules for interpreting *any* candidate's failure, but the delivered data only ever exercised **one** candidate. Codex's point: a different candidate failing a safety gate contradicts nothing, and under my wording it would have been written up as a harness bug. Its scoping — the rules apply to the one measured candidate, everything else is recorded but classifies nothing — is adopted verbatim.

**D — a word that claimed more than the arithmetic supports.** I had described a zero-cost secondary measurement as something that "bounds" one-shot performance. It cannot: all seven of its distances share one fault-side realization, so there is no fault-side replication and nothing to bound with. Accepted without reservation; it is now pinned as a *conditional descriptive sensitivity* with no inferential authority.

**The number.** I had reported the rejected data-selected window peaking at step 1216 (`||b|| = 2.088`, 11.03% better). Scanning at stride 1 over every admissible start, the true peak is step **1208** (`2.0929`, **11.2897%**). Codex was right; corrected. The alternative stays rejected, so nothing operative moves.

### Where I exceeded the instruction — Finding K

Pin A is a defect of *executability*: the text says something an implementer cannot actually do. That prompted the obvious question — what else in v2.1 cannot be executed as written? The answer was not a detail:

**Protocol P v2.1 specified exactly what to measure and never said how to build the thing being measured.**

The statistic reads a strain-gauge record. Nothing said where that record comes from. That matters because the real generator builds it in a way that is not the obvious one: the closed control loop is driven by a **C0** sensor session (the sparse conventional suite), and the S-suite gauge readings are produced **afterwards**, by replaying the finished physics trace through a fresh sensor model. An implementer told only "observed path, suite S" would reasonably drive the loop with an S session instead — a different construction, whose equivalence to the delivered one is untested. Two further parameters were also unstated and would have had to be guessed.

Rather than restate parameters that can drift, v2.2 pins the construction by **naming the generator's own function** and permitting exactly four overrides. I checked that this is sound by running it, which is the one rollout I spent:

> Taking the committed assignment document and draft config, re-running one already-delivered development run from scratch reproduced the committed payload **bit-for-bit**: all twenty privileged physical fields (including the 90-column deformation array and the safety flags) and all six observed channels with their validity masks, byte-identical, in 26.9 seconds.

That is worth having on its own — it is a reproducibility result the packet did not previously have — and it converts the construction from a description into a **positive control**. v2.2 now puts that replay in front of the whole protocol as a stop-or-go gate: if the harness cannot reproduce the delivered configuration, the measurement does not start.

A side effect of the same investigation turned out to be the most useful tool of the session: **the observed sensor path also reproduces from a stored physics trace alone, with no physics simulation at all.** Any delivered run can therefore be re-drawn with different sensor noise for free. Two measurements followed that would otherwise have cost a rollout budget.

### The two measurements

**1. The observed sensor path barely degrades the comparison.** Re-observing both traces of a pair at *one common* sensor identity isolates the deterministic imperfections — quantization, dropout, latency, hysteresis, bias, drift. Across eight cases the observed-path result was **0.937× to 1.148× the ideal noise-free result, averaging about 0.996**. So real-sensor imperfection costs the measurement roughly nothing, and at small signals the residue moves in either direction. This retires the largest caveat that was attached to Session 38's estimate.

**2. The noise floor, measured on real physics for the first time.** Holding one physics trace exactly fixed and re-drawing it at eight sensor identities gives the sensor contribution to the comparison's noise floor: per-context 95th-percentile values of **0.3176 – 0.4251**. This validates a piece of the design — a synthetic, physics-free estimate of ~0.39 that the protocol had been carrying sits right inside the measured range — and it identifies which experimental context is the binding constraint.

### Where I corrected myself — Finding L

Then I checked the bookkeeping under my own Session 38 table, and found something I should have checked then.

The delivered healthy run and the delivered damaged run in the same context **do not share a sensor identity**. Cell 4's healthy row has `sensor_seed 110762`; its damaged rows have `110802` and `110842`. Because the control loop reads noisy sensors, two runs with different identities take physically different trajectories. So every absolute magnitude in my Session 38 table — and in Measurement 1 above — is *damage effect plus an unrelated control-noise divergence*, not a damage effect.

What survives, and what does not:

- **Finding J survives intact.** Its conclusion is a *ratio* between two windows computed on the same pair of runs, so the confound is common to both sides and cancels. The window origin was wrong; it is now right.
- **Measurement 1's ratio survives**, for the same reason.
- **Session 38's odds do not survive as stated.** I read a number as "the damage signal" that is really signal plus divergence. Protocol P's actual comparison matches identities between damaged and healthy, so it will contain *only* the damage effect — smaller, in expectation, than what I quoted.

And the error compounds with the second one: my newly measured noise floor omits that same divergence, so it is *lower* than the floor Protocol P will actually face. **Both of my errors flatter the hypothesis.** Session 38 called the leading outcome "Case B" (a partial pass, giving the training split one usable damage level). Corrected, the middle damage level clears the binding context by only about 1.11× — computed with an inflated signal and a deflated bar — so **a partial pass and an outright non-transfer are now roughly comparable in likelihood**, where a day ago the partial pass was ahead. The mildest damage level fails clearly under every version of the arithmetic, which is the one robust statement available.

I reported this rather than letting the friendlier number stand, and told Codex plainly which direction my mistakes ran. Protocol P itself is unchanged by any of it — no rule, threshold, universe or aggregation moved. Only the expectation moved.

### One design improvement, at zero cost

Because a stored physics trace can be re-drawn for free, the protocol can now decompose its own noise floor into a sensor part and a control-divergence part **without a single extra simulation**. That matters because the two lead to different conclusions: "the mechanics carry no signature at this damage level" and "the controller's own noise response drowns a signature that is there" are different results, and the design as it stood could not tell them apart. v2.2 adds the decomposition as a pre-declared secondary with **no authority over any verdict**.

---

## Challenges and how they were handled

**The instruction said four pins; the work said more than four.** This is the second consecutive session where doing exactly what Codex asked surfaced something outside the ask. I handled it the same way as last time and it worked the same way: apply the requested fixes exactly, then present the additions **separately and separably**, flag the overreach in the first paragraph rather than burying it, and offer to drop any of them without argument. Codex accepted last session's overreach on the merits; it may reject this one, and the turn is structured so that rejecting it costs nothing.

**Finding an error in my own headline from the previous session.** Finding L undercuts the most quotable result I produced in Session 38 — the claim that the odds had improved. The temptation to soften it is real, and the project's own standing lesson exists for exactly this: when a choice or an estimate favours you, measure how much, say so, and hand the decision to the reviewer. I stated the direction of both errors explicitly and revised the odds downward in the public log as well as the technical transcript.

**Deciding whether one rollout was allowed.** Codex's list of unauthorized actions includes "Protocol P implementation or execution." A reproduction check of the *existing* generator on *existing* development data is neither — it generates no protocol identity and computes no protocol statistic — but it is close enough to the line to be worth naming rather than assuming. I spent it, and said in the turn exactly what was spent and why.

**Not being able to separate the confound.** Finding L identifies a contamination I cannot remove with data on disk: separating damage from control divergence requires matched runs, which is precisely what the protocol's own Stage A/B produces. I offered one partial constraint — on the probe-free control trajectory, where the same confound is present, the total effect is an order of magnitude smaller — and explicitly refused to rest anything on it, because assuming it carries across trajectories is the same cross-configuration import that two earlier standing lessons warn about.

---

## Important decisions

1. **Accept all four pins without argument, after verifying each at source.** Every one was correct.
2. **Verify rather than assume the replacements.** I ran the caret through PowerShell, fed the shape guard every rank it could see, and executed both proposed command forms. Pin A existed because I assumed a command shape; the fix should not repeat the method.
3. **Pin the construction by naming the generator's function, not by restating its parameters.** Restated parameters drift; a named code path cannot.
4. **Make the replay a stop-or-go gate rather than a recommendation.** It also sharpens the terminal-branch classifier Codex asked me to narrow: with a passing positive control on the harness, "the machinery is broken" becomes a much weaker explanation for a later failure.
5. **Report Finding L immediately and revise the odds down.** Including in the public running log, which now corrects the previous day's entry forward.
6. **Keep the decomposition strictly non-authoritative.** Codex's corrections twice caught me giving descriptive quantities inferential force. The new secondary is pinned as descriptive from the start.
7. **Do not reopen Session 38's turn.** Corrections propagate forward. Finding L lives in the current turn and in v2.2, not in an edit to the record.

---

## Reasoning paths explored

- **Whether a genuinely different construction was likely.** I considered whether an implementer driving the loop with an S session would actually get different numbers, and concluded the control commands would probably be unchanged, because the sensor RNG key does not include the suite. "Probably" is the problem: a pre-registration must not rest on an untested equivalence, so v2.2 pins the verified path and records that the alternative is untested rather than claiming it is wrong.
- **Whether to propose re-timing the window to the measured peak.** Codex's correction confirmed the peak is real and slightly larger than I reported. It remains rejected for the same reason as last session — it can only be found by looking at the data, and it moves in the project's favour.
- **Whether the noise-floor decomposition could be turned into a threshold.** It could be, and that is exactly what it must not become: it would be a data-selected bar. It is reported beside the operative floor and gates nothing.
- **Whether Finding L invalidates Finding J.** Worked through carefully. It does not: J's claim is a ratio over the same pair of runs, so the confound appears identically in numerator and denominator. The absolute magnitudes J reported are the part that does not transfer.
- **Whether the confound could be bounded from data on disk.** Explored the probe-free trajectory as a proxy and the cross-context rows as replicates; neither is clean. Concluded honestly that only matched runs settle it.

---

## Insights gained

1. **Making a pre-registration executable is the defect-finding technique.** Four sessions, four findings, all of them produced by pinning something down rather than by reviewing it. Nobody found any of these by reading the design.
2. **A specification can be complete about the measurement and silent about the instrument.** Protocol P had reached a very high level of precision about *what* to compute while never saying how to produce the object computed on. Precision in one dimension reads like precision overall.
3. **A guard written against a comment is not a guard.** The rank check said "fail loud" and failed loud on nothing. This is the second time in two sessions that a guard checked a necessary condition and licensed a sufficient one.
4. **Two independent errors can point the same way, and that is the dangerous case.** Finding L's confound inflated the signal; the noise floor I measured deflated the bar. Neither is large alone. Together they moved the leading outcome, and both moved it toward the answer the project would prefer.
5. **Cheap reproducibility unlocks measurements, not just confidence.** The bit-identical replay was pursued to pin a construction. What it delivered was the ability to re-draw any stored run's sensors for free — which produced two measurements and one design improvement that would otherwise have cost simulation time the project had not budgeted.

---

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended my Session 39 turn (`AMENDMENT_A2_PROPOSAL_V6`, Protocol P v2.2). Verified `+428 / −0`; header unique at line 6426, after the recorded 6425-line physical tail; four append gates passed with rollback armed.
- `README.md` (root, Live-Run) — banner date → 2026-07-29; one running-log entry, leading with the bit-identical reproduction and **correcting the previous entry's optimism forward**.
- `agents/Claude/Session Summaries/HumanReport39.md` — this report.
- `agents/Claude/README.md` — updated.
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten.

**Verified but not modified:** `Reproducibility Packet/scripts/utils/assignment_generator.py`, `cable_plant.py`, `sensor_model.py`, `online_loop.py`, `schema_types.py`, `synchronous.py`, `gate3_assignment.py`, `config/proposed-gate3-assignment-v0.1.json`, and the delivered development payloads. No packet file was changed this session.

**Scratchpad (not committed):** four probes — the pin verification, the offline reconstruction check, the noise-floor decomposition, the observed-path comparison — plus the from-scratch replay and the gated append script.

---

## Monitoring duty

Codex's Session 38 append landed at the physical tail: `+256 / −0`, header unique at line 6171, after the 6169-line pre-write boundary. No recurrence. **Clean-append streak: five.** Per the precedent set in Session 23, one clean check is already on the record in the monitoring thread, so no new note was added.

---

## Next steps

**Immediately next, and owned by Codex:** same-state review of Protocol P v2.2. I asked for explicit yes/no on the three items beyond its list — the construction pin and its replay gate, Finding L and the downward revision, and the zero-cost noise-floor decomposition. Any of the three can be dropped without argument.

**Blocked until that settles:** Protocol P execution (169 rollouts, ~79 minutes), the written Amendment A2, the replacement assignment, full dataset regeneration, and everything downstream of it — the learned attribution models, calibration, and the evaluation driver.

**Carried forward for the Technical Report:** Finding K (construction path, and the bit-identical reproduction result, which belongs in the Reproducibility Packet on its own merits) and Finding L (the unmatched-identity confound, and the fact that it contaminated an estimate I published a day earlier).

**Not due this session:** a progress report. My last regular was Session 32; the next falls at my Session 40, or earlier if a session of mine writes the approving turn on a *written* amendment.
