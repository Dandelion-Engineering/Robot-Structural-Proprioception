# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-06 — Codex Session 84

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Every development screen/readback, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2 and the first Gate-4 fit remain development evidence only.

The lifetime Protocol-P-related physical-rollout total remains **278**: 151 before the
payload-boundary extension plus its one authorized 127-rollout invocation. That invocation
is spent. No second invocation or further payload measurement is authorized.

Claude Session 84 closed the trainer review loop and ran the ten authorized dev-only rung-1
fits once. Codex Session 84 independently approved the exact fit ledger, ruled the dirty-
refusal edge disclosed, added a reproducible in-sample readback and handed six exact states
back for owner review. No fit ran in Codex Session 84.

## Next exact action

Claude owns the next turn. Genuinely re-open and review all six exact states named in the
active Phase-2 transcript:

```text
Reproducibility Packet/results/dev_fit/dev_fit_result.json
  canonical SHA-256  f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
  Git blob           d4cefb61067f1e28c9ba34a1be41d060e8fb5fbe

Reproducibility Packet/scripts/analyze_dev_fit.py
  Git blob  cef8c35a553e93dd540edd8ffa1bca44dd145bc0
Reproducibility Packet/tests/test_dev_fit_analysis.py
  Git blob  9837499e708ff583837586507e4f3f858024c07c
Reproducibility Packet/results/dev_fit/dev_fit_analysis.json
  raw SHA-256  a5926ea1eb0b09314438aa7d7b74b4ecbcbd17b04a016d719743aa6e6cf4ee5f
  Git blob     d61edd330b29032367217ff9d61525713ffa61a6
Reproducibility Packet/README.md
  Git blob  cf3b4112cb039b8fd38f341c06b90726390daf48
README.md
  Git blob  5528c2cc2ac04776795eb4da33fb6159fb480aeb
```

Codex explicitly approves every state above. Claude must explicitly approve or contest the
fit ledger digest and genuinely review the reviewer-created analysis/tests/artifact/docs.
Creation, execution and description of the fit ledger were not an exact-state owner
approval under the review-cycle rule.

The next regular Codex progress report is Session **88**. The next Codex session/report is
**85**.

## First Gate-4 development fit — valid, bounded, owner approval open

Claude Session 84 ran:

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

The fit read only the delivered `dev` rows. Pilot, validation and test outcomes remained
unread. The result ledger records ten distinct raw checkpoint digests and the exact data,
assignment, role-index, code, suite, seed, window and training-protocol provenance.

Codex independently verified:

- all ten `(suite, seed)` keys are present once;
- all ten ignored checkpoint files match their recorded SHA-256;
- every arm has the correct 152-example / two-trajectory census;
- every arm and the top level share the exact eight-file code identity;
- the manifest/config/assignment/role-index digests are the approved delivered state;
- the ledger contains no drive letter, backslash or local machine identity; and
- `config/config.json` remains absent.

The checkpoints are development-only. They do not carry a selected capacity, calibrated
threshold, held-out result or confirmatory authority.

## Finding W — disclosed for the historical producer

`dev_fit_trainer.py` at `caa00418...` can raise if its own dirty-refusal artifact name is
occupied by an unwritable file or directory. This edge is real, loud and non-destructive.
Codex ruled it **disclosed** because:

1. the authorized fit requires a fresh output directory, so the path is not on its graph;
2. no prior ledger/checkpoint bytes are destroyed; and
3. changing the fitted producer after the run solely for this edge would make the current
   packet's producer state diverge from the code identity recorded by every checkpoint.

If a later authorization admits reused/hostile output directories, or if the producer is
changed for another reason, W must close before that new state executes. Do not infer a
general waiver from this historical ruling.

## Finding X — separate in-sample analysis, not a rewritten fit ledger

The fit ledger records only total training loss/history. That total can be negative because
the severity Gaussian NLL contains a learned `log_scale` term, so it is not an interpretable
learning/ranking statistic by itself.

Codex added `scripts/analyze_dev_fit.py`. It:

- validates strict JSON, the complete matched plan and every arm binding;
- requires the fit result to name the current executable training state;
- loads only the exact authorized dev rows through production loaders;
- verifies each checkpoint digest before strict state-dict loading;
- runs inference only under the shared deterministic-convolution context;
- reports fixed-four-class accuracy/macro-F1 and the four separate post-fit loss terms;
- records exact fit/analysis code identities with bare labels only; and
- persists the no-generalization/no-selection/no-threshold boundary.

The tracked output is path-free and byte-identical on repeated regeneration.

## Exact development-only readback

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

The mean post-fit loss decomposition is:

```text
                         C1        S
class CE              +0.434    +0.557
location CE           +0.515    +0.557
severity Gaussian NLL -1.162    -1.116
OOD BCE               +0.023    +0.017
total                 -0.190    +0.016
```

The scores are computed on the same 152 examples used to fit each arm. They establish that
the end-to-end executable optimizes above simple in-sample baselines. They do **not**
establish generalization, a C1-versus-S result, OOD performance or a capacity choice.

The seed SD is about three times the Claim-Sheet 0.05 effect bar and is a real Gate-6
sample-size warning. It does not itself authorize more fit seeds or change the confirmatory
design. Any design consequence must be reviewed before later-role outcomes are read.

## Capacity boundary

Rung 1 uses the same 39,594-parameter network for both suites. S supplies four additional
nonzero gauge channels but receives no additional parameters. The adverse in-sample S-C1
direction is preserved publicly and does not establish that structural sensing is useless.
The preplanned capacity ladder is the instrument for testing whether this fixed rung is
undersized.

No next-rung implementation or fit is authorized by Session 84. It requires its own
reviewed executable state and explicit execution authority. Do not treat the completed
rung-1 fit as blanket permission to climb the ladder.

## Packet runbook state

`Reproducibility Packet/README.md` now contains:

- Step 26: plan mode and the fresh-directory ten-arm fit command;
- Step 27: the read-only in-sample analysis command and exact tracked artifact; and
- a current boundary that correctly says one development-only rung-1 fit has completed.

The tested PowerShell trainer form is:

```powershell
$env:PYTHONPATH = "scripts"
.\.venv\Scripts\python.exe -m utils.dev_fit_trainer ...
```

`python -m scripts.utils.dev_fit_trainer` is wrong for this packet because `utils` is the
expected import root.

## Trainer and contract states already closed

Both agents explicitly approve the fitted trainer state:

```text
Reproducibility Packet/scripts/utils/dev_fit_trainer.py
  caa00418b2f404575dca7cda167e6be76c99183a
Reproducibility Packet/tests/test_dev_fit_trainer.py
  cbc4064fddee8d2b548c95ddc32709dfbf0653e6
```

It enforces the assignment-derived window policy, exact delivered dev dataset, matched
five-seed/two-suite plan, production role loaders, eight-file code identity, complete
provenance before checkpoint persistence, fresh-output requirement and terminal evidence.

Both agents approve the development-fit contract:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py
  bd2c0d080f3046837af6fc38232b530749238e4c
Reproducibility Packet/tests/test_dev_fit_contract.py
  fbd941b592436d0303b2ddd6ec6c69906d08bd88
```

The generic `row_disclosure` remains free text in the closed contract; the trainer passes
only `DevRowCensus.disclosure()`, and the trainer test pins the producer behavior. Do not
reopen the contract unless a future executable ingress makes the field bound-permeable.

## Training-window policy — jointly settled

```text
origin_step(trajectory) = onset_step(trajectory) + lead_steps(split)
lead_steps(split)       = that split's diagnostic probe start offset
decision_step           = origin_step + 768
windows per run         = 1

dev diagnostic          onset 500 + lead 500 -> [1000, 1768)
dev ordinary            onset 400 + lead 500 -> [ 900, 1668)
```

Equal lead removes an avoidable time-since-onset difference. It does not make excitation
the only trajectory difference; target joints and task timing still differ. The arithmetic
is total over later splits but authorizes no later-role outcome read.

## Gate-4 rung 1 implementation — jointly approved

```text
Reproducibility Packet/scripts/utils/attribution_net.py
  c4fa3c63e7439236e09f4e5eeb08b7c76a6087ab
Reproducibility Packet/tests/test_attribution_net.py
  5a401ca14be170d0002c508111b7ce32a5291bb0
```

`TemporalAttributionNet` has 39,594 trainable parameters, a causal dilated temporal
convolution, 1,023-sample receptive field, fixed values/mask registry input and matched
C1/S capacity. Incoming weights/device transfer are validated on a deep copy and copied
into the existing live network so checkpoint attachment preserves transactionality, module
identity, optimizer references and provenance.

An unfitted instance remains uniform/abstaining with infinite severity uncertainty. The
ten fitted checkpoints are separate dev-only artifacts and do not turn the class into a
calibrated or confirmatory estimator.

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

The first dev fit advances one part of this sequence. It authorizes no pilot/validation
work, no threshold, no freeze and no confirmatory action.

## Amendment A2 and closed payload evidence

Amendment A2 remains jointly approved at:

```text
Claim Sheet.md              baa8fd53146bb838b673946b34fe435c77d8ec06
Accessible Claim Sheet.md   203aab77f1f244f0a11943955a6f8ec123944030
```

A2 retains the full payload/severity ladders, pre-registers payload-bounded structural
non-transfer and requires payload-stratified structural reporting. It leaves all original
numerical success, confidence, recall, tracking, seed and safety bars unchanged.

The one authorized payload-boundary result remains closed at canonical SHA-256
`7746372f1adea931722cf547adee36489971493c4e1b5217f588d4c6d1c9aa04`, outcome
`X_CASE_EMPTY`, complete mass coverage, replay pass and 127 extension rollouts. It licenses
no fitted curve, independence or mechanism claim and cannot change Protocol P, role
coverage or establish/refute the headline hypothesis.

## Verification state

Session 84 verification:

```text
analysis tests                       10 passed
analysis tests under python -O       10 passed; expected warning only
trainer + analysis focused           59 passed
focused under python -O              59 passed; expected warning only
full packet suite                     1,526 passed in 126.52 s
compileall                            clean
git diff --check                      clean
documented plan command               X_PLAN_OK; 10 arms; 0 fits; 0 rollouts
analysis regeneration                 byte-identical twice
checkpoint digests                    10 / 10 matched
analysis path disclosure              none
fits / generation / rollouts          0 / 0 / 0 in Codex Session 84
pilot / validation / test reads       0
config/config.json                    absent
```

## Public and authorization boundary

The root README remains Phase 2 / `In Progress`. Its newest entry records the first fit,
the in-sample/seed-sensitivity boundary, the adverse S-C1 direction and the precise
same-parameter/four-additional-nonzero-gauge-channel fact.

Absent separate explicit authorization, all remain blocked:

- any next capacity fit;
- pilot, validation or test outcome reads;
- capacity selection or probability/detection/abstention/OOD/uncertainty thresholds;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation or further payload measurement;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Transcript integrity

Session 84 used a verified unique physical EOF block and preserved the complete prefix:

```text
pre-write bytes          1,445,575
pre-write lines          22,897
pre-write SHA-256        5694c0c22377b9ff99fb9a0486779f15a43aa55ca3c26f7b72f23eae2cc01aa7
final bytes              1,451,674
final lines              23,022
header                    unique at line 22,901
diff                      +125 / -0
last                      Codex
```

The older Session-82 append-order recurrence remains preserved and corrected forward. Do
not derive or extend an append streak number from memory.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence
  are not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information,
  action authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Keep README updates lean and milestone-based.
