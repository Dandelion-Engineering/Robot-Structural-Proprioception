# Human Report — Claude Session 57

**Current date and time:** 2026-08-01 20:21 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner re-review. Codex reviewed my three Session-56 states: it approved two as-is and edited two artifacts (one of mine from Session 56, one progress report). This session re-reviewed both edits, approved one, returned a better version of the other, and posted my half of the execution authorization.

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config/config.json` does not exist.

**Protocol-P execution state:** **Zero rollouts spent this session.** Stage 0 remains executed exactly once (my Session 48) and jointly approved. Stages A, B and C remain unexecuted. The replay gate was not re-run — deliberately, for a reason given below. The confirmatory test split is untouched.

---

## Summary

Codex approved the Stage-A/B/C driver and its test file at my exact blobs, ruled that the redundant vocabulary guard may stay, and declared the pre-execution implementation list empty. It made one reviewer edit to the packet runbook's Step 25 and one to my Session-56 progress report, and handed both back for owner re-review. That re-review was this session's work.

**Both edits were right in kind. One I approved unchanged after measuring it. The other I returned, because it corrected a wrong number with another wrong number.**

The Step-25 edit changed "180 stamps over 168 rollouts" to "180 provenance references comprising 168 distinct stamps." I did not want to approve that from a code read, because a note I have been carrying since Session 53 says the opposite. So I ran the entire 180-row screen end to end through the production driver against synthetic bodies — zero simulations — and counted. Codex is right, my carried note is stale, and the note has been corrected forward rather than dropped.

The progress-report edit corrected a claim that Protocol P had so far cost **one** simulated run, changing it to four. Checking that against the session records, the real figure is **thirteen**. Session 45 ran the reproduction check twice, not once, and Codex itself ran it twice more while reviewing that session — facts recorded in our own reports, which neither of us had gone back to. A further six runs were spent in Sessions 39, 40 and 41 on checks that predate the reproduction check entirely.

Then one new finding, raised before the execution decision rather than after it: **the reproduction check that is supposed to verify the instrument immediately before the measurement runs the simulator on a path the measurement does not use.** Details below, along with a free check that closes the gap.

Two files changed plus the public log and the transcript. Zero rollouts.

---

## What Codex settled, and what I did not re-ask

```text
APPROVED AS-IS, loop closed:
  scripts/run_protocol_p_screen.py   7668793e147a2776cb003ea90c79e76247d9b4de
  tests/test_protocol_p_driver.py    23222d0ed03c26f57cfff5f53267ca8186a8d31a
KEEP_REDUNDANT_HELPER_VOCABULARY_GUARD
  Codex's reasoning is better than mine was: the protocol's executable sketch puts
  the closed-set refusal inside that named helper, and the vocabulary tuple is
  imported from the construction layer rather than redefined, so keeping the line
  preserves the pre-registered surface without creating a second authority.
NO_STAGE_A_B_C_EXECUTION_AUTHORIZATION_IN_THAT_TURN
  and acceptance of my replay-gate sequencing proposal for a dedicated round.
```

I verified both approved blobs against my working tree — exact — and did not reopen the plan-mode default, the Stage-0 imports, or the Stage-C label, all of which Codex settled in earlier sessions.

---

## Step 25: approved, after running rather than reading

My original sentence contradicted itself. Two clauses earlier the same paragraph says the twelve reusing rows "cite the original rollout's provenance stamp rather than minting a new one," and then it told a reader they would find "180 stamps." Both cannot be true.

Rather than accept the correction from a code read, I ran the whole screen. The executor is the approved test suite's synthetic-body stub, which observes through the real sensor model; every number below is produced by the production driver, not by the probe.

```text
logical rows in results table     180
rollout_provenance REFERENCES     180
  ... DISTINCT                    168
physical_ledger entries           168      distinct provenance_hash 168
executor calls (real rollouts)    168      distinct stamps minted   168
rows carrying reused_from          12      each cited stamp used exactly twice
every reference resolves to a ledger stamp                          PASS
references - distinct == reused rows                                PASS
elapsed 34.4 s, terminal None, zero MuJoCo rollouts
```

The four Stage-C `k=0` rows cite the Stage-A healthy stamps, and cell 4's is `dev-d732ceb4ff2a8bc6...` — the same value the Session-53 dry-run recorded for the Stage-A healthy identity, which is an independent confirmation of Codex's Session-53 citation ruling at the byte level.

**A carried note is now wrong and is corrected forward.** My limitation 53 reads: "the screen's provenance stamps outnumber its rollouts 180 to 168, by design; no write-up may say 'one provenance stamp per rollout'." That was written from the Session-53 dry-run, *before* the citation ruling was implemented in Session 54. Under the driver we have both approved there is exactly one distinct stamp per rollout, so the prohibition as written would now forbid a true sentence. Restated: **168 distinct stamps, one per physical rollout; 180 references to them in the results table; the twelve reuses reference an origin's stamp a second time.**

---

## The cost record: one, then four, then thirteen

Codex's correction was right in kind. I checked it the way I would check an accusation — against the session records rather than against its reasoning — and found two things it did not have.

```text
Session 45 ran the gate TWICE, not once.
  My HumanReport45 line 92 and the transcript at line 9416: both runs produced
  58/58 equality, at 25.58 s and 26.37 s -- once before and once after I added the
  ephemerality denominator.
Codex ran it twice MORE while reviewing that same session.
  Its own HumanReport45 line 202: "Codex ran the gate twice while reviewing";
  final reviewer replay wall clock 27.46 s.
The replay gate is not the whole protocol's simulator cost.
  Codex S39  1  a replay of an already-delivered healthy development row
  Claude S40 1  the transparency check, overrides=None, 26.4 s
  Claude S41 4  the onset-consequence probe, "all 4 ADMISSIBLE"
```

```text
S39 1  +  S40 1  +  S41 4  +  S45 4  +  S46 2  +  S51 1   =   13
```

I swept Sessions 42–44 and 47–56 for both agents and found zero in every one, checking Codex's S43 and S44 separately since neither carries a "Rollouts spent" line. I also swept the packet README and the public log for a count claim of this kind and found none — the packet's "One MuJoCo rollout, about 26 s" is a per-invocation cost and is correct. The error was confined to the progress report. The eleven prior human reports that carry the wrong figure are dated records and stay as they are; corrections propagate forward.

**Why this happened, which matters more than the number.** Both agents re-verify a fixed list every session: the configuration is still unfrozen, the test split is still at zero, no stage rollout has run. Every one of those is a claim about the project's *present state*, and each gets re-measured. The cost figure was a claim about the project's *past*. A claim about the past looks settled, so for eleven consecutive sessions neither agent re-derived it — each quoted the previous one. This is Standing Lesson 65 with a sharper edge: the danger is not only that a long-true clause survives into a session where it is false, it is that a clause about history is never re-measured at all, by anyone, precisely because both parties treat it as a fact rather than as a measurement.

Thirteen single rollouts is roughly five and a half minutes of simulator time, so the cost discipline itself survives intact. The bookkeeping did not.

---

## The new finding: what the replay gate does and does not certify

This bears directly on the authorization, so I raised it before the decision.

```text
The replay gate runs with overrides=None -- explicitly, at gate line 572, and the
packet's Step 23 names it.  Every MuJoCo rollout this project has spent through the
section-4 construction path either ran with overrides=None or predates the seam
entirely (the seam landed in my Session 44, commit 3fa806c; the dataset was
generated 2026-07-24).

THEREFORE: no MuJoCo rollout has ever executed with an ACTIVE override bundle.
The first of the 168 will be the first time that join runs.
```

Being precise about what *is* covered, because "unverified" would be unfair to the work already done:

- **The physics half is verified.** `tests/test_cable_plant_softening_boundary.py` — invariant I13b, co-owned, approved by Codex in Session 43 — builds the real softened MuJoCo model at reduced fidelity and asserts the swap happens at exactly the declared onset step and never before, and that a healthy plant builds no softened model at all.
- **The plumbing half is verified.** The Session-44 seam, 37 tests, no physics.
- **The join has never run.** Two verified halves, never connected in a real rollout.

A gross failure aborts on the first rollout at about 26 seconds: the pre-registered fault check runs before execution, the realized-identity equality check runs immediately after, and the hard safety gates are measured on every body. **The failure mode worth flagging is the silent one** — an override accepted, a physically valid body produced, but the softening never applied. Every gate passes, the difference statistic collapses toward the sensor-only null, and the screen reports SUB-THRESHOLD everywhere. That is indistinguishable in the output from the genuine negative result the screen exists to be able to report. Codex's own Session-41 measurement is the precedent: a fault activating at step 0 instead of step 500 left every safety gate admissible at roughly seventy times margin.

**The check is free, and the data is already persisted.** `stage_ab_identity(cell)` depends on the cell alone, so within a cell the healthy rollout and both structural rollouts share `sensor_seed` and `pair_id`; `cable_plant.py` carries no RNG (measured Session 37). So if an override failed to reach the plant, the faulted body *is* the healthy body, and the Session-55 ledger's `gate_report.max_abs_gauge_true` for the two would be **exactly equal, bit for bit**:

```text
For each cell in {4,5,6,7}, read from physical_ledger alone:
  max_abs_gauge_true(healthy)  !=  max_abs_gauge_true(structural 0.75)
  max_abs_gauge_true(healthy)  !=  max_abs_gauge_true(structural 0.35)
  ordering monotone: healthy < remEI 0.75 < remEI 0.35
Exact equality on any pair -> the override did not reach the plant, and the run is a
construction failure to diagnose, NOT a scientific SUB-THRESHOLD result.
```

I deliberately proposed **no magnitude threshold.** Session 20's table (healthy 19.2 µε; remEI 0.50 → 38.4; 0.25 → 72.4) was measured in a different configuration, and importing its numbers here would be exactly the Lesson-11/12 move I keep flagging in other people's work. Direction and non-equality are configuration-free; magnitude is not. Codex owns the ruling on whether this is a mandatory readback or a specification matter.

---

## My half of the execution authorization

```text
CLAUDE_AUTHORIZES_ONE_ROW_REPLAY_GATE_RUN
  one rollout, ~26 s, overrides=None.  Scope stated so the Technical Report cannot
  overstate it later: it certifies the SHARED machinery has not drifted.  It does
  NOT certify the overridden path.
CLAUDE_AUTHORIZES_STAGE_A_B_C_168_ROLLOUTS
  conditional on the gate passing and on the ledger readback (or Codex's
  alternative) running before any outcome case is treated as a scientific result.
RECOMMENDED: ONE session runs the gate and then the 168, with nothing in between.
```

**Why I did not run the replay gate this session,** even though the pace is the thing my last progress report flagged as the honest problem: nothing on its watched path has changed since Session 51, so a run now would measure nothing, and the entire value of my Session-56 proposal is temporal adjacency — "the instrument was verified immediately before the measurement" is only true if nothing intervenes. Running it now would spend that adjacency to produce motion rather than progress. The 168 cannot be authorized by me alone in any case.

---

## What I deliberately did not do

No rollout of any kind. Did not re-execute Stage 0. Did not run the replay gate. Changed **no code** — the only files I touched are two markdown documents, the public log, and the transcript. Did not touch the protocol file, the assignment, the draft config, the Stage-0 artifact, the driver, its tests, the results layer, the seam, or any payload. Did not edit any dated public-log entry or any prior human report. No new dependency. No result artifact written into the repository — the probe's output went to the scratchpad.

---

## Verification

```text
Codex's two approved blobs vs my tree      exact, both
progress report reviewer blob 39c5924...   confirmed present before my edit
my returned blob              1723e545...  +33/-8
packet README Step 25         9c9fa7f0...  approved unchanged
Stage-0 artifact              31c1e6d1...  unchanged; results/protocol_p holds one
                                           file; q95 0.4008810868833315, pairs 100
full 180-row screen through the production driver, synthetic executor, 0 rollouts
full packet suite                          975 passed
config.json                                absent
confirmatory test split                    untouched
transcript append                          +225/-0, header unique, at line 13,783,
                                           after the 13,779-line pre-write boundary
public log                                 +2/-0, no dated entry edited
```

---

## Files created or updated

- `agents/Claude/Progress Reports/Progress Report Session 56.md` — **returned as a new exact state**, blob `1723e545…` (+33/−8). The cost paragraph now gives thirteen with a per-session breakdown and says why the number went unchecked.
- `README.md` (root, public Live-Run log) — one new dated entry (+2/−0). No dated entry edited.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — my Session-57 turn (+225/−0).
- `agents/Claude/Session Summaries/HumanReport57.md` — this file.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.
- **Approved unchanged, not edited:** `Reproducibility Packet/README.md` Step 25 at Codex's blob `9c9fa7f0…`.

---

## Next steps

1. **Codex re-reviews the returned progress-report state** (`1723e545…`) and rules on the ledger readback.
2. **Then the execution round.** Codex posts its half of the authorization; whichever agent holds the next turn runs the replay gate and then the 168 rollouts in **one** session, roughly 70–80 minutes as a background job.
3. **Before any outcome case is read as science,** run the healthy-vs-faulted peak-strain readback out of the persisted ledger.
4. Then: Codex reviews the result and the branch → written amendment A2 and a replacement assignment → full regeneration from zero.

The one open request for the director — `director_requests.md` entry 1, the Claim Sheet review — remains open and non-blocking. Nothing else of mine is waiting on anyone.
