# Human Report — Codex Session 53

**Current date and time:** 2026-08-01 06:09 PDT

**Phase:** Phase 2 — Execution

**Session role:** Exact-state reviewer of Claude Session 53's returned public README and decision owner for Protocol-P reused-rollout provenance

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config/config.json` does not exist

**Protocol-P execution state:** Stage 0 remains executed exactly once and jointly approved. No replay, Stage-A/B/C rollout, or Stage-0 re-execution occurred this session. Stages A/B/C remain unexecuted. Driver/results implementation is now authorized for review, but execution remains unauthorized. The confirmatory test split remains untouched.

---

## Summary

Claude's Session 53 returned the newest public live-run entry after finding a third stale current-state claim in the same sentence both agents had already reviewed. The returned edit is correct: it replaces “nothing was executed / no screen stage has run” with the narrower and accurate state that no new measurement was spent, Stage 0 remains the only screen stage that has run, and Stages A/B/C remain unrun and unauthorized. I re-opened and approved root `README.md` at Git blob `ce5e8dce...` unchanged. This closes the public-entry review loop.

Claude also dry-ran the entire pre-registered Stage-A/B/C logical inventory through the approved construction layer and found a driver-level provenance hazard. Protocol P contains 180 logical result rows but only 168 physical rollouts because twelve rows reuse selected Stage-A measurements: eight Stage-B rows at remaining-EI 0.75/0.35 and four Stage-C `k=0` rows. Because `stage` is part of the provenance payload, asking the construction layer to rebuild those rows as Stage B or C mints twelve new hashes for bodies that do not run again.

I independently reproduced the full count and hash behavior from the real approved assignment, draft config, Protocol-P specification, and construction module. I accepted Claude's proposed origin-provenance rule: the physical rollout owns the provenance. A reused logical row cites its immutable Stage-A result, including the exact Stage-A provenance hash and canonical payload; it does not call the construction layer or generator and does not mint a new hash.

This ruling is a clarification of the existing specification, not an amendment. Protocol P already budgets 168 Stage-A/B/C rollouts and describes the twelve measurements as reused, while its provenance rule applies per rollout. The public loop is closed and Claude may now implement the narrow results module and driver for exact-state review. That permission does not authorize any rollout.

---

## What I reviewed

I followed the `AgentPrompt.md` workflow before acting:

- read the current project details, Codex continuity, Codex-involving chat summaries, transcript-monitoring thread, authoritative Phase-2 chronology/current tail, and Claude's latest human report;
- read the review-cycle and live-run README playbooks;
- reviewed root `README.md` at its exact returned bytes and audited the whole occurrence set for the stale phrase;
- read Protocol P's provenance scope, realized-identity table, Stage-A/B/C reuse rules, fail-loud invariants, result scope, and cost section;
- read the approved construction module's stage-identity and provenance paths; and
- independently rebuilt the 180-row logical inventory without simulation.

No production or test file was edited.

---

## Public README decision

### Approved unchanged

Exact state:

```text
README.md
  git blob    ce5e8dce3bdbef84865bbe7ba69526bfb17ad07e
  raw sha256  93046b1f470e73c16e3d49c7254977c924819dc33d4978b5f26e9ff88e152d8a
  bytes       76,726
```

The edit changes only the newest entry still under review. Four earlier uses of “No screen stage has run” are dated 2026-07-29 and were true when published. The returned entry now states all current boundaries accurately:

- no new measurement was spent;
- Stage 0 is the only screen stage that has run;
- Stages A/B/C have not run and remain unauthorized;
- the construction layer is jointly approved;
- the driver is not built or approved;
- config remains unfrozen; and
- the confirmatory split remains untouched.

Claude explicitly approved `ce5e8dce...`, and this session records Codex's explicit approval of that same state. The review loop is closed.

---

## Reused-rollout provenance ruling

### Accepted rule

Provenance belongs to the physical request that actually executed, not to every logical stage row that later consumes its measurement.

The driver/results representation must therefore enforce:

1. Stage-B remaining-EI values 0.75 and 0.35 in each cell cite the selected Stage-A structural rollout.
2. Stage-C `k=0` in each cell cites the selected Stage-A healthy rollout.
3. Those twelve reused rows do not call `build_overrides`, do not call `_generate_reservation`, and do not mint Stage-B/Stage-C provenance.
4. Each carries a fail-loud `reused_from` reference to an immutable Stage-A result key, plus the exact origin `rollout_provenance` and canonical payload.
5. The result schema distinguishes the logical consumer stage from the physical origin and never relabels an origin canonical payload.
6. The physical ledger contains 168 entries and 168 distinct stamps; the logical analysis inventory contains 180 rows, exactly twelve reused, all resolving to those 168 entries.

This follows the already-approved document rather than changing it: sections 6, 8, and 11 declare the reuses and the 168-rollout cost, while section 0 and invariant I8 require a stamp for each rollout. A reused row is not a new rollout.

### Required driver tests

Before execution can be considered, the handoff must discriminate:

- 180 logical rows against 168 physical executions;
- exactly twelve correct Stage-A reuse references;
- zero construction/generator calls for reuse rows;
- zero new provenance hashes for reuse rows;
- exact provenance-hash and canonical-payload equality to each origin;
- onset derived from the bound trajectory and control timestep, with off-grid refusal; and
- the real driver wired to a real temporary results root, with an injected wrong write failing the results-only persistence gate.

The selected candidate remains a Stage-A result. Tests may inject a selected result as a fixture but may not let a placeholder leak into production selection or a persisted result.

---

## Independent inventory check

I used the project virtual environment and the actual approved documents/module to construct every logical request without simulation. A placeholder admissible candidate was used only to instantiate the post-selection reuse arithmetic.

```text
admissible candidates                    9
logical rows                            180
distinct physical request keys          168
distinct request stamps if all built    180
reused rows whose stage changes hash     12
derived onset index                     500
config.json                             absent
```

This reproduces Claude's hazard: the twelve reused bodies receive new hashes only because `stage` changes inside the canonical provenance payload. The correct driver behavior is to reference the existing Stage-A physical result rather than construct another request.

---

## Verification

```text
full packet suite                         750 passed in 13.28 s
compileall                                clean
git diff --check                          clean (checkout-EOL warning only)
config.json                               absent
Stage-0 artifact                          unchanged; not re-executed
replay / Protocol-P stage rollouts        none this session
confirmatory test split                   untouched
```

The transcript append passed the hard gate:

```text
pre-write lines                           12,730
pre-write bytes                           887,661
old-prefix SHA-256                        373b46a1003b625bb51af5e186a295875e808a29bb50b99049c4d1fd3d6bda02
old prefix after append                   exact
Codex Session-53 header                   exactly once, line 12,734
header after pre-write boundary           yes
transcript diff                           +108 / -0
physical tail                             Codex Session 53
```

---

## Challenges and reasoning

### Separating a logical row from a physical rollout

The construction layer correctly produces a unique provenance identity for every request it receives. The problem appears only if the driver treats a reused logical stage row as a new request. Keeping a physical ledger separate from the logical analysis view makes the cost, provenance, and reuse semantics agree without weakening the construction layer's stage-binding checks.

### Determining whether the ruling changes the protocol

The specification already says the relevant Stage-B and Stage-C measurements are reused and already budgets no new rollout for them. The provenance text says per rollout, not per report row. The ruling makes the future implementation obey those two existing statements; it does not alter a success criterion, identity formula for an executed request, cost, stage, or scientific estimand.

### Closing the public entry without another edit

Claude's returned sentence repairs both stale clauses and leaves the rest of the active entry intact. A broader rewrite would have added churn to a state that now says exactly what the evidence supports.

---

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the exact-state README approval, independent inventory reproduction, reuse ruling, and driver implementation gate.
- `agents/Codex/Session Summaries/HumanReport53.md` — this report.
- `agents/Codex/README.md` — adds Session 53 and updates the authoritative Phase-2/public-state routing.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the next session.

No public README, production module, test, protocol specification, assignment, config, dataset payload, result artifact, or confirmatory material changed in Codex Session 53.

No progress report was due: Session 53 is not an every-eighth session, and no phase transition or approved Claim Sheet amendment occurred.

---

## Next steps

1. Claude may implement the Stage-A/B/C results module and driver under the 180-logical / 168-physical origin-provenance rule and hand the exact state to Codex for review.
2. Driver implementation is not execution authorization. No replay or Stage-A/B/C rollout may run before the driver review loop closes explicitly.
3. After any eventual development-screen result, Amendment A2, a replacement approved assignment/config lineage, coherent regeneration, Gates 4–7, joint final config approval, and one-shot confirmatory generation remain downstream.
4. The next regular Codex progress report is Session 56 unless an approved amendment or phase transition triggers one sooner.

— Codex
