# Summary of Only Necessary Context - Codex

**Last rewritten:** 2026-08-09 - Codex Session 101

## Resume here

The project remains in **Phase 2 - Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every Protocol-P measurement, payload extension, learned fit, in-sample analysis
and capacity action remains development evidence only.

The `stage1-run-2` terminal result/equivalence exact-state review is closed. Both agents explicitly
approved the same bytes. Invariant C7 is now built by Codex and handed to Claude, but its code/test
review is open. **No real C7 invocation or descriptive curve read has occurred.**

```text
Finding-AU production/test review                  CLOSED / SAME-STATE APPROVED
stage1-run-2 zero-fit plan                         CLOSED / SAME-STATE APPROVED
stage1-run-2 execution                             COMPLETE / X_SWEEP_OK
result/equivalence exact-state review              CLOSED / BOTH APPROVED
C7 script/test owner state                         CODEX APPROVED / CLAUDE REVIEW OPEN
C7 real execution                                  NOT AUTHORIZED / NOT RUN
section 5.4 capacity interpretation                BLOCKED
capacity selection / Stage 2                       BLOCKED
```

Do **not** run `capacity_sweep.py --mode plan` or `--mode execute` again. Both execution halves are
spent, the completed root must remain preserved, and a replay under either existing label must be
refused. Do not run `analyze_capacity_sweep.py` until its exact code/test loop closes and a separate
execution authorization names the command, approved sweep-result digest and input/output roots.

## C7 exact state under review

Codex Session 101 created and explicitly approved:

```text
Reproducibility Packet/scripts/analyze_capacity_sweep.py
  Git blob                 5dcc094742ba76ae4d5f288a1c426c8e87acfb5b
  canonical/raw SHA-256    c33e21f547c751e46425e905ed13f85a1c27f69fb27f4bacb5c03a35fa35fe27
  size                     41,787 bytes / 1,037 lines

Reproducibility Packet/tests/test_capacity_sweep_analysis.py
  Git blob                 5e4497fd2b14ae4685a75f3306debeb4b4073a52
  canonical/raw SHA-256    1d95cdc9b297ec99eb861022b8e9bce2eb456f65ff14a31a617f2ffa05842586
  size                     25,807 bytes / 707 lines
```

The analyzer:

- imports `headroom`, `pair_constraint`, `classify_shape`, `quantize`, `derived_label` and
  `require_complete_sweep` from `utils.capacity_sweep`;
- requires an invocation-supplied exact sweep-result SHA-256;
- authenticates result, plan, frozen design, current sweep identity, approved anchor analysis,
  source fields and zero later-role/resource boundary;
- enforces C10 plus per-arm source, full fit identity, shapes, checkpoint digests and new-arm loss
  history;
- loads only authorized dev examples and the 55 named checkpoints, then independently recomputes
  all persisted classification metrics through approved definitions;
- carries section 3's loss decomposition, class census and baselines per point;
- derives only section 5.2's raw/quantized fields, constraints, crossings, shapes, paired range,
  anchor-SD comparison and pure label;
- writes compact canonical UTF-8 JSON exclusively, with no final newline; and
- records zero fits, generation, rollouts and non-development reads.

Tests are synthetic only. Verification on the owner state:

```text
new C7 tests, normal                    21 passed
capacity executable + C7, normal      238 passed
capacity executable + C7, python -O   238 passed; expected pytest warning
full packet                          1,789 passed
compileall                              clean
production AST                          26/26 functions documented; zero assert guards
real C7 invocation                      0
```

Claude must genuinely re-open both exact files and either approve those same bytes or return an
edited state for Codex owner re-review. Creation, testing, handoff and downstream use are not
Claude approval.

## Exact jointly approved sweep state

The one authorized retry command ran from `Reproducibility Packet/scripts/` after both transcript
halves were physically present:

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

## Approved plan/code state

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
is a recorded Phase-3 obligation, not a reason to edit it during the C7 review loop.

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

Codex Session 101 appended one C7 handoff:

```text
pre-write bytes/hash        1,752,845 / b5fe72e6...571f2133
header                      unique at physical line 28,139
transcript Git diff         +81 / -0
prior prefix                exact
last agent                  Codex
```

No Transcript Order Monitoring note was needed. The public README is unchanged this session: the
joint exact-result review closure is already reflected by Claude's lean entry, while C7 remains an
open implementation review rather than a settled milestone.

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
- C7 execution before its exact script/test loop closes and a separate authorization names the
  reviewed result digest plus all input/output roots;
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

- Next Codex session number: **102**.
- Next regular Codex progress report: **Session 104** unless an event trigger fires sooner.
- First inspect whether Claude genuinely approved both exact C7 files unchanged or returned edits.
- If Claude approves unchanged, the code/test loop closes. Treat one real C7 execution, its exact
  output review, joint section-5.4 application and any Stage-2 decision as separate gates.
- If Claude edits either file, re-open both the feedback and changed bytes, test the exact returned
  state, and explicitly approve or return a correction. Do not infer owner approval from the edit.
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
