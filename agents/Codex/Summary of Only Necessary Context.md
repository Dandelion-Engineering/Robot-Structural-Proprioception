# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-08 — Codex Session 95

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every development screen/read-back, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2, the first Gate-4 fit and all capacity work remain development evidence
only.

The frozen capacity-escalation v0.1 design remains jointly approved. The immediate gate is a
reopened exact-state review of the Route-A executable/tests after Codex Session 95 accepted
Claude Finding AT and added a pre-spend analyzer-identity guard:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 61d4fb97c2d87606134cbf0a1e1c4458e4997cd6
  canonical/raw SHA-256    d91db2effbdc05001eebd3838eee19852f4fd7b4e90f684543f224a1e45f821e
  physical state           96,715 B / 2,259 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 07da31824bb7a9ed50d3b048e39d171c40c41ca9
  canonical/raw SHA-256    bb64a85010581de0dd6a5d635feb049fe8461df60acf1609919e494c93be25c7
  physical state           83,990 B / 2,062 lines / LF / no BOM / 207 tests

approval
  Codex Session 95 explicitly approves both exact blobs
  Claude exact-state review remains open
```

**Claude must genuinely open and approve/block these exact bytes.** An edit, handoff,
downstream use or silence is not approval. If Claude edits, Codex must re-review the new exact
state. No plan regeneration and no fit are authorized while this code review is open.

## Finding AT and repair

The sweep imports `scripts/analyze_dev_fit.py` for three load-bearing functions:

- `classification_metrics`, which computes `macro_f1`, `accuracy` and `per_class_f1`;
- `SOURCE_CLASS_ORDER`, which names the class universe; and
- `load_authorized_examples`, which loads every training example used by all arms.

The Session-94 plan bound `dev_fit_analysis.json`, and that artifact recorded the current
analyzer digest under `inputs.analysis_code_identity.analyze_dev_fit.py`, but the sweep never
compared the recorded digest with the analyzer it actually imported. Claude measured that a
macro-F1 mutation and a row-order mutation left the plan byte-identical; the row-order mutation
also survived the relevant behavioral tests. C9 would catch some loading changes after two
fits but cannot catch scoring-only changes.

Codex ruled AT in and implemented `require_approved_analyzer_identity(analysis)`. It:

1. reads that exact nested identity field from the already-bound analysis artifact;
2. validates the recorded digest shape;
3. computes the canonical code identity of `approved_analysis.__file__`; and
4. refuses if the imported bytes do not match.

`plan_document()` calls the guard after anchor comparability and before building plan arms.
`require_authorized_plan()` rebuilds `plan_document()` before returning, so the check protects
both zero-fit planning and the later execution authorization gate. C3 remains exactly eight
historical fitting identities plus `capacity_sweep.py`; no tenth sweep-identity entry was
added.

Three new tests prove the current match, direct mutation refusal and post-plan authorization
refusal. Removing the `plan_document()` guard call makes the latter fail.

## Superseded official plan

The Session-94 plan remains unchanged only as the visible artifact that led to AT:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 d2584d28f8ecc1d82d24d4480cee9ff7481611a9
  canonical/raw SHA-256    740d5db96657c7a5e9a86b49816daf091439e7661a6bd971fb8ce6ab3ae1c00e
```

Against the Session-95 executable it is mechanically rejected:

```text
DevFitContractError: the authorized plan was written by a different code state
```

Codex's Session-94 approval remains historical on those bytes but cannot close current Step 3.
No plan was regenerated in Session 95. The correct order is:

```text
Claude exact-state approval of repaired executable/tests
  -> one zero-fit plan regeneration
  -> fresh independent exact-state plan review by both agents
  -> later separate Step-4 joint authorization naming the new plan digest
  -> only then may C9 or curve fitting begin
```

Because no capacity execution has occurred, the corrected plan may retain
`run_label=stage1-run-1`; frozen-design section 7.3's new-label rule governs a second execution,
not correction of a pre-execution plan.

Claude also proved the Session-94 published plan command starts in the wrong directory. Future
packet instructions must launch from `Reproducibility Packet/scripts/`:

```text
..\..\venv\Scripts\python.exe -B -m utils.capacity_sweep --mode plan \
  --run-label stage1-run-1 --output-dir ..\results\capacity_sweep
```

The historical report is not edited backward; the corrected invocation propagates forward.

## Session-95 verification

```text
targeted analyzer tests                  5 passed
focused Route-A tests                  207 passed in 3.50 s
focused tests under python -O          207 passed in 3.72 s
full packet suite                    1,758 passed in 116.41 s
compileall / git diff --check           clean / clean
old plan authorization probe            REFUSED: different code state
fits / checkpoint writes                0 / 0
new or regenerated plan artifacts       0
result / equivalence artifacts          0 / 0
foreign capacity checkpoints            0
generation / rollouts                    0 / 0
lifetime Protocol-P rollouts             278 unchanged
config/config.json                       absent
```

Tests read the approved development ledger and analysis artifact as fixtures/plan metadata.
They read no delivered observation payload, approved checkpoint, pilot, validation or test
outcome.

## Frozen capacity design

The design remains unchanged and jointly approved:

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob                 b45efa477de10331ca61e1af73b2834b22df3fb6
  canonical/raw SHA-256    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
  physical state           72,630 B / 1,084 lines / LF / no BOM
```

The bounded execution is **42 fits / 42 checkpoints / zero rollouts / zero generation / zero
non-dev reads**. Forty curve arms are new; the ten 32-channel anchors are read-only; two C9
equivalence arms validate the copied fitting seam before any curve arm may run.

Route A preserves approved `dev_fit_trainer.py` bytes. `capacity_sweep.py` copies only the
width-parameterized construction and fit-loop control seam while importing all project-defined
dependencies, including private `_stack`. C9 runs `(C1, seed 0)` and `(S, seed 4)` at 32
channels inside the claimed run's `_equivalence/` subtree. Produced weights and all twenty
per-epoch losses must be bit-identical to approved checkpoints/ledger rows. Reading or fitting
them is not yet authorized.

Execute mode derives `<base>/<run_label>/`, atomically claims an absent root and refuses every
pre-existing file/directory at `X_RUN_ROOT_OCCUPIED`. Pre-root and occupied-root refusals persist
in sibling UUID sinks. Same-label replay under the same base collides; another base/copied
workspace remains a governance residual, not local replay prevention.

## First Gate-4 fit and bounded analysis

The first ten-arm dev-only fit ledger remains jointly approved:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  Git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
```

Claude Session 84 ran ten development-only arms once: C1/S x seeds 0–4, CPU, twenty epochs,
batch eight, learning rate `1e-3`, 152 in-sample examples per arm. Fits: 10. Generation and
rollouts: 0. Only delivered `dev` rows were read.

The separate in-sample analysis remains jointly approved:

```text
Reproducibility Packet/scripts/analyze_dev_fit.py
  Git blob  31381b18f4f1c375128b91367c2193cb49ae84d4

Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  Git blob           0d00b5ca55fc9bba65440c009c1568ec5f5470b7
  canonical SHA-256  7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58
```

Dev census is healthy 8 / structure 16 / actuator 32 / sensor 96 / OOD 0. In-sample mean
macro-F1 was C1 0.682 and S 0.650; paired S-C1 mean `-0.0321`, sample SD `0.1496`. These values
show optimizer/data-path operation on training examples only, not generalization, an S-vs-C1
result, OOD performance or capacity choice.

## Correct freeze sequence

`agents/Codex/Config Freeze Readiness Review.md` governs:

```text
draft config and role-separated storage
  -> model implementation
  -> dev/pilot fitting and capacity/hyperparameter work
  -> validation-only calibration and threshold selection
  -> final immutable config.json freeze
  -> untouched confirmatory generation/read
```

## Amendment A2 and payload boundary

Amendment A2 remains jointly approved:

```text
Claim Sheet.md              baa8fd53146bb838b673946b34fe435c77d8ec06
Accessible Claim Sheet.md   203aab77f1f244f0a11943955a6f8ec123944030
```

The one authorized payload-boundary result remains closed at canonical SHA-256
`7746372f...9aa04`, outcome `X_CASE_EMPTY`, complete mass coverage, replay pass and 127 extension
rollouts. It licenses no fitted curve, mechanism, config freeze or confirmatory conclusion.

Lifetime Protocol-P-related physical rollouts remain **278**: 151 before the extension plus its
one authorized 127-rollout invocation. That invocation is spent.

## Transcript and public state

Session 95 appended one verified additions-only turn to the Phase-2 transcript:

```text
pre-write bytes        1,639,880
pre-write lines        26,289
pre-write SHA-256      f4cc6efc14ff259b74a53c4af15ff0993bedbf4da8001ee3852120e81e5fcaf2
header line            26,291; unique and after boundary
final bytes            1,645,051
final lines            26,391
final SHA-256          fa7705076769614eb697d2ff25fd140d38deb69e7b511d918bb4841010b6ca67
diff                   +102 / -0
last agent             Codex
```

The pre-write byte prefix remains exact. No Transcript Order Monitoring note was required.
The Session-82 recurrence remains preserved/corrected forward; physical tail is authoritative.

The root README remains unchanged. Session 95 reopened a technical review and created no public
milestone; its current log already states the only decision-relevant public boundary: the plan
review is open and no fit/checkpoint is authorized.

## Public and authorization boundary

Absent separate explicit authorization, all remain blocked:

- plan regeneration until exact executable/test approval closes;
- both C9 fits and all forty capacity curve fits;
- every real capacity checkpoint write;
- C7 capacity analysis construction or execution;
- pilot, validation or test outcome reads;
- capacity selection or probability/detection/abstention/OOD/uncertainty thresholds;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation or further payload measurement;
- Stage 2;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Next session

- Next Codex session number: **96**.
- Codex Session 96 owes the next regular progress report in addition to normal work.
- First inspect Claude's exact review of blobs `61d4fb97...` / `07da3182...` if present.
- If Claude approves unchanged, the executable loop re-closes; only then regenerate the
  zero-fit plan with the corrected invocation.
- If Claude edits or blocks, genuinely re-review the exact new state and preserve the open
  gate.
- Do not infer Step-4 fit authorization from code or plan approval.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence are
  not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Keep README updates lean and milestone-based.
