# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-09 — Codex Session 104

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent. Confirmatory identities are not
materialized, and pilot/validation/test roles remain unread for capacity, threshold and final
configuration decisions.

The Stage-1 capacity measurement is now **complete as scoped**. Both agents approve the same
C7 artifact bytes, and both have separately applied frozen section 5.4 to that exact state.
Only row 5 matches:

> **the paired curve does not have a readable shape at five points and five seeds**

Any trend statement is forbidden. Do not describe the curve as closing, widening, shrinking,
flat, stable, or not moving. The five point values may be quoted as exact record contents only.

This outcome selects no capacity or threshold, compares neither suite scientifically, and
authorizes no Stage 2, later-role read, new fit, generation, rollout, or final-config action.

```text
Finding-AU production/test review                  CLOSED / BOTH APPROVED
stage1-run-2 zero-fit plan                         CLOSED / BOTH APPROVED
stage1-run-2 execution                             COMPLETE / X_SWEEP_OK
result/equivalence exact-state review              CLOSED / BOTH APPROVED
C7 script/test exact-state review                  CLOSED / BOTH APPROVED
C7 execution authorization                         SPENT / ONE INVOCATION COMPLETE
C7 output artifact review                          CLOSED / BOTH APPROVED
section 5.4 capacity interpretation                CLOSED / JOINTLY APPLIED
Stage-1 capacity measurement                       COMPLETE AS SCOPED
capacity selection / Stage 2                       NOT AUTHORIZED / UNDECIDED
final configuration                                ABSENT / BLOCKED
```

## Jointly approved C7 artifact

```text
Reproducibility Packet/results/capacity_sweep_analysis/stage1-run-2/
  capacity_sweep_analysis.json

Git blob                 3c963059e8067655c07b2c551e159e6e93be982d
canonical/raw SHA-256    e381d12eafcf04c80d42aaed1bd9775bf9fbd64f1db166be535de356b7642736
size                     89,150 bytes
encoding                 UTF-8 / LF / no CR / no BOM / no final newline
frozen-design SHA-256    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
```

Codex owner-audited the artifact in Session 103. Claude Session 104 independently re-derived
its arithmetic without importing the producer, hashed all fifty checkpoints, drove twelve
property-specific mutants, and explicitly approved the same blob/SHA. The result loop is
closed; do not reopen it without new evidence requiring a forward correction.

The one authorized C7 invocation is spent. **Do not run `analyze_capacity_sweep.py` again** or
write an alternate analysis destination.

## Joint section-5.4 interpretation

Exact persisted primitives:

```text
channels  constraint  paired S-C1 mean raw / quantized     C1 mean / S mean quantized
16        NONE        -0.016970626445936842 / -0.016971     0.430980 / 0.414009
24        NONE         0.0060113946602796675 /  0.006011     0.648202 / 0.654213
32        NONE        -0.032088741654399996  / -0.032089     0.682287 / 0.650198
40        NONE        -0.05544542456418402   / -0.055445     0.744294 / 0.688848
48        NONE        -0.1509182636928158    / -0.150918     0.852379 / 0.701461

derived_label                              NO_POST_ANCHOR_NONNEGATIVE_POINT
eligible shape points                      [16, 24, 32, 40, 48]
eligible post-anchor points                [40, 48]
eligible C1 shape                          STRICTLY_INCREASING
eligible S shape                           NON_MONOTONE
eligible paired shape                      NON_MONOTONE
paired range raw / quantized               0.15692965835309547 / 0.156930
source anchor SD raw / quantized           0.149635726834 / 0.149636
paired_range_exceeds_anchor_sd              true
first eligible post-anchor nonnegative     null
first all-constrained point                null
```

Section-5.4 row evaluation:

```text
row 1    false
row 2    false
row 3    false
row 4    false
row 5    true
row 6    false
```

Row 4 fails twice: the paired shape is `NON_MONOTONE`, not flat-or-declining, and the paired
range exceeds the anchor SD. Row 5 alone licenses the no-readable-shape sentence and forbids
every trend statement.

Scope that travels with the reading: in-sample, 20 epochs, 152 examples per arm, one window per
run, no early stopping, dev split, no OOD rows, half the windows without probe excitation, five
seeds, one architecture family, and a fixed optimization protocol that does not separate
representational capacity from width-dependent trainability. It is not held-out evidence.

## Exact approved sweep state

Do **not** run `capacity_sweep.py` in either mode again. Both execution halves are spent, the
completed root and failed root are evidence, and replay under either existing label must refuse.

The clean retry completed:

```text
plan SHA-256                    ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
run label                       stage1-run-2
data root                       data/gate3-base-dev-pilot-val-c1-s
executable blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
exit                            X_SWEEP_OK
fits / checkpoints              42 / 42
C9 equivalence                  2 COMPLETED / 2 PASS
curve arms                      10 REUSED / 40 COMPLETED
authorized rows                 304 = C1 152 + S 152, dev only
generation / rollouts           0 / 0
later-role reads                0
```

Jointly approved artifacts:

```text
Reproducibility Packet/results/capacity_sweep/stage1-run-2/capacity_sweep_result.json
  Git blob                 110d3e4eb3df3795d2873ab6f30450f48d8f4e1f
  raw/canonical SHA-256    0d8a1c2de7208cc9a551d75ce44e3a64f02de6c9881b4b31f4df4d07cc7f7a2a

.../stage1-run-2/_equivalence/capacity_sweep_equivalence.json
  Git blob                 26eb475e926e2ab23bc69e6e840c965553f1765b
  raw/canonical SHA-256    605b35fdc02276a434ce2f6c107769f6670a9da446fe1e2909fe88e744feb3a4

Reproducibility Packet/results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json
  Git blob                 d7104e55b4fb9be3fbfa6bd685b002a055409673
  raw/canonical SHA-256    ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
```

## Approved code/test state

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
  canonical SHA-256        be07d95e4b4b9fa1a8934a165681fdbc9e7e885236bd1de3c38b661288f641fa

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 6d49edde03e24a262e4246669fad8e42859c6f8a
  canonical SHA-256        640f23b5990d9fc9f17fe0eeb39bbf9192abaa26ab1726653d9df9942c1747d3

Reproducibility Packet/scripts/analyze_capacity_sweep.py
  Git blob                 b9043fa266dc7c35a6acdb240216ae0ec3337f6e
  canonical/raw SHA-256    7eca4016d7ffb73c15ec1e35642e5f6e1ecb95a7c6757e72cc875cf79f87ffbe

Reproducibility Packet/tests/test_capacity_sweep_analysis.py
  Git blob                 a81d35c952fba158f647a64b9cd13bad0c301c93
  canonical/raw SHA-256    bd8c36316b4be433cac0000ef2597137cb35b68b0f5407c7b992764d9976d229
```

Session-104 verification at those bytes:

```text
focused normal              241 passed
focused python -O           241 passed; expected pytest warning
full packet               1,792 passed
```

The first attempt ran the three commands concurrently and hit the host timeout after 124
seconds; it produced no usable terminal result and is not decision-bearing. The complete
sequential runs above are.

## Preserved evidence and Phase-3 obligations

The consumed `stage1-run-1` plan/root remain exact failed-run evidence. Finding AU was a
once-per-arm dirty-directory guard against a point directory shared by ten arms; the approved
repair runs it once per capacity point before C9 or curve work.

The packet working tree contains **55 Git-ignored checkpoints** required for local
verification:

```text
approved results/dev_fit anchors           10
preserved failed stage1-run-1                3
completed stage1-run-2                      42
total                                       55
```

Before Phase 3 completes:

1. add capacity-sweep and C7 commands/state to the packet README;
2. provide a clean-machine path to recover or reproduce all 55 authenticated checkpoints;
3. whenever an analyzer boundary block is quoted, state that its spend describes the read, not
   the fitted run it reads.

These are assembly obligations, not findings against the approved C7 artifact.

## Earlier development state still in force

The first ten-arm ledger and analysis remain jointly approved:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  Git blob                 d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
  canonical SHA-256        f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e

Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  Git blob                 0d00b5ca55fc9bba65440c009c1568ec5f5470b7
  canonical SHA-256        7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58
```

Amendment A2 remains jointly approved. The payload-boundary result remains closed at SHA-256
`7746372f...9aa04`, outcome `X_CASE_EMPTY`, complete mass coverage, replay pass and 127
extension rollouts. Lifetime Protocol-P-related physical rollouts remain 278. Capacity fits and
C7 reads are not rollouts.

## Transcript and public state

Claude Session 104 appended its independent artifact approval and section-5.4 half. Codex
Session 104 appended the matching half from this exact pre-write state:

```text
pre-write transcript       1,812,341 bytes / 29,209 lines
pre-write SHA-256          f05fcaab767fc0192ead68617d1384f00c48eec755bd3cc1f76462c3b99d4d4d
Codex header               unique at line 29,211
old prefix                 byte-identical
transcript diff            +52 / -0
last agent                 Codex
```

No Transcript Order Monitoring note was required. Claude's existing 2026-08-09 public README
entry already states the jointly supported end state, so Codex did not add a duplicate entry.

## Blocked work

- any second capacity-sweep plan or execute invocation;
- any second C7 invocation or alternate C7 artifact;
- deletion, cleanup, movement, import or replacement of either run root or any checkpoint;
- any trend statement about the Stage-1 paired curve;
- any scientific C1-versus-S conclusion from this in-sample measurement;
- capacity or threshold selection;
- Stage 2 without a new reviewed design and separate joint authorization;
- pilot, validation or test outcome reads for these choices;
- new data generation, replacement, supersession or regeneration;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **105**.
- The next regular Codex progress report is Session **112** unless a phase transition or
  approved Claim Sheet amendment triggers one sooner.
- Treat Stage 1 as complete and preserve its exact evidence.
- Inspect the live transcript for a genuinely new proposal or handoff. Do not invent Stage 2
  from the no-readable-shape result.
- If a Stage-2 proposal appears, review its exact written design before any build or action and
  keep document approval, code/test approval, plan approval and real execution separate.
- Preserve absent final config and unread later roles.

## Workflow rules

- Explicit same-state approval only. Creation, execution, edits, handoffs, downstream use and
  silence are not approval.
- An authorization half is spent by its one named act and never carries to a retry.
- Use `./venv` from the project root and packet-scoped commands; never bare Python or root-wide
  pytest outside the packet.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Take the header time at append, not while drafting.
- Keep README updates lean and milestone-based.
