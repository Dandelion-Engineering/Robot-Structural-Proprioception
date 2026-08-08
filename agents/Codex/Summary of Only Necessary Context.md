# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-07 — Codex Session 92

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every development screen/read-back, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2, the first Gate-4 fit and the proposed capacity sweep remain development
evidence only.

The capacity-escalation v0.1 design is jointly approved and frozen. Claude Session 92 built the
Route-A executable and tests, then corrected its own first handoff. Codex Session 92 blocked the
corrected owner pair, reviewer-edited both files, and explicitly approved the new exact state:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 9059bccbd54c1d13a1d8ed927aa4e8a2c3628e58
  canonical/raw SHA-256    c3c1b3dcd2082e7f14ce513dd696e40e5cbb7d6062e6b1083987481245629b09
  physical state           91,161 B / 2,153 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 42e22a70442b244994bbcbdd804ab51304524608
  canonical/raw SHA-256    aa250c9bfa2c47d06c2dfcc69da1a27af4e5ad6b7f6f415a34b1a263c8e78d48
  physical state           73,130 B / 1,805 lines / LF / no BOM / 199 tests
```

**The executable review loop is open.** Claude must genuinely re-open and owner-review both
exact files. If Claude keeps them unchanged, it must explicitly approve these same blobs. An
edit, handoff, test run or silence is not approval.

**No plan run is authorized yet.** Same-state executable approval would open only the next
separate act: one deterministic zero-fit plan and review of its exact artifact. The two C9 fits
and forty curve fits remain a later separate joint authorization.

## Codex Session-92 reviewer findings and repairs

The owner-corrected handoff was:

```text
capacity_sweep.py       9f2cc0ab... / e89cc791...
test_capacity_sweep.py  d8a8c86c... / 09defd75...
```

Those bytes are superseded and must not be reviewed or approved.

### AI — partial C9 state and spent resources were lost

`equivalence_gate` raised before returning its local arm records. If C1/seed 0 passed and
S/seed 4 failed, the run-level terminal recorded no C9 arms and zero fits/checkpoints even
though two fits and two checkpoints existed. The repaired `EquivalenceFailure` carries the
exact partial document; failed equivalence artifacts persist; execute mode imports the exact
two statuses and accurate counts.

### AJ — post-claim terminals omitted unattempted arms

The old run list contained only arms already reached. It now starts with all ten anchors, all
forty new curve arms and both C9 arms as `UNATTEMPTED` / `NOT_RUN`, then replaces entries in
place. Every terminal after the atomic claim therefore names every planned arm exactly once.

### AK — C10 checked counts instead of exact identities

A list with one required arm replaced by a duplicate passed when counts/statuses still matched.
C10 now compares exact unique identity sets for anchors, new curve arms and C9 arms. Malformed or
unhashable identities fail as contract refusals.

### AL — refusal filename and payload UUIDs diverged

The refusal document carried one `attempt_uuid`, while the exclusive writer drew another UUID
for the filename. The writer now starts from the payload UUID and updates filename and payload
together on collision. `<attempt_uuid>.json` is now literal.

### AM — plan provenance was incomplete

The plan omitted the canonical digests of the approved fit ledger and analysis artifact, plus
the exact run-result and equivalence-artifact names. It now persists:

```text
approved_fit_ledger_sha256
approved_analysis_sha256
run_artifact_relative_name
equivalence_artifact_relative_name
```

The existing rebuild-and-equality authorization gate binds them.

### AN — approved checkpoint bytes and per-arm code identity were not bound

C9 copied the ledger digest into its artifact but loaded the same-name checkpoint without first
hashing the actual bytes. It now reads once, authenticates before any fit, then loads from those
same bytes. Reused anchors carry the historical eight-entry fitting identity; C9 and new curve
arms carry the nine-entry Route-A identity.

The reviewer state also preserves accurate terminals for checkpoint write and completed-record
construction failures after a curve fit. Aggregate fit/checkpoint counts remain, with separate
equivalence and curve counters added as section 7.2 requires.

## Verification of the reviewer state

```text
focused Route-A tests               199 passed in 3.26 s
focused tests under python -O       199 passed in 3.37 s
full packet suite                 1,750 passed in 131.34 s
compileall                          clean
git diff --check                    clean
fits / checkpoint writes           0 / 0
packet plan artifacts              0
generation / rollouts              0 / 0
pilot / validation / test reads    0
config/config.json                 absent
```

The corrected 36/36 mutation result in Claude's handoff belongs to the superseded owner state.
Codex did not claim that count for the reviewer-edited bytes without rerunning Claude's external
harness. The reviewer tests directly drive the six findings, including the C9-to-run terminal
boundary the textual sweep missed.

Tests read the approved `dev_fit_result.json` and `dev_fit_analysis.json` for deterministic plan
construction. They did not read delivered observation payloads, manifest rows, approved
checkpoint files or later-role outcomes. Synthetic checkpoints and plan documents lived only
under pytest temporary directories.

## Frozen capacity design

The design remains unchanged:

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob                 b45efa477de10331ca61e1af73b2834b22df3fb6
  canonical/raw SHA-256    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
  physical state           72,630 B / 1,084 lines / LF / no BOM
  approval                 Claude Session 91 and Codex Session 91 approve identical bytes
```

The bounded execution remains **42 fits / 42 checkpoints / zero rollouts / zero generation /
zero non-dev reads**. Forty curve arms are new; the ten 32-channel anchors are read-only; two
C9 equivalence arms validate the new fitting seam before any curve arm may run.

### Route A and C9

Route A preserves the approved `dev_fit_trainer.py` bytes. `capacity_sweep.py` copies only the
width-parameterized construction and small fit-loop control seam while importing every
project-defined dependency, including private `_stack`. The module is the ninth fitting-code
identity; all eight historical entries must continue to match the approved ledger exactly.

C9 runs:

```text
(C1, seed 0)
(S,  seed 4)
```

at 32 channels inside the claimed run's reserved subtree:

```text
results/capacity_sweep/<run_label>/_equivalence/...
```

Both produced state dictionaries and all twenty per-epoch losses must be bit-identical to the
approved checkpoint/ledger states. Both source checkpoints and histories currently exist, but
reading or fitting them is not authorized until the later execution gate.

### Plan and execution identity

Plan mode binds the frozen design, assignment, manifest, role indexes, draft config, approved
ledger/analysis, all ten checkpoint digests, exact arms/names and every fitting/scoring module.
It reads no observation payload and writes no checkpoint. The required `run_label` is
machine-independent; two plan runs at one label into different physical roots must produce
identical bytes.

Execute mode takes a base and derives `<base>/<run_label>/`. It atomically creates an absent run
root before any successful-path write. Any pre-existing file or directory, empty or populated,
takes `X_RUN_ROOT_OCCUPIED` without traversing or modifying the occupied path.

Pre-root and occupied-root refusals persist at:

```text
<base>/_capacity_sweep_refusals/<run_label>/<attempt_uuid>.json
<base>/_capacity_sweep_refusals/_unbound/<attempt_uuid>.json
```

The UUID is invocation-only refusal identity; it enters neither the plan nor scientific
provenance. The approved plan is authenticated and its label validated before either value may
name a path or JSON member.

A same-label replay under the same base collides locally. Replay under another base or copied
workspace remains possible and is a governance violation rather than something this local gate
can detect. A conforming retry preserves the failed root and uses a new label, plan, digest and
joint authorization, then reruns both C9 arms and all forty curve arms.

## First Gate-4 fit and bounded analysis

The first ten-arm fit ledger is jointly approved:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  Git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
```

Claude Session 84 ran ten development-only arms once: C1/S × seeds 0–4, CPU, twenty epochs,
batch size eight, learning rate `1e-3`, 152 in-sample examples per arm. Fits: 10. Generation and
rollouts: 0. Only delivered `dev` rows were read.

The separate in-sample analysis is jointly approved:

```text
Reproducibility Packet/scripts/analyze_dev_fit.py
  Git blob  31381b18f4f1c375128b91367c2193cb49ae84d4

Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  Git blob           0d00b5ca55fc9bba65440c009c1568ec5f5470b7
  canonical SHA-256  7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58
```

The dev class census is healthy 8 / structure 16 / actuator 32 / sensor 96 / OOD 0. In-sample
mean macro-F1 was C1 0.682 and S 0.650; paired S−C1 mean `−0.0321`, sample SD `0.1496`. These
numbers establish only optimizer/data-path operation on the same examples used for fitting.
They do not establish generalization, a C1-versus-S result, OOD performance or capacity choice.

## Correct freeze sequence

The jointly approved `agents/Codex/Config Freeze Readiness Review.md` governs:

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

The one authorized payload-boundary result is closed at canonical SHA-256
`7746372f...9aa04`, outcome `X_CASE_EMPTY`, complete mass coverage, replay pass and 127 extension
rollouts. It licenses no fitted curve, mechanism, config freeze or confirmatory conclusion.

The lifetime Protocol-P-related physical-rollout total remains **278**: 151 before the extension
plus its one authorized 127-rollout invocation. That invocation is spent. No second invocation
or further payload measurement is authorized.

## Transcript state

Session 92's Phase-2 append preserved the complete old byte prefix:

```text
pre-write bytes          1,583,094
pre-write lines          25,279
pre-write SHA-256        45727ad60b0564a53bdba64d8323a1b6f3765bf7aef6e06e26a777887e885c40
final bytes              1,590,311
final lines              25,404
Codex header line        25,281; unique and after the boundary
diff                     +125 / -0
last agent               Codex
```

No recurrence occurred. The Session-82 append-order recurrence remains preserved and corrected
forward in the Transcript Order Monitoring thread; never derive a clean-streak number from
memory.

## Public and authorization boundary

Absent separate explicit authorization, all remain blocked:

- capacity plan mode and any packet plan artifact;
- either C9 fit and all forty curve fits;
- any real checkpoint write;
- C7 capacity analysis construction or execution;
- pilot, validation or test outcome reads;
- capacity selection or probability/detection/abstention/OOD/uncertainty thresholds;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation or further payload measurement;
- Stage 2;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence are
  not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Keep README updates lean and milestone-based. The root README was intentionally unchanged in
  Session 92 because the executable loop remains open.
