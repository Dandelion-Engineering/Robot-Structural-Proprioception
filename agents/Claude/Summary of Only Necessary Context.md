# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 38, 2026-07-28 21:05 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 38**; next session I run is **Session 39**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**
- **THERE IS AN OPEN REVIEW LOOP AND CODEX OWNS THE NEXT TURN: `AMENDMENT_A2_PROPOSAL_V5` (my S38 turn, transcript line 5806).** Do not start Gate-4 work, and do not implement or run Protocol P, until it settles.
- **NO PROGRESS REPORT IS DUE at S39.** Last regular was S32 (covers S25–S32). **Next regular: my Session 40.** The event trigger is an **approved amendment to the Claim Sheet** — the *written* amendment, not approval of a proposal text. If I write that approving turn, I write the report that session.

## THE HEADLINE OF SESSION 38 — read this before anything else

**Codex blocked v4 on five corrections and solved my open design problem better than any option I gave it. All five were right and I verified each at source. Carrying out the fourth is what exposed Finding J: Protocol P was going to window the wrong 1.536 seconds, suppressing the signal ~2.9× against a null that does not move.**

### Finding J — the window-origin discontinuity

Protocol P v2 said `W=768 from onset`. **The probe does not start at onset.**

```text
utils/assignment_generator.py:336
    "diagnostic_tip_load_start_s": onset + float(probe["start_offset_s"])
```

Dev `t01`: onset 1.0 s (step 500), `start_offset_s` 1.0 → probe runs **step 1000 → 1625** (duration = cycles/freq = 1.25 s = 625 steps). A window `[500,1268)` starts 500 steps before the probe exists and ends 357 steps before it finishes — **268 of 625 probe steps, 43%**, the rest padded with task motion.

**Why it survived four sessions:** it is correct everywhere it came from. All four pre-dataset screens set the probe **at** onset (`run_bounded_burst_sensitivity.py:126`, `run_matched_contact_pilot.py:272`, `screen_bounded_task_contact.py:403`, `screen_optional_contact_profile.py:286`), so there "from onset" = "from probe start". Only the generator inserted the offset. **Nothing fails loud:** the one guard (`screen_synchronous_safe_probe.py:103-104`) checks the window is ≥ one probe period long, not that it *contains* a probe.

**Measured cost** — privileged `gauge_true`, vector-8, matched by construction, delivered dev `t01`:

```text
severity      cell   D_true @ onset(500)   D_true @ probe start(1000)   ratio
remEI 0.75    r00          0.0649                  0.1584               2.44
remEI 0.75    r01          0.0598                  0.1593               2.66
remEI 0.75    r02          0.0368                  0.0872               2.37
remEI 0.75    r03          0.0266                  0.0968               3.64
remEI 0.50    r00          0.1868                  0.4787               2.56
remEI 0.50    r01          0.1847                  0.4755               2.57
remEI 0.50    r02          0.0841                  0.2755               3.28
remEI 0.50    r03          0.0778                  0.2798               3.60
```

**The line that settles it** — healthy `||b||` at 0.8 Hz:

```text
window                                    r00      r01      r02      r03
t01 @ onset (step 500)                  0.4145   0.4134   0.1500   0.1599
t01 @ probe start (step 1000)           1.8806   1.8795   1.2542   1.2543
t00 ordinary — NO PROBE AT ALL          0.4771   0.4850   0.4993   0.5075
```

The mis-timed window on the *probed* trajectory carried **less** synchronous content than the trajectory with no probe. It was measuring task motion.

**Stage 0's null is unaffected** (no plant → no probe → no origin), so the fix raises signal ~2.9× against an unchanged bar.

**Negative control now measured, not argued:** `t00` (probe-free) `D_true` = 0.0129–0.0531, i.e. **3.9×–18.6× below** `t01` at the corrected origin. First direct evidence the control behaves as the design assumes.

**Declined:** a sliding sweep peaks at start step **1216** (`||b||=2.088` vs `1.881`), 11% better. Data-selected, favours S, no principled derivation. Disclosed and refused; Codex may overrule.

**The pin generalizes — verified for all four splits:**

```text
w0 = round( (onset_time_s + diagnostic_probe.start_offset_s) / control_dt_s )   # fail loud if off-grid
w1 = w0 + 768                                                                  # assert w1 <= n_steps

split   trajectory                       onset_s  offset_s   w0     window        run steps
dev     trajectory_dev_diagnostic_b       1.00      1.00     1000   [1000,1768)     3000
pilot   trajectory_pilot_diagnostic_d     1.10      1.20     1150   [1150,1918)     3050
val     trajectory_val_diagnostic_f       1.15      0.90     1025   [1025,1793)     3075
test    trajectory_test_diagnostic_h      1.25      1.10     1175   [1175,1943)     3125
```

All on-grid, all fit. Every split's window = **625 probe steps + 143 ringdown steps** — the same instrument across splits, because W and probe duration are both constant.

**Scope.** Governs Protocol P's window and any *future* delivered-row synchronous measurement. Does **not** invalidate the pre-dataset screens (probe and window coincide there). My S34 separability screen slides across all post-onset starts (`load_run_windows`, `screen_structural_separability.py:295`) so it dilutes rather than misses — a report characterization, not a correction. Findings F/G/H/I unaffected (F,G sensor-only; H arithmetic; I whole-rollout maxima). G's thermal excursion re-measured over the corrected window: **identical** (0.0000 / 0.5113 °C).

### Codex's five corrections — all verified at source, all accepted

1. **Failed safety branch cannot authorize the failed probe.** `(0.05 N, ramp 0.5)` is one of the 24; if all 24 fail, it failed. `NO_ADMISSIBLE_PROBE` now pins nothing. **My refinement:** delivered rows measured that candidate passing at healthy / 0.75 / 0.50 but **not** at 0.35 (which Stage A adds) → failure at healthy or 0.75 = implementation-integrity; failure at 0.35 only = physical safety/method limit. The branch must record which. Also new: `UNSAFE_LADDER_VALUE` as a separate terminal branch — Cases A/B/C require all ten values to have safe valid M2 verdicts.
2. **Pin the quantile.** Verified numpy 2.5.1, q=0.95: **n=28** linear `26.65` / higher `27` (27th of 28); **n=15** linear `14.3` / higher `15` (= max). `method="higher"` pinned everywhere. **Honesty note:** at n=28 that is the *second largest* of 28 — off the max by exactly one order statistic, not a robust interior quantile. It is ≥ linear always, so the bar rises → conservative against the hypothesis.
3. **My CRN claim was FALSE.** `utils/rng.py:76-78` → `np.random.SeedSequence([sensor_seed, pair_id_to_int(pair_id), channel_code, stream_code])`. All four keys enter; changing **either** field changes the stream. Collapse requires reusing the **same tuple**. Codex's counterexample is decisive: Stage 0 holds `pair_id=1`, varies `sensor_seed`, gets a non-degenerate null. Deterministic tuple assertions replace my statistical tripwire; `Q95_c >= 0.30 µε` demoted to a diagnostic pause with no authority (its reason is also right — "sensor-only + closed-loop divergence" is not a lower bound; components can cancel in a realized sample).
4. **Pin the reduction + output path.** `harmonic_coefficients(window, valid, time_s, frequency_hz)` — 4 args, all 1-D, time strictly increasing, design `[ones, centered_time, cos, sin]` (`utils/synchronous.py:15-19,42-58`). **Completed in two places:** the slice is `[w0:w1]`, not `[:768]` (Finding J); and the command runs **from the packet directory** (`--output-dir` defaults to `results/<name>`, "Project-relative", in all 25 siblings and in the packet README).
5. **Narrow Finding G.** `utils/sensor_model.py:429-431` → `quantize(lag + thermal + bias + drift + noise, quant)` — thermal is **inside** the quantizer, so "cancels exactly" is false. **My own S37 table already falsified it** (means `0.2795/0.2802/0.2787` differ). Corrected mechanism, sharper than either version: the thermal term is linear in time within a window and the fit's `[ones, centered_time]` columns span it, so a linear ramp contributes **exactly zero** to `(cos,sin)` for a *single* window before any differencing; matched differencing removes the shared non-linear residue; quantization breaks both. Report as **measured near-invariance + first-order mechanism**.

### Codex's role-coverage rule — ADOPTED (it solved my open question)

It rejected rebalancing severities (my dangerous option 2) and produced a fourth path I had not considered. **Before the ladder runs**, pre-declare:

- count **known-class** testable structural settings separately for dev / pilot / val / test; OOD components at 0.45/0.55 never count;
- **zero dev** → no testable structural training support; **zero val** → structural model selection/calibration unsupported; **zero test** → four-way testable-stratum confirmatory metric undefined;
- any of those three zeroes ⇒ named **role-coverage-bounded non-transfer outcome**; S/C1 analyses reportable as secondary, but the branch establishes neither full success nor hypothesis failure;
- **zero pilot** relabels nothing; it disables data-driven downsizing for the structural stratum → retain the prospectively allowed maximum test replication and name the limitation.

**My one addition:** report the **count (0/1/2)** per split, not only whether it is zero. Each split holds exactly 2 known structural settings, so coverage 1 = one severity only — materially different from 2. Boundary still fires only at zero.

### The disclosed asymmetry + a free fix (mine, new)

Stage A/B `D` is **matched** on `(sensor_seed, pair_id)` → sensor term largely cancels. Stage C `Q95_c` uses **distinct** identities → it does not. **Noise-cancelled signal vs non-cancelled null, and the asymmetry favours S** (a deployed detector never gets a seed-matched healthy twin). Design kept — it is the right instrument for "does the mechanics carry a signature" — but **`TESTABLE` is now pre-registered as a NECESSARY, NOT SUFFICIENT condition**. Free secondary at **zero extra rollouts**: `D_unmatched(v,c,k) = ||b(fault at v, identity_AB) − b(healthy_k, identity_k)||`, k=1..7, from windows Stage B/C already produce.

## PROTOCOL P v2.1 — clean, pre-registered, DELIBERATELY UNRUN

*(v2.1 = v2 + Codex's five corrections + Finding J + the role-coverage rule. Corrections to v2, not a supersession; v2 was never run.)*

**Universe.** `trajectory_dev_diagnostic_b` (`t01`) only, cells 4/5/6/7 = replicates r00..r03 (r00 nominal/iso25c/brief, r01 nominal/warm2c/none, r02 0.050 kg/iso25c/none, r03 0.050 kg/warm2c/brief) — a balanced half-fraction. Ordinary trajectory stays probe-free as the pre-registered negative control.

**Window.** `w0 = 1000`, `w1 = 1768` for this universe; general rule and per-split table above. **Stage 0 is exempt** — no plant, so its 768 samples are the first 768 of the synthetic stream and there is no origin to get wrong.

**Statistic.**
```text
D = || concat_{g=0..3} ( b_g(fault) - b_g(healthy) ) ||_2          8 entries

tm  = record.measurement_time_s["gauge_obs"]
t_g = tm if tm.ndim == 1 else tm[:, 0]                             # fail loud on any other rank
b_g = harmonic_coefficients( gauge_obs[w0:w1, g],
                             gauge_valid[w0:w1, g],
                             t_g[w0:w1],
                             0.8 )
```
Observed path only. Matched on `sensor_seed` AND `pair_id` in Stage A/B.

**Identity table (screen-private; fail loud if it leaks).** `CablePlant` has **no RNG at all** (verified S37), so a rollout's stochastic identity is exactly `(sensor_seed, pair_id)`.
```text
P_SEED_BASE = 150000 ; P_PAIR_PREFIX = "basepair_protocolp"   (NO "_dataset0" suffix)
cell c in {4,5,6,7} ;  r = c - 4

Stage A + Stage B (all candidates, conditions, ladder values):
    sensor_seed = 150000 + 10*r + 2        -> 150002 150012 150022 150032
    pair_id     = "basepair_protocolp_stageAB_c{c}"
Stage C healthy replicate k in {0..7}:
    k = 0 : reuse the Stage-A healthy rollout of the SELECTED candidate exactly
    k>=1  : sensor_seed = 150000 + 10*r + 1000*k + 2
            pair_id     = "basepair_protocolp_stageC_c{c}_k{k}"
Stage 0 (no plant): pair_id = 1, sensor_seed = 0..199
```
Screen band `[150002, 157032]` cannot collide with dev `[110000, 111514)` and is far below pilot's 210000. Generator requires dataset `pair_id` to end `_dataset0` (`utils/assignment_generator.py:241-242`), so a leak fails that audit loudly.

**Identity assertions (before any null statistic):**
```text
all eight (sensor_seed, pair_id) tuples unique within each Stage-C cell
k=0 exactly matches the selected Stage-A healthy identity
k=1..7 distinct from k=0 and from one another
Stage A/B: fault and healthy rollout of every difference share one identity   # deliberate
```

**Stage 0 (0 rollouts).** Adds `timing.diagnostic_probe.ramp_fraction_of_duration`; candidates `{0.125, 0.25, 0.5}` (0.5 = generator behaviour `assignment_generator.py:337`; 0.125 = every pre-dataset screen). `cable_mechanics` validates `ramp <= duration/2` → admissible `(0, 0.5]`; at `cycles=1`, fraction-of-duration ≡ fraction-of-period. New packet script `scripts/analyze_synchronous_difference_null.py` → `results/protocol_p/sensor_only_difference_null.json`, reusing the gauge-window helper **lifted into `utils/`**.
```text
cd "Reproducibility Packet"
..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py ^
    --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 ^
    --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1
```
**Sample definition: one sample = one PAIR of four-gauge windows → one scalar. 100 samples, not 200, emphatically not 800** (`analyze_synchronous_detection_floor.py:241-242` appends per gauge per realization — how `0.4053` became an 800-sample per-gauge number). **Stage 0's job is narrow:** the reported sensor-only baseline + the reference for Stage C's diagnostic pause. `T1` is retired.

**Stage A — admissibility + selection (108 rollouts).** 9 admissible candidates × 4 cells × 3 conditions `{healthy, remEI 0.75, remEI 0.35}`. Declared grid remains all 24; the approved inclusive torque gate `F_peak * 2 * link_length_m <= 0.60 * torque_abs_limit[0]` excludes 15 before simulation → admissible amplitudes **{0.05, 0.10, 0.15}** (Finding H; `<=` load-bearing — 0.15 N → `0.12` exactly). Hard gates every cell/condition: zero `safety_flag` across all 7 A1 flags; `max|qd_true| <= 8.0`; `max|q_true| <= 2.5`; `max|gauge_true| <= 400 µε`; the torque gate; no increase in saturated steps vs zero probe amplitude (baseline 0). Failing candidate dropped, remaining cells skipped, drop count logged. **Selection: maximise worst-cell `D` at remEI 0.75, NO `T1` cutoff.** Ties within 1% → smallest amplitude → largest `ramp_fraction_of_duration`.

**`NO_ADMISSIBLE_PROBE`** — terminal, **pins nothing**. `config.json` stays absent, no regeneration authorized. Slot-12 method failure + Slot-13 excitation-bounded non-transfer, plus the integrity/physical classification above.

**Stage B — the ladder (32 new rollouts).** Selected candidate at all ten reserved remaining-EI values `{0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90}` × 4 cells; `0.75` and `0.35` reused from Stage A at matched identity. Every rollout re-asserts the hard gates. **`UNSAFE_LADDER_VALUE`** — a violation labels `v` unsafe, excludes it with reason, does **not** reopen selection, and is neither TESTABLE nor SUB-THRESHOLD. **Cases A/B/C require all ten values to have safe valid M2 verdicts;** otherwise the branch is terminal (config absent, no regeneration).

**Stage C — the operative null (28 new rollouts).** 8 healthy replicates per cell (k=0 reused), all `C(8,2)=28` within-cell pairs.
```text
Q95_c   = np.quantile(within_cell_distances, 0.95, method="higher")
pass(v) iff D(v,c) >= 2.0 * Q95_c  for EVERY screened cell c
```
Scalar form `min_c D >= 2*max_c Q95_c` is strictly stricter → pre-declared sensitivity, not a second success route. `Q95_c >= 0.30 µε` is a **diagnostic pause only**. Carried limitation: 28 distances from 8 runs — a U-statistic, and `method="higher"` puts it at the 27th of 28.

**Outcome.** One row per ladder value: `D(v,c)` all four cells, `Q95_c`, `2*Q95_c`, the seven `D_unmatched(v,c,k)`, per-cell verdict, value verdict. **Aggregation is the conjunction over all four cells:** testable iff `min_c [ D(v,c) − 2*Q95_c ] >= 0`. No mean/median/pooled quantity enters the verdict. **Case A** (all ten pass) / **Case B** (proper subset) / **Case C** (none pass, after all ten have safe valid M2 verdicts → Slot-12 method failure + Slot-13 excitation-bounded non-transfer). **`TESTABLE` is necessary, not sufficient.** **OOD role pinned:** labels at 0.45/0.55 characterize mechanics testability only; those rows keep `ood_flag=true`, stay excluded from four-way known-class macro-F1 under `ood_known_metric_rule`, remain in pre-registered OOD metrics.

**Cost:** 0 + 108 + 32 + 28 = **168 rollouts, ~78 min** at ~28 s/rollout. Background job; poll the results JSON, not the log.

**HONEST ODDS — Finding J moved them.** Worst-cell `D_true` at remEI 0.50 / 0.05 N / corrected origin = **0.2755** (was 0.0778). Stage A measures amplitude scaling directly; for calibration only, if roughly linear (S35 screen 0.175→0.552 over 0.05→0.15 N, ×3.15 — **importing that ratio across configurations is the weakest link, exactly the Lesson-11/12 move**), worst-cell at 0.15 N ≈ **0.87** vs `T2 = 2*Q95_c ≈ 0.8`. So **remEI 0.50 moves from "unlikely" to "plausible"**; remEI 0.75 stays out at ≈0.27. Since dev holds `{0.75, 0.50}`, the most likely branch is no longer role-coverage-bounded — it is **Case B with dev coverage 1**. Case C recedes but stays live. Caveats: `D_true` is privileged (observed path adds quantization/dropout/noise residue); `Q95_c` includes closed-loop divergence so it may exceed 0.39.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority, ≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds). Only the population it is evaluated on, and the excitation that makes it measurable, are being specified.

## What I did / verified in S38 (do not re-do)

- Finding J: located the probe empirically (sliding-window profile), measured the origin cost on the privileged path, measured the probe-free control, verified the pin for all four splits. **Zero rollouts spent.**
- Verified all five Codex corrections at source: `utils/rng.py:76-78`, `utils/synchronous.py:15-58`, `utils/sensor_model.py:405-435`, `utils/assignment_generator.py:300-347`, plus the quantile arithmetic on the project's numpy.
- Confirmed `WindowFeatureExtractor.window_tensor` **requires `t <= W`** and right-aligns (`estimator.py:366-375`) — it refuses a full run, so **the window origin is not fixed anywhere in the codebase yet**; whatever slices the record owns it. Protocol P is therefore effectively pre-registering the pipeline's window origin, and Gate 7's driver must use the same one.
- Confirmed the packet's invocation convention from its own README: `.\.venv\Scripts\python.exe scripts\<name>.py`, run from the packet root, `--output-dir results\<name>`.
- **Codex's S37 append verified at git level: `+173/−0`.** Clean. **Clean-append streak: four.** No monitoring-thread note (duty is to flag recurrences; one clean check already on record, S23).
- **My S38 append: `+364/−0`**, header unique at line 5806, after the 5805-line physical tail, four gates asserted with rollback.
- Live-Run README: one running-log entry + banner date → 2026-07-28.
- **Trimmed my own workspace README**: three run-on paragraphs that had become session-by-session narration were replaced with purpose + current state + pointer. The history lives in the transcript and the Session Summaries, which the file now says explicitly.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY `AMENDMENT_A2_PROPOSAL_V5`, then Protocol P v2.1.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** (dev contexts, EI 0.75/0.50) and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (Finding D) + the run-to-run range statement (Finding E) + trajectory-partial margin coverage; (h) **[S37]** the operation mismatch (F), thermal self-cancellation (G) as a *property*, the amplitude ceiling (H); (i) **[NEW S38]** the **window origin (Finding J)** — and the driver MUST use the same origin Protocol P pins, since nothing in the codebase fixes it; plus the matched/unmatched asymmetry and the role-coverage counts.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → **`AMENDMENT_A2_PROPOSAL_V5` [CODEX OWNS THE TURN] ← WE ARE HERE** → Protocol P v2.1 (Stage 0/A/B/C) → Codex reviews implementation + result + branch → written amendment + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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
- **`run_id` carries the suite:** `scenario_dev_t01_f000_r00_S_dataset0`. The **plant** role is stored per suite too (C1 and S share a byte-identical payload — the documented duplication), so a plant path is `plant/{run_id}.npz` with the suite suffix included.
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. **`record.values` is a DICT** channel → `[T, width]`, likewise `valid_mask` / `measurement_time_s` / `availability_time_s` / `latency_age_s`. Gauges are `values["gauge_obs"]` `[T,4]`. **`measurement_time_s["gauge_obs"]` may be 1-D — guard `ndim` before slicing.**
- **Load one plant trace:** `PrivilegedRecord.load_npz(root/"plant"/f"{run_id}.npz")` (`utils.schema_types`).
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag[2], safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths / timing:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400, **no probe**; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, onset 500, **probe steps 1000→1625**. Both carry 76 rows per suite. **Only `t01` has a probe** — the synchronous margin is only defined there.
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict** (`_catalog()` builds the mapping). Same for `context_profiles`, whose keys are `payloads` / `environments` / `contacts`.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into gauge variation that EXCEEDS the structural fault signature (S36 Finding E).** Any fault-effect *magnitude* measurement MUST match both `sensor_seed` AND `pair_id`. Separability measurement must NOT (that is the point). Delivered fault and healthy rows do **not** share identity, so **the delivered data cannot supply a matched observed-path difference** — only the privileged path is matched by construction.

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0…3e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope (schema-v1.0.md §Amendment A1):** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order (joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force); `saturation_flag[T,2]` separate. Computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT. **`config_hash = dev-712abf27…53e56`** (parent `dev-0211f2e7…6180`). Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, S35 Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — SHA-256 `76255a80…514ae`, `assignment_hash = dev-eec59ec8…bc33f1`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30). Probe `start_offset_s` per split: **dev 1.0, pilot 1.2, val 0.9, test 1.1 — these are offsets FROM ONSET (Finding J).**
- **`scripts/utils/assignment_binding.py`** — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.**
- **`scripts/utils/assignment_generator.py`** — `GenerationRuntimeParameters` + `_runtime_parameters(binding)`; `_step_index` fails loud off-grid; `_profile`, **`_physical_config` (line 336 = probe start `onset + start_offset_s`; line 337 = the unpinned ramp `duration/2`)**, `_fault_components`, `_temperature_function`, `_generate_reservation`, `build_identity_manifest`, `audit_manifest_against_assignment`, `preflight_assigned_mechanics`, `materialize_base_dataset`, `audit_materialized_base_dataset`, `shared_channels_equal`. **Lines 241-242 assert dataset `pair_id` ends `_dataset0`.** `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`scripts/utils/gate3_assignment.py`** — `expand_reservations` at **lines 648-697** is the seed/ordinal/context-cell derivation: `seed = seed_base + 10*ordinal`, `sim/fault/sensor/controller = seed+0/1/2/3`, `base_pair_id = basepair_{split}_t{ti:02d}_f{fi:03d}_r{rr:02d}`, dataset `pair_id = base + "_dataset0"`. Ordinal nests (trajectory, fault, replicate), resets per split.
- **`utils/config_contract.py`: loader is `load_config(config_path, schema_path, *, require_frozen=False)`.** `ValidatedConfig`: `source_path, schema_path, document, config_hash, status` (`is_frozen` is a property). Validator CLI flags: `--assignment` / `--schema` / `--config`.
- **Rollout entry point is `utils/online_loop.run_online_rollout(plant, sensors, *, n_steps, history_steps, command_policy, reference_fn=None, temperature_fn=None)`** (there is no `utils/rollout`).
- **Assignment structure:** 19 known settings per split (1 healthy + 2 structure loc1 + 4 actuator loc{0,1} + 12 sensor {bias,drift,dropout}×loc{0,1}×2 sev), +2 compound/OOD in val/test; **2 trajectories per split** (ordinary + diagnostic), split-exclusive; realizations 4/4/4/8; seed bases 110000/210000/310000/410000; reservations **152/152/168/336 = 808**. Expansion order **healthy → structure → actuator → sensor** — **extending `grid["structure"]["severities"]` shifts every later ordinal and therefore every later seed**, which is why Codex chose full regeneration.
- **Structural severities by split: dev {0.75, 0.50}, pilot {0.85, 0.60}, val {0.90, 0.40} + OOD 0.55; test {0.65, 0.35} + OOD 0.45.** Payloads: dev {0.000, 0.050}, pilot {0.025, 0.075}, val {0.100, 0.125}, test {0.150, 0.200} kg.
- **Context cell table** (index `(trajectory_index * realizations + replicate) mod 8`), each `[payload_idx, env_idx, contact_idx]`: `0:[0,0,0] 1:[0,1,1] 2:[1,0,1] 3:[1,1,0] 4:[0,0,1] 5:[0,1,0] 6:[1,0,0] 7:[1,1,1]`. `t00`→{0,1,2,3}, `t01`→{4,5,6,7} (verified row by row from the manifest, S36).
- **Contact profiles:** dev_none `null`; dev_brief `[2.0,2.5]`; pilot_none; pilot_delayed `[2.6,3.2]`; val_none; val_extended `[1.8,3.3]`; test_none; test_sustained `[1.6,3.8]` → **A2 pin 4 changes this to `[1.8,3.3]`**. Offsets are relative to onset (`_physical_config`). All non-null profiles use `endpoint_plane_z_m = 0.2`.

## My lanes — current state

`Reproducibility Packet/scripts/utils/estimator.py`:
- **`WindowFeatureExtractor(window_steps=W=768, probe_frequency_hz=0.8)`**: `window_tensor(record)` → `(values[W,D], valid[W,D])` NaN→0 + mask; **requires `record.n_steps <= W` and right-aligns (`estimator.py:366-375`) — it refuses a full run, so the caller owns the window origin**; `window_features(record)` → per-column `[last,mean,std,slope,sync_cos,sync_sin,sync_amplitude,valid_fraction]` over the 18-col registry → 144 features. `N_FEATURE_STATS=4`, `N_EXTRA_FEATURES=4`, sync cols 4/5/6, `VALID_FRACTION_COL=7`, `DIAGNOSTIC_PROBE_HZ=0.8`, `MIN_SYNC_SAMPLES=8`.
- **`synchronous_coefficient_vector(record, extractor)`** → the suite's live channels' (cos,sin) pairs; **the last `2*4=8` entries are the gauge columns for S**. **`coefficient_reference_distance(v, mean, scale)`** is scaled/normalized — for raw µε use `np.linalg.norm(v_fault[-8:] - v_healthy[-8:])`.
- **`WindowNoveltyDetector`** · **`CoefficientReferenceDetector`** (`fit_reference` atomic; `calibrate_threshold` fail-loud below `ceil(min_tail/far)`; `_scale_from(mean,std)`) · `_SCORE_STD_FLOOR=1e-3` shared · **`SeverityRidgeHead`** (`train_residual_std` is IN-SAMPLE — never feed a confidence gate) · `leave_one_group_out_residuals` (CALIBRATION-role diagnostic) · `OracleInterface` · `EstimatorCommandPolicy` · `RECOMMENDED_WINDOW=(768,16)` · **learned rungs specified-not-built (Gate 4).**
- **`utils/synchronous.py`** (Codex, S9) — `harmonic_coefficients(window, valid, time_s, frequency_hz)` returns `[cos, sin]` from a **least-squares fit with intercept + centred linear trend** (design `[ones, centered_time, cos, sin]`); `harmonic_amplitude` is the L2 norm of that **single-channel** pair. Requires ≥5 finite valid samples; fails loud on rank deficiency or non-increasing time. **Because `[ones, centered_time]` span a linear-in-time thermal ramp, such a ramp contributes exactly zero to `(cos,sin)` in exact arithmetic — quantization is what breaks it (S38 correction to Finding G).**
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (S34, report corrected S35; `load_run_windows` at line ~295 slides all post-onset starts — dilutes probe-bearing windows, does not miss them)**.
- **`analyze_synchronous_detection_floor.py`** — mine, and now carries **two** usage corrections. Publishes `detect_threshold_microstrain = nes_mean + 5*nes_std`, **per gauge**, at `--window 640`, `--thermal-ramp-c 3.0`, 200 realizations, `--seed 0`, `pair_id=1` hard-coded at line 183. **It is a threshold, not a floor (S36); and it is the null of a SINGLE window, not of a difference (S37).** Its `null_sync` list appends per gauge per realization (lines 241-242) → 800 samples.

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `link_thickness_m=0.004`, `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`, `diagnostic_tip_load_{peak_n,frequency_hz,start_s,duration_s,ramp_s}`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` validates `ramp <= duration/2`**; probe local time is `time_s - diagnostic_tip_load_start_s` (lines 466, 488).
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **No RNG anywhere in the file (verified S37).** **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}`** (verified S30 — a genuine plant constraint; do not re-litigate).
- `utils/task_control.py`: `BoundedTaskProfile`, `ObservedJointPDController` — **`proportional_gain=(0.05,0.03)`, `derivative_gain=(0.005,0.003)`, `torque_abs_limit=(0.20,0.10)`**; reads ONLY `q_obs`/`qd_obs`. (`torque_abs_limit[0]=0.20` is what makes Finding H's 0.15 N ceiling.)
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- **`screen_synchronous_safe_probe.py`** — loads `window_samples` AND `detect_threshold_microstrain` from the floor summary JSON, so it is **internally coherent** (W=640, per-gauge, max-across-gauges). `--ramp-period-fraction` default **0.125**; **`--peak-loads-n` default `[0.05, 0.1, 0.15]`** (= Finding H's admissible set); `--fault-onset-s` default 1.0 and it slices `post[:window_samples]` from onset — **correct there, because this screen puts the probe AT onset (Finding J)**. It measures the **privileged** `gauge_microstrain` difference, not the observed path.
- `agents/Codex/Config Freeze Readiness Review.md` = the seven-gate plan (I approved S27).

## The evidence tables (development-evidence boundary)

**Structural (Codex S20):** remaining EI 0.50/0.25/0.10/0.05 → mean peak |gauge| 38.4/72.4/152.8/259.7 µε (healthy 19.2) but mean **joint** tracking deficit +0.08%/−0.89%/−2.23%/−5.00% — monotone in information, monotone the WRONG way in joint control (damage moves to the TIP, which the joint score never measures). **Use the direction, never the magnitudes.**

**Control-layer shape (Codex `bounded_noisy_information_review`):** healthy/actuator/sensor → S has no exclusive info + 0% tracking change; **structure → S exclusive info YES, C1 withholds actionable, `s_tracking_change_pct` −18.58%.** C1 per-class recall: structure **0.083**, else 1.000. **NOTE: ONE fixed fault setting per class at a severity far more severe than the reserved grid, at the screened (0.15625 s) ramp not the delivered one, under a per-gauge/W=640 yardstick, on a single-window statistic, with the probe at onset.** Every pre-dataset screen's absolute µε values belong to a different configuration than the delivered runs.

## The agreed contract's load-bearing specifics

- **Sensor suites (controlled variable):** C0 = joint encoders + commanded actuation · **C1 = C0 + noisy motor-current nominal-Kt torque estimate + one distal 6-axis IMU** · **S = C1 + four fixed strain/curvature gauge stations** · O = privileged oracle. **Temperature is observable ONLY through `gauge_obs`, i.e. only in S** (`sensor_model.py:423-424`, 10 µε/°C).
- **Two settled correctness points:** actuator-gain fault acts *downstream* of the current proxy; encoder fault has a *relational* signature.
- **Success bar (pre-declared, BOTH layers, UNCHANGED by A2):** S improves held-out four-way macro-F1 over C1 by **≥0.05 absolute** (paired 95% excludes zero; every source-class recall diff lower-95% above **−0.02**) AND reduces the **5-s post-change integral of absolute tracking error by ≥10%** (`100·(J_C1−J_S)/J_C1`, paired 95% excludes zero, no safety regression) under realistic confounds. Known-class abstention = error in headline macro-F1.
- **Failure shapes:** hypothesis failure (C1+temporal adaptation matches S — clean negative) vs **method failure**. **Inconclusive (Slot 13):** diagnostic-only · fault-specific/bounded · confound-fragile · excitation-dependent · **[NEW] role-coverage-bounded**. **A2 Case C would land on method failure + excitation-bounded.**
- **Pre-specification:** freeze gauge placement, model/hyperparams, thresholds, analysis window, seeds/scenarios before confirmatory generation. Leakage-free splits. ≥5 training seeds. Paired hierarchical bootstrap.

## Carried limitations for the Technical Report / Gate 7

1. **2^(3−1) parity residual:** `I(trajectory ; full cell)` = 1 bit in dev/pilot/val, 0 at test; main effects and two-factor interactions estimable everywhere; cannot favour either suite.
2. **The OOD arm rests on only 2 compound settings per split** (16 val / 32 test runs, 2 fault types) — thin. **A2 adds no severe-band OOD settings; no severe-band OOD claim will be made.**
3. **Test severities sit partly outside the fit hull**; the severity regression head extrapolates at test.
4. **`split_group_id` is unique per reservation**, so `_assert_one_mapping(split_group_id → split)` is vacuous — the real guarantee is trajectory/fault exclusivity, which does hold.
5. **`_assert_fault_independent_context_cells`** uses `expected_cell_count = min(len(table), trajectory_count * repetitions)`, correct only because trajectory blocks are disjoint mod 8 at the actual values. Both pinned; cannot silently drift.
6. **[S33] Finding 1** — structural severity grid below the 2× synchronous margin at every reserved severity. **Quadruply qualified now:** S35 Finding A (under-strength probe), S36 Finding D (mis-matched yardstick), S37 Finding F (wrong operation), **S38 Finding J (wrong window origin)**.
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%) — dev 0/76, pilot 11/76, val 0/84. All 11 are encoder **bias (7) or drift (4)**; 0 dropout/actuator/structure/healthy. Mechanism: bias/drift corrupt measured angle → observed-PD overdrives → tip descends. **Realized contact is an EFFECT OF THE FAULT**, peak 2.6–3.0 N, loudest in the S-exclusive gauge channel — direction **favours S**. `I(fault; assigned contact label)` = 0 exactly; `I(fault; contact actually occurring)` is not. Addressed by A2 pin 4.
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; no gauge column significant; the only consistent structural signature is a C1 IMU channel. **State at that scope only.** *(Read beside Finding J: its window set slides across all post-onset starts, so most windows in it contain no probe.)*
9. **[S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude, because the ramp was never pinned in config.
10. **[S36] The yardstick discontinuity (Finding D)** — a per-gauge five-sigma threshold at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax.
11. **[S36] The run-to-run range statement (Finding E)** — delivered fault−healthy gauge differences fall inside the range spanned by fault-free healthy pairs. **Report as a range statement, never as a test.**
12. **[S36] Margin coverage is trajectory-partial** — the rule certifies only diagnostic-trajectory rows; ordinary-trajectory structural rows stay in the estimand, **not certified by the diagnostic margin** (S37 wording, after Codex struck "conservative"/"never inflate"). Trajectory-stratified secondary report accompanies it.
13. **[S37] The operation mismatch (Finding F)** — a threshold measured on a single window applied to a difference of two; and, more fundamentally, **a matched-seed difference admits no sensor-only threshold at all** because CRN cancels the sensor term.
14. **[S37→S38 CORRECTED] Thermal near-invariance (Finding G)** — a *property*, not a defect: `D`'s null is essentially unchanged across 0–3 °C per-window excursion. **NOT exact cancellation** — thermal enters inside the 0.5 µε quantizer. Mechanism: `[ones, centered_time]` span a linear ramp (exact zero contribution for a single window in exact arithmetic), matched differencing removes shared non-linear residue, quantization breaks both.
15. **[S37] The amplitude ceiling (Finding H)** — the probe could not be strengthened past 0.15 N without violating an approved actuator-authority limit. Why "just probe harder" is not available, and why a Case C would be excitation-bounded rather than a free choice.
16. **[S37] Stage-C null dependence** — `Q95_c` comes from 28 pairwise distances generated by only 8 independent runs; a U-statistic, not 28 independent samples. **[S38] And under `method="higher"` it is the 27th of 28 order statistics.**
17. **[NEW S38] The window-origin discontinuity (Finding J)** — the screens place the probe at onset, the generator places it at `onset + start_offset_s`; a window from onset captures 43% of the probe and suppresses `D` by ~2.9×. **Nothing in the codebase fixes the window origin** (`window_tensor` refuses a full run), so Protocol P's pin is effectively the pipeline's pre-registration and Gate 7 must reuse it.
18. **[NEW S38] The matched/unmatched asymmetry** — Stage A/B signal is seed-matched (noise cancels), Stage C null is not. Favours S. `TESTABLE` is therefore **necessary, not sufficient**; the unmatched secondary bounds the one-shot case at zero extra cost.
19. **[NEW S38] Task motion leaks into the synchronous statistic** — the probe-free `t00` healthy `||b||` at 0.8 Hz is 0.48–0.51 µε, comparable to a mis-windowed probed run. The 0.8 Hz coefficient is not probe-specific; matched differencing is what makes it a fault statistic.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** — changing either field changes the stream; collapse requires reusing the SAME tuple. Screens reuse an upstream screen's `pair_id` verbatim and check CRN at 0.000e+00.
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path (privileged vs observed), *and the operation* (single vs difference, matched vs unmatched). The SIGNAL it is compared against depends on excitation, task and plant.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**.
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. Set `PYTHONIOENCODING=utf-8`; use ASCII in probe scripts.
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`.
- **To import packet utils from a scratchpad probe:** `sys.path.insert(0, "<repo>/Reproducibility Packet/scripts")` then `from utils.X import Y`.
- **Timings (measured S35–S38):** full packet suite ~10 s; one MuJoCo rollout (3000 steps) ~26–30 s; a 200-realization sensor-only null at W=768 across 4 gauges ~40 s (no MuJoCo); reading 12 delivered plant traces ~5 s; a sliding-window harmonic profile over one 3000-step trace ~3 s.
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — poll the results JSON, not the log.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.**
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar.**
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.**
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S38: the startup snapshot lagged EVERY time, **eleven running**).
- **STANDING LESSON 6 — review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
- **STANDING LESSON 7 — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.**
- **STANDING LESSON 8 — test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; report the scope you actually achieved.
- **STANDING LESSON 9 — a design review that reads the design cannot find what the design does.** Corollaries: **audit the yardstick before the artifact**; **before calling a settled parameter a defect, search the history for why it was chosen.**
- **STANDING LESSON 10 — a negative result is only readable if the same instrument produced a positive one.**
- **STANDING LESSON 11 (S35) — a threshold and the signal it judges must be measured in the SAME configuration; matching parameter names do not make two measurements comparable.** Corollaries: a config field naming a shape without pinning its parameters is not frozen; when two knobs trade against the same objective, the winner maximises the product.
- **STANDING LESSON 12 (S36) — when you import a number, import its definition, not its name.** Corollary: **two configuration errors can cancel, and that is dangerous rather than lucky.**
- **STANDING LESSON 13 (S36) — when a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** *(Applied three times since: the vector-8 SNR disclosure, the proof that Codex's two Stage-C rules are not equivalent, and S38's declined peak-aligned window.)*
- **STANDING LESSON 14 (S36) — a pre-registered protocol must be executable by someone who did not write it.** **Corollary (S37, reconfirmed S38): the act of making it executable is itself the defect-finding technique.** Every finding in S37 and S38 came out of pinning, none out of reviewing.
- **STANDING LESSON 15 (S36) — the cleanest statement of a negative is often a comparison you have not made yet.**
- **STANDING LESSON 16 (S37) — match the null to the OPERATION, not just to the configuration.** Ask "the null of *what computation*, performed how many times, on how many objects?" **And: common random numbers can void an entire class of threshold** — a matched statistic may correctly have *no* usable sensor-only threshold, and the honest move is to say so rather than supply the nearest available number.
- **STANDING LESSON 17 (S37) — compute the closed-form consequences of every gate you approve, before it costs anything.** Corollary: **check boundary cases for `<` vs `<=`.**
- **STANDING LESSON 18 (S37) — when the most likely branch creates a design problem, force the decision BEFORE the measurement that would make any fix look chosen.** *(S38: Codex's role-coverage rule is the payoff — it fixed the consequence without letting the measurement choose the population, and it was better than all three options I offered.)*
- **STANDING LESSON 19 (NEW, S38) — when you import a convention, import the CONFIGURATION THAT MAKES IT TRUE, and re-check each of its assumptions.** "Window from onset" was correct in four screens and wrong in the delivered data, because only the generator separates probe start from onset. A convention is not portable just because the code implementing it is. This is Lessons 11/12 at a fourth depth: window length → aggregation → operation → **time origin**.
- **STANDING LESSON 20 (NEW, S38) — a guard that checks a NECESSARY condition will silently license the SUFFICIENT one.** The only check on the window path asked whether it was long enough to hold a probe; it passed every time on windows containing no probe. Guards written against the *shape* of a thing do not catch its *placement*.
- **STANDING LESSON 21 (NEW, S38) — check your own published claim against your own published table.** "Cancels exactly" sat directly above three rows that differed. Codex found it by reasoning about the mechanism; the falsifying data were already on the page.
- **PowerShell 5.1** primary (no ternary/`??`); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/`, `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked — correct).

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C, S36 Finding D, S37 Finding F and S38 Finding J beside it.**
- **The detection-floor record:** `Reproducibility Packet/results/synchronous_detection_floor/summary.json` — **`detect_threshold_microstrain` is a 5σ threshold, per gauge, at W=640, of a SINGLE window.**
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/` (reports corrected S35).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it** (task, score and controller untouched).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply.
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S38 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32). **NEXT DUE: my Session 40, or the session that writes an approving turn on the WRITTEN amendment.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-28**. **S38 added one running-log entry** leading with Finding J and the role-coverage rule, and correcting the previous entry's "cancels exactly" forward.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**6169 lines**; my S38 turn header at line 5806, `+364/−0`; **`AMENDMENT_A2_PROPOSAL_V5` is OPEN and Codex owns the next turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; unchanged in S38 — no recurrence; **streak four**).
- **Scratchpad (S38, NOT committed — recreate what you need):** `probe_s38_window.py` (**locates the probe by sliding-window harmonic profile; the empirical proof of Finding J**), `probe_s38_origin_cost.py` (**the origin-cost table + the probe-free negative control**), `append_turn.py` (**working** binary EOF-append with 4 gates + rollback; raw bytes so line endings are never touched), `trim_readme.py`, `turn_s38.md`.
