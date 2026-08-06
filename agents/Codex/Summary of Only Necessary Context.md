# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-06 — Codex Session 82

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. All development screens/readbacks, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2 and any Gate-4 fit are development evidence only.

The lifetime Protocol-P-related physical-rollout total remains **278**: 151 before the
payload-boundary extension plus its one authorized 127-rollout invocation. That invocation
is spent. No second invocation or further payload measurement is authorized.

## Next exact action

Claude owns the next turn. Genuinely owner-review the reviewer-edited trainer state:

```text
Reproducibility Packet/scripts/utils/dev_fit_trainer.py
  788fc240c404797f883c08fc843296f277412643
Reproducibility Packet/tests/test_dev_fit_trainer.py
  c95bd8fbb5cf3dcb5d99bfb7f22799d738dcb0f7
```

Codex explicitly approves those exact bytes, including the assignment-derived training
window policy. Claude must preserve or contest Findings O–R and the implementation, then
explicitly approve or hand back a changed exact state. **No development fit may run until
that executable loop closes.** The next regular Codex progress report is Session **88**;
the next Codex session/report is **83**.

## Training-window policy — accepted

The policy derives one window per trajectory from the approved assignment:

```text
origin_step(trajectory) = onset_step(trajectory) + lead_steps(split)
lead_steps(split)       = that split's diagnostic probe start offset
decision_step           = origin_step + 768
windows per run         = 1

dev diagnostic          onset 500 + lead 500 -> [1000, 1768)
dev ordinary            onset 400 + lead 500 -> [ 900, 1668)
```

The diagnostic line exactly reproduces Protocol P v2.3.3 §8. The ordinary line uses the
same prospectively fixed post-onset lead rather than introducing a second chosen number.
One window per row avoids an unregistered stride and correlated-window multiplication.

Equal lead removes an avoidable time-since-onset difference; it does **not** make
excitation the only trajectory difference. The assignment also changes target joints and
task timing. The same arithmetic is total over the reserved pilot/validation/test design,
but that fact authorizes no later-role outcome read.

## Trainer review — reviewer corrections awaiting Claude

Claude Session 82 preserved all six Session-81 corrections and fixed the handler defect
where `DevFitContractError` / `DevFitDataError` were swallowed as generic `RuntimeError`.
Codex accepts those changes and added four further corrections:

### Finding O — exact pair identity and schedule coverage

Equal per-trajectory C1/S counts were insufficient: a scheduled trajectory missing from
both suites and disjoint equal-count `pair_id` sets both passed. The reviewer state now
requires every scheduled trajectory and exact per-trajectory C1/S `pair_id` equality.

### Finding P — persisted label-onset binding

The assignment-derived schedule is now cross-checked against the independent persisted
`onset_index` and `onset_time_s` before a row is windowed. The real delivered dev labels
all agree: ordinary 400 / 0.8 s and diagnostic 500 / 1.0 s, with 76 C1 and 76 S rows per
trajectory.

### Finding Q — strict schedule-control refusal

Claude's handed-off blob accepted `window_steps=True` as a one-step window and leaked raw
`TypeError` / `ZeroDivisionError` for an empty probe and zero control period. The reviewer
state validates assignment shape, ids, probe shape, positive non-bool window length, the
fixed positive development control period and boolean probe flag under
`DevFitContractError`.

### Finding R — stale checkpoint population

A partial rerun into the same directory could mix old and current deterministic checkpoint
names. The reviewer state refuses a prior `dev_fit_result.json` or any
`dev_fit_*_seed*.pt` before the first fit. A plan artifact alone remains allowed.

The Session-81 protections remain intact:

- online-equivalent `availability_time_s <= decision_time_s` masking;
- exact data-root, manifest, config and three role-index pins before payload access;
- hash-checking `DeployableObservationLoader` / `RolePayloadLoader` ingress;
- eight-module code identity across plan and all arms;
- in-memory checkpoint serialization, digest and validated provenance before write;
- one full training protocol in plan, arm and terminal artifacts;
- non-finite loss/weight, device, runtime and serialization refusal; and
- complete arm records on partial failure plus all named `main()` exits driven.

## Verification of the reviewer state

```text
focused trainer tests                37 passed
focused under python -O              37 passed; expected warning only
full packet suite                    1,504 passed in 128.96 s
compileall                           clean
git diff --check                     clean
production plan probe                X_PLAN_OK; 10 arms; 0 fits; 0 rollouts
selected real manifest rows          304 dev; 640 withheld
exact real pairing                   76 C1 / 76 S pairs per trajectory
real payload reads                   304 dev labels; 0 observations
pilot / val / test outcomes          0 reads
fits / checkpoints / results         0 / 0 / 0
generation / rollouts                0 / 0
config/config.json                   absent
```

## Development-fit contract — jointly closed

Both agents approve:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py
  bd2c0d080f3046837af6fc38232b530749238e4c
Reproducibility Packet/tests/test_dev_fit_contract.py
  fbd941b592436d0303b2ddd6ec6c69906d08bd88
```

The generic `row_disclosure` remains free-text in the closed contract; the trainer passes
only `DevRowCensus.disclosure()`, and the trainer test pins that producer behavior. Do not
reopen the contract unless a future executable ingress makes the field bound-permeable.

## Gate-4 rung 1 — jointly approved but untrained

Both agents explicitly approve:

```text
Reproducibility Packet/scripts/utils/attribution_net.py
  c4fa3c63e7439236e09f4e5eeb08b7c76a6087ab
Reproducibility Packet/tests/test_attribution_net.py
  5a401ca14be170d0002c508111b7ce32a5291bb0
```

`TemporalAttributionNet` has 39,594 trainable parameters, a causal dilated temporal
convolution, 1,023-sample receptive field, fixed values/mask registry input and matched
C1/S capacity. Incoming weights/device transfer are validated on a deep copy, then copied
into the existing live network to preserve transactionality, module identity, optimizer
references and provenance. Unfitted behavior remains uniform class probability, abstain,
no localization/detection and infinite severity uncertainty.

The model is **untrained**. Approved implementation is not permission to fit.

## Exact development-only fitting authority

Conceptual dev-only fitting is authorized against the already-delivered `dev` partition,
but execution still requires Claude's exact-state trainer approval.

1. Read only persisted rows whose role is exactly `dev` from the approved delivered base
   dataset. Pilot, validation and test outcomes remain unread.
2. Generate no plant, sensor, label or role payload and spend zero physical rollouts.
3. Hold architecture and training protocol identical across C1/S and run only network
   seeds 0, 1, 2, 3 and 4 in both arms.
4. Use a fresh output directory. Each checkpoint/result carries exact development-only
   authority; data, assignment and code identities; suite/seed; training protocol;
   schedule; row disclosure; role-index hashes; and raw checkpoint digest.
5. A dev fit may establish learnability or expose implementation failure. It may not set
   validation-owned probability/detection/abstention/OOD/uncertainty thresholds, choose a
   headline capacity from later roles or become a confirmatory research result.

The trainer and evaluation driver must share `deterministic_conv_precision()` across
forward and backward computation. Execution is exactly the ten arms from
`matched_fit_plan()`, with `require_dev_only(rows, suite=...)` at consumption and
`require_complete_matched_plan(done)` before any comparison.

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

This sequence does not authorize pilot or validation work now.

## Amendment A2 and closed payload evidence

Amendment A2 remains jointly approved at:

```text
Claim Sheet.md              baa8fd53146bb838b673946b34fe435c77d8ec06
Accessible Claim Sheet.md   203aab77f1f244f0a11943955a6f8ec123944030
```

A2 retains the full payload/severity ladders, pre-registers payload-bounded structural
non-transfer and requires payload-stratified structural reporting. All original numerical
success, confidence, recall, tracking, seed and safety bars remain unchanged. A2 itself
adds or supersedes no delivered data.

The one authorized payload-boundary result remains closed at canonical SHA-256
`7746372f1adea931722cf547adee36489971493c4e1b5217f588d4c6d1c9aa04`, outcome
`X_CASE_EMPTY`, mass coverage complete, replay pass, 127 extension rollouts. It licenses
no fitted curve, independence or mechanism claim and cannot change Protocol P, role
coverage or establish/refute the headline hypothesis.

## Public state and authorization boundary

The root README remains Phase 2 / `In Progress`. Session 82 deliberately added no public
entry: the trainer loop is open and no fit has run. The packet README likewise remains
unchanged until the trainer closes; it owes an execution step then.

Absent separate explicit authorization, all remain blocked:

- any fit before Claude approves the exact reviewer-edited trainer bytes;
- pilot, validation or test outcome reads;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation or further payload measurement;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Transcript integrity and recurrence

The first Session-82 technical review append used a repeated single-line signature rather
than the complete unique EOF block that had been verified. It landed at line 19,334 before
the recorded 22,206-line tail. The verifier caught it before commit. The misplaced review
was preserved and a complete decision-bearing correction was appended from a new unique
EOF block.

Final technical transcript:

```text
bytes      1,414,699
lines      22,349
SHA-256    dca21bf5406e4dda735d986a66257111c3a3c50a6c78f715ba7cc81072c625ae
diff       +143 / -0
last       Codex; correction header unique at line 22,313
```

The recurrence is reported in the director-visible monitoring thread. Its first note
landed in order but normalized CRLF inside its EOF context; that byte-prefix failure is
also preserved and corrected forward. Final monitoring transcript:

```text
bytes      12,617
lines      204
SHA-256    a76596a0788013b0e54f02533069c96bd758b097e249e4c97d75a9e51210335f
diff       +51 / -0
last       Codex; byte-correction header unique at line 189
```

The operational rule remains absolute: record byte/line/hash boundary, verify a complete
unique physical EOF block, use that **same full block** in the patch, then require one
post-boundary header, exact prefix, additions-only diff and physically last author. A
failed assertion requires a forward correction, not deletion.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence
  are not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information,
  action authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Keep README updates lean and milestone-based.
