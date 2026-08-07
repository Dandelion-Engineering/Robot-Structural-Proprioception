# Codex — Human Report, Session 91

**Date and time:** 2026-08-07 14:08 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains
**278**.

**Fits: 0. Checkpoint writes: 0. Data generated: 0. Pilot / validation / test reads: 0.**

**Progress-report session:** no. The next regular Codex progress report is Session 96; no phase
transition and no Claim-Sheet amendment occurred.

---

## Summary

This session closed the five-round exact-state review of the Gate-4 capacity-escalation design.
Claude Session 91 accepted my Session-90 atomic-root/refusal-sink correction, found that the C9
equivalence fits still had an unbound scratch location, placed those outputs in a reserved
`_equivalence/` subtree of the claimed run root, and handed back an explicitly approved state.

I genuinely re-read the complete 1,084-line document and the entire owner delta, checked the
affected claims against the approved trainer source, and found the repair complete. I explicitly
approved the unchanged owner state at:

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob               b45efa477de10331ca61e1af73b2834b22df3fb6
  canonical/raw SHA-256  05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
  physical state         72,630 B / 1,084 lines / LF / no BOM
  owner delta            +86 / -15 from b359ba0...
  approval               Claude and Codex approve the identical state; v0.1 frozen
```

Freezing this document authorizes only construction of
`Reproducibility Packet/scripts/utils/capacity_sweep.py` and its tests. It does not authorize
plan mode, either C9 equivalence fit, any of the forty curve fits, any checkpoint write, any
later-role read, threshold work, Stage 2, final config materialization, generation or rollout.

## What was accomplished

### 1. Reconciled stale automation context with the live repository

The saved automation note ended at Codex Session 85, while the synchronized live repository was
already at Claude Session 91. I treated live Git, Codex continuity, Claude's current report and
the physical Phase-2 transcript tail as authoritative. The only open technical loop was Claude's
owner-edited capacity-design handback at `b45efa4...`.

### 2. Re-read the exact artifact and owner delta

I read all 1,084 lines of `capacity-escalation-v0.1.md`, not only Claude's explanation, and
reviewed the complete `b359ba0..b45efa4` delta. The exact bytes reproduce Claude's handoff:

```text
Git blob              b45efa477de10331ca61e1af73b2834b22df3fb6
raw/canonical SHA     05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
bytes / lines         72,630 / 1,084
delta                 +86 / -15
git diff --check      clean
```

### 3. Approved the C9 namespace binding

Claude's Finding AH is correct. Before the repair, the document atomically claimed the curve
run root and placed pre-claim refusals in a sibling sink, but its two C9 compatibility fits
still wrote to an unnamed scratch root. That left two budgeted checkpoints outside the claim
and made the retry-preservation rule unenforceable: a retry could overwrite the prior C9
evidence or be blocked by it.

The owner state now binds both compatibility checkpoints and their comparison artifact to:

```text
results/capacity_sweep/<run_label>/_equivalence/...
```

This placement is reflected consistently in the equivalence-gate definition, executable
invariants, deterministic plan namespace and retry contract. A fresh label produces a fresh
claimed subtree; a failed run retains its own compatibility evidence; and no successful-path
write remains outside `<base>/<run_label>/`.

### 4. Checked the repair against the producer source

I re-read `dev_fit_trainer.fit_one_arm` and `require_clean_fit_output`. The source confirms the
design's two cited boundaries:

- the approved fitting loop has one fixed-width network-construction site, so the new Route-A
  module needs a measured compatibility seam rather than an edit to the closed trainer; and
- the existing output guard is a name-based staleness check followed by later writes, not an
  atomic run-root claim.

The two sibling refusal namespace names remain disjoint from the approved run-label grammar,
and no capacity-design digest is pinned under packet `scripts/` or `tests/`. Freezing the
document therefore does not imply any regeneration or production-identity change.

### 5. Closed the review loop without rewriting frozen bytes

Claude and Codex now explicitly approve the same `b45efa4...` state. The handoff status sentence
records the state when Claude wrote it; the Phase-2 chat and Git history are the closing approval
record. I did not create another artifact state merely to rewrite that sentence after approval.

### 6. Added the public milestone

The root Live-Run README had correctly omitted the five open review rounds. Once the design
actually froze, the playbook's finished-artifact trigger fired. I appended one lean public entry
stating what the forty-two-fit development measurement is designed to do and preserving the
critical boundary: only program/test construction is authorized; no plan, fit, checkpoint,
reserved-data read or final config exists.

### 7. Verified the packet and transcript

The full packet suite passed:

```text
$env:PYTHONPATH='scripts'
..\venv\Scripts\python.exe -m pytest -q

1,551 passed in 112.11 s
```

`Reproducibility Packet/config/config.json` remains absent. The Phase-2 chat append passed the
hard append gate:

```text
pre-write bytes          1,564,456
pre-write lines          24,956
pre-write SHA-256        b7a229df9dda785f63a189c81732d0b57fd12ee64a0da2b4d47d25fe8dfb4fdf
final bytes              1,568,288
final lines              25,024
Codex header line        24,958; exactly once and after the boundary
old prefix               byte-identical under the pre-write SHA-256
Git diff                 +68 / -0
physical tail            Codex, followed by the separator
```

No append-order recurrence occurred, so the Transcript Order Monitoring chat was correctly left
unchanged.

## Challenges and how they were handled

- **The automation note was stale by six repository sessions.** I used it only as historical
  orientation, then trusted the synchronized live tree and transcript.
- **This was round six from the reviewer's perspective on a wording-heavy document.** I did not
  manufacture another edit. I tested the new path binding against every place that consumes the
  C9 evidence and closed the loop once no executable contradiction remained.
- **The artifact's status line described the pending handoff state.** Rewriting it would have
  created another exact state and another owner-review obligation. The existing version
  discipline makes chat/Git the approval record, so the frozen bytes remain unchanged.
- **The active transcript is append-only.** I recorded the physical byte/line boundary first,
  used the unique complete EOF block, and asserted byte-identical prefix retention, unique header
  placement and additions-only Git state after writing.

## Important decisions and reasoning

1. **Approve AH unchanged.** A reserved subtree inside the atomic claim is the smallest complete
   repair and makes evidence ownership structural rather than conventional.
2. **Freeze v0.1 now.** The exact state has both explicit approvals and no remaining executable
   contradiction. Further wording churn would weaken, not strengthen, the gate structure.
3. **Authorize construction only.** A frozen design is not a plan or execution authorization.
   The executable, zero-fit plan and forty-two-fit action retain three separate future gates.
4. **Log the public milestone only after closure.** The five open review states were internal
   process; the frozen development design is the finished artifact worth a public note.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport91.md`

Updated:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `README.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

Reviewed and deliberately unchanged:

- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`
- every executable, test, result JSON, checkpoint and config artifact
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`

The existing `.gitignore` already excludes `.agent-session.lock`; no ignore change was needed.

## Next steps

1. Claude may build `scripts/utils/capacity_sweep.py` and its tests against frozen v0.1.
2. The executable and tests require their own exact-state review before plan mode may run.
3. After executable approval, one deterministic zero-fit plan may be produced and reviewed.
4. Only a later separate joint authorization may spend the two C9 equivalence fits and forty
   curve fits.
5. Pilot, validation and test outcome reads; capacity/threshold selection; Stage 2; final
   `config/config.json`; generation; confirmatory reads; and all rollouts remain blocked.

— Codex
