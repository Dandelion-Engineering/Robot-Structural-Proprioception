# Human Report — Claude Session 54

**Current date and time:** 2026-08-01 09:02 PDT

**Phase:** Phase 2 — Execution

**Session role:** Implementer. Built the Protocol-P Stage A/B/C results layer and screen driver under the origin-provenance rule Codex ruled on in its Session 53, and handed both to Codex for exact-state review.

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config/config.json` does not exist.

**Protocol-P execution state:** **Zero rollouts spent this session.** Stage 0 remains executed exactly once (my Session 48) and jointly approved. Stages A, B and C remain unexecuted and unauthorized. The replay gate was not re-run. The confirmatory test split is untouched.

---

## Summary

Codex's Session 53 did three things: it approved the public README at my returned state, closing that loop; it ruled on the reuse/provenance question I handed it; and it authorized me to implement the Stage-A/B/C results module and driver for review. This session did that.

The result is four new files — a results layer, the driver, and a test file for each — totalling 156 new automated checks. The full packet suite went from 750 to 906, all green. Nothing was executed: the driver's default mode builds and audits the entire plan and then stops, having run no simulation at all.

The substance of the session is the rule the two of us settled last session, now made executable and checked. Protocol P declares 180 result rows and budgets 168 simulations. The gap is twelve rows that consume a measurement an earlier row already paid for. Because the stage's name is inside the hashed provenance payload, asking the construction layer for a Stage-B or Stage-C version of a reused Stage-A body produces a *different, perfectly well-formed* fingerprint for a simulation that never ran again — twelve hashes no artifact carries, in a record that a per-row audit would still report as complete. The implemented rule is that the physical rollout owns its provenance: a reused row cites the origin's hash and canonical payload verbatim, never calls the construction layer, and never mints anything.

I then attacked my own patch. Fifty-eight injected defects, one at a time, each with the focused test file re-run and the file restored afterwards. Fifty-two were caught. Of the six survivors, five were real gaps in my tests and are now closed; the sixth is a check no data can reach, and I kept the line and wrote down why rather than deleting it or claiming coverage.

---

## What I read before acting

Following the `AgentPrompt.md` workflow:

- `Project Details/Project Details.md` in full, and `AgentPrompt.md` in full;
- my own `Summary of Only Necessary Context.md`;
- the summaries of every concluded chat I am in, the active transcript-monitoring thread, and the tail of the Phase-2 transcript;
- **Codex's most recent human report (`HumanReport53.md`) and its Session-53 chat turn** — the cross-review requirement;
- Protocol P v2.3.3 sections 8 through 12 (window, statistic, stages, outcomes, invariants, cost) and the approved construction layer `utils/protocol_p_conditions.py` in full.

---

## What I built

| File | What it is |
|---|---|
| `Reproducibility Packet/scripts/utils/protocol_p_results.py` | The results layer: the physical-body key, the logical row, the ledger, the inventory builders, the reuse rule, and the results-only persistence boundary. |
| `Reproducibility Packet/scripts/run_protocol_p_screen.py` | The driver: derived onset, derived window, invariants I9–I12, Stage A with candidate drops, the selection rule, Stages B and C with reuse, both secondaries, and the results document. |
| `Reproducibility Packet/tests/test_protocol_p_results.py` | 71 tests. |
| `Reproducibility Packet/tests/test_protocol_p_driver.py` | 85 tests, including an end-to-end rehearsal of all 168 simulations. |

### The design decision that carries the rule

A physical result is keyed by what makes the simulated body distinct — the sensor identity, the realized pair id, the condition, the severity, and the selected probe. **The stage is deliberately *not* part of that key**, and there is a test asserting it, because including the stage is exactly what would make the reuse disappear and the twelve phantom fingerprints appear.

The declared reuse set is then checked against the *computed* set of rows whose body was already measured. Those two must be the same set, in both directions: a row that declares a reuse but does not duplicate anything is refused, and a row that duplicates something without declaring it is refused too. Reaching that check required a mutation that keeps the count at twelve while moving *which* twelve, since any single-row change also trips the simpler count check first. That test exists and says so in its own comment.

### Two things derived rather than carried

**The fault onset.** The screen's source setting is healthy, so the generator derives no onset for us; the driver must supply one. It reads `onset_time_s` from the bound trajectory, converts it with the generator's own grid helper, and then asserts equality with the value it actually passes into the construction layer. The value is 500 — which is also what a hard-coded literal would have said today, and that is the point. A literal that is currently correct is indistinguishable from one that has stopped being correct, and the Session-41 defect was exactly a missing onset making two different experiments look identical.

**The window origin.** Nothing in the codebase fixes it, so the driver derives it from onset plus the probe's start offset, through the same helper that refuses an off-grid time. The two conversions are wrapped separately, so the error message says *which* one drifted: an off-grid onset moves the damage, an off-grid offset moves the measurement, and those are different failures. Both branches have their own test.

### Execution authority encoded in the CLI

`--mode plan` is the default and runs zero rollouts; `--mode execute` runs the screen. This is my choice, not a pre-registered one, and I flagged it as such to Codex. The reasoning: implementation was authorized and execution was not, and a command-line tool whose default spends 169 simulations is one keystroke away from spending them.

Run in plan mode against the real committed inputs, it prints:

```text
admissible candidates   9          derived onset index   500
logical rows            180        window                [1000, 1768)
physical rollouts       168        config.json           absent
reused rows             12         rows by stage         A 108  B 40  C 32
```

That reproduces both my Session-53 dry-run and Codex's independent Session-53 reconstruction — this time from the running program rather than from either of our one-off probes.

---

## Challenges, and how they were resolved

### The census could only ever audit one plan

My first version pinned 180, 168 and 12 as literals inside the audit function. A two-candidate integration test then failed — correctly, and for a reason that was my defect rather than the test's: the pre-registered totals are stated for the nine admissible candidates, but a partial plan is a legitimate object and has to satisfy the same arithmetic.

The fix is the pattern this project has settled on for exactly this shape: derive the counts from the plan's own structure, keep the pre-registered totals as pins, and reconcile the two **by equality** at the nine-candidate grid. A change to either the formula or the pins now fails loudly instead of one quietly following the other. Two tests cover both halves — that a wrong pin fails at the grid it is stated for, and that it does *not* break a legitimate smaller plan.

### A test of mine that could never have failed

The mutation sweep caught this and it is the most useful thing it found. I had written a test asserting that an integer severity and a float severity produce one key rather than two. Removing the normalisation the test exists to protect left it green — because Python already has `1 == 1.0` and the same hash, so the key would have deduplicated either way. The test was verifying a property of Python, not a property of my code.

What the normalisation actually guarantees is the recorded *type*, which is what a reader sees in a serialised report. The test now asserts that, and now goes red when the normalisation is removed. This is the project's standing question — *what exact state would make this test red?* — answered the hard way rather than the comfortable way.

### A guard that was only ever tested in isolation

Deleting the driver's call to the torque gate survived the whole suite. The gate itself had a test; nothing tested that the driver *reached* it. A 0.20 N probe is finite and positive, so the construction layer's own admissibility check waves it through — that call site was the only thing standing between an over-torque probe and a simulation.

Having found one instance, I looked for the class rather than fixing the instance: the derived-onset assertion had the identical shape and the identical gap. Both now have wire tests, and both mutations are caught.

---

## Verification

```text
full packet suite                     906 passed in 57.63 s   (750 before this session)
  tests/test_protocol_p_results.py     71 collected
  tests/test_protocol_p_driver.py      85 collected
compileall over the packet scripts    clean
plan-mode run against real inputs     180 / 168 / 12, onset 500, window [1000, 1768)
end-to-end rehearsal                  168 executor calls, 180 reported rows,
                                      168 distinct fingerprints, 12 citations
mutation sweep                        58 cases, 52 caught, 6 survived
survivor re-check                     both results-side survivors re-run against the
                                      driver test file too; both still survived
after the fixes                       8 re-checks, 7 caught, 1 survivor kept and documented
Stage-0 artifact                      unchanged, not re-executed
replay gate                           not run (no file it watches changed)
Protocol-P stage rollouts             none
config.json                           absent
```

Transcript append passed its four hard gates: pre-write 12,838 lines, post-write 13,001, header exactly once at line 12,839, after the pre-write boundary, `+163 / −0`.

I also discharged the standing transcript-order monitoring duty at the git level: Codex's Session-53 commit changed the transcript by `+108 / −0`, its header occurs exactly once at line 12,734, after its recorded 12,730-line boundary, and Codex was physically last. Clean — twenty consecutive clean appends. The duty is to flag recurrences, so no note was filed.

---

## Decisions I made, and the two I handed to Codex rather than settling

1. **The plan/execute CLI split** — mine, flagged, and reversible if Codex would rather the mode be required with no default.
2. **The driver imports three helpers from the Stage-0 script** rather than re-implementing section 8's per-gauge statistic. A second copy of the protocol's own statistic is the exact class of defect this project keeps finding. By Codex's own earlier answer the extraction trigger is the *third* consumer and there are now two, so the precedent says accept the import and extract later — but it is a script-to-script import inside Codex's stated sequencing rule, so I led with it and handed over the decision rather than assuming an answer.
3. **No packet-README step for the driver yet.** A runbook step describes something a reader can run and rely on; an unreviewed script is not that. It belongs in the session that closes this review loop.

---

## What is honest to say about where this leaves the project

The screen can now be *run*. It has not been, and the decision to run it is not mine alone — Codex reviews the exact executable state first, and implementation permission was never execution permission.

It is also worth restating what the screen will and will not settle, because a working program invites more confidence than the plan warrants. The honest prior recorded in the protocol is unchanged: the milder damage level is expected to fail in every context by a wide margin, and the level that clears the binding case does so by about 1.11×, on a projection computed with an inflated signal against a deflated bar — both errors favouring the hypothesis. A partial pass and a complete failure remain roughly comparable in likelihood. The third stage settles it, and it costs 169 simulations, roughly seventy-six minutes.

---

## Files created or updated

- `Reproducibility Packet/scripts/utils/protocol_p_results.py` — **created**.
- `Reproducibility Packet/scripts/run_protocol_p_screen.py` — **created**.
- `Reproducibility Packet/tests/test_protocol_p_results.py` — **created**, 71 tests.
- `Reproducibility Packet/tests/test_protocol_p_driver.py` — **created**, 85 tests.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the handoff (`+163 / −0`).
- `README.md` (root, the public Live-Run log) — **one new entry appended** (`+2 / −0`); no dated entry edited. The now-settled previous entry says the driver "is not yet built or approved," and that half stopped being true this session.
- `agents/Claude/Session Summaries/HumanReport54.md` — this report.
- `agents/Claude/README.md` — updated.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

No protocol specification, assignment, configuration, dataset payload, result artifact, or confirmatory material changed. No new dependency was added.

No progress report was due: Session 54 is not an every-eighth session, and no phase transition or approved Claim-Sheet amendment occurred. The next regular one is my Session 56.

---

## Next steps

1. **Codex reviews the four exact states** and rules on the two open questions (the CLI default, and whether the Stage-0 import is premature under its own third-consumer trigger).
2. If that loop closes on an executable state, the next decision is whether to authorize the run — 169 rollouts, about 76 minutes, as a background job polling the results JSON rather than the log.
3. Downstream and unchanged: the written Amendment A2, a replacement assignment and configuration lineage, full regeneration from zero, Gates 4 through 7, the joint immutable freeze, and one-shot confirmatory generation.

— Claude
