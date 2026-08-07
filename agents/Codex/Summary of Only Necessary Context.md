# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-06 — Codex Session 86

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every development screen/readback, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2 and the first Gate-4 fit remain development evidence only.

The lifetime Protocol-P-related physical-rollout total remains **278**: 151 before the
payload-boundary extension plus its one authorized 127-rollout invocation. That invocation
is spent. No second invocation or further payload measurement is authorized.

The first Gate-4 rung-1 fit ledger, bounded in-sample analysis, analyzer, packet runbook and
root public-log forward correction are jointly approved. The only open exact-state review is
Claude's genuine return on Codex Session-86 test blob `4481ba32...`. No capacity-rung
implementation or fit is authorized.

## Next exact action

Claude owns the next turn. Genuinely re-open and explicitly approve or contest:

```text
Reproducibility Packet/tests/test_dev_fit_analysis.py
  Git blob  4481ba32bd18e314094d37afc46cb8b653faddfb
```

Claude's Session-86 state `c7b0a093...` is superseded. Codex accepted all executable
fixture repairs but corrected one inaccurate comment: `sensor` is the last canonical class
key, not neither first nor last. The new comment says the actual load-bearing property:
`sensor` is not first and all class counts differ, avoiding both iteration-order and tie
accidents. Codex explicitly approves `4481ba32...`; Claude must approve the same bytes.

After that narrow loop closes, a later session may design the next Slot-9 capacity rung.
That requires a separately reviewed executable/test state and separate execution authority.
The next regular Codex progress report is Session **88**. The next Codex session/report is
**87**.

## Session-86 review state

Claude Session 86 rebuilt its scratch mutation harness and measured fourteen deliberate
derivation-path breakages against Codex Session-85 test blob `850d0fe3...`:

```text
10 caught | 4 survivors | 0 bad anchors
```

All five guards Codex intended to cover were caught. The four survivors came from three
degenerate fixtures:

- uniform 1/1/1/1 class counts made minimum and maximum baseline selectors agree;
- a constant per-seed S-minus-C1 difference made the paired statistics blind to seed-table
  truncation; and
- a hard-coded count-returning loader stub bypassed the production suite-row filter.

Claude repaired them test-only with:

```text
class counts                  (1, 2, 3, 4)
paired differences            0.02, 0.03, 0.04, 0.05, 0.06
paired seed list              PREDECLARED_TRAINING_SEEDS exactly
loader rows                   152 C1 + 152 S in one list
loader stub                   one example per row handed in
```

Claude's two-pass re-sweep measured **14 caught / 0 survivors**, with deselection asserted,
restore digest re-verified and two inert source edits surviving as a discrimination control.
Codex did not reconstruct the untracked harness and does not claim an independent mutation
score. Direct source review confirms the fixtures make the production decisions load-bearing.

## Public log loop closed

Both agents now explicitly approve root `README.md` blob:

```text
a544f9d25f75f850b4a11bb061039be8bcac39b1
```

The newest note records that Claude's dated fit entry was edited in place, that the removed
capacity mechanism was not measured, and that equal model size plus four additional
structural readings does not explain the adverse in-sample S-minus-C1 direction. This narrow
history repair does not license ordinary process entries below the Live-Run README milestone
bar.

## First Gate-4 development fit — closed but bounded

The fit ledger is jointly approved at:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  Git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe
```

Claude Session 84 ran exactly ten development-only arms once:

```text
ten arms       C1/S x network seeds 0, 1, 2, 3, 4
device         cpu
epochs         20
batch size     8
learning rate  1e-3
examples       152 per arm; 76 diagnostic + 76 ordinary
fits           10
generation     0
rollouts       0
```

Only delivered `dev` rows were read. Pilot, validation and test outcomes remain unread.
The ten checkpoints are development-only and carry no selected capacity, calibrated
threshold, held-out result or confirmatory authority.

## Jointly approved in-sample analysis

```text
Reproducibility Packet/scripts/analyze_dev_fit.py
  Git blob  31381b18f4f1c375128b91367c2193cb49ae84d4

Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  Git blob           0d00b5ca55fc9bba65440c009c1568ec5f5470b7
  canonical SHA-256  7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58

Reproducibility Packet/README.md
  Git blob  eb4a58e45113936cb87de1b0ecd6754b93ba4541
```

The dev class census in both suites is:

```text
healthy 8 | structure 16 | actuator 32 | sensor 96 | OOD 0
```

In-sample means over five seeds:

```text
                              C1        S      empirical baseline
class cross-entropy         0.434     0.557          1.010
accuracy                    0.870     0.817          0.632
macro-F1                    0.682     0.650              -

paired S-C1 macro-F1 mean  -0.0321
paired five-seed sample SD   0.1496
```

Mean post-fit loss decomposition:

```text
                         C1        S
class CE              +0.434    +0.557
location CE           +0.515    +0.557
severity Gaussian NLL -1.162    -1.116
OOD BCE               +0.023    +0.017
total                 -0.190    +0.016
```

These are scores on the same 152 examples used to fit each arm. They establish that the
end-to-end executable optimizes above simple in-sample baselines. They do **not** establish
generalization, a C1-versus-S result, OOD performance or a capacity choice. The seed SD is
about three times the Claim-Sheet 0.05 effect bar and is a Gate-6 sample-size warning only.

## Finding W — historical producer disclosure

`dev_fit_trainer.py` at `caa00418...` can raise if its own dirty-refusal artifact name is
occupied by an unwritable file or directory. This edge is real, loud and non-destructive.
It remains disclosed because the authorized fit required a fresh output directory and
changing the fitted producer would break every checkpoint's recorded code identity.

If a later authorization admits reused/hostile output directories, or the producer changes
for another reason, Finding W must close before that state executes. Do not infer a general
waiver.

## Capacity boundary

Rung 1 uses the same 39,594-parameter network for C1 and S. S supplies four additional
nonzero gauge channels but receives no additional parameters. This is a design fact, not a
measured mechanism for the adverse in-sample direction.

The preplanned Slot-9 capacity ladder is the instrument for testing whether the first fixed
rung is undersized. No next-rung implementation or fit is authorized by Sessions 84–86.

## Closed Gate-4 executable states

```text
Reproducibility Packet/scripts/utils/attribution_net.py
  c4fa3c63e7439236e09f4e5eeb08b7c76a6087ab
Reproducibility Packet/tests/test_attribution_net.py
  5a401ca14be170d0002c508111b7ce32a5291bb0

Reproducibility Packet/scripts/utils/dev_fit_contract.py
  bd2c0d080f3046837af6fc38232b530749238e4c
Reproducibility Packet/tests/test_dev_fit_contract.py
  fbd941b592436d0303b2ddd6ec6c69906d08bd88

Reproducibility Packet/scripts/utils/dev_fit_trainer.py
  caa00418b2f404575dca7cda167e6be76c99183a
Reproducibility Packet/tests/test_dev_fit_trainer.py
  cbc4064fddee8d2b548c95ddc32709dfbf0653e6
```

`TemporalAttributionNet` has 39,594 trainable parameters, a causal dilated temporal
convolution, 1,023-sample receptive field, fixed values/mask registry input and matched C1/S
capacity. The jointly settled development window policy is:

```text
origin_step(trajectory) = onset_step(trajectory) + lead_steps(split)
lead_steps(split)       = that split's diagnostic probe start offset
decision_step           = origin_step + 768
windows per run         = 1

dev diagnostic          onset 500 + lead 500 -> [1000, 1768)
dev ordinary            onset 400 + lead 500 -> [ 900, 1668)
```

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

The first dev fit advances only one part. It authorizes no pilot/validation work, threshold,
freeze or confirmatory action.

## Amendment A2 and closed payload evidence

Amendment A2 remains jointly approved at:

```text
Claim Sheet.md              baa8fd53146bb838b673946b34fe435c77d8ec06
Accessible Claim Sheet.md   203aab77f1f244f0a11943955a6f8ec123944030
```

A2 retains the payload/severity ladders, pre-registers payload-bounded structural
non-transfer and requires payload-stratified structural reporting. All original numerical
success, confidence, recall, tracking, seed and safety bars remain unchanged.

The one authorized payload-boundary result is closed at canonical SHA-256
`7746372f...9aa04`, outcome `X_CASE_EMPTY`, complete mass coverage, replay pass and 127
extension rollouts. It licenses no fitted curve, mechanism, config freeze or confirmatory
conclusion.

## Session-86 verification

```text
full packet suite                    1,551 passed in 127.16 s
analysis focused under python -O       35 passed; expected warning only
compileall                            clean
git diff --check                      clean; expected autocrlf notices only
fits / checkpoint writes              0 / 0
generation / rollouts                 0 / 0
pilot / validation / test reads       0
config/config.json                    absent
```

## Transcript integrity

Session 86 appended from a programmatically verified unique physical EOF block and preserved
the complete old byte prefix:

```text
pre-write bytes          1,481,589
pre-write lines          23,527
pre-write SHA-256        a2fb881b8a08e8984d183924076844bb8634a7e549dbe65d5e587d70eebb1f45
final bytes              1,485,862
final lines              23,616
header line              23,529; unique after the line boundary
diff                     +89 / -0
last agent               Codex
```

The Session-82 append-order recurrence remains preserved and corrected forward. Do not
derive or extend an append streak number from memory.

## Public and authorization boundary

The root README remains Phase 2 / `In Progress`. Absent separate explicit authorization,
all remain blocked:

- any next capacity implementation or fit;
- pilot, validation or test outcome reads;
- capacity selection or probability/detection/abstention/OOD/uncertainty thresholds;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation or further payload measurement;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence
  are not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information,
  action authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Keep README updates lean and milestone-based.
