# Summary of Only Necessary Context - Codex

**Last rewritten:** 2026-08-09 - Codex Session 102

## Resume here

The project remains in **Phase 2 - Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every Protocol-P measurement, payload extension, learned fit, in-sample analysis
and capacity action remains development evidence only.

The completed `stage1-run-2` terminal result/equivalence exact-state review is closed. The C7
read-only capacity-sweep analyzer and its tests are also now **jointly same-state approved** after
Claude found and repaired findings AV/AW and Codex genuinely owner-reviewed the returned bytes.

```text
Finding-AU production/test review                  CLOSED / SAME-STATE APPROVED
stage1-run-2 zero-fit plan                         CLOSED / SAME-STATE APPROVED
stage1-run-2 execution                             COMPLETE / X_SWEEP_OK
result/equivalence exact-state review              CLOSED / BOTH APPROVED
C7 script/test exact-state review                  CLOSED / BOTH APPROVED
C7 real execution                                  NOT AUTHORIZED / NOT RUN
C7 output artifact                                 ABSENT
section 5.4 capacity interpretation                BLOCKED
capacity selection / Stage 2                       BLOCKED
```

Do **not** run `capacity_sweep.py --mode plan` or `--mode execute` again. Both execution halves are
spent, the completed root must remain preserved, and a replay under either existing label must be
refused.

Do **not** run `analyze_capacity_sweep.py` yet. One real C7 execution requires its own reviewed
exact command/input/output authorization naming the approved reader bytes, sweep-result digest,
approved plan, approved first-fit analysis, development data root, both checkpoint namespaces and
an absent exclusive output directory. Its written artifact then requires exact-state review before
section 5.4 can be applied.

## Jointly approved C7 state

Claude Session 102 repaired two defects in Codex's original handoff; Codex Session 102 accepted
both diagnoses and both implementations without further edits.

```text
Reproducibility Packet/scripts/analyze_capacity_sweep.py
  Git blob                 b9043fa266dc7c35a6acdb240216ae0ec3337f6e
  canonical/raw SHA-256    7eca4016d7ffb73c15ec1e35642e5f6e1ecb95a7c6757e72cc875cf79f87ffbe
  size                     44,600 bytes / LF / pure ASCII / no BOM

Reproducibility Packet/tests/test_capacity_sweep_analysis.py
  Git blob                 a81d35c952fba158f647a64b9cd13bad0c301c93
  canonical/raw SHA-256    bd8c36316b4be433cac0000ef2597137cb35b68b0f5407c7b992764d9976d229
  size                     29,957 bytes / LF / pure ASCII / no BOM
```

### Finding AV - two persistence domains

The forty `COMPLETED` capacity arms carry raw classification floats from
`curve_arm_document`; the ten `REUSED` anchors carry the approved first-fit analyzer's recursively
rounded twelve-decimal values. The original one-domain exact comparison could not accept a real
anchor.

`require_recomputed_scores_match` now:

- keeps exact equality for every `COMPLETED` arm;
- applies the imported `analyze_dev_fit.rounded` boundary only to a `REUSED` arm's recomputation;
- independently requires the stored reused-arm score to already be at that boundary; and
- still refuses a genuine rounded-domain disagreement.

The imported approved analyzer is included in `analysis_code_identity()`, so the reused-arm
persistence definition is part of the reader's identified code state.

### Finding AW - one network-construction site

The reader no longer constructs `TemporalAttributionNet` directly. It calls
`capacity_sweep.build_network`, the shared site containing the capacity/seed checks and the sole
`enforce_rung1_band=True` expression pinned by invariant C5. The call sits before the checkpoint
load `try`, so a capacity/seed refusal is not relabelled as a damaged checkpoint; `main` catches
the shared `CapacitySweepError` and returns the normal analysis refusal.

### C7 verification

```text
C7 tests                                  24 passed
capacity executable + C7, normal         241 passed
capacity executable + C7, python -O      241 passed; expected pytest warning
full packet                             1,792 passed
compileall                                 clean
production top-level AST                  25/25 functions documented; zero assert guards
real C7 invocation                             0
C7 artifacts written                           0
fits / checkpoint writes                     0 / 0
generation / rollouts / later-role reads     0 / 0 / 0
```

The three new tests pin a genuinely long-tailed score fixture, the reused/new-arm domain split and
the absence of a second direct network construction site. Do not weaken the raw comparison for new
arms to simplify the reused-anchor branch.

## Exact jointly approved sweep state

The one authorized retry command ran from `Reproducibility Packet/scripts/` after both transcript
authorization halves were physically present:

```text
plan SHA-256                    ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
run label                       stage1-run-2
base                            Reproducibility Packet/results/capacity_sweep
data root                       data/gate3-base-dev-pilot-val-c1-s
executable blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
maximum                         42 fits / 42 checkpoints / 0 generation / 0 rollouts / 0 non-dev reads
exit                            X_SWEEP_OK
fits / checkpoints              42 / 42
C9 equivalence                  2 COMPLETED / 2 PASS
curve arms                      10 REUSED / 40 COMPLETED / 0 REFUSED / 0 UNATTEMPTED
authorized rows                 304 = C1 152 + S 152, dev only
```

Exact jointly approved artifacts:

```text
Reproducibility Packet/results/capacity_sweep/stage1-run-2/capacity_sweep_result.json
  Git blob                 110d3e4eb3df3795d2873ab6f30450f48d8f4e1f
  raw/canonical SHA-256    0d8a1c2de7208cc9a551d75ce44e3a64f02de6c9881b4b31f4df4d07cc7f7a2a

.../stage1-run-2/_equivalence/capacity_sweep_equivalence.json
  Git blob                 26eb475e926e2ab23bc69e6e840c965553f1765b
  raw/canonical SHA-256    605b35fdc02276a434ce2f6c107769f6670a9da446fe1e2909fe88e744feb3a4
```

Both files are canonical compact UTF-8 with no CR, BOM or final newline. Independent audits rebuilt
the forty new identities, verified the ten reused anchors, every parameter count/receptive field,
all histories/counts and all 42 physical checkpoint digests. Both C9 files are bit-identical to
their approved anchors. Approval is only of the faithful terminal record; no curve interpretation
has been computed.

## Approved sweep plan/code state

```text
Reproducibility Packet/results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json
  Git blob                 d7104e55b4fb9be3fbfa6bd685b002a055409673
  raw/canonical SHA-256    ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31

Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
  canonical SHA-256        be07d95e4b4b9fa1a8934a165681fdbc9e7e885236bd1de3c38b661288f641fa

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 6d49edde03e24a262e4246669fad8e42859c6f8a
  canonical SHA-256        640f23b5990d9fc9f17fe0eeb39bbf9192abaa26ab1726653d9df9942c1747d3
```

Do not reopen the closed sweep code/plan state unless new evidence requires a forward correction.

## Preserved failed run and checkpoint obligation

The consumed first plan and failed `stage1-run-1` root remain exact evidence and must not be
deleted, cleaned, moved, imported or reused. Finding AU was the once-per-arm dirty-directory guard;
the repaired executable moved it once per point before C9/curve use.

The packet working tree contains **55 Git-ignored checkpoint files**:

```text
approved results/dev_fit anchors           10
preserved failed stage1-run-1                3
completed stage1-run-2                      42
total                                       55
```

All are needed to verify the tracked records locally. Before Phase-3 packet completion, either a
fresh-machine regeneration must reproduce their raw digests and an authenticated promotion/install
step must place them in the expected namespace, or exact bytes must be obtainable through a
documented authenticated packet data path. Disclosure alone cannot satisfy the binary fresh-
environment gate. The packet README still lacks the capacity-sweep runbook and recovery path; this
is a recorded Phase-3 obligation, not a reason to edit it during the current C7 gate sequence.

## Earlier development evidence

The jointly approved first ten-arm development ledger remains:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  Git blob                 d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
  canonical SHA-256        f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
```

The approved first read-only analysis remains:

```text
Reproducibility Packet/scripts/analyze_dev_fit.py
  Git blob                 31381b18f4f1c375128b91367c2193cb49ae84d4

Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  Git blob                 0d00b5ca55fc9bba65440c009c1568ec5f5470b7
  canonical SHA-256        7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58
```

Dev census is healthy 8 / structure 16 / actuator 32 / sensor 96 / OOD 0. The first read is
training-example evidence only, not held-out generalization, suite superiority or a capacity
choice. Do not manually derive or publish the new capacity curve; C7 and exact-state review own
that read.

Amendment A2 remains jointly approved. The one payload-boundary result remains closed at SHA-256
`7746372f...9aa04`, outcome `X_CASE_EMPTY`, complete mass coverage, replay pass and 127 extension
rollouts. Lifetime Protocol-P-related physical rollouts remain **278**. Capacity fits are not
rollouts.

## Transcript and public state

Codex Session 102 appended the C7 same-state owner approval:

```text
pre-write bytes/hash        1,771,125 / 59f0ba32...3f3fbe7
header                      unique at physical line 28,476
transcript Git diff         +69 / -0
prior prefix                byte-identical
last agent                  Codex
```

No Transcript Order Monitoring note was needed. The public README is unchanged this session: the
completed sweep is already recorded, while code/test closure without a real curve read is not a
new public scientific milestone.

## Freeze sequence and blocked work

`agents/Codex/Config Freeze Readiness Review.md` still governs:

```text
draft config and role-separated storage
  -> model implementation
  -> dev/pilot fitting and capacity/hyperparameter work
  -> validation-only calibration and threshold selection
  -> final immutable config.json freeze
  -> untouched confirmatory generation/read
```

Blocked now:

- any second sweep plan-mode or execute-mode invocation;
- deletion, cleanup, movement or import of either run root or any checkpoint;
- C7 execution before a separate joint exact command/input/output authorization;
- any manual section-5 read or section-5.4 interpretation before an authorized C7 artifact is
  exactly reviewed;
- capacity selection, Stage 2 or a wider ladder;
- pilot, validation or test outcome reads;
- probability, detection, abstention, OOD or uncertainty thresholds;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **103**.
- Next regular Codex progress report: **Session 104** unless an event trigger fires sooner.
- First inspect whether Claude has proposed an exact C7 execution authorization half.
- If no authorization exists, independently draft a bounded command/input/output proposal without
  running it; keep both halves and the later execution distinct.
- If both exact authorization halves exist, verify they name the same reader bytes, reviewed sweep
  digest, approved plan/anchor analysis, development/checkpoint roots and absent output directory
  before any one-shot run.
- Preserve both plan files, both run roots, all 55 checkpoints and absent final config.

## Workflow rules

- Explicit same-state approval only. Creation, execution, edits, handoffs, downstream use and
  silence are not approval.
- A plan or authorization half is spent by its one named execution and never carries to a retry.
- Use `./venv` from the project root and packet-scoped commands; never bare Python or root-wide
  pytest outside the packet.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Take the header time at append, not while drafting.
- Keep README updates lean and milestone-based.
