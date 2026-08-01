# Human Report — Claude Session 55

**Current date and time:** 2026-08-01 13:21 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner re-review. Codex blocked the four-file Stage-A/B/C state I built in Session 54; this session reproduced all three of its findings by construction, corrected them, added the discriminating tests it required, and returned a corrected exact state.

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config/config.json` does not exist.

**Protocol-P execution state:** **Zero rollouts spent this session.** Stage 0 remains executed exactly once (my Session 48) and jointly approved. Stages A, B and C remain unexecuted and unauthorized. The replay gate was not re-run. The confirmatory test split is untouched.

---

## Summary

Codex's Session 54 reviewed the Stage-A/B/C driver and results layer I built in Session 54 and refused the exact state. It accepted three design decisions I had handed it — the zero-cost `--mode plan` default, the driver's temporary imports of three Stage-0 helpers, and the origin-provenance reuse rule in substance — and blocked the executable state on three findings. All three are real.

The single most important fact about this session: **the full 906-test suite was green while two of those three defects were live.** Codex found them by driving the whole driver end to end through states the tests never put it in, using synthetic bodies and no physics engine. That is the same instrument I have used to find defects in Codex's work, pointed back at mine, and it worked.

I reproduced every finding independently before changing a line, and my numbers matched Codex's exactly. Then I corrected all three, implemented the section-9 sub-branch distinction Codex also asked for, fixed the non-blocking docstring defect it named, added 32 new tests aimed specifically at the states the old suite could not reach, and ran a 32-case mutation sweep over my own patch — which found one real gap in my new tests, of a class this project has now hit three times.

The corrected four-file state is handed back to Codex. No rollout was spent, nothing was executed, and running the screen remains unauthorized.

---

## The three findings, and how I verified them

The discipline here is Lesson 8 and Lesson 50: verify a correction the same way you would verify an accusation — by construction, not by reading the reviewer's reasoning and agreeing. I built a probe that imports the committed test module's own stub machinery (so the probe cannot drift from it) and drove the real `run_screen` through each state.

### 1. A mixed Stage-A drop aborted after spending valid later work

Stage A tries nine candidate probe amplitudes and drops a candidate as soon as one of its twelve rollouts fails a hard gate. But `run_screen` then defined "the rows to report" as *all rows of surviving candidates* — which excludes the rollout the dropped candidate actually ran and recorded. The completeness check saw that real result as unplanned surplus and raised.

Reproduced, two candidates, first saturating on its first row:

```text
ProtocolPError: the ledger holds 1 unplanned physical result(s):
  PhysicalKey(sensor_seed=150002, pair_id='basepair_protocolp_stageAB_c4',
              condition='healthy', severity=None, peak=0.05, ramp=0.125)
executor_calls = 73
```

73 stubbed rollouts spent, then the whole run thrown away at the final check. Identical to Codex's reproduction.

The same class is sharper in the all-dropped terminal, which returned drop summaries only: two rollouts spent, zero rows reported, no ledger view at all.

**Fix.** `run_stage_a` now returns `measured_rows` — every row it called `run_logical_row` on. The function that ran the rows is the one that says which rows ran; reconstructing that downstream from candidate survival is exactly what lost them. `_executed_rows` composes that with every Stage-B/C row and refuses a measured row that is not in the inventory built at the selected candidate.

### 2. Stage-B and Stage-C hard-gate failures were measured, then ignored

Protocol P section 8 says "Every rollout re-asserts the hard gates," and I12 scopes the gates to every cell and every condition. `run_logical_row` did compute a `GateReport` for every rollout in every stage — and `run_reuse_aware_rows` discarded the returned result. Only Stage A consumed it.

The consequence, reproduced with one candidate and a stubbed remEI-0.40 body carrying one saturated step:

```text
terminal        None
outcome_case    CASE_A
remEI 0.40      verdict TESTABLE, min_margin 6.230
```

A damage level whose simulation drove an actuator into saturation was reported as measurable and safe. Section 9's `UNSAFE_LADDER_VALUE` branch — which exists to exclude such a value with a reason, call it neither TESTABLE nor SUB-THRESHOLD, and make the outcome terminal — was unreachable in the implementation.

Codex's Stage-C claim was a code-reading claim rather than a reproduction, so I established it separately and this is the one place my evidence goes past its report. My first attempt used a seed-modulo filter and could not show the injected failure had landed on a Stage-C replicate at all — which would have made the demonstration vacuous, the exact failure mode of a test whose fixture cannot exhibit the defect. Retargeted on the exact identity `stage_c_identity(4, 3)`, it lands once, and the failing body's coefficients are differenced straight into the cell's operative null:

```text
injection landed on 1 rollout: basepair_protocolp_stageC_c4_k3
terminal None, outcome CASE_A, cell-4 q95_c 0.4057822419953376
the failing replicate reported as a clean Stage-C row
```

That matters more than the Stage-B case: `Q95_c` is the protocol's *only* operative null. Every later verdict is measured against it.

**Fix.** `run_reuse_aware_rows` returns the gate failures it measured instead of discarding them. `build_ladder_table` reads each fault-side body's gate report from the ledger and labels a failing cell `UNSAFE_LADDER_VALUE` with no margin — writing a margin beside that label would invite exactly the comparison section 9 forbids. `unsafe_ladder_values` is a separate function, and `classify_outcome` now raises on a table that still holds one, so its docstring's claim to be called only after safety is established is checkable rather than aspirational. A failing Stage-C replicate terminates before the null is built.

### 3. The persisted result was not an I12 audit record

`PhysicalResult` held `gate_report`, `n_steps` and `elapsed_s`; `logical_row_report` persisted none of them. The 180-row document could not show the hard-gate margins, the step counts, or the elapsed time — so a reader could not have audited either of the first two findings from the artifact.

**Fix.** Codex offered two designs and I took the second: an explicit 168-entry physical ledger the rows cite, rather than copying the gate report into each row. Twelve rows would otherwise carry a second copy of an origin's gate report, and a second copy is a second authority — the same defect class the whole module exists to prevent, one level up. Rows join to it on `rollout_provenance`, and the document says so in its own text. A `timing` block records the rollout count and summed elapsed time, which is the elapsed-time record Codex's Session-46 answer asked for, captured at the run rather than reconstructed after it.

One function attaches all of this on **every** exit path — the two terminals and the normal one — so a future terminal branch cannot be added that silently reports less than the others.

---

## The section-9 sub-branches, and one decision I did not make alone

Codex also required the `NO_ADMISSIBLE_PROBE` terminal to implement section 9's three-way split, keyed to the reference candidate 0.05 N / ramp 0.5:

- healthy or remEI-0.75 failure there → implementation-integrity failure, carrying **no** defect-localization claim;
- failure only at the ladder bottom → newly observed physical safety or method limit;
- any other candidate → recorded, classifies nothing.

The second branch is the one section 9 fences most tightly: it may not be asserted unless both construction checks (I13a and I13b) are in a passing state. So the implementation *reports the precondition rather than assuming it* — I13a named as asserted for that specific rollout by the construction layer before it ran, and I13b named as `tests/test_cable_plant_softening_boundary.py`, **which this script does not run and does not assert.** Session 41 measured that the safety gates pass with roughly seventy times margin under a construction defect; that is why the document has to say what it did not check.

**The decision I handed to Codex rather than taking.** Section 9 names `UNSAFE_LADDER_VALUE` for a ladder *value*. It is silent about a Stage-C healthy replicate failing a hard gate, even though I12 scopes the gates to every condition. I did not want to invent a pre-registered name, and I did not want to bump a specification version that has been settled since Session 43 over a branch that has never been reachable. So I implemented the only behaviour that cannot manufacture a result — terminate, build no `Q95_c`, preserve everything — under a driver-side label, `UNSAFE_STAGE_C_REPLICATE`, and both the constant's comment and the results document say plainly that the label is the driver's while the terminal outcome is section 9's. If Codex reads that as needing a specification note, it says so and I will not argue it.

---

## What the mutation sweep found in my own tests

32 distinct cases across two passes, each restoring exact bytes, each naming its own target test files.

The first pass ran 27 cases and produced 26 verdicts — 25 caught, **one real survivor**, plus one anchor of mine that matched twice and produced no verdict at all:

```text
section_9_branch_not_computed   SURVIVED.  All three of my branch tests call
                                classify_no_admissible_probe DIRECTLY, so deleting
                                the driver's call site left every one of them green.
```

This is the third instance in this project of that exact shape: a guard with its own tests and nothing asserting the program ever reaches it. Because one instance usually means a class is present, I then swept the call site of every new function reachable only from `run_screen` — which turned up that nothing asserted the clean path reaches `classify_outcome` either. Both gaps were in the tests, not the production code, and both are closed. The second pass — the re-formed anchor, the survivor re-run after the fix, and five more call sites — caught 7 of 7.

Also fixed: the `physical_key` docstring Codex flagged as non-blocking. It claimed an integer and a float severity would hash to different ledger keys. They do not — Python already has `1 == 1.0` and equal hashes — which is why the test written against that claim could never have gone red. The docstring now records what the normalisation actually guarantees (the recorded numeric type) *and* records that the earlier claim was a property of the language rather than of the function, because that is the useful half.

---

## Challenges

**The temptation to accept a correct review on authority.** Codex's report was accurate and detailed, its numbers were reproducible, and re-deriving all of it cost most of an hour. The reason to do it anyway is that one of the three findings — the Stage-C one — was a code-reading claim rather than a reproduction, and my own first attempt to reproduce it was vacuous. Had I accepted the report wholesale I would have written a test that did not exercise what it claimed to.

**Getting the specification's silence right rather than filling it in.** The Stage-C gate consequence is genuinely unspecified. Two wrong moves were available: implement nothing (leaving the operative null buildable from an unsafe body), or quietly invent a pre-registered-sounding name for a branch the protocol does not contain. The route taken — implement the conservative behaviour, name the label as the driver's own, hand the naming question to the reviewer — is the one that leaves the record honest either way.

---

## Files created or updated

- `Reproducibility Packet/scripts/run_protocol_p_screen.py` — the driver. `+386/−43`. Blob `99e2d44744eaf7ecd2bda1a21acce1ec9ce435c4`, 74,697 B.
- `Reproducibility Packet/scripts/utils/protocol_p_results.py` — the results layer; adds `ledger_report` and `physical_key_report`, corrects the `physical_key` docstring. `+71/−3`. Blob `e84e5f9f4e6d10408873d87b81b2baef9535d50e`, 40,090 B.
- `Reproducibility Packet/tests/test_protocol_p_driver.py` — `+490/−0`, 111 collected (was 85). Blob `3f1a81067116f2815f8680e6307e15e06c629db6`, 70,556 B.
- `Reproducibility Packet/tests/test_protocol_p_results.py` — `+82/−0`, 77 collected (was 71). Blob `cbac30ed3d41c961f7d5c54c306c8a09fa1be1cd`, 33,724 B.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — my Session-55 turn, `+202/−0`, clean append at the physical end (header once, line 13,139).
- `README.md` (root, the public Live-Run log) — one new entry, `+2/−0`. No dated entry edited.
- `agents/Claude/Session Summaries/HumanReport55.md` — this report.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — updated / rewritten.

All four code files are UTF-8, no BOM, pure LF, verified by measurement.

---

## Verification

```text
findings reproduced before any fix     3 of 3, plus the all-dropped and Stage-C variants
full packet suite                      938 passed in 114.30 s   (906 + 32 new)
compileall                             clean
mutation sweep                         32 cases, 2 passes, 32 of 32 caught
                                       (1 real survivor in pass 1, closed and re-verified)
plan mode re-run                       9 candidates, 180 rows / 168 rollouts / 12 reuses,
                                       onset 500, window [1000, 1768), zero rollouts
Protocol-P plant rollouts              zero
Stage 0                                not re-executed; artifact unchanged
replay gate                            not re-run (nothing on its watched path changed)
config.json                            absent
confirmatory test split                untouched
files changed outside the four         README.md (one appended entry) and the transcript
```

No progress report was due: Session 55 is not an every-eighth session, no phase transition occurred, and no Claim Sheet amendment was approved. My next regular progress report is Session 56.

---

## Next steps

1. Codex reviews the corrected four-file exact state and rules on the `UNSAFE_STAGE_C_REPLICATE` label — whether it stands as a driver-side name or needs a specification note.
2. If that loop closes, the remaining pre-execution work is a packet README step for the driver (a runbook step describes something a reader can rely on, so it belongs in the session that closes the review), and `screen_physical_faults`.
3. No Stage-A/B/C rollout runs until both agents explicitly approve the same executable state. Execution authorization is a separate decision from implementation approval and has not been given.
4. Downstream and unchanged: written Amendment A2, replacement assignment and config lineage, full regeneration, Gates 4–7, the joint immutable freeze, and one-shot confirmatory generation.

— Claude
