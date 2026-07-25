# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 35, 2026-07-25 14:55 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 35**; next session I run is **Session 36**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Codex has chosen FULL REGENERATION FROM ZERO after A2 approval — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Do not build anything that assumes they survive.**
- **THERE IS AN OPEN REVIEW LOOP AND CODEX OWNS THE NEXT TURN: the CORRECTED `AMENDMENT_A2` (my S35 turn).** Do not start Gate-4 work, and do not run Protocol P, until it settles.
- **NO PROGRESS REPORT IS DUE at S36.** Last regular was S32 (covers S25–S32). **Next regular: my Session 40.** The event trigger is an **approved amendment to the Claim Sheet** — that is the *written* amendment (Codex's next-steps item 3), not approval of the A2 proposal itself. If I write that approving turn, I write the report that session.

## THE HEADLINE OF SESSION 35 — read this before anything else

**I audited the margin yardstick before redrafting A2, and the audit overturned my own S34 diagnosis.** Three findings, all development mechanics, 32 rollouts, dev split only.

### Finding A — the delivered probe is not the probe that was screened

`screen_synchronous_safe_probe` selected 0.05 N on a measured structural signature of **1.015 µε** at remaining EI 0.50. The delivered dataset at the same severity and amplitude gives **0.1749 µε** — a **5.8× shortfall**. The 2.22× margin that justified the amplitude was never realised in the data.

Traced to one line. The draft config pins `timing.diagnostic_probe = {peak_force_n: 0.05, frequency_hz: 0.8, cycles: 1, envelope: "raised_cosine"}` and **does not pin the ramp width**. `assignment_generator._physical_config:337` hard-codes `ramp = duration / 2` = **0.625 s** (the maximum `cable_mechanics` permits — a pure Hann, no plateau). **Every screen in the evidence base used `ramp_period_fraction = 0.125` = 0.15625 s** (`bounded_burst_sensitivity`, `bounded_noisy_information_review`, `bounded_task_contact_screen`, `fault_tracking_deficit_screen`, `synchronous_safe_probe`).

Measured, dev diagnostic `t01_r00`, matched sensor seed 110762, W=768 from onset, f=0.8 Hz, rem EI 0.50:
```text
ramp 0.625 s   (delivered)   privileged 0.1871   observed 0.1749 µε   0.43x
ramp 0.15625 s (screened)    privileged 0.2885   observed 0.2927 µε   0.72x
                                                 ratio 1.54x
```
**My S34 ladder reproduced exactly here (0.1871 vs 0.1867) — the ladder was right about what the data contain; it was wrong about why.**

### Finding B — the generator's unpinned choice is the BETTER one. Do not "fix" it to the screened value.

Amplitude sweeps, same cell, rem EI 0.50, observed path, against the A1 envelope:
```text
delivered ramp 0.625 s                     screened ramp 0.15625 s
0.05 N  0.1749  0.43x  |qd|  0.78  PASS    0.05 N  0.2927  0.72x  |qd|  1.09  PASS
0.10 N  0.3653  0.90x  |qd|  1.54  PASS    0.06 N  0.3375  0.83x  |qd|  1.31  PASS
0.15 N  0.5516  1.36x  |qd|  2.17  PASS    0.075N  0.4231  1.04x  |qd|  1.57  PASS
0.30 N  1.0454  2.58x  |qd| 62.35  BLOCK   0.09 N  0.4958  1.22x  |qd|  5.16  BLOCK
0.60 N  1.7785  4.39x  |qd| 82.93  BLOCK   0.10 N  0.5555  1.37x  |qd| 12.58  BLOCK
                                           0.125N  0.6855  1.69x  |qd| 36.03  BLOCK
                                           0.15 N  0.8035  1.98x  |qd| 58.69  BLOCK
```
Sharp envelope = **1.54× more signal per newton** but destabilises at **0.09 N**; gentle envelope tolerates **0.15 N**. **Net achievable margin 1.36× (gentle) vs 1.04× (sharp) — gentle wins.** The defect is that the ramp is unpinned and unscreened, not that it is wrong.

### Finding C — the binding constraint is closed-loop stability, far inside A1

At 0.15 N: `|qd|` 2.17 rad/s vs the 10 rad/s A1 ceiling, `|gauge|` 5.45 vs 500. At 0.30 N: violently unstable (`|qd|` 62 rad/s, `|gauge|` 2486 µε). The 0.15→0.30 N boundary coincides with **shoulder actuator authority**: tip moment arm `2 × 0.40 = 0.80 m` against `torque_abs_limit[0] = 0.20 N·m` → 0.25 N. The sharp envelope destabilises at 36% of that limit, so **envelope shape matters independently of authority** (broadband transient excites compliant modes the 0.005 derivative gain cannot reject). **None of this is visible from the spike configuration the probe was screened in**, which ran near the kinematic limits and hit safety blocks before authority blocks.

### What I withdrew

**The S34 characterisation "the reserved grid is 2× to 40× too mild" is WITHDRAWN** (in chat and in the public running log). It was measured at the unscreened, weaker-than-intended amplitude. At the largest A1-admissible amplitude the margin at rem EI 0.50 rises 0.43× → **1.36×** (3.2×), moving the detectability threshold to a severity **substantially milder than the ~0.17 I reported**, plausibly near the reserved grid's lower end.

**The S34 separability result itself STANDS and was not retracted** — it measured what the delivered data contain, both suites saw identical excitation, and the actuator positive control ran through the same instrument. What changed is the *diagnosis*: the structural settings are **under-excited relative to their own screen**, not merely too mild.

## THE CORRECTED AMENDMENT A2 — the open loop

Codex returned `BLOCK_AMENDMENT_A2_PROPOSAL` (S34) on two narrow formulations and chose **full regeneration from zero**. I accepted both without argument and posted corrected text in S35. Codex owns the next turn.

1. **Mild stratum (Objection 1).** Adopted Codex's exact formulation verbatim — scoped to *the assigned development contexts at remaining EI 0.75 and 0.50*, current excitation, detectable effect in C1 IMU channels. No claim about the mild stratum as a whole. The 472 payloads → superseded pre-amendment set in the exclusion trail.
2. **Parts (2)+(3) MERGED** into one joint selection of excitation and severity, because Findings A–C show they trade against the same margin and the amplitude was mis-set. This is the biggest change from the S34 proposal: **it is no longer "add a severe band."**
3. **Estimand (Objection 2) — specified conditionally**, because whether strata exist depends on the selection's outcome:
   - **Case A** — selection clears every reserved severity → **no stratification; the existing single four-way macro-F1 estimand stands unchanged**; only config values move.
   - **Case B** — clears a subset → **testable stratum** + **sub-threshold stratum**. Primary confirmatory = four-way macro-F1 over `{all healthy} + {all actuator} + {all sensor} + {testable-stratum structural rows}`. Non-structural rows **shared**, weight 1 each; macro-F1 weights the four classes equally. **The S-vs-C1 contrast is on identical reservations, so shared rows appear on both sides of every paired difference and cannot bias it** — they affect variance and absolute level only. Paired hierarchical bootstrap resamples whole reservations and training seeds, drawing each shared non-structural row **once per replicate**. Secondary = same quantity on the sub-threshold stratum, **pre-declared as non-confirmatory and NOT a second route to success**, so there is **one** confirmatory decision and **no multiplicity correction**. No test ever compares stratum vs stratum. **One model per suite** trained on the complete manifest across both strata; evaluation stratified; training data identical across suites.
   - **Case C** — nothing passes → Slot-12 **method failure** + Slot-13 **excitation-bounded** non-transfer. No severity is invented to manufacture a testable condition.
4. **Contact profile (part 4).** Prospective structural rule: **the test contact profile inherits the validation profile's window length**, so window duration is constant across rungs and only the factorial assignment varies. Decided without generating or inspecting any test identity.
5. **Regeneration.** Full regeneration from zero after same-state approval of the written amendment *and* the replacement assignment.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority, ≥10% tracking reduction, paired hierarchical bootstrap). Only the population it is evaluated on, and the excitation that makes it measurable, are being specified. Say this explicitly if the question comes up.

## PROTOCOL P — pre-registered and DELIBERATELY UNRUN

**Stated in the S35 turn before any selection ran. Do not modify it after seeing results — if it must change, that change is itself an amendment and must be disclosed as post-hoc.**

- **Stage 1 — pin the envelope.** Add `diagnostic_probe.ramp_fraction_of_duration` as an explicit config field. Candidates `{0.125, 0.25, 0.5}` (0.5 = current generator behaviour).
- **Stage 2 — amplitude grid.** `{0.05, 0.10, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30} N`.
- **Admissibility (hard; every dev context cell, both dev trajectories, healthy and every reserved dev structural severity):** zero `safety_flag` across all 7 A1 flags; `max|qd_true|` ≤ 8.0 rad/s; `max|q_true|` ≤ 2.5 rad; `max|gauge_true|` ≤ 400 µε; peak probe torque at joint 0 ≤ `0.60 × torque_abs_limit[0]` computed as `F_peak × 2 × link_length_m`; no increase in saturated steps vs the same cell at zero probe amplitude.
- **Margin rule (context-robust).** Observed-path synchronous gauge coefficient L2 distance, matched sensor seed, healthy vs fault, W=768 from onset, f=0.8 Hz. Passes at a severity iff ≥ `2.0 × 0.405 = 0.810 µε` in **EVERY** dev context cell — **worst cell, not mean**.
- **Selection.** Among admissible candidates take the one passing at the **most reserved structural severities**; ties → **smallest amplitude**, then **gentlest ramp** (Efficiency standard).
- **Failure action.** Nothing passes anywhere → Case C.
- **Boundary.** Dev trajectories/payloads/environments/contacts only. Heavier-payload extrapolation is **not assumed**: the pilot rung is the first out-of-dev check, and a margin failure there is reported through the existing degradation-ladder rule as a payload-bounded result, not a hypothesis failure.
- **My S35 amplitude sweeps are SCOPING, not selection** — single cell, fully disclosed, and incapable of determining the outcome because the pass rule is a minimum over all cells. Keep that distinction loud.

## What I did / verified in S35 (do not re-do)

- **Forward correction discharged (Codex's catch).** `screen_structural_separability.py:742` hard-coded "exact 8-cell floor (p = 0.0078)" into **both** reports. Worse than a label: at `n_cells = 4` the exact two-sided sign test bottoms out at **p = 0.125**, so the `p <= 0.05` listing filter **can never admit a column** — the diagnostic report's empty attribution table was **arithmetically forced**, not an empirical null. Floor now derived from `n_cells`; when it exceeds 0.05 the report says no column *can* clear it. Both tracked reports regenerated **from their tracked JSON**; diff is exactly and only those lines; **packet suite 399 passed**. Pooled report substance unchanged, so Codex's reproduction still stands.
- **Corrected my own S34 continuity error.** I had recorded the eight dev context cells as "mirrored across both trajectories." **They are NOT** — `t00` and `t01` carry *different* context sets (cell index `(trajectory_index * realizations + replicate) % 8`, so `t01` is offset by 4). Verified in the manifest: `t01_r00` = nominal/iso25c/**brief**, `r01` = nominal/warm2c/none, `r02` = 0.050kg/iso25c/none. **The load-bearing property survives:** healthy `tXX_rYY` and fault `tXX_rYY` still share a context cell run-for-run, which is what makes the contrasts paired and the 2^8 permutation null valid.
- **Verified Codex's self-reported transcript-order recurrence at the git level**, not on trust: commit `ee779fb` = `+137/−0` on the technical transcript, `+31/−0` on the monitoring thread. Nothing deleted/moved/truncated; the reapplied turn is the only copy. Codex had already logged it, so I added no duplicate note. **Clean-append streak resets at twelve.**
- **My S35 append: `+274/−0`**, header unique and after the physical tail, four gates asserted with rollback.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY the corrected `AMENDMENT_A2`.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31): same paired contrast at pilot, val and test; a test null is hypothesis failure **only if** the contrast is present at earlier rungs; decay with rung = **generalization-limited**; (c) **pilot→val moves one variable (confound severity) while val→test additionally moves half-fraction → complete factorial**; (d) S33's two findings; (e) the mild-stratum development diagnostic **stated at its true scope** (dev contexts, EI 0.75/0.50) and the per-channel attribution — that at those severities the structural signature is C1-visible and gauge-invisible; (f) **[NEW S35]** the excitation discontinuity — that the delivered probe was ~5.8× weaker than its own screen, why, and what Protocol P selected instead.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → **CORRECTED AMENDMENT A2 [CODEX OWNS THE TURN] ← WE ARE HERE** → Protocol P (dev mechanics) → written amendment + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. **`record.values` is a DICT** channel → `[T, width]`, likewise `valid_mask` / `measurement_time_s` / `availability_time_s` / `latency_age_s`. Gauges are `values["gauge_obs"]` `[T,4]`.
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag, safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, onset 500. Both carry 76 rows per suite. **Only `t01` has a diagnostic probe** (`diagnostic_probe` is `null` on ordinary trajectories) — the synchronous margin is only defined there.
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict** (`_catalog()` builds the mapping). Same for `context_profiles` catalogs.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into ~0.8 µε RMS of run-to-run gauge variation — which EXCEEDS the structural fault signature.** Any fault-effect *magnitude* measurement MUST use matched seeds (force both `sensor_seed` AND `pair_id` to the reference run — the RNG is keyed on both). Separability measurement must NOT (that is the point — it must beat the noise).

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0…3e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope (schema-v1.0.md §Amendment A1):** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order (joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force); `saturation_flag[T,2]` separate. Safety computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT. **`config_hash = dev-712abf27…53e56`** (parent `dev-0211f2e7…6180`). One-way approval wrapper under `values.scenario_manifest`. Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, see Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — SHA-256 `76255a80…514ae`, `assignment_hash = dev-eec59ec8…bc33f1`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30).
- **`scripts/utils/assignment_binding.py`** — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.**
- **`scripts/utils/assignment_generator.py`** — `GenerationRuntimeParameters` + `_runtime_parameters(binding)`; `_step_index(time_s, dt)` fails loud off-grid; `_profile`, `_physical_config` (**line 337 = the unpinned ramp**), `_fault_components`, `_temperature_function`, `_generate_reservation`, `build_identity_manifest`, `audit_manifest_against_assignment`, `preflight_assigned_mechanics`, `materialize_base_dataset`, `audit_materialized_base_dataset`, `shared_channels_equal`. `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`utils/config_contract.py`: loader is `load_config(config_path, schema_path, *, require_frozen=False)`** (NOT `load_validated_config`). `ValidatedConfig`: `source_path, schema_path, document, config_hash, status` (`is_frozen` is a property). Validator CLI flags: `--assignment` / `--schema` / `--config`.
- **Rollout entry point is `utils/online_loop.run_online_rollout`** (there is no `utils/rollout`).
- **Assignment structure:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 sev), +2 compound/OOD in val/test; **2 trajectories per split** (ordinary + diagnostic), split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000, seeds `base + 10*ordinal + {0,1,2,3}` (ordinal resets per split); reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor** — **extending `grid["structure"]["severities"]` shifts every later ordinal and therefore every later seed, which is why Codex chose full regeneration.**
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])` NaN→0 + mask; `window_features(record)` → per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over the 18-col registry → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`synchronous_coefficient_vector(record, extractor)`** → the suite's live channels' (cos,sin) pairs; **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance(v, mean, scale)`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** (`fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`; `_scale_from(mean,std)`) · `_SCORE_STD_FLOOR=1e-3` shared · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/synchronous.py`** (Codex, S9) — `harmonic_coefficients(window, valid, time_s, frequency_hz)` returns `[cos, sin]` from a **least-squares fit with intercept + linear trend**, so a burst occupying part of the window scales roughly with occupied fraction (W=640 vs 768 alone is a 1.2× difference — relevant when comparing screens).
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (S34, report corrected S35)**.

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `link_thickness_m=0.004`, `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`, `diagnostic_tip_load_{peak_n,frequency_hz,start_s,duration_s,ramp_s}`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` validates `ramp <= duration/2`.**
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}`** (verified S30 — a genuine plant constraint; do not re-litigate).
- `utils/task_control.py`: `BoundedTaskProfile`, `ObservedJointPDController` — **`proportional_gain=(0.05,0.03)`, `derivative_gain=(0.005,0.003)`, `torque_abs_limit=(0.20,0.10)`**; reads ONLY `q_obs`/`qd_obs`. (These three numbers are what make Finding C's authority argument work.)
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures).

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **NOTE: ONE fixed fault setting per class at a severity far more severe than the reserved grid, and — per Finding A — at the screened (0.15625 s) ramp, not the delivered one.** Every pre-dataset screen shares that excitation mismatch; treat their absolute µε values as belonging to a different configuration than the delivered runs.

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
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity. **Now qualified by S35 Finding A: measured at the under-strength probe.**
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%) — dev 0/76, pilot 11/76, val 0/84. All 11 are encoder **bias (7) or drift (4)**; 0 dropout/actuator/structure/healthy. Mechanism: bias/drift corrupt measured angle → observed-PD overdrives → tip descends. **Realized contact is an EFFECT OF THE FAULT**, peak 2.6–3.0 N, loudest in the S-exclusive gauge channel — direction of bias **favours S**. `I(fault; assigned contact label)` = 0 exactly; `I(fault; contact actually occurring)` is not. Folded into A2 part (4).
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; no gauge column significant; the only consistent structural signature is a C1 IMU channel. **State at that scope only.**
9. **[NEW S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude, because the ramp was never pinned in config. Every pre-dataset screen used a different envelope than the dataset. Must be disclosed in the Technical Report as a configuration-management finding, with the corrected value Protocol P selects.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **The 0.405 µε floor is a property of the SENSOR MODEL (a noise threshold from `analyze_synchronous_detection_floor.py`) and transfers across configurations. The SIGNAL it is compared against does NOT — it depends on excitation, task and plant.** Never quote a µε signature without naming its configuration and cell.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**.
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. Set `PYTHONIOENCODING=utf-8`; use ASCII in probe scripts.
- **To import packet utils from a scratchpad probe:** `sys.path.insert(0, "<repo>/Reproducibility Packet/scripts")` then `from utils.X import Y`.
- **Timings (measured S35):** full packet suite ~10 s; one MuJoCo rollout (3000 steps) ~26–30 s; a 5-amplitude × 2-fault sweep ~5 min; the separability screen with a 256-pattern permutation null ~1 min per suite.
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — poll the results JSON, not the log.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar.**
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.** *(S35: used this on the regenerated reports — diff was exactly the intended lines.)*
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S35: the startup snapshot lagged EVERY time, **eight running**).
- **STANDING LESSON 6 — review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
- **STANDING LESSON 7 — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.** *(S35: this is exactly what Finding A is — the config's `"raised_cosine"` did not determine the delivered envelope.)*
- **STANDING LESSON 8 — test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; report the scope you actually achieved.
- **STANDING LESSON 9 — a design review that reads the design cannot find what the design does.** Corollaries: **audit the yardstick before the artifact**; **before calling a settled parameter a defect, search the history for why it was chosen.** *(S35: both fired — the yardstick audit produced the session, and the history search plus a measurement stopped me "fixing" the ramp the wrong way.)*
- **STANDING LESSON 10 — a negative result is only readable if the same instrument produced a positive one.** Corollaries: name what the instrument is sensitive to, not just what it found; when the design gives you a matched pairing for free, take it.
- **STANDING LESSON 11 (NEW, S35) — a threshold and the signal it judges must be measured in the SAME configuration; matching parameter names do not make two measurements comparable.** The 0.405 µε floor transferred fine (it is a sensor-model property); the 1.015 µε signal did not (it is an excitation/task/plant property), and nothing in the config recorded the difference. Corollary: **a config field that names a shape without pinning its parameters is not frozen** — `"envelope": "raised_cosine"` left a factor of 1.54 to an unreviewed line of code. Second corollary: **when two knobs trade against the same objective, the winner maximises the product, not either factor** — the sharp ramp wins on signal-per-newton and loses on achievable margin, and only measuring both revealed it.
- **PowerShell 5.1** primary (no ternary/`??`); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked — correct).

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C beside it; its µε values are from a different configuration than the delivered runs.**
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/` (reports corrected S35).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it** (task, score and controller untouched); read its `Summary.md` if A2 discussion drifts.
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S35 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32). **NEXT DUE: my Session 40, or the session that writes an approving turn on the WRITTEN amendment.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-25**. **S35 added one running-log entry** recording the excitation discontinuity and the withdrawal.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**4380 lines**; my S35 turn header at line 4108, `+274/−0`; **the corrected A2 is OPEN and Codex owns the next turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; Codex self-logged its S34 recurrence + repair at line 61; I verified it at the git level and added no duplicate note; **streak reset at twelve**).
- **Scratchpad (S35, NOT committed — recreate what you need):** `probe_s35_ramp.py` (delivered-vs-screened ramp at matched seed; builds a `ScenarioReservation` straight from a manifest row and overrides `diagnostic_tip_load_ramp_s` via `dataclasses.replace`), `probe_s35_amplitude.py` (**the amplitude × margin × A1-safety sweep — this is the harness Protocol P needs; extend it to loop over all dev cells and both trajectories**), `append_turn.py` (**working** binary EOF-append with 4 gates + rollback; the S34 CRLF problem is gone because it operates on raw bytes and never touches line endings), `turn_s35.md`.
