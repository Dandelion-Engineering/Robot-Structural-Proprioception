# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 136 on 2026-08-14.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3 and Step 4a are closed / both approved. Step-4a exact design blob is
  `032db1666efbe00adec5696de70424d531ba33a2`, raw SHA-256
  `f761a673ff8fcca6c58fe530a3faaed57630315a87a5e241d8ca9675a13c4ffc`, 83,181 bytes /
  1,062 LF / 0 CR.
- Step 4b-i is **OPEN — Round 1 reviewer ledger complete; awaiting Claude's owner response**. Codex
  does not approve either candidate. Claude owns the response unless labor is explicitly reassigned.
- Governing card: `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md`.
- Active narrow chat: `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/Slot-8 Step-4b-i
  Connection-Record Contract - Active.md`.
- Step 4b-ii has not started and is not authorized while 4b-i is open. Even 4b-i closure would approve
  only record parsing/binding, not source reads, bundle construction, persistence or full Step 4b.
- No production connection record, real role/index/payload/checkpoint/result read, Step 4c–4f work,
  capacity or threshold choice, final configuration, adapter run, or C1-versus-S claim is authorized.
- The next regular Codex progress report is Session 144.

## Exact Step-4b-i candidate and evidence

- Module: `Reproducibility Packet/scripts/utils/connection_record.py`, Git blob
  `b1a574650b1fcf673d04daf1df0b2d9c24f868f0`, raw SHA-256
  `12bf71e5626f817f2ccc271882906af13afacc24cc7120a55aa96cffa3713046`, 59,076 bytes /
  1,468 LF / 0 CR.
- Tests: `Reproducibility Packet/tests/test_connection_record.py`, Git blob
  `6c89914502e0dff2f00e96a8b70b09d63349c30c`, raw SHA-256
  `5b24716dd541d2f2ea7b6aa7585ad68b6470f9497818cbe7c2c5cec9238e5d25`, 50,022 bytes /
  1,245 LF / 0 CR.
- Verification passed 212 focused tests, the same 212 under `python -O`, `py_compile`, and 2,479
  packet-wide tests with zero failures or collection errors. `git diff --check` was clean.
- The green suite does not construct the five blocking states below. No candidate source or test was
  edited by Codex.

## Complete Round-1 blocker ledger

1. **Record path/open set:** valid bytes load from an arbitrary path; `bind_root_domains` has no actual
   record path to bind against `packet_root / record_relative_path(record_label)`; and
   `expected_open_set` omits the record. Bind the real path, carry it in `BoundPaths`, include it in W3's
   exact set, and test arbitrary/output-tree copies.
2. **Deep immutability:** frozen dataclasses contain mutable `document`, `arms`, `roles`, `manifest_row`,
   `links` and `sources` mappings. Exact probes mutated both a role reference and the retained record
   label. Deep-freeze every parsed mapping and test mutation refusal at every typed layer.
3. **Huge integer:** `analysis_window_s = 10**400` raises raw `OverflowError` during `float()` instead of
   `X_CONNECTION_UNAUTHORIZED`. Translate overflow/conversion failures and cover the large-integer form
   across numeric helper classes.
4. **Portable paths/containment:** embedded NUL reaches raw `ValueError`; Windows ADS, device names and
   trailing-dot/space components pass; the output parent bypasses `_resolve_under`, permitting a
   junction/symlink escape. Define a total portable component grammar, translate resolution failures and
   prove every packet-relative source and destination remains under one injected root.
5. **`case_id` output traversal:** arbitrary non-empty strings reach renderer filenames. The integration
   probe wrote `../escaped-case` PNG/JSON beside the requested bundle directory. Require a portable leaf
   token at the record boundary and writer-side containment; test traversal, separators, drive/ADS/device
   aliases and the observed write set.

Claude must integrate or contest the whole ledger in one owner response and name both changed and
mechanically byte-identical regions. Round 2 is delta-only: review each disposition, the named acceptance
tests and regressions introduced by the delta. Do not restart a whole-file audit absent contrary evidence.

## Review and chat protocol

- The director's Review Card and convergence method governs formal review and supersedes the remainder
  of `Playbooks/review-cycle.md` where they conflict.
- Authenticate every candidate with its full Git blob, raw digest, byte count and EOL figures; verify the
  Git object resolves before relying on it.
- A reviewer records the complete numbered ledger in Round 1. The owner answers every item and identifies
  changed plus unchanged regions. Round 2 is a bounded delta review.
- Same-state explicit approval by both agents is required. Green tests, reviewer edits, downstream use,
  a handoff or silence are not approval.
- Use the active Step-4b-i chat only for this first-half contract. Do not append to concluded Step-4a or
  other concluded subject chats.
- The director-visible Review Boundary and Convergence chat is only for method feedback/problems, not the
  subject decision. No method triage is currently open.
- Use Transcript Order Monitoring only if the same writer's message appears after a verified opposite-agent
  EOF tail. No recurrence occurred in Session 136.

## Session-136 public and continuity state

- `agents/Codex/Progress Reports/Progress Report Session 136.md` covers Sessions 129–136: closure of the
  synthetic fixture, Step-4a convergence, the Review Card rollout and the current blocked implementation.
- Root `README.md` was intentionally not changed. A rejected first-half candidate is not a finished public
  milestone, and the Session-135 heartbeat already states the active boundary.
- `agents/Codex/Session Summaries/HumanReport136.md` records the exact probes, evidence, decision and
  preserved authority limits.
- Non-blocking general recent-work note: Claude's HumanReport136 files-updated list omits
  `agents/Claude/Permanent Instruments.md`, although the Claude Session-136 commit changed it by 25 lines.
  Claude should reconcile that record; it does not affect the formal Step-4b-i verdict.

## Existing durable boundaries

- Stage 1 remains complete only as a development screen: no readable paired shape at five points/five
  seeds, no licensed trend statement, and no capacity or threshold selected.
- Rung 2 remains complete only as scoped. Its fit/analyzer invocations are spent; all ten arms have zero
  healthy and structure F1, which is an observed development fact rather than a causal claim.
- The verified synthetic Slot-8 fixture is four deterministic 300-DPI case figures under
  `Reproducibility Packet/results/verification_fixture/`. It proves the display mechanism, not a scientific
  result, and its real-role path refuses before a scientific file opens.
- Project counters remain 278 rollouts, 67 fits, 67 checkpoints, and zero pilot/validation/test reads.
- Amendment A2, role separation, no-exploratory-recompute rules, the 67-checkpoint distribution/recovery
  issue, the non-blocking Claim Sheet director request, and all unspent scientific gates remain in force.

## Append-only transcript discipline

Before any transcript append:

1. read the UTF-8 physical tail and record byte and line counts;
2. patch only against a programmatically verified unique multiline EOF anchor;
3. verify the entire pre-write byte sequence is the new file prefix;
4. verify the new session header occurs exactly once after the old byte boundary; and
5. reread the physical tail and confirm the new message is last.

If any assertion fails, stop and repair with a dated append-only correction before commit.
