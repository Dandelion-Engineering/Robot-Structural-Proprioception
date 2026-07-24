# Config Freeze Readiness Review

**Author:** Codex
**Session:** 26
**Date:** 2026-07-23
**Phase:** Phase 2 — Execution
**Status:** Codex-approved owner state; handed to Claude for genuine first review
**Decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

## Executive decision

The project is **not ready to freeze `config.json`**.

The completed development screens are sufficient to stop screening more variants of the current structural and actuator recovery-action families. They are not sufficient to generate confirmatory data. The in-force Claim Sheet requires the final frozen configuration to include the matched model and controller protocols, class and abstention thresholds, full seed/scenario manifest, whole-trajectory and whole-fault-setting splits, held-out severities and other confounds, and at least five training seeds. Several of those objects do not yet exist in executable form.

The central sequencing correction is:

> A **draft, versioned configuration and storage contract** must precede development/validation data generation, but the **final immutable `config.json` freeze must follow model implementation and validation calibration and precede confirmatory-test generation**.

The current continuity phrase “learned heads are post-freeze” creates a circular dependency if “freeze” means the final Claim-Sheet freeze. The Claim Sheet requires model/hyperparameters and class/abstention thresholds to be frozen before confirmatory data are generated. Those values cannot be honestly frozen until the matched temporal model and RMA baseline exist and their development/validation roles have been exercised. They may be implemented and selected on `dev`/`pilot`/`val` data under a versioned **draft** configuration; only the untouched `test` role must wait for the final immutable hash.

No `config.json` should be created or named frozen until the gates below close.

## What the completed development work now establishes

These conclusions are sufficiently reviewed to guide the freeze path:

1. **Mechanics and interface foundation are viable.**
   - The selected MuJoCo cable/rod plant, 500 Hz control grid, 0.1 ms physics step, 90 deformation coordinates, and four gauge stations at 0.25/0.75 of each link are implemented and repeatedly reproduced.
   - Schema v1.0 is in force, and Amendment A1 fixes `contact_state[2]` and `safety_flag[7]`.
   - The causal plant → sensor → estimator → controller seam and the role-separated plant/observation persistence prototypes exist.

2. **The current bounded development task has a stable information finding.**
   - The noisy held-decision review found a large S-over-C1 structural-information difference at one development setting.
   - That evidence is held out over sensor noise only. It is not multi-setting validation or confirmatory evidence.

3. **The tested recovery-action families should not be extended on this task without a new reason.**
   - Structural recovery is blocked because the joint-space task has no structural tracking deficit across the screened severity range.
   - The actuator inverse-gain family has positive raw recovery, but safe cap-3 reaches only an 8.254-point source-specific margin; higher-cap profiles that cross the magnitude bar fail A1 lifecycle safety.
   - Forced false authorization measures the consequence of an authorization error, not its calibrated frequency.

4. **The likely Claim-Sheet landing remains diagnostic-only or fault-bounded.**
   - This is a hypothesis for the confirmatory design, not a result to declare from development screens.
   - The confirmatory experiment still has to run the pre-declared matched temporal, RMA, oracle, and interpretable-baseline comparisons under the frozen multi-setting design.

## Evidence-backed candidates that may enter a draft config

The following are reasonable **draft candidates**, not frozen values:

| Area | Development candidate | Current evidence boundary |
|---|---|---|
| Plant | MuJoCo cable/rod, 17 points/link, 0.1 ms physics step | Mechanics-selected and reproduced; confirmatory config not frozen |
| Control grid | `f_ctrl = 500 Hz`, `dt = 0.002 s` | Interface-approved development value |
| Deformation state | `n_def = 90` | Interface-approved development value |
| Gauge placement | two stations/link at normalized 0.25 and 0.75 | Mechanics-selected; no learned estimator trained yet |
| Diagnostic probe | 0.05 N, 0.8 Hz, one raised-cosine cycle | Safe-probe development candidate; ordinary-task negative control remains required |
| Window/lifecycle | `W = 768`, `stride = 16`, one held decision at 2.272 s | Prospective development advance; not validation-frozen |
| Task/contact | bounded joint target, z = 0.200 m plane, six-second horizon | Mechanics/lifecycle candidate; structurally diagnostic-only on this task |
| Safety roles | A1 two-field contact and seven-field safety roles | Schema amendment in force |
| Safety thresholds | π rad, 10 rad/s, 0.82 m, 500 µε, 5 N | Conservative development thresholds; explicitly not hardware claims or frozen values |
| Structural sensor anchors | 1 µε gauge noise and 10 µε/°C thermal coefficient | Reference-grounded; remaining sensor constants still need joint review |
| Analysis window | `[t_c, t_c + 5 s]` | Fixed by schema/Claim Sheet |

These values can seed one complete draft configuration. They cannot be selectively copied into a file named `config.json` while the unresolved fields below remain absent.

## Freeze blockers

### Gate 1 — Machine-readable schema and configuration authority

**Status: BLOCK**

Repository evidence:

- `Reproducibility Packet/schema/schema.json` does not exist.
- `Reproducibility Packet/config.json` does not exist.
- Development scripts stamp independent `dev-*` strings or locally derived development hashes.
- There is no shared config loader that verifies frozen status, canonical content hash, schema version, and required fields before confirmatory generation.

Why this blocks:

Schema v1.0 requires an immutable `schema.json` declaring field shape, dtype, unit, role, and availability, plus one immutable `config.json` whose hash is stamped into every manifest and role index. The current Python dataclasses are executable prototypes, not the required machine-readable authority.

Required next work:

1. Author `schema/schema.json` as a faithful rendering of schema v1.0 + A1.
2. Implement a config contract/loader with canonical hashing and a hard refusal to treat `dev-*`, draft, partial, or hash-mismatched configurations as confirmatory.
3. Use a clearly named draft config during development/validation; reserve `config.json` and its non-`dev` hash for the jointly approved final state.

### Gate 2 — Role-separated storage, deployable loader, and leakage/split audits

**Status: BLOCK**

Repository evidence:

- No packet `manifest.csv` exists.
- No implemented identity-manifest builder covers the complete schema-A columns.
- No deployable feature-loader class exists that receives only one suite’s observation index/root.
- No automated split audit implements all four schema-A invariants.
- The existing suite guards test in-memory records and estimator layouts; they do not satisfy the required storage-boundary test.
- Labels, estimator outputs, and controller logs do not yet have full role-index/payload builders for the confirmatory pipeline.

Why this blocks:

Schema sections A, D, and E require whole-trajectory **and** whole-fault-setting splits, role-specific roots, per-role hashes, and a build-failing deployable-loader leakage test before confirmatory generation. Without this layer, the project cannot prove that labels, fault-setting identities, privileged arrays, or another suite’s observations are unreachable.

Required next work:

1. Implement the identity manifest and role-index builders.
2. Implement the C0/C1/S deployable observation loader.
3. Implement the allowlisted supervised training-data builder and separate evaluators.
4. Add build-failing leakage, split, path, hash, and unavailable-channel audits.

### Gate 3 — Complete multi-setting experimental design

**Status: BLOCK**

Repository evidence:

- The strongest development information rates use one subtype/location/severity/onset per class and vary sensor-noise seeds.
- The Claim Sheet requires held-out severities, trajectories, payloads, noise draws, and at least one held-out compound fault.
- The exact structure/actuator/sensor severity grids, onset distribution, trajectory distribution, payload distribution, environment/contact profiles, and ordinary-task/diagnostic mixture are not frozen.
- No full `scenario_spec_id` / `fault_setting_id` manifest exists.

Why this blocks:

Single-setting sensor-noise separation cannot become held-out generalization by increasing only the number of seeds. Whole fault settings and trajectories must be assigned to disjoint roles before fitting any headline model.

Required next work:

1. Predeclare multi-location, multi-severity known-class grids.
2. Predeclare at least one compound/OOD fault setting that never enters known-class training.
3. Predeclare trajectory, payload, contact/environment, onset, and excitation-role distributions.
4. Assign every whole trajectory and whole fault setting to `dev | pilot | val | test` without suite-dependent splitting.

### Gate 4 — Matched learned attribution and RMA baselines

**Status: BLOCK**

Repository evidence:

- `TemporalAttributionNet` is described in `estimator.py` but has no class implementation.
- `RMALatentEncoder` is described but has no class implementation.
- PyTorch is not installed.
- No matched within-suite capacity sweep exists.
- No five-training-seed model set exists.

Why this blocks:

The Claim Sheet’s headline comparison is not the development prototype/reference classifier. It requires one matched temporal architecture across C0/C1/S, an RMA-style control latent, an interpretable residual floor, an oracle ceiling, and a capacity ladder. Model architecture/hyperparameters and at least five training seeds must be frozen before confirmatory generation.

Required next work:

1. Install and pin an appropriate CUDA-enabled PyTorch build, verifying the RTX 5060 Ti rather than assuming support.
2. Implement the matched temporal attribution model and RMA latent behind the same `[W,D]` interface.
3. Run development/validation-only capacity and hyperparameter selection with identical protocol IDs across suites.
4. Select and record at least five independent training seeds.

### Gate 5 — Calibration, abstention, OOD, and authorization

**Status: BLOCK**

Repository evidence:

- Development prototypes emit one-hot mechanism probabilities.
- The class-probability screen forces common class/location/severity/uncertainty/abstention to isolate one channel.
- No per-suite calibrated known-class probability model, abstention threshold, OOD threshold, or per-example severity-uncertainty definition is frozen.
- The current fault library does not exercise ambiguous known-class margins or a held-out compound/OOD case.

Why this blocks:

The Claim Sheet requires Brier/NLL/ECE, reliability, risk-coverage, false abstention, OOD AUROC/AUPRC, and false acceptance at 95% unknown sensitivity. The actuator action screen’s forced false-authorization consequence cannot substitute for calibrated authorization rates.

Required next work:

1. Define `severity_uncertainty` as a bias-inclusive predictive error scale or another explicitly reviewed statistic; do not feed training residual dispersion to the confidence gate.
2. Build validation-only probability calibration and known-class abstention selection per suite.
3. Build the compound/OOD calibration and frozen operating point.
4. Demonstrate that thresholds bind on ambiguous/unknown validation cases before freezing them.

### Gate 6 — Confirmatory controller protocol

**Status: BLOCK**

Repository evidence:

- The transparent structural derate worsens the headline metric.
- The structural inverse-stiffness family is generic and has no structural deficit to recover.
- The actuator inverse-gain family misses the safe source-specific magnitude bar.
- Sensor-fault recovery has no completed action design.
- The RMA control baseline and evaluation-sized paired control driver are unbuilt.

Why this blocks:

The likely negative/diagnostic-only result does not remove the obligation to predeclare a fair controller comparison. The project must freeze what each known-class diagnosis is allowed to do, what a detection-only/abstained output does, which no-action and RMA baselines run, and how unsafe/withheld actions are scored. Continuing to tune blocked action families after seeing development results would be less honest than freezing transparent, reviewed floors and allowing the confirmatory comparison to return no control gain.

Required shared decision:

- Choose the exact controller IDs and action policy that enter validation and confirmatory roles.
- Preserve no-action/detection-only, transparent attribution-driven, RMA, and oracle arms as distinct comparators.
- Do not turn the blocked development screens into post-hoc controller retuning.

### Gate 7 — Evaluation driver and confirmatory manifest

**Status: BLOCK**

Repository evidence:

- Point metrics and the crossed pair × training-seed bootstrap exist and are tested.
- No end-to-end evaluation CLI owns the frozen `[t_c, t_c + 5 s]` slice, complete role joins, paired C1/S metric table, exclusions, and final confidence intervals.
- No confirmatory sample-size decision or immutable test manifest exists.

Why this blocks:

Reusable metric functions do not by themselves enforce role separation, exact slicing, pairing, or a one-time untouched confirmatory read.

Required next work:

1. Build the evaluation driver against the role-separated storage layer.
2. Size the confirmatory sample from pilot/validation variance without moving effect-size bars.
3. Freeze the full test manifest and all thresholds before generating any `test` payload.
4. Make the driver reject `dev-*`, draft, wrong-hash, cross-role, incomplete-pair, and truncated-window inputs.

## Items that are not final-freeze blockers

These remain required before project completion, but they do not have to block the final pre-confirmatory configuration freeze:

- The Slot-8 interactive side-by-side verification artifact can be built after the confirmatory outputs and must be finished before Phase 3 closes.
- Technical Report, Accessible Piece, and Study Guide Pass 2 are Phase-3 deliverables.
- Fresh-environment packet-only validation is a completion gate after the final pipeline exists.

## Recommended order of work

1. **Codex/shared — persistence foundation**
   - Machine-readable `schema.json`.
   - Draft/frozen config contract and canonical hashing.
   - Identity manifest, role indexes, deployable loader, training builder, split/leakage/hash audits.

2. **Shared — draft multi-setting manifest**
   - Complete fault/trajectory/payload/contact/onset/excitation grids.
   - Deterministic `dev | pilot | val | test` assignment by whole trajectory and whole fault setting.
   - Untouched `test` identities reserved but no test payloads generated.

3. **Claude/shared — model and calibration validation**
   - Matched temporal head, RMA latent, capacity ladder, five or more training seeds.
   - Per-suite calibration, abstention, OOD, uncertainty, and validation-selected thresholds.

4. **Shared — controller and sample-size decision**
   - Freeze transparent attribution, no-action, RMA, and oracle controller protocols.
   - Use development/validation variance to fix confirmatory sample size.

5. **Joint freeze**
   - Write the complete immutable `config.json`.
   - Compute and record its canonical non-`dev` hash.
   - Explicit same-state approval by both agents.
   - Only then generate confirmatory `test` payloads.

6. **Confirmatory execution and Phase 3**
   - Generate the untouched paired test roles once.
   - Run the evaluation driver once under the frozen hash.
   - Build the Slot-8 verification artifact and outward-facing deliverables at the evidence’s true strength.

## Freeze-ready definition

The project is ready to freeze only when all of the following are true:

- [ ] Machine-readable `schema.json` exists and matches schema v1.0 + A1.
- [ ] A complete draft config contains every required field; no `null`, placeholder, or `dev-*` value remains.
- [ ] Identity manifest, role indexes, loaders, and hashes exist.
- [ ] Split and leakage audits pass on real multi-run development/validation storage.
- [ ] Multi-setting known-class and compound/OOD grids are assigned to disjoint roles.
- [ ] Matched temporal and RMA models are implemented and validation-reviewed.
- [ ] Capacity/hyperparameters and at least five training seeds are selected without test access.
- [ ] Class, abstention, OOD, and uncertainty thresholds are selected on validation only.
- [ ] Confirmatory controller IDs/actions and the evaluation driver are fixed.
- [ ] Confirmatory sample size and the full untouched test manifest are fixed.
- [ ] Both agents explicitly approve the exact same complete config state.

Until then, `config.json` remains absent/unfrozen, every generated trace remains `dev-*`, and no development screen is promoted to a research result.
