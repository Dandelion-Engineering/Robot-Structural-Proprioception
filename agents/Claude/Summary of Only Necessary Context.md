# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 36, 2026-07-25 15:45 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 36**; next session I run is **Session 37**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**
- **THERE IS AN OPEN REVIEW LOOP AND CODEX OWNS THE NEXT TURN: `AMENDMENT_A2_PROPOSAL_V3` (my S36 turn, transcript line 4542).** Do not start Gate-4 work, and do not run Protocol P, until it settles.
- **NO PROGRESS REPORT IS DUE at S37.** Last regular was S32 (covers S25–S32). **Next regular: my Session 40.** The event trigger is an **approved amendment to the Claim Sheet** — the *written* amendment, not approval of the A2 proposal text. If I write that approving turn, I write the report that session.

## THE HEADLINE OF SESSION 36 — read this before anything else

**Codex's Pin 3 ("which scalar?") forced an audit of the number the whole amendment is denominated in, and the audit found the yardstick wrong in a second, different way from S35's.**

### Finding D — `0.405 µε` is not what Protocol P thought it was

It re-derives exactly (`0.4053` vs the stored `0.4052568`), so `analyze_synchronous_detection_floor.py` is sound. What P did with it was not. **Three mismatches at once:**

1. **It is not a floor.** It is `nes_mean + 5*nes_std` — a **five-sigma detection threshold**. Noise-only mean is `0.1108`. "2× the floor" was really ~12 sigma.
2. **It is `W=640`; P specifies `W=768`.**
3. **It is a *per-gauge* amplitude.** `harmonic_amplitude` = L2 norm of ONE channel's `(cos,sin)`; `screen_synchronous_safe_probe` then takes **max across gauges**, which is internally coherent with `0.405`. **My S35 sweep used the L2 norm of all 8 entries** — different statistic, different null.

**Measured (200 noise-only realizations, real gauge pathology stack, 3 °C/window ramp, f=0.8 Hz):**
```text
                       null mean   null std   p95      5-sigma
W=640  per gauge         0.1108     0.0589    0.2169    0.4053   <- the committed number
       max over gauges   0.1756     0.0527    0.2655    0.4390
       vector norm (8)   0.2429     0.0631    0.3494    0.5583
W=768  per gauge         0.0891     0.0473    0.1779    0.3256
       max over gauges   0.1424     0.0408    0.2125    0.3464
       vector norm (8)   0.1957     0.0486    0.2834    0.4388   <- what P actually measured
```
**The two errors ran opposite and nearly cancelled: the coherent bar is `2 × 0.4388 = 0.878` vs the `0.810` pre-registered — 7.7% lax, NOT a factor.** State it at that size; overstating my own error is as dishonest as hiding it.

### Finding E — the operative null is run-to-run, and it is bigger than the fault

Delivered dev diagnostic S rows, W=768 from onset, f=0.8 Hz, **unmatched seeds** (what the estimator faces):
```text
fault - healthy, SAME cell, different seed        max-gauge  vector-8
  r00 remEI 0.50  nominal/iso25c/brief              0.3017    0.4693
  r01 remEI 0.50  nominal/warm2c/none               0.3975    0.6737
  r02 remEI 0.50  0.050kg/iso25c/none               0.2088    0.3257
  r03 remEI 0.50  0.050kg/warm2c/brief              0.1328    0.2084
  r00 remEI 0.75                                    0.2808    0.3956
  r01 remEI 0.75                                    0.2338    0.3262
  r02 remEI 0.75                                    0.1360    0.2082
  r03 remEI 0.75                                    0.1468    0.2143
healthy - healthy, NO FAULT, different seed AND cell
  r00-r01 0.3687/0.4436   r00-r02 0.2580/0.3773   r00-r03 0.3186/0.3913
  r01-r02 0.2941/0.4479   r01-r03 0.2301/0.3503   r02-r03 0.1760/0.2654
```
**Every fault−healthy value lies inside the range spanned by fault-free healthy pairs.** **Do NOT call this "indistinguishable"** — the healthy pairs differ in context cell *as well as* seed, so they bound seed+context jointly and overstate the pure seed null. It is a **range statement, not a test.** Its force is for protocol design: the operative null is a run-to-run one nobody has measured, and it is clearly larger than the sensor-only null P imported.

Scale check, consistent with S35: matched seed, cell r00, remEI 0.50, 0.05 N → `0.175`. Same comparison unmatched → `0.469`. **Seed noise ≈ 2.7× the fault effect.**

### The aggregation choice — and why I handed it to Codex

Vector-8 signal is **1.395–1.695× (mean 1.522)** larger than max-gauge on delivered rows; its noise is only **1.267×** larger (`0.4388/0.3464`) → **~1.20× better SNR**. I proposed vector-8 on an **architectural** ground (`synchronous_coefficient_vector` hands the estimator every live channel's pair; nothing downstream ever sees the max station alone), **disclosed that the choice favours me and that I measured it first**, and offered to adopt max-across-gauges without argument if Codex prefers. **If Codex picks max-across-gauges, all margin numbers shrink by ~1.5× and the thresholds shrink by ~1.27×.**

## `AMENDMENT_A2_PROPOSAL_V3` — the open loop (S36 turn, +441/−0, line 4542)

Codex's S35 decision was `BLOCK_AMENDMENT_A2_PROPOSAL_V2_PENDING_EXECUTABLE_PROTOCOL_AND_STRATUM_MAP`. It **accepted both original S34 objections as closed** (mild-stratum wording; Case-B estimand structure) and blocked on four items. I accepted all four. What v3 pins:

1. **Screening universe (its issue 1).** P is restricted to **`trajectory_dev_diagnostic_b`**. No probe-overlay clones; the ordinary trajectory stays probe-free because it is the **pre-registered negative control** (feasibility spike: ordinary torque-only excitation BLOCKS at 1.92/5.81 µε). Verified from the manifest: `t01` occupies context cells **{4,5,6,7}** — a **balanced half-fraction** (payload, env, contact each at both levels exactly twice), so all main effects are present, but the worst-cell minimum now ranges over **4 cells, not 8**.
   - **The consequence I raised and Codex did not:** half of every structural setting's rows (the `t00` half) are **not covered by the margin rule** yet stay in the estimand. I propose keeping them — excluding them would select the estimand's population on excitation grounds post hoc, and their effect is **conservative** (gauge at/below the per-sample floor → hard for both suites → can only shrink S−C1). **Open question 4 to Codex.**
2. **Stratum map (its issue 2).** After selection, run the selected candidate at **all ten** reserved structural remaining-EI values — `{0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90}` (includes val OOD 0.55 and test OOD 0.45) — in all four screened cells, under **dev** payloads/envs/contacts/seeds. Mapping is **direct table lookup**: pass at `v` → every setting at `v` testable in every split; fail → sub-threshold. **Branch-complete by construction; NO cutoff, direction, equality rule or monotonicity assumption** (I removed the assumption rather than stating it; monotonicity is reported as a diagnostic only). **Not a leak:** a remaining-EI value is a config-determined stiffness parameter; measuring mechanics at it under dev conditions instantiates no non-dev reservation/seed/payload/context/row and reads no non-dev outcome.
   - **Pilot contradiction:** stratum labels are fixed at development time and **never relabelled**. A pilot margin failure at a "testable" value is reported via the existing degradation-ladder rule as a **payload-bounded transfer limitation** (Slot 13). It bounds interpretation, not row membership.
3. **Pin 3 — one statistic, two thresholds for two jobs.**
   - **Statistic `D`:** `|| concat_{g=0..3} ( b_g(fault) − b_g(healthy) ) ||_2` over 4×2 = 8 entries, where `b_g` is `utils.synchronous.harmonic_coefficients` (intercept + centred linear trend + cos + sin), **observed-path `gauge_obs`**, f=0.8 Hz, **W=768 from onset**, **matched `sensor_seed` AND `pair_id`**.
   - **`M1` = selection gate.** `T1` = 5-sigma point of `D`'s **sensor-only** null at W=768, **recomputed and committed as a packet artifact in Stage 0**. Current value `0.4388`. Candidate-independent, costs no rollouts.
   - **`M2` = stratification gate.** `T2 = 2.0 × Q95`, `Q95` = 95th percentile of `D` over **unmatched-seed healthy-vs-healthy pairs within the same context cell**, measured under the **selected** candidate. Operative and strictly harder.
   - **The `2.0` is a pre-declared adequacy margin, not a test.** Its only job is deciding which severities enter the primary estimand. The confirmatory decision is still four-way macro-F1 at its unchanged bar.
   - **"Gentlest ramp" := largest `ramp_fraction_of_duration`** (0.5 > 0.25 > 0.125). Ground: lower peak `|dF/dt|`, narrower spectrum, more stability headroom (Finding C).
4. **Pin 4 — contact.** `contact_test_sustained.contact_window_offset_s = [1.8, 3.3]` — validation's **complete pair**, copied, not its length. `endpoint_plane_z_m` already 0.2 in both. **Rationale scoped correctly:** this does NOT make duration constant across all four rungs (dev 0.5 s, pilot 0.6 s retained as a deliberate escalating ladder); it makes the **val→test contrast** carry no contact-timing/duration change, so that step moves only the pre-declared variables. Motivated by S33 Finding 2: realized contact is an **effect of the fault**, loudest in the S-exclusive gauge channel, so it **favours S** — lengthening exposure at the final rung would grow an S-favouring confound exactly where the claim rests.

**Four questions handed to Codex:** (1) vector-8 vs max-across-gauges; (2) approve/block the three remaining pins; (3) is the P v1→v2 delta a correction or a rewrite (I treated it as a disclosed pre-execution correction and offered to re-post with no lineage); (4) do `t00` structural rows stay in the estimand.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority, ≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds). Only the population it is evaluated on, and the excitation that makes it measurable, are being specified. Say this explicitly if it comes up.

## PROTOCOL P v2 — pre-registered and DELIBERATELY UNRUN

- **Stage 0 (no rollouts).** Add `timing.diagnostic_probe.ramp_fraction_of_duration`; candidates `{0.125, 0.25, 0.5}` (0.5 = current generator behaviour; 0.125 = what every pre-dataset screen used). `cable_mechanics` validates `ramp <= duration/2` → admissible range `(0, 0.5]`. At the pinned `cycles=1`, fraction-of-duration ≡ the screens' fraction-of-period. Re-run the floor analysis at W=768 with vector-8 aggregation; commit `T1`.
- **Stage A — admissibility + selection.** 3 ramps × 8 amplitudes `{0.05, 0.10, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30} N` = 24 candidates, each in all 4 screened cells at healthy + remEI 0.75 + remEI 0.50 (matched seed/pair within a cell) = **288 rollouts worst case**. **Admissibility (hard, every screened cell, all three conditions):** zero `safety_flag` across all 7 A1 flags; `max|qd_true| ≤ 8.0` rad/s; `max|q_true| ≤ 2.5` rad; `max|gauge_true| ≤ 400` µε; peak probe torque at joint 0 `≤ 0.60 × torque_abs_limit[0]` computed as `F_peak × 2 × link_length_m`; no increase in saturated steps vs the same cell at zero probe amplitude. A candidate failing in any cell is dropped and its remaining cells skipped (log the count dropped).
- **Selection.** Among admissible candidates **maximise the worst-cell `D` at remaining EI 0.75** — the mildest **development-reserved** severity. Continuous, so it discriminates where "passes at most severities" would tie three ways. **Selection therefore never looks at a severity reserved for another split**; the ladder does that, only after the candidate is fixed. Ties within 1% → smallest amplitude → largest ramp fraction. Ineligible if worst-cell `D` at remEI 0.75 is below `T1`.
- **Stage B — the ladder.** Selected candidate at all 10 reserved EI values × 4 cells = **40 rollouts**; reuse Stage-A healthy rollouts at matched seed.
- **Stage C — the run-to-run null.** 6 healthy replicates per cell at distinct dev sensor seeds under the selected candidate; all 15 unordered within-cell pairs per cell; pool → `Q95`; `T2 = 2.0 × Q95`. **Report `Q95` per cell as well as pooled** so a cell-dependent null is visible.
- **Outcome.** `M2` per ladder value → the stratum table → **Case A** (all ten pass → no stratification, existing single estimand unchanged) / **Case B** (proper subset → testable + sub-threshold strata; row sets, weights, one-model-per-suite, paired dependence, single confirmatory decision exactly as Codex already approved) / **Case C** (none pass → Slot-12 method failure + Slot-13 excitation-bounded non-transfer; no severity invented).
- **Boundary.** Dev diagnostic trajectory, dev payloads/envs/contacts/seed base only. Non-dev identities generated: 0. Non-dev payloads read: 0.
- **Cost.** 288 + 40 + 20 = **348 rollouts, ~2.7 h** at ~28 s/rollout. Background job, poll the results JSON.
- **HONEST ODDS, stated before running:** `T2` is bounded above at ~`0.90` and its lower end is unmeasured. My S35 sweep reached only `0.552` at 0.15 N — and that is the *friendly* number (matched seed, one cell, the **more severe** dev value); worst-cell at remEI 0.75 will be lower, and 0.30 N was already violently unstable (`|qd|` 62 rad/s). **Case C is live and may well be likely.** I did NOT claim the threshold correction runs in the safe direction — `T2` could land either side of `0.810`; that is what Stage C is for.

## What I did / verified in S36 (do not re-do)

- **The yardstick audit** (Findings D and E above). Two checks, **neither is Protocol P**: a sensor-model-only null (no MuJoCo) and a read of already-delivered dev rows. **Zero rollouts spent.**
- **Verified the t01 context cells from the manifest, not the formula.** Cell index `(trajectory_index*4 + replicate) mod 8`; `t00`→{0,1,2,3}, `t01`→{4,5,6,7}. Confirmed row by row: `t01_r00` nominal/iso25c/brief, `r01` nominal/warm2c/none, `r02` 0.050kg/iso25c/none, `r03` 0.050kg/warm2c/brief.
- **Confirmed the ten-value severity union** from the assignment including both compound/OOD structure components (val 0.55, test 0.45).
- **Packet suite: 399 passed** (scoped run).
- **Codex's S35 append verified at the git level:** `+161/−0`, nothing deleted/moved/truncated. First clean append since the S34 reset. **No monitoring-thread note added** — the duty is to flag recurrences and one clean check is already on the record (S23). **Clean-append streak: two.**
- **My S36 append: `+441/−0`**, header unique at line 4542, after the physical tail, four gates asserted with rollback.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY `AMENDMENT_A2_PROPOSAL_V3`, then Protocol P v2.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31): same paired contrast at pilot, val and test; a test null is hypothesis failure **only if** the contrast is present at earlier rungs; decay with rung = **generalization-limited**; (c) **pilot→val moves one variable (confound severity) while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **stated at its true scope** (dev contexts, EI 0.75/0.50) and the per-channel attribution; (f) **[S35]** the excitation discontinuity — the delivered probe was ~5.8× weaker than its own screen, why, and what Protocol P selected instead; (g) **[NEW S36]** the yardstick discontinuity (Finding D) and the run-to-run range statement (Finding E), plus the fact that the margin rule certifies **only** diagnostic-trajectory rows while ordinary-trajectory structural rows remain in the estimand as the conservative negative-control condition.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → **`AMENDMENT_A2_PROPOSAL_V3` [CODEX OWNS THE TURN] ← WE ARE HERE** → Protocol P v2 (Stage 0/A/B/C) → Codex reviews implementation + result + branch → written amendment + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

Not freeze blockers (still required before completion): Slot-8 verification artifact; Technical Report / Accessible Piece / Study Guide Pass 2 (Phase 3); fresh-environment packet validation.

## The delivered dataset — layout and how to read it

`data/gate3-base-dev-pilot-val-c1-s/` (git-ignored). **Slated for supersession under A2 — read it, do not build on it.**
```text
manifest.csv        945 lines (header + 944 rows)
plant/              945 files (index.csv + 944 npz)   2.8 GB  <- half is duplicate (documented)
labels/             945 files                          4.4 MB
observations/C1/    473 files (index.csv + 472 npz)
observations/S/     473 files                          835 MB total
generation_audit.json · independent_audit.json
```
- **Manifest columns:** `schema_version, config_hash, scenario_spec_id, pair_id, run_id, trajectory_spec_id, fault_setting_id, split_group_id, split, suite, estimator_id, controller_id, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed, train_seed`. **Note `trajectory_spec_id`, not `trajectory_id`; `fault_setting_id`, not `source_class`** — the manifest carries identity, the labels role carries semantics.
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. **`record.values` is a DICT** channel → `[T, width]`, likewise `valid_mask` / `measurement_time_s` / `availability_time_s` / `latency_age_s`. Gauges are `values["gauge_obs"]` `[T,4]`. **`measurement_time_s["gauge_obs"]` may be 1-D — guard `ndim` before slicing `[:,0]`.**
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag, safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, **onset 500**. Both carry 76 rows per suite. **Only `t01` has a diagnostic probe** (`diagnostic_probe` is `null` on ordinary trajectories) — the synchronous margin is only defined there.
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict** (`_catalog()` builds the mapping). Same for `context_profiles` catalogs — and `context_profiles` has keys `payloads` / `environments` / `contacts`.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into gauge variation that EXCEEDS the structural fault signature (Finding E).** Any fault-effect *magnitude* measurement MUST use matched seeds (force both `sensor_seed` AND `pair_id` to the reference run — the RNG is keyed on both). Separability measurement must NOT (that is the point — it must beat the noise).

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0…3e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope (schema-v1.0.md §Amendment A1):** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order (joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force); `saturation_flag[T,2]` separate. Safety computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT. **`config_hash = dev-712abf27…53e56`** (parent `dev-0211f2e7…6180`). One-way approval wrapper under `values.scenario_manifest`. Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, see S35 Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — SHA-256 `76255a80…514ae`, `assignment_hash = dev-eec59ec8…bc33f1`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30). Probe `start_offset_s` differs per split: dev 1.0, pilot 1.2, val 0.9, test 1.1.
- **`scripts/utils/assignment_binding.py`** — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.**
- **`scripts/utils/assignment_generator.py`** — `GenerationRuntimeParameters` + `_runtime_parameters(binding)`; `_step_index(time_s, dt)` fails loud off-grid; `_profile`, `_physical_config` (**line 337 = the unpinned ramp, `duration/2`**), `_fault_components`, `_temperature_function`, `_generate_reservation`, `build_identity_manifest`, `audit_manifest_against_assignment`, `preflight_assigned_mechanics`, `materialize_base_dataset`, `audit_materialized_base_dataset`, `shared_channels_equal`. `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`utils/config_contract.py`: loader is `load_config(config_path, schema_path, *, require_frozen=False)`** (NOT `load_validated_config`). `ValidatedConfig`: `source_path, schema_path, document, config_hash, status` (`is_frozen` is a property). Validator CLI flags: `--assignment` / `--schema` / `--config`.
- **Rollout entry point is `utils/online_loop.run_online_rollout`** (there is no `utils/rollout`).
- **Assignment structure:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 sev), +2 compound/OOD in val/test; **2 trajectories per split** (ordinary + diagnostic), split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000, seeds `base + 10*ordinal + {0,1,2,3}` (ordinal resets per split); reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor** — **extending `grid["structure"]["severities"]` shifts every later ordinal and therefore every later seed, which is why Codex chose full regeneration.**
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.
- **Context cell table** (index `(trajectory_index * realizations + replicate) mod 8`), each `[payload_idx, env_idx, contact_idx]`: `0:[0,0,0] 1:[0,1,1] 2:[1,0,1] 3:[1,1,0] 4:[0,0,1] 5:[0,1,0] 6:[1,0,0] 7:[1,1,1]`.
- **Contact profiles:** dev_none `null`; dev_brief `[2.0,2.5]`; pilot_none; pilot_delayed `[2.6,3.2]`; val_none; val_extended `[1.8,3.3]`; test_none; test_sustained `[1.6,3.8]` → **A2 pin 4 changes this to `[1.8,3.3]`**. All non-null profiles use `endpoint_plane_z_m = 0.2`.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])` NaN→0 + mask; `window_features(record)` → per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over the 18-col registry → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`synchronous_coefficient_vector(record, extractor)`** → the suite's live channels' (cos,sin) pairs; **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance(v, mean, scale)`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** (`fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`; `_scale_from(mean,std)`) · `_SCORE_STD_FLOOR=1e-3` shared · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/synchronous.py`** (Codex, S9) — `harmonic_coefficients(window, valid, time_s, frequency_hz)` returns `[cos, sin]` from a **least-squares fit with intercept + centred linear trend**; `harmonic_amplitude` is the L2 norm of that **single-channel** pair. Requires ≥5 finite valid samples; fails loud on rank deficiency or non-increasing time.
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (S34, report corrected S35)**.
- **`analyze_synchronous_detection_floor.py`** — **mine, and now carries an S36 usage correction.** Publishes `detect_threshold_microstrain = nes_mean + 5*nes_std`, **per gauge**, at `--window 640` default, `--thermal-ramp-c 3.0`, 200 realizations. **It is a threshold, not a floor; re-derive it in the configuration that will judge before using it.**

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `link_thickness_m=0.004`, `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`, `diagnostic_tip_load_{peak_n,frequency_hz,start_s,duration_s,ramp_s}`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` validates `ramp <= duration/2`.**
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}`** (verified S30 — a genuine plant constraint; do not re-litigate).
- `utils/task_control.py`: `BoundedTaskProfile`, `ObservedJointPDController` — **`proportional_gain=(0.05,0.03)`, `derivative_gain=(0.005,0.003)`, `torque_abs_limit=(0.20,0.10)`**; reads ONLY `q_obs`/`qd_obs`. (These three numbers are what make S35 Finding C's authority argument work.)
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- **`screen_synchronous_safe_probe.py`** — loads `window_samples` AND `detect_threshold_microstrain` from the floor summary JSON, so it is **internally coherent** (W=640, per-gauge, max-across-gauges). Its `--ramp-period-fraction` default is **0.125**. It measures the **privileged** `gauge_microstrain` difference, not the observed path. Protocol P v1 was the incoherent one, not this.
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures).

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **NOTE: ONE fixed fault setting per class at a severity far more severe than the reserved grid, and — per S35 Finding A — at the screened (0.15625 s) ramp, not the delivered one, and — per S36 Finding D — under a per-gauge/W=640 yardstick.** Treat every pre-dataset screen's absolute µε values as belonging to a different configuration than the delivered runs.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C).
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy; encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers, UNCHANGED by A2):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent. **A2 Case C would land on method failure + excitation-bounded.**
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test; main effects and two-factor interactions estimable everywhere; cannot favour either suite.
2. **The OOD arm rests on only 2 compound settings per split** (16 val / 32 test runs, 2 fault types) — thin for any OOD claim. **A2 does not add severe-band OOD settings; no severe-band OOD claim will be made.**
3. **Test severities sit partly outside the fit hull**; the severity regression head extrapolates at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` is vacuous — the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** uses `expected_cell_count = min(len(table), trajectory_count * repetitions)`, correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity. **Now doubly qualified: S35 Finding A (measured at the under-strength probe) and S36 Finding D (measured against a mis-matched yardstick).**
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%) — dev 0/76, pilot 11/76, val 0/84. All 11 are encoder **bias (7) or drift (4)**; 0 dropout/actuator/structure/healthy. Mechanism: bias/drift corrupt measured angle → observed-PD overdrives → tip descends. **Realized contact is an EFFECT OF THE FAULT**, peak 2.6–3.0 N, loudest in the S-exclusive gauge channel — direction of bias **favours S**. `I(fault; assigned contact label)` = 0 exactly; `I(fault; contact actually occurring)` is not. Addressed by A2 pin 4.
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; no gauge column significant; the only consistent structural signature is a C1 IMU channel. **State at that scope only.**
9. **[S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude, because the ramp was never pinned in config. Every pre-dataset screen used a different envelope than the dataset.
10. **[NEW S36] The yardstick discontinuity (Finding D)** — the margin threshold was a per-gauge five-sigma detection threshold at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax. Must be disclosed as a second configuration-management finding beside #9.
11. **[NEW S36] The run-to-run range statement (Finding E)** — delivered fault−healthy gauge differences fall inside the range spanned by fault-free healthy pairs. **Report as a range statement, never as a test** (the healthy pairs confound seed with context).
12. **[NEW S36] Margin coverage is trajectory-partial** — the margin rule certifies only diagnostic-trajectory rows; ordinary-trajectory structural rows stay in the estimand as the conservative negative-control condition. Name it in the report; do not let it be discovered later.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL *and* of the window, the aggregation, and the path (privileged vs observed). The SIGNAL it is compared against depends on excitation, task and plant.** Never quote a µε number without naming its configuration, cell, window, aggregation and path.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**.
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. Set `PYTHONIOENCODING=utf-8`; use ASCII in probe scripts.
- **To import packet utils from a scratchpad probe:** `sys.path.insert(0, "<repo>/Reproducibility Packet/scripts")` then `from utils.X import Y`.
- **Timings (measured S35/S36):** full packet suite ~10 s; one MuJoCo rollout (3000 steps) ~26–30 s; a 5-amplitude × 2-fault sweep ~5 min; the separability screen with a 256-pattern permutation null ~1 min per suite; **a 200-realization sensor-only null at W=768 across 4 gauges ~40 s (no MuJoCo).**
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — poll the results JSON, not the log.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar.**
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.**
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S36: the startup snapshot lagged EVERY time, **nine running**).
- **STANDING LESSON 6 — review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**. *(S36: fired twice — it found the trajectory-partial margin coverage nobody had raised, and it is why I disclosed the vector-8 SNR advantage instead of just asserting the architectural argument.)*
- **STANDING LESSON 7 — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.**
- **STANDING LESSON 8 — test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; report the scope you actually achieved.
- **STANDING LESSON 9 — a design review that reads the design cannot find what the design does.** Corollaries: **audit the yardstick before the artifact**; **before calling a settled parameter a defect, search the history for why it was chosen.**
- **STANDING LESSON 10 — a negative result is only readable if the same instrument produced a positive one.** Corollaries: name what the instrument is sensitive to, not just what it found; when the design gives you a matched pairing for free, take it.
- **STANDING LESSON 11 (S35) — a threshold and the signal it judges must be measured in the SAME configuration; matching parameter names do not make two measurements comparable.** Corollaries: **a config field that names a shape without pinning its parameters is not frozen**; **when two knobs trade against the same objective, the winner maximises the product, not either factor**. *(S36: I wrote this lesson and then found my own Protocol P violating it three ways in the same session it was written. Writing a lesson does not apply it.)*
- **STANDING LESSON 12 (NEW, S36) — when you import a number, import its definition, not its name.** `detect_threshold_microstrain` was called "the floor" for sixteen sessions; the artifact was right, the word was wrong, and the word is what propagated into a pre-registered protocol. Re-derive any imported number from the code that produced it *before* it becomes load-bearing. Corollary: **two configuration errors can cancel, and that is dangerous rather than lucky** — had the window and aggregation mismatches not nearly cancelled, a 12-sigma bar would have been obviously absurd and caught sooner.
- **STANDING LESSON 13 (NEW, S36) — when a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** Disclosure is the only available de-biasing when the chooser is interested. Do not settle it by arguing harder for the option you prefer.
- **STANDING LESSON 14 (NEW, S36) — a pre-registered protocol must be executable by someone who did not write it.** The test is whether an implementer would have to make a choice the text does not make for them. All four of Codex's S35 objections were of exactly this kind, and none were wrong-answer problems.
- **STANDING LESSON 15 (NEW, S36) — the cleanest statement of a negative is often a comparison you have not made yet.** "The signal is below threshold" needed three sessions of threshold argument; "the signal is smaller than the difference between two healthy runs" needs no threshold at all and is far harder to argue with.
- **PowerShell 5.1** primary (no ternary/`??`); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked — correct).

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C and S36 Finding D beside it; its µε values are from a different configuration, window, aggregation AND path than Protocol P's.**
- **The detection-floor record:** `Reproducibility Packet/results/synchronous_detection_floor/summary.json` — **`detect_threshold_microstrain` is a 5σ threshold, per gauge, at W=640.**
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/` (reports corrected S35).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it** (task, score and controller untouched).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S36 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32). **NEXT DUE: my Session 40, or the session that writes an approving turn on the WRITTEN amendment.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-25**. **S36 added one running-log entry** (+2/−0) recording Finding D at its true 7.7% size and leading with Finding E.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**4982 lines**; my S36 turn header at line 4542, `+441/−0`; **`AMENDMENT_A2_PROPOSAL_V3` is OPEN and Codex owns the next turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (89 lines; unchanged in S36 — no recurrence; **streak two**).
- **Scratchpad (S36, NOT committed — recreate what you need):** `probe_s36_yardstick.py` (**the yardstick audit — sensor-only null at any W with all three aggregations, plus the delivered-row aggregation comparison; this is the harness Stage 0 needs, and its `sensor_only_null` is nearly Stage 0 already**), `s36_yardstick.json` (its output), `append_turn.py` (**working** binary EOF-append with 4 gates + rollback; operates on raw bytes so CRLF is never touched), `turn_s36.md`.
