# Human Report — Claude Session 46

**Current date and time:** 2026-07-29 20:58 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner re-review of Codex's corrections to the replay gate; then implementation and handoff of Protocol P Stage 0

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config.json` remains absent

**Protocol-P execution state:** The one authorized replay rollout is the only Protocol-P rollout ever spent. **Stage 0 was NOT run** — `results/protocol_p/` does not exist. No Protocol-P identity, statistic, or screen artifact exists. The confirmatory test split remains untouched at zero identities and zero payloads.

---

## Summary

Two things happened this session. First, I re-reviewed the corrections Codex made to my replay gate and approved them, closing that loop. Second, I implemented Protocol P's Stage 0 and handed it off for review without running it.

The through-line of the whole session turned out to be a single idea, which arrived four separate times in four disguises: **a test that calls a function directly proves the function works, and says nothing about whether the program ever calls it.** Codex found that shape in my work in Session 44. I found it in Codex's fix this session. Then I found it three more times in my own new code, each time by deliberately breaking the code and checking whether the tests objected. That is now the first thing I check.

### Part 1 — The replay gate: both defects were real, and I approved the fixes

Codex had approved my replay *result* at one-row-exact scope but refused to approve the *implementation*, finding two blocking defects, fixing them directly, growing the test file from 30 to 36 tests, and handing it back for my genuine owner re-review. I confirmed both defects against the parent source:

1. **Filesystem effects were diagnostic-only.** My `main()` printed every added, modified, and removed watched path and then printed `REPLAY_GATE_PASS` and returned zero unconditionally. This is my own Session-45 lesson stopped one step short of its point: I had made the report disclose how many files it examined, and then left the claim itself unenforced. The check could go red in its prose and never in its exit status.

2. **A newly created repository-top-level file was invisible.** My code enumerated the repository's top-level files *once*, before the rollout, and handed that same fixed list to both snapshots. A file created during the run could not appear in the after-snapshot, so that scope was structurally guaranteed to report zero additions. The recursive scopes were fine; only the top level was blind — which is exactly where MuJoCo would write a log file. Codex's fix re-enumerates the *namespace* rather than the members, which is the right shape.

Codex also fixed a third, narrower thing: an incompatible dtype change (a float array becoming a string array) escaped as a bare NumPy `TypeError` instead of the protocol's required error type. I noted one clarification for the record so neither of us mis-cites it later: dtype drift was always *detected* — my Session-45 injection sweep caught it — because the equality result already required dtype equality. What the fix repairs is the *error path*, not detection.

**I verified everything from the committed bytes rather than from the report.** All four of Codex's claimed identifiers (two git blobs, two SHA-256 digests, two byte counts) reproduce exactly. The focused tests give 36 passed; the full packet suite gave 478 passed. I then ran the gate itself and reproduced the substantive result: 20/20 privileged fields, 38/38 observed entries, 3,124 watched files across 3 scopes, zero changes, 26.64 s.

**The one thing I did not take on trust, and it found a real gap.** Every one of Codex's six new tests calls `require_no_inventory_changes` directly with a hand-built dictionary. That proves the guard raises. It does not prove `main()` calls it — and a call site in `main()` is the entire content of defect 1. So I ran the real command-line gate again while a real file was created at the repository top level eight seconds into the twenty-seven-second rollout, in a place the before-snapshot could not have known about. The gate failed, named the offending path, raised the protocol's error type, and exited nonzero. One run verified both fixes end to end: the shallow scope discovered a name it had never seen, and the exit status encoded the violation. Under the pre-fix code that run would have been green *twice over*. I verified the cleanup left the repository clean.

I recommended **against** committing that as a permanent test, for the same reason Codex and I both rejected a skip-if-absent integration test: it needs the retained dataset, 27 seconds, and a real write inside the repository, so it would skip on every clean checkout and advertise coverage it does not provide. It belongs where it is — a scratchpad technique, recorded here, rebuilt whenever this gate or the coming stage driver is patched.

**Two measurements I took because Codex's change turned a diagnostic into a hard gate.** Promoting a report to a gate creates a new failure mode — spurious failure — so I measured instead of assuming. Python bytecode cannot cause it: the entire packet has exactly two function-level imports, both of a module already loaded, neither in the rollout path, so no `__pycache__` write can land inside the watched interval even on a clean checkout. And `MUJOCO_LOG.TXT` already exists at the repository root, so both of our runs' "zero modified" is a real measurement about a really-watched file.

I also verified Codex's new runbook text for `embed_approved_assignment.py` against the script rather than accepting it, since it landed in a section I own. All four of its claims hold, including a case-insensitive refusal to write a file named `config.json`.

I raised one non-blocking imprecision and deliberately did not edit it: the anti-vacuity failure message still reports its denominator as "roots" and omits the new shallow scopes, so a refusal now understates what it watched. It fires only when the gate is already refusing to certify, so it cannot license anything. Editing it would have cost a full re-approval round-trip on a state we had just closed; I offered to fold it into a later commit instead.

### Part 2 — Stage 0: implemented, tested, handed off, not run

Codex authorized exactly one next action: implement and hand off the Stage-0 script, and do not run it. Stage 0 is the sensor-only difference null — it measures how much of the screen's statistic the sensor path produces on its own, with no simulated arm in the loop at all. It sets no threshold and gates nothing; it exists so that a later number can be read against something.

**I led the handoff with a deviation, because implementing Stage 0 as pre-registered required editing a closed screen.** The protocol specifies Stage 0 as reusing "the gauge-window helper lifted into `utils/`" — and that lift had never happened. The helper lived inside a *closed* screen whose published results another screen still reads. Copying it instead would have created a second copy of a sensor-path driver that could agree with itself while diverging from production — precisely the failure mode Codex had cited two hours earlier about a different shared function. So I lifted it into a new `utils/gauge_windows.py`, changed exactly two things, and disclosed both: a hard-coded sensor identity became a required argument (the protocol pins its value, so no measurement moves), and an `assert` became an explicit raise (the protocol forbids `assert` in decision-bearing code because Python's optimized mode deletes it).

**Then I proved the closed screen had not moved**, because a lift that perturbs published evidence is not a lift. I re-ran it to a scratch directory and diffed: both published artifacts, the JSON summary and the markdown report, are **byte-identical** to the committed versions.

I flagged a second decision for Codex rather than deciding it silently. Stage 0 needs the protocol's text-hashing helper, its error type, and two pinned digests — all of which exist only inside the replay gate. I import them from there so there is one implementation of the hashing rule and one copy of each digest. The better architecture is to extract them into a shared module, and I did not, because that would edit the gate at the exact state we had just agreed on. My recommendation is to extract when the stage driver arrives and makes a third consumer. I measured the cost of the coupling rather than worrying about it: importing the gate also pulls in the physics engine, and the total import takes 0.21 s.

**A reachability finding worth recording.** My first attempt to feed one of the protocol's invariants the state it rejects *could not be written*. The invariant requires the Stage-0 identity to differ from the base configuration hash — but the identity is a hash *of a document containing* that hash, so a collision would require finding a SHA-256 fixed point. All three parts of that invariant are unreachable from the real construction path. So for Stage 0 it guards against a *code* defect — a future edit returning the wrong variable — not a *data* defect. I kept it (the protocol requires it, and it is nearly free), extracted it into its own function so the rejected states can actually be fed to it, added a test proving the constructor calls it, and wrote the reachability truth into the docstring instead of implying a risk that does not exist.

### The mutation sweep, and the three gaps it found in my own tests

I injected defects into my own finished code: 26 cases, one anchor at a time, each anchor asserted to match exactly once, focused tests run, files restored from pristine bytes and re-verified. All 26 now behave as required — but it took three rounds, and the two intermediate failures were worth more than the final green:

1. **A changed quantile method went uncaught.** My test helper had reimplemented the summary arithmetic, so every test that "checked" the distribution was checking a second copy that agreed with itself. Fixed at the root: the summary is now one function used by both production and the tests.
2. **Deleting a guard's call site went uncaught.** With the correct seed mapping, no duplicate seed can occur, so calling the guard and not calling it are behaviourally identical. Closed with a test that replaces the guard with one that always raises and confirms the caller reaches it.
3. **A truncated summary went uncaught even after fix 1** — because my test fixture used two samples, and at two samples every statistic is insensitive to both ordering and dropping one element. **The fixture was too small for its own property to be discriminating.** Now three, with the reason written beside the constant.

## Challenges and how they were overcome

**Distinguishing a report from a gate, from the other side.** In Session 45 I fixed a check that could not be told apart from one that examined nothing. Codex then found that I had fixed the *disclosure* and not the *enforcement*. Seeing my own lesson land one step short was the most useful thing in the session, and it is why I went looking for the wire rather than accepting six green tests.

**Implementing a pre-registered step whose prerequisite did not exist.** The protocol assumed a helper had been lifted into a shared module. Confirming it had not, and that lifting it meant editing closed evidence, was the session's one genuine judgment call. Resolved by doing the lift, keeping the change to two disclosed items, and proving byte-identical published output before claiming anything.

**Testing a stage I am not allowed to run.** Stage 0 must not execute before its own review, but handing over untested code is not a handoff. Resolved by splitting it the way the gate was split: pure layers covered portably, plus a few deliberately tiny calls into the measurement loop — three pairs at a shorter window, writing nothing — to cover the wires that pure tests structurally cannot reach. I stated that boundary explicitly in the tests and in the handoff so Codex can overrule the reading.

## Important decisions

- **Approved Codex's edited gate state unconditionally**, and said so at the top, so the approval could not read as contingent on the Stage-0 work in the same turn.
- **Did not commit the stray-write injection test**, for the same reason we both rejected a skip-by-default integration test.
- **Did not edit the cosmetic denominator imprecision**, to avoid a re-approval round-trip on a just-closed state; offered instead.
- **Put the lifted helper in a new module** rather than in the plant-side fixture module, on domain grounds, and handed the layout decision to Codex.
- **Deferred the packet runbook step for Stage 0.** A runbook step describes an executed, reviewed step; adding one now would place an unauthorized action in the reproduction path and point at an artifact that does not exist. Flagged rather than silently omitted.
- **Did not reopen the previous session's public log entry.** My Session-45 note had said a phrase in it ("no replay or screen stage has run yet") would need correcting. Codex's dated entry supersedes it in sequence, and the project's rule is that corrections propagate forward rather than by reopening earlier records. The log is chronological; each entry's claims are time-stamped by its date.

## Reasoning paths explored

- **Copy the gauge-window helper into Stage 0 instead of lifting it.** Rejected: two copies of a sensor driver is the exact failure mode under discussion, and the protocol pre-registers the lift.
- **Extract the hashing helpers into a shared module now.** Rejected for this session: it edits the gate at the state just approved. Recommended for when the stage driver lands.
- **Add a permanent end-to-end ephemerality test.** Rejected: it cannot run on a clean checkout.
- **Delete the unreachable invariant instead of keeping it.** Rejected: the protocol requires it and it still catches code defects; made testable instead.
- **Write the Stage-0 runbook step now with a "do not run" label.** Rejected in favour of deferring it to the session that runs the stage.

## Insights gained

1. **A test that calls a guard directly and a test that proves the program uses the guard are different tests.** Four instances in one session across two authors. The cheap way to tell them apart is to delete the call site and see whether anything goes red.
2. **A test fixture can be too small for its own property to be discriminating.** Two samples make ordering and truncation defects invisible, because every summary statistic is insensitive to both. This is a new failure mode for me: not a missing test, not an unreachable assertion, but a correct test whose *example* cannot express the flaw.
3. **Ask of every invariant whether the state it rejects is constructable.** When it is not, the invariant is guarding the code, not the data — and saying so plainly is more useful than an implication of runtime risk.
4. **Promoting a diagnostic to a hard gate deserves its own false-positive measurement.** The change is strictly stronger against real defects and strictly weaker against noise; the second half is worth a number.
5. **The most valuable review is of the fix to your own defect.** Codex fixed my hole correctly and left one behind of the same family; the only reason it surfaced is that I re-reviewed the fix as work rather than as a verdict.

## Files created or updated

- `Reproducibility Packet/scripts/analyze_synchronous_difference_null.py` — **new.** Protocol P Stage 0. Not run.
- `Reproducibility Packet/scripts/utils/gauge_windows.py` — **new.** The pre-registered shared gauge-window helper and thermal profile.
- `Reproducibility Packet/tests/test_synchronous_difference_null.py` — **new.** 72 tests.
- `Reproducibility Packet/tests/test_gauge_windows.py` — **new.** 15 tests.
- `Reproducibility Packet/scripts/analyze_synchronous_detection_floor.py` — modified to import the lifted helper; published artifacts proven byte-identical.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the owner re-review, approval, and Stage-0 handoff (+334 / −0).
- `README.md` — one Live-Run running-log entry.
- `agents/Claude/Session Summaries/HumanReport46.md` — this report.
- `agents/Claude/README.md` — workspace map updated.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten for Session 47.

Unchanged and verified: `config.json` absent, `results/protocol_p/` absent, `.gitattributes`, both `.gitignore` files, every dataset payload, `agents/Claude/references.md` (no external sources were read this session).

## Verification performed this session

```text
Codex's four claimed identifiers            reproduced exactly
focused replay-gate tests                   36 passed in 0.30 s
packet suite before my changes             478 passed in 11.42 s
replay gate, control run                    exit 0, 20/20 + 38/38, 3,124 files, 0 changes, 26.64 s
replay gate, stray write injected at t+8s   exit 1, ProtocolPError, path named, 27.03 s
repository clean after the injection         confirmed
detection-floor screen re-run               both published artifacts BYTE-IDENTICAL
Stage-0 mutation sweep                      26 / 26 cases behaved as required
new focused tests                           87 passed
packet suite after my changes              565 passed in 12.33 s
compileall                                  clean
Stage-0 module import cost                  0.21 s, writes nothing
results/protocol_p                          ABSENT
transcript append                           +334 / −0, header once at line 9700
Codex's Session-45 append                   +131 / −0, header once at 9570 — clean, no recurrence
```

## Next steps

1. **Codex reviews the Stage-0 implementation at exact state.** Four questions are open in the transcript: the lifted helper's home, whether to accept the gate import or extract now, confirmation of the seed pairing (the protocol pins the consumed range but not the pairing), and whether it wants a wall-clock figure before reviewing.
2. **Stage 0 must not run before that review.** Stages A/B/C remain unauthorized.
3. The packet runbook step for Stage 0 goes in with the session that runs it.
4. The stage driver, when built, must still satisfy Codex's enumerated requirements — the full override bundle, I3–I8, I13a, keying results from the explicit condition, and a real results-only persistence guard tested against the actual output root.
5. `config.json` stays absent and the test split stays untouched.
6. My next regular progress report is due at **my Session 48**, unless a phase transition or an approved written Claim Sheet amendment triggers one earlier.

## Cross-review performed

I read Codex's `HumanReport45.md` in full, its complete Session-45 transcript turn, the full diff of both files it edited, its packet-README changes, and the relevant sections of Protocol P v2.3.3 (§0, §6, §7, §8, §10, Corrections 2, 5, 6). I reproduced every measurement Codex reported. Its report is honest about scope, and its two stated insights are the correct generalization of my Session-45 lesson, carried one step further than I had carried it. I disagreed with nothing, added one clarification about which part of the dtype behaviour was actually repaired, and closed one gap its own fix had left.

No external literature was read, so `references.md` did not change. Session 46 is not a multiple-of-eight session, and no phase transition or approved written Claim Sheet amendment occurred, so no progress report was due.
