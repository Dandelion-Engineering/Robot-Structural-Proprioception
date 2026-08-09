# Codex Human Report - Session 99

**Date and time:** 2026-08-08 22:12 PDT

**Phase:** Phase 2 - Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset:** 0. **Checkpoint writes:** 0. **Data generation:** 0.
**Pilot / validation / test outcome reads:** 0. One zero-fit plan artifact was published. Plan
mode received no `--data-root` and read no observation payload, approved checkpoint or reserved
outcome.

**Progress-report session:** no. The next regular Codex progress report is Session 104 unless a
phase transition or approved Claim Sheet amendment fires sooner.

---

## Summary

Session 98 ended with a repaired capacity-sweep executable that Codex approved, plus one
reviewer-edited test file that Claude still had to re-open and approve. Claude Session 99 did that
work genuinely: it drove a ten-case mutation sweep against both test states, confirmed that the old
tests missed three broken point-iteration forms rather than the one Codex demonstrated, verified
that the reviewer edit weakened nothing, and explicitly approved the same production/test blobs
Codex had approved. That closed the first gate of the restart sequence.

This session completed only the next gate. After verifying the exact approved code state and the
preservation preconditions, I ran one `--mode plan` invocation for `stage1-run-2`. It produced the
exact artifact Claude had predicted in advance: SHA-256
`ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31`, 13,786 bytes. I audited
the document independently, explicitly approved its exact bytes, and handed it to Claude for the
second gate-2 review.

The plan was deliberately written under
`Reproducibility Packet/results/capacity_sweep/plans/stage1-run-2/`. That preserves the consumed
`stage1-run-1` plan in place and leaves the actual execution root
`results/capacity_sweep/stage1-run-2/` absent for a later atomic claim. No execution authorization
half was issued. Every fit and checkpoint write remains blocked.

## What was accomplished

### 1. Reconciled the live review state

- Read the current Phase-2 transcript and Claude's Session-99 report rather than relying on the
  older automation memory.
- Verified production blob `53e5dcb79d4f8c131b6856fd5fa57fce6049976a` and test blob
  `6d49edde03e24a262e4246669fad8e42859c6f8a` in the working tree.
- Accepted Claude's explicit same-state approval as closure of the Finding-AU executable/test loop.
  This was approval of exact bytes, not approval inferred from a handoff.
- Cross-reviewed Claude's mutation evidence. The important additional result is that the original
  returned tests were blind not only to `for point in [48]`, but also to a three-of-four subset and
  reverse iteration. The reviewer sequence assertion closes all three without weakening the old
  coverage.

### 2. Verified the one-plan preconditions

Immediately before plan mode:

```text
git working tree                         clean
.claude-session.lock                     absent
.agent-session.lock                      present (this session)
approved production/test blobs           exact
consumed plan                            present, SHA-256 bdf674d5...1c0a5
failed stage1-run-1 root                 present
new plan-history directory              absent
stage1-run-2 execution root              absent
config/config.json                       absent
tracked checkpoints                      0
packet checkpoint files                  13 (10 anchors + 3 preserved failed-run files)
Python processes                         0
```

The one authorized invocation was:

```powershell
..\venv\Scripts\python.exe -B -m utils.capacity_sweep `
  --mode plan `
  --run-label stage1-run-2 `
  --output-dir results\capacity_sweep\plans\stage1-run-2
```

It returned:

```text
X_PLAN_OK: 40 new arms + 2 equivalence arms planned at run label stage1-run-2, 0 fits run
```

### 3. Audited the plan independently

The published artifact is:

```text
Reproducibility Packet/results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json
  Git blob                 d7104e55b4fb9be3fbfa6bd685b002a055409673
  canonical/raw SHA-256    ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
  size                     13,786 bytes
  encoding shape           UTF-8, zero CR bytes, no BOM, no final newline
```

The independent audit imported nothing from the producer module. It parsed and compactly
re-emitted the JSON, compared every leaf to the consumed plan, rebuilt the exact arm and
destination sets, and checked the executable identity directly from canonical source bytes.

```text
canonical compact re-emission                       byte-identical
full leaves, consumed / replacement                 413 / 413
added / removed / changed leaves                    0 / 0 / 48
changed leaves                                      40 curve checkpoint paths
                                                    + 2 equivalence checkpoint paths
                                                    + 4 namespace/artifact paths
                                                    + run_label
                                                    + capacity_sweep.py identity
new curve grid                                      {16,24,40,48} x {C1,S} x seeds 0-4
anchors / new arms / equivalence arms               10 / 40 / 2
declared destinations                               44 distinct, all packet-relative
maximum budget                                      42 fits / 42 checkpoints
generation / rollouts / non-development reads      0 / 0 / 0
other eight code identities                         unchanged
anchors / approved document bindings / protocol    unchanged
```

The producer's own `require_authorized_plan()` gate accepts the exact plan and digest. This proves
the published artifact is not merely well-shaped JSON; it is the document the approved executable
would accept at a later execution gate.

### 4. Preserved the failed evidence and authorization boundaries

- The consumed plan remains SHA-256 `bdf674d5...1c0a5` in its original path.
- The failed result remains SHA-256 `2be7e421...7559`.
- The failed equivalence artifact remains SHA-256 `e5afaec2...8182`.
- All 13 ignored checkpoint files remain present. None was moved, deleted, imported or reused.
- The `stage1-run-2` execution root remains absent.
- `config/config.json` remains absent.
- No old Step-4 half was carried forward. Both old halves remain spent.
- The transcript handoff explicitly says the new plan approval is **not** an execution-authorization
  half.

### 5. Verification

```text
capacity-sweep focused suite                    217 passed
capacity-sweep focused suite, python -O         217 passed, 1 expected pytest warning
full Reproducibility Packet suite             1,768 passed
compileall                                      clean
git diff --check                                clean before closeout edits
plan independent audit                          AUDIT_OK
require_authorized_plan exact-plan probe        accepted
```

The first focused-test launch was interrupted by an overly short tool timeout, which closed
pytest's output stream and produced an `OSError` during reporting. It was not a test failure and
made no project change. The same command was rerun with the correct long-running window and passed
217 tests.

### 6. Recorded the handoff under the append-only hard gate

The Phase-2 transcript append used a physical UTF-8 EOF block verified unique before the write.
Post-write assertions passed:

```text
pre-write bytes                 1,715,147
pre-write LF count              27,535
pre-write SHA-256               7571b1f7...eb493
prior prefix retained           exact
new header count                1
new header physical line        27,537
final bytes                     1,719,036
final LF count                  27,606
final SHA-256                   baa7e17e...ffd4b65
Git diff                        +71 / -0
physical last speaker           Codex
```

No Transcript Order Monitoring entry was needed.

## Challenges and how they were handled

### `CODEX_HOME` was unset

The automation memory instruction names `$CODEX_HOME`, but that variable was null in this process.
I used the known Codex home at `C:\Users\cresp\.codex`, read the existing automation memory, and
did not treat the failed lookup as project state.

### The first audit probe used one wrong field name

My independent JSON probe expected `n_reused_anchors`; the actual document names the field
`n_anchor_arms`. The probe stopped with `KeyError` before completing and wrote nothing. I enumerated
the actual schema keys, corrected that field and the analysis-digest field name, then reran the
full audit to `AUDIT_OK`.

### The first transcript verifier was computationally poor

The initial post-append verifier tried to count 1.7 million bytes through a PowerShell object
pipeline and timed out before producing a result. It made no write. I replaced it with direct byte
loops and re-ran every required prefix, uniqueness, line-boundary, physical-tail and additions-only
assertion successfully.

## Important decisions

1. **Publish the new plan in a plan-history directory.** Overwriting the consumed plan would erase
   the exact plan named by the failed evidence. Writing the plan at the future run root would make
   the later atomic claim fail by construction. The separate `plans/stage1-run-2/` directory
   preserves both invariants.
2. **Approve the artifact, not the execution.** The exact plan is owner-approved and ready for
   Claude's audit. That approval does not spend or imply a Step-4 authorization half.
3. **Use Claude's prediction as an independent instrument.** The artifact matched a digest and byte
   count recorded before it existed. That is materially stronger than deriving an expectation only
   after looking at the published bytes.
4. **Keep the public statement narrow.** The noteworthy event is a deterministic replacement plan
   that matched the pre-registered fingerprint. It is still only planning: no capacity curve,
   model-selection result, final configuration or confirmatory evidence exists.

## Files created or updated

- `Reproducibility Packet/results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json`
  - new exact zero-fit plan artifact.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  - additions-only owner approval and Claude handoff.
- `README.md`
  - lean public milestone for the predicted replacement plan's publication; no phase/banner change.
- `agents/Codex/Session Summaries/HumanReport99.md`
  - this report.
- `agents/Codex/README.md`
  - workspace index and current gate state.
- `agents/Codex/Summary of Only Necessary Context.md`
  - completely rewritten resume state.

No source, test, protocol, consumed plan, failed-run evidence, checkpoint, configuration or data
file was modified.

## Next steps

1. Claude independently audits and either explicitly approves exact plan blob
   `d7104e55b4fb9be3fbfa6bd685b002a055409673` / SHA-256 `ffb00965...b7cb31` or returns an edit.
2. Only after same-state plan approval, the agents separately record a fresh two-half Step-4 joint
   authorization naming that digest, label, base, exact executable, anchors and maximum budget.
3. Only after both matching halves exist may one execute invocation claim
   `results/capacity_sweep/stage1-run-2/`, rerun both C9 fits, and attempt the forty curve fits.
4. The exact result then requires joint review before section 5.4 or C7. Capacity selection,
   pilot/validation/test reads, final config freeze, generation, rollouts and confirmatory use remain
   blocked.

**Next Codex session number:** 100.
