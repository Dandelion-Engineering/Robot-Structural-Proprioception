# Codex - Human Report, Session 103

**Date and time:** 2026-08-09 14:19 PDT

**Phase:** Phase 2 - Execution.

**Progress-report session:** no. The next regular Codex progress report is Session 104 unless
a phase transition or an approved written Claim-Sheet amendment fires first.

## Summary

This session moved the capacity-escalation lane through one deliberately separate gate: the
single pre-registered C7 descriptive read now exists as an exact development-only artifact.
It has one agent's owner approval and still requires Claude's independent same-state review.
No section-5.4 scientific interpretation, capacity choice, threshold, Stage-2 action or
later-role read occurred.

Claude Session 103 had already closed the C7 implementation review and issued the first half
of an authorization for one exact command, input set and exclusive output destination. I
read Claude's latest report and physical transcript turn, re-measured the exact approved
reader and test bytes, authenticated the three inputs, drove the entire real-state pre-read
chain through all fifty checkpoint evaluations, and stopped immediately before
`derive_analysis`. I then ran both focused suites and the full packet suite before issuing
Codex's matching authorization half.

That preflight caught one non-load-bearing error in Claude's record. The capacity-sweep base
does not contain exactly three entries; it contains the preserved first-run
`capacity_sweep_plan.json` plus three directories: `plans/`, `stage1-run-1/` and
`stage1-run-2/`. Claude's three names were the complete directory census, not the complete
entry census. I corrected the statement forward in Codex's authorization turn. The omitted
file changed neither the proposed analysis destination nor any authenticated input, so it did
not block the run.

After both halves were physically present, I ran the exact command once from
`Reproducibility Packet/scripts/`. It exited zero and exclusively wrote:

```text
Reproducibility Packet/results/capacity_sweep_analysis/stage1-run-2/capacity_sweep_analysis.json
```

The command performed no fitting, checkpoint writing, simulation, generation, physical
rollout or pilot/validation/test read. It reread only the 304 authorized development examples
(C1 152, S 152) and the fifty checkpoints named by the jointly approved terminal record. It
wrote one 89,150-byte canonical JSON artifact.

I then independently audited the artifact without calling the production
`derive_analysis`. The audit matched every one of its fifty reported arms to the authenticated
source records and to its physical checkpoint digest, rebuilt every pair difference,
headroom, constraint, suite mean, paired mean, sample standard deviation, loss-term mean,
eligible-domain field, curve shape, range, quantized companion and derived label, and checked
all eleven analysis-code identities against the current files. The terminal was
`ARTIFACT_EXACT_STATE_OK`.

I explicitly owner-approved the exact artifact bytes and handed them to Claude. That is the
first half of the artifact review loop, not the completed loop. Claude must genuinely audit
and explicitly approve the same blob before the pre-written section-5.4 prose may be applied
jointly. Even then, capacity selection and Stage 2 remain separate decisions.

## Exact states

### Jointly approved C7 reader and tests

```text
Reproducibility Packet/scripts/analyze_capacity_sweep.py
  Git blob                 b9043fa266dc7c35a6acdb240216ae0ec3337f6e
  canonical/raw SHA-256    7eca4016d7ffb73c15ec1e35642e5f6e1ecb95a7c6757e72cc875cf79f87ffbe

Reproducibility Packet/tests/test_capacity_sweep_analysis.py
  Git blob                 a81d35c952fba158f647a64b9cd13bad0c301c93
  canonical/raw SHA-256    bd8c36316b4be433cac0000ef2597137cb35b68b0f5407c7b992764d9976d229
```

The one execution authorization for these bytes is spent. Do not invoke this reader again.

### Authenticated inputs

```text
capacity_sweep_result.json  canonical 0d8a1c2de7208cc9a551d75ce44e3a64f02de6c9881b4b31f4df4d07cc7f7a2a
capacity_sweep_plan.json    canonical ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
dev_fit_analysis.json       canonical 7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58
```

### New C7 artifact

```text
Reproducibility Packet/results/capacity_sweep_analysis/stage1-run-2/capacity_sweep_analysis.json
  Git blob                 3c963059e8067655c07b2c551e159e6e93be982d
  canonical/raw SHA-256    e381d12eafcf04c80d42aaed1bd9775bf9fbd64f1db166be535de356b7642736
  size                     89,150 bytes
  encoding                 UTF-8 / LF domain / no CR / no BOM / no final newline
```

Persisted record fields, reproduced here only to identify the review state:

```text
channels  constraint  paired S-C1 mean raw / quantized
16        NONE        -0.016970626445936842 / -0.016971
24        NONE         0.0060113946602796675 /  0.006011
32        NONE        -0.032088741654399996  / -0.032089
40        NONE        -0.05544542456418402   / -0.055445
48        NONE        -0.1509182636928158    / -0.150918

derived_label                              NO_POST_ANCHOR_NONNEGATIVE_POINT
eligible post-anchor points                [40, 48]
first post-anchor nonnegative point        null
first eligible post-anchor nonnegative     null
first all-constrained point                null
paired range raw / quantized               0.15692965835309547 / 0.156930
anchor SD raw / quantized                  0.149635726834 / 0.149636
paired_range_exceeds_anchor_sd             true
C1 shape, all / eligible                   STRICTLY_INCREASING
S shape, all / eligible                    NON_MONOTONE
paired shape, all / eligible               NON_MONOTONE
```

These fields are not a project conclusion. The artifact itself says they are an in-sample,
development-only description and authorizes no capacity or threshold.

## Verification

### Before the read

```text
reader/test raw digests and Git blobs                 exact
three input canonical digests                         exact
output base / leaf / file                             absent
final config.json                                     absent
checkpoint census                                     55 = 10 + 3 + 42
real-state pre-read chain                              passed
arms                                                   50 = 10 REUSED + 40 COMPLETED
authorized development rows                           304 = 152 + 152
physical checkpoints evaluated                        50
derive_analysis calls                                 0
tracked worktree after preflight                       clean
focused tests, normal                                 241 passed
focused tests, python -O                              241 passed; expected warning
full packet                                         1,792 passed in 183.22 s
```

The first focused-test attempt was terminated by my one-second shell timeout. Pytest's
stdout failed while the host terminated the process; this was not a test failure. I checked
that the worktree had not changed, then reran both complete focused suites with the correct
execution window. Only the complete 241/241 runs above are decision-bearing.

### After the read

```text
exclusive artifact count                               1
canonical compact JSON re-emission                     byte-identical
authenticated input digests in artifact                3 / 3 exact
analysis code identities                               11 / 11 current
reported arms vs source records                        50 / 50 exact
physical checkpoint digests                            50 / 50 exact
arm census                                             10 REUSED / 40 COMPLETED
point/pair/headroom/constraint calculations            rebuilt exact
suite/paired means and sample SDs                       rebuilt exact
per-point post-fit loss-term means                      rebuilt exact
six-decimal ROUND_HALF_EVEN companions                  all exact
eligible/crossing/range/shape fields                    rebuilt exact
derived label                                           rebuilt exact
forbidden capacity-verdict tokens                       absent
section-5.4 interpretation applied                      no
post-read checkpoint census                            55
final config.json                                      absent
owner audit terminal                                   ARTIFACT_EXACT_STATE_OK
final post-artifact full packet                       1,792 passed in 141.74 s
```

## Challenges and decisions

1. **Treat the live branch as authoritative.** The automation note ended before Claude's
   Session 103. Reading the live transcript and report exposed a valid first authorization
   half and avoided drafting against stale state.
2. **Correct the entry census without invalidating a sound destination.** The omitted
   first-run plan is preserved evidence and must be named. Its presence does not move the
   analysis into the sweep namespace or alter any input digest, so the right action was a
   forward correction plus the matching half, not a needless restart of the authorization
   cycle.
3. **Run every check below the irreversible read first.** The pre-registration is spent when
   the curve is derived, even if writing later fails. The real-state chain therefore stopped
   before `derive_analysis` until both agents had separately authorized the exact act.
4. **Keep production and audit derivations separate.** The owner audit rebuilt the artifact
   from its persisted primitives with independent arithmetic and did not call the production
   derivation function. This is still owner review; Claude's independent audit remains
   mandatory.
5. **Do not apply section 5.4 early.** The exact record contains the values needed for that
   interpretation, but the frozen sequence requires same-state artifact approval first. I
   recorded fields and boundaries only.
6. **Update the public log once, at the milestone boundary.** The root README now says that
   the pre-registered development read exists and that independent review remains open. It
   does not publish a scientific interpretation or a model choice.

## Transcript integrity

The C7 authorization and execution handoffs were two separately gated physical-tail appends.

Authorization append:

```text
pre-write bytes/hash        1,786,439 / a71d915f...20b85d
pre-write physical lines    28,755
header                      unique at physical line 28,757
prior prefix                byte-identical
final Git diff then         +94 / -0
```

Execution/owner-handoff append:

```text
pre-write bytes/hash        1,791,126 / 6d0a630a...65c07d
pre-write physical lines    28,849
header                      unique at physical line 28,851
prior prefix                byte-identical
combined transcript diff    +179 / -0
Codex                       physically last
```

No Transcript Order Monitoring note was needed.

## Files created or updated

- `Reproducibility Packet/results/capacity_sweep_analysis/stage1-run-2/capacity_sweep_analysis.json`
  - created by the one authorized C7 invocation; exact state above.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  - appended Codex's authorization half, forward census correction, execution record, owner
    approval and Claude review handoff; additions only.
- `README.md`
  - appended one lean public milestone; banner remains Phase 2 / In Progress.
- `agents/Codex/README.md`
  - updated navigation and live review state; added this report and the C7 artifact.
- `agents/Codex/Summary of Only Necessary Context.md`
  - completely rewritten for the open Claude artifact review gate.
- `agents/Codex/Session Summaries/HumanReport103.md`
  - this report.

No script, test, plan, sweep result, checkpoint, protocol, data file, configuration or prior
public log entry was edited. `.gitignore` already excludes the session lock, model payloads,
caches and local data while allowing the new JSON artifact, so no ignore change was needed.

## Next steps

1. Claude independently audits artifact blob `3c963059...` / SHA-256
   `e381d12e...42736` and either explicitly approves those same bytes or returns a corrected
   state.
2. If the exact-state loop closes, both agents apply frozen section 5.4 jointly in a separate
   transcript turn. Do not infer the prose from the label before that act.
3. Capacity selection and any Stage-2 action remain separate joint decisions after the
   interpretation; neither is licensed by C7.
4. Preserve both plans, both run roots, the C7 artifact, all 55 checkpoints and absent final
   `config.json`.
5. The packet README still needs the capacity-sweep/C7 runbook and authenticated clean-machine
   checkpoint recovery path during Phase 3; do not fold that obligation into this review.
