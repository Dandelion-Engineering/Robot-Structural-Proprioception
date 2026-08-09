# Codex — Human Report, Session 98

**Date and time:** 2026-08-08 18:16 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits / checkpoint writes / data generation:** 0 / 0 / 0. **Pilot / validation / test reads:** 0 / 0 / 0.

**Progress-report session:** no. The next regular Codex report is Session 104 unless a phase transition or approved Claim Sheet amendment fires sooner.

---

## Summary

Claude Session 98 issued the second Step-4 authorization half, ran the one authorized
`stage1-run-1` capacity sweep, and found **Finding AU** after 31.3 seconds. The run spent two C9
equivalence fits and one curve fit, then stopped at `X_OUTPUT_DIRTY`: the executable checked a
shared capacity-point directory once per arm, so the second arm treated the first arm's checkpoint
as contamination from an earlier attempt. The failed root is preserved as required. C9 passed on
both suite paths, but one curve arm is not a curve and licenses no capacity interpretation.

I independently audited the preserved run state, the frozen design, Claude's production repair,
and the returned tests. I **approve the production repair unchanged**, including Claude's separate
judgment to place the capacity-point cleanliness checks above C9. Once the root has been atomically
claimed and the authenticated dev inputs have loaded, a dirty point can be detected before the two
irreversible equivalence fits. Putting the check below C9 would spend two fits to learn an existing
output-cleanliness fact and would not close the already-disclosed concurrent-writer residual.

The returned tests had one live coverage gap. Replacing the repaired four-point loop with
`for point in [48]:` in a disposable packet copy still passed all three new tests, even though
widths 16, 24, and 40 were never checked. I reviewer-edited the whole-loop test to wrap the real
guard and assert the exact once-each sequence for all four point directories. The same mutation
then failed. The exact reviewer state passes 217 focused tests normally and under `python -O`,
1,768 packet tests, and compilation.

Because I changed the test file, the executable review loop remains open for Claude's genuine
owner re-review of the exact reviewer test blob. I did not regenerate a plan. The consumed
`stage1-run-1` plan and both authorization halves remain spent, and the repaired executable
mechanically refuses that plan as a different code state.

## What was accomplished

### 1. Reconciled the live state and reviewed Claude Session 98

- Read the controlling project documents, Codex continuity, all Codex-including chat summaries,
  the live Phase-2 tail, Claude continuity, and Claude's `HumanReport98.md`.
- Confirmed `HEAD == origin/main` at Claude Session 98 before making Codex-owned changes.
- Re-read `Playbooks/review-cycle.md` and `Playbooks/reproducibility-packet.md` before reviewing the
  packet artifacts.
- Kept the review scoped to the exact handoff: production blob `53e5dcb7...`, returned test blob
  `2dc93297...`, the preserved failed-run evidence, and the design clauses they implement.

### 2. Independently reconstructed the failed-run state

The tracked artifacts remain:

```text
Reproducibility Packet/results/capacity_sweep/stage1-run-1/capacity_sweep_result.json
  Git blob                 32743393908cf7a5f2109eabb034eafe849d78a7
  raw SHA-256              2be7e421cfff103296b94a1ba3c539320a334f8e242e4352994b10be54817559

Reproducibility Packet/results/capacity_sweep/stage1-run-1/_equivalence/
  capacity_sweep_equivalence.json
  Git blob                 cd8bdc1421961c6d7b3a828992e8f22996003370
  raw SHA-256              e5afaec2b525d38f8a8d421bcc74d3370b97edc9e84a9b8035d88725946b8182
```

Independent parsing reproduced:

```text
exit / reason              X_OUTPUT_DIRTY / DevFitContractError
fits                       3 = 2 equivalence + 1 curve
checkpoint writes          3 = 2 equivalence + 1 curve
curve census               10 REUSED / 1 COMPLETED / 39 UNATTEMPTED
rollouts / generation      0 / 0
non-development reads      0
C9 C1 seed 0               PASS, produced digest == approved digest
C9 S seed 4                PASS, produced digest == approved digest
```

All three ignored `.pt` files exist and match the digests in the artifacts. The tracked JSON and
ignored checkpoint evidence were not modified. The one completed 16-channel C1 seed-0 arm remains
development evidence from a partial run, not an analyzable curve.

### 3. Ruled on the production repair

The approved production state is:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
  canonical/raw SHA-256    be07d95e4b4b9fa1a8934a165681fdbc9e7e885236bd1de3c38b661288f641fa
```

The once-per-point move is required by C2: there is one output directory per width and ten arms
share it. The above-C9 move is also approved. The check occurs after the atomic root claim and
authenticated input loading but before any fit or checkpoint. This preserves C9's requirement to
run before every curve fit while preventing a known output refusal from needlessly spending the
two C9 fits.

The concurrency boundary is unchanged and stated rather than overclaimed: a foreign writer can
race any pre-use check. Moving the check closer to the curve loop narrows a timing window but does
not create a guarantee; it only guarantees a two-fit cost first.

### 4. Found and repaired the returned-test gap

The returned tests correctly caught:

- the original per-arm placement;
- the below-C9 placement; and
- a call site nested inside the curve-arm loop.

They did not verify that all four directories were visited. In a disposable copy I replaced the
four-point iterator with `[48]`; the three tests still reported `3 passed`. I then edited the
whole-loop test to record calls through the real guard and require exactly:

```text
channels_016, channels_024, channels_040, channels_048
```

With that reviewer edit, the skipped-point mutation fails one of the three tests. No production
line changed in Codex Session 98.

The reviewer-approved test state is:

```text
Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 6d49edde03e24a262e4246669fad8e42859c6f8a
  canonical/raw SHA-256    640f23b5990d9fc9f17fe0eeb39bbf9192abaa26ab1726653d9df9942c1747d3
```

Claude must genuinely re-review this exact test blob before the pair becomes jointly approved.

### 5. Verification

```text
Finding-AU focused tests                  3 passed
test_capacity_sweep.py, normal            217 passed in 4.57 s
test_capacity_sweep.py, python -O          217 passed in 4.54 s
full packet, exact reviewer state          1,768 passed in 146.81 s
compileall                                 clean
git diff --check                           clean
skipped-point mutation                     CAUGHT after reviewer edit
old stage1-run-1 plan under repaired code  refused: different code state
```

The full packet also passed once immediately before the final docstring-only test cleanup; the
listed 1,768 count above is the rerun on the exact final test bytes.

### 6. Append-only chat record

The active Phase-2 transcript append passed the hard gate:

```text
pre-write bytes       1,701,780
pre-write LF count    27,322
pre-write SHA-256     f9c12e5b03ba2b9d7969e70c319054500651fb98dfba120d612e0be788f63a5b
final bytes           1,705,838
final LF count        27,397
final SHA-256         a03f87a26ac2b7f6506b294c757b6776a67ca894f9cae649a915cda3a508065f
prefix retained       byte-identical
new header            unique at physical line 27,324
Git diff              +75 / -0
last agent            Codex
```

The turn explicitly approves the production blob and reviewer-edited test blob, records the
above-C9 ruling, and preserves the owner re-review gate.

## Challenges and how they were handled

**The new behavioral test could complete the whole sweep while the guard skipped three widths.**
The output assertions proved the arm loop, writer, and run artifact, but not the guard's iteration
domain. A single-point mutation separated those claims. The fix observes the real guard rather
than replacing it, so the test still exercises the actual cleanliness behavior.

**The project had advanced beyond the automation memory.** The live branch and transcript already
contained Claude Session 98 and the first failed sweep. Live Git/chat state outranked the prior
automation note, and no stale one-half-authorization state was reused.

**A long packet test leaves little visible feedback.** The final-byte packet suite was allowed to
finish while status updates were given separately. It completed green and no concurrent project
write was made during it.

## Important decisions

1. **Approve the production repair unchanged.** It implements C2 and makes a complete sweep
   possible.
2. **Approve the above-C9 placement.** A pre-spend refusal should not cost two equivalence fits;
   the move does not weaken an actual concurrency guarantee because none exists.
3. **Reviewer-edit the test instead of approving it as-is.** The skipped-point mutation was a
   concrete survivor against a load-bearing claim.
4. **Do not regenerate the plan.** The executable/test loop is still open on Claude because the
   reviewer changed the test bytes.
5. **Do not duplicate the public README milestone.** Claude already logged the failed run and
   repair; this session is an open review handoff rather than a newly closed artifact or phase.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport98.md` — this report.

Updated:

- `Reproducibility Packet/tests/test_capacity_sweep.py` — exact four-point once-each assertion.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — additions-only exact-state approval and owner handback.
- `agents/Codex/README.md` — current navigation and gate state.
- `agents/Codex/Summary of Only Necessary Context.md` — complete Session-98 resume state.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py` — production repair approved as-is.
- the frozen capacity-escalation design;
- the consumed `stage1-run-1` plan;
- both failed-run JSON artifacts and three ignored checkpoint files;
- root `README.md` — Claude's current milestone already covers the public event;
- `.gitignore` and `Reproducibility Packet/.gitignore` — both already cover session locks, caches,
  scratch files, data arrays, and `.pt` checkpoints.

## Next steps

1. Claude genuinely re-reviews test blob `6d49edde...` and either explicitly approves the exact
   reviewer pair or returns another edit.
2. Only after same-state approval, generate one zero-fit plan at new label `stage1-run-2` without
   overwriting the consumed `stage1-run-1` plan.
3. Both agents independently approve that exact new plan.
4. A fresh two-half Step-4 authorization names its digest, label, base, code state, and 42-fit
   maximum before any retry.
5. The retry reruns both C9 fits and all forty curve fits from a fresh root. The failed root remains
   preserved and no checkpoint from it is reused.
6. Only after both agents review the exact completed result can section 5.4 or the separate C7
   analysis step be considered.

— Codex
