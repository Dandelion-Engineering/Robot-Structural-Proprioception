# Codex — Human Report, Session 95

**Date and time:** 2026-08-08 06:10 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Capacity fits: 0. Checkpoint writes: 0. New or regenerated plan artifacts: 0. Data generated: 0. Pilot / validation / test reads: 0.** The test suite read the approved development ledger and analysis artifact as fixtures and plan metadata. It opened no delivered observation payload and no approved checkpoint.

**Progress-report session:** no. Codex Session 96 owes the next regular progress report; no phase transition or Claim-Sheet amendment occurred.

---

## Summary

Claude's independent review found that the official zero-fit capacity plan faithfully described the approved sweep but did not mechanically bind one imported module: `scripts/analyze_dev_fit.py`, which both loads every training example and computes every arm's reported classification metrics. The plan bound the approved analysis artifact, and that artifact recorded the analyzer's digest, but the sweep never compared the recorded digest with the module it actually imported. Claude measured the gap: a macro-F1 mutation left the plan byte-identical, and a row-order mutation also survived the relevant behavioral tests. I ruled the finding in and implemented Claude's recommended sibling guard. Plan construction and execution authorization now compare the exact analyzer identity carried by the approved analysis artifact with the canonical identity of the imported analyzer before any spend can occur.

The repair changes the sweep executable's own digest, so the Session-94 plan is now mechanically rejected as having been written by a different code state. I deliberately did not regenerate it: the reopened executable review must close on the exact new code and tests first. The new state is explicitly approved by Codex and handed to Claude for genuine re-review. Every fit remains blocked.

---

## Cross-review and ruling on Finding AT

I read Claude's `HumanReport95.md`, its full Session-95 transcript turn, the exact plan, the live sweep/analyzer sources, the frozen design's section 7.1 binding requirement, and the current authorization gate.

Claude's finding is correct. The prior chain was:

```text
plan
  -> binds dev_fit_analysis.json
       -> records analyze_dev_fit.py digest

capacity_sweep.py
  -> imports analyze_dev_fit.py to load and score arms
  -> never compares the imported file with the recorded digest
```

The two C9 equivalence fits would detect some loading changes only after spending two fits and would not detect a scoring-only mutation because C9 compares weights and loss histories, not macro-F1. Treating that residual coverage as sufficient would leave the pre-spend authorization gate blind to a module the frozen design explicitly says to bind.

I accepted the recommended repair rather than adding `analyze_dev_fit.py` as a tenth `sweep_code_identity()` entry. A tenth entry would violate C3's exact rule: eight historical fitting identities plus only `capacity_sweep.py`. The sibling guard converts the existing transitive record into an executable check without changing that cardinality contract.

---

## Implementation

Updated `Reproducibility Packet/scripts/utils/capacity_sweep.py`:

- added the exact nested path `inputs.analysis_code_identity.analyze_dev_fit.py` as a named contract field;
- added `require_approved_analyzer_identity(analysis)`, which validates the recorded digest, hashes the imported analyzer's exact file through the existing code-identity mechanism, and refuses on disagreement; and
- called the guard from `plan_document()` after anchor comparability is authenticated and before plan arms are built.

Because `require_authorized_plan()` rebuilds `plan_document()` and requires exact equality before returning, the same analyzer check runs at both boundaries:

```text
plan mode before a valid plan is written
execute authorization before the plan can name any run path or spend
```

Updated `Reproducibility Packet/tests/test_capacity_sweep.py` with three new tests:

1. the real approved analysis identity equals the imported analyzer identity;
2. a synthetic changed imported analyzer is refused directly; and
3. a synthetic analyzer change made after planning is refused by `require_authorized_plan()`.

The third test depends on the guard being called from the plan reconstruction path; deleting that call makes it fail, so a dormant helper cannot satisfy the suite.

---

## Exact state and approval

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 61d4fb97c2d87606134cbf0a1e1c4458e4997cd6
  canonical/raw SHA-256    d91db2effbdc05001eebd3838eee19852f4fd7b4e90f684543f224a1e45f821e
  physical state           96,715 B / 2,259 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 07da31824bb7a9ed50d3b048e39d171c40c41ca9
  canonical/raw SHA-256    bb64a85010581de0dd6a5d635feb049fe8461df60acf1609919e494c93be25c7
  physical state           83,990 B / 2,062 lines / LF / no BOM / 207 tests
```

I explicitly approved these exact two blobs and handed them to Claude. The reopened executable review remains open until Claude explicitly approves these same bytes unchanged. An edit or handoff is not approval.

---

## Plan state and execution boundary

The existing plan remains unchanged in the repository:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 d2584d28f8ecc1d82d24d4480cee9ff7481611a9
  canonical/raw SHA-256    740d5db96657c7a5e9a86b49816daf091439e7661a6bd971fb8ce6ab3ae1c00e
```

The repaired executable rejects it with:

```text
DevFitContractError: the authorized plan was written by a different code state
```

Codex's Session-94 approval remains historical evidence about those exact bytes, but it cannot close the current Step 3. The plan is superseded and mechanically unauthorized. I did not overwrite or regenerate it. Once Claude approves the repaired executable/tests unchanged, one zero-fit re-plan may replace the still-active plan artifact and receive a fresh two-agent exact-state review. Since no capacity execution has occurred, the run label can remain `stage1-run-1`; the frozen design's new-label rule governs a second execution, not correction of a pre-execution plan.

I also accepted Claude's reproduction-command correction. The future packet runbook must invoke the module from `Reproducibility Packet/scripts/` and point its output to `../results/capacity_sweep`. Session 94's published command remains historical rather than being edited backward.

No Step-4 fit authorization exists. Both C9 fits, all forty curve fits, every capacity checkpoint write, C7 analysis, pilot/validation/test reads, Stage 2, final `config/config.json`, generation and all rollouts remain blocked.

---

## Verification

```text
targeted analyzer tests                  5 passed
focused Route-A tests                  207 passed in 3.50 s
focused tests under python -O          207 passed in 3.72 s
full packet suite                    1,758 passed in 116.41 s
compileall                              clean
git diff --check                        clean
old plan authorization probe            refused: different code state
capacity result files                    only the unchanged plan
capacity checkpoints outside dev_fit     0
config/config.json                       absent
fits / checkpoint writes                0 / 0
new or regenerated plan artifacts       0
generation / rollouts                    0 / 0
```

The full suite used the required project virtual environment and packet-scoped `PYTHONPATH`. No bare Python invocation was used.

---

## Transcript hard gate

The Phase-2 transcript append used its exact UTF-8 physical tail and passed every assertion:

```text
pre-write bytes       1,639,880
pre-write lines       26,289
pre-write SHA-256     f4cc6efc14ff259b74a53c4af15ff0993bedbf4da8001ee3852120e81e5fcaf2
prefix after append   byte-identical
new header            unique at line 26,291, after the recorded boundary
post-write bytes      1,645,051
post-write lines      26,391
post-write SHA-256    fa7705076769614eb697d2ff25fd140d38deb69e7b511d918bb4841010b6ca67
Git diff              +102 / -0
physical last agent   Codex
```

No Transcript Order Monitoring entry was needed because there was no recurrence.

---

## Challenges and reasoning paths

- **The plan itself was faithful.** Blocking only its bytes would have targeted the wrong layer. The defect lived in the executable contract the plan inherited.
- **The obvious tenth identity was invalid.** C3 deliberately permits only one addition to the historical fit identity. The repair therefore had to authenticate the analyzer beside, not inside, that nine-entry set.
- **Approval sequencing matters.** Regenerating immediately would create a plan from code that only one agent has approved. I kept the old plan visible and invalidated, reopened executable review, and preserved plan regeneration as the next zero-fit act after same-state code closure.
- **The old command was wrong but the old artifact was not.** The correction propagates into the future runbook instead of rewriting a concluded report.

---

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport95.md` — this report.

Updated:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py` — analyzer identity guard.
- `Reproducibility Packet/tests/test_capacity_sweep.py` — three direct regressions.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — append-only ruling, exact-state approval and handoff.
- `agents/Codex/README.md` — current navigation and Session-95 entry.
- `agents/Codex/Summary of Only Necessary Context.md` — fully rewritten resume state.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json` — preserved as the now-superseded plan under review; not regenerated before executable approval.
- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` — frozen design.
- `Reproducibility Packet/scripts/analyze_dev_fit.py` and approved development artifacts — identity sources, unchanged.
- root `README.md` — heartbeat checked. This session reopened a technical review and produced no public milestone, so the lean public log remains unchanged.
- `.gitignore` and `Reproducibility Packet/.gitignore` — already cover the session lock, environments, caches, generated model payloads and logs; no update required.

---

## Next steps

1. Claude genuinely reviews exact blobs `61d4fb97...` and `07da3182...` and explicitly approves or edits them.
2. If Claude approves unchanged, the executable loop re-closes; only then regenerate the zero-fit plan at `stage1-run-1` using the corrected working-directory invocation.
3. Both agents independently review and explicitly approve the regenerated plan's exact bytes.
4. Step 4 remains a later separate joint authorization naming that plan digest. No fit may run before it.
5. Codex Session 96 writes the next regular progress report in addition to normal session work.

— Codex
