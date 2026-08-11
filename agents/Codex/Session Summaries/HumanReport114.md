# Codex — Human Report, Session 114

**Date and time:** 2026-08-10 23:11 PDT

**Phase:** Phase 2 — Execution, with limited Phase-3 packet assembly

**Progress-report session:** No. The next regular Codex progress report is Session 120 unless a
phase transition or approved Claim Sheet amendment triggers one sooner.

---

## Summary

Claude Session 114 genuinely re-opened Codex's reviewer-edited rung-2 test state, independently
drove both review findings, reproduced the full packet test count, and explicitly approved the
same module and test blobs Codex had approved. I authenticated those identities directly and
recognized the loop as closed:

```text
Reproducibility Packet/scripts/utils/attribution_net_rung2.py
Git blob                 ca192af0b1263fdb7d19491e09a2b5c99dc7639b
raw SHA-256              59333b48b4c9a580a165c83f672232a75cbc8220debe98a7c04748ac705ff7c7
review state             CLOSED / BOTH APPROVED

Reproducibility Packet/tests/test_attribution_net_rung2.py
Git blob                 c43d33b007701cf3c9b24c1f6a267d2329c25c1e
raw SHA-256              caaf108deab021eecfc418a93ea2ae6c6965ab771303dcae51cc4584d6017f82
review state             CLOSED / BOTH APPROVED
```

Step 2 of the frozen seven-step rung-2 sequence is now closed. Only Step 3 is newly authorized:
Claude may write `Reproducibility Packet/scripts/utils/rung2_escalation.py` and
`Reproducibility Packet/tests/test_rung2_escalation.py`; Codex will review the returned pair.
Plan mode, fitting, analysis, role reads, capacity and threshold selection, and final
configuration remain separately blocked.

The general recent-work review found two narrow precision defects in Claude's new public rung-2
log entry. The entry called all eleven mutation cases defects even though nine were faults and two
were deliberately harmless controls. It also called the five remaining sequence steps "joint
approvals," while frozen design section 11 distinguishes build/review loops, a zero-fit plan action
plus review, a separate two-half execution authorization, and the final exact-state/joint-read
gate. I corrected only those two phrases and explicitly approved the reviewer state:

```text
README.md
incoming Claude Git blob    4377a68341d9a54a241ca0aadfb9b4ab9a80e961
reviewer Git blob           e291a229b3ab57fc64287f0d3ba0cde68e5200f6
reviewer raw SHA-256        b18f810a7adddc2d2adbf953ca76aefaad5ab2e6ed9b9ebe950dc850e5bdc77b
reviewer bytes / EOL        144,309 / 205 LF / 199 CR
review delta                +1 / -1, newest public-log line only
review state                CODEX APPROVED / CLAUDE OWNER RE-REVIEW OPEN
```

The milestone and its public scope are otherwise sound: the larger network exists and is jointly
approved, nothing has been trained with it, and no scientific result is claimed.

## Startup and continuity audit

The automation gate was followed before project work:

1. `CODEX_HOME` was unset, so the required automation memory was read from the standard local
   location `C:\Users\cresp\.codex\automations\robot-structural-proprioception\memory.md`.
2. `.agent-turn` named Codex.
3. `.agent-session.lock` was absent, so Codex created it.
4. The mandatory second `.agent-turn` read still named Codex.
5. `AgentPrompt.md`, all project details, Codex continuity, all Codex-participant chat summaries,
   the monitoring chat, and the unseen Phase-2 suffix were ingested before work.

The previously published 1,942,223-byte Session-113 transcript state hashed exactly to Codex's
recorded `614e48ae...`; the only unseen suffix was Claude Session 114. This prevented older
automation memory from being mistaken for current approval state.

## Review of Claude Session 114

Claude's owner re-review was measurement-backed rather than inferred:

- an eleven-case wiring grid showed the two Codex-named live-but-misordered paths survived the
  incoming tests and were caught by the reviewer test;
- seven other fault mutations were caught by both states;
- two harmless controls survived both states;
- the new encoder-order test was the sole failing test for each Codex negative control;
- a throwaway forward hook proved the approved `capacity_sweep.score_arm` seam actually executed
  rung 2 once and returned the approved three-metric mapping; and
- focused normal, focused optimized-mode and packet-wide suites reproduced at 71, 71 and 1,863
  passing tests.

I accepted Claude's separate ruling that constructor parameter-draw order is not a missing design
contract. The design specifies architecture, not initialization draw sequence; no rung-2 fit
exists to reproduce; and the later executable binds module code identity. Adding a test would
freeze an unapproved requirement.

I did not rerun the Python suites this session. Both code artifacts are byte-identical to the
states Codex already tested and approved, and Claude's independent owner pass reproduced the full
suite at those exact identities. The only working changes in this session are prose.

## Step-3 ownership decision

Claude asked whether Codex would rather write the Step-3 executable. I declined and left the build
with Claude because the agreed Phase-1 labor split assigns the learned attribution estimator and
capacity ladder to Claude, Claude owns the module the executable must instantiate, and review
closure did not amend that split. Codex remains the required reviewer.

This avoids silently reassigning an artifact at the moment its implementation begins. The
authorization is narrow: executable plus tests only. Frozen design section 11 still requires the
remaining five gated steps in order.

## Public Live-Run review

I read the Live-Run playbook before reviewing the new entry. The architecture milestone is
genuinely noteworthy and warranted one lean public entry. The banner remains correctly in
Phase 2 / In Progress, so no banner edit was needed.

The review changed no result, cost, architecture, parameter count, training state or
authorization boundary. It only made the case count and gate vocabulary agree with Claude's own
measured grid and the frozen sequence. The earlier cost-correction loop remains closed at README
blob `bb98b66e...`; this is a separate, newest-entry review loop.

## Transcript integrity

The Phase-2 response used Claude's complete, programmatically verified unique physical EOF block.
The old prefix was rehashed after the append rather than inferred from Git.

```text
pre-write transcript       1,950,094 bytes / 31,512 LF / 19,456 CR
pre-write SHA-256          2566e16f689b6003de115ed42f736e8373793a5b3983e9489f6cab8580bd6db3
cross-agent prior/post     exact match to Claude's published Session-114 digest
old prefix                 byte-identical
Codex header               unique at physical line 31,514
transcript diff            +86 / -0
last agent                 Codex
post-write transcript      1,954,669 bytes / 31,598 LF / 19,456 CR
post-write SHA-256         2adbf843d6bea5d3e6229938cf75dd4c8e2ae84aa73b537c6e9b09580de687c8
```

No Transcript Order Monitoring entry was warranted: the append landed at the physical tail, the
old prefix remained exact, the header was unique after the boundary, and the Git diff is
additions-only.

## Challenges and decisions

Two host details required fallbacks without changing project state. `CODEX_HOME` was unset, so the
automation memory used its standard explicit path. This PowerShell host also lacks
`Convert.ToHexString`; prefix hashing therefore used `BitConverter` after the first unsupported
call returned no hash. The recomputed digest matched the known state exactly.

The substantive judgment was whether the public wording differences were material enough to
repair. They were: one contradicted the documented composition of the mutation grid, and the
other collapsed five different sequencing steps into one kind of approval. Both are cheap to fix
while the newest entry is still under same-state review, and neither requires reopening settled
technical work.

## Files created or updated

- `README.md` — corrected the newest public rung-2 entry's mutation count and sequencing
  vocabulary; reviewer blob awaits Claude owner re-review.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended Step-2 closure, Step-3 ownership, README review and the resource boundary.
- `agents/Codex/Session Summaries/HumanReport114.md` — this report.
- `agents/Codex/README.md` — updated the workspace index and current review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 115.

Deliberately unchanged: both rung-2 code artifacts, the frozen rung-2 design, every Stage-1
executable/plan/result/artifact/checkpoint, the C7 analysis, the Claim Sheet, both `.gitattributes`
files, both `.gitignore` files, `director_requests.md`, and the absent final configuration.

## Resource and evidence boundary

This session opened no manifest, `.npz`, label payload, model checkpoint, pilot outcome,
validation outcome or test outcome. It ran no fit, wrote no checkpoint, generated no data, spent
no rollout, invoked no C7 reader or analyzer, ran no plan mode, selected no capacity, set no
threshold and materialized no final configuration.

Rollouts remain 278. The lifetime fit counter remains 13. Stage 1 remains complete as scoped and
licenses only its no-readable-shape sentence.

## Next steps

1. Claude genuinely re-opens README blob `e291a229...` and either explicitly approves it or
   returns another newest-entry state. That review is independent of Step 3.
2. Claude writes only `rung2_escalation.py` and `test_rung2_escalation.py` under frozen design
   section 4.4 onward, then explicitly approves and hands the exact pair to Codex.
3. Codex's next session authenticates and reviews the returned executable/test pair. It must not
   run plan mode or fit.
4. Plan mode, execution, the analyzer, exact result review, role reads, capacity selection,
   thresholds and final configuration remain separately gated.
5. The 55-checkpoint clean-machine recovery/distribution limitation remains open for Phase 3.
6. Codex Session 120 is the next regular progress-report session.
