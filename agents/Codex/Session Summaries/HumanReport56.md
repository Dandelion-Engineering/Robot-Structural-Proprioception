# Human Report — Codex Session 56

**Current date and time:** 2026-08-01 18:13 PDT

**Phase:** Phase 2 — Execution

**Session role:** Exact-state reviewer of Claude Session 56's pre-registered fault helper, live I13a onset check, machine-path correction, driver tests, and packet README Step 25

**Final config state:** **UNFROZEN**; `Reproducibility Packet/config/config.json` does not exist

**Protocol-P execution state:** Stage 0 remains executed exactly once and jointly approved. No replay, Stage-A/B/C rollout, or Stage-0 re-execution occurred this session. Stages A/B/C remain unexecuted and unauthorized. The confirmatory test split remains untouched.

---

## Summary

Claude Session 56 added the pre-registered `screen_physical_faults` helper, replaced the construction layer's same-input onset comparison with a driver-level check whose expected onset is independently re-derived from the bound trajectory document, removed an absolute machine path from the plan/results artifact, added 37 driver tests, and documented the zero-rollout plan path as packet README Step 25.

I reproduced Claude's three handed-off Git blobs and reviewed the implementation against Protocol P v2.3.3, the review-cycle and reproducibility-packet playbooks, and the project's portability and evidence-boundary standards.

The driver and test states are approved unchanged:

```text
Reproducibility Packet/scripts/run_protocol_p_screen.py
  7668793e147a2776cb003ea90c79e76247d9b4de

Reproducibility Packet/tests/test_protocol_p_driver.py
  23222d0ed03c26f57cfff5f53267ca8186a8d31a
```

I made one narrow reviewer edit to Step 25. The handed-off sentence said a reader would find "180 stamps over 168 rollouts." Reused logical rows do not mint stamps; the table contains 180 provenance references comprising 168 distinct stamps. I changed only that phrase and approve the reviewer-edited packet README at:

```text
Reproducibility Packet/README.md
  9c9fa7f03de8b000580704330755f232cfdb8ef1
```

Because that is a reviewer-edited owner artifact, its review loop remains open for Claude's explicit same-state re-review. The executable implementation list is empty on my review, but this session deliberately did not make the separate execution-authorization decision.

The required recent-work cross-review then found one separate error in Claude's Session-56 progress report. It said Protocol P had spent one simulation total. The project has one official replay result, but the simulator physically ran that one-row gate four times: the original Session-45 result, a clean and an injected-stray-write run in Session 46, and a regression run after the Session-51 shared-import edit. I corrected that paragraph and approve the reviewer-edited report at blob `39c592422639b84005a2dd7d9539171be541a84c`; Claude must genuinely owner-review that state too. Stage 0 still used no physics and Stages A/B/C still spent zero rollouts.

---

## What I reviewed

Following `AgentPrompt.md`, I read the project details, Codex continuity, every Codex-including chat summary, both active Codex transcripts, Claude's latest human report, and the authoritative Phase-2 delta after the verified Session-55 checkpoint. I also read:

- `Playbooks/review-cycle.md`;
- `Playbooks/reproducibility-packet.md`;
- `Playbooks/live-run-readme.md`;
- `Playbooks/research-progress-report.md`;
- Protocol P v2.3.3 Correction 1 and invariants I13a/I13b;
- the complete Session-56 driver additions and their production call site;
- all 37 new driver tests and the corrected error-message anchor;
- packet README Step 25 and its surrounding Protocol-P runbook steps;
- Claude's Session-56 progress report and public milestone; and
- the live commit/diff scope and exact Git blob identities.

The public Live-Run README already contains Claude's lean Session-56 milestone with the correct unrun/unauthorized boundary. This review changed no public scientific state, so I did not append another near-duplicate entry.

---

## Review findings and decisions

### Approved: document-derived onset makes the I13a check live

The previous construction check built the requested tuple and its comparison tuple through the same helper with the same caller-supplied onset. It could detect mutation after construction, but it could not tell whether the shared onset itself came from the trajectory document or was an incorrect literal.

The new split closes that specific gap:

1. `build_overrides` still creates the tuple the rollout will carry.
2. `screen_onset_index` independently reads `onset_time_s` from the bound trajectory document and uses the generator's off-grid-refusing `_step_index` conversion.
3. `screen_physical_faults` builds the expected tuple from that document-derived onset.
4. `require_preregistered_faults` compares every `FaultSpec` field and type immediately before the executor is called.

The discriminating test constructs a real bundle at onset 0. The construction layer's old comparison accepts it when given onset 0; the new check refuses it because the document requires onset 500. The wire test then monkeypatches the new check to refuse and proves the rollout executor receives zero calls. This is the right evidence for a pre-execution guard.

### Approved: one production authority for fault fields, one independent specification test

The runtime helper delegates the non-onset fields to `requested_fault_specs`; it does not copy the seven field literals into a second production implementation. The independent test quotes Correction 1 and binds the shared builder to those exact literals.

That means the runtime field comparison is live against a mutated constructed tuple, while a mutation to the shared builder's own constants is caught by the specification test rather than by a second production copy. The driver states this limitation plainly instead of presenting the field half as an independent derivation.

### Approved: keep the redundant helper vocabulary guard

Claude asked whether the helper's own closed-vocabulary refusal should remain even though `requested_fault_specs` independently refuses the same unknown condition.

I ruled **keep it**. Correction 1's executable sketch places the closed-set check inside the named helper, so keeping it preserves the pre-registered surface. It does not create a second vocabulary because `SCREEN_CONDITIONS` is an alias of the construction layer's tuple. The code and tests also explicitly state that deleting the line changes the message, not the outcome, and do not count it as load-bearing coverage.

### Approved: remove the machine fingerprint from the artifact

Plan mode previously recorded the absolute config path. The corrected artifact records `config/draft-config-v0.1.json` for an in-packet file and a name-only marker for an outside-packet file. The same input block retains the canonical base-config hash, so the path remains readable without becoming the identity authority.

My independent plan run confirmed the written JSON contains no drive-letter path.

### Reviewer-edited: distinguish provenance references from distinct stamps

Step 25 correctly explains 180 logical rows, 168 physical rollouts, and twelve reuses. Its final provenance sentence blurred occurrences with identities. I changed:

```text
180 stamps over 168 rollouts
```

to:

```text
180 provenance references comprising 168 distinct stamps
```

This changes no command, count, cost estimate, result boundary, or execution authority.

### Accepted for the later execution round: replay immediately before measurement

I accepted Claude's sequencing proposal in principle but did not execute it. The dedicated execution round should first explicitly authorize the one replay-gate check, run and review that bit-level positive control, and then separately decide whether to authorize the 168 Stage-A/B/C rollouts. This keeps replay authority separate from implementation approval and preserves the honest claim that the instrument was checked immediately before measurement.

### Reviewer-edited: one official replay result is not one physical execution

Claude's progress report collapsed two valid counts. There is one official exact replay result, but four physical replay-gate executions occurred:

```text
Session 45   original exact replay result                         26.37 s
Session 46   clean corrected-gate control run                     26.64 s
Session 46   injected-stray-write corrected-gate refusal          27.03 s
Session 51   regression after the shared-import edit              25.08 s
```

I changed only that paragraph, preserved the cost-discipline point, and made the Stage-0/no-Stage-A/B/C boundary explicit. The handed-off blob was `fb0a8d74e1afe7ffa8217f4de334b3bea5d00fa9`; the reviewer-edited approved blob is `39c592422639b84005a2dd7d9539171be541a84c`.

---

## Verification

```text
Claude driver/test blobs                    exact
plan mode                                   0.287 s; zero rollouts
plan census                                 9 candidates / 180 logical rows /
                                            168 physical rollouts / 12 reuses
derived onset and window                    500 / [1000, 1768)
plan results                                null
recorded config path                        config/draft-config-v0.1.json
drive-letter path in plan artifact          absent
focused driver suite                        148 passed in 96.43 s
full packet suite                           975 passed in 110.92 s
compileall                                  clean
config.json                                 absent
test-named / results NPZ material           0 / 0
Protocol-P plant rollouts                   zero
Stage 0 / replay gate                       not re-run
confirmatory split                          untouched
```

Both transcript appends passed the hard gate. The first review append recorded:

```text
pre-write lines                             13,628
pre-write bytes                             945,410
old-prefix SHA-256                          a652d4df4db0ef9772d72a199cd10267f40d4541bdad7658c1496d2b3d4d3ea0
old prefix after append                     exact
Codex Session-56 header                     exactly once, line 13,632
header after pre-write boundary             yes
transcript diff                             +113 / -0
post-write lines                            13,741
post-write bytes                            950,681
post-write SHA-256                          6c44700e277621e9706f0fad8e7b961a16326ae902efb5ebb67ce7175799141a
```

The later progress-report correction preserved that entire first append as its exact prefix:

```text
second pre-write lines                      13,741
second pre-write bytes                      950,681
second old-prefix SHA-256                   6c44700e277621e9706f0fad8e7b961a16326ae902efb5ebb67ce7175799141a
second old prefix after append              exact
cross-review correction header              exactly once, line 13,745
header after second boundary                yes
cumulative transcript diff                  +151 / -0
final lines                                 13,779
final bytes                                 952,348
final SHA-256                               5f127b2608f982b32f2c549a9992582fccaffea3efbd8b7b2810761adec564ef
```

Session 56 is an every-eighth Codex session, so I also wrote `agents/Codex/Progress Reports/Progress Report Session 56.md`.

---

## Files created or updated

- `Reproducibility Packet/README.md` — one reviewer precision edit in Step 25.
- `agents/Claude/Progress Reports/Progress Report Session 56.md` — corrected one official replay result versus four physical replay-gate executions; reviewer-approved and returned for owner re-review.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the exact-state approvals, guard ruling, Step-25 reviewer edit, verification, replay sequencing, and unchanged execution boundary.
- `agents/Codex/Session Summaries/HumanReport56.md` — this report.
- `agents/Codex/Progress Reports/Progress Report Session 56.md` — regular director-facing eight-session update.
- `agents/Codex/README.md` — adds Session 56 and updates active-state routing.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the next session.

No driver module, driver test, result layer, result-layer test, protocol specification, assignment, draft config, dataset payload, result artifact, confirmatory material, or public Live-Run entry changed in Codex Session 56.

---

## Next steps

1. Claude reopens packet README blob `9c9fa7f03de8b000580704330755f232cfdb8ef1` and progress-report blob `39c592422639b84005a2dd7d9539171be541a84c`, then explicitly approves each unchanged or returns a new exact state.
2. After the Step-25 review loop closes, the agents enter a separate execution-authorization round; the progress-report loop is a reporting correction rather than an execution prerequisite, but should also close normally.
3. In that round, explicitly authorize and run the one-row replay gate immediately before measurement, review its result, and only then decide whether to spend the 168 Stage-A/B/C physical rollouts.
4. The downstream sequence remains written Amendment A2, replacement assignment/config lineage, coherent regeneration, Gates 4–7, joint immutable freeze, and one-shot confirmatory generation/evaluation.

— Codex
