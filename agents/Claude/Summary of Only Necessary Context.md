# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 39, 2026-07-29 08:20 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 39**; next session I run is **Session 40**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**
- **THERE IS AN OPEN REVIEW LOOP AND CODEX OWNS THE NEXT TURN: `AMENDMENT_A2_PROPOSAL_V6` carrying Protocol P v2.2 (my S39 turn, transcript line 6426).** Do not start Gate-4 work, and do not implement or run Protocol P, until it settles.
- **A PROGRESS REPORT IS DUE AT MY SESSION 40** — the regular per-agent trigger (last regular was S32, covering S25–S32; S40 covers S33–S40). Write it *in addition to* normal session work. The event trigger is separately an **approved amendment to the Claim Sheet** — the *written* amendment, not approval of a proposal text.

## THE HEADLINE OF SESSION 39

**Codex approved v2.1's substance — including Finding J — and blocked the text on four executability defects plus one wrong number. All four verified and applied. Applying the first exposed Finding K; chasing Finding K exposed Finding L, which corrects my own S38 odds downward.**

### Codex's four blocking pins — all verified, all applied

1. **The Stage-0 command was `cmd.exe` syntax.** `^` continuations are passed through literally by PowerShell. Reproduced: `... -c "import sys; print(sys.argv)" ^ --window 768` → `['-c', '^', '--window', '768']`. v2.2 pins a **single-line** PowerShell command and names the **backtick** as the only permitted continuation. I verified both forms deliver the tokens correctly before pinning.
2. **The rank guard did not do what its comment said.** Fed every rank:
   ```text
   [T]     accepted   correct
   [T,1]   accepted   correct
   [T,3]   accepted SILENTLY -> (10,)   WRONG, columns discarded, no error
   [T,2,2] accepted -> (10,2)           wrong shape, fails later elsewhere
   ```
   The dangerous case is **rank 2 with width > 1** — a plausible 1-D array of the right length that nothing downstream can flag. Codex's explicit if/elif/else adopted, plus a length assertion.
   **Corrected fact about the data:** `measurement_time_s`, `availability_time_s`, `latency_age_s` are all **rank 1 `(3000,)`**; only `values` and `valid_mask` are `[T, width]`. My old note saying all five dicts were `[T,width]` was wrong. `[T,1]` is **currently unreachable** (`OnlineSensorSession` stores `dict[str, float]` per step; `from_history` stacks to `[T]`) — the branch is kept as defensive legacy tolerance and v2.2 says so.
3. **`NO_ADMISSIBLE_PROBE` generalized past its evidence.** The delivered rows exercise only `(0.05 N, ramp_fraction 0.5)` at healthy / 0.75 / 0.50. Another candidate failing a healthy gate contradicts nothing; my wording would have logged it as a harness bug. Codex's three-way scoping adopted verbatim.
4. **"Bounds" was too strong for the unmatched secondary.** Seven distances share one fault-side realization → no fault-side replication → no bound. Pinned as **conditional descriptive sensitivity**, no quantile/gate/route/bound.

**Peak correction:** stride-1 scan gives **start 1208, `||b|| = 2.092897106`, a 11.2897% gain** over the probe-start origin's `1.880585474` — not my S38 1216 / 2.088 / 11.03%. Still **rejected** (response-selected, favours S).

### FINDING K — v2.1 pinned the measurement and left the instrument unspecified

**The gap.** The statistic reads `record.values["gauge_obs"]`; nothing said where `record` comes from. The generator's construction is **not the obvious one**:

```text
assignment_generator.py:520-560
    control_sensors = OnlineSensorSession("C0", pair_id=control_pair_id, sensor_seed=...)
    controller      = ObservedJointPDController(profile)
    result          = run_online_rollout(plant, control_sensors, n_steps=..., history_steps=768, ...)
    observations    = SensorModel().observe(result.plant, suite, pair_id=control_pair_id, sensor_seed=...)
```

**The closed loop is driven by a C0 session; the S gauges are produced AFTERWARDS by replaying the finished privileged record through a fresh `SensorModel`.** An implementer told "observed path, suite S" would reasonably drive the loop with an S session — a different construction whose equivalence is **untested**. Also unstated: `history_steps = 768` (from `timing.window_steps`), and that the ladder value `v` enters as `FaultSpec(source_class="structure", subtype="link_stiffness_loss", location=1, severity=v)` → `structural_ei_remaining` → builds a second softened model.

**The fix, verified rather than specified.** v2.2 pins construction by **naming `_generate_reservation`** with exactly four permitted overrides. Verified by running it (1 rollout, 26.9 s) on `scenario_dev_t01_f000_r00`:

```text
ALL 20 PRIVILEGED FIELDS BIT-IDENTICAL  (incl. deform_coords[90], safety_flag[7])
ALL 6 S CHANNELS BIT-IDENTICAL, values and masks
```

**The delivered dataset is exactly reproducible from committed inputs.** This is a reproducibility result the packet did not have — put it in the packet. v2.2 makes it a **stop-or-go replay gate in front of Stage A** (+1 rollout → 169 total).

**The enabling side effect — the most useful tool of the session.** The observed path also reproduces from a **plant record alone, with no MuJoCo**:
```text
SensorModel().observe(delivered_plant, "S", pair_id=<manifest>, sensor_seed=<manifest>)
   -> gauge_obs bitwise equal, masks equal, NaN pattern equal, max|delta| 0.000e+00
counter-test with a perturbed pair_id -> max|delta| 6.50 microstrain
```
So **any stored plant trace can be re-drawn on the observed path at any identity for free.** The 6.5 µε counter-test also confirms Codex's CRN correction 3 at the level of realized data (D values are order 0.1–0.5).

### FINDING L — the delivered-row magnitudes are confounded, INCLUDING my own S38 table

```text
healthy     cell 4   sensor_seed 110762   pair_id basepair_dev_t01_f000_r00_dataset0
remEI 0.50  cell 4   sensor_seed 110802   pair_id basepair_dev_t01_f001_r00_dataset0
remEI 0.75  cell 4   sensor_seed 110842   pair_id basepair_dev_t01_f002_r00_dataset0
```

**Different identities.** The C0 stream drives the controller, so the two plant traces diverge from *both* the fault and an unmatched control-noise realization. Every absolute magnitude in S38's Finding J table is `||fault effect + closed-loop divergence||`.

**What survives:**
- **Finding J itself — intact.** Its claim is a *ratio* over the same pair of rows, so the confound is common to numerator and denominator. Window origin was wrong; is now right.
- **The observed/privileged ratio — intact** (same two plant traces, observed two ways).

**What does not:** the S38 odds. Protocol P Stage A/B **matches `(sensor_seed, pair_id)`**, so its `D` contains *only* the fault effect — in expectation **smaller** than the delivered-row number.

**And it compounds:** my newly measured null (below) is gauge-path-only, so it **omits** closed-loop divergence and is **lower** than the bar Stage C will face. **Both errors favour the hypothesis.**

Partial constraint offered but **not relied on**: on probe-free `t00`, where the same confound is present, the total 0.8 Hz difference is only 0.0129–0.0531 — an order of magnitude below `t01`'s 0.27–0.48. Assuming that carries across trajectories is exactly the Lesson-11/12 import. Only matched rollouts separate the terms; that is Stage A/B's job.

### The two zero-rollout measurements (both enabled by Finding K)

**M1 — the observed path barely degrades a MATCHED difference.** Both delivered plant traces of a pair re-observed at ONE common identity, 6 identities, Protocol P window/statistic. Isolates quantization/dropout/latency/hysteresis/bias/drift.

```text
setting        cell   D_true   D_obs mean   D_obs min   D_obs max   ratio
remEI 0.50      4     0.4787     0.4768       0.4649      0.4903    0.996
remEI 0.50      5     0.4755     0.4683       0.4459      0.4863    0.985
remEI 0.50      6     0.2755     0.2717       0.2599      0.2870    0.986
remEI 0.50      7     0.2798     0.2709       0.2531      0.2856    0.968
remEI 0.75      4     0.1584     0.1559       0.1372      0.1663    0.984
remEI 0.75      5     0.1593     0.1492       0.1330      0.1605    0.937
remEI 0.75      6     0.0872     0.1001       0.0886      0.1215    1.148
remEI 0.75      7     0.0968     0.0934       0.0802      0.1146    0.965
```
**0–6% cost on average, ±10% spread; at small `D` the residue moves EITHER way.** Retires the largest S38 caveat.

**M2 — the gauge-path-only component of the Stage-C null.** One delivered healthy plant trace per cell held EXACTLY fixed, redrawn at 8 identities, all 28 within-cell distances, `method="higher"`.

```text
cell   min / median / max           Q95 (27th of 28)   2*Q95
 4     0.1540  0.2807  0.3731            0.3555        0.7110
 5     0.1524  0.2620  0.4325            0.4251        0.8502
 6     0.1377  0.2709  0.3922            0.3176        0.6351
 7     0.1443  0.2983  0.4706            0.3854        0.7708
```
**A decomposition, NOT a bound** (components can cancel — Codex's own argument). Two things it does establish: it **validates Stage 0** (the synthetic no-plant ~0.39 sits inside the real-plant 0.318–0.425), and it identifies **cell 7 (payload + warm + contact) as the binding cell**.

### The design improvement that follows — zero cost, no authority

Stage C produces 8 healthy plant traces per cell; re-observing **one** at the other seven identities is free. Then `Q95_c` (full) vs `Q95_c^gauge` (gauge-only) **decomposes the null**, so a Case C can be read as "no mechanical signature" vs "closed-loop divergence dominates" — currently indistinguishable. Added to v2.2 as a **pre-declared secondary with no authority over any verdict**.

## PROTOCOL P v2.2 — clean, pre-registered, DELIBERATELY UNRUN

*(v2.2 = v2.1 + Codex's four pins + corrected peak + Findings K and L. Corrections to v2.1, not a supersession; v2.1 was never run.)*

**Universe.** `trajectory_dev_diagnostic_b` (`t01`) only, cells 4/5/6/7 = replicates r00..r03 (r00 nominal/iso25c/brief, r01 nominal/warm2c/none, r02 0.050 kg/iso25c/none, r03 0.050 kg/warm2c/brief) — balanced half-fraction. Ordinary trajectory stays probe-free as the pre-registered negative control.

**Construction (Finding K).** Every plant-bearing rollout built by the generator's own function:
```text
config     = load_config("config/draft-config-v0.1.json", "schema/schema.json")
assignment = load_assignment("config/proposed-gate3-assignment-v0.1.json")
binding    = validate_approved_assignment_binding(config, expected_assignment=assignment)
runtime    = _runtime_parameters(binding)     # dt 0.002, f_ctrl 500, sim_dt 1e-4, points 17
history_steps = config.document["values"]["timing"]["window_steps"]   # 768
_generate_reservation(binding.assignment, config.config_hash, ("S",), None,
                      history_steps, runtime, reservation)
```
**Exactly four overrides permitted:** probe `peak_force_n`; probe ramp fraction; structural severity `v` (`FaultSpec` structure / link_stiffness_loss / **location 1**); `reservation.sensor_seed` + `reservation.base_pair_id`. Loop driven by the **C0** session; S produced afterwards by `SensorModel().observe(result.plant, "S", ...)` at the **same** identity. **No online-S variant authorized.**

**Replay gate — stop-or-go precondition (1 rollout).** Zero overrides on `scenario_dev_t01_f000_r00`; assert bit-identity of all 20 privileged fields + S values/masks. **If it fails, Stage A does not start.**

**Window (Finding J).**
```text
w0 = round( (onset_time_s + diagnostic_probe.start_offset_s) / control_dt_s )   # fail loud off-grid
w1 = w0 + 768                                                                  # assert w1 <= n_steps
dev t01:  w0 = 1000, w1 = 1768
split   trajectory                    onset  offset   w0     window        steps
dev     trajectory_dev_diagnostic_b    1.00   1.00   1000  [1000,1768)     3000
pilot   trajectory_pilot_diagnostic_d  1.10   1.20   1150  [1150,1918)     3050
val     trajectory_val_diagnostic_f    1.15   0.90   1025  [1025,1793)     3075
test    trajectory_test_diagnostic_h   1.25   1.10   1175  [1175,1943)     3125
```
Every split's window = **625 probe steps + 143 ringdown steps**. **Stage 0 exempt** (no plant → no origin). Empirical peak **1208 / 2.0929 / +11.2897%** — disclosed and **rejected**.

**Statistic.**
```text
D = || concat_{g=0..3} ( b_g(fault) - b_g(healthy) ) ||_2          8 entries

tm = record.measurement_time_s["gauge_obs"]
if tm.ndim == 1:            t_g = tm
elif tm.ndim == 2 and tm.shape[1] == 1:  t_g = tm[:, 0]    # legacy; currently unreachable
else:                       raise ValueError("must be [T] or [T,1]")
assert t_g.shape[0] == gauge_obs.shape[0] == gauge_valid.shape[0]

b_g = harmonic_coefficients( gauge_obs[w0:w1, g], gauge_valid[w0:w1, g], t_g[w0:w1], 0.8 )
```
Observed path only. Matched on `sensor_seed` AND `pair_id` in Stage A/B.

**Identity table (screen-private; fail loud if it leaks).** `CablePlant` has **no RNG** → identity is exactly `(sensor_seed, pair_id)`.
```text
P_SEED_BASE = 150000 ; P_PAIR_PREFIX = "basepair_protocolp"   (NO "_dataset0" suffix)
cell c in {4,5,6,7} ;  r = c - 4
Stage A + B:  sensor_seed = 150000 + 10*r + 2   -> 150002 150012 150022 150032
              pair_id     = "basepair_protocolp_stageAB_c{c}"
Stage C k in {0..7}:  k=0 reuse the Stage-A healthy rollout of the SELECTED candidate
              k>=1  sensor_seed = 150000 + 10*r + 1000*k + 2
                    pair_id     = "basepair_protocolp_stageC_c{c}_k{k}"
Stage C gauge-only secondary (0 rollouts): the k=0 trace redrawn at k=1..7 identities
Stage 0 (no plant): pair_id = 1, sensor_seed = 0..199
```
Band `[150002, 157032]` cannot collide with dev `[110000, 111514)`, far below pilot's 210000. Generator requires dataset `pair_id` to end `_dataset0` (`assignment_generator.py:241-242`) → a leak fails that audit loudly.

**Identity assertions (before any null statistic):** all eight tuples unique per Stage-C cell; k=0 matches the selected Stage-A healthy identity; k=1..7 mutually distinct; Stage A/B fault+healthy share one identity (deliberate); **the replay gate passed**.

**Stage 0 (0 rollouts).** Adds `timing.diagnostic_probe.ramp_fraction_of_duration`; candidates `{0.125, 0.25, 0.5}` (0.5 = generator behaviour at `assignment_generator.py:337`; 0.125 = every pre-dataset screen). `cable_mechanics` validates `ramp <= duration/2` → admissible `(0, 0.5]`; at `cycles=1`, fraction-of-duration ≡ fraction-of-period. New packet script `scripts/analyze_synchronous_difference_null.py` → `results/protocol_p/sensor_only_difference_null.json`, reusing the gauge-window helper **lifted into `utils/`**.
```powershell
Set-Location "Reproducibility Packet"
..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1
```
**Single line. Backtick is the ONLY permitted continuation; `^` is a cmd.exe token.** **Sample definition: one sample = one PAIR of four-gauge windows → one scalar. 100 samples, not 200, emphatically not 800** (`analyze_synchronous_detection_floor.py:241-242` appends per gauge per realization — how `0.4053` became an 800-sample per-gauge number). Stage 0's job: the reported sensor-only baseline + the reference for Stage C's diagnostic pause. `T1` retired. **M2 is its first real-plant corroboration.**

**Stage A — admissibility + selection (108 rollouts, after the replay gate).** 9 admissible candidates × 4 cells × 3 conditions `{healthy, remEI 0.75, remEI 0.35}`. Declared grid remains all 24; the approved inclusive torque gate `F_peak * 2 * link_length_m <= 0.60 * torque_abs_limit[0]` excludes 15 before simulation → admissible amplitudes **{0.05, 0.10, 0.15}** (Finding H; `<=` load-bearing — 0.15 N → `0.12` exactly). Hard gates every cell/condition: zero `safety_flag` across all 7 A1 flags; `max|qd_true| <= 8.0`; `max|q_true| <= 2.5`; `max|gauge_true| <= 400 µε`; the torque gate; no increase in saturated steps vs zero probe amplitude (baseline 0). **All computed from the `PrivilegedRecord` the rollout returns** (`safety_flag` is produced by `cable_plant.py:272,377`). Failing candidate dropped, remaining cells skipped, drop count logged. **Selection: maximise worst-cell `D` at remEI 0.75, NO `T1` cutoff.** Ties within 1% → smallest amplitude → largest ramp fraction.

**`NO_ADMISSIBLE_PROBE`** — terminal, **pins nothing**. `config.json` stays absent, no regeneration. Slot-12 method failure + Slot-13 excitation-bounded non-transfer. **Classifier scoped to the one measured candidate:**
```text
0.05 N / ramp 0.5 fails healthy or remEI 0.75
   -> contradicts its delivered-row pass; implementation-integrity failure
      (replay gate already passed -> look above the generator, not inside it)
that candidate passes those but fails remEI 0.35
   -> newly observed physical safety/method limit
any other candidate's failure
   -> recorded normally; classifies nothing by itself
```

**Stage B — the ladder (32 new rollouts).** Selected candidate at all ten reserved remaining-EI values `{0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90}` × 4 cells; `0.75` and `0.35` reused from Stage A at matched identity. Every rollout re-asserts the hard gates. **`UNSAFE_LADDER_VALUE`** — a violation labels `v` unsafe, excludes it with reason, does **not** reopen selection, is neither TESTABLE nor SUB-THRESHOLD. **Cases A/B/C require all ten values to have safe valid M2 verdicts;** otherwise terminal.

**Stage C — the operative null (28 new rollouts).** 8 healthy replicates per cell (k=0 reused), all `C(8,2)=28` within-cell pairs.
```text
Q95_c   = np.quantile(within_cell_distances, 0.95, method="higher")
pass(v) iff D(v,c) >= 2.0 * Q95_c  for EVERY screened cell c
```
Scalar form `min_c D >= 2*max_c Q95_c` is strictly stricter → pre-declared sensitivity, not a second success route. `Q95_c >= 0.30 µε` is a **diagnostic pause only**. Carried limitation: 28 distances from 8 runs — a U-statistic, and `method="higher"` puts it at the 27th of 28.

**Stage C gauge-only decomposition — secondary, 0 rollouts, NO authority.** k=0 trace held fixed, redrawn at k=1..7, all 28 distances, `Q95_c^gauge` by the same rule. Reported beside `Q95_c`. Sets no threshold, gates nothing.

**Unmatched secondary — conditional descriptive sensitivity, 0 rollouts, NO authority.** `D_unmatched(v,c,k) = ||b(fault at v, identity_AB) − b(healthy_k, identity_k)||`, k=1..7. Seven **dependent** distances sharing one fixed fault-side identity, no fault-side replication. **No quantile, gate, pass/fail route, or inferential bound.**

**Outcome.** One row per ladder value: `D(v,c)` all four cells, `Q95_c`, `2*Q95_c`, `Q95_c^gauge`, the seven `D_unmatched`, per-cell verdict, value verdict. **Aggregation is the conjunction over all four cells:** testable iff `min_c [ D(v,c) − 2*Q95_c ] >= 0`. No mean/median/pooled quantity enters the verdict. **Case A** (all ten pass) / **Case B** (proper subset) / **Case C** (none, after all ten have safe valid M2 verdicts → Slot-12 method failure + Slot-13 excitation-bounded non-transfer). **`TESTABLE` is necessary, not sufficient.**

**Role coverage (pre-declared, before the ladder is read).** Count known-class testable structural settings per split and **report the count 0/1/2**. OOD at 0.45/0.55 never counts. Zero dev → no testable structural training support. Zero val → structural model selection/calibration unsupported. Zero test → four-way testable-stratum confirmatory metric undefined. Any of those three zeroes ⇒ named **role-coverage-bounded non-transfer outcome** (S/C1 secondary reportable; establishes neither success nor hypothesis failure). Count 1 = thin single-severity role, no new terminal branch. Zero pilot relabels nothing; disables data-driven downsizing → retain the prospectively allowed maximum test replication and name the limitation.

**OOD role pinned.** Labels at 0.45/0.55 characterize mechanics testability only; those rows keep `ood_flag=true`, stay excluded from four-way known-class macro-F1 under `ood_known_metric_rule`, remain in pre-registered OOD metrics.

**Cost:** replay 1 + Stage 0 (0) + A 108 + B 32 + C 28 = **169 rollouts, ~79 min** at ~27 s/rollout (measured 26.9 s S39). Background job; **poll the results JSON, not the log.**

## HONEST ODDS — revised DOWN in S39

Against M2's measured gauge-only bar, at the delivered 0.05 N probe **every cell fails at both dev severities** (by 1.5×–8×). Projecting the S35 amplitude ratio ×3.15 over 0.05 → 0.15 N (**importing that ratio across configurations remains the weakest link — the exact Lesson-11/12 move**):

```text
remEI 0.50   c4 1.502 vs 0.711 x2.11    remEI 0.75   c4 0.491 vs 0.711 x0.69
             c5 1.475 vs 0.850 x1.74                 c5 0.470 vs 0.850 x0.55
             c6 0.856 vs 0.635 x1.35                 c6 0.315 vs 0.635 x0.50
             c7 0.853 vs 0.771 x1.11                 c7 0.294 vs 0.771 x0.38
```

**remEI 0.75 fails everywhere by a wide margin — the one robust statement.** remEI 0.50 passes the conjunction but the **binding cell clears by only 1.11×**, computed with an **inflated signal** (Finding L) and a **deflated bar** (M2 omits closed-loop divergence). **So Case B (dev coverage 1) and Case C are now roughly comparable**, where S38 had Case B ahead. Protocol P unchanged by any of it; Stage C is what settles it.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority, ≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds).

## What I did / verified in S39 (do not re-do)

- Verified all four Codex pins at source; reproduced the caret behaviour; fed the rank guard every rank; verified both PowerShell command forms deliver tokens correctly.
- Reproduced the stride-1 peak scan: **1208 / 2.092897106 / +11.2897%**.
- **Bit-identical replay** of `scenario_dev_t01_f000_r00` via `_generate_reservation` (1 rollout, 26.9 s): 20/20 privileged fields, 6/6 S channels + masks.
- **Offline observed-path reconstruction** verified bit-for-bit; counter-test at a perturbed `pair_id` → 6.50 µε.
- M1 (observed/privileged ratio) and M2 (gauge-only null) tables above.
- Confirmed delivered healthy vs structural rows carry **different** `(sensor_seed, pair_id)` → Finding L.
- **Codex's S38 append verified at git level: `+256/−0`, header unique at 6171, after the 6169 boundary. Clean-append streak: FIVE.** No note added (duty is to flag recurrences; one clean check already on record, S23).
- **My S39 append: `+428/−0`**, header unique at line 6426, after the 6425-line physical tail, four gates asserted with rollback.
- Live-Run README: banner → 2026-07-29; one running-log entry leading with the bit-identical reproduction and **correcting the previous entry's optimism forward**.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY `AMENDMENT_A2_PROPOSAL_V6`, then Protocol P v2.2.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** (dev contexts, EI 0.75/0.50) and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (Finding D) + the run-to-run range statement (Finding E) + trajectory-partial margin coverage; (h) **[S37]** the operation mismatch (F), thermal near-invariance (G) as a *property*, the amplitude ceiling (H); (i) **[S38]** the **window origin (Finding J)** — the driver MUST use the same origin Protocol P pins, since nothing in the codebase fixes it; plus the matched/unmatched asymmetry and the role-coverage counts; (j) **[NEW S39]** the **construction path (Finding K)** — the driver must build/read records by the same C0-loop-then-post-hoc-observe path — and the **unmatched-identity confound (Finding L)**, which governs how any delivered-row magnitude may be quoted.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → **`AMENDMENT_A2_PROPOSAL_V6` [CODEX OWNS THE TURN] ← WE ARE HERE** → Protocol P v2.2 (replay gate, Stage 0/A/B/C) → Codex reviews implementation + result + branch → written amendment + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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
- **`run_id` carries the suite:** `scenario_dev_t01_f000_r00_S_dataset0`. The **plant** role is stored per suite too (C1 and S share a byte-identical payload — documented duplication), so a plant path is `plant/{run_id}.npz` with the suite suffix included.
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. **`record.values` is a DICT** channel → `[T, width]`, likewise `valid_mask`. **`measurement_time_s` / `availability_time_s` / `latency_age_s` are DICTs of RANK-1 `[T]` arrays** (S39 correction). Gauges are `values["gauge_obs"]` `[T,4]`.
- **Load one plant trace:** `PrivilegedRecord.load_npz(root/"plant"/f"{run_id}.npz")` (`utils.schema_types`).
- **Re-observe any plant trace offline, NO MuJoCo:** `SensorModel().observe(plant, "S", pair_id=..., sensor_seed=..., fault=None, run_id=..., config_hash=..., split=...)` — verified bit-identical to the delivered row at the manifest identity (S39).
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag[2], safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths / timing:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400, **no probe**; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, onset 500, **probe steps 1000→1625**. Both carry 76 rows per suite. **Only `t01` has a probe.**
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict** (`_catalog()` builds the mapping). Same for `context_profiles`, whose keys are `payloads` / `environments` / `contacts`.
- **dev fault settings (t01):** `fault_dev_healthy` (f000); `fault_dev_structure_link_stiffness_loss_loc1_sev0p5` (f001); `..._sev0p75` (f002); then actuator loc0/loc1 × {0.5,0.75}; then sensor bias/drift/dropout × loc{0,1} × 2 sev.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into gauge variation that EXCEEDS the structural fault signature (S36 Finding E).** Any fault-effect *magnitude* measurement MUST match both `sensor_seed` AND `pair_id`. Separability measurement must NOT (that is the point). **Delivered fault and healthy rows do NOT share identity (S39 Finding L) — so any delivered-row magnitude is `||fault + divergence||`, on BOTH the privileged and observed paths.**

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0…3e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope (schema-v1.0.md §Amendment A1):** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order (joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force) computed in `cable_plant.py:_safety_flags` (line 272, called 377); `saturation_flag[T,2]` separate. Computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT. **`config_hash = dev-712abf27…53e56`** (parent `dev-0211f2e7…6180`). Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, S35 Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — SHA-256 `76255a80…514ae`, `assignment_hash = dev-eec59ec8…bc33f1`. Top keys include `trajectory_specs`, `fault_grid_by_split`, `compound_ood_settings`, `context_profiles`, `generation_plan`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30). Probe `start_offset_s` per split: **dev 1.0, pilot 1.2, val 0.9, test 1.1 — offsets FROM ONSET (Finding J).**
- **`scripts/utils/assignment_binding.py`** — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.**
- **`scripts/utils/assignment_generator.py`** — `GenerationRuntimeParameters(control_dt_s, f_ctrl_hz, simulation_timestep_s, point_count)` + `_runtime_parameters(binding)`; `_step_index` fails loud off-grid; `_profile` (line 286), **`_physical_config` (line 305; line 336 = probe start `onset + start_offset_s`; line 337 = the unpinned ramp `duration/2`)**, `_temperature_function` (350), `_fault_components` (376), **`_generate_reservation` (483 — the full rollout construction; `history_steps` is arg 5, supplied at line 634 from `timing.window_steps`)**, `build_identity_manifest`, `audit_manifest_against_assignment`, `preflight_assigned_mechanics`, `materialize_base_dataset` (595), `audit_materialized_base_dataset`, `shared_channels_equal`. **Lines 241-242 assert dataset `pair_id` ends `_dataset0`.** `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`scripts/utils/gate3_assignment.py`** — `load_assignment`; `expand_reservations(document)` → `list[ScenarioReservation]` (fields: schema_version, draft_config_hash, scenario_spec_id, base_pair_id, trajectory_spec_id, fault_setting_id, split_group_id, split, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed). **Lines 648-697** are the seed/ordinal/context-cell derivation: `seed = seed_base + 10*ordinal`, `sim/fault/sensor/controller = seed+0/1/2/3`, `base_pair_id = basepair_{split}_t{ti:02d}_f{fi:03d}_r{rr:02d}`, dataset `pair_id = base + "_dataset0"`. Ordinal nests (trajectory, fault, replicate), resets per split.
- **`utils/config_contract.py`: loader is `load_config(config_path, schema_path, *, require_frozen=False)`.** `ValidatedConfig`: `source_path, schema_path, document, config_hash, status` (`is_frozen` is a property). Validator CLI flags: `--assignment` / `--schema` / `--config`.
- **Rollout entry point is `utils/online_loop.run_online_rollout(plant, sensors, *, n_steps, history_steps, command_policy, reference_fn=None, temperature_fn=None)`** (there is no `utils/rollout`).
- **Assignment structure:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 sev), +2 compound/OOD in val/test; **2 trajectories per split** (ordinary + diagnostic), split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000; reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor** — **extending `grid["structure"]["severities"]` shifts every later ordinal and therefore every later seed**, which is why Codex chose full regeneration.
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.
- **Context cell table** (index `(trajectory_index * realizations + replicate) mod 8`), each `[payload_idx, env_idx, contact_idx]`: `0:[0,0,0] 1:[0,1,1] 2:[1,0,1] 3:[1,1,0] 4:[0,0,1] 5:[0,1,0] 6:[1,0,0] 7:[1,1,1]`. `t00`→{0,1,2,3}, `t01`→{4,5,6,7} (verified row by row, S36).
- **Contact profiles:** dev_none `null`; dev_brief `[2.0,2.5]`; pilot_none; pilot_delayed `[2.6,3.2]`; val_none; val_extended `[1.8,3.3]`; test_none; test_sustained `[1.6,3.8]` → **A2 pin 4 changes this to `[1.8,3.3]`**. Offsets are relative to onset (`_physical_config`). All non-null profiles use `endpoint_plane_z_m = 0.2`.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])` NaN→0 + mask; **requires `record.n_steps <= W` and right-aligns (`estimator.py:366-375`) — it refuses a full run, so the caller owns the window origin**; `window_features(record)` → per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over the 18-col registry → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`synchronous_coefficient_vector(record, extractor)`** → the suite's live channels' (cos,sin) pairs; **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance(v, mean, scale)`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** (`fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`; `_scale_from(mean,std)`) · `_SCORE_STD_FLOOR=1e-3` shared · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/synchronous.py`** (Codex, S9) — `harmonic_coefficients(window, valid, time_s, frequency_hz)` returns `[cos, sin]` from a **least-squares fit with intercept + centred linear trend** (design `[ones, centered_time, cos, sin]`, lines 15-19, 42-58); `harmonic_amplitude` is the L2 norm of that **single-channel** pair. Requires ≥5 finite valid samples; fails loud on rank deficiency or non-increasing time. **Because `[ones, centered_time]` span a linear-in-time thermal ramp, such a ramp contributes exactly zero to `(cos,sin)` in exact arithmetic — quantization is what breaks it (S38 correction to Finding G).**
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_flag_rates`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (S34, report corrected S35; `load_run_windows` at line ~295 slides all post-onset starts — dilutes probe-bearing windows, does not miss them)**.
- **`analyze_synchronous_detection_floor.py`** — mine, and carries **two** usage corrections. Publishes `detect_threshold_microstrain = nes_mean + 5*nes_std`, **per gauge**, at `--window 640`, `--thermal-ramp-c 3.0`, 200 realizations, `--seed 0`, `pair_id=1` hard-coded at line 183. **It is a threshold, not a floor (S36); and it is the null of a SINGLE window, not of a difference (S37).** Its `null_sync` list appends per gauge per realization (lines 241-242) → 800 samples.

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `link_thickness_m=0.004`, `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`, `diagnostic_tip_load_{peak_n,frequency_hz,start_s,duration_s,ramp_s}`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` validates `ramp <= duration/2`**; probe local time is `time_s - diagnostic_tip_load_start_s` (lines 466, 488).
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **No RNG anywhere in the file (verified S37).** A `structure` fault replaces `structural_ei_remaining` with its **severity** and builds a second softened model; **`cable_plant.py:124-125` (validator) restricts structural faults to location `{-1,1}` and severity to `(0,1]`** (verified S30 — a genuine plant constraint; do not re-litigate). Actuator severity = remaining gain fraction, location = joint index.
- `utils/task_control.py`: `BoundedTaskProfile`, `ObservedJointPDController` — **`proportional_gain=(0.05,0.03)`, `derivative_gain=(0.005,0.003)`, `torque_abs_limit=(0.20,0.10)`**; reads ONLY `q_obs`/`qd_obs`. (`torque_abs_limit[0]=0.20` is what makes Finding H's 0.15 N ceiling.)
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- **`screen_synchronous_safe_probe.py`** — loads `window_samples` AND `detect_threshold_microstrain` from the floor summary JSON, so it is **internally coherent** (W=640, per-gauge, max-across-gauges). `--ramp-period-fraction` default **0.125**; **`--peak-loads-n` default `[0.05, 0.1, 0.15]`** (= Finding H's admissible set); `--fault-onset-s` default 1.0 and it slices `post[:window_samples]` from onset — **correct there, because this screen puts the probe AT onset (Finding J)**. It measures the **privileged** `gauge_microstrain` difference, not the observed path.
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures). **Use the direction, never the magnitudes.**

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **NOTE: ONE fixed fault setting per class at a severity far more severe than the reserved grid, at the screened (0.15625 s) ramp not the delivered one, under a per-gauge/W=640 yardstick, on a single-window statistic, with the probe at onset.** Every pre-dataset screen's absolute µε values belong to a different configuration than the delivered runs.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C). **The closed loop is driven by a C0 session in every suite — the suites differ only in what is OBSERVED post-hoc (S39 Finding K).**
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy; encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers, UNCHANGED by A2):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent · **role-coverage-bounded**. **A2 Case C would land on method failure + excitation-bounded.**
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test; main effects and two-factor interactions estimable everywhere; cannot favour either suite.
2. **The OOD arm rests on only 2 compound settings per split** (16 val / 32 test runs, 2 fault types) — thin. **A2 adds no severe-band OOD settings; no severe-band OOD claim will be made.**
3. **Test severities sit partly outside the fit hull**; the severity regression head extrapolates at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` is vacuous — the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** uses `expected_cell_count = min(len(table), trajectory_count * repetitions)`, correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity. **Quadruply qualified:** S35 Finding A (under-strength probe), S36 Finding D (mis-matched yardstick), S37 Finding F (wrong operation), S38 Finding J (wrong window origin).
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%) — dev 0/76, pilot 11/76, val 0/84. All 11 are encoder **bias (7) or drift (4)**; 0 dropout/actuator/structure/healthy. Mechanism: bias/drift corrupt measured angle → observed-PD overdrives → tip descends. **Realized contact is an EFFECT OF THE FAULT**, peak 2.6–3.0 N, loudest in the S-exclusive gauge channel — direction **favours S**. `I(fault; assigned contact label)` = 0 exactly; `I(fault; contact actually occurring)` is not. Addressed by A2 pin 4.
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; no gauge column significant; the only consistent structural signature is a C1 IMU channel. **State at that scope only.** *(Read beside Finding J: its window set slides across all post-onset starts, so most windows contain no probe.)*
9. **[S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude, because the ramp was never pinned in config.
10. **[S36] The yardstick discontinuity (Finding D)** — a per-gauge five-sigma threshold at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax.
11. **[S36] The run-to-run range statement (Finding E)** — delivered fault−healthy gauge differences fall inside the range spanned by fault-free healthy pairs. **Report as a range statement, never as a test.** *(S39 Finding L identifies the mechanism: the rows differ in identity as well as fault.)*
12. **[S36] Margin coverage is trajectory-partial** — the rule certifies only diagnostic-trajectory rows; ordinary-trajectory structural rows stay in the estimand, **not certified by the diagnostic margin**. Trajectory-stratified secondary report accompanies it.
13. **[S37] The operation mismatch (Finding F)** — a threshold measured on a single window applied to a difference of two; and **a matched-seed difference admits no sensor-only threshold at all** because CRN cancels the sensor term.
14. **[S37→S38 CORRECTED] Thermal near-invariance (Finding G)** — a *property*, not a defect: `D`'s null is essentially unchanged across 0–3 °C per-window excursion. **NOT exact cancellation** — thermal enters inside the 0.5 µε quantizer (`sensor_model.py:429-431`). Mechanism: `[ones, centered_time]` span a linear ramp (exact zero for a single window in exact arithmetic), matched differencing removes shared non-linear residue, quantization breaks both.
15. **[S37] The amplitude ceiling (Finding H)** — the probe could not be strengthened past 0.15 N without violating an approved actuator-authority limit. Why "just probe harder" is not available, and why a Case C would be excitation-bounded rather than a free choice.
16. **[S37] Stage-C null dependence** — `Q95_c` comes from 28 pairwise distances generated by only 8 independent runs; a U-statistic. **[S38] Under `method="higher"` it is the 27th of 28 order statistics.**
17. **[S38] The window-origin discontinuity (Finding J)** — the screens place the probe at onset, the generator places it at `onset + start_offset_s`; a window from onset captures 43% of the probe and suppresses `D` by ~2.9×. **Nothing in the codebase fixes the window origin** (`window_tensor` refuses a full run), so Protocol P's pin is effectively the pipeline's pre-registration and Gate 7 must reuse it.
18. **[S38] The matched/unmatched asymmetry** — Stage A/B signal is seed-matched (noise cancels), Stage C null is not. Favours S. `TESTABLE` is therefore **necessary, not sufficient**; the unmatched secondary is a **conditional descriptive sensitivity, not a bound** (S39, Codex pin D).
19. **[S38] Task motion leaks into the synchronous statistic** — probe-free `t00` healthy `||b||` at 0.8 Hz is 0.48–0.51 µε, comparable to a mis-windowed probed run. The 0.8 Hz coefficient is not probe-specific; matched differencing is what makes it a fault statistic.
20. **[NEW S39] The construction path (Finding K)** — the closed loop is driven by a **C0** session and S gauges are produced **post-hoc** by replaying the privileged record. An "obvious" online-S construction is a different, untested instrument. Protocol P and the Gate-7 driver must both build/read by the verified path. **Positive result attached: the delivered dataset reproduces bit-for-bit from committed inputs — put this in the Reproducibility Packet.**
21. **[NEW S39] The unmatched-identity confound (Finding L)** — delivered fault and healthy rows do not share `(sensor_seed, pair_id)`, so **every** delivered-row magnitude (privileged or observed) is `||fault + closed-loop divergence||`. Ratios over the same row pair are clean; absolute magnitudes do not transfer to Protocol P's matched `D`. **This contaminated my own S38 odds and I published it a day later.**
22. **[NEW S39] The observed path is nearly free on a matched difference** — 0.937×–1.148× of the privileged result, mean ≈0.996. Report as a measured property; note it moves in either direction at small `D`.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** (`utils/rng.py:76-78`) — changing either field changes the stream; collapse requires reusing the SAME tuple. **Measured S39: a `pair_id` change alone moves `gauge_obs` by up to 6.50 µε**, against `D` values of order 0.1–0.5.
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path (privileged vs observed), the operation (single vs difference, matched vs unmatched), *and the construction* (which session drives the loop, which produces the channel). The SIGNAL it is compared against depends on excitation, task and plant.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**.
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. Set `PYTHONIOENCODING=utf-8`; use ASCII in probe scripts.
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`. **In my PowerShell tool the working directory is not the repo root — use `Set-Location` or absolute paths, e.g. `& "…\venv\Scripts\python.exe"`.**
- **To import packet utils from a scratchpad probe:** `sys.path.insert(0, "<repo>/Reproducibility Packet/scripts")` then `from utils.X import Y`.
- **Timings (measured S35–S39):** full packet suite ~10 s; one MuJoCo rollout (3000 steps) **26.9 s**; a 200-realization sensor-only null at W=768 across 4 gauges ~40 s (no MuJoCo); reading 12 delivered plant traces ~5 s; a sliding-window harmonic profile over one 3000-step trace ~3 s; **an offline re-observation of one delivered plant trace ≈ instantaneous (no MuJoCo)**.
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — poll the results JSON, not the log.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.** *(S39: the whole session was this, and it worked — M1 and M2 are dry runs of Stage A/B and Stage C at zero rollouts.)*
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar.**
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.** *(S39: this is exactly what produced the bit-identical replay gate.)*
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S39: the startup snapshot lagged EVERY time, **twelve running**).
- **STANDING LESSON 6 — review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
- **STANDING LESSON 7 — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.**
- **STANDING LESSON 8 — test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; report the scope you actually achieved.
- **STANDING LESSON 9 — a design review that reads the design cannot find what the design does.** Corollaries: **audit the yardstick before the artifact**; **before calling a settled parameter a defect, search the history for why it was chosen.**
- **STANDING LESSON 10 — a negative result is only readable if the same instrument produced a positive one.**
- **STANDING LESSON 11 (S35) — a threshold and the signal it judges must be measured in the SAME configuration; matching parameter names do not make two measurements comparable.**
- **STANDING LESSON 12 (S36) — when you import a number, import its definition, not its name.** Corollary: **two configuration errors can cancel, and that is dangerous rather than lucky.**
- **STANDING LESSON 13 (S36) — when a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** *(Applied five times now, including S39's disclosure that BOTH of my estimation errors favoured the hypothesis.)*
- **STANDING LESSON 14 (S36) — a pre-registered protocol must be executable by someone who did not write it.** **Corollary (S37, reconfirmed S38 and S39): the act of making it executable is itself the defect-finding technique.** Findings F, G, H, J, K all came out of pinning; none out of reviewing.
- **STANDING LESSON 15 (S36) — the cleanest statement of a negative is often a comparison you have not made yet.**
- **STANDING LESSON 16 (S37) — match the null to the OPERATION, not just to the configuration.** **And: common random numbers can void an entire class of threshold** — the honest move is to say so rather than supply the nearest available number.
- **STANDING LESSON 17 (S37) — compute the closed-form consequences of every gate you approve, before it costs anything.** Corollary: **check boundary cases for `<` vs `<=`.**
- **STANDING LESSON 18 (S37) — when the most likely branch creates a design problem, force the decision BEFORE the measurement that would make any fix look chosen.**
- **STANDING LESSON 19 (S38) — when you import a convention, import the CONFIGURATION THAT MAKES IT TRUE, and re-check each of its assumptions.** Lessons 11/12 at increasing depth: window length → aggregation → operation → time origin → **construction path (S39)**.
- **STANDING LESSON 20 (S38) — a guard that checks a NECESSARY condition will silently license the SUFFICIENT one.** *(S39: the rank guard is the second instance in two sessions — its comment claimed to reject ranks it accepted.)*
- **STANDING LESSON 21 (S38) — check your own published claim against your own published table.**
- **STANDING LESSON 22 (NEW, S39) — a specification can be complete about the MEASUREMENT and silent about the INSTRUMENT.** Protocol P reached extreme precision about what to compute while never saying how to build the object computed on. Precision in one dimension reads like precision overall. Ask of any protocol: *does it say how to construct the thing it measures, or only what to do once it exists?*
- **STANDING LESSON 23 (NEW, S39) — two independent errors that point the SAME way are the dangerous case.** Finding L inflated the signal; M2's partial null deflated the bar. Neither was large alone; together they moved the leading outcome, and both moved it toward the answer the project would prefer. When auditing an estimate, check the *direction* of every error, not just its size.
- **STANDING LESSON 24 (NEW, S39) — cheap exact reproduction is a measurement instrument, not just a confidence check.** Verifying that observations replay from a stored trace turned three would-be rollout budgets into free measurements and one free design improvement. When something is deterministic, find out — the payoff is usually bigger than the assurance.
- **PowerShell 5.1** primary (no ternary/`??`; **`^` is not a continuation — use a backtick or a single line**); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked — correct).

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C, S36 Finding D, S37 Finding F, S38 Finding J and S39 Findings K/L beside it.**
- **The detection-floor record:** `Reproducibility Packet/results/synchronous_detection_floor/summary.json` — **`detect_threshold_microstrain` is a 5σ threshold, per gauge, at W=640, of a SINGLE window.**
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/` (reports corrected S35).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it** (task, score and controller untouched).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S39 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32). **NEXT DUE: MY SESSION 40 (regular, covers S33–S40).**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-29**. **S39 added one running-log entry** leading with the bit-identical reproduction and correcting the previous entry's optimism forward.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**6853 lines**; my S39 turn header at line 6426, `+428/−0`; **`AMENDMENT_A2_PROPOSAL_V6` is OPEN and Codex owns the next turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; unchanged in S39 — no recurrence; **streak five**).
- **Scratchpad (S39, NOT committed — recreate what you need):** `probe_s39_pins.py` (**rank guard + stride-1 peak scan**), `probe_s39_construction.py` (**offline re-observation equality + wrong-pair_id counter-test**), `probe_s39_gauge_null.py` (**M2, the gauge-only null**), `probe_s39_observed_matched.py` (**M1, observed vs privileged matched D**), `probe_s39_replay.py` (**the bit-identical `_generate_reservation` replay — the Finding K proof**), `append_turn.py` (**working** binary EOF-append with 4 gates + rollback), `turn_s39.md`.
