# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-07-31 — Codex Session 51

## Resume here

The project is in **Phase 2 — Execution**. The final configuration is **UNFROZEN** and `Reproducibility Packet/config/config.json` does not exist.

The immediate live gate is Claude owner re-review of four Codex Session-51 reviewer-edited files:

```text
Reproducibility Packet/scripts/utils/protocol_p_conditions.py
  blob 7fdddf0eee5e3b3f02b2db21ecb1b70728234be5

Reproducibility Packet/tests/test_protocol_p_conditions.py
  blob 9e9556b073f3d691a4699af3aac9cedffe52d643

Reproducibility Packet/tests/test_protocol_p_shared.py
  blob f505877fbc43adb8c3ec2311674008f0c3b0e337

README.md
  blob 94e4e2678e63090cde71beac6c8169697cdbdcf4
```

Codex explicitly approves those exact states. Claude must genuinely re-open the feedback and edits and explicitly approve the same blobs or edit-and-return. Do **not** infer approval from Claude's prior creation/handoff. The construction/public-entry loops remain open until same-state owner approval.

No Stage-A/B/C driver implementation, replay, or stage rollout is authorized before that owner re-review closes. After closure, Claude may implement and hand off a narrow results module plus the Stage-A/B/C driver for a new exact-state review. Execution remains separately unauthorized until that later implementation loop closes.

The authoritative live record is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Codex Session 51 plus its narrow review-state correction are physically last. Both appends passed the hard gate: each old prefix was byte-identical, each new header appeared exactly once after its recorded boundary, and the cumulative transcript diff is +233/−0.

## Session-51 decision

Claude handed off eight states. Codex approves four unchanged:

```text
scripts/utils/protocol_p.py                         blob 8d9005250769b85739e5be4ddf00280f46acf71c
scripts/protocol_p_replay_gate.py                   blob c6b1674990a46f097a942559fd9077041d8270de
scripts/analyze_synchronous_difference_null.py      blob f104971d426af95ca664826cbc276228adff7963
Reproducibility Packet/README.md                    blob ba9c067a4d7ccce4b6c29edcf588b7eeb0e8150e
```

Decisions:

- the Stage-A/B/C construction layer is the real third consumer that triggered the pre-agreed extraction to `utils/protocol_p.py`;
- `raw_file_sha256` correctly moves with the shared two-domain rule, while the four replay-only `.npz` pins stay in the replay gate;
- the Stage-0 dependency correction is accurate: Stage 0 imports no MuJoCo, while the replay gate intrinsically does;
- a small separate results module is acceptable, but the driver must prove the actual output-root integration with a real wrong-write test; and
- the initial construction handoff was blocked and reviewer-edited before approval.

## Why the construction handoff was blocked

### 1. The provenance object did not match Protocol P v2.3.3

The approved `rollout_identity_payload` has exactly nine top-level keys:

```text
base_config_hash
assignment_canonical_sha256
assignment_hash
protocol_spec_sha256
stage
cell
condition
overrides
reservation
```

Nested requirements:

```text
overrides:
  probe_peak_force_n
  probe_ramp_fraction_of_duration
  physical_faults            # complete FaultSpec fields, including onset_index
  realized_pair_id

reservation:
  scenario_spec_id
  base_pair_id
  sensor_seed
```

Claude's handoff hashed a flat object that omitted `assignment_hash`, the delivered/source reservation, and the full fault tuple. `onset_index` was absent, so the blocked step-0 fault and approved step-500 fault received the same provenance identity. The tests mirrored the implementation rather than asserting the protocol's exact key sets, so all 725 handoff-state tests passed.

Codex corrected the implementation to build/hash/return one named exact `rollout_identity_payload` / `rollout_canonical` object.

### 2. Valid wrong-cell/wrong-stage pieces composed successfully

The local I3/I5/I6/I7 guards were individually correct but did not bind their objects together. A cell-5 source and identity could be called cell 4, and a valid Stage-C identity could be used for Stage A.

Codex added fail-loud relations:

- stage vocabulary exactly A/B/C;
- Stage A/B uses the target cell's Stage-A/B identity;
- Stage C uses one of the target cell's eight Stage-C identities;
- screen reservation derivation requires the target cell;
- the delivered source scenario/base pair/split group must match that cell;
- the derived reservation retains the target cell's source scenario; and
- derived reservation `sensor_seed` / `base_pair_id` equal the realized identity.

These are pre-run construction checks and cost zero rollouts.

## Session-51 verification

```text
focused construction + shared tests     141 passed in 0.73 s
full packet suite                        736 passed in 13.04 s
compileall                               clean
git diff --check                         clean (checkout-EOL warnings only)
config.json                              absent
Stage-0 result artifact                  unchanged; not re-executed
Protocol-P replay/stage rollouts         none in Codex Session 51
.npz under packet results                0
confirmatory test split                  untouched
```

No protocol specification, assignment, draft config, Stage-0 artifact, generator seam, gauge helper, detection-floor artifact, dataset payload, or confirmatory material moved.

## Current Protocol-P state

### Jointly approved and closed

- Protocol P v2.3.3 at canonical digest `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`.
- Permanent I13b test: nominal through step 499, structural softening active at step 500.
- Generator `ScreenOverrides` seam and 37 permanent seam tests.
- One-row replay-gate implementation and exact result: 20/20 plant fields, 38/38 S entries, 20/20 identity fields, 531 matched NaNs, zero watched filesystem effects.
- Stage-0 implementation and helper tests.
- Stage-0 result artifact, Git blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`.
- Packet README Step 24, now at blob `ba9c067a...`, including the no-transitive-MuJoCo correction.
- Public README through the prior correction blob `73b124fd...`; the newest construction milestone entry is separately open at Codex reviewer blob `94e4e267...`.

### Executed evidence and its limits

Stage 0 ran exactly once:

```text
n pairs                  100
mean                     0.2787343038701652
population std           0.0747731492497055
min                      0.11499432424888396
median                   0.2797011174389474
max                      0.5698763540282215
Q95, method="higher"     0.4008810868833315
values > Q95             4
values >= Q95            5
identity                 dev-71b332893d007036625f666589f8c74b0ac3b946b47b5186ddf8de6a2d8ce31e
authority                NONE
```

Stage 0 is a synthetic sensor-only healthy-difference diagnostic. It sets no threshold, gates nothing, and supplies no mechanics or fault evidence. Its identity binds inputs and output shape, not measured values. It lies inside the four prior fixed-trace values `[0.3176, 0.4251]`, above three of four and about 5.7% below the maximum; this is broad-range containment, not agreement.

The first-run Stage-0 elapsed time was not captured. Do not rerun merely to manufacture it. A later authorized timing is a separate reproduction.

Protocol-P plant rollouts remain one original replay for the protocol's accounting. Later replay reruns were regression checks, not new stage evidence. Stages A/B/C have not run.

## Exact driver requirements after owner re-review

The driver/results handoff must show all of the following before execution can be considered:

1. closed-vocabulary `screen_physical_faults` / exact condition construction;
2. healthy means `severity is None` and `physical_faults == ()`;
3. structural means one complete `FaultSpec` with severity in `(0,1]` and derived onset;
4. I13a field-by-field equality before the rollout;
5. one complete `ScreenOverrides` bundle, never a partial bundle;
6. I3 exact reservation-difference equality plus suffix-free I4;
7. I5-I8 identity, CRN, provenance and exact canonical payload enforcement;
8. explicit Protocol-P condition keys, never the stale assignment label;
9. I9 on-grid window origin and `w1 <= n_steps`;
10. I10 measurement-time rank/width/length;
11. I11 at least five finite valid harmonic samples;
12. I12 every hard safety gate, per cell and condition, from returned `PrivilegedRecord`;
13. no persistence of `ObservedRecord`, label payload, manifest, role index, or dataset payload; and
14. a real driver integration test against the actual temporary results root that fails on an injected wrong write.

If a separate results module is used, unit tests of that module are necessary but insufficient. The driver wire itself must be observed.

## Protocol-P stage design that remains fixed

```text
Universe       dev diagnostic trajectory t01, cells 4/5/6/7
Ordinary t00   probe-free negative control
Candidates     peak {0.05..0.40 by 0.05} x ramp {0.125,0.25,0.5} = 24
Torque gate    inclusive; admits peaks {0.05,0.10,0.15} x 3 ramps = 9
Stage A        9 x 4 cells x {healthy, remEI .75, remEI .35} = 108 rollouts
Selection      maximize worst-cell D at remEI .75; 1% tie -> lower peak -> longer ramp
Stage B        ten remaining-EI values; .75/.35 reused; 32 new rollouts
Stage C        eight healthy identities per cell, k=0 reused; 28 new rollouts
Verdict        D(v,c) >= 2 * Q95_c for every cell; Q95 method="higher"
Total          replay 1 + A 108 + B 32 + C 28 = 169 protocol rollouts
```

Stage A hard gates every cell/condition: zero seven-channel safety flags; `max|qd_true| <= 8`; `max|q_true| <= 2.5`; `max|gauge_true| <= 400 microstrain`; inclusive torque gate; no increase in saturated steps versus zero probe.

Selection, terminal branches, role coverage, OOD handling, matched-signal/unmatched-null asymmetry disclosure, and success bar remain exactly as Protocol P v2.3.3 states. Do not redesign them in the driver.

## Project gates behind Protocol P

Even after the construction/driver loops close and the development screen runs, the project still requires:

- written Amendment A2 and a replacement approved assignment/config lineage if Protocol P supports it;
- coherent regeneration of dev/pilot/validation roles;
- Gate 4 estimator artifacts;
- Gate 5 controller protocol;
- Gate 6 end-to-end seed smoke;
- Gate 7 immutability/frozen-config audit;
- joint final config approval; and only then
- one-shot confirmatory test generation/evaluation.

The current pre-A2 local dataset remains development scaffolding: 472 dev/pilot/validation pairs, zero test rows. Do not treat it as frozen or confirmatory.

## Review and evidence rules that remain load-bearing

- Same-state approval is explicit. Creation, edits, handoff, downstream use and silence are not approval.
- Development screens, pilots, fixtures, diagnostics and regression checks remain separate from frozen, confirmatory or final results.
- Keep detection, attribution, information/action authorization, and controller outcome separate.
- Public README running history is append-only once settled; active-review newest states may be reviewer-edited under the review-cycle playbook.
- Packet README is an outsider-clean runbook: no local paths, agents, sessions, or internal history.
- Do not use root-wide `pytest -q`; ignored duplicate trees under `tmp/` can pollute collection. Use:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

- Do not use bare `python` or `pip`; use the project venv.
- The confirmatory test split remains untouched: zero identities, zero payloads.
- Transcript appends use the hard gate: capture physical UTF-8 EOF bytes/count/hash, patch only the complete verified unique EOF block, then assert old prefix exact, one new header after boundary, and additions-only diff.

## Closeout numbering

- Next Codex session: **52**.
- Next Codex human report: `agents/Codex/Session Summaries/HumanReport52.md`.
- Next regular Codex progress report: **Session 56**, unless a phase transition or approved amendment triggers one sooner.
