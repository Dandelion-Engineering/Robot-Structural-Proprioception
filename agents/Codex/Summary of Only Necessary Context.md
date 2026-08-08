# Summary of Only Necessary Context - Codex

**Last rewritten:** 2026-08-08 - Codex Session 97

## Resume here

The project remains in **Phase 2 - Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every Protocol-P measurement, payload extension, first learned fit, in-sample
analysis and capacity action remains development evidence only.

The capacity design, Route-A executable/tests and corrected official zero-fit plan are jointly
approved. Step 3 is closed. The immediate gate is **Claude's independent decision on the second
Step-4 authorization half**:

```text
joint capacity design approval                COMPLETE
joint Route-A executable/test approval        COMPLETE
corrected zero-fit plan creation              COMPLETE
joint exact-state plan approval (Step 3)      COMPLETE
Codex Step-4 authorization half               ISSUED
Claude Step-4 authorization half              ABSENT
execute permission                            ABSENT
C9 and forty curve fits                       BLOCKED
```

No execute command may run until Claude physically records a matching half that names the exact
approved plan digest. One half is not authorization.

## Exact approved capacity state

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob                 b45efa477de10331ca61e1af73b2834b22df3fb6
  canonical/raw SHA-256    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002

Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 61d4fb97c2d87606134cbf0a1e1c4458e4997cd6
  canonical/raw SHA-256    d91db2effbdc05001eebd3838eee19852f4fd7b4e90f684543f224a1e45f821e

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 8e97f6a94a3c5ac12e6ac85376913c9104424725
  canonical/raw SHA-256    61f700fb4b6c51df495cdfca1c0fa0b5aacb3d9021c0c04e3cee2a72746b99e0

Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 c048b54b8081271d76a6adacf8526d201c446c17
  canonical/raw SHA-256    bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5
  physical state           13,786 B / one canonical JSON line / no final newline
```

Both agents explicitly approve the same plan bytes. Claude's Session-97 audit re-derived 413
leaves independently, found exactly one change from the superseded plan, measured plan-byte
determinism across two scratch destinations plus the published artifact, and drove the plan gate
against one valid artifact plus twenty-one neighbours. Step 3 is genuinely closed.

## Codex Step-4 half

Codex Session 97 issued one authorization half for exactly one execution of plan SHA-256
`bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5`, run label
`stage1-run-1`, in the current tree with packet-relative base `results/capacity_sweep` and the ten
pre-existing approved 32-channel checkpoints.

The maximum budget is exactly:

```text
two C9 equivalence fits
forty new curve fits       widths 16/24/40/48 x suites C1/S x seeds 0-4
checkpoint writes         42 maximum
generation                0
rollouts                   0
non-development reads      0
```

C9 must pass before any curve arm. Before the eventual command, the runner must re-check all ten
anchor digests, the unchanged plan/code state, absence of `stage1-run-1`, and absence of a
concurrent packet/root writer. Claude must independently issue the matching half first.

## Session-97 local preflight

```text
plan SHA-256                         bdf674d5...1c0a5 exact
plan/ledger/physical checkpoint      10 / 10 exact matches
all packet checkpoints               exactly those ten under results/dev_fit
foreign .pt files                    0
delivered data root                  present
stage1-run-1 root                    absent
config/config.json                   absent
full packet suite                    1,765 passed in 119.21 s
fits/checkpoints/generation/rollouts 0 / 0 / 0 / 0 this session
pilot/validation/test reads          0 / 0 / 0
lifetime Protocol-P rollouts         278 unchanged
```

## Clean-machine checkpoint obligation

Claude Session 97 correctly surfaced that the ten approved anchor checkpoints exist only as
Git-ignored files in this working tree. Execute mode reads them from the fixed packet-relative
`results/dev_fit` namespace and offers no checkpoint-directory override. The packet's current
regeneration/analyzer instructions write/read `results/dev_fit_reproduced`, so a clean reader
following the runbook still cannot run the capacity sweep.

Codex ruled:

- This is **not** a `director_requests.md` item. It needs no Randy identity, access or judgment.
- It does not block the local development measurement once both authorization halves exist; the
  current tree holds all exact approved bytes.
- It is a real agent-owned **Phase-3 Reproducibility Packet obligation**.
- Before packet completion, either fresh-machine regeneration must reproduce all ten raw digests
  and an authenticated promotion/install step must place them into `results/dev_fit`, or the exact
  approved bytes must be available through a documented authenticated packet data path.
- Disclosure alone cannot satisfy the packet playbook's binary fresh-environment gate. If neither
  route works, the packet remains explicitly incomplete for this sweep.
- Do not weaken C9 with a free checkpoint-directory flag.

## Claude Session-96 progress report

Both agents now approve the exact report:

```text
agents/Claude/Progress Reports/Progress Report Session 96.md
  Git blob                 c824173cb0d75bd7e10ca5b20567004af89a0ba7
  raw SHA-256              eeeaf53d8ef8074fb74c4b58bd4c374e88462386844154eae6246bbc3f27e157
```

Codex Session 97 approved it unchanged. It accurately explains finding AT, states the
twelve-Claude-session scientific-result gap, reports no Slot-8 change, and preserves all
reserved-data and confirmatory boundaries. The report review loop is closed.

## First Gate-4 fit and bounded analysis

The first ten-arm development-only ledger remains jointly approved:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  Git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
```

Claude Session 84 ran C1/S x seeds 0-4 once, CPU, twenty epochs, batch eight, learning rate
`1e-3`, 152 in-sample examples per arm. The read-only analysis remains jointly approved:

```text
Reproducibility Packet/scripts/analyze_dev_fit.py
  Git blob  31381b18f4f1c375128b91367c2193cb49ae84d4

Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  Git blob           0d00b5ca55fc9bba65440c009c1568ec5f5470b7
  canonical SHA-256  7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58
```

Dev census is healthy 8 / structure 16 / actuator 32 / sensor 96 / OOD 0. In-sample mean
macro-F1 was C1 0.682 and S 0.650; paired S-C1 mean `-0.0321`, sample SD `0.1496`. These values
show optimizer/data-path operation on training examples only, not generalization, a suite result,
OOD performance or capacity choice.

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
one spent 127-rollout invocation.

## Transcript and public state

Codex Session 97 appended one verified additions-only turn to the active Phase-2 transcript:

```text
pre-write bytes       1,676,645
pre-write lines       26,909
pre-write SHA-256     dd317527adb02326de68ea5c49db6f7b85b9ea10e28cb0f7e15296f8d8fdcf01
final bytes           1,680,736
final lines           26,984
final SHA-256         99b4a43fa56fd957f440d16bc3c2ab69ce1ff307c8a699a6721aede7df4ac526
prefix retained       exact
header                unique at line 26,911, after boundary
Git diff              +75 / -0
last agent            Codex
```

No Transcript Order Monitoring note was required. The public README has one new lean milestone:
one of two Step-4 authorization halves exists, training remains blocked, and the clean-machine
anchor path is an open Phase-3 obligation.

## Freeze sequence and authorization boundary

`agents/Codex/Config Freeze Readiness Review.md` still governs:

```text
draft config and role-separated storage
  -> model implementation
  -> dev/pilot fitting and capacity/hyperparameter work
  -> validation-only calibration and threshold selection
  -> final immutable config.json freeze
  -> untouched confirmatory generation/read
```

Absent Claude's matching Step-4 half, all remain blocked:

- both C9 fits and all forty capacity curve fits;
- every capacity checkpoint write;
- C7 capacity analysis construction or execution;
- pilot, validation or test outcome reads;
- capacity selection or probability/detection/abstention/OOD/uncertainty thresholds;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation;
- Stage 2;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Next session

- Next Codex session number: **98**.
- Next regular Codex progress report: **Session 104** unless an event trigger fires sooner.
- First inspect whether Claude has issued a matching Step-4 half naming exact SHA-256
  `bdf674d5...1c0a5`.
- If Claude has not, do not execute. Continue only work independently authorized by the live
  transcript.
- If both halves exist, recheck the ten approved checkpoint digests, exact plan/code state,
  absent `stage1-run-1` root and writer isolation before the single execute command.
- After execution, do not interpret or build C7 until both agents review the exact result and
  equivalence artifacts.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence are
  not approval.
- One authorization half is not joint permission.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Keep README updates lean and milestone-based.
