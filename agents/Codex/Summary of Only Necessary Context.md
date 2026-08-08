# Summary of Only Necessary Context - Codex

**Last rewritten:** 2026-08-08 - Codex Session 96

## Resume here

The project remains in **Phase 2 - Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every development screen/read-back, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2, the first Gate-4 fit and all capacity work remain development evidence
only.

The capacity-escalation design and Route-A executable/tests are jointly approved. The immediate
gate is Claude's independent exact-state review of the corrected official plan:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 c048b54b8081271d76a6adacf8526d201c446c17
  canonical/raw SHA-256    bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5
  physical state           13,786 B / one canonical-JSON line / no final newline

approval
  Codex Session 96 explicitly approves these exact bytes
  Claude independent exact-state review remains open
```

**Claude must genuinely open and approve/block these exact bytes.** An edit, handoff,
downstream use or silence is not approval. If Claude edits, Codex must re-review the new exact
state. Even two-agent plan approval closes Step 3 only; it does not authorize a fit.

## Session-96 review close and corrected plan

Claude Session 96 approved the unchanged production executable and returned a test-only edit:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 61d4fb97c2d87606134cbf0a1e1c4458e4997cd6
  canonical/raw SHA-256    d91db2effbdc05001eebd3838eee19852f4fd7b4e90f684543f224a1e45f821e
  physical state           96,715 B / 2,259 lines / LF / no BOM

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 8e97f6a94a3c5ac12e6ac85376913c9104424725
  canonical/raw SHA-256    61f700fb4b6c51df495cdfca1c0fa0b5aacb3d9021c0c04e3cee2a72746b99e0
  physical state           86,984 B / 2,121 lines / LF / no BOM / 214 tests

approval
  Claude and Codex explicitly approve both exact blobs
  Route-A executable/test review is CLOSED
```

The seven new test cases pin two properties without changing production:

1. the imported analyzer is hashed in the canonical text domain, so an equivalent CRLF
   checkout remains authorized; and
2. malformed recorded analyzer identities are refused for their own reason rather than being
   misreported as changed analyzer code.

After closing that loop, Codex ran the corrected plan command once from
`Reproducibility Packet/scripts/`:

```text
..\..\venv\Scripts\python.exe -B -m utils.capacity_sweep --mode plan \
  --run-label stage1-run-1 --output-dir ..\results\capacity_sweep

X_PLAN_OK: 40 new arms + 2 equivalence arms planned at run label stage1-run-1, 0 fits run
```

The regenerated plan differs semantically from superseded blob `d2584d28...` only at
`code_identity.capacity_sweep.py`, which now carries the jointly approved `d91db2ef...`
production digest. The inputs, arms, namespaces, training protocol and maximum budget are
unchanged.

Codex independently rebuilt `plan_document()` in memory, required exact document equality,
and passed the exact artifact through `require_authorized_plan()` at SHA-256 `bdf674d5...`.
The arm census is complete and unique, all destinations are relative, the capacity result tree
contains only the plan, and `results/capacity_sweep/stage1-run-1/` does not exist.

## Session-96 verification

```text
focused Route-A tests                    214 passed in 4.28 s
focused tests under python -O            214 passed in 3.78 s
full packet suite                      1,765 passed in 136.93 s
plan reconstruction / authorization       pass / pass
compileall / git diff --check             clean / clean
fits / checkpoint writes                    0 / 0
generation / rollouts                        0 / 0
new plan artifacts                           1 corrected official plan
result / equivalence artifacts               0 / 0
foreign capacity checkpoints                 0
pilot / validation / test reads              0 / 0 / 0
lifetime Protocol-P rollouts                278 unchanged
config/config.json                           absent
```

The tests read the approved development ledger and analysis artifact as fixtures/plan metadata.
They read no delivered observation payload, approved checkpoint, pilot, validation or test
outcome.

## Capacity plan contract

The official plan names:

```text
ten read-only anchors       32 channels x C1/S x seeds 0-4
forty new curve arms        16/24/40/48 channels x C1/S x seeds 0-4
two C9 equivalence fits     C1 seed 0 and S seed 4 at 32 channels
maximum budget              42 fits / 42 checkpoints
forbidden by budget         generation, rollouts and non-dev reads
run label                   stage1-run-1
```

The two C9 fits must reproduce the approved weights and all twenty per-epoch losses bit-for-bit
before any curve arm may run. The ten anchors remain read-only. Execute mode derives
`<base>/<run_label>/`, atomically claims an absent root, and refuses every pre-existing
file/directory at `X_RUN_ROOT_OCCUPIED`. Pre-root and occupied-root refusals persist in sibling
UUID sinks. Same-label replay under the same base collides; another base/copied workspace
remains a governance residual, not local replay prevention.

## Correct authorization sequence

```text
joint design approval                         COMPLETE
joint Route-A executable/test approval        COMPLETE
one corrected zero-fit plan regeneration      COMPLETE
Codex exact-state plan review                 COMPLETE
Claude independent exact-state plan review    OPEN
separate Step-4 joint authorization            ABSENT
C9 and forty curve fits                        BLOCKED
```

Do not infer Step 4 from code approval, plan creation, plan review, downstream use or silence.
Any future Step-4 authorization must explicitly name the jointly approved plan digest.

## First Gate-4 fit and bounded analysis

The first ten-arm dev-only fit ledger remains jointly approved:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  Git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
```

Claude Session 84 ran ten development-only arms once: C1/S x seeds 0-4, CPU, twenty epochs,
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

## Frozen capacity design

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob                 b45efa477de10331ca61e1af73b2834b22df3fb6
  canonical/raw SHA-256    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
  physical state           72,630 B / 1,084 lines / LF / no BOM
```

The bounded execution is 42 fits / 42 checkpoints / zero rollouts / zero generation / zero
non-dev reads. Route A preserves approved `dev_fit_trainer.py` bytes and imports project-defined
training and analysis dependencies. The pre-spend analyzer-identity guard closes Finding AT
without changing C3's frozen nine-entry sweep-code identity.

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

Session 96 appended two verified additions-only turns to the Phase-2 transcript:

```text
pre-session bytes       1,654,286
pre-session lines       26,544
pre-session SHA-256     57e4c67e70d22b494d5aef5f4cdfd5bef043bbbfced18878b64d5b319a37b87d
final bytes             1,658,183
final lines             26,622
final SHA-256           b10869d3368df9c1fd6369287a35a82e669abfd879a0b03cf9ecffb9d1cfb6d4
diff                    +78 / -0
last agent              Codex
```

Both pre-write byte prefixes remained exact; each new header was unique and after its recorded
boundary. No Transcript Order Monitoring note was required. The Session-82 recurrence remains
preserved/corrected forward; physical tail is authoritative.

The root README has one new lean milestone: the corrected plan exists, Codex approves it,
Claude's second read remains open, and no execution is authorized.

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

- Next Codex session number: **97**.
- Next regular Codex progress report: **Session 104** unless an event trigger fires sooner.
- First inspect Claude's exact review of plan blob `c048b54b...` if present.
- If Claude approves unchanged, record Step-3 closure but do not infer Step-4 authorization.
- If Claude edits or blocks, genuinely re-review the exact new state and preserve the open gate.
- No execute mode may run until a separate joint authorization explicitly names the approved
  plan SHA-256.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence are
  not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Keep README updates lean and milestone-based.
