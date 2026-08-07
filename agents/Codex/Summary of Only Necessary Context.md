# Summary of Only Necessary Context -- Codex

**Last rewritten:** 2026-08-06 -- Codex Session 87

## Resume here

The project remains in **Phase 2 -- Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every development screen/readback, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2 and the first Gate-4 fit remain development evidence only.

The lifetime Protocol-P-related physical-rollout total remains **278**: 151 before the
payload-boundary extension plus its one authorized 127-rollout invocation. That invocation
is spent. No second invocation or further payload measurement is authorized.

The first Gate-4 rung-1 fit ledger, bounded in-sample analysis, analyzer, packet runbook and
root public-log forward correction are jointly approved. Codex now explicitly approves the
strengthened analysis-test blob `6f29bf05...`; Claude's literal approval of that same blob is
still missing. Capacity-escalation v0.1 is reviewable but blocked in draft. No capacity
executable, plan execution or fit is authorized.

## Next exact actions

Claude owns the next turn.

The next Codex session/report is **88**, which is also the next regular every-eighth-session
director progress-report trigger.

### 1. Close the narrow test loop literally

Genuinely re-open and explicitly approve or contest:

```text
Reproducibility Packet/tests/test_dev_fit_analysis.py
  Git blob  6f29bf05ddebae9f33817381f4713089f99ee7e4
```

Codex Session 87 independently reviewed and explicitly approved these exact bytes. Claude's
Session-87 handoff called them the returned state and asked Codex to approve or contest, but
never explicitly said that Claude approved the blob. An unchanged literal owner approval in
chat closes the loop; do not edit the test merely to record approval.

The approved substance is:

- `_DERIVED_CLASS_COUNTS = (1, 2, 4, 3)` preserves the same class-proportion multiset;
- `actuator` is the unique interior majority, so first-key, last-key, minimum and tie
  accidents no longer share the expected answer;
- empirical-prior cross-entropy remains `1.2798542258336676`;
- majority accuracy remains `0.4`; and
- the test-only change is outside `analysis_code_identity()`, so no analysis artifact
  regeneration is owed.

Session-87 verification: 35 focused tests under `python -O`, 1,551 full packet tests and clean
compileall.

### 2. Revise and explicitly approve the capacity design

Current draft:

```text
Reproducibility Packet/protocol/capacity-escalation-v0.1.md
  Git blob          b86d46aa64da883a8438b3880d90bc37c11360eb
  canonical SHA-256 2250add159c9adf5c95a5520a85b50595af04d84a704d389e3d095ed1cc11cf0
  status            BLOCKED DRAFT; approved by nobody
```

Codex accepts reviewing this document now; the sequencing deviation is closed. The draft
must return as an explicitly owner-approved state before an exact review loop can close.

Required corrections:

1. **Remove the causal `CAPACITY_BOUND` claim.** A fixed-20-epoch width sweep measures width
   sensitivity under one optimization protocol. It cannot isolate representational capacity
   from width-dependent optimization/trainability, and a relative crossing may come from C1
   worsening rather than S improving. Persist both absolute suite curves and use descriptive
   observation labels or no executable verdict.
2. **Make any outcome function complete and exact.** "Increasing," "no upward trend" and
   "small relative to the seed spread" are undefined. Suite-mean saturation can hide
   seed-level saturation. Prefer publishing exact curves plus saturation diagnostics and
   reserving interpretation for joint review. If a classifier remains, enumerate exact,
   exhaustive, mutually exclusive inequalities and one non-contradictory license per branch.
3. **Correct the cross-width seed claim.** At fixed width/seed, C1 and S share identical
   same-shaped initialization and row order. Across widths, tensors have different shapes;
   repeated integer seed labels are not common initial weights or cross-width CRN. The fixed
   seed set prevents different seed samples from confounding width; claim only that.
4. **Use grid `{16, 24, 32, 40, 48}`.** Codex independently measured the 40-channel model at
   61,010 parameters and receptive field 1,023, inside rung 1. This gives a second point above
   the fitted anchor if 48 is saturated. The revised plan has 50 total arms, ten reused and
   **40 new fits**. Measure 40-channel cost; do not interpolate.
5. **Do not add the proposed two-trajectory holdout.** The dev trajectories are different
   regimes: diagnostic/probe/onset-500/origin-1000/run-3000 versus ordinary/no-probe/
   onset-400/origin-900/run-2900. A one-to-other split measures cross-regime transfer, halves
   training data and breaks comparability with the approved 32-channel ledger. Any future
   transfer diagnostic needs its own symmetric pre-registration.
6. **Reconcile bound 5 and Slot 14.** The Technical Report must disclose the within-suite
   sweep as development-only instrument diagnosis and capacity-search history; it may not
   treat it as held-out C1-vs-S evidence, a headline result or a capacity selection.
7. **Add aggregate plan/partial-state rules.** Before fits, require a canonical zero-fit plan
   binding all new/reused arms, source/data/protocol identities, a fresh output root, exact
   output names and maximum budget. A run-level terminal artifact must record completed,
   refused and unattempted arms plus checkpoint digests. No silent overwrite/resume, no
   second 32-channel fit and no partial directory presented as a complete curve.

Choices Codex approves in principle: no Claim Sheet amendment; Stage 1 wholly inside rung 1;
width not depth; 1,023-sample receptive field fixed; reuse never rerun of 32-channel arms;
dev-only/zero-rollout/later-role refusal; separate document, executable, zero-fit plan and
execution gates; protocol-folder placement; approved-version immutability.

## First Gate-4 development fit -- closed but bounded

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

Only delivered `dev` rows were read. Pilot, validation and test outcomes remain unread. The
ten checkpoints are development-only and carry no selected capacity, calibrated threshold,
held-out result or confirmatory authority.

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

## Finding W -- historical producer disclosure

`dev_fit_trainer.py` at `caa00418...` can raise if its own dirty-refusal artifact name is
occupied by an unwritable file or directory. This edge is real, loud and non-destructive.
It remains disclosed because the authorized fit required a fresh output directory and
changing the fitted producer would break every checkpoint's recorded code identity.

If a later authorization admits reused/hostile output directories, or the producer changes
for another reason, Finding W must close before that state executes. Do not infer a waiver.

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

`TemporalAttributionNet` at 32 channels has 39,594 trainable parameters, a causal dilated
temporal convolution, 1,023-sample receptive field, fixed values/mask registry input and
matched C1/S capacity. The jointly settled development window policy is:

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

## Session-87 verification and transcript integrity

```text
analysis focused under python -O       35 passed; expected warning only
full packet suite                   1,551 passed in 129.39 s
compileall                            clean
git diff --check                      clean; expected autocrlf notices only
40-channel constructor probe          61,010 parameters / receptive field 1,023
fits / checkpoint writes              0 / 0
generation / rollouts                 0 / 0
pilot / validation / test reads       0
config/config.json                    absent
```

Session 87 appended from a programmatically verified unique physical EOF block and preserved
the complete old byte prefix:

```text
pre-write bytes          1,496,410
pre-write lines          23,792
pre-write SHA-256        32bc9961821a95f6f79207a258f2e09747ce3f003d314eac101c5c0d52ab3fe6
final bytes              1,506,399
final lines              23,975
header line              23,794; unique after the line boundary
diff                     +183 / -0
last agent               Codex
```

The Session-82 append-order recurrence remains preserved and corrected forward. Do not derive
or extend an append streak number from memory.

## Public and authorization boundary

The root README remains Phase 2 / `In Progress` and was deliberately unchanged in Session 87.
Absent separate explicit authorization, all remain blocked:

- any capacity executable, zero-fit plan execution or fit;
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
