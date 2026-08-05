# Codex — Human Report, Session 77

**Date and time:** 2026-08-05 06:14 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.

---

## Summary

This session reviewed Claude Session 77's first learned attribution rung, reproduced one
checkpoint-provenance defect in the exact handed-off implementation, repaired it directly,
and handed a replacement exact two-file state back for Claude's genuine owner re-review.

The submitted architecture is the Claim Sheet's Gate-4 rung 1: a 39,594-parameter causal
temporal-convolutional network behind the existing `DiagnosisEstimator` interface. It uses
the same fixed-width values-plus-validity-mask input and the same parameter count for C0,
C1, and S; has a 1,023-sample receptive field over the proposed 768-sample window; keeps
normalization causal; abstains when unfitted; leaves thresholds and calibrated predictive
uncertainty to Gate 5; and carries a CPU-portable PyTorch pin with a verified CUDA build on
the project machine.

I approved those design choices, but not Claude's original exact state. PyTorch's
`load_state_dict` may copy compatible tensors before raising on a missing or incompatible
key. In a direct reproduction, an attempted replacement changed `input_proj.weight`, then
raised because `severity_head.bias` was missing, while the estimator retained the old
`training_provenance`. The live model was therefore a mixed state falsely labeled as the
old run.

I changed the loader to operate on a deep-copied candidate and install it only after the
entire state dictionary and device transfer succeed. A new regression test proves that a
failed replacement leaves both every live tensor and the prior provenance unchanged. I
explicitly approved the reviewer-edited state:

```text
Reproducibility Packet/scripts/utils/attribution_net.py
  80d7639f3df3a40b61c4229c4cf06649d1f613ae
Reproducibility Packet/tests/test_attribution_net.py
  861b8e83f6481da34668087cba238e356a13ed40
```

The review cycle remains open because Claude has not yet re-opened and explicitly approved
these reviewer-edited bytes.

## Independent review of the architecture and shared documentation

The following parts of Claude's implementation survived review:

1. **Matched-suite capacity.** C0, C1, and S all enter the identical network. Missing
   channels are represented by zero values accompanied by false validity-mask channels,
   so the sensor suite changes information rather than model capacity.
2. **Causality.** Each dilated convolution is left-padded and the per-step `LayerNorm`
   operates over channels, not time. Perturbation tests establish that later samples do
   not change earlier features and independently demonstrate that a time-mixing
   normalization would fail the same check.
3. **Honest unfitted behavior.** An estimator without attached weights returns uniform
   four-class probability, abstains, reports no location, leaves detection unset, and
   reports infinite severity uncertainty rather than interpreting random initialization.
4. **Calibration boundary.** The raw severity scale is deliberately exposed only under a
   `raw_` name. The schema-facing uncertainty remains infinite until Gate 5 produces a
   bias-inclusive calibrated predictive scale.
5. **Capacity ladder and efficiency.** Rung 1 is the only built learned rung and the
   constructor refuses parameter counts outside the Claim Sheet's 10,000–100,000 band
   unless a caller explicitly waives the guard for tests.
6. **Device portability.** The installed project build is `torch==2.11.0+cu128`, CUDA 12.8
   is available on the RTX 5060 Ti, and the base `torch==2.11.0` requirement keeps a CPU
   installation possible. The model's full-float32 convolution context restores the
   global flag after use.

I accepted Claude's unchanged requirement and packet-README blobs:

```text
Reproducibility Packet/requirements.txt  3b103c526ae263dcc1c566fbac740b4452d18ffc
Reproducibility Packet/README.md         9f4a1d592c2c9f1b5f10e575136b0199ab860d72
```

The root public README's new learned-model entry ended by saying that training required
blocked data generation. That was inaccurate because the jointly approved delivered
development partition already exists. The running log is append-only, so I preserved the
original text and appended a short forward scope correction rather than rewriting history.
I explicitly approved the resulting root README blob:

```text
README.md  d06f844b9476c1c43f4b74cb5edce4d7e413b0e1
```

## Training-authorization ruling

I ruled that fitting rung 1 against the already-delivered `dev` partition is authorized
as development evidence. Training does not itself require new simulation or payload
generation. Amendment A2 did not independently grant that permission; this session opens
the bounded fitting gate under the already-approved Config Freeze Readiness sequencing.

The authorization is deliberately narrow:

- input rows must be persisted `dev` rows from the jointly approved base dataset;
- no pilot, validation, or test outcomes may be read during this step;
- no plant, sensor, label, or role payload may be generated, so rollout cost stays zero;
- the matched suites use the same architecture and training protocol with at least five
  predeclared independent training seeds;
- every checkpoint and result remains development-only and records the dev data root,
  manifest/config/assignment digests, suite, seed, training protocol/code identity, and
  checkpoint digest; and
- a dev fit may test whether the implementation learns or expose defects, but may not set
  validation-owned probability, detection, abstention, OOD, or uncertainty thresholds or
  become a research result.

The conceptual gate is open, but no fitting may begin yet. Claude must first close the
current two-file owner re-review. The trainer, checkpoint/result schema, data-role refusal,
and seed/suite plan must then be implemented and jointly reviewed. After that executable
review closes under these bounds, no additional conceptual permission is needed for the
dev-only fits.

## Freeze-order ruling

Claude correctly identified a contradiction between `utils/estimator.py` and the
jointly approved Config Freeze Readiness Review. The review governs:

```text
draft config and role-separated storage
  -> model implementation
  -> dev/pilot fitting and capacity/hyperparameter work
  -> validation-only calibration and threshold selection
  -> final immutable config.json freeze
  -> untouched confirmatory generation/read
```

The old sentence saying learned rungs are trained only after final `config.json` freeze is
stale and must be corrected forward. The final configuration cannot contain selected model
and threshold choices before those choices exist. This sequencing ruling does not yet
authorize pilot or validation work; the only newly open execution class is the bounded dev
fit described above.

## Verification

```text
original-state partial-load reproduction
  exception                           RuntimeError
  input_proj.weight changed           yes
  previous provenance remained        yes

reviewer-edited focused suite         65 passed in 2.21 s
reviewer-edited focused suite, -O     65 passed in 3.85 s
full packet suite                     1,371 passed in 128.92 s
compileall                            clean
installed torch                       2.11.0+cu128
CUDA                                  12.8, available
GPU                                   NVIDIA GeForce RTX 5060 Ti
config/config.json                    absent
rollouts                              0
```

The optimized-Python run emitted only pytest's expected warning that ordinary assertions
outside test modules are disabled under `-O`; every test still passed.

## Transcript integrity

Before appending the response, the authoritative Phase-2 transcript was 1,316,541 bytes /
20,550 lines with SHA-256
`4adcc30b6ed1682f9b651a190edecbc444f3ca5c6b410ddce00591017cd0722f`.
The complete final Claude block used as the patch anchor occurred exactly once at the
physical EOF.

Post-write checks passed:

- the complete 1,316,541-byte prefix is byte-identical at the same SHA-256;
- the Session-77 header occurs exactly once at line 20,554, after the recorded boundary;
- Codex is physically last;
- the transcript is now 1,322,488 bytes / 20,675 lines; and
- the Git diff is additions-only at `+125/-0`.

No transcript repair was needed.

## Files created or updated

- `Reproducibility Packet/scripts/utils/attribution_net.py` — transactional checkpoint
  installation
- `Reproducibility Packet/tests/test_attribution_net.py` — failed-load atomicity and
  provenance regression
- `README.md` — append-only public scope correction
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — exact-state review, training/freeze rulings, verification, and owner handback
- `agents/Codex/Session Summaries/HumanReport77.md` — this report
- `agents/Codex/README.md` — workspace index and active gate state
- `agents/Codex/Summary of Only Necessary Context.md` — rewritten resume state

The `.gitignore` already ignores `.agent-session.lock`; no ignore update was needed.

## Next steps

1. Claude must genuinely re-review and either explicitly approve blobs `80d7639...` /
   `861b8e8...` or edit and return a new state. Training remains blocked until then.
2. Claude should correct the stale post-freeze training sentence in `utils/estimator.py`.
3. Build and jointly review the dev-only trainer, checkpoint/result schema, strict role
   refusal, and matched five-seed suite plan; then run only the authorized dev fits.
4. Keep pilot, validation, test, final `config.json`, further payload measurement, and all
   confirmatory work blocked until separately authorized.
5. The next regular Codex progress report remains Session 80.
