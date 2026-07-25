# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 37, 2026-07-25 16:50 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 37**; next session I run is **Session 38**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**
- **THERE IS AN OPEN REVIEW LOOP AND CODEX OWNS THE NEXT TURN: `AMENDMENT_A2_PROPOSAL_V4` (my S37 turn, transcript line 5129).** Do not start Gate-4 work, and do not run Protocol P, until it settles.
- **NO PROGRESS REPORT IS DUE at S38.** Last regular was S32 (covers S25–S32). **Next regular: my Session 40.** The event trigger is an **approved amendment to the Claim Sheet** — the *written* amendment, not approval of a proposal text. If I write that approving turn, I write the report that session.

## THE HEADLINE OF SESSION 37 — read this before anything else

**Codex blocked v3 on two real structural defects (both correct, both mine) and approved five of my six arbitration requests. Fixing the block was routine. Pinning the four execution details it asked for is what produced everything below — including a third yardstick error and a design problem that must be decided before the next measurement.**

### The four things Codex approved outright (do not reopen)

Vector-8 aggregation · diagnostic-only screening universe · the ten-value development-conditions ladder with direct table lookup · `contact_test_sustained.contact_window_offset_s = [1.8, 3.3]`. Plus two rulings: **P v1→v2 is a supersession, not a correction** (so v2 is now presented clean and standalone), and **ordinary-trajectory (`t00`) structural rows stay in the primary estimand but my "can only shrink / never inflate" claim is struck** — a per-sample mechanics BLOCK bounds neither what a windowed learned estimator extracts from 768 samples nor the finite-sample direction of a difference. I accepted that fully; replacement wording is in the turn.

### Finding F — `T1` was the five-sigma point of the wrong random variable

`D` is a **difference** of two coefficient vectors. The `0.4388` committed in v3 is the five-sigma point of a **single** window's vector-8 norm. Measured, sensor model only, W=768, f=0.8 Hz, `pair_id=1`, seeds 0..199 → 100 **disjoint** pairs:

```text
statistic                                  mean     std      p95      5-sigma
||b||_2, one noise-only window (v3's T1)  0.1957   0.0486   0.2834   0.4388
||b_i - b_j||_2, seeds differ only        0.2787   0.0748   0.3958   0.6526
ratio of means 1.424  (sqrt(2) = 1.414)   <- the confirmation these are the objects I think
```

Single-window reproduces S36 to four decimals, so the harness is continuous; the defect is which line v3 quoted. **It is NOT repairable by substituting `0.6526`:** that is the *unmatched* difference null, while Stage A/B `D` is **matched on `(sensor_seed, pair_id)`**, so CRN cancels the sensor term. **A matched-seed difference has no useful sensor-only threshold at all.** `T1` is retired as a gate; its only surviving job is Stage C's validity tripwire (below), where pairs are unmatched by construction and therefore measure the same object.

### Finding G — `D` is thermally self-cancelling (a check that went against my hypothesis)

Realized per-window excursion in delivered dev diagnostic rows: `env_dev_iso25c` **0.0000 °C**, `env_dev_warm2c` **0.5113 °C**. The committed floor path assumes **3.0 °C** — 6× the worst real value — and it does not matter:

```text
ramp        difference mean   p95      5-sigma
0.0000 C        0.2795       0.3910   0.6514
0.5113 C        0.2802       0.3976   0.6586
3.0000 C        0.2787       0.3958   0.6526
```

Thermal cross-sensitivity is deterministic given the profile (10 µε/°C), and both windows of any difference share a profile, so **it cancels exactly**. The sensor pathology we modelled most carefully cannot inflate this statistic's noise. This is why Stage 0 is pinned at 3.0 °C — continuity with the committed artifact, and the sensitivity proves the choice cannot matter.

### Finding H — the approved torque gate caps amplitude at exactly 0.15 N

`F_peak * 2 * link_length_m <= 0.60 * torque_abs_limit[0]` → `F_peak * 0.80 <= 0.12` → **`F_peak <= 0.15 N`**. In IEEE double: 0.15 N → `0.12` exactly, limit `0.12` exactly, so it admits — **but only if written `<=`, not `<`.** Admissible amplitudes are **{0.05, 0.10, 0.15}**; 15 of 24 candidates die by arithmetic before any rollout. Codex's own `screen_synchronous_safe_probe.py` defaults to exactly `[0.05, 0.1, 0.15]` — independent corroboration. **Stage A worst case: 288 → 108 rollouts.** S35's "0.30 N violently unstable at 62 rad/s" was never a live candidate.

### Finding I — `NO_ADMISSIBLE_PROBE` is empirically near-empty

The delivered dev diagnostic rows **are** candidate `(0.05 N, ramp 0.5)` evaluated in all four screened cells at healthy / remEI 0.75 / remEI 0.50. All 12 rows pass every measurable gate: peak `|qd_true|` **0.784** vs 8.0 · peak `|q_true|` **0.397** vs 2.5 · peak `|gauge_true|` **6.13 µε** vs 400 · **0** saturated steps · **no** safety flags. Counterweight: S35 found 0.30 N violently unstable, so the dynamics turn sharply nonlinear between 0.15 and 0.30 N; the dynamic gates may bind at the top of the admissible band even though they are inert at the bottom. **Saturated-step baseline is 0 in every screened cell**, which makes the "no increase vs zero probe amplitude" gate exact.

## THE OPEN QUESTION — must be settled BEFORE Stage B runs

If the testable band lands at the severe end (now the most likely outcome), **every development-reserved severity is sub-threshold.** Reserved: dev `{0.75, 0.50}`, pilot `{0.85, 0.60}`, val `{0.90, 0.40}`+OOD 0.55, test `{0.65, 0.35}`+OOD 0.45. If testable = `{0.35, 0.40}`, the model trains on structural damage below the run-to-run null and is graded on damage above it. **A null would then be uninterpretable** — "strain carries no structural information" cannot be separated from "the model never saw a detectable example."

Three options handed to Codex, deliberately without advocacy:
1. **Accept and report** — pre-register it as a severity-coverage-bounded Slot-13 result; biased against S, so conservative, possibly uninformative.
2. **Rebalance severities across splits** — A2 already forces one regeneration, so deciding now is free and deciding later costs a second one. **DANGEROUS DIRECTION:** choosing which severities land in test partly on measured detectability selects test toward detectability and **favours S**. Only admissible as a symmetric rule fixed in advance (e.g. every split spans the same range), never a per-split adjustment.
3. **Leave the design alone and narrow the claim** to whatever turns out testable.

**The timing is the whole point:** after Stage B, any choice is made in knowledge of which severities passed, and option 2 becomes indefensible.

## PROTOCOL P v2 — clean, pre-registered, DELIBERATELY UNRUN

**Universe.** `trajectory_dev_diagnostic_b` (`t01`) only, cells 4/5/6/7 = replicates r00..r03 (r00 nominal/iso25c/brief, r01 nominal/warm2c/none, r02 0.050 kg/iso25c/none, r03 0.050 kg/warm2c/brief) — a balanced half-fraction. Ordinary trajectory stays probe-free as the pre-registered negative control.

**Statistic.** `D = || concat_{g=0..3} ( b_g(fault) − b_g(healthy) ) ||_2` over 8 entries, `b_g = utils.synchronous.harmonic_coefficients`, observed path `gauge_obs`, f=0.8 Hz, **W=768 from onset**, matched `sensor_seed` AND `pair_id`.

**Identity table (screen-private, fail-loud if it leaks).** `CablePlant` has **no RNG at all** (verified), so a rollout's stochastic identity is exactly `(sensor_seed, pair_id)`.
```text
P_SEED_BASE = 150000 ; P_PAIR_PREFIX = "basepair_protocolp"  (NO "_dataset0" suffix)
cell c in {4,5,6,7};  r = c - 4
Stage A + Stage B (all candidates, all conditions, all ladder values):
    sensor_seed = 150000 + 10*r + 2      -> 150002 150012 150022 150032
    pair_id     = "basepair_protocolp_stageAB_c{c}"
Stage C healthy replicate k in {0..7}:
    k = 0 : reuse the Stage-A healthy rollout of the SELECTED candidate exactly
    k>=1  : sensor_seed = 150000 + 10*r + 1000*k + 2
            pair_id     = "basepair_protocolp_stageC_c{c}_k{k}"
Stage 0 (no plant): pair_id = 1, sensor_seed = 0..199
```
Why safe: dataset seeds are `seed_base + 10*ordinal (+0..3)` (`utils/gate3_assignment.py:663-696`), dev occupying `[110000, 111514)`; the screen band `[150002, 157032]` cannot collide with dev and is far below pilot's 210000 — **no screen rollout shares an RNG stream with any dataset row**, stronger than v3's "dev seed base only". And the generator *requires* dataset `pair_id` to end `_dataset0` (`utils/assignment_generator.py:241-242`), so a screen row leaking into a manifest **fails that audit loudly**.

**Stage 0 (0 rollouts).** Add `timing.diagnostic_probe.ramp_fraction_of_duration`; candidates `{0.125, 0.25, 0.5}` (0.5 = current generator behaviour, `assignment_generator.py:337`; 0.125 = every pre-dataset screen). `cable_mechanics` validates `ramp <= duration/2` → admissible `(0, 0.5]`; at `cycles=1`, fraction-of-duration ≡ fraction-of-period. New packet script `scripts/analyze_synchronous_difference_null.py` → `results/protocol_p/sensor_only_difference_null.json`, reusing the gauge-window helper **lifted into `utils/`** (not copy-pasted). Pinned command: `--window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1`. **Sample definition: one sample = one PAIR of four-gauge windows → one scalar. 100 samples, not 200, and emphatically not 800** — `analyze_synchronous_detection_floor.py:241-242` appends one value **per gauge per realization**, which is exactly how `0.4053` became an 800-sample per-gauge number later read as a four-gauge one.

**Stage A — admissibility + selection (108 rollouts).** 9 admissible candidates × 4 cells × 3 conditions **{healthy, remEI 0.75, remEI 0.35}** (0.35 replaces v3's 0.50: same cost, brackets the whole compliance range the selected probe will be driven through). Hard gates, every cell, all three conditions: zero `safety_flag` across all 7 A1 flags; `max|qd_true| ≤ 8.0`; `max|q_true| ≤ 2.5`; `max|gauge_true| ≤ 400 µε`; the torque gate (`<=`); no increase in saturated steps vs zero probe amplitude (baseline 0). Failing candidate dropped, remaining cells skipped, drop count logged. **Selection: maximise worst-cell `D` at remEI 0.75, NO `T1` cutoff** (Codex's repair). Ties within 1% → smallest amplitude → largest ramp fraction ("gentlest ramp" := largest `ramp_fraction_of_duration`; ground: lower peak `|dF/dt|`, narrower spectrum, more headroom — Finding C).

**`NO_ADMISSIBLE_PROBE`** (all 24 fail a hard gate): pin `ramp_fraction_of_duration = 0.5`, keep 0.05 N, record Slot-12 method failure + Slot-13 excitation-bounded non-transfer, regenerate with the estimand **unstratified**. A safety/method failure, **not** a measured Case C.

**Stage B — the ladder (32 new rollouts).** Selected candidate at all ten reserved remaining-EI values `{0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90}` × 4 cells; `0.75` and `0.35` reused from Stage A at matched identity. Every ladder rollout re-asserts the hard safety gates; a violation labels that value **`unsafe_at_severity`**, excludes it with the reason recorded, and **does not reopen selection**.

**Stage C — the operative null (28 new rollouts).** **8** healthy replicates per cell (k=0 reused), all `C(8,2)=28` within-cell pairs. **Per-cell rule, operative:**
```text
Q95_c = 95th percentile of within-cell healthy/healthy D for cell c
pass(v) iff D(v,c) >= 2.0 * Q95_c for EVERY screened cell c
```
**Disclosed:** Codex's two offered rules are not equivalent — `min_c D >= 2*max_c Q95_c` implies the per-cell form, so **I picked the laxer one**. Ground: the noise obscuring a signal in cell c is cell c's noise; the scalar form judges the quietest cell's signal against the noisiest cell's null. Finding G supplies the physical mechanism for real cell-to-cell null differences (two cells iso25c at 0.0000 °C, two warm2c at 0.5113 °C, plus payload/contact differences). The scalar form is reported as a **pre-declared sensitivity**. Offered to switch without argument.
**The one change Codex did NOT request:** 6 → 8 replicates per cell. Its per-cell repair makes `Q95_c` an order statistic of 15 dependent distances from 6 draws (at n=15 the 95th percentile is essentially the max, so one unlucky pair sets a cell's bar). 28 pairs moves the quantile off the extreme. Cost **+8 rollouts ≈ 4 min**. Flagged explicitly; will hold at 6 without re-arguing if Codex calls it scope creep. Dependence remains at either count (28 pairs from 8 draws) — carried to the report.
**Validity tripwire:** assert `Q95_c >= 0.30 µε` per cell; stop and diagnose if it fires. Ground: sensor-only difference p95 is `0.391`–`0.398` across 0–3 °C, and Stage C's null is that plus closed-loop divergence. **The failure it exists to catch:** varying `sensor_seed` but not `pair_id` (or vice versa) collapses the null toward **zero** via CRN, collapsing `T2` with it and declaring **every** ladder value testable — silent, two orders of magnitude below the tripwire, and pointing the wrong way. Diagnostic, not a scientific gate.

**Outcome — aggregation stated explicitly.** One row per ladder value with `D(v,c)` for all four cells, `Q95_c`, `2*Q95_c`, per-cell verdict, value verdict. **Aggregation is the conjunction over all four cells**: testable iff `min_c [ D(v,c) − 2*Q95_c ] >= 0`. No mean/median/pooled quantity enters the verdict. **Case A** (all ten pass → no stratification) / **Case B** (proper subset → testable + sub-threshold strata, exactly as Codex approved in S34) / **Case C** (none pass **after all ten measured** → Slot-12 method failure + Slot-13 excitation-bounded non-transfer). **OOD role, pinned:** ladder labels at `0.45`/`0.55` characterize **mechanics testability only**; those rows keep `ood_flag=true`, stay excluded from four-way known-class macro-F1 under `ood_known_metric_rule`, and remain in the pre-registered OOD metrics.

**Cost:** Stage 0 = 0 · Stage A = 108 · Stage B = 32 · Stage C = 28 → **168 rollouts, ~78 min** at ~28 s/rollout (v3 said 348 / ~2.7 h). Background job; poll the results JSON.

**HONEST ODDS (revised, and they moved).** Max admissible amplitude is **0.15 N**, so S35's matched-seed vector-8 `D = 0.552` at 0.15 N / remEI 0.50 / cell r00 is near the **ceiling** at that severity, and worst-cell is below it; `D` scaled ~linearly with amplitude (0.175 at 0.05 N → 0.552 at 0.15 N), so there is no headroom left to buy. `Q95_c` is bounded below by ~`0.39`, and S36's cross-cell healthy pairs ran `0.265`–`0.448`, so `T2 = 2*Q95_c` plausibly lands near **`0.8`** → **dev's two severities are unlikely to pass.** The severe end is where the chance is: structural response grows **superlinearly** with damage (S20: remEI 0.50/0.25/0.10/0.05 → peak |gauge| 38.4/72.4/152.8/259.7 µε over healthy 19.2 — **direction only; do NOT import those magnitudes**, different excitation/window/aggregation/path). **Case B at the severe end is now most likely; Case C remains live; Case A unlikely.** That is exactly what makes the open question above load-bearing.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority, ≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds). Only the population it is evaluated on, and the excitation that makes it measurable, are being specified. Say this explicitly if it comes up.

## What I did / verified in S37 (do not re-do)

- Findings F–I above. **Zero rollouts spent** — sensor model plus already-delivered dev rows only.
- Read the seed derivation **from source** (`utils/gate3_assignment.py:663-696`): `seed = seed_base + 10*ordinal`, `sim/fault/sensor/controller = seed+0/1/2/3`, `base_pair_id = basepair_{split}_t{ti:02d}_f{fi:03d}_r{rr:02d}`, dataset `pair_id = base + "_dataset0"`. Ordinal nests (trajectory, fault, replicate), resets per split.
- Confirmed `utils/cable_plant.py` contains **no** seed/random/Generator — the plant is fully deterministic.
- Confirmed `analyze_synchronous_detection_floor.py:241-242` pools **per gauge per realization** (800 samples at 200 realizations) — the mechanism behind Finding D.
- **Packet suite: 399 passed** (9.63 s, scoped). `config.json` absent at both candidate paths.
- **Codex's S36 append verified at git level: `+145/−0`.** Clean. **Clean-append streak: three.** No monitoring-thread note (duty is to flag recurrences; one clean check already on record, S23).
- **My S37 append: `+505/−0`**, header unique at line 5129, after the 5127-line physical tail, four gates asserted with rollback.
- Live-Run README: one running-log entry, `+2/−0`.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY `AMENDMENT_A2_PROPOSAL_V4`, then Protocol P v2.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** (dev contexts, EI 0.75/0.50) and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (Finding D) + the run-to-run range statement (Finding E) + trajectory-partial margin coverage; (h) **[NEW S37]** the operation mismatch (Finding F), the thermal self-cancellation (Finding G) as a *property* of the statistic, and the amplitude ceiling (Finding H) as the reason the excitation could not be strengthened further.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → **`AMENDMENT_A2_PROPOSAL_V4` [CODEX OWNS THE TURN] ← WE ARE HERE** → Protocol P v2 (Stage 0/A/B/C) → Codex reviews implementation + result + branch → written amendment + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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
- **Manifest columns:** `schema_version, config_hash, scenario_spec_id, pair_id, run_id, trajectory_spec_id, fault_setting_id, split_group_id, split, suite, estimator_id, controller_id, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed, train_seed`. **Note `trajectory_spec_id`, not `trajectory_id`; `fault_setting_id`, not `source_class`.**
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. **`record.values` is a DICT** channel → `[T, width]`, likewise `valid_mask` / `measurement_time_s` / `availability_time_s` / `latency_age_s`. Gauges are `values["gauge_obs"]` `[T,4]`. **`measurement_time_s["gauge_obs"]` may be 1-D — guard `ndim` before slicing `[:,0]`.**
- **Load one plant trace:** `PrivilegedRecord.load_npz(root/"plant"/f"{run_id}.npz")` (`utils.schema_types`).
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag[2], safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, **onset 500**. Both carry 76 rows per suite. **Only `t01` has a diagnostic probe** — the synchronous margin is only defined there.
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict** (`_catalog()` builds the mapping). Same for `context_profiles`, whose keys are `payloads` / `environments` / `contacts`.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into gauge variation that EXCEEDS the structural fault signature (S36 Finding E).** Any fault-effect *magnitude* measurement MUST match both `sensor_seed` AND `pair_id`. Separability measurement must NOT (that is the point).

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0…3e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope (schema-v1.0.md §Amendment A1):** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order (joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force); `saturation_flag[T,2]` separate. Computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT. **`config_hash = dev-712abf27…53e56`** (parent `dev-0211f2e7…6180`). Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, S35 Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — SHA-256 `76255a80…514ae`, `assignment_hash = dev-eec59ec8…bc33f1`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30). Probe `start_offset_s` per split: dev 1.0, pilot 1.2, val 0.9, test 1.1.
- **`scripts/utils/assignment_binding.py`** — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.**
- **`scripts/utils/assignment_generator.py`** — `GenerationRuntimeParameters` + `_runtime_parameters(binding)`; `_step_index` fails loud off-grid; `_profile`, `_physical_config` (**line 337 = the unpinned ramp, `duration/2`**), `_fault_components`, `_temperature_function`, `_generate_reservation`, `build_identity_manifest`, `audit_manifest_against_assignment`, `preflight_assigned_mechanics`, `materialize_base_dataset`, `audit_materialized_base_dataset`, `shared_channels_equal`. **Lines 241-242 assert dataset `pair_id` ends `_dataset0`.** `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`scripts/utils/gate3_assignment.py`** — `expand_reservations` at **lines 648-697** is the seed/ordinal/context-cell derivation (see identity table above).
- **`utils/config_contract.py`: loader is `load_config(config_path, schema_path, *, require_frozen=False)`.** `ValidatedConfig`: `source_path, schema_path, document, config_hash, status` (`is_frozen` is a property). Validator CLI flags: `--assignment` / `--schema` / `--config`.
- **Rollout entry point is `utils/online_loop.run_online_rollout(plant, sensors, *, n_steps, history_steps, command_policy, reference_fn=None, temperature_fn=None)`** (there is no `utils/rollout`).
- **Assignment structure:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 sev), +2 compound/OOD in val/test; **2 trajectories per split** (ordinary + diagnostic), split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000; reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor** — **extending `grid["structure"]["severities"]` shifts every later ordinal and therefore every later seed**, which is why Codex chose full regeneration.
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.
- **Context cell table** (index `(trajectory_index * realizations + replicate) mod 8`), each `[payload_idx, env_idx, contact_idx]`: `0:[0,0,0] 1:[0,1,1] 2:[1,0,1] 3:[1,1,0] 4:[0,0,1] 5:[0,1,0] 6:[1,0,0] 7:[1,1,1]`. `t00`→{0,1,2,3}, `t01`→{4,5,6,7} (verified row by row from the manifest, S36).
- **Contact profiles:** dev_none `null`; dev_brief `[2.0,2.5]`; pilot_none; pilot_delayed `[2.6,3.2]`; val_none; val_extended `[1.8,3.3]`; test_none; test_sustained `[1.6,3.8]` → **A2 pin 4 changes this to `[1.8,3.3]`**. All non-null profiles use `endpoint_plane_z_m = 0.2`.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])` NaN→0 + mask; `window_features(record)` → per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over the 18-col registry → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`synchronous_coefficient_vector(record, extractor)`** → the suite's live channels' (cos,sin) pairs; **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance(v, mean, scale)`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** (`fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`; `_scale_from(mean,std)`) · `_SCORE_STD_FLOOR=1e-3` shared · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/synchronous.py`** (Codex, S9) — `harmonic_coefficients(window, valid, time_s, frequency_hz)` returns `[cos, sin]` from a **least-squares fit with intercept + centred linear trend**; `harmonic_amplitude` is the L2 norm of that **single-channel** pair. Requires ≥5 finite valid samples; fails loud on rank deficiency or non-increasing time.
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (S34, report corrected S35)**.
- **`analyze_synchronous_detection_floor.py`** — mine, and now carries **two** usage corrections. Publishes `detect_threshold_microstrain = nes_mean + 5*nes_std`, **per gauge**, at `--window 640`, `--thermal-ramp-c 3.0`, 200 realizations, `--seed 0`, `pair_id=1` hard-coded at line 183. **It is a threshold, not a floor (S36); and it is the null of a SINGLE window, not of a difference (S37).** Its `null_sync` list appends per gauge per realization (lines 241-242) → 800 samples.

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `link_thickness_m=0.004`, `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`, `diagnostic_tip_load_{peak_n,frequency_hz,start_s,duration_s,ramp_s}`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` validates `ramp <= duration/2`.**
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **No RNG anywhere in the file (verified S37).** **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}`** (verified S30 — a genuine plant constraint; do not re-litigate).
- `utils/task_control.py`: `BoundedTaskProfile`, `ObservedJointPDController` — **`proportional_gain=(0.05,0.03)`, `derivative_gain=(0.005,0.003)`, `torque_abs_limit=(0.20,0.10)`**; reads ONLY `q_obs`/`qd_obs`. (`torque_abs_limit[0]=0.20` is what makes Finding H's 0.15 N ceiling.)
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- **`screen_synchronous_safe_probe.py`** — loads `window_samples` AND `detect_threshold_microstrain` from the floor summary JSON, so it is **internally coherent** (W=640, per-gauge, max-across-gauges). `--ramp-period-fraction` default **0.125**; **`--peak-loads-n` default `[0.05, 0.1, 0.15]`** (= Finding H's admissible set). It measures the **privileged** `gauge_microstrain` difference, not the observed path.
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures). **Use the direction, never the magnitudes.**

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **NOTE: ONE fixed fault setting per class at a severity far more severe than the reserved grid, at the screened (0.15625 s) ramp not the delivered one, under a per-gauge/W=640 yardstick, on a single-window statistic.** Every pre-dataset screen's absolute µε values belong to a different configuration than the delivered runs.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C).
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy; encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers, UNCHANGED by A2):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent. **A2 Case C would land on method failure + excitation-bounded.**
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test; main effects and two-factor interactions estimable everywhere; cannot favour either suite.
2. **The OOD arm rests on only 2 compound settings per split** (16 val / 32 test runs, 2 fault types) — thin. **A2 adds no severe-band OOD settings; no severe-band OOD claim will be made.**
3. **Test severities sit partly outside the fit hull**; the severity regression head extrapolates at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` is vacuous — the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** uses `expected_cell_count = min(len(table), trajectory_count * repetitions)`, correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity. **Triply qualified now:** S35 Finding A (under-strength probe), S36 Finding D (mis-matched yardstick), S37 Finding F (wrong operation).
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%) — dev 0/76, pilot 11/76, val 0/84. All 11 are encoder **bias (7) or drift (4)**; 0 dropout/actuator/structure/healthy. Mechanism: bias/drift corrupt measured angle → observed-PD overdrives → tip descends. **Realized contact is an EFFECT OF THE FAULT**, peak 2.6–3.0 N, loudest in the S-exclusive gauge channel — direction **favours S**. `I(fault; assigned contact label)` = 0 exactly; `I(fault; contact actually occurring)` is not. Addressed by A2 pin 4.
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; no gauge column significant; the only consistent structural signature is a C1 IMU channel. **State at that scope only.**
9. **[S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude, because the ramp was never pinned in config.
10. **[S36] The yardstick discontinuity (Finding D)** — a per-gauge five-sigma threshold at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax.
11. **[S36] The run-to-run range statement (Finding E)** — delivered fault−healthy gauge differences fall inside the range spanned by fault-free healthy pairs. **Report as a range statement, never as a test.**
12. **[S36] Margin coverage is trajectory-partial** — the rule certifies only diagnostic-trajectory rows; ordinary-trajectory structural rows stay in the estimand, **not certified by the diagnostic margin** (S37 wording, after Codex struck "conservative"/"never inflate"). Trajectory-stratified secondary report accompanies it.
13. **[NEW S37] The operation mismatch (Finding F)** — a threshold measured on a single window applied to a difference of two; and, more fundamentally, **a matched-seed difference admits no sensor-only threshold at all** because CRN cancels the sensor term.
14. **[NEW S37] Thermal self-cancellation (Finding G)** — a *property*, not a defect: `D`'s null is invariant across 0–3 °C per-window excursion, so the project's most carefully modelled sensor pathology cannot inflate it. Worth reporting because it bounds what the realism modelling buys for this statistic.
15. **[NEW S37] The amplitude ceiling (Finding H)** — the probe could not be strengthened past 0.15 N without violating an approved actuator-authority limit. This is why "just probe harder" is not available and why a Case C result would be excitation-bounded rather than a free choice.
16. **[NEW S37] Stage-C null dependence** — `Q95_c` comes from 28 pairwise distances generated by only 8 independent runs; it is a U-statistic, not 28 independent samples.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)`** — `pair_id` load-bearing; screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window, the aggregation, the path (privileged vs observed) *and the operation* (single vs difference, matched vs unmatched). The SIGNAL it is compared against depends on excitation, task and plant.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**.
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. Set `PYTHONIOENCODING=utf-8`; use ASCII in probe scripts.
- **To import packet utils from a scratchpad probe:** `sys.path.insert(0, "<repo>/Reproducibility Packet/scripts")` then `from utils.X import Y`.
- **Timings (measured S35–S37):** full packet suite ~10 s; one MuJoCo rollout (3000 steps) ~26–30 s; a 200-realization sensor-only null at W=768 across 4 gauges ~40 s (no MuJoCo); reading 12 delivered plant traces ~5 s.
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — poll the results JSON, not the log.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar.**
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.**
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S37: the startup snapshot lagged EVERY time, **ten running**).
- **STANDING LESSON 6 — review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
- **STANDING LESSON 7 — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.**
- **STANDING LESSON 8 — test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; report the scope you actually achieved.
- **STANDING LESSON 9 — a design review that reads the design cannot find what the design does.** Corollaries: **audit the yardstick before the artifact**; **before calling a settled parameter a defect, search the history for why it was chosen.**
- **STANDING LESSON 10 — a negative result is only readable if the same instrument produced a positive one.**
- **STANDING LESSON 11 (S35) — a threshold and the signal it judges must be measured in the SAME configuration; matching parameter names do not make two measurements comparable.** Corollaries: a config field naming a shape without pinning its parameters is not frozen; when two knobs trade against the same objective, the winner maximises the product.
- **STANDING LESSON 12 (S36) — when you import a number, import its definition, not its name.** Corollary: **two configuration errors can cancel, and that is dangerous rather than lucky.**
- **STANDING LESSON 13 (S36) — when a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** *(S37: applied twice — the vector-8 SNR disclosure carried forward, and the proof that Codex's two Stage-C rules are not equivalent and I picked the laxer.)*
- **STANDING LESSON 14 (S36) — a pre-registered protocol must be executable by someone who did not write it.** **Corollary (S37): the act of making it executable is itself the defect-finding technique.** All four of S37's findings came out of pinning, none out of reviewing.
- **STANDING LESSON 15 (S36) — the cleanest statement of a negative is often a comparison you have not made yet.**
- **STANDING LESSON 16 (NEW, S37) — match the null to the OPERATION, not just to the configuration.** Findings D and F are the same mistake at two depths: D got the window/aggregation wrong, F got the *operation* wrong (a single window's spread standing in for the spread of a difference). Ask "the null of *what computation*, performed how many times, on how many objects?" **And: common random numbers can void an entire class of threshold.** Matching seeds to isolate an effect also cancels the noise term any unmatched null would have bounded — so a matched statistic may correctly have *no* usable sensor-only threshold, and the honest move is to say so rather than supply the nearest available number.
- **STANDING LESSON 17 (NEW, S37) — compute the closed-form consequences of every gate you approve, before it costs anything.** The torque gate sat approved for two sessions while nobody multiplied `0.15 × 0.80`. It silently pruned 62% of the candidate grid and halved the protocol's cost. Corollary: **check boundary cases for `<` vs `<=`** — the largest admissible candidate landed exactly on the limit.
- **STANDING LESSON 18 (NEW, S37) — when the most likely branch creates a design problem, force the decision BEFORE the measurement that would make any fix look chosen.** The training-coverage question is worth more than any number this session produced, precisely because in two sessions it would have been unfixable without bias.
- **PowerShell 5.1** primary (no ternary/`??`); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked — correct).

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C, S36 Finding D and S37 Finding F beside it.**
- **The detection-floor record:** `Reproducibility Packet/results/synchronous_detection_floor/summary.json` — **`detect_threshold_microstrain` is a 5σ threshold, per gauge, at W=640, of a SINGLE window.**
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/` (reports corrected S35).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it** (task, score and controller untouched).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S37 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32). **NEXT DUE: my Session 40, or the session that writes an approving turn on the WRITTEN amendment.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-25**. **S37 added one running-log entry** (+2/−0) leading with the training-coverage problem rather than the third yardstick error.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**5632 lines**; my S37 turn header at line 5129, `+505/−0`; **`AMENDMENT_A2_PROPOSAL_V4` is OPEN and Codex owns the next turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (89 lines; unchanged in S37 — no recurrence; **streak three**).
- **Scratchpad (S37, NOT committed — recreate what you need):** `probe_s37_pins.py` (**torque gate + difference null + admissibility dry run; the difference-null function is nearly the Stage-0 artifact already**), `probe_s37_thermal.py` (**realized thermal + null-vs-ramp sweep**), `s37_pins.json`, `s37_thermal.json`, `probe_s36_yardstick.py`, `append_turn.py` (**working** binary EOF-append with 4 gates + rollback; raw bytes so CRLF is never touched), `turn_s37.md`.
