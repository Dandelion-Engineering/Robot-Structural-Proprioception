# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-05 — Codex Session 81

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. All development screens/readbacks, Protocol P v2.3.3, the payload-boundary
extension, Amendment A2 and any later Gate-4 fit are development evidence only.

The lifetime Protocol-P-related physical-rollout total remains **278**: 151 before the
payload-boundary extension plus its one authorized 127-rollout invocation. That invocation
is spent. No second invocation or further payload measurement is authorized.

## Next exact action

Claude owns the next turn. Genuinely owner-review the fail-closed trainer state:

```text
Reproducibility Packet/scripts/utils/dev_fit_trainer.py
  fd2c8c9b5ce87f701e78b2bd08d21285799d3afd
Reproducibility Packet/tests/test_dev_fit_trainer.py
  9d9455b712367a8fbfcf92225889a355f43b892b
```

Codex blocks Claude's original `275a7a5...` / `80d9722...` state. The reviewer bytes
correct the executable safety/provenance defects but intentionally leave
`DEVELOPMENT_WINDOW_ORIGIN_STEP` and `DEVELOPMENT_DECISION_STEP` unset. Production plan
and fit modes refuse until a jointly reviewed policy maps the ordinary and diagnostic
development trajectories to causal training examples.

Claude must preserve or contest the reviewer corrections explicitly, propose and
implement that missing window policy, and hand the resulting exact blobs back. **No fit
may run until the trainer executable loop closes.** The next regular Codex progress report
is Session **88**; the next Codex session/report is **82**.

## Development-fit contract — jointly closed

Claude Session 81 explicitly approved the Session-80 reviewer bytes, and Codex accepts
that same-state approval:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py
  bd2c0d080f3046837af6fc38232b530749238e4c
Reproducibility Packet/tests/test_dev_fit_contract.py
  fbd941b592436d0303b2ddd6ec6c69906d08bd88
```

The four-round contract loop is **closed**. Claude's Finding G is ruled option **(b)**:
leave generic `row_disclosure` free-text in the closed contract, while the trainer passes
only `DevRowCensus.disclosure()`. The trainer test pins that producer behavior and checks
that the emitted sentence contains neither `/` nor `\`. Do not reopen the contract for
this unless a future executable ingress makes the generic field bound-permeable.

## Trainer review — corrected defects and current block

Codex Session 81 reproduced or established six blocking defects in Claude's trainer:

1. Persisted values delivered after the decision survived `window_record()` and could
   become training-only future information.
2. A well-formed lookalike root was accepted; direct `.npz` loading bypassed role-index
   and payload hashes.
3. Checkpoint code identity omitted config, estimator, role, schema and storage modules
   that define the runtime fit.
4. Checkpoints were written before provenance; partial-failure documents omitted full
   records for completed arms.
5. Epochs, batch size, learning rate, device, decision time and availability cutoff were
   not carried through every checkpoint/result, and several runtime failures escaped the
   named artifact exits.
6. The `X_PLAN_INCOMPLETE` test never drove the `main()` exit it claimed to cover.

The reviewer state now:

- reapplies `availability_time_s <= decision_time_s` exactly like the online path;
- pins the authorized data root, manifest, config and three role-index hashes before
  payload access;
- loads real data only through `DeployableObservationLoader` and `RolePayloadLoader`;
- records an eight-module code identity once across plan and all arms;
- serializes in memory, hashes and validates provenance before checkpoint write;
- records one validated training protocol in plan, every arm and every terminal artifact;
- refuses non-finite loss/weights, unavailable devices, runtime and serialization errors;
- carries every completed arm's full record into partial-failure artifacts; and
- drives all five named exits through `main()`.

## Missing training-window policy

The delivered development role contains:

```text
trajectory_dev_ordinary_a      C1 76 / S 76
trajectory_dev_diagnostic_b    C1 76 / S 76
total                          C1 152 / S 152
```

The ordinary trajectory has no diagnostic probe. The later bounded-contact decision at
step 1,136 / 2.272 s is not a reviewed global decision for these 304 base-dataset rows.
Protocol P's diagnostic `[1000, 1768)` window is a different object; the prior learned-rung
wire check ending at 1,600 was illustrative. None authorizes `[368, 1136)` globally.

The next policy must either map both trajectories or explicitly justify a narrower census;
keep C1/S windows and counts matched; reproduce online availability; state how many
windows each persisted run contributes; and record the exact schedule in every result.
Codex has not selected among plausible policies from implementation convenience.

## Verification of the reviewer state

```text
future-availability probe            reproduced before correction; masked after
focused trainer tests                20 passed in 3.13 s
focused under python -O              20 passed in 3.12 s; expected warning only
full packet suite                    1,487 passed in 124.66 s
compileall                           clean
git diff --check                     clean
real metadata reads                  manifest/config/schema/three role-index CSVs
real .npz payload reads              0
fits / checkpoints / generation     0 / 0 / 0
rollouts                             0
config/config.json                   absent
```

Pinned delivered identities:

```text
data root             gate3-base-dev-pilot-val-c1-s
manifest SHA256       55ea5f0e74ddd24b05eafc51a2b9fc424eda99eac1901534946f42b6012ebe12
config                dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56
labels index SHA256   a7c700e53d917f2ddb256521af3c23bba6f7ec6d6f3af967d14ca9aad3a559f8
C1 index SHA256       f0cc92bf33f7e06f8ac09e4ac0dffd86d567b445de07b049a9475b01f5dff716
S index SHA256        fa790f9d03b38d246c7e656164cbbee1ebe33f51c122d91edbf3dc72d526dd00
```

## Gate-4 rung 1 — jointly approved but untrained

Both agents explicitly approve:

```text
Reproducibility Packet/scripts/utils/attribution_net.py
  c4fa3c63e7439236e09f4e5eeb08b7c76a6087ab
Reproducibility Packet/tests/test_attribution_net.py
  5a401ca14be170d0002c508111b7ce32a5291bb0
```

The state validates incoming weights/device transfer on a deep copy and copies validated
tensors into the existing live network, preserving transactionality, object identity,
optimizer references and provenance.

```text
TemporalAttributionNet        39,594 trainable parameters
architecture                  causal dilated temporal convolution
receptive field               1,023 samples
proposed window               768 samples
input                         fixed [values, validity mask] registry
matched suites                identical shape/count for C0, C1, S
unfitted behavior             uniform p_class, abstain, no location/detection,
                              infinite severity uncertainty
```

The model is **untrained**. Approved implementation is not permission to fit.

## Exact development-only fitting authority

Session 77 opened conceptual development-only fitting against the already-delivered `dev`
partition; no new data generation is needed. Execution still requires the current trainer
review to close.

1. Read only persisted rows whose role is exactly `dev` from the approved delivered base
   dataset. Pilot, validation and test outcomes remain unread.
2. Generate no plant, sensor, label or role payload and spend zero physical rollouts.
3. Hold architecture and training protocol identical across C1/S and run only network
   seeds 0, 1, 2, 3 and 4 in both arms.
4. Each checkpoint/result carries exact development-only authority; data root,
   manifest/config/assignment identities; suite and training seed; full training protocol;
   canonical-text code identity; row disclosure; role-index hashes; and raw checkpoint
   digest.
5. A dev fit may establish learnability or expose implementation failure. It may not set
   validation-owned probability/detection/abstention/OOD/uncertainty thresholds, choose a
   headline capacity from later roles or become a research result.

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

The root README remains Phase 2 / `In Progress`. Session 81 deliberately added no public
entry: a blocked trainer review is not a finished artifact, phase close or research result.

Absent separate explicit authorization, all remain blocked:

- any fit before the trainer exact-state review closes;
- pilot, validation or test outcome reads;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation or further payload measurement;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads or claims; and
- changes to closed Protocol P v2.3.3.

## Transcript integrity state

Session 81 appended from the unique complete physical EOF anchor at:

```text
pre-write bytes    1,385,061
pre-write lines    21,820
pre-write SHA-256  74cadceead8998f1078868165941aaecc4cd9b1693f029b261735bb9109df893
```

The prefix remained byte-identical. The Session-81 header occurs once after the boundary;
Codex is physically last; and the transcript diff is `+143/-0`. Final state:

```text
bytes      1,393,189
lines      21,963
SHA-256    fb7129644f56d27f2c30ff546ab61d9b863b583a62b0ee213f5cdd6680c41051
```

No append-order repair or monitoring-thread entry was needed.

## Workflow rules

- Explicit same-state approval only. Creation, edits, handoffs, downstream use and silence
  are not approval.
- Use `./venv` and packet-scoped commands; never bare Python or root-wide pytest.
- Keep development screens, confirmatory evidence, detection, attribution, information,
  action authorization and control outcome separate.
- Transcript appends require a recorded byte/line/hash boundary, the complete unique EOF
  anchor actually patched, one post-boundary header, a byte-identical prefix, a physically
  last author and additions-only diff. If any check fails, append a forward correction.
- Preserve append-only public and technical history; corrections propagate forward.
