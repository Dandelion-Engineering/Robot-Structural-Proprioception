# Codex Human Report - Session 100

**Date and time:** 2026-08-09 02:25 PDT

**Phase:** Phase 2 - Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains
**278**. Fits are not rollouts.

**Fits against the delivered development dataset:** 42: two C9 equivalence fits plus forty
capacity-curve fits. **Checkpoint writes:** 42. **Data generation:** 0. **Pilot / validation /
test outcome reads:** 0. The executable read 304 authorized development rows, C1 152 and S 152.

**Progress-report session:** no. The next regular Codex progress report is Session 104 unless a
phase transition or approved Claim Sheet amendment fires sooner.

---

## Summary

Claude Session 100 independently audited and explicitly approved the exact replacement plan that
Codex published in Session 99. That closed the zero-fit plan-review gate on Git blob
`d7104e55b4fb9be3fbfa6bd685b002a055409673`, SHA-256
`ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31`. Claude then issued one
fresh Step-4 execution-authorization half naming that plan, `stage1-run-2`, the exact executable,
the base and data roots, the ten anchors and a 42-fit/42-checkpoint ceiling.

I independently re-opened every named input rather than accepting the handoff. The plan, frozen
design, executable, tests, delivered manifest, three role indexes and ten physical anchor files all
matched. The ordered ten-anchor digest aggregate was
`a37b2f769a150e562132cc3111c392ba6e3e8c92f04765508bc1322c9e9908c6`; the retry root and its
label-specific refusal sink were absent; `config/config.json` was absent; the branch matched
`origin/main`; and no Python process was active. I recorded Codex's separate authorization half
under the append-only hard gate. Only after both halves were physically present did I run one
execute-mode invocation.

The retry completed successfully in 441.5 seconds of shell wall time, with the artifact recording
439.594 seconds:

```text
X_SWEEP_OK
42 fits attempted / 42 checkpoints written
2 equivalence arms COMPLETED / PASS
40 new curve arms COMPLETED
10 approved 32-channel anchors REUSED
0 refused / 0 unattempted
0 rollouts / 0 generation / 0 non-development reads
```

I then audited the exact terminal state mechanically. The main result and C9 equivalence artifact
are canonical compact JSON, bind the exact approved plan/code/design, contain the complete expected
arm sets and counts, and point to exactly the 42 checkpoint files present under the claimed run
root. Every recorded checkpoint digest matches its file. Both C9 outputs are bit-identical to their
approved anchors. The protected project digest domain and delivered-data stat domain were identical
before and after the run.

I explicitly approved both exact JSON artifacts and handed them to Claude for the independent
section-12 step-5 review. This is one approval, not a joint result. I did not run C7, compute the
section-5 descriptive read, apply section 5.4, choose a capacity, read a later role, change a
threshold, authorize Stage 2 or create the final configuration.

## What was accomplished

### 1. Reconciled the live gate state

- Read Claude's Session-100 report, continuity and exact transcript turns rather than relying on
  the automation memory, which ended at Codex Session 94.
- Confirmed Claude explicitly approved the same replacement plan bytes Codex approved in Session
  99; creation or downstream use was not substituted for same-state approval.
- Read the frozen capacity design's sequencing contract plus the review-cycle and reproducibility
  packet playbooks before acting.
- Preserved the separation between plan approval, execution authorization, execution, exact-state
  result review, C7 and section-5.4 interpretation.

### 2. Independently verified the execution preconditions

The final pre-command state was:

```text
branch / remote                         clean before transcript append; HEAD == origin/main
only change before execution            Codex's additions-only authorization turn
approved plan                           blob d7104e55... / SHA-256 ffb00965...b7cb31
frozen design                           SHA-256 05109d97...c15e002; matched plan binding
approved executable                     blob 53e5dcb7... / SHA-256 be07d95e...f641fa
approved tests                          blob 6d49edde... / SHA-256 640f23b5...747d3
manifest / three role indexes           all raw hashes matched the plan
ten anchor files                        all matched the plan
ordered anchor digest aggregate         a37b2f76...e9908c6
packet checkpoint files                 13 before execution
stage1-run-2 execution root             absent
label-specific refusal sink             absent
config/config.json                      absent
Python processes                        0
```

The external pre-run bracket recorded:

```text
protected project domain        492 files / b8d69f60...293313a
delivered-data stat domain      2,839 files / 4affb0ff...aa0ab
```

The project digest domain excluded `.git`, `venv`, caches, `tmp`, the 3.86 GB data root and the
future claimed run root. The data root was independently bracketed by relative path, byte size and
UTC modification ticks. This preserves Claude's stated limitation: a content change that preserved
both size and mtime would not be detected in the data stat domain.

### 3. Issued the second authorization half and ran once

Codex's transcript turn names:

```text
plan          ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
run label     stage1-run-2
base          Reproducibility Packet/results/capacity_sweep
data root     data/gate3-base-dev-pilot-val-c1-s
executable    blob 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
budget        42 fits / 42 checkpoints / 0 generation / 0 rollouts / 0 non-dev reads
```

The one authorized command ran from `Reproducibility Packet/scripts/` with the project virtual
environment and the exact approved plan path/digest. It returned:

```text
X_SWEEP_OK: 40 new arms fitted, 10 anchors reused, 2 equivalence checks passed, 0 rollouts spent
```

No retry, second plan write, second execute invocation or downstream analyzer ran.

### 4. Audited the exact terminal state

The persisted artifacts are:

```text
Reproducibility Packet/results/capacity_sweep/stage1-run-2/capacity_sweep_result.json
  Git blob                 110d3e4eb3df3795d2873ab6f30450f48d8f4e1f
  raw/canonical SHA-256    0d8a1c2de7208cc9a551d75ce44e3a64f02de6c9881b4b31f4df4d07cc7f7a2a
  size                     85,079 bytes

.../stage1-run-2/_equivalence/capacity_sweep_equivalence.json
  Git blob                 26eb475e926e2ab23bc69e6e840c965553f1765b
  raw/canonical SHA-256    605b35fdc02276a434ce2f6c107769f6670a9da446fe1e2909fe88e744feb3a4
  size                     3,354 bytes
```

Independent checks established:

- canonical compact JSON with no CR, BOM or final newline;
- exact approved plan, design and nine-code-identity bindings;
- exactly forty completed new arms at `{16,24,40,48} x {C1,S} x seeds 0-4`;
- exactly ten reused 32-channel anchors;
- exactly two completed/PASS C9 arms;
- every plan-relative and run-root-relative checkpoint name resolves to the same file;
- every checkpoint digest, parameter count and receptive field matches its record;
- twenty loss-history values and 152 examples for each new arm;
- exactly 42 declared checkpoint files under the run root, all with distinct digests;
- 304 authorized development rows and zero later-role reads; and
- zero rollouts and zero generation.

After the run, both external bracket aggregates were byte-for-byte identical to their pre-run
values. The plan, executable, anchors and delivered data remained unchanged. No refusal artifact or
Python process remained. `config/config.json` remained absent.

### 5. Verified the completed tree

```text
test_capacity_sweep.py, normal       217 passed in 3.75 s
test_capacity_sweep.py, python -O    217 passed in 4.06 s; expected warning
full packet                          1,768 passed in 123.74 s
exact-state audit                    RESULT_EXACT_STATE_OK
git diff --check                     deferred to final staged verification
```

The tests were run only after the execution process terminated. They changed no tracked code or
evidence and generated no bytecode because `PYTHONDONTWRITEBYTECODE=1` and `-B` were set.

### 6. Preserved the review boundary and public state

- Appended Codex's authorization and exact-state result approval as two physical-EOF-verified,
  additions-only turns.
- Added one lean public README milestone: the development sweep completed, one exact-state review
  exists, the second is open, and there is no interpretation or downstream authorization.
- Did not update the public banner or claim a research result.
- Did not write a Session-100 progress report because no cadence, phase-transition or approved-
  amendment trigger fired.

## Transcript integrity

Authorization append:

```text
pre-write bytes          1,734,735
pre-write SHA-256        f30d6872...0483f8
prior prefix retained    exact
new header count         1
new header line          27,840
Git diff after append    +50 / -0
```

Execution-record append:

```text
pre-write bytes          1,737,553
pre-write SHA-256        ab84f95e...4948e6
prior prefix retained    exact
new header count         1
new header line          27,890
cumulative Git diff      +123 / -0
physical last speaker    Codex
```

Both headers used freshly measured append-time clock values. No Transcript Order Monitoring entry
was needed.

## Challenges and how they were handled

### Automation memory was stale

The automation memory ended at Codex Session 94, while the live branch was at Claude Session 100.
I treated the live transcript, reports, continuity and Git tree as authoritative and rebuilt the
gate state from them.

### Two preflight expectations came from abbreviated notes

My first audit expanded the frozen-design digest from an abbreviated display incorrectly and looked
for the delivered data beneath the packet rather than at project-root `data/`. Both mismatches were
in the read-only probe. I replaced the guessed design digest with the plan's exact binding, located
the authorized root from the live tree and executable interface, and reran the whole preflight.

### Three post-run probe defects were caught before approval

One PowerShell parser expression was invalid, one checkpoint object was passed as a display name
instead of a full path, and the first Python audit compared the plan's packet-relative checkpoint
names directly to the result's run-root-relative names. Each probe stopped without writing. I fixed
the probes, made the path projection explicit, added labeled assertions and reran to
`RESULT_EXACT_STATE_OK`. No artifact was changed to satisfy the audit.

### The run produced no streaming terminal output

The executable buffered its fit messages until completion. I left the single process undisturbed,
reported status approximately every fifty seconds and waited for the persisted terminal state.

## Important decisions

1. **Issue the second half only after independent physical verification.** Claude's audit and half
   were necessary inputs, not substitutes for Codex's own measurement of the named bytes.
2. **Run only after both halves were physically recorded.** The same session could be the runner
   because it saw both halves at the transcript tail and rechecked the state immediately before the
   command.
3. **Approve the terminal record without interpreting it.** The result artifact is mechanically
   complete and faithfully persisted. That does not make its numbers a jointly reviewed capacity
   finding and does not authorize C7 or section 5.4.
4. **Keep checkpoint portability explicit.** The packet now contains 55 ignored `.pt` files: ten
   approved anchors, three failed-run files and 42 retry files. A clean-machine authenticated
   recovery path remains a Phase-3 binary obligation.
5. **Keep the public update milestone-sized.** The honest public event is completion of one bounded
   development measurement whose exact state is still under cross-review.

## Files created or updated

- `Reproducibility Packet/results/capacity_sweep/stage1-run-2/capacity_sweep_result.json`
  - new tracked terminal result proposed for exact-state review.
- `Reproducibility Packet/results/capacity_sweep/stage1-run-2/_equivalence/capacity_sweep_equivalence.json`
  - new tracked C9 equivalence record proposed for exact-state review.
- `Reproducibility Packet/results/capacity_sweep/stage1-run-2/**/*.pt`
  - 42 new local, Git-ignored checkpoint files; required to verify and later reproduce the tracked
    terminal record.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  - additions-only Codex authorization and exact-state review handoff.
- `README.md`
  - one lean public completion/review-pending milestone; no banner change.
- `agents/Codex/Session Summaries/HumanReport100.md`
  - this report.
- `agents/Codex/README.md`
  - workspace index and current exact-result review gate.
- `agents/Codex/Summary of Only Necessary Context.md`
  - completely rewritten resume state.

No source, test, frozen protocol, approved/consumed plan, failed-run artifact, delivered data,
threshold or configuration file was modified.

## Next steps

1. Claude independently re-opens and reviews exact result blob `110d3e4e...` / SHA-256
   `0d8a1c2d...7f7a2a` and equivalence blob `26eb475e...` / SHA-256
   `605b35fd...feb3a4`, then explicitly approves the same bytes or returns a correction.
2. Until that approval exists, do not run C7, compute the section-5 descriptive read, apply section
   5.4, select capacity, authorize Stage 2 or read any later role.
3. After exact-state review closes, treat C7 construction/review/execution and the joint section-
   5.4 interpretation as separate gates; do not infer either from the completed sweep.
4. Preserve the consumed plan, failed `stage1-run-1` root, completed `stage1-run-2` root, all 55
   checkpoint files and absent final `config/config.json`.

**Next Codex session number:** 101.
