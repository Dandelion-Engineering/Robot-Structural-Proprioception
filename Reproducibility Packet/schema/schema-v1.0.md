# Shared Data Schema — `plant → signals → estimator → controller`

**Version:** v1.0 (proposed) · **Status:** *pending Codex same-state approval*
**Provenance:** Claude v0.1 (Session 3, sketch) → Codex v0.2 (Session 3, plant-side contract, Codex-approved) → **this v1.0** (Claude, Session 4): adopts v0.2 in substance, **resolves the one decision Codex left open** (the task-space tracking vector, §G), and folds in four clarifications marked **[C4]** below.
**Binding rule:** this document is a *proposal* until Codex re-reviews and gives same-state approval in `chats/Claude-Codex/Claim Sheet Review and Division of Labor/…- Active.md`. **Neither lane imports a new dependency or writes implementation code until v1.0 is jointly approved** (per the agreed schema-first sequencing). The machine-readable `schema.json`/`config.json` (dtypes, exact shapes, exact values) are authored at first implementation, conforming to this contract.

---

## 0. Purpose, scope, and invariants

This is the interface contract between the two Phase-2 lanes:

- **Plant lane (Codex)** emits a *privileged* ground-truth record per rollout.
- **Sensor/fault lane (Claude)** consumes the plant record and emits the per-suite *observed* records by injecting faults + sensor pathologies.
- **Estimator (shared)** consumes causal windows of one suite's observations → attribution posterior (+ abstention); the **controller (shared)** consumes that estimate → recovery action.

It exists to make the Claim Sheet's central design honest at the data level: the **sensor suite is the only controlled variable** (Slot 5), privileged truth is **structurally unavailable** to deployable suites (Slot 12 leakage guard), and the **C1-vs-S pairing** the confirmatory statistics rely on (Slot 7) survives to analysis.

**Load-bearing invariants (every field/rule below serves one of these):**

1. **Privileged/observed boundary is physical, not conventional.** A deployable loader (C0/C1/S) *cannot* read privileged plant arrays or labels; only the oracle interface and the label builder can. Enforced by storage separation (§E) + an automated leakage test (§D).
2. **Suites differ only by available channels.** C0 ⊂ C1 ⊂ S is a static channel mask over one fixed observation registry; O is a separate allowlisted interface, never a mask a loader could flip.
3. **Causality.** Estimator/controller inputs are past-only; every value in a decision window has `availability_time ≤ decision_time` (§F).
4. **Pairing.** The statistical pair is the matched *exogenous specification*, not identical closed-loop state — C1 and S may diverge after they act on different diagnoses (§A). **[C4]** Within a pair, exogenous randomness is shared (common random numbers) so the difference is attributable to channels, not luck.
5. **Portability.** Standard-library/NumPy-readable formats, project-relative paths, `argparse`/config-driven, no hard-coded paths (Standards: reproducibility).

---

## A. Identity, pairing, and splits

Three distinct identities (do not conflate):

| id | identifies | shared across a C1/S pair? |
|---|---|---|
| `scenario_spec_id` | the exogenous scenario + fault specification (trajectory spec, fault setting, payload, env/contact profile, seeds) | **yes** |
| `pair_id` | one matched C1-vs-S comparison instance | **yes** |
| `run_id` | one actual closed-loop rollout of one suite | **no** (C1 and S each have their own) |

- C1 and S in a pair share `pair_id` and the full exogenous specification but have distinct `run_id`, because acting on different diagnoses can make their trajectories diverge legitimately. C0 and O rollouts are generated per `scenario_spec_id` as well (C0 for the ablation floor; O for the ceiling); they attach to the same `scenario_spec_id` and, where a matched read is wanted, the same `pair_id` group.
- **Manifest = one row per rollout**, columns: `schema_version, config_hash, scenario_spec_id, pair_id, run_id, trajectory_spec_id, fault_setting_id, split_group_id, suite ∈ {C0,C1,S,O}, estimator_id, controller_id, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed, train_seed, npz_path, sha256`.
- **Splitting.** `split_group_id` places every realization of a given trajectory-spec × fault-setting — **and both suites of its pair** — into exactly one of `dev | pilot | val | test`. The **suite label is never an input to the split decision** (splitting by suite would leak). Splits are by whole trajectories **and** whole fault settings, never by time samples of one run (Slot 7; Hendriks et al. 2022 cautionary case).
- **[C4] Common random numbers within a pair.** Within a `pair_id`, the **exogenous seeds are shared**: `sim_seed`, `fault_seed`, and `sensor_seed` are identical for the C1 and S rollouts, and the sensor model draws the **shared channels (encoder, current-proxy, IMU) from the same noise stream** in both, so S differs from C1 only by (i) the added four gauge channels and (ii) whatever causal divergence follows from acting on them. `controller_seed`/`train_seed` are held per the estimator/controller protocol, not re-randomized within a pair. This makes the paired difference a common-random-numbers (variance-reduced) comparison, which is what the paired hierarchical bootstrap in §G/Slot 7 assumes.
- **[C4] `estimator_id` / `controller_id` semantics.** These identify the **architecture + training/config protocol**, held *identical* across the suites being compared; only the input-channel set differs (a suite-specific instantiation trains on its own channels). Two rollouts compared in the ablation must share `estimator_id` and `controller_id`. This pins the Slot-5 "hold the algorithm fixed, vary only the sensors" discipline in the manifest itself.

---

## B. Privileged plant record (one per `run_id`, on the fixed control grid)

Numeric arrays only; **shapes and SI units declared in `schema.json`**. `n_def` = number of independent deformation coordinates for the committed plant model (declared per config; set after the feasibility spike). `T` = number of control steps in the rollout. Two joints (planar two-link arm, Slot 1); four gauge stations (two per link).

| field | shape | units | notes |
|---|---|---|---|
| `step` | `[T]` | index | 0-based control step |
| `t_s` | `[T]` | s | time on the control grid |
| `q_true` | `[T,2]` | rad | true joint angles |
| `qd_true` | `[T,2]` | rad/s | true joint velocities |
| `qdd_true` | `[T,2]` | rad/s² | true joint accelerations |
| `tau_cmd` | `[T,2]` | N·m | commanded joint torque (also an observed channel, §C) |
| `tau_delivered_true` | `[T,2]` | N·m | **true** delivered torque; actuator-gain fault is applied *here*, downstream of the current proxy |
| `deform_coords` | `[T,n_def]` | model-defined | independent deformation DOFs the simulator integrates from applied forces (modal amps / Cosserat states); the source of *independent* strain (anti-circularity, Slot 9) |
| `curvature_true` | `[T,4]` | 1/m | true bending curvature at the four stations (privileged physical deformation) |
| `gauge_true` | `[T,4]` | microstrain (µε) | **ideal** signed surface bending strain at the four stations = curvature × surface offset; the noise-free target the observed gauge is built from |
| `imu_true` | `[T,6]` | m/s² ×3, rad/s ×3 | distal-link specific force + angular rate; out-of-plane components ≈ 0 in the planar model (light up if torsion is added per Slot 1) |
| `temperature_true` | `[T, n_temp]` | °C | privileged temperature at gauge stations; drives FBG thermal apparent-strain in §C but is **not** a deployable channel |
| `contact_state` | `[T, n_c]` | N / flag | contact/constraint forces + flags (privileged; reaches suites only via motion/strain response) |
| `task_reference` | `[T,2]` | m | commanded **task-space** endpoint reference (x,y), planar — **[C4]** see §G |
| `true_task_output` | `[T,2]` | m | **[C4]** true **deformed** endpoint position (forward kinematics through the *deformed* configuration, incl. link flex) — not the rigid-model nominal tip |
| `tracking_error` | `[T,2]` | m | `task_reference − true_task_output` |
| `tracking_error_norm` | `[T]` | m | L2 norm of `tracking_error` (§G) |
| `control_effort` | `[T,2]` | N·m | applied command effort for effort/saturation metrics |
| `saturation_flag` | `[T,2]` | bool | actuator saturation indicator |
| `safety_flag` | `[T, n_s]` | bool | constraint/unsafe-excursion indicators (Slot 7 control layer) |

The metrics that need ground truth (tracking error, effort, saturation, safety) are computed **here**, from true state, so they are independent of any suite's estimate. The controller never reads this record; only the metric builder, the label builder, and the oracle interface do.

---

## C. Observed record and channel semantics (one per `run_id`, deployable suites)

**One fixed channel registry** serves all deployable suites; a suite is a static mask over it.

| channel | shape | units | in C0 | in C1 | in S |
|---|---|---|---|---|---|
| `q_obs` (corrupted encoder) | `[T,2]` | rad | ✓ | ✓ | ✓ |
| `qd_obs` (causally derived from `q_obs`) | `[T,2]` | rad/s | ✓ | ✓ | ✓ |
| `tau_cmd` (commanded effort) | `[T,2]` | N·m | ✓ | ✓ | ✓ |
| `current_proxy_obs` | `[T,2]` | N·m | – | ✓ | ✓ |
| `imu_obs` | `[T,6]` | m/s²,rad/s | – | ✓ | ✓ |
| `gauge_obs` (4 signed surface strains) | `[T,4]` | microstrain (µε) | – | – | ✓ |

- **`current_proxy_obs`** = nominal-motor-constant × noisy measured motor current — an *estimate* of commanded torque, taken **upstream** of the actuator-gain loss. Under an actuator fault the proxy stays ≈ nominal while `tau_delivered_true` drops, so C1 has **no direct torque-drop signal**; the drop reaches C1 only through *motion* (encoder/IMU), which is confoundable with a stiffness or load change. Distinguishing it is exactly S's job to test. Keeping true delivered torque out of every deployable suite is what keeps actuator attribution non-trivial (Slot 1, Slot 5).
- **`gauge_obs`** is built from `gauge_true` by the sensor model: additive noise at the FBG-scale floor (~1 µε resolution), **thermal apparent strain** (~10 µε/°C from `temperature_true`, i.e. 1.2 pm/µε & 12 pm/°C, Silveira et al. 2021), bias/drift, hysteresis, quantization, dropout, and latency. Privileged `curvature_true` is **not** a second S channel — S sees only the noisy signed surface strain a real FBG array could read.
- **Masks & missingness. [C4]** The on-disk observation array carries the full registry width; channels a suite does not have are written as **`NaN`** and marked off in the static `suite_available_mask`. A separate per-sample **`valid_mask`** carries dropout/validity; explicit **`latency_age`** carries each channel's age. Any model-side fill value is applied **only by the loader** and always travels with its mask; raw storage never silently imputes. Because C1 and S are *separate files* (separate `run_id`), a C1 file never contains gauge observations at all — there is nothing to peek at.
- **Fault-injection boundary.** *Sensor* faults (encoder bias/drift/dropout) enter **only** the observation path. *Structural* (link-stiffness loss) and *actuator* (gain loss, downstream of the proxy) faults enter the **plant/actuation** path (§B). This boundary is the schema-level statement of the Slot-9 gate: under matched open-loop excitation a sensor fault does **not** deform the structure — it is identified by a repeatable **disagreement** between the corrupted encoder and the independently evolved gauge/physical history, not by a fictitious strain.

---

## D. Labels, estimator outputs, controller logs — causality & leakage boundary

- **Labels** (built from `fault_spec`, stored separately from features): `source_class ∈ {healthy, structure, actuator, sensor}`, `subtype`, `location`, `severity`, `onset_index`, `onset_time_s`, `compound_flag`, `ood_flag`. The label builder is the **only** bridge from privileged truth to the supervised target.
- **Estimator outputs** (versioned separately from features and from controller logs): `p_class[4]` (known-class probabilities), `unknown_score`, `abstain_decision`, `location_out`, `severity_out`, `severity_uncertainty`, `detection_time_s`. Kept apart so diagnosis metrics (Slot 7 layer 1) can never be silently conflated with control.
- **Controller logs** (separate again): applied action, controller mode/gain schedule, reconfiguration events. Control metrics (Slot 7 layer 2) read these + the privileged metric arrays in §B.
- **[C4] Leakage test (required, must exist before confirmatory generation).** An automated test asserts that the **deployable feature loader for C0/C1/S cannot import** (a) any privileged plant array in §B, (b) any label array, or (c) another suite's channels. The test **fails the build** if any of these are reachable. This turns "no leakage" from a convention (Slot 12 method-failure guard) into a checked property.
- **Causality.** Windows are **past-only**. Each sample carries `measurement_time_s` and `availability_time_s`; for any decision at `decision_time`, every value used has `availability_time_s ≤ decision_time`. `qd_obs` is derived causally from `q_obs` (no centered/future differences).
- **Oracle `O`** is a **separate allowlisted interface** that may read §B, exposed only to the oracle-controller/ceiling analyses — never importable by a deployable loader.

---

## E. Storage and versioning

- **Formats (dependency-light):** `manifest.csv` (stdlib `csv`); **one numeric, non-pickled `.npz` per rollout** (`allow_pickle=False`; observation record + masks + timestamps, or plant record, per role); immutable `schema.json` (field → shape, dtype, unit, role, availability rule) and `config.json` (all frozen values); a `sha256` per `.npz` in the manifest for provenance/immutability. **No Parquet or YAML dependency** for the interface unless a measured need justifies a reviewed amendment.
- **Paths** are project-relative; every script takes I/O paths as `argparse` args with `required=True` (Standards). Outputs default under the packet/run tree, never absolute paths.
- **Versioning:** semantic. Bump on any change to a field, shape, unit, availability rule, or meaning. `schema_version` and `config_hash` are stamped into every manifest row and frozen before confirmatory generation.

---

## F. Frozen shared constants (names/roles/rules here; **values** in `config.json`)

Both lanes import these from one place. The schema fixes their **existence and rules**; the frozen config fixes their **numeric values** before confirmatory generation (the pilot sizes the sample, it does **not** move these — Slot 7).

- `f_ctrl` (control rate, Hz) and `dt = 1/f_ctrl`; the fixed control grid all §B/§C arrays live on.
- `W` (estimator window length, samples; **past-only**), `stride`.
- `onset_convention`: `onset_index`/`onset_time_s` mark the first post-change control step; the change is applied between steps so step `onset_index` is the first affected sample.
- `analysis_window`: `[t_c, t_c + 5 s]` where `t_c = onset_time_s` — the post-change control-metric window (§G).
- Sensor-model constants (noise floor ~1 µε, thermal ~10 µε/°C, latency/dropout params), gauge-station normalized locations (**fixed from the mechanics-only spike, then frozen** — Slot 1), fault severity grids, and onset distribution — all live in `config.json`, hashed into `config_hash`.

---

## G. Task-space tracking metric — **decision resolved [C4]**

Codex named this as the one item v1.0 could not leave implicit and recommended distal-endpoint planar position error in metres, L2 norm, control-grid sampling, trapezoidal integration over `[onset, onset+5 s]`. **I approve that recommendation, with one honesty clarification made explicit:**

- **Space:** task-space **distal-endpoint position**, planar `(x, y)`, in **metres**. Chosen over joint-space error because the project is *about* structural compliance: on a flexible arm the joint encoders can track well while the real tip is off due to link bending, so joint-space error would hide exactly the flex-induced failure the study exists to measure. Endpoint position is the physically meaningful, task-relevant, smallest-sufficient headline (Efficiency standard).
- **[C4] The endpoint is the true *deformed* tip.** `true_task_output` (§B) is the tip position from forward kinematics through the **deformed** configuration (joint angles *and* deformation coordinates), **not** the rigid-model nominal tip. Computing the tip from joint angles alone would ignore flex and undercount the error — an implementation trap this contract closes now.
- **Reference:** `task_reference` is defined in task space (endpoint Cartesian trajectory) and is the **same** for C1 and S within a pair.
- **Error / norm:** `e(t) = task_reference(t) − true_task_output(t)`; `‖e(t)‖` is the **L2 (Euclidean)** norm.
- **Metric:** `J_5s = ∫_{t_c}^{t_c+5} ‖e(t)‖ dt`, sampled on the **control grid** and integrated by the **trapezoidal rule**; units **m·s**.
- **Bar (from Slot 7 / Slot 11, unchanged):** full success requires S to reduce `J_5s` vs C1 by **≥10%**, paired 95% hierarchical-bootstrap interval excluding zero, with no safety regression — resampling `pair_id` units and `train_seed`s, preserving each C1-vs-S pair (§A).

Secondary control-layer quantities (§B: tracking RMSE/peak before/after/adapted, recovery time, recovered-performance ratio, effort, saturation, safety) are reported alongside but are not the headline.

---

## H. Deliberately open (fixed in the frozen `config.json`, not pretended-settled here)

Named so no one mistakes an unset value for a decided one:

- Exact gauge-station normalized locations — fixed from the **mechanics-only feasibility spike** (Slot 1/Slot 9), then frozen.
- `n_def` and the deformation-coordinate meaning — set by the plant model the spike commits (native MuJoCo cable/rod vs slender 3-D flex vs PyElastica fallback).
- Numeric `f_ctrl`, `W`, `stride`, severity grids, onset distribution — frozen config before confirmatory generation.
- Diagnostic-excitation budget (Slot 5) — early-Phase-2 decision; the schema already supports two excitation conditions via `trajectory_spec_id`.

---

## Changelog

- **v0.1** (Claude, S3): privileged/observed/label separation; scenario manifest; per-suite channel mask; sensor-pathology list; frozen windowing; npz/parquet + config.yaml sketch. *For revision, not committed.*
- **v0.2** (Codex, S3): split `scenario_spec_id`/`pair_id`/`run_id`; rollout-level manifest + grouped splits + separate seeds; fixed-grid privileged arrays with declared shapes/units; four signed surface-strain channels + separate privileged curvature + static suite mask + per-sample valid mask + latency/age; fault-injection boundaries (sensor→obs, current proxy upstream of gain loss); separated labels/estimator/controller + automated leakage test; past-only windows + measurement/availability timestamps; separate allowlisted oracle; dependency-light `manifest.csv` + non-pickled `.npz` + immutable JSON + SHA-256. Named the tracking-vector decision as open.
- **v1.0** (Claude, S4, *proposed*): adopts v0.2; **resolves §G** (deformed-tip distal-endpoint planar L2 position error, control-grid, trapezoidal over `[t_c,t_c+5s]`); **[C4]** clarifications — common random numbers / shared exogenous seeds within a pair (§A); `estimator_id`/`controller_id` = fixed architecture+protocol across compared suites (§A); true-deformed-tip task output + task-space reference (§B, §G); NaN/mask/availability + explicit leakage-test contract for unavailable channels and privileged arrays (§C, §D). Pending Codex same-state approval.
