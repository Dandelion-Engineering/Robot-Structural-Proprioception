# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-05 — Codex Session 78

## Resume here

The project remains in **Phase 2 — Execution**. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent and confirmatory identities remain
unmaterialized. Protocol P v2.3.3, its development screens/readbacks, the payload-boundary
extension, and any future Gate-4 fit are development evidence only, never confirmatory or
final evidence.

The lifetime Protocol-P-related physical-rollout total is **278**: 151 before the
payload-boundary extension plus its one authorized 127-rollout invocation. That invocation
is spent. No second invocation or further payload measurement is authorized.

## Next exact action

Claude owns the next review turn. Re-open and genuinely review these reviewer-edited files:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py
  6541cebcbd78d10918d5d6ab58b5f5501340ebf9
Reproducibility Packet/tests/test_dev_fit_contract.py
  9df7d7f79a7120e42ab84a81ba3bd76b1494ec32
```

Codex explicitly approves these exact bytes. The loop is **OPEN** until Claude explicitly
approves the same state or edits and hands back a replacement. No fit may run before this
loop closes and the trainer/checkpoint/result executable state is itself jointly reviewed.

The next regular Codex progress report is Session 80. The next Codex session/report is
**79**.

## Gate-4 rung 1 — jointly approved implementation

Both agents explicitly approve:

```text
Reproducibility Packet/scripts/utils/attribution_net.py
  c4fa3c63e7439236e09f4e5eeb08b7c76a6087ab
Reproducibility Packet/tests/test_attribution_net.py
  5a401ca14be170d0002c508111b7ce32a5291bb0
```

The two review rounds closed paired silent-state defects:

1. Claude's original direct `load_state_dict` could partially mutate live tensors before
   raising while leaving the previous `training_provenance` attached.
2. Codex's first transactional repair validated on a candidate but rebound `self.net`,
   orphaning optimizers or callers that captured the original module.

The approved state validates the incoming dictionary and device transfer on a deep copy,
then writes the validated tensors into the existing live network object. It preserves
transactionality and object identity. The optimizer consequence test passes, as do
success/refusal identity and provenance tests.

Rung-1 facts:

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

## Development-only fitting contract — reviewer state open

Claude's original contract blobs were:

```text
dev_fit_contract.py                 73e5e743393ee5d0b0a2e548da6070bfceb1599e
test_dev_fit_contract.py            3959ff28cad18efd8e55c3e8786951d1cea78e51
```

Codex reproduced four defects and blocked that state:

- a duplicate suite/seed arm was collapsed by a set and accepted as a complete plan;
- the point-of-consumption guard accepted both empty input and `dev/C0` rows;
- a withheld `dev/C0` row was mislabeled as non-dev in the census disclosure; and
- a newline-bearing bare name could split the promised one-line provenance string.

The approved reviewer edit refuses duplicate fits, refuses empty/unmatched/cross-suite
consumption, distinguishes non-dev from unmatched-suite dev exclusions, and refuses ASCII
control characters in path-free names/labels. Claude's re-review is still required.

The contract's approved design direction, pending exact-state closure:

```text
authorized data                     persisted dev rows only
matched fit suites                  C1 and S
training seeds                      0, 1, 2, 3, 4
plan                                exact 10-arm suite x seed cross-product
authority                           DEVELOPMENT ONLY: ineligible for confirmatory
                                    analysis; cannot change Protocol P outcome or
                                    role-coverage counts.
assignment identity                 exact ASSIGNMENT_CANONICAL_SHA256 equality
configuration identity              dev- prefixed only
data-root record                    bare name plus manifest digest, never local path
source digest domain                canonical text
checkpoint digest domain            raw binary
```

The authority string remains local because importing an entry-point script into `utils`
is the wrong direction and moving the source would edit a closed executable. Tests pin the
literal by equality against the extension script and frozen protocol document.

## Development-only fitting authorization

Session 77 opened the **conceptual** Gate-4 dev-fitting gate. Training rung 1 against the
already-delivered development partition does not require new data generation. Amendment A2
did not independently grant this permission.

The authority is exact:

1. Read only persisted rows whose role is exactly `dev` from the jointly approved delivered
   base dataset. Pilot, validation, and test outcomes remain unread.
2. Generate no plant, sensor, label, or role payload and spend zero physical rollouts.
3. Hold architecture and training protocol identical across C1/S and run only the five
   predeclared independent training seeds in both arms.
4. Every checkpoint/result carries the exact development-only authority and the dev data
   root, manifest/config/assignment identities, suite, training seed, training-protocol
   code identity, row disclosure, and checkpoint digest.
5. A dev fit may establish learnability or expose implementation failures. It may not set
   validation-owned probability/detection/abstention/OOD/uncertainty thresholds, select a
   headline capacity from later roles, or become a research result.

Before execution, close the current contract review, then build and jointly review the
trainer and its checkpoint/result writer. The trainer and evaluation driver must use the
same `deterministic_conv_precision()` scope for forward/backward computation. Once those
exact executable bytes close under these bounds, no additional conceptual permission is
needed for the dev-only fits.

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

The full identities remain in `HumanReport78.md`; the short forms above are navigation.

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

Claude corrected the stale post-freeze wording in both `utils/estimator.py` and
`utils/__init__.py`; Codex approves those changes and the packet README as-is:

```text
estimator.py                        b2abf463d9a4b2678f182568f50417774a6191e7
utils/__init__.py                   04647db4f61b18aac33e088543c6c49d54feb584
Reproducibility Packet/README.md    ebef72fef5e423779901ba8a47529ae64d6a4433
```

This sequence does not authorize pilot or validation work now.

## Verification of the current reviewer state

```text
direct adversarial probes           all corrected boundaries refuse
focused tests                       126 passed
focused tests under python -O       126 passed
full packet suite                   1,432 passed in 130.27 s
compileall                          clean
payload files read                  0
fits / checkpoints / generation    0 / 0 / 0
rollouts                            0
config/config.json                  absent
```

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
or fault-grid entry. It shifts no seed ordinal and by itself invalidates no delivered datum.
Any later dataset supersession is separate and requires its own authorization and archive /
exclusion trail.

## Closed payload-boundary evidence

Both agents approve the protocol, executable/test state, official plan, and exact result:

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
`d06f844b9476c1c43f4b74cb5edce4d7e413b0e1`. Session 78 deliberately added no public
entry: the model is untrained, the trainer does not exist, and the contract loop is open.

Absent a new separately explicit authorization, all remain blocked:

- fitting before the contract and trainer executable reviews close;
- any pilot, validation, or test outcome read;
- any new dataset generation, replacement, supersession, or regeneration;
- any second payload-extension invocation or further payload measurement;
- final `config/config.json` materialization;
- confirmatory identities, generation, reads, or claims; and
- changes to closed Protocol P v2.3.3.

## Transcript integrity state

Session 78 appended from a verified unique physical EOF block at:

```text
pre-write bytes    1,337,850
pre-write lines    20,937
pre-write SHA-256  70518b713090a9e595ec5b78089acd558f60a527fbe24f453cb6feb10898c43f
```

The prefix remained byte-identical; the new header occurs once after the boundary; Codex
is physically last; the diff is `+108/-0`; and the transcript now has 1,343,389 bytes /
21,045 lines. No repair was needed.

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
