# Human Report — Claude Session 51

**Current date and time:** 2026-07-31 20:37 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner re-review closing the public-README loop; then the first build session of the Stage-A/B/C work — the shared-primitives extraction and the construction layer, handed to Codex for review

**Final config state:** **UNFROZEN**; no `config.json` exists

**Protocol-P execution state:** Stage 0 has run exactly once and was **not** re-executed. Protocol P has spent one plant rollout total (the Session-45 replay). Stages A/B/C remain **unbuilt as executables and unauthorized**. The confirmatory test split remains untouched.

---

## Summary

Two things happened this session, and the second is the substantive one.

First, I closed the open review loop. Codex's Session 50 reviewed the public README I had edited and returned in my Session 50, approved it at the exact blob, and then — in a second turn, before committing — correctly withdrew its own claim that the loop was therefore closed. It had inferred my owner approval from the fact that I edited and handed the file back, even though my handoff said in as many words that I had not approved it. That is the same rule I learned the hard way in Session 48, pointed the other direction, and Codex caught it on itself. I re-reviewed the artifact as work rather than as a verdict, verified the withdrawal's scope at a wider radius than either of us had used, and approved the exact state. That loop is closed.

Second, the Stage-A/B/C work began. Stages A, B and C are the parts of the pre-registered screen that actually test the research question, and they cost 168 simulated rollouts, so nothing about them may be improvised. This session built the two pieces that come before any of that: a small module holding the rules and fixed fingerprints every part of the screen must agree on, and a **construction layer** whose entire job is to decide, before a simulation runs, whether the run about to happen is the run the specification described.

The construction layer exists because of a measurement from Session 41 rather than because of a principle. In that session we found that the safety checks that run *after* a rollout passed with roughly seventy times margin while the program was, in fact, simulating the wrong body. A check on the result cannot see a mistake in the request. So the checks that catch that class of error have to run first — and they are free, because they run before the physics does.

The extraction had a measurable side effect worth stating plainly. Session 50 discovered that the finished Stage-0 program was importing the MuJoCo physics engine even though it runs no simulation, through a chain four modules deep, and that discovery forced corrections in both the packet runbook and the public log. Moving the shared pieces into their own dependency-free module removes that import entirely: one of eight project imports before, zero after, measured in fresh interpreters before and after. The correction is now a fact rather than an explanation, and an automated test loads the script in a clean interpreter and fails if the dependency ever returns.

Everything built this session is handed to Codex for review and is **not** approved. Nothing was executed: no screen stage ran, no plant rollout was spent on the protocol, `config.json` remains absent.

---

## What was done, in order

### 1. Owner re-review and closure of the public-README loop

Codex's review was correct and short. Re-reviewing it as work rather than agreeing with it produced one thing agreement would not have: I ran the withdrawn-claim search across **every outward-facing markdown file in the repository**, not just the README that prompted the correction. That is the actual shape of the failure mode this rule exists for — a withdrawn claim surviving somewhere else — and the wider search is what licenses saying the withdrawal is complete.

```text
"physics engine"   README.md:94   2026-07-30 entry   withdrawn, covered by the correction
                   README.md:96   2026-07-31 entry   withdrawn, covered by the correction
                   README.md:98   the correction itself
                   Accessible Claim Sheet.md:169     unrelated and correct
```

No third instance exists anywhere a stranger reads. I also re-checked the two supporting claims by running them rather than recalling them (eight project imports; `mujoco==3.10.0` pinned at `requirements.txt` line 2 and installed by packet Step 1), and re-ran the per-import measurement myself instead of reusing my own Session-50 numbers. Approved at blob `73b124fd…`; loop closed.

### 2. The extraction — `Reproducibility Packet/scripts/utils/protocol_p.py`

Moved out of the replay gate, where Stage 0 had been importing them: the exception type, the fail-loud `require` helper that replaces `assert` (which `python -O` deletes), both hash-domain functions, the single JSON-serialization rule every identity is hashed through, and the two text-domain fingerprints with their filenames. The module imports only the Python standard library, which is the property that makes it safe for a consumer that runs no simulation.

The two `.npz` fingerprints stayed in the replay gate, because a pin belongs with the check that enforces it and the gate is their only reader. The `raw_file_sha256` helper did move, because the two-domain rule is a pair and shipping half of it invites the next consumer to re-implement the other half — which is exactly the defect the rule exists to prevent.

**Measured, per module, each in its own fresh interpreter:**

```text
                                      before   after
analyze_synchronous_difference_null    True    False   <- the point of the exercise
protocol_p_replay_gate                 True    True    <- intrinsic; it rebuilds a reservation
seven utils.* modules                  False   False
utils.protocol_p                         -     False
```

### 3. The construction layer — `Reproducibility Packet/scripts/utils/protocol_p_conditions.py`

It enforces seven of the protocol's invariants as preconditions and deliberately enforces none of the others, saying in its own documentation where each of the rest lives. In plain terms it decides:

- that a screen run is derived from the right delivered run, with **exactly two** fields changed and everything else identical;
- that the screen's identity cannot collide with the real dataset's;
- that the eight repeats used to build the "how much does this move anyway" baseline are genuinely distinct, and that the first of them *is* the run the earlier stage already performed rather than a lookalike;
- that a damage run and its healthy partner share one identity, which is what makes their difference a measurement of damage rather than of sensor noise;
- that the damage requested is the damage constructed — the right link, the right severity, the right instant, field by field, over a closed vocabulary of exactly two conditions;
- and that every screen result carries a stamp marking it permanently ineligible for the final analysis.

Three details I want on the record:

**The candidate-strength gate's boundary is exact, and I measured it rather than trusting the specification's prose.** The strongest admissible probe passes by exact equality — `0.15 × 2 × 0.40` and `0.60 × 0.20` are both exactly `0.12` in binary floating point, at both association orders — so writing `<` instead of `≤` would silently drop the strongest candidate the protocol admits. A test asserts the equality directly.

**Two numbers that also live in the mechanics code are checked by equality, never adopted.** The layer pins the link length and torque limit and refuses unless the live values equal them; the admissible ramp interval is checked against the mechanics validator accepting exactly half a burst duration and refusing a hair more. Reading those values instead of checking them would let the gate move silently whenever the mechanics moved.

**Two of the guards defend code rather than present-day data, and each says so in its own docstring.** This is the fourth member of a class this project keeps finding, and stating it is the difference between an honest write-up and an overclaimed one.

### 4. The verification, including the part that found a defect in my own tests

```text
full packet suite            725 passed in 13.22 s   (595 before)
new focused tests            130
replay gate                  PASS, re-run after its own edit, 25.08 s
Stage-0 measurement path     bit-identical to the approved artifact
mutation sweep               16 cases
```

I did not re-run Stage 0's pre-registered 100-pair measurement — it has been spent, and re-running it is not authorized. Instead I called its measurement function directly at two pairs, which consumes the same first seeds, and compared against the approved file:

```text
recorded artifact  0.17764883124109498   0.1894914916579524
fresh at 2 pairs   0.17764883124109498   0.1894914916579524
```

Bit-identical, so the refactor is numerically inert on the path that matters.

The mutation sweep is the part that earned its keep. Sixteen deliberate defects, one at a time, each a plausible edit rather than a contrived one. Fifteen were caught. One survivor — removing the line-ending fold from the text fingerprint — turned out to be caught by the *full* suite (Codex's replay-gate tests own that property), so it is a scope artifact of my focused sweep and not a coverage gap; I measured that rather than assuming it, and I did not add a duplicate test.

**But an earlier version of the sweep found a real gap, and it was mine.** Weakening one guard's exact-set comparison to a subset comparison survived the entire 724-test suite. The reason is precise and worth carrying: all three of my tests for that guard asserted the string `"I3"`, which appears at *both* of the function's failure messages, so the weakened guard still refused two of the three bad states — for the wrong reason — and every test stayed green. The state the weakening actually lets through is a screen run that changed only its sensor seed while still carrying a delivered run's identifier into the screen's reserved band, and I had no test for it at all. Both problems are fixed: every test now matches a phrase unique to one failure site, and the missing state has its own test. The mutation is now caught.

That is Codex's Session-48 rule finding me one session later. `"I3"` is a label, not a reason.

### 5. Documentation

The packet runbook's Step 24 said the MuJoCo package "is still imported transitively by shared input-binding code." That is now false, so I replaced it with the current state and named the test that pins it. That reopens a small review loop, which is correct — the fact changed.

I also added **one** public-log entry, and the reasoning cuts against my own Session-50 argument for restraint, so it belongs here. The newest dated entry says Stage 0 "currently imports the MuJoCo Python package transitively." Once the runbook says the opposite, leaving that alone ships two outward-facing documents disagreeing about the same fact — worse for a stranger than either being stale. I edited no dated entry; corrections propagate forward. The new entry says plainly that the code is under review and not approved.

---

## Challenges and how they were resolved

**A sequencing question I could not resolve unilaterally.** Codex's Session-46 answer made the extraction conditional on "the Stage-A/B/C driver being the third consumer." The driver *script* does not exist yet; the construction layer does, and it is a real third consumer. I judged the trigger fired, led my handoff with the deviation rather than burying it, gave three reasons (writing the driver against the old arrangement means refactoring reviewed code; bundling a refactor of approved files with a large new implementation makes one review carry two unrelated risks; and the extraction discharges an obligation I recorded last session), and handed Codex the decision explicitly. If it reads the trigger as the finished script, I will treat the extraction as premature rather than argue it.

**A guard I could not test the ordinary way.** One invariant's failure state is unreachable by construction — the value it compares against is inside the payload being hashed, so failing it would require a cryptographic fixed point. Rather than write a test that reaches it some other way and pretend, I split the check into its own function so the rejected state can be built and fed to it, then verified that the real code actually *calls* it by replacing it with something that always fails. Unit-testing both ends of a wire does not test the wire.

**A test-count discrepancy in my own report.** The suite reported 724 at one point and 725 at another; the difference is the test I added mid-session after the mutation sweep exposed the I3 gap. Both numbers are in this report because both were real at the moment they were measured.

---

## Decisions I made

1. **Do the extraction now, and say it is a deviation.** Reasoning above; the decision is handed to Codex.
2. **Do not re-run Stage 0.** Its pre-registered invocation has been spent. A two-pair call to the measurement function answers the refactor question exactly and costs nothing.
3. **Re-run the replay gate.** It is one simulated rollout as a regression check, on the precedent set in Session 46, and I edited the gate's own imports. It passed.
4. **Leave the survivor of the mutation sweep alone.** It is covered by another test file, which I measured; adding a duplicate test would advertise coverage the project already has.
5. **Add one public-log entry despite last session's argument for restraint.** Consistency between two outward-facing documents outweighs leanness when a code change makes one of them false.
6. **Do not build the driver script this session.** The parts that remain — the output root and its persistence check, the post-rollout safety gates, the label-stamp scope test — are testable only where they live, and bundling them into this review would make it worse.

---

## Files created or updated

**Created:**
- `Reproducibility Packet/scripts/utils/protocol_p.py`
- `Reproducibility Packet/scripts/utils/protocol_p_conditions.py`
- `Reproducibility Packet/tests/test_protocol_p_shared.py` (19 tests)
- `Reproducibility Packet/tests/test_protocol_p_conditions.py` (111 tests)
- `agents/Claude/Session Summaries/HumanReport51.md` (this file)

**Updated:**
- `Reproducibility Packet/scripts/protocol_p_replay_gate.py` (imports the shared module; +16/−59)
- `Reproducibility Packet/scripts/analyze_synchronous_difference_null.py` (imports the shared module; +23/−46)
- `Reproducibility Packet/README.md` (Step 24's dependency sentence; +1/−1)
- `README.md` (one new running-log entry; +2/−0)
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` (two turns; +83/−0 and +240/−0, cumulative +323/−0)
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md` (rewritten)

**Deliberately untouched:** the protocol specification, the approved assignment, the draft config, the Stage-0 result artifact, `utils/gauge_windows.py`, the detection-floor screen and its published artifacts, the generator seam, `.gitattributes`, every dataset payload, and every dated public-log entry.

---

## Next steps

1. **Codex reviews the eight handed-off states** and answers the sequencing question about the extraction's trigger, plus two smaller ones (where the binary-domain helper belongs; whether the driver's output-root boundary should be its own module).
2. **Then the driver script itself** — the executable that runs Stages A, B and C against the enumerated fail-loud requirements. No rollout is authorized before that reaches its own approval.
3. Unchanged behind that: the written A2 amendment and replacement assignment, full dataset regeneration, the learned model rungs, the controller protocol, the joint configuration freeze, and only then the one-shot confirmatory generation and evaluation.
4. My next regular progress report is due at my **Session 56**, unless a phase transition or an approved amendment triggers one sooner.

---

## One honest note on where this sits

Nothing this session moved the research question. It built the machinery that will move it, and it removed a dependency that had already cost two documentation corrections. The part I would defend as genuinely valuable is smaller and less flattering than the code: a deliberate attempt to break my own tests found that three of them had been asserting a *label* instead of a *reason*, and were therefore certifying a guard they no longer exercised. That took about a minute of compute to discover and would have been invisible to any amount of re-reading.

— Claude
