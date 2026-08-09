# Summary of Only Necessary Context - Codex

**Last rewritten:** 2026-08-08 - Codex Session 98

## Resume here

The project remains in **Phase 2 - Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every Protocol-P measurement, payload extension, first learned fit, in-sample
analysis and capacity action remains development evidence only.

The first authorized Stage-1 capacity sweep ran once at `stage1-run-1` and failed safely after
three fits. Finding AU is repaired in production, but the executable/test review loop is **open on
Claude** because Codex reviewer-edited the returned test file.

```text
joint capacity design approval                    COMPLETE
old Route-A executable/test approval              SUPERSEDED BY AU REPAIR
stage1-run-1 plan                                 CONSUMED / SUPERSEDED / PRESERVED
old Step-4 halves                                 SPENT
stage1-run-1 execution                            SPENT ONCE; FAILED SAFELY
Finding-AU production review by Codex             APPROVED
Finding-AU reviewer test state                    APPROVED BY CODEX / OPEN ON CLAUDE
stage1-run-2 plan                                 ABSENT / BLOCKED
fresh Step-4 authorization                        ABSENT / BLOCKED
retry execution                                   BLOCKED
```

Do not run `--mode plan` or `--mode execute` yet. Claude must genuinely re-review the exact
reviewer test blob first. A reviewer edit and handoff are not owner approval.

## Finding AU and the preserved failed run

Claude Session 98 recorded its matching old Step-4 half and executed the single authorized
`stage1-run-1` invocation. It ran from 2026-08-08 16:15:53 to 16:16:26 PDT and terminated at
`X_OUTPUT_DIRTY` on the second curve arm.

```text
fits attempted             3 = 2 C9 equivalence + 1 curve
checkpoints written        3 = 2 C9 equivalence + 1 curve
curve census               10 REUSED / 1 COMPLETED / 39 UNATTEMPTED
rollouts / generation      0 / 0
non-development reads      0
elapsed_s                  31.313
```

Mechanism: `_execute_mode` called `require_clean_capacity_point(point_dir)` once per **arm**
against a directory ten arms share. The first width-16 arm wrote its checkpoint; the second
width-16 arm found that checkpoint and treated this run's own output as an earlier attempt. The
executable could never complete more than one arm per capacity point.

The preserved evidence is:

```text
Reproducibility Packet/results/capacity_sweep/stage1-run-1/capacity_sweep_result.json
  Git blob                 32743393908cf7a5f2109eabb034eafe849d78a7
  raw SHA-256              2be7e421cfff103296b94a1ba3c539320a334f8e242e4352994b10be54817559

.../stage1-run-1/_equivalence/capacity_sweep_equivalence.json
  Git blob                 cd8bdc1421961c6d7b3a828992e8f22996003370
  raw SHA-256              e5afaec2b525d38f8a8d421bcc74d3370b97edc9e84a9b8035d88725946b8182
```

Three `.pt` files under the failed root are Git-ignored but present. Their raw digests match the
tracked JSON. Section 7.3 controls: do not delete, clean, reuse, move or import from this root.

## What survived the failed run

C9 passed end to end through the complete fit path:

```text
C1 seed 0   produced 6403e894... == approved 6403e894...   PASS
S  seed 4   produced eb9dbb0c... == approved eb9dbb0c...   PASS
```

This is valid development evidence that the old approved width-parameterized executable reproduced
the approved 32-channel fit bytes across both suites and two seeds. It does not license a curve,
capacity choice, analysis or confirmatory claim. Because the AU repair moved the executable bytes,
the eventual conforming retry must re-run and re-establish C9; the old pass is not inherited.

The one completed curve arm is 16 channels / C1 / seed 0 with in-sample macro-F1 0.463789,
accuracy 0.802632, final loss 0.152582 and 10,586 parameters. It is a partial-run record only.
C10 correctly leaves thirty-nine arms `UNATTEMPTED`, so section 5.4 cannot be applied.

## Exact open executable/test state

Codex explicitly approves:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
  canonical/raw SHA-256    be07d95e4b4b9fa1a8934a165681fdbc9e7e885236bd1de3c38b661288f641fa

Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 6d49edde03e24a262e4246669fad8e42859c6f8a
  canonical/raw SHA-256    640f23b5990d9fc9f17fe0eeb39bbf9192abaa26ab1726653d9df9942c1747d3
```

Production repair:

1. iterate the four distinct `curve_arms()` channel values and call the real point-cleanliness
   guard once for each; and
2. do so above C9, after the atomic root claim and authenticated dev-input load but before any fit.

Codex approves both properties. Moving the check below C9 would spend two fits before a known
output refusal and would not close the foreign-writer race, which is an explicit residual either
way.

Codex found one returned-test gap: mutating the loop to check only `[48]` still passed all three
Claude tests. The reviewer edit wraps the real guard and requires the exact call sequence
`channels_016`, `channels_024`, `channels_040`, `channels_048`. That mutation now fails.

Exact-state verification:

```text
test_capacity_sweep.py, normal       217 passed
test_capacity_sweep.py, python -O     217 passed, expected pytest warning
full packet                           1,768 passed
compileall                            clean
git diff --check                      clean
skipped-point mutation                caught
```

Claude explicitly approved its earlier test blob `2dc93297...`, not Codex's `6d49edde...` edit.
The loop closes only if Claude genuinely reopens and explicitly approves the exact reviewer pair.

## Consumed plan and required restart sequence

The consumed plan remains preserved:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 c048b54b8081271d76a6adacf8526d201c446c17
  canonical/raw SHA-256    bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5
  run label                stage1-run-1
```

The repaired module refuses it with `DevFitContractError: the authorized plan was written by a
different code state`. Do not overwrite this file: it is the exact plan the failed evidence names.

The conforming order is four separate gates:

1. Claude owner-reviews and approves the exact AU repair pair.
2. One zero-fit plan is generated at new label `stage1-run-2`; both agents independently approve
   its exact bytes.
3. A fresh two-half Step-4 joint authorization names that new digest, label, base, executable,
   anchors and maximum budget.
4. One retry runs both C9 fits plus all forty curve fits from the fresh root. Then both agents
   review the exact result before section 5.4 or C7.

No old authorization half carries forward. The retry is a second execution and requires a second
joint act.

## Clean-machine checkpoint obligation

The approved ten anchor checkpoints and the failed run's three checkpoint files exist only as
Git-ignored files in this working tree. A completed retry would add forty-two more ignored files.
This is not a `director_requests.md` item and does not block a correctly authorized local
development measurement, but it is a real **Phase-3 Reproducibility Packet obligation**.

Before packet completion, either fresh-machine regeneration must reproduce raw checkpoint digests
and an authenticated promotion/install step must put them in the namespace the sweep reads, or the
exact bytes must be obtainable through a documented authenticated packet data path. Disclosure
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

Codex Session 98 appended one verified additions-only turn to the active Phase-2 transcript:

```text
pre-write bytes       1,701,780
pre-write LF count    27,322
pre-write SHA-256     f9c12e5b03ba2b9d7969e70c319054500651fb98dfba120d612e0be788f63a5b
final bytes           1,705,838
final LF count        27,397
final SHA-256         a03f87a26ac2b7f6506b294c757b6776a67ca894f9cae649a915cda3a508065f
prefix retained       exact
header                unique at physical line 27,324
Git diff              +75 / -0
last agent            Codex
```

No Transcript Order Monitoring note was required. The public README already has Claude's lean
Finding-AU milestone and was deliberately left unchanged in Codex Session 98 because this session
is an open review handoff, not a newly closed public artifact or phase.

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

Blocked until the AU loop, new plan review and fresh authorization close:

- both C9 fits and all forty capacity curve fits;
- every capacity checkpoint write;
- plan regeneration before Claude owner approval;
- C7 construction or execution and section-5.4 interpretation;
- pilot, validation or test outcome reads;
- capacity selection or probability/detection/abstention/OOD/uncertainty thresholds;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation;
- Stage 2;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Next session

- Next Codex session number: **99**.
- Next regular Codex progress report: **Session 104** unless an event trigger fires sooner.
- First inspect whether Claude genuinely approved test blob `6d49edde...` with production blob
  `53e5dcb7...`.
- If not, do not plan or execute; continue only independently authorized work in the live thread.
- If exact owner approval exists, plan mode may generate one new `stage1-run-2` artifact with zero
  fits. Preserve the consumed `stage1-run-1` plan and failed root.
- Plan approval, fresh Step-4 authorization, retry execution, exact result review, section 5.4 and
  C7 remain separate gates.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence are not
  approval.
- An old plan or authorization half never carries across a producer-code change or retry.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Keep README updates lean and milestone-based.
