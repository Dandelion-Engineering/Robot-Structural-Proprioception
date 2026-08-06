# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-05 — Codex Session 80

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, all development screens/readbacks, the payload-boundary
extension, Amendment A2, and any future Gate-4 development fit are development evidence
only, never confirmatory or final evidence.

The lifetime Protocol-P-related physical-rollout total is **278**: 151 before the
payload-boundary extension plus its one authorized 127-rollout invocation. That invocation
is spent. No second invocation or further payload measurement is authorized.

## Next exact action

Claude owns the next review turn. Re-open and genuinely owner-review:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py
  bd2c0d080f3046837af6fc38232b530749238e4c
Reproducibility Packet/tests/test_dev_fit_contract.py
  fbd941b592436d0303b2ddd6ec6c69906d08bd88
```

Codex explicitly approves these exact bytes. Claude explicitly approves only the
superseded `9d6ecfea...` / `d4202c8e...` state, so the loop is **OPEN** until Claude
approves the current blobs or edits and hands back a replacement.

No fit may run before this loop closes and the trainer/checkpoint/result executable state
is itself jointly reviewed. The next regular Codex progress report is Session **88**. The
next Codex session/report is **81**.

## Current development-fit contract review lineage

Claude Session 80 accepted all Session-79 exact-digest and provenance-type repairs and
centralized code-identity validation in one shared `require_code_identity` predicate.
Both the producer and provenance consumer call it; the producer also refuses non-mappings
before `.items()` and non-path values before `Path()`. Claude's exact handoff was:

```text
dev_fit_contract.py       9d6ecfea816833678fdfa667e956539d75e11ade
test_dev_fit_contract.py  d4202c8ea07bed623b4515cd39d9b51a4b470199
```

Codex Session 80 accepts that design and accepts Claude's decision not to normalize forty
remaining fail-closed caller-shape exceptions in the row/plan entry points. It found one
cross-field ordering regression caused by removing the producer's early label call:

```text
{"C:\\PRIVATE\\secret.py": None}
  -> disclosed the full path-shaped label before require_bare_name ran

{"net.py": valid_file, None: valid_file}
  -> foreign TypeError inside sorted() before the post-condition
```

The reviewer state restores one early call to the already-shared `require_bare_name`
predicate. This is not a second implementation of the rule: the early producer call orders
validation before path handling/sorting, while the final shared post-condition proves the
completed mapping is non-empty and audit-valid. A new test drives both mixed-label orders,
the disclosure case, and the absence of the full path from the refusal message.

Earlier lineage, still relevant but superseded:

```text
Claude S78 original       73e5e743... / 3959ff28...
Codex S78 reviewer        6541cebc... / 9df7d7f7...
Claude S79 returned       2448ad4d... / 2aa5f762...
Codex S79 reviewer        872c6b12... / 3125a618...
Claude S80 returned       9d6ecfea... / d4202c8e...
Codex S80 current         bd2c0d08... / fbd941b5...
```

## Verification of the current reviewer state

```text
pre-edit direct probes          path-shaped label disclosed;
                                mixed labels raised TypeError
post-edit direct probes         3/3 DevFitContractError;
                                complete path absent from message
focused contract tests          93 passed
focused under python -O         93 passed; expected pytest warning only
full packet suite               1,467 passed in 174.44 s
compileall                      clean
real dataset/manifest reads     0
fits / checkpoints / generation 0 / 0 / 0
rollouts                        0
config/config.json              absent
```

## Gate-4 rung 1 — jointly approved implementation

Both agents explicitly approve:

```text
Reproducibility Packet/scripts/utils/attribution_net.py
  c4fa3c63e7439236e09f4e5eeb08b7c76a6087ab
Reproducibility Packet/tests/test_attribution_net.py
  5a401ca14be170d0002c508111b7ce32a5291bb0
```

The approved state validates incoming weights/device transfer on a deep copy, then copies
validated tensors into the existing live network. It preserves transactionality, network
object identity, attached optimizer references, and provenance correctness.

```text
TemporalAttributionNet              39,594 trainable parameters
architecture                        causal dilated temporal convolution
receptive field                     1,023 samples
proposed window                     768 samples
input                               fixed [values, validity mask] registry
matched suites                      identical shape/count for C0, C1, S
unfitted behavior                   uniform p_class, abstain, no location,
                                    no detection, infinite severity uncertainty
installed torch                     2.11.0+cu128
CUDA / GPU                          12.8 / NVIDIA GeForce RTX 5060 Ti
```

The model is **untrained**. Joint implementation approval is not permission to fit.

## Development-only fitting authorization

Session 77 opened the **conceptual** Gate-4 dev-fitting gate. Training rung 1 against the
already-delivered development partition does not require new data generation. Amendment A2
did not independently grant this permission.

The authority is exact:

1. Read only persisted rows whose role is exactly `dev` from the jointly approved
   delivered base dataset. Pilot, validation, and test outcomes remain unread.
2. Generate no plant, sensor, label, or role payload and spend zero physical rollouts.
3. Hold architecture and training protocol identical across C1/S and run only training
   seeds 0, 1, 2, 3, 4 in both arms.
4. Every checkpoint/result carries the exact development-only authority and the dev data
   root, manifest/config/assignment identities, suite, training seed, training-protocol
   canonical-text code identity, row disclosure, and raw checkpoint digest.
5. A dev fit may establish learnability or expose implementation failures. It may not set
   validation-owned probability/detection/abstention/OOD/uncertainty thresholds, select a
   headline capacity from later roles, or become a research result.

Before execution, close the current contract review, then build and jointly review the
trainer and checkpoint/result writer. The trainer and evaluation driver must use the same
`deterministic_conv_precision()` scope around forward **and backward** computation. The
trainer must iterate the exact ten-arm `matched_fit_plan()`, call
`require_dev_only(rows, suite=...)` at point of consumption, and emit one validated
`DevFitProvenance` record per checkpoint/result. No additional conceptual permission is
needed only after those exact executable bytes close under these bounds.

## Delivered development partition

A Session-78 read-only manifest check opened no `.npz` payload and found:

```text
data root                           gate3-base-dev-pilot-val-c1-s
manifest rows                       944
selected dev rows                   304
C1 / S selected                     152 / 152
withheld                            640 (pilot 304, val 336)
config identity                     dev-712abf27c3f8f3c331ae9b76e3f22c4...
manifest raw SHA-256                55ea5f0e74ddd24b05eafc51a2b9fc42...
```

The full identities remain in `HumanReport78.md`. Sessions 79–80 did not read this
manifest or any payload.

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

Both agents approve the corrected sequence in:

```text
Reproducibility Packet/scripts/utils/estimator.py
  b2abf463d9a4b2678f182568f50417774a6191e7
Reproducibility Packet/scripts/utils/__init__.py
  04647db4f61b18aac33e088543c6c49d54feb584
Reproducibility Packet/README.md
  ebef72fef5e423779901ba8a47529ae64d6a4433
```

This sequence does not authorize pilot or validation work now.

## Amendment A2 remains in force

Both agents approve the same A2 files:

```text
Claim Sheet.md              baa8fd53146bb838b673946b34fe435c77d8ec06
Accessible Claim Sheet.md   203aab77f1f244f0a11943955a6f8ec123944030
```

A2 retains the full payload and severity ladders, pre-registers payload-bounded structural
non-transfer, and requires structural S-versus-C1 reporting by payload as well as pooled.
Every original numerical success threshold, confidence requirement, recall margin,
tracking-improvement bar, seed requirement, and safety condition remains unchanged.

A2 adds no severity, payload, split, trajectory, environment, contact profile, assignment,
or fault-grid entry. It shifts no seed ordinal and by itself invalidates no delivered
datum. Any later dataset supersession is separate and requires its own authorization and
archive/exclusion trail.

## Closed payload-boundary evidence

Both agents approve:

```text
Reproducibility Packet/results/payload_boundary_extension/payload_boundary.json
canonical SHA-256  7746372f1adea931722cf547adee36489971493c4e1b5217f588d4c6d1c9aa04
Git blob          2cf19daa385ec3f96c91acca9de3747d7ba0f115
outcome           X_CASE_EMPTY
mass coverage     COMPLETE
replay            PASS, 1 rollout
anchor            X_ANCHOR_PASS
extension         126 rollouts
total             127 rollouts
```

The development-context `TESTABLE_SET`s are:

```text
0.025 kg  {0.35, 0.40, 0.45, 0.50}
0.050 kg  {0.35, 0.40, 0.45}
0.075 kg  {0.35, 0.40}
0.100 kg  {0.35}
0.125 kg  {0.35}
0.150 kg  EMPTY
0.200 kg  EMPTY
```

Payload-matched development-context role coverage is 0/0/0/0. Binding limits: the
0.125/0.150-kg transition is unresolved inside the 10% reproducibility band; `MONOTONE`
means set inclusion rather than strict raw-distance monotonicity; seven CRN masses license
no fitted curve or independence claim; no mechanism is identified; raw gauge traces were
not persisted/re-derived; and this evidence cannot change Protocol P, role coverage, or
establish/refute the hypothesis.

## Public state and authorization boundary

The root README remains Phase 2 / `In Progress`, current blob
`d06f844b9476c1c43f4b74cb5edce4d7e413b0e1`. Session 80 deliberately added no public
entry: the contract loop is open, the model is untrained, and no finished milestone or
research result exists.

Absent a new separately explicit authorization, all remain blocked:

- fitting before the contract and trainer executable reviews close;
- any pilot, validation, or test outcome read;
- any new dataset generation, replacement, supersession, or regeneration;
- any second payload-extension invocation or further payload measurement;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads, or claims; and
- changes to closed Protocol P v2.3.3.

## Transcript integrity state

Session 80 appended from a verified unique normalized physical EOF block at:

```text
pre-write bytes    1,367,293
pre-write lines    21,485
pre-write SHA-256  8031be30c6d98bebdf0a51c811641576d030cdc3e467b850d433690c703bf609
```

The main handback prefix remained byte-identical and produced `+92/-0`. Diff hygiene then
found one accounting typo (`tests +27/-0` rather than `+28/-0`), so Codex appended a
forward bookkeeping correction from a second verified boundary of 1,371,908 bytes /
21,577 lines / SHA-256
`8e0d32013f51ca60c12b0ecbf6ec22d19e6a318676f5930be20393f32fada453`.
Both prefixes remained byte-identical; each header occurs once after its boundary; Codex
is physically last; the total diff is `+110/-0`; and the transcript now has 1,372,343
bytes / 21,595 lines. No ordering repair was needed.

## Session-80 reporting

The required regular report exists at
`agents/Codex/Progress Reports/Progress Report Session 80.md` and covers Sessions 73–80:
payload execution/result, A2, the untrained learned rung, and the current bounded fitting
contract. The next regular report is Session 88.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use, and silence
  are not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information,
  action authorization, and control outcome separate.
- Transcript appends require a recorded byte/line/hash boundary, the complete unique EOF
  anchor actually used by the patch, one post-boundary header, a byte-identical prefix, a
  physically last author, and additions-only diff. If any check fails, stop and append a
  forward correction before closeout.
- Preserve append-only public and technical history; corrections propagate forward.
