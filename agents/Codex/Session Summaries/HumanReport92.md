# Codex — Human Report, Session 92

**Date and time:** 2026-08-07 18:25 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains
**278**.

**Fits against delivered data: 0. Checkpoint writes: 0. Packet plan artifacts: 0. Data
generated: 0. Pilot / validation / test reads: 0.**

**Progress-report session:** no. The next regular Codex progress report is Session 96; no phase
transition and no Claim-Sheet amendment occurred.

---

## Summary

Claude Session 92 built the Route-A Gate-4 capacity-sweep executable and tests authorized by the
jointly frozen v0.1 design. Claude first handed over one state, correctly withdrew it after
discovering that its mutation harness could not report survivors, repaired five measured gaps,
and explicitly approved a corrected pair:

```text
capacity_sweep.py       blob 9f2cc0ab...
test_capacity_sweep.py  blob d8a8c86c...
```

I did not approve that pair unchanged. The corrected 36-case mutation set exercised local
guards, but it did not cross the run-level persistence and exact-identity seams those guards
feed. I reproduced two failures immediately: C10 accepted a complete-looking arm list in which
one required arm had been replaced by a duplicate, and a sibling refusal file's UUID name did
not match the `attempt_uuid` persisted inside it. The source audit found four adjacent contract
violations: C9 failures discarded partial arm state and under-reported spent fits/checkpoints;
post-claim terminals omitted all downstream `UNATTEMPTED` arms; the deterministic plan omitted
the fit-ledger and analysis-artifact digests plus two terminal result names; and C9 loaded a
same-name approved checkpoint without authenticating its actual bytes against the ledger digest.

I reviewer-edited the executable and tests, added direct regressions for every finding, and
explicitly approved this new exact state:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 9059bccbd54c1d13a1d8ed927aa4e8a2c3628e58
  canonical/raw SHA-256    c3c1b3dcd2082e7f14ce513dd696e40e5cbb7d6062e6b1083987481245629b09
  physical state           91,161 B / 2,153 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 42e22a70442b244994bbcbdd804ab51304524608
  canonical/raw SHA-256    aa250c9bfa2c47d06c2dfcc69da1a27af4e5ad6b7f6f415a34b1a263c8e78d48
  physical state           73,130 B / 1,805 lines / LF / no BOM / 199 tests

Reviewer delta from Claude's corrected handoff
  module +476 / -144; tests +249 / -5
```

The frozen design remains byte-identical at blob `b45efa477de10331ca61e1af73b2834b22df3fb6`
and canonical/raw SHA-256
`05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002`.

The executable review loop remains **open** pending Claude's genuine same-state owner re-review
of the two reviewer blobs. Plan mode remains unauthorized in project state; tests exercised
plan code paths only under temporary directories. No root public milestone was added because no
artifact loop closed.

## What was accomplished

### 1. Reconciled stale automation context with the live repository

The saved automation memory ended at Codex Session 86. The synchronized repository was already
at Claude Session 92, with `HEAD == origin/main == 267ea3d` when this session started. I followed
the lock gate first, read `AgentPrompt.md`, the complete project details, Codex continuity, all
Codex-including chat summaries, the Transcript Order Monitoring thread, and the current physical
tail of the 1.58 MB Phase-2 transcript. Live state established that the frozen capacity design
was closed and the only open technical loop was Claude's exact executable/test handoff.

### 2. Distinguished the corrected handoff from the withdrawn one

Claude's first Session-92 turn named module blob `e041d0f0` and test blob `ab01e2c6`, then
appended two corrections. The authoritative final owner state was `9f2cc0ab` / `d8a8c86c`.
I reviewed only that final pair. I preserved the withdrawn state as history and did not infer
approval from its supersession, its tests, or the owner handoff.

### 3. Reproduced the exact-identity and refusal-identity failures

Before editing, I drove two small adversarial checks against the handed-over bytes:

```text
C10_DUPLICATE_ACCEPTED
REFUSAL_UUID_MATCH False
```

The first replaced one required completed curve arm with a duplicate of another while retaining
the required count of forty. `require_complete_sweep` passed because it counted statuses rather
than comparing the actual `(channels, suite, seed)` set. The second constructed one refusal
document with a fixed `attempt_uuid` and wrote it through the sibling sink. The filename used a
second independently drawn UUID, contradicting the design's `<attempt_uuid>.json` identity.

After repair, the same probes returned:

```text
C10_DUPLICATE_REFUSED
REFUSAL_UUID_BOUND
```

### 4. Preserved partial C9 evidence and accurate accounting

The handed-over `equivalence_gate` accumulated its two arm records in a local list, wrote the
equivalence artifact only after both arms passed, and raised a plain exception on any failure.
Execute mode therefore received none of the partial state. If C1/seed 0 passed and S/seed 4
failed, the run-level terminal recorded an empty C9 list and zero fits/checkpoints even though
two fits and two checkpoint files existed. A first-arm post-fit mismatch similarly spent and
wrote one while reporting zero.

The repaired gate builds both C9 arm identities before work begins, records a refusal or pass in
place, persists the partial equivalence artifact, and raises an `EquivalenceFailure` carrying
the exact document. Execute mode imports those records and the real `fits_attempted` /
`checkpoints_written` counts before writing its run terminal. Aggregate counts remain present,
but are now also separated into equivalence and curve fits/checkpoints as section 7.2 requires.

A cross-function regression drives a first-arm pass followed by a second-arm loss-history
failure and verifies:

- two exact C9 identities remain present;
- the first is `COMPLETED/PASS` and the second `COMPLETED/FAIL`;
- two fits and two checkpoints are recorded;
- the failed equivalence artifact is physically persisted; and
- the run-level terminal imports the same state rather than reconstructing it.

### 5. Made every post-claim terminal structurally complete

The handed-over run list started with the ten reused anchors and appended new arms only when
execution reached them. A data refusal before C9 omitted all forty future curve arms and both
C9 arms. A refusal partway through the sweep omitted every later curve arm. That violates the
design's requirement that every curve and equivalence arm carry exactly one status.

Execute mode now begins with all fifty curve identities and both C9 identities:

```text
10 anchors + 40 new curve arms  -> UNATTEMPTED initially
2 C9 arms                       -> UNATTEMPTED / NOT_RUN initially
```

Records are replaced in place as anchors are reused, fits complete, or an arm refuses. The
terminal artifact therefore preserves downstream non-actions explicitly. The integration test
for a C9 refusal checks exactly ten `REUSED`, forty `UNATTEMPTED`, and both C9 states.

### 6. Repaired C10 from a count gate into an identity gate

C10 now compares unique exact sets:

```text
set(anchor identities in REUSED state)    == set(anchor_arms())
set(curve identities in COMPLETED state)  == set(curve_arms())
set(C9 identities)                        == set(EQUIVALENCE_ARMS)
```

It separately requires both C9 comparisons to be `PASS`. Duplicate replacement is refused for
all three families. Malformed or unhashable JSON identities now become named contract refusals
rather than escaping as Python `TypeError`s.

### 7. Completed the deterministic plan's provenance surface

Section 7.1 requires the plan to bind the approved fit ledger, approved analysis artifact, and
exact result names. The handed-over plan contained values extracted from the two approved JSON
files, but not their own canonical digests. An unused-field edit could therefore leave the plan
unchanged. It also named the logical namespace and checkpoints but omitted the exact run-result
and equivalence-artifact filenames.

The plan now carries:

```text
approved_fit_ledger_sha256
approved_analysis_sha256
run_artifact_relative_name
equivalence_artifact_relative_name
```

`require_authorized_plan` already rebuilds the complete expected plan and compares it by
equality, so adding these fields extends the existing gate without a second validation path.

### 8. Bound checkpoint bytes and per-arm fitting identity

The handed-over C9 path copied `checkpoint_sha256` from the approved ledger but did not hash the
actual file before loading it. A replaced file at the approved name could therefore be compared
while the artifact claimed the ledger's old digest. The repaired gate reads the bytes once,
hashes them, refuses before fitting on a mismatch, and passes those same authenticated bytes to
`torch.load`. A direct regression confirms a digest mismatch spends zero fits and writes zero
checkpoints.

Reused anchors now carry the historical eight-entry fitting identity from the approved ledger;
C9 and new curve arms carry the nine-entry Route-A identity. This makes section 5.2's per-arm
provenance literal rather than relying only on a run-level dictionary.

### 9. Hardened post-fit persistence failures

The reviewer state also catches checkpoint serialization/write errors and completed-record
construction errors after a curve fit. A terminal remains accurate if a fit completed but its
checkpoint or result record could not be persisted. The checkpoint count advances only after a
successful write, while the fit count advances before the fit call.

The module docstring was narrowed so it no longer says `X_FORBIDDEN_BASE` is the only
artifact-free exit without qualification. It is the only artifact-free refusal **after a
destination is supplied**. Missing `--output-dir` / `--base-dir` values are pre-destination CLI
refusals with nowhere authorized to write, matching section 7.2's explicit boundary.

### 10. Preserved the no-execution and evidence boundaries

No delivered `.npz` payload, manifest row, approved checkpoint, pilot row, validation row or
test row was read. The approved fit ledger and in-sample analysis JSON were read by deterministic
plan-construction tests, which was already true in Claude's 189-test state. Synthetic C9
checkpoints and plan artifacts were written only beneath pytest temporary directories.

No packet `capacity_sweep_plan.json`, `capacity_sweep_equivalence.json` or
`capacity_sweep_result.json` exists. `Reproducibility Packet/config/config.json` remains absent.
The lifetime physical-rollout total remains 278.

## Verification

All verification below applies to the exact approved reviewer blobs:

```text
focused Route-A suite                199 passed in 3.26 s
focused suite under python -O        199 passed in 3.37 s
                                      expected pytest optimization warning only
full packet suite                  1,750 passed in 131.34 s
compileall                           clean
git diff --check                     clean
hard-coded local paths               none in module or tests
production assert statements         none in capacity_sweep.py
```

The 36/36 mutation result Claude reported belongs to its superseded corrected handoff. I did
not extend that count to the reviewer-edited bytes without rerunning Claude's external harness.
Instead, I added direct deterministic regressions for the six findings, including the C9-to-run
cross-function seam that the textual mutation set did not cover.

The frozen design remained unchanged:

```text
capacity-escalation-v0.1.md
  blob                 b45efa477de10331ca61e1af73b2834b22df3fb6
  canonical/raw SHA    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
  bytes / lines        72,630 / 1,084
```

## Transcript integrity

The Phase-2 review response used the append-only hard gate:

```text
pre-write bytes          1,583,094
pre-write lines          25,279
pre-write SHA-256        45727ad60b0564a53bdba64d8323a1b6f3765bf7aef6e06e26a777887e885c40
final bytes              1,590,311
final lines              25,404
Codex header line        25,281; exactly once and after the boundary
old prefix               byte-identical under the pre-write SHA-256
Git diff                 +125 / -0
UTF-8 replacement chars  0
physical tail            Codex, followed by the separator
```

No append-order recurrence occurred, so the Transcript Order Monitoring thread was left
unchanged.

## Challenges and how they were handled

- **The saved automation note was six Codex sessions stale.** I treated it as orientation only
  and used live Git, continuity and physical transcript state as authoritative.
- **Claude had three Session-92 turns and two superseded byte pairs.** I followed physical order
  and reviewed only the last explicitly approved pair.
- **The corrected mutation result looked strong.** I did not treat 36/36 as exhaustive. I walked
  the consumers of each guard—the equivalence exception boundary, terminal artifact builder,
  plan identity and analysis backstop—and found the untested cross-function failures.
- **A repair to failure accounting can itself become a second source of truth.** The code carries
  the partial C9 document through the exception instead of reconstructing counts from filesystem
  side effects, and initializes exact identity sets once rather than appending guesses.
- **The transcript is large and append-only.** I used an exact unique UTF-8 EOF block, retained
  the byte-identical old prefix, and completed all placement assertions before closeout work.

## Important decisions and reasoning

1. **Block the owner pair and repair directly.** The failures were executable and localized;
   the review-cycle playbook authorizes reviewer edits followed by an explicit approval and
   owner re-review.
2. **Treat identity as more than cardinality.** A complete scientific sweep is a fixed set of
   named arms, not merely fifty rows with acceptable status words.
3. **Count attempted work where it is attempted.** A failed comparison cannot retroactively
   erase a fit or checkpoint already spent.
4. **Authenticate before comparison.** A ledger digest is provenance only if the bytes loaded
   are checked against it before fitting begins.
5. **Keep the public log lean.** This session returned an edited state and did not close the
   artifact loop, so the root Live-Run README received no new milestone.
6. **Preserve authorization sequencing.** Executable approval is not plan authorization; plan
   approval is not fit authorization.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport92.md`

Updated:

- `Reproducibility Packet/scripts/utils/capacity_sweep.py`
- `Reproducibility Packet/tests/test_capacity_sweep.py`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

Reviewed and deliberately unchanged:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`
- every approved result JSON and checkpoint
- `README.md` and `Reproducibility Packet/README.md`
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
- `.gitignore` and `Reproducibility Packet/.gitignore`

The ignore files already cover `.agent-session.lock`, bytecode/caches, temporary directories and
future `.pt` checkpoints; no ignore change was needed.

## Exact next steps

1. Claude genuinely re-opens and owner-reviews module blob `9059bccb...` and test blob
   `42e22a70...`.
2. If Claude accepts both unchanged, it explicitly approves those exact states and closes the
   executable review loop.
3. Only then may one deterministic zero-fit plan be created and reviewed as its own artifact.
4. The two C9 equivalence fits and forty curve fits require a later separate joint
   authorization naming the approved plan digest.
5. C7 analysis, pilot/validation/test reads, thresholds, capacity selection, Stage 2, final
   `config/config.json`, generation, confirmatory work and all rollouts remain blocked.

— Codex
