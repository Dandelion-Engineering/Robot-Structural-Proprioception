# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-08 — Codex Session 94

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every development screen/read-back, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2, the first Gate-4 fit and the capacity work remain development evidence
only.

The capacity-escalation v0.1 design and Route-A executable/test pair are now jointly approved.
Codex Session 94 accepted Claude Session 94's low-severity AS single-directory-definition
repair unchanged, closing Step 2 at:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 937ab73c960ac4d5e6ffcbcd1c869f071c47a8b5
  canonical/raw SHA-256    9ceb1298bad4247086d42d9fd08a01e1460647af91603a3391e5f4347fbfe489
  physical state           95,248 B / 2,222 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 0a8f8b71fccae95d9e0648bc45bea14902d9cb14
  canonical/raw SHA-256    dbee9c98e786a5cd2a5adaf189b3b56d95a76bf5710d31011dc33581a6535a19
  physical state           82,127 B / 2,019 lines / LF / no BOM / 204 tests
```

After exact executable closure, Codex ran the single zero-fit Step-3 plan invocation. The
official plan now exists:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 d2584d28f8ecc1d82d24d4480cee9ff7481611a9
  canonical/raw SHA-256    740d5db96657c7a5e9a86b49816daf091439e7661a6bd971fb8ce6ab3ae1c00e
  physical state           13,786 B / one canonical JSON record / no BOM /
                           no CRLF / no terminal newline
  approval                 Codex Session 94 explicitly approves exact bytes
```

**Claude's independent exact-state plan review is the next and only immediate gate.** Claude
must genuinely open this artifact and approve/block these exact bytes. `X_PLAN_OK`, creation,
Codex's audit, downstream use and silence are not Claude approval.

**No fit is authorized.** Even identical two-agent approval would close Step 3 only. Step 4 is
a later separate joint authorization naming the exact plan digest before either C9 fit or any
of the forty curve fits may run.

## Codex Session-94 executable review

Claude independently accepted Codex Session-93 Finding AR: plan mode must keep and use the
resolved destination returned by invariant C1's protected-tree guard.

Claude then found AS. The per-capacity cleanliness guard and checkpoint writer each formatted
`channels_{channels:03d}` independently. They currently agreed, so no behavior failed, and the
guard is unreachable on the ordinary freshly claimed run-root path. The equality was still
unbound: changing only the guard's copy survived all 1,754 then-current packet tests.

Claude extracted `capacity_point_directory(channels)` and made both the guard and
`checkpoint_relative_name` consume it. The new AST/runtime test pins the one producer, both
consumers and all forty arm paths. Codex independently found two prior-state producers, read
both returned files in full, drove the new seam and accepted the repair unchanged.

The repair-before-plan judgment is settled. AS is low-severity coverage, but the next plan
binds the module digest and exact checkpoint names. Deferring the repair would make a small
cleanup invalidate an approved plan. The exact spelling pin is appropriate because design
section 7.1 makes checkpoint names contract-visible.

Claude's `HumanReport94.md` calls its pass round three while its transcript calls it round four.
This was corrected forward. The pass count did not decide closure; exact bytes and measured
behavior did.

## Verification of the jointly approved executable

```text
prior-state AST probe                 2 independent channels_ f-string producers
targeted AS regression                1 passed in 1.36 s
focused Route-A tests               204 passed in 3.70 s
focused tests under python -O       204 passed in 3.54 s
full packet suite                 1,755 passed in 125.98 s
fits / checkpoint writes             0 / 0
packet plan artifacts before Step 3  0
generation / rollouts                0 / 0
config/config.json                 absent
```

The tests read approved tracked `dev_fit_result.json` and `dev_fit_analysis.json` as
comparability/plan metadata. They read no delivered observation payload and no approved `.pt`
checkpoint. No plan ran during executable review.

## Official Step-3 plan

The one official invocation, from the packet directory, was:

```text
..\venv\Scripts\python.exe -B -m utils.capacity_sweep --mode plan \
  --run-label stage1-run-1 --output-dir results\capacity_sweep
```

It returned `X_PLAN_OK` and wrote only the exact plan artifact above.

Independent audit of the persisted JSON, without calling the plan producer, established:

```text
read-only anchors                  10 = 32 channels x C1/S x seeds 0..4
new curve arms                     40 = 16/24/40/48 x C1/S x seeds 0..4
C9 equivalence arms                 2 = (C1, 0), (S, 4)
distinct declared output paths     44 = 40 curve + 2 C9 + C9 artifact + run artifact
code identities                     9 = eight approved historical + capacity_sweep.py
maximum budget                42 fits / 42 checkpoints / 0 rollouts /
                              0 generations / 0 non-dev reads
```

The forty new identities equal the full cross-product, exclude 32-channel fits and have no
duplicates. Every path is below `results/capacity_sweep/stage1-run-1/`; no host path, parent
traversal or UNC spelling is serialized. C9 target digests match their read-only anchors.

A separate audit recomputed all nine current code-identity digests and the frozen design,
approved ledger and approved analysis digests from tracked files. All match. The raw plan bytes
are strict sorted canonical JSON.

Resource state after Step 3:

```text
fits / checkpoint writes        0 / 0
official plan artifacts         1
result / equivalence artifacts  0 / 0
observation payload reads       0
approved checkpoint reads       0
pilot / validation / test reads 0 / 0 / 0
generation / rollouts           0 / 0
lifetime Protocol-P rollouts    278 unchanged
config/config.json              absent
```

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
dependencies, including private `_stack`. The module is the ninth code identity.

C9 runs `(C1, seed 0)` and `(S, seed 4)` at 32 channels inside the claimed run's reserved
`_equivalence/` subtree. Produced weights and all twenty per-epoch losses must be bit-identical
to approved checkpoints/ledger rows. Reading or fitting them is not yet authorized.

Execute mode takes a base and derives `<base>/<run_label>/`, atomically claims an absent root
and refuses every pre-existing file/directory at `X_RUN_ROOT_OCCUPIED`. Pre-root and occupied-
root refusals persist in sibling UUID sinks. Same-label replay under the same base collides;
another base/copied workspace remains a governance residual, not local replay prevention.

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

Lifetime Protocol-P-related physical rollouts remain **278**: 151 before the extension plus
its one authorized 127-rollout invocation. That invocation is spent.

## Transcript and public state

Session 94 appended two verified additions-only turns to the Phase-2 transcript:

```text
session-start bytes       1,619,145
session-start lines       25,918
session-start SHA-256     25a8926b0ced660810703e31d8ffc86b7e15e4d9ea167db0400aa86024865d14
executable header line    25,920; unique and after boundary
plan header line          26,000; unique and after its boundary
final bytes               1,626,311
final lines               26,076
final SHA-256             f2781d5999cb24a255c6663d0fc03816669517c778820de05fc0aa21743581c7
diff                      +158 / -0
last agent                Codex
```

Each pre-write byte prefix remains exact. No Transcript Order Monitoring note was required.
The Session-82 recurrence remains preserved/corrected forward; physical tail is authoritative.

The root README banner is 2026-08-08 and carries one lean entry covering exact executable
closure and the official plan's still-open second review. The packet README remains unchanged
until the plan loop closes and the public runnable surface can advance honestly.

## Public and authorization boundary

Absent separate explicit authorization, all remain blocked:

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

- Next Codex session number: **95**.
- First inspect Claude's exact review of plan blob `d2584d28...` if present.
- If Claude approves unchanged, Step 3 is jointly closed; do not infer Step-4 authorization.
- If Claude edits or blocks, genuinely review the exact new state and preserve the open gate.
- Codex Session 96, not 95, owes the next regular progress report.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence are
  not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Keep README updates lean and milestone-based.
