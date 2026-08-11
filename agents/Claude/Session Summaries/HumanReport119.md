# Claude — Human Report, Session 119

**Date and time:** 2026-08-11 08:44 PDT

**Phase:** Phase 2 — Execution

**Progress-report session:** No. Session 119 is not a multiple of eight, no phase transition closed here, and no Claim-Sheet amendment was approved. My next regular progress report is **Session 120**.

---

## Summary

This session spent the last gated action standing between the completed rung-2 training run and the pre-registered read of it. **The read ran, once, and it succeeded.** Concretely:

1. I confirmed that Codex closed the step-6 review loop at my exact bytes with no edit, so there was no owner re-review for me to do.
2. I ran a **57-check preflight** that drives the analyzer's own authentication chain against the real state and **stops strictly before the derivation**, and then issued my half of the two-part production authorization. Codex had issued the other half in its Session 118.
3. I ran **the one authorized invocation**. `X_ANALYSIS_OK`, exit code 0, **11.97 seconds**, zero fits, zero checkpoints, zero rollouts, zero generation, zero reserved-role reads.
4. I audited the resulting artifact with a **165-check independent instrument** that imports nothing from the analyzer and re-derives every published number from the primary documents using arithmetic written inside the audit itself. All 165 passed. I approved those exact bytes and handed step 7 to Codex.
5. I found and reported **one substantive observation about what the run actually contains**, which I think is the most important thing in this session and which I describe in full below.

**What is still not done, and deliberately:** section 5.4 — the pre-registered interpretation — has **not** been applied. It requires both agents to have reviewed the exact derived artifact and then to apply it jointly. Codex's review is the open loop. Nothing in this session states what the numbers mean.

## The seven-step rung-2 sequence, and where it now stands

The rung-2 escalation was designed in Session 111 as seven separately gated steps, precisely so that no single session could carry the work from "we wrote a program" to "here is what it shows." The state after this session:

| step | what it is | status |
|---|---|---|
| 1 | the design document, reviewed and frozen | closed, both agents, Session 112 |
| 2 | the network module and its 71 tests | closed, both agents, Sessions 113–114 |
| 3 | the training executable and its 142 tests | closed, both agents, Session 115 |
| 4 | the zero-fit plan artifact | closed, both agents, Session 116 |
| 5 | the training run itself, two authorization halves | **spent** — one run, Codex Session 117, 12 fits |
| 6 | the read-only analyzer and its 103 tests | **closed, both agents** — I built it S118, Codex approved it unedited S118 |
| 7 | both agents review the derived artifact, then apply §5.4 jointly | **open on Codex** ← we are here |

Between steps 6 and 7 sits a gate that is not numbered: the analyzer had to be *authorized to run* as a separate act from being *approved as code*. That is the gate this session closed. The project's standing rule is that **a closed review loop authorizes the next step only and never a run**, and this is the third time that rule has forced an explicit second authorization where a less careful process would have simply executed.

## What I did, in order

### 1. Confirming there was no open loop of mine

Codex's Session-118 turn approved analyzer blob `7cf3cc6a…` and test blob `a642b3d3…` **as-is**, with no edit. The review cycle only bounces back to the owning agent when the reviewer edits. It did not, so step 6 closed at bytes both of us had already named, and I moved to the authorization gate rather than re-reviewing my own file.

### 2. The preflight — 57 checks, and it stops before the answer

The discipline I have used at every previous execution gate is that a preflight must exercise everything the run depends on **except the thing the run exists to produce**. If the preflight computes the answer, the authorization is theatre. So this one calls the reader's own validators against the real files and then halts: it never calls `derive_analysis`, never loads a development row, never re-scores a checkpoint, and never reads a comparison number out of the record.

| part | checks | what it established |
|---|---|---|
| A | 11 | the analyzer on disk is byte-for-byte the approved state — raw digest, Git blob, 48,308 bytes, 1,125 lines, pure ASCII, no carriage returns, one final newline — and the working tree carries no modification anywhere in the packet |
| B | 17 | every one of the five input documents reproduces the digest the authorization names, each in its correct domain; the two raw run artifacts were additionally shown to contain **zero** line endings, so the raw-versus-canonical distinction that caused Finding AV last month cannot arise for them |
| C | 20 | the analyzer's 14-entry code identity is sorted, uses bare filenames, and is a strict superset of the run's 12-entry producing identity; **all ten training arms carry one identical fitting identity and it is the run-level identity**; every one of the twelve entries equals the current on-disk digest; the envelope validator accepts; ten training arms, two gate arms and ten anchors all validate; and I hashed **all twelve checkpoint files myself** and each reproduced the digest the record names |
| D | 9 | the destination directory and artifact are absent and outside the run's own namespace; and in a scratch copy, a first write succeeds, **a second write refuses by name**, and the first artifact survives that refusal byte-identical |

I also re-ran the analyzer's 103 focused tests at these exact bytes: `103 passed in 1.95 s`.

### 3. Issuing my half, and naming what I could not close

I posted my authorization half as its own turn in the technical chat: the exact command with all nine required arguments, every digest **re-measured this session rather than copied from Codex's half**, the destination state, the maximum budget, and an explicit list of what the authorization does not license.

I also named five residuals rather than letting them pass silently. The two worth repeating here:

- **What gets spent is the pre-registration, not the bytes.** A gate can only refuse a state it was built to see. It cannot refuse a state nobody thought of. This has been true at every execution gate in this project and restating it does not make it smaller.
- **The destination's absence is a measurement with a gap after it.** Something could in principle write there between my measurement and the invocation. No measurement closes that. What closes it is the second layer — the exclusive create, which I drove in scratch this session and which turns the hazard into a named refusal rather than a silent overwrite. I said which layer I was relying on instead of implying the measurement covered it.

### 4. The run

```text
Gate-4 rung-2 escalation descriptive read (zero fits, zero rollouts)
rung-2 arms: 10; equivalence arms: 2; anchors read: 10
objective-reduction status: OPTIMIZATION_CHECK_PASSED (10 of 10 arms)
paired macro-F1 sign label: MIXED
BOUNDARY: development-only in-sample description; no rung, capacity or threshold selected.
```

Exit code 0, 11.97 seconds. The artifact:

```text
Reproducibility Packet/results/rung2_escalation_analysis/rung2-run-1/rung2_escalation_analysis.json
  Git blob     a2fa857b7df14baefc047bf0b8b4b7a4d87c7b43
  raw SHA-256  604d72724b4cf11a97ce0af836ecef1163442e9ff7e6423aa2fd0fad9556951c
  40,270 bytes / one canonical line / no line endings at all / pure ASCII
```

Both halves are now spent. There is no retry authority and I did not ask for one.

### 5. The audit — 165 checks by a second instrument

The rule I hold myself to when reviewing a derived artifact is that **the reviewing instrument must not share code with the producing instrument**, or it is a report of a check rather than a check. This audit imports nothing from the analyzer. It re-computes every mean, every sample standard deviation, every difference, every six-decimal rendering and every sign count with arithmetic written inside the audit file, and it walks the anchors' recorded field paths into the approved rung-1 analysis by hand.

| part | checks | what it established |
|---|---|---|
| A | 7 | the artifact is one canonical line; re-serializing the parsed object reproduces the file **byte for byte**; no `NaN` or `Infinity` token anywhere; exactly the eleven declared top-level fields |
| B | 24 | §5.3's prohibitions hold — no p-value, confidence interval, significance, power, minimum-detectable-difference, trend, slope, or any of the forbidden causal connectives; the word fragment `generaliz` occurs **only** inside the boundary flag `generalization_established`, checked by position rather than by count; and no absolute path, UNC path, home-directory name or project-directory name appears |
| C | 27 | all five input digests and the design digest reproduce from their files, and the design digest is the frozen jointly approved one; the recorded fitting identity equals the run record's own; and **each of the fourteen code-identity entries re-digests from the file it names on disk** |
| D | 10 | every carried field of every training arm is bit-equal to the terminal record's own value; each arm's objective-reduction flag was re-derived from that arm's own loss history; twenty epochs each; the right parameter count and receptive field on every arm; ten distinct checkpoint digests |
| E | 7 | every anchor's recorded field path was walked into the approved analysis **by the audit** and found to hold exactly the published value — read, never recomputed — and each anchor checkpoint digest was matched against **two different documents** |
| F | 7 | the objective-reduction status was re-evaluated from §5.1's own conjunction and gives exactly the published result |
| G | 70 | for macro-F1 and each of four per-class metrics: the per-seed rows carry the seeds in order, each row's two sides are the two arms' own values, each raw difference recomputes, each six-decimal string renders its own raw value, and mean, sample SD and sign counts recompute **exactly** — not to a tolerance. Both rung-comparison blocks likewise, and both confirmed to carry no sign count and no label. The three-valued label was re-derived twice by two independent routes and both gave the published name |
| H | 7 | the development census, class counts, out-of-distribution counts, trajectory census and baselines are present and consistent with every arm's example count |
| I | 6 | the run's namespace still holds exactly fourteen files, the two raw run artifacts are byte-unchanged, the output directory holds exactly one file, and **the project-wide checkpoint count is still 67** |

All 165 passed. I approved those exact bytes.

## The observation that matters, and why I reported it before anyone interprets anything

While auditing, I found something in the record that a reader needs and that no pre-registered sentence covers. It is a description of persisted values, not an interpretation, and I attached no cause to it.

**Every one of the ten rung-2 arms scored exactly zero on two of the four classes.** All ten have `healthy` F1 = 0.000000 and `structure` F1 = 0.000000. Four of the ten sit exactly at the majority-class baseline the artifact itself records — an accuracy of 0.631579, which is what you get by answering "sensor" to every example on this census of 32 actuator / 8 healthy / 96 sensor / 16 structure out of 152. The other six produce a non-zero score on `actuator` and nothing else. **The smaller rung-1 networks, in the same artifact, are not like this**: all ten of those produce four non-zero per-class scores.

Three consequences, which I put in the chat before either agent writes a sentence:

1. **The zeros in the paired comparison for those two classes are "both sides zero," not "both sides equal."** A sign count of five ties is arithmetically correct and descriptively hollow when both arms scored nothing. The same applies to one seed's macro-F1 tie: both arms are sitting at the majority-class value.
2. **This is precisely the hazard the design pre-declared, arriving.** Section 5.1 says, in writing and before any of this ran, that the training objective contains a term whose scale can drive a reduction without improving classification, and that the objective-reduction check is therefore *not* a learning signal. Ten of ten arms reduced the objective. The check certified exactly what it said it would certify and nothing more. That is the system working, not failing — but only if someone says so out loud.
3. **It is not a recording error.** The analyzer re-scored all ten checkpoints from their authenticated bytes against the development rows and demanded **exact** equality with the persisted numbers. The run returning success means that equality held ten times over. These are properties of the saved weights.

I am not proposing an amendment, not asking for a retry, and not attaching a cause — not capacity, not protocol, not optimization, not data. What I asked is that the Technical Report carry this paragraph next to whatever the frozen interpretation licenses, because a sentence saying the larger rung is built and fitted, standing alone, would be true and would leave a reader with a materially wrong picture of what the run contains.

## Challenges, and how they were handled

**My own audit was wrong three times before the artifact was right once.** The first run failed on a status string I had spelled in the wrong case, the second on a field-path walker that assumed a structure the artifact does not use, the third on an assumption that a mean is a bare number when the artifact publishes it as a `{raw, quantized}` pair.

I reported all three rather than quietly fixing them, and the third one taught me something about my own design that I had not appreciated when I wrote it. The artifact publishes both the full-precision float **and** its six-decimal rendering side by side, so a reader never has to guess which domain a number is in. That is the lesson of an earlier finding — where a comparison silently crossed a rounding boundary and could not have completed — built into the *schema* rather than into a comparison. My audit tripped over it because it assumed the simpler shape. The stricter shape is the right one.

There is a general point here that I want on the record: **an audit that passes on the first attempt has usually not been calibrated.** The three red runs are what tell me the instrument was actually reaching the artifact rather than agreeing with it.

## Decisions I made

1. **I ran the invocation myself rather than handing the second half back.** Codex issued half one and explicitly left the matching half to an independent preflight. The established pattern in this project is that the agent issuing the second half spends both, and doing otherwise would have added a session of latency for no gain in independence — the independence lives in the two separate preflights, which happened.
2. **I did not update the public Live-Run README.** Codex ruled in its Session 118 that public logging should be reconsidered only after the joint read, and the reasoning is sound: a log entry written now would either say nothing or start interpreting. The heartbeat check happened; the answer was "not yet."
3. **I accepted Codex's runbook ruling in full.** The packet runbook still has no step for the rung-2 lane. Codex ruled that I should write one edit containing two consecutive steps — the module/plan/run first, then the analysis read naming this exact digest — after step 7, so the second step can name a jointly reviewed state instead of a state that must be rewritten a session later. Agreed, and I wrote no interim version.
4. **I reported the degeneracy observation in the technical chat rather than saving it for the report.** It bears on how section 5.4 should be read, and section 5.4 is applied jointly. Discovering something that changes how a joint act should be performed and then holding it until after that act would be the wrong order.

## Reasoning paths explored, and one I rejected

I considered whether the degeneracy finding should be raised as a **defect in the artifact** rather than an observation about it — that is, whether the analyzer should have flagged it. I decided it should not, and the reason is worth stating: the analyzer publishes the per-class scores, the accuracy, and the majority-class baseline in the same document, so a reader holding **only** the artifact can perform this comparison unaided. Adding a derived "degenerate" flag would mean adding a criterion that the frozen design does not contain, in the same session that criterion's answer became visible. That is exactly the shape of post-hoc rule-making the whole gated structure exists to prevent. The right place for the observation is the report and the review, not a new field.

I also considered whether the observation constitutes grounds for the design's failure path. It does not: the failure path is defined by three specific branches — equivalence failure, incomplete run, and objective-check failure — and none of them occurred. Reading the failure path as "or anything else that looks disappointing" would make its pre-declaration meaningless.

## Insights gained

- **A check that certifies a narrow property does its job when the narrow property turns out to be the only one that holds.** The objective-reduction gate was written to be weak, and it was written to say so. Ten of ten arms passed it and the classifications are largely degenerate. That is not a gate failure; it is a gate that was honestly labelled. The value of pre-declaring a check's weakness is realised precisely on the day the weak version passes.
- **Publish the number and its rendering together.** The one design decision of mine that my own audit stumbled over is the one that removes an entire class of error from a future reader's path.
- **Reviewing instruments must not share code with producing instruments** — and the practical test of whether they are genuinely separate is whether the reviewing instrument can be *wrong in its own way*. Mine was, three times. Shared code cannot be wrong in its own way.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended two turns: my authorization half, and the run result plus my step-7 exact-state review and the degeneracy observation.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md` — appended the monitor's entry: no order violation this session, Codex's Session-118 append verified clean at the Git level.
- `Reproducibility Packet/results/rung2_escalation_analysis/rung2-run-1/rung2_escalation_analysis.json` — **new, tracked.** The derived artifact, blob `a2fa857b`, raw `604d7272…`.
- `agents/Claude/README.md` — the rung-2 bullet's current-state lead updated in place.
- `agents/Claude/Session Summaries/HumanReport119.md` — this report.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 120.

Not modified: the frozen design, the network module and its tests, the executable and its tests, the consumed plan, the two raw run artifacts, the twelve checkpoints, the analyzer and its tests, the public README, the delivered dataset.

## Resource accounting

```text
fits                              0
checkpoints written               0
rollouts                          0
generation runs                   0
pilot / validation / test reads   0
production analyzer invocations   1   ← the one authorized, both halves spent
```

Project-wide totals, re-derived from the artifacts' own ledgers rather than remembered: **67 fits, 67 checkpoints, 278 rollouts.** The checkpoint count was measured on disk again this session and is unchanged.

## Next steps

1. **Codex reviews the derived artifact at blob `a2fa857b` / raw `604d7272…`.** This is the one open loop in the project and it is the whole of step 7.
2. **Only after that: section 5.4, applied jointly.** One status sentence plus, because the status row is the successful one, exactly one sign sentence. No causal connective may be attached to either.
3. **Then the packet runbook edit** — one review cycle, two consecutive rung-2 steps, mine to write, per Codex's ruling.
4. **Then the public Live-Run README**, reconsidered as Codex ruled.
5. Everything else stays blocked: no capacity or rung selected, no threshold set, no generation, no rollout, no reserved-role read, and the final configuration remains unfrozen.
