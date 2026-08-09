# Summary of Only Necessary Context - Codex

**Last rewritten:** 2026-08-08 - Codex Session 99

## Resume here

The project remains in **Phase 2 - Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every Protocol-P measurement, payload extension, first learned fit, in-sample
analysis and capacity action remains development evidence only.

The Finding-AU executable/test loop is now jointly closed. A replacement zero-fit plan for
`stage1-run-2` has been published and Codex explicitly approves its exact bytes. Claude's
independent plan review is **open**, so the plan loop is not closed and no execution authorization
exists.

```text
Finding-AU production/test review                  CLOSED / SAME-STATE APPROVED
stage1-run-2 zero-fit plan                         PUBLISHED / CODEX APPROVED
stage1-run-2 independent plan review               OPEN ON CLAUDE
fresh Step-4 authorization halves                  0 OF 2 / ABSENT
stage1-run-2 execution                             BLOCKED
section 5.4 capacity interpretation                BLOCKED
C7 read-only analysis                              BLOCKED
```

Do **not** run `--mode plan` again. Do **not** run `--mode execute`. The plan already exists and
must remain byte-identical for Claude's review. Even Claude approval would close planning only;
execution requires a new, separate two-half joint act naming the exact plan, label, base,
executable, anchors and maximum budget.

## Exact replacement plan state

One plan-mode invocation ran in Codex Session 99 with no `--data-root`, zero fits and zero real-data
payload reads:

```text
X_PLAN_OK: 40 new arms + 2 equivalence arms planned at run label stage1-run-2, 0 fits run
```

The exact artifact is:

```text
Reproducibility Packet/results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json
  Git blob                 d7104e55b4fb9be3fbfa6bd685b002a055409673
  canonical/raw SHA-256    ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
  size                     13,786 bytes
  encoding                 UTF-8; zero CR; no BOM; no final newline
```

Claude pre-registered that exact digest and byte count before the artifact existed. Codex's
independent audit then confirmed:

```text
canonical compact re-emission                     byte-identical
full leaves, consumed / replacement               413 / 413
added / removed / changed                         0 / 0 / 48
new arms                                          40 = {16,24,40,48} x {C1,S} x seeds 0-4
anchors / equivalence arms                        10 / 2
declared output destinations                      44 distinct, packet-relative
maximum budget                                    42 fits / 42 checkpoints
generation / rollouts / non-development reads    0 / 0 / 0
```

The 48 changed leaves are exactly forty curve checkpoint paths, two equivalence checkpoint paths,
four namespace/artifact paths, `run_label`, and `code_identity.capacity_sweep.py`. The anchor arms,
approved result/analysis bindings, training protocol and other eight code identities are identical
to the consumed plan. The executable's own `require_authorized_plan()` accepts the exact new bytes
and digest.

Codex explicitly approves this plan blob and digest in the live transcript. Claude has not yet
approved it. Creation, prediction, handoff and silence are not a second approval.

## Why the new plan has a separate path

The consumed plan remains at:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 c048b54b8081271d76a6adacf8526d201c446c17
  canonical/raw SHA-256    bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5
  run label                stage1-run-1
```

It is exact evidence for the failed execution and must not be overwritten. The new plan therefore
lives under `results/capacity_sweep/plans/stage1-run-2/`. It also does **not** live in
`results/capacity_sweep/stage1-run-2/`, because that future execution root must stay absent for
`claim_run_root()` to create atomically.

At Session-99 close:

```text
results/capacity_sweep/stage1-run-1/               PRESENT / PRESERVED
results/capacity_sweep/stage1-run-2/               ABSENT
results/capacity_sweep/plans/stage1-run-2/         PLAN ONLY
config/config.json                                 ABSENT
```

## Finding AU and the preserved failed run

The first authorized capacity sweep, `stage1-run-1`, ran once and failed safely after three fits:

```text
fits attempted             3 = 2 C9 equivalence + 1 curve
checkpoints written        3 = 2 C9 equivalence + 1 curve
curve census               10 REUSED / 1 COMPLETED / 39 UNATTEMPTED
rollouts / generation      0 / 0
non-development reads      0
elapsed_s                  31.313
```

Mechanism: old `_execute_mode` called `require_clean_capacity_point(point_dir)` once per **arm**
against a directory ten arms share. The first width-16 arm wrote its checkpoint; the second found
that same-run output and treated it as stale debris. The executable could never finish more than
one arm per capacity point.

Preserved tracked evidence:

```text
Reproducibility Packet/results/capacity_sweep/stage1-run-1/capacity_sweep_result.json
  Git blob                 32743393908cf7a5f2109eabb034eafe849d78a7
  raw SHA-256              2be7e421cfff103296b94a1ba3c539320a334f8e242e4352994b10be54817559

.../stage1-run-1/_equivalence/capacity_sweep_equivalence.json
  Git blob                 cd8bdc1421961c6d7b3a828992e8f22996003370
  raw SHA-256              e5afaec2b525d38f8a8d421bcc74d3370b97edc9e84a9b8035d88725946b8182
```

Three ignored `.pt` files remain under the failed root and match the tracked JSON digests. Combined
with the ten approved anchors, the packet contains 13 ignored checkpoints. Do not delete, clean,
move, import, reuse or add anything under the failed root.

Both old Step-4 authorization halves named the consumed plan and were spent on `stage1-run-1`.
They do not carry to a retry.

## What survived the failed run

C9 passed end to end through the complete old fit path:

```text
C1 seed 0   produced 6403e894... == approved 6403e894...   PASS
S  seed 4   produced eb9dbb0c... == approved eb9dbb0c...   PASS
```

This is development evidence that the old approved width-parameterized executable reproduced the
approved 32-channel checkpoint bytes. It licenses no curve, capacity choice, held-out read or
confirmatory claim. The repaired executable has different bytes, so `stage1-run-2` must repeat and
re-establish both C9 fits inside that run.

The one completed curve arm is 16 channels / C1 / seed 0 with in-sample macro-F1 0.463789,
accuracy 0.802632, final loss 0.152582 and 10,586 parameters. It is a partial-run record only.

## Exact jointly approved executable/test state

Both agents now explicitly approve:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
  canonical SHA-256        be07d95e4b4b9fa1a8934a165681fdbc9e7e885236bd1de3c38b661288f641fa

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 6d49edde03e24a262e4246669fad8e42859c6f8a
  canonical SHA-256        640f23b5990d9fc9f17fe0eeb39bbf9192abaa26ab1726653d9df9942c1747d3
```

Production checks the four distinct `curve_arms()` channel values once each after atomic root
claim and authenticated dev-input load but before C9 or any fit. The residual foreign-writer race
is explicit; moving the checks below C9 would spend two fits before refusing a pre-existing dirty
point and would not close that race.

Codex's reviewer edit binds the real guard's exact call sequence:
`channels_016`, `channels_024`, `channels_040`, `channels_048`. Claude's genuine owner re-review
confirmed the edit catches three mutations the returned suite missed, weakens none of its old
coverage, and is independently anchored by the rest of the suite.

Verification on the exact post-plan tree:

```text
test_capacity_sweep.py, normal       217 passed
test_capacity_sweep.py, python -O     217 passed, expected pytest warning
full packet                           1,768 passed
compileall                            clean
plan independent audit               AUDIT_OK
exact-plan authorization probe       accepted
```

## Required restart sequence

Four gates govern the retry:

1. Finding-AU executable/test same-state approval. **CLOSED.**
2. One `stage1-run-2` zero-fit plan and same-state approval. **PUBLISHED; CODEX APPROVED; OPEN ON
   CLAUDE.**
3. A fresh two-half Step-4 joint authorization naming the approved replacement plan. **ABSENT.**
4. One execution from the absent `stage1-run-2` root, containing two C9 fits plus forty curve fits.
   **BLOCKED.**

After a completed run, both agents must review the exact result before section 5.4 or C7. Plan
approval, authorization halves, execution, result review, section 5.4 and C7 are separate gates.

## Clean-machine checkpoint obligation

The approved ten anchor checkpoints and the failed run's three checkpoint files exist only as
Git-ignored files in this working tree. A completed retry would add forty-two more ignored files.
This is not a `director_requests.md` item and does not block a correctly authorized local
development measurement, but it remains a real **Phase-3 Reproducibility Packet obligation**.

Before packet completion, either fresh-machine regeneration must reproduce raw checkpoint digests
and an authenticated promotion/install step must place them in the namespace the sweep reads, or
the exact bytes must be obtainable through a documented authenticated packet data path. Disclosure
alone cannot satisfy the binary fresh-environment gate. Do not weaken C9 with a free checkpoint
directory override.

## First Gate-4 fit and bounded analysis

The first ten-arm development-only ledger remains jointly approved:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  Git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
```

The approved read-only analysis remains:

```text
Reproducibility Packet/scripts/analyze_dev_fit.py
  Git blob           31381b18f4f1c375128b91367c2193cb49ae84d4

Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  Git blob           0d00b5ca55fc9bba65440c009c1568ec5f5470b7
  canonical SHA-256  7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58
```

Dev census is healthy 8 / structure 16 / actuator 32 / sensor 96 / OOD 0. In-sample mean
macro-F1 was C1 0.682 and S 0.650; paired S-C1 mean `-0.0321`, sample SD `0.1496`. These values
show optimizer/data-path operation on training examples only, not generalization, a suite result,
OOD performance or a capacity choice.

## Amendment A2 and payload boundary

Amendment A2 remains jointly approved:

```text
Claim Sheet.md              baa8fd53146bb838b673946b34fe435c77d8ec06
Accessible Claim Sheet.md   203aab77f1f244f0a11943955a6f8ec123944030
```

The one authorized payload-boundary result remains closed at canonical SHA-256
`7746372f...9aa04`, outcome `X_CASE_EMPTY`, complete mass coverage, replay pass and 127 extension
rollouts. It licenses no fitted curve, mechanism, config freeze or confirmatory conclusion.
Lifetime Protocol-P-related physical rollouts remain **278**.

## Transcript and public state

Codex Session 99 appended one verified additions-only turn to the active Phase-2 transcript:

```text
pre-write bytes       1,715,147
pre-write LF count    27,535
pre-write SHA-256     7571b1f73385558ab4b7c735cddbfd417d3696aee3312fdb7b924be4cd8eb493
final bytes           1,719,036
final LF count        27,606
final SHA-256         baa7e17ef69be4496863cc855562ce8c25c9813f9b9888d35e77b3ba7ffd4b65
prefix retained       exact
header                unique at physical line 27,537
Git diff              +71 / -0
last agent            Codex
```

No Transcript Order Monitoring note was needed. The public README gained one lean entry stating
that the replacement plan matched the fingerprint published before it existed, while preserving
that one plan review and every execution gate remain open. The Phase-2 banner is unchanged.

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

Blocked now:

- any second plan-mode write or plan replacement;
- both C9 fits and all forty capacity curve fits;
- every capacity checkpoint write;
- every Step-4 execute command before two fresh matching authorization halves;
- C7 construction/execution and section-5.4 interpretation;
- pilot, validation or test outcome reads;
- capacity selection or probability/detection/abstention/OOD/uncertainty thresholds;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation;
- Stage 2;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Next session

- Next Codex session number: **100**.
- Next regular Codex progress report: **Session 104** unless an event trigger fires sooner.
- First inspect whether Claude genuinely approved plan blob `d7104e55...` / SHA-256
  `ffb00965...b7cb31` unchanged.
- If Claude did not approve it, do not plan, authorize or execute; continue only independently
  authorized work in the live thread.
- If Claude did approve the exact plan, gate 2 is closed. A fresh Step-4 authorization remains a
  separate act. Record at most the appropriate new authorization half after rechecking the exact
  plan/code/anchor/root state; do not execute without both halves.
- Preserve the consumed plan, failed root, 13 current checkpoints and absent `stage1-run-2` root.

## Workflow rules

- Explicit same-state approval only. Creation, prediction, edits, handoffs, downstream use and
  silence are not approval.
- An old plan or authorization half never carries across a producer-code change or retry.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Keep README updates lean and milestone-based.
