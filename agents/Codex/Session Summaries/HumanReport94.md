# Codex — Human Report, Session 94

**Date and time:** 2026-08-08 02:14 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Data generated: 0. Observation-payload reads: 0. Approved-checkpoint reads: 0. Pilot / validation / test reads: 0.** One official zero-fit plan artifact was created after the executable review loop closed.

**Progress-report session:** no. The next regular Codex progress report is Session 96; no phase transition or Claim-Sheet amendment occurred.

---

## Summary

Claude Session 94 genuinely owner-reviewed my Session-93 destination-binding repair, accepted
it, and returned a new capacity-sweep executable/test pair after finding one further
low-severity coverage seam: the per-capacity cleanliness guard and checkpoint writer each
built the same directory name independently. I reopened both files in full, independently
confirmed the prior state had two producers, drove the new binding, and accepted Claude's
single-definition repair and its exact-name test. Both agents now explicitly approve the same
Route-A executable/test blobs, closing Step 2 after 204 focused tests and all 1,755 packet
tests passed. I then ran the newly open Step 3 exactly once in plan mode. It wrote one
canonical zero-fit plan for `stage1-run-1`; I independently audited its arm census, paths,
budgets, code identities and bound document digests and explicitly owner-approved its exact
bytes. Claude's independent plan read is now the only open immediate gate. No C9 or curve fit,
checkpoint, observation payload, approved checkpoint, generation, rollout or later-role
outcome was read or produced.

---

## Exact-state executable review

### Claude's returned state

Claude explicitly approved and handed back:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 937ab73c960ac4d5e6ffcbcd1c869f071c47a8b5
  canonical/raw SHA-256    9ceb1298bad4247086d42d9fd08a01e1460647af91603a3391e5f4347fbfe489
  physical state           95,248 B / 2,222 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 0a8f8b71fccae95d9e0648bc45bea14902d9cb14
  canonical/raw SHA-256    dbee9c98e786a5cd2a5adaf189b3b56d95a76bf5710d31011dc33581a6535a19
  physical state           82,127 B / 2,019 lines / LF / no BOM / 204 tests
```

Claude also independently reproduced my Session-93 AR finding and accepted its one-line
resolved-destination repair. I accepted that owner re-review.

### AS — one capacity-point directory definition

Before Claude's repair, the per-point guard and the checkpoint writer each formatted
`channels_{channels:03d}` independently. The two current copies agreed, so this was not a
live behavior failure. The guard is also unreachable on the ordinary path because execute
mode atomically claims an absent run root. Claude correctly described AS as a coverage defect
over defence in depth rather than inflating its severity.

The equality was nevertheless unbound. My independent AST probe against my Session-93 source
found exactly two `channels_...` f-string producers. Claude's state extracts:

```python
def capacity_point_directory(channels: int) -> str:
    require_capacity_point(channels)
    return f"channels_{channels:03d}"
```

Both `_execute_mode`'s cleanliness guard and `checkpoint_relative_name` now consume this one
definition. The complete checkpoint names are behaviorally unchanged for all forty new arms.

Claude's decision to repair a low-severity coverage gap before planning was sound. The next
plan binds this module's digest and every expected checkpoint name. Deferring the repair one
gate would turn a small single-definition change into an invalidated plan artifact and review.
The new test deliberately pins the current directory spelling because design section 7.1
makes those names contract-visible; changing one is not a behavior-free refactor.

### Approval decision

I explicitly approved both exact Claude Session-94 blobs unchanged. Claude had already
approved the same bytes, so the Route-A executable/test review loop is now closed. Every
earlier pair is superseded.

One bookkeeping correction was propagated forward in the live transcript: Claude's
`HumanReport94.md` calls its Session-94 pass round three, while its exact transcript turn calls
it round four. The count did not decide closure. The current-byte review found no broken
behavior; AS was an accurately scoped coverage repair and was implemented correctly.

---

## Executable verification

```text
prior-state AST probe                 2 independent channels_ f-string producers
targeted AS regression                1 passed in 1.36 s
focused Route-A tests               204 passed in 3.70 s
focused tests under python -O       204 passed in 3.54 s
full packet suite                 1,755 passed in 125.98 s
fits / checkpoint writes             0 / 0
packet plan artifacts before Step 3  0
generation / rollouts                0 / 0
config/config.json                 absent
```

The focused and full suites read the approved tracked `dev_fit_result.json` and
`dev_fit_analysis.json` as development comparability and plan metadata. They read no delivered
observation payload and no approved `.pt` checkpoint bytes. No fit or plan run occurred during
the executable review itself.

The frozen design remained unchanged:

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob                 b45efa477de10331ca61e1af73b2834b22df3fb6
  canonical/raw SHA-256    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
```

---

## Official zero-fit plan

With Step 2 closed, design section 12 opened the separate Step-3 planning act. From the packet
directory I ran:

```text
..\venv\Scripts\python.exe -B -m utils.capacity_sweep --mode plan \
  --run-label stage1-run-1 --output-dir results\capacity_sweep
```

The executable returned:

```text
X_PLAN_OK: 40 new arms + 2 equivalence arms planned at run label stage1-run-1,
0 fits run
```

The exact artifact is:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 d2584d28f8ecc1d82d24d4480cee9ff7481611a9
  canonical/raw SHA-256    740d5db96657c7a5e9a86b49816daf091439e7661a6bd971fb8ce6ab3ae1c00e
  physical state           13,786 B / one canonical JSON record / no BOM /
                           no CRLF / no terminal newline
```

I explicitly approve this exact plan. Claude must independently review and explicitly approve
the same blob before Step 3 closes. Creation, the executable's `X_PLAN_OK`, my audit, and a
handoff are not Claude approval.

### Independent plan audit

I parsed the persisted JSON directly and reconstructed its census without calling the plan
producer:

```text
read-only anchors                  10 = 32 channels x C1/S x seeds 0..4
new curve arms                     40 = 16/24/40/48 x C1/S x seeds 0..4
C9 equivalence arms                 2 = (C1, 0), (S, 4)
distinct declared output paths     44 = 40 curve + 2 C9 + C9 artifact + run artifact
code identities                     9 = eight approved historical + capacity_sweep.py
maximum budget                42 fits / 42 checkpoints / 0 rollouts /
                              0 generations / 0 non-dev reads
```

The forty new identities equal the full declared cross-product and contain no duplicate or
32-channel fit. Every output name is below
`results/capacity_sweep/stage1-run-1/`; no host path, parent traversal or UNC spelling is
serialized. The two equivalence target digests match their corresponding read-only anchors.

A separate read-only identity audit recomputed all nine code digests plus the frozen design,
approved fit-ledger and approved analysis digests from the tracked files. Every value matches
the plan. The raw artifact equals strict sorted canonical JSON byte for byte.

### Resource boundary after planning

```text
fits / checkpoint writes        0 / 0
official plan artifacts         1
result / equivalence artifacts  0 / 0
observation payload reads       0
approved checkpoint reads       0
pilot / validation / test reads 0 / 0 / 0
generation / rollouts           0 / 0
lifetime Protocol-P rollouts    278 unchanged
config/config.json              absent
```

---

## Public status

Closing the executable loop is a finished artifact and producing the official zero-fit plan is
a noteworthy public milestone. I advanced the root README banner to 2026-08-08 and appended one
lean entry. It records the repeated guard/writer destination-binding pattern, exact executable
closure, 1,755-test packet verification, the plan's 10/40/2 structure, and the open second-read
gate. It does not imply fit authorization or a scientific result.

The Reproducibility Packet README remains unchanged. Step 3 is still under exact-artifact
review, so adding fit/run instructions would widen the public runnable surface before the plan
is jointly approved.

---

## Transcript hard gate

The active Phase-2 transcript received two append-only Codex turns.

First append — exact executable approval:

```text
pre-write bytes          1,619,145
pre-write lines          25,918
pre-write SHA-256        25a8926b0ced660810703e31d8ffc86b7e15e4d9ea167db0400aa86024865d14
post-write bytes         1,623,151
post-write lines         25,998
Codex header line        25,920; unique and after the boundary
post-write SHA-256       fa2f8e505b81a9e6463094771fc3157e0c15d3d3cf34a193a42452e3cde43070
```

Second append — exact plan handoff:

```text
pre-write bytes          1,623,151
pre-write lines          25,998
pre-write SHA-256        fa2f8e505b81a9e6463094771fc3157e0c15d3d3cf34a193a42452e3cde43070
final bytes              1,626,311
final lines              26,076
Codex header line        26,000; unique and after the boundary
final SHA-256            f2781d5999cb24a255c6663d0fc03816669517c778820de05fc0aa21743581c7
cumulative diff          +158 / -0
last agent               Codex
```

Both prior byte prefixes remain exact. No monitoring-thread note was warranted because no
append-order or prefix recurrence occurred.

---

## Decisions

1. **AS accepted unchanged.** It is low-severity coverage, accurately disclosed, and the
   single-definition implementation closes the exact guard/writer equality before planning.
2. **Executable loop closed on exact bytes.** Both agents explicitly approve blobs
   `937ab73c...` and `0a8f8b71...`.
3. **Step 3 run exactly once.** The plan invocation consumed zero fits and created only the
   canonical plan artifact.
4. **Plan owner-approved, second read open.** Codex approves blob `d2584d28...`; Claude approval
   is still required.
5. **No implicit Step-4 authorization.** Joint plan approval would close Step 3 only. The two
   C9 and forty curve fits remain a separate later authorization naming the exact plan digest.
6. **Public update warranted.** The finished executable plus real zero-fit plan clears the
   live-log milestone bar; no packet runbook expansion is yet warranted.

---

## Files created or updated

Created:

- `Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json` — official zero-fit
  Step-3 plan, owner-approved by Codex and awaiting Claude's exact-state review.
- `agents/Codex/Session Summaries/HumanReport94.md` — this report.

Updated:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only executable approval and plan handoff.
- `README.md` — banner date and one lean executable/plan milestone.
- `agents/Codex/README.md` — Session-94 navigation and current exact-state pointers.
- `agents/Codex/Summary of Only Necessary Context.md` — fully rewritten Session-94 resume
  state.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py`
- `Reproducibility Packet/tests/test_capacity_sweep.py`
- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`
- `Reproducibility Packet/README.md`
- `.gitattributes`, `.gitignore` and `Reproducibility Packet/.gitignore`

---

## Cross-review

I read Claude's `HumanReport94.md`, its full Session-94 transcript turn, and both returned
files. The report accurately describes AR, AS, the low severity of AS, the zero-execution
boundary and the exact handed-back identities. Its only correction is the round-count
inconsistency described above; I propagated that forward without editing the historical
report. No substantive correction remains open in Claude's work.

---

## Next steps

1. Claude independently reviews and explicitly approve/blocks exact plan blob
   `d2584d28f8ecc1d82d24d4480cee9ff7481611a9` / SHA-256 `740d5db9...`.
2. If Claude approves the same bytes, Step 3 closes. That closure still does not itself spend
   any fit.
3. Step 4 requires a separate joint authorization naming this plan digest before either C9 fit
   or any of the forty curve fits may run.
4. The C7 read-only analysis build, every later-role outcome read, Stage 2, final config,
   generation and all rollouts remain separately blocked.

— Codex
