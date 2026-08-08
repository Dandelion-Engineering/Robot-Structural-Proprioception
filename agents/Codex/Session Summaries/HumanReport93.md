# Codex — Human Report, Session 93

**Date and time:** 2026-08-07 22:14 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Plan artifacts: 0. Data generated: 0. Pilot / validation / test reads: 0.**

**Progress-report session:** no. The next regular Codex progress report is Session 96; no phase transition or Claim-Sheet amendment occurred.

---

## Summary

Claude Session 93 genuinely owner-reviewed the six Session-92 findings, accepted their
implementations, and returned a new Route-A capacity-sweep executable/test pair with three
additional repairs. I reopened both returned files in full and accepted all three repairs:
plan mode now invokes invariant C1 before its first write, the C9 checkpoint name has one
validated definition used by both plan and gate, and the maximum-budget comment no longer
claims a runtime assertion the code does not make. My review then found one further measured
C1 defect in Claude's new call site: plan mode checked a resolved destination but discarded the
resolved return and later wrote through the original relative spelling. A deterministic
temporary-root reproduction changed the working directory after the guard and showed the plan
landing inside a fake protected `results/dev_fit` tree. I repaired the binding with one line,
added a regression test, and explicitly approved the new reviewer-edited exact state. The
focused suite passes 203 tests normally and under `python -O`; the full packet suite passes
1,754 tests. The executable loop remains open for Claude's owner re-review. No plan mode, fit,
checkpoint, generation, rollout or later-role read was authorized or performed.

---

## What I reviewed

### Claude's returned owner state

Claude handed back and explicitly approved:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 9a1d11a73239226e5458a4ac84ecfa7caadbc26a
  canonical/raw SHA-256    d4db066544a5fa8962af516e9c2794dc7220b2088fdfb66c91c68fa14b65dddf

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 2a043f99d2d7703b921a9d01dd3bbdb63bba2e35
  canonical/raw SHA-256    81e6e1e5c705d3afbe1e5a39d8bb357c1e4e8f1684d8a89bae4922a0e0eb0ff3
```

Those bytes are superseded by the reviewer edit below and must not be approved.

### AO — plan-mode C1 guard

Accepted. The frozen design constrains the executable, not only execute mode. Claude correctly
added the same protected-tree refusal before plan mode's first write and reused
`X_FORBIDDEN_BASE`. The test proves the tracked approved checkpoint directory gains nothing.

### AP — one C9 checkpoint-name definition

Accepted. `equivalence_checkpoint_name(suite, seed)` is now the single validated definition;
`equivalence_relative_name` composes it and `equivalence_gate` uses it when writing. The new
test compares the exact plan-declared paths to the files the synthetic gate physically writes,
closing the prior consequence-only count check.

### AQ — accurate maximum-budget comment

Accepted. The 42-fit budget is an arithmetic property of the fixed arm lists, pinned by a test;
it is not a runtime ceiling checked on every exit. Correcting the comment is smaller and more
accurate than inventing a new unreachable refusal path.

### Session-92 findings AI through AN

Claude explicitly accepted and adversarially re-drove all six findings and the two additional
persistence hardenings. I checked that his returned edits did not regress them. There is no
same-issue disagreement to escalate.

---

## Finding AR — the validated destination was not the destination used

`require_permitted_base` resolves its input and returns the exact path it checked against the
protected packet tree. Execute mode already stores and uses that return. Claude's new plan-mode
call invoked the helper only for its side effect:

```python
require_permitted_base(output_dir)
```

The subsequent writes still used the unresolved original `Path`. That is a check/use split.
Under a temporary fake packet root I supplied relative `--output-dir plan`, let C1 resolve it
under a safe working directory, then changed the process working directory to the fake
protected tree after the guard. The handed-back state produced:

```text
initial cwd                 <tmp>/safe
checked destination         <tmp>/safe/plan
cwd after the guard         <tmp>/packet/results/dev_fit
safe write present          False
fake protected write        True
```

No real packet path or real result was touched. The production protocol does not intentionally
change the process working directory, but C1 is an executable invariant rather than a
convention about imported calls or concurrent threads. The resolved path is the object the
guard authenticated and must remain the object the writer consumes.

The repair is:

```python
output_dir = require_permitted_base(output_dir)
```

The regression test performs the same transition under `tmp_path` and proves the plan stays at
the resolved safe destination. It fails on Claude's returned bytes and passes on the reviewer
state.

---

## New exact reviewer state

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 907394d0dda086fb694174b77f0caedbbfd2dff8
  canonical/raw SHA-256    00b341d04b2e5c9a537a28723a2453490ca6e52b6ca3de432cb259c474c9b0ce
  physical state           93,933 B / 2,198 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 240fb77aa9c0c921139709b2a86645a41c0198e7
  canonical/raw SHA-256    85e80331669130818aadac0c091ee130ed376d82dfc39b9f8ea0766563acfe42
  physical state           78,900 B / 1,937 lines / LF / no BOM / 203 tests
```

I explicitly approve both exact reviewer-edited files. Claude must genuinely reopen and
owner-review these same blobs. The executable loop closes only if Claude explicitly approves
them unchanged; an edit creates another exact state and returns the loop to Codex.

---

## Verification

```text
targeted AR regression                1 passed in 1.41 s
focused Route-A tests               203 passed in 4.00 s
focused tests under python -O       203 passed in 4.10 s
full packet suite                 1,754 passed in 131.82 s
compileall                          clean; cache redirected outside the repository
git diff --check                    clean
capacity plan/result artifacts      absent
config/config.json                  absent
fits / checkpoint writes            0 / 0
generation / rollouts                0 / 0
```

The focused tests necessarily read the approved tracked `dev_fit_result.json` and
`dev_fit_analysis.json` as comparability and deterministic-plan metadata. They do not read
delivered observation payloads or approved `.pt` checkpoint bytes. This is a forward
precision correction to Claude's broader Session-93 phrase that no tracked result file was
read; the zero-real-execution boundary remains intact.

The frozen design remains unchanged:

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob                 b45efa477de10331ca61e1af73b2834b22df3fb6
  canonical/raw SHA-256    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
```

---

## Transcript hard gate

The Session-93 handoff was appended to the active Phase-2 transcript using the physical-EOF
hard gate:

```text
pre-write bytes          1,603,230
pre-write lines          25,622
pre-write SHA-256        e52aae95dc2c0936d13a96c00e4dcbf902e987630800b90fe7d4b7890caa1227
EOF-anchor occurrences   1
final bytes              1,608,413
final lines              25,733
Codex header line        25,624; unique and after the boundary
final SHA-256            430a0751d60e52472ec8410f49e41c67d6cc49b21ccc42708656b73ee9a3aa43
diff                     +111 / -0
last agent               Codex
```

The complete old byte prefix remains identical and the appended turn is physically last.

---

## Decisions

1. **Returned AO/AP/AQ implementations accepted.** They are correct, narrow and consistent
   with the frozen design.
2. **Reviewer edit rather than same-state approval.** AR is a measured invariant violation,
   so approving around it would create a false two-agent closure.
3. **One-line destination binding.** The guard already returns the authenticated resolved
   path; consuming that return is sufficient and adds no new policy or exit.
4. **Public README unchanged.** The review loop remains open, no phase moved, no new result
   exists and the live log is milestone-based.
5. **Execution boundary preserved.** Code review licenses no plan, fit, checkpoint or later
   action.

---

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport93.md` — this report.

Updated:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py` — binds plan mode to the resolved,
  C1-checked destination.
- `Reproducibility Packet/tests/test_capacity_sweep.py` — adds the temporary-root destination
  binding regression.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only exact-state handoff and forward evidence correction.
- `agents/Codex/README.md` — Session-93 navigation and current exact-state pointer.
- `agents/Codex/Summary of Only Necessary Context.md` — fully rewritten Session-93 resume state.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`
- `README.md`
- `Reproducibility Packet/README.md`
- `.gitignore` and `Reproducibility Packet/.gitignore`

---

## Cross-review

I read Claude's `HumanReport93.md`, both returned files, and the complete Session-93 transcript
turn. The report accurately describes the AO/AP/AQ code changes, exact returned identities and
zero-execution boundary. Its statement that no tracked results file was read is too broad
because the focused tests read the approved ledger and analysis JSONs; I corrected that
forward in the live transcript rather than rewriting Claude's historical report.

---

## Next steps

1. Claude owner-reviews exact blobs `907394d0...` and `240fb77a...`.
2. If Claude explicitly approves them unchanged, the Route-A executable loop closes.
3. Only after that closure may the agents separately authorize one deterministic zero-fit plan
   run and review its exact artifact.
4. The two C9 fits and forty curve fits remain a later separate joint authorization naming the
   approved plan digest.
5. The C7 read-only analysis build, every later-role read, Stage 2, final config, generation and
   all rollouts remain blocked.

— Codex
