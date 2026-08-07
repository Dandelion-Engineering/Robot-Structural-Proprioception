# Codex — Human Report, Session 90

**Date and time:** 2026-08-07 10:13 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains
**278**.

**Fits: 0. Checkpoint writes: 0. Data generated: 0. Pilot / validation / test reads: 0.**

**Progress-report session:** no. The next regular Codex progress report is Session 96; no phase
transition and no approved Claim-Sheet amendment occurred.

---

## Summary

This was the same-state reviewer re-review requested by Claude Session 90. I genuinely reopened
the full returned capacity-escalation design at Git blob
`b2f650e19a1187360621c60be7f91d544ad9ea40`, reviewed its complete delta from my Session-89
state, and checked the affected claims against the approved trainer source.

Claude's AF diagnosis is correct: binding execute mode to `<base>/<run_label>/` is a useful
local mechanism that a free operator-selected run root was not. It preserves deterministic
plan bytes, makes conforming same-base retries use a different label/root, and leaves the
unpreventable different-base/copied-workspace replay residual explicit.

The returned state still had one executable contradiction below that repair. It refused only
an existing **non-empty** root, which admits empty-root reuse and a check-then-create race. It
also required every refusal to persist while naming no place where the occupied-root refusal
could be written without traversing or changing the resource whose occupancy triggered it.

I corrected those seams and explicitly approve the reviewer-edited design at:

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob               b359ba0b189a168207f3a15d37e7ba1153bbd326
  canonical/raw SHA-256  825afdfd18cc594ccc9055b470e1e80123f2e133049801aa5d9b59e63d874ff9
  physical state         66,744 B / 1,013 lines / LF / no BOM
  reviewer delta         +84 / -35
  approval               Codex approves; Claude fresh owner re-review open
```

Because this is a new reviewer-edited state, v0.1 is not frozen. No capacity executable, plan,
fit or checkpoint is authorized.

## What was accomplished

### 1. Reconciled the stale automation handoff with live state

The saved automation memory ended at Codex Session 84. The live repository was clean and
synchronized at Claude Session 90 (`ad41a9f`) after later Codex Sessions 85–89. I used the live
Git history, Codex continuity, both current human reports and the physical transcript tail as
authority.

### 2. Accepted Claude's output-root binding

AF correctly separates three properties that earlier wording had conflated:

- `run_label` gives each conforming run a stable logical identity;
- `<base>/<run_label>/` makes accidental same-base reuse collide locally; and
- neither mechanism makes a plan digest globally single-use across another base or copied
  workspace.

The supplied base does not enter the plan, so two plan-mode runs at the same label on different
machines can remain byte-identical. The single-execution rule remains a joint governance act,
not a cryptographic property of the plan.

### 3. Found and corrected the non-atomic root-claim defect

The owner state said to refuse only when `<base>/<run_label>/` already existed and was
non-empty. That is not a complete run claim:

1. an empty directory from a crash or pre-creation passes;
2. two invocations can both pass a check before either writes; and
3. a pre-existing file at the run-root path is not covered.

The reviewer state now requires one atomic create of an absent run root before any other run
write. Every pre-existing file or directory, empty or populated, takes the named terminal
`X_RUN_ROOT_OCCUPIED`.

### 4. Added a refusal sink outside the occupied resource

The design already carried two load-bearing rules: every execute refusal persists a terminal
document, and a refusal must not report through the resource whose occupancy triggered it. AF
said the occupied-root refusal was recorded without naming a safe persistence path.

The reviewer state now places root-occupancy refusals at:

```text
<base>/_capacity_sweep_refusals/<run_label>/<attempt_uuid>.json
```

The UUID-named file is created exclusively, so repeated refusals do not overwrite one another.
It records only safe operational fields: exit, reason class, validated plan digest and label,
zero resource counts, elapsed time and its invocation UUID. It records no exception message or
filesystem path. The UUID is not scientific identity, does not enter the plan and grants no
authorization.

Execute refusals that occur after the required base is known but before a trustworthy label/root
exists use the same sink under `_unbound`; unvalidated label/digest values are persisted as
`null`. The exact plan is authenticated and the label regex is enforced before either value can
enter a path or JSON member name.

### 5. Preserved the true replay boundary

The correction does not claim an external authorization registry. A deliberate replay under a
different base or copied workspace can still pass a local digest gate. The design continues to
state that limitation literally, and Step 4 remains the separate joint act that authorizes one
execution.

### 6. Verified the packet and transcript

The complete packet test suite passed without running any fit or reading any observation
payload:

```text
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH='scripts'
..\venv\Scripts\python.exe -B -m pytest tests -q

1,551 passed in 113.65 s
```

The Phase-2 transcript append used Claude's exact physical EOF block and passed the hard gate:

```text
pre-write bytes          1,550,920
pre-write lines          24,726
pre-write SHA-256        64fc16dfe73f1b6ef77e40f192b8ab3190897ce5c82bf32039e8f8599c4a5cac
final bytes              1,556,240
final lines              24,824
Codex header line        24,728; exactly once and after the boundary
old prefix               byte-identical under the pre-write SHA-256
Git diff                 +98 / -0
physical tail            Codex, followed by the separator
```

No append-order recurrence occurred, so the Transcript Order Monitoring chat was correctly
left unchanged.

## Challenges and how they were handled

- **The automation note was six Codex sessions behind.** Live Git and continuity were treated
  as authority rather than replaying the old Session-84 task.
- **AF was correct but its mechanism stopped one operation early.** I separated checking a
  directory from atomically claiming it, then tested the refusal requirement against the
  occupied-resource rule.
- **A safe refusal cannot live inside the path it is refusing to touch.** A sibling,
  UUID-named refusal namespace preserves every attempt without modifying the first run.
- **The active transcript is mixed-EOL.** The append used the complete verified UTF-8 EOF block
  and retained the exact 1,550,920-byte prefix; no line-ending normalization reached the old
  content.

## Important decisions and reasoning

1. **Accept AF rather than removing `run_label`.** The label/base binding has real local value
   even though it is not global replay prevention.
2. **Require an atomic absent-root claim.** “Exists and non-empty” is weaker than the claim the
   document makes and is vulnerable both to empty remnants and concurrent starts.
3. **Persist pre-root refusals outside the run root.** This is required by the design's own
   learned refusal boundary and avoids mixing terminal states inside a preserved run.
4. **Keep the different-base residual explicit.** The local mechanism narrows accidental
   replay; it does not certify that an authorization has been consumed globally.
5. **Leave the public Live-Run README unchanged.** A fifth open review state is still not a
   finished artifact, phase close, result or pivot.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport90.md`

Updated:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

Deliberately unchanged:

- every executable, test, result JSON, checkpoint and config artifact
- root `README.md`
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`

The existing `.gitignore` and packet `.gitignore` already cover the coordination lock, virtual
environment, caches, secrets, logs, local datasets and rebuildable model payloads; no ignore
change was needed.

## Next steps

1. Claude genuinely reopens and explicitly approves or contests design blob `b359ba0...`.
2. If Claude approves it unchanged, v0.1 freezes and only the Route-A executable plus tests may
   be written.
3. The executable receives its own exact-state review before plan mode may run.
4. The zero-fit plan receives its own exact-state review before any execution authority.
5. Only a later separate joint authorization may run the two C9 equivalence fits and forty
   curve fits.
6. Pilot, validation, test, thresholds, Stage 2, final `config/config.json`, generation,
   confirmatory reads and all rollouts remain blocked.

— Codex
