# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 40, 2026-07-29 12:55 PDT.*

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 40**; next session I run is **Session 41**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**
- **THERE IS AN OPEN REVIEW LOOP AND CODEX OWNS THE NEXT TURN: `PROTOCOL_P_V2.3_POSTED_FOR_EXACT_STATE_REVIEW` (my S40 turn, transcript line 7108).** Do not start Gate-4 work, do not apply the seam patch to the packet, and do not implement or run Protocol P until it settles.
- **Progress report DONE at S40** (regular, covered S33–S40). **Next regular: my Session 48.** Event triggers still stack: a phase transition, or an approved amendment to the Claim Sheet (the *written* amendment, not approval of a proposal text).
- **This is the fourth consecutive block on this protocol. I committed in writing (turn + HumanReport40) to escalating to the director rather than looping a fifth time if round five does not converge.** Honour that.

## THE HEADLINE OF SESSION 40

**Codex required nine changes. All nine hold at source; none was wrong; two are worse than Codex's text said. The session's substantive addition: the override seam v2.2 described but did not have is now BUILT AND VERIFIED — in scratchpad, not the packet.**

### The two pins that were worse than stated

1. **The `_dataset0` suffix inverted a safety claim of mine.** v2.2 said a leaked screen row would fail the manifest audit *because it lacked* the suffix. The construction named in the same paragraph appends it unconditionally, so the row would have **carried** it and the guard would have **passed the leak through**. Third instance of the guard family (rank guard S39, necessary-vs-sufficient S38). v2.3 chooses a suffix-free screen identity and **tests both tripwires** with the exact state.
2. **The ramp override is unreachable, not merely un-plumbed.** Peak and severity *are* reachable without touching Codex's file (mutated in-memory assignment document) — rejected on provenance grounds. Ramp is reachable by **no route at all**: `_physical_config:338` computes `duration / 2.0` from `cycles`/`frequency_hz`, so every input yields exactly fraction 0.5. Fraction 0.125 (every pre-dataset screen's value) is unreachable. **The code change is forced, not preferred.**

### Claims of mine withdrawn in S40

- **Finding J's ratio does NOT cancel its confound.** The two norms reduce **different time samples**, so unmatched divergence enters each with its own 0.8 Hz content, and a norm is not additive in the two terms. "Cancels" and "clean" withdrawn. **2.37–3.64× is now: the ratio of the TOTAL unmatched-row four-gauge 0.8 Hz difference between two windows.** Not a fault-effect multiplier. **The probe-start origin is retained on purely prospective grounds** (config-derived, contains the whole declared burst, fixed before any response is seen) — Codex approves that separately.
- **`Q95_c^gauge` cannot classify a Case C.** One fixed trace identifies redraw variation *for that trace*; components can interact or partially cancel. It may say whether the full healthy null exceeds the fixed-trace redraw term and by how much, conditional on that trace. **No mechanism attribution. No authority.** Same narrowing applies to M2.
- **"Look above the generator, not inside it"** removed from the `NO_ADMISSIBLE_PROBE` branch. One zero-override healthy row cannot validate an override path that did not exist when the gate ran.

## THE SEAM — full spec, because the prototype is NOT committed

Scratchpad only: `probe_s40_seam.py`. **Rebuild from this section if needed.** Three additions to `Reproducibility Packet/scripts/utils/assignment_generator.py`, all keyword-only, all defaulting to current behaviour.

```python
@dataclass(frozen=True)
class ScreenOverrides:
    probe_peak_force_n: float | None = None
    probe_ramp_fraction_of_duration: float | None = None
    physical_faults: tuple[FaultSpec, ...] | None = None
    realized_pair_id: str | None = None
    provenance_hash: str | None = None
    def is_active(self) -> bool:
        return any(v is not None for v in (self.probe_peak_force_n,
            self.probe_ramp_fraction_of_duration, self.physical_faults, self.realized_pair_id))

def screen_pair_id(reservation, overrides) -> str:
    if overrides is not None and overrides.realized_pair_id is not None:
        return str(overrides.realized_pair_id)
    return f"{reservation.base_pair_id}_dataset0"
```

`_physical_config(..., *, control_dt_s, overrides=None)` — inside the `probe is not None` branch only: `peak_n` and `ramp_s` become locals (`ramp_s = duration / 2.0` default); peak override must be finite and `> 0`; ramp fraction must be finite and in `(0, 0.5]` else raise. In the `probe is None` branch a probe override **raises** rather than being silently discarded.

`_generate_reservation(..., overrides=None)`: active overrides without a provenance hash raise; `stamped_hash = provenance_hash if active else config_hash` and **`stamped_hash` — not `config_hash` — is passed to the `OnlineSensorSession` and every `SensorModel.observe`**; `physical_faults` override replaces the derived list (raises if `sensor_fault is not None`); `control_pair_id = screen_pair_id(reservation, overrides)`.

### Verification results (do not re-do)

```text
B REACH (0 rollouts)
  overrides=None peak / ramp      == 0.05 / 0.625 (= duration/2, duration 1.25 s)
  peak 0.15                       -> CableModelConfig 0.15
  ramp fraction 0.125             -> 0.15625        0.25 -> 0.3125     0.5 -> 0.625
  ramp fraction 0.5               == delivered hard-code EXACTLY  <- the seam's regression test
  ramp 0.0 / 0.5000001 / 0.6 / -0.1 / nan            all rejected
  active overrides, no provenance hash               rejected
  structural FaultSpec severity   -> plant._physical_config.structural_ei_remaining 0.75
  faulted plant builds _soft_model; healthy plant has _soft_model is None
  identity override               -> "basepair_protocolp_stageAB_c4" exactly
C LEAK GUARD (0 rollouts) — guard fed the exact state
  suffix-free row      -> AssignmentGenerationError "dataset pair_id lacks the dataset0 suffix"
  suffixed, unapproved -> AssignmentGenerationError "manifest reservation set differs from selection"
A TRANSPARENCY (1 rollout, 26.4 s) — overrides=None on scenario_dev_t01_f000_r00
  20/20 privileged array fields byte-identical ; 30/30 S observation arrays byte-identical
  realized pair_id unchanged by the patch
```

### Named but NOT patched — open scope question handed to Codex

When `physical_faults` is overridden, `_fault_components` still returns the **source reservation's label**, so a screen run on a healthy reservation describes itself as healthy while its plant carries a structural fault. Protocol P never persists or reads a screen label, so I left it. My judgement: belongs to whatever first persists an overridden run, not to Protocol P. Codex owns the file and may disagree.

## PROTOCOL P v2.3 — clean, pre-registered, DELIBERATELY UNRUN

*(v2.3 = v2.2 + the seam + realized-identity correction + provenance + narrowed J and `Q95^gauge` + fail-loud. Nothing has ever been run.)*

**Universe.** `trajectory_dev_diagnostic_b` (`t01`) only, cells 4/5/6/7 = replicates r00..r03 (r00 nominal/iso25c/brief, r01 nominal/warm2c/none, r02 0.050 kg/iso25c/none, r03 0.050 kg/warm2c/brief) — balanced half-fraction. Ordinary trajectory stays probe-free as the pre-registered negative control.

**Construction.** Every plant-bearing rollout via `_generate_reservation` through the seam:
```text
config     = load_config("config/draft-config-v0.1.json", "schema/schema.json")
assignment = load_assignment("config/proposed-gate3-assignment-v0.1.json")
binding    = validate_approved_assignment_binding(config, expected_assignment=assignment)
runtime    = _runtime_parameters(binding)      # dt 0.002, f_ctrl 500, sim_dt 1e-4, points 17
history    = config.document["values"]["timing"]["window_steps"]     # 768
_generate_reservation(binding.assignment, config.config_hash, ("S",), None,
                      history, runtime, screen_reservation, overrides=ScreenOverrides(...))
```
Loop driven by the **C0** session; S produced afterwards by `SensorModel().observe(result.plant, "S", ...)` at the **same realized identity**. **No online-S variant authorized** (Finding K).

**Screen reservation.** Copy the delivered dev `t01` reservation for the target context cell (`r00..r03` — that is what fixes payload/environment/contact), replace **exactly two fields** (`sensor_seed`, `base_pair_id`), assert every other field equal to source. `fault_setting_id` stays the dev **healthy** setting so `_fault_components` returns no physical and no sensor fault; the ladder fault enters only via `overrides.physical_faults`. The assignment catalog is never mutated.

**Realized identity table (suffix-free by override).** `CablePlant` has no RNG → identity is exactly `(sensor_seed, realized pair_id)`.
```text
P_SEED_BASE = 150000 ; cell c in {4,5,6,7} ; r = c - 4
Stage A + B: sensor_seed = 150000 + 10*r + 2   -> 150002 150012 150022 150032
             pair_id     = "basepair_protocolp_stageAB_c{c}"
Stage C k=0: reuse the Stage-A healthy rollout of the SELECTED candidate
      k>=1:  sensor_seed = 150000 + 10*r + 1000*k + 2
             pair_id     = "basepair_protocolp_stageC_c{c}_k{k}"
Stage C gauge-only secondary (0 rollouts): the k=0 trace redrawn at k=1..7
Stage 0 (no plant): pair_id = 1, sensor_seed = 0..199
```
Band `[150002, 157032]` cannot collide with dev `[110000, 111514)`; far below pilot's 210000. **Two tested leak tripwires:** the suffix assertion at `assignment_generator.py:241-242` and the approved-set comparison at `:244-245`.

**Provenance (req 4).** Every screen rollout stamps `screen_provenance_hash = "dev-protocolp-v2.3-" + sha256(canonical_json)[:32]`, never the base config hash. `canonical_json` = `json.dumps({..}, sort_keys=True, separators=(",",":"))` over: `base_config_hash`, `assignment_file_sha256`, `assignment_hash`, `protocol_spec_sha256` (of the v2.3 block, recorded once at implementation), `stage`, `cell`, `condition`, `overrides` (all four values), `reservation` (`scenario_spec_id`, `base_pair_id`, `sensor_seed`). `dev-` prefix retained so screen artifacts stay ineligible for confirmatory analysis. Results JSON records the full `canonical_json` per rollout, not just the digest.

**Replay gate — stop-or-go precondition (1 rollout).** Hash both pinned references; **absent or changed ⇒ raise and stop** (no fallback to whatever is on disk). Rebuild `scenario_dev_t01_f000_r00` with `overrides=None`; require all 20 privileged array fields and all 38 npz payload entries equal. **Failure ⇒ Stage A does not start.**
```text
data/gate3-base-dev-pilot-val-c1-s/   (git-ignored, local only — retained development data, NOT committed payload)
plant/scenario_dev_t01_f000_r00_S_dataset0.npz
  ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45   (verified S40, matches Codex)
observations/S/scenario_dev_t01_f000_r00_S_dataset0.npz
  cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83   (verified S40, matches Codex)
```
**Achieved scope is ONE-ROW EXACT REPLAY.** The 472-reservation / 944-pair dataset was never regenerated; make no dataset-wide reproduction claim.

**Window (Finding J).**
```text
w0 = round((onset_time_s + diagnostic_probe.start_offset_s) / control_dt_s)   # raise if off-grid
w1 = w0 + 768                                                                # raise if w1 > n_steps
split   trajectory                    onset  offset   w0     window        steps
dev     trajectory_dev_diagnostic_b    1.00   1.00   1000  [1000,1768)     3000
pilot   trajectory_pilot_diagnostic_d  1.10   1.20   1150  [1150,1918)     3050
val     trajectory_val_diagnostic_f    1.15   0.90   1025  [1025,1793)     3075
test    trajectory_test_diagnostic_h   1.25   1.10   1175  [1175,1943)     3125
```
Every split = 625 probe steps + 143 ringdown steps. **Stage 0 exempt** (no plant → no origin). Empirical peak **1208 / 2.092897106 / +11.2897%** over the probe-start origin's `1.880585474` — disclosed and **rejected** (response-selected, favours S).

**Statistic.**
```text
D = || concat_{g=0..3} ( b_g(fault) - b_g(healthy) ) ||_2          8 entries
tm = record.measurement_time_s["gauge_obs"]
if   tm.ndim == 1:                       t_g = tm
elif tm.ndim == 2 and tm.shape[1] == 1:  t_g = tm[:, 0]    # legacy; currently unreachable
else:                                    raise ProtocolPError("must be [T] or [T,1]")
if not (t_g.shape[0] == gauge_obs.shape[0] == gauge_valid.shape[0]): raise ProtocolPError(...)
b_g = harmonic_coefficients(gauge_obs[w0:w1, g], gauge_valid[w0:w1, g], t_g[w0:w1], 0.8)
```
Observed path only. Matched on `sensor_seed` **and** realized `pair_id` in Stage A/B.

**Stage 0 (0 rollouts).** Adds `timing.diagnostic_probe.ramp_fraction_of_duration`; candidates `{0.125, 0.25, 0.5}` → ramps `0.15625 / 0.3125 / 0.625 s` (duration 1.25 s). At `cycles=1`, fraction-of-duration ≡ fraction-of-period. `cable_mechanics` admits `(0, 0.5]`. New packet script `scripts/analyze_synchronous_difference_null.py` → `results/protocol_p/sensor_only_difference_null.json`, reusing the gauge-window helper **lifted into `utils/`**.
```powershell
Set-Location "Reproducibility Packet"
..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1
```
**Single line. Backtick is the ONLY permitted continuation; `^` is a cmd.exe token.** **One sample = one PAIR of four-gauge windows → one scalar. 100 samples, not 200, emphatically not 800** (`analyze_synchronous_detection_floor.py:241-242` appends per gauge per realization — how `0.4053` became an 800-sample per-gauge number). `T1` retired. **M2 is its first real-plant corroboration.**

**Stage A — admissibility + selection (108 rollouts, after the replay gate).** 9 admissible candidates (peak `{0.05,0.10,0.15}` N × ramp fraction `{0.125,0.25,0.5}`) × 4 cells × 3 conditions `{healthy, remEI 0.75, remEI 0.35}`. Declared grid stays all 24; the approved inclusive torque gate `F_peak * 2 * link_length_m <= 0.60 * torque_abs_limit[0]` excludes 15 before simulation (0.15 N → `0.12` exactly; **`<=` is load-bearing**). Hard gates every cell/condition, **all computed from the returned `PrivilegedRecord`**: zero `safety_flag` across all 7 A1 flags; `max|qd_true| <= 8.0`; `max|q_true| <= 2.5`; `max|gauge_true| <= 400 µε`; the torque gate; no increase in saturated steps vs zero probe amplitude (baseline 0). Failing candidate dropped, remaining cells skipped, drop count logged. **Selection: maximise worst-cell `D` at remEI 0.75, NO `T1` cutoff.** Ties within 1% → smallest amplitude → largest ramp fraction.

**`NO_ADMISSIBLE_PROBE`** — terminal, **pins nothing**; `config.json` stays absent, no regeneration. Slot-12 method failure + Slot-13 excitation-bounded non-transfer. Scoped to the one measured candidate:
```text
0.05 N / ramp 0.5 fails healthy or remEI 0.75
   -> contradicts its delivered-row pass; implementation-integrity failure requiring
      diagnosis before further execution   (NO defect-localization claim)
that candidate passes those but fails remEI 0.35
   -> newly observed physical safety/method limit
any other candidate's failure -> recorded normally; classifies nothing by itself
```

**Stage B — the ladder (32 new rollouts).** Selected candidate at all ten reserved remaining-EI values `{0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.75,0.85,0.90}` × 4 cells; `0.75` and `0.35` reused from Stage A at matched identity. Every rollout re-asserts the hard gates. **`UNSAFE_LADDER_VALUE`** labels `v` unsafe, excludes it with reason, does **not** reopen selection, is neither TESTABLE nor SUB-THRESHOLD. **Cases A/B/C require all ten values to have safe valid M2 verdicts;** otherwise terminal.

**Stage C — the operative null (28 new rollouts).** 8 healthy replicates per cell (k=0 reused), all `C(8,2)=28` within-cell pairs.
```text
Q95_c   = np.quantile(within_cell_distances, 0.95, method="higher")
pass(v) iff D(v,c) >= 2.0 * Q95_c   for EVERY screened cell c
```
Scalar form `min_c D >= 2*max_c Q95_c` is strictly stricter → pre-declared sensitivity, not a second success route. `Q95_c >= 0.30 µε` is a **diagnostic pause only**. Carried limitation: 28 distances from 8 runs is a U-statistic; `method="higher"` puts it at the 27th of 28.

**Stage C gauge-only decomposition — secondary, 0 rollouts, NO authority.** k=0 trace held fixed, redrawn at k=1..7, all 28 distances, `Q95_c^gauge` same rule. **Conditional healthy-null diagnostic only** — may report whether `Q95_c` exceeds the fixed-trace redraw term and by how much; **no mechanism attribution**, sets no threshold, gates nothing.

**Unmatched secondary — conditional descriptive sensitivity, 0 rollouts, NO authority.** `D_unmatched(v,c,k) = ||b(fault at v, identity_AB) − b(healthy_k, identity_k)||`, k=1..7. Seven **dependent** distances sharing one fixed fault-side identity, no fault-side replication. **No quantile, gate, route, or bound.**

**Outcome.** One row per ladder value: `D(v,c)` all four cells, `Q95_c`, `2*Q95_c`, `Q95_c^gauge`, the seven `D_unmatched`, per-cell verdict, value verdict. **Aggregation is the conjunction over all four cells:** testable iff `min_c [ D(v,c) − 2*Q95_c ] >= 0`. No mean/median/pooled quantity enters a verdict. **Case A** (all ten pass) / **Case B** (proper subset) / **Case C** (none, after all ten have safe valid M2 verdicts → Slot-12 method failure + Slot-13 excitation-bounded non-transfer). **`TESTABLE` is necessary, not sufficient.**

**Role coverage (pre-declared, before the ladder is read).** Count known-class testable structural settings per split; **report the count 0/1/2**. OOD at 0.45/0.55 never counts. Zero dev → no testable structural training support. Zero val → structural model selection/calibration unsupported. Zero test → four-way testable-stratum confirmatory metric undefined. Any of those three zeroes ⇒ named **role-coverage-bounded non-transfer outcome** (S/C1 secondary reportable; establishes neither success nor hypothesis failure). Count 1 = thin single-severity role, no new terminal branch. Zero pilot relabels nothing; disables data-driven downsizing → retain the prospectively allowed maximum test replication and name the limitation.

**OOD role pinned.** Labels at 0.45/0.55 characterize mechanics testability only; those rows keep `ood_flag=true`, stay excluded from four-way known-class macro-F1 under `ood_known_metric_rule`, remain in pre-registered OOD metrics.

**Fail-loud (req 9).** Every decision-bearing invariant is `if ...: raise ProtocolPError` — never `assert` (`python -O` removes them). `assert` only in `tests/`. The twelve named invariants: reference hashes; byte equality (20 fields + 38 npz entries); screen reservation differs from source in exactly `{sensor_seed, base_pair_id}`; realized pair_id carries no `_dataset0`; all eight Stage-C identities unique per cell; Stage-C k=0 == selected Stage-A healthy identity; Stage-A/B fault+healthy share one identity (deliberate, asserted not assumed); active overrides carry a provenance hash and the stamped hash != base config hash; window origin on-grid and `w1 <= n_steps`; measurement-time rank/width/length (explicit if/elif/else); harmonic fit ≥5 finite valid samples; every hard safety gate per cell and condition.

**Cost:** replay 1 + Stage 0 (0) + A 108 + B 32 + C 28 = **169 rollouts, ~76 min** at 26.4 s/rollout (measured S40). Background job; **poll the results JSON, not the log.**

## HONEST ODDS — unchanged in direction from S39, one reason removed

Against M2's measured gauge-only bar, projecting the S35 amplitude ratio ×3.15 over 0.05 → 0.15 N (**importing that ratio across configurations remains the weakest link — the exact Lesson-11/12 move**):
```text
remEI 0.50   c4 1.502 vs 0.711 x2.11    remEI 0.75   c4 0.491 vs 0.711 x0.69
             c5 1.475 vs 0.850 x1.74                 c5 0.470 vs 0.850 x0.55
             c6 0.856 vs 0.635 x1.35                 c6 0.315 vs 0.635 x0.50
             c7 0.853 vs 0.771 x1.11                 c7 0.294 vs 0.771 x0.38
```
**remEI 0.75 fails everywhere by a wide margin — the one robust statement.** remEI 0.50 clears the binding cell by only **1.11×**, computed with an **inflated signal** (Finding L) against a **deflated bar** (M2 omits closed-loop divergence) — both errors favour the hypothesis. **Case B (dev coverage 1) and Case C remain roughly comparable.** **New in S40:** Finding J's ratio can no longer be quoted as evidence the signal rises, so one of S38's reasons for leaning to Case B is gone. Stage C settles it.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority, ≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds).

## The two zero-rollout measurements from S39 (still valid)

**M1 — the observed path barely degrades a MATCHED difference.** Both delivered plant traces of a pair re-observed at ONE common identity, 6 identities. Isolates quantization/dropout/latency/hysteresis/bias/drift.
```text
setting        cell   D_true   D_obs mean   ratio        setting     cell  D_true  D_obs mean  ratio
remEI 0.50      4     0.4787     0.4768     0.996        remEI 0.75    4   0.1584    0.1559   0.984
remEI 0.50      5     0.4755     0.4683     0.985        remEI 0.75    5   0.1593    0.1492   0.937
remEI 0.50      6     0.2755     0.2717     0.986        remEI 0.75    6   0.0872    0.1001   1.148
remEI 0.50      7     0.2798     0.2709     0.968        remEI 0.75    7   0.0968    0.0934   0.965
```
**0–6% cost on average, ±10% spread; at small `D` the residue moves EITHER way.**

**M2 — the gauge-path-only component of the Stage-C null.** One delivered healthy plant trace per cell held EXACTLY fixed, redrawn at 8 identities, all 28 within-cell distances, `method="higher"`.
```text
cell   min / median / max           Q95 (27th of 28)   2*Q95
 4     0.1540  0.2807  0.3731            0.3555        0.7110
 5     0.1524  0.2620  0.4325            0.4251        0.8502
 6     0.1377  0.2709  0.3922            0.3176        0.6351
 7     0.1443  0.2983  0.4706            0.3854        0.7708
```
**A decomposition, NOT a bound.** It does two things: **validates Stage 0** (synthetic no-plant ~0.39 sits inside the real-plant 0.318–0.425) and identifies **cell 7 (payload + warm + contact) as the binding cell**.

**The enabling tool (S39, reconfirmed S40).** `SensorModel().observe(delivered_plant, "S", pair_id=<manifest>, sensor_seed=<manifest>)` reproduces the delivered row **bit-for-bit with no MuJoCo**; a perturbed `pair_id` moves `gauge_obs` by up to **6.50 µε** (against `D` of order 0.1–0.5). **Any stored plant trace can be re-drawn on the observed path at any identity for free.**

## What I did / verified in S40 (do not re-do)

- Confirmed all four Codex pins at source: `assignment_generator.py:521` (suffix, used at both `:524` and `:554`), `:338` (ramp hard-code), `_fault_components:382-384` (severity from catalog), `data/` git-ignored at `.gitignore:19`.
- Established the ramp is unreachable by **any** document input; peak/severity reachable but rejected on provenance grounds.
- **Built and verified the seam** (three test classes, table above; 1 rollout, 26.4 s).
- **Fed both leak tripwires the exact state** and observed both raise.
- Re-hashed both replay references — **match Codex exactly**. Re-hashed the assignment file.
- Reconciled 38-vs-30: npz = **38 keys** = 30 per-channel arrays (5 dicts × 6 channels) + 8 metadata (`schema_version, suite, run_id, pair_id, config_hash, split, channel_names, suite_available_mask`). Both agents reported full equality of the same bytes.
- **Codex's S39 append verified at git level: 6,853 → 7,107, `+254/−0`, header unique at 6,855, after the boundary. Clean-append streak: SIX.** No monitoring note (duty is recurrences).
- **My S40 append: `+662/−0`**, header unique at line 7,108, after the 7,107-line tail, four gates asserted with rollback. Transcript now **7,769 lines**.
- Live-Run README: one running-log entry (banner already 2026-07-29). Progress Report Session 40 written.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY Protocol P v2.3, then the written A2.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** (dev contexts, EI 0.75/0.50) and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (D) + the run-to-run range statement (E) + trajectory-partial margin coverage; (h) **[S37]** the operation mismatch (F), thermal near-invariance (G) as a *property*, the amplitude ceiling (H); (i) **[S38]** the **window origin (J)** — the driver MUST use the same origin Protocol P pins, since nothing in the codebase fixes it; plus the matched/unmatched asymmetry and role-coverage counts; (j) **[S39]** the **construction path (K)** — build/read records by the same C0-loop-then-post-hoc-observe path — and the **unmatched-identity confound (L)**, which governs how any delivered-row magnitude may be quoted; (k) **[NEW S40]** if the seam ships, the driver must distinguish **`base_pair_id` from realized `pair_id`** in every identity join and audit, and must never stamp an overridden run with the base config hash.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → **Protocol P v2.3 [CODEX OWNS THE TURN] ← WE ARE HERE** → apply the seam patch + post the diff → replay gate → Stage 0/A/B/C → Codex reviews implementation + result + branch → written amendment + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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
- **Manifest columns** (= `IdentityManifestRow` fields, 20): `schema_version, config_hash, scenario_spec_id, pair_id, run_id, trajectory_spec_id, fault_setting_id, split_group_id, split, suite, estimator_id, controller_id, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed, train_seed`. **Note `trajectory_spec_id`, not `trajectory_id`; `fault_setting_id`, not `source_class`. `pair_id` here is the REALIZED id (with `_dataset0`), not `base_pair_id`.**
- **`run_id` carries the suite:** `scenario_dev_t01_f000_r00_S_dataset0`. The **plant** role is stored per suite too (C1 and S share a byte-identical payload — documented duplication), so a plant path is `plant/{run_id}.npz` with the suite suffix included.
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. Fields: `suite, run_id, pair_id, config_hash, values, valid_mask, measurement_time_s, availability_time_s, latency_age_s, suite_available_mask, schema_version, split`. **`values` and `valid_mask` are DICTs** channel → `[T, width]`. **`measurement_time_s` / `availability_time_s` / `latency_age_s` are DICTs of RANK-1 `[T]` arrays.** Gauges are `values["gauge_obs"]` `[T,4]`.
- **Load one plant trace:** `PrivilegedRecord.load_npz(root/"plant"/f"{run_id}.npz")` (`utils.schema_types`).
- **Re-observe any plant trace offline, NO MuJoCo:** `SensorModel().observe(plant, "S", pair_id=..., sensor_seed=..., fault=None, run_id=..., config_hash=..., split=...)` — verified bit-identical at the manifest identity (S39/S40).
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag[2], safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths / timing:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400, **no probe**; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, onset 500, **probe steps 1000→1625**. Both carry 76 rows per suite. **Only `t01` has a probe.**
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict** (`_catalog()` builds the mapping). Same for `context_profiles`, whose keys are `payloads` / `environments` / `contacts`.
- **dev fault settings (t01):** `fault_dev_healthy` (f000); `fault_dev_structure_link_stiffness_loss_loc1_sev0p5` (f001); `..._sev0p75` (f002); then actuator loc0/loc1 × {0.5,0.75}; then sensor bias/drift/dropout × loc{0,1} × 2 sev.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into gauge variation that EXCEEDS the structural fault signature (S36 Finding E).** Any fault-effect *magnitude* measurement MUST match both `sensor_seed` AND realized `pair_id`. Separability measurement must NOT (that is the point). **Delivered fault and healthy rows do NOT share identity (S39 Finding L) — so any delivered-row magnitude is `||fault + divergence||`, on BOTH the privileged and observed paths.**

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0fec4269180139efc9a4c9ce38e7f8f23d890d182dc8eb063803e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope (schema-v1.0.md §Amendment A1):** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order (joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force) computed in `cable_plant.py:_safety_flags` (line 272, called 377); `saturation_flag[T,2]` separate. Computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT. **`config_hash = dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56`** (parent `dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180`). Embedded assignment hash lives at `/values/scenario_manifest/approved_assignment_hash`. Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, S35 Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — file SHA-256 `76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae`, `assignment_hash = dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1`. Top keys include `trajectory_specs`, `fault_grid_by_split`, `compound_ood_settings`, `context_profiles`, `generation_plan`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30). Probe `start_offset_s` per split: **dev 1.0, pilot 1.2, val 0.9, test 1.1 — offsets FROM ONSET (Finding J).**
- **`scripts/utils/assignment_binding.py`** — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.**
- **`scripts/utils/assignment_generator.py`** — `GenerationRuntimeParameters(control_dt_s, f_ctrl_hz, simulation_timestep_s, point_count)` + `_runtime_parameters(binding)`; `_step_index` fails loud off-grid; **`audit_manifest_against_assignment` (225; `:241-242` suffix assertion, `:244-245` approved-set comparison — the two leak tripwires)**; `_profile` (286), **`_physical_config` (305; `:334` peak from assignment, `:336` probe start = `onset + start_offset_s`, `:338` the hard-coded ramp `duration/2`)**, `_temperature_function` (350), `_fault_components` (376; `:382-384` severity from the expanded-settings catalog keyed by `fault_setting_id`), **`_generate_reservation` (483; `:521` the unconditional `_dataset0` suffix, used at `:524` OnlineSensorSession and `:554` SensorModel.observe; `history_steps` is arg 5, supplied at 634 from `timing.window_steps`)**, `build_identity_manifest` (165), `preflight_assigned_mechanics`, `materialize_base_dataset` (595), `audit_materialized_base_dataset`, `shared_channels_equal`. `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`scripts/utils/gate3_assignment.py`** — `load_assignment`; `expand_reservations(document)` → `list[ScenarioReservation]` (fields: schema_version, draft_config_hash, scenario_spec_id, base_pair_id, trajectory_spec_id, fault_setting_id, split_group_id, split, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed). **Lines 648-697** are the seed/ordinal/context-cell derivation: `seed = seed_base + 10*ordinal`, `sim/fault/sensor/controller = seed+0/1/2/3`, `base_pair_id = basepair_{split}_t{ti:02d}_f{fi:03d}_r{rr:02d}`, realized dataset `pair_id = base + "_dataset0"`. Ordinal nests (trajectory, fault, replicate), resets per split.
- **`scripts/utils/storage_contract.py`** — `IdentityManifestRow` (20 fields, above), `IDENTITY_MANIFEST_FIELDS`, `DeployableObservationLoader`.
- **`utils/config_contract.py`: loader is `load_config(config_path, schema_path, *, require_frozen=False)`.** `ValidatedConfig`: `source_path, schema_path, document, config_hash, status` (`is_frozen` is a property). Validator CLI flags: `--assignment` / `--schema` / `--config`.
- **`utils/sensor_model.py`** — `config_hash` is **free-form provenance, never validated** (`:235, :253, :612, :641`), which is what makes the derived screen-provenance stamp safe. Temperature reaches the gauges at `:423-424` (10 µε/°C); the 0.5 µε quantizer is at `:429-431`.
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

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `link_thickness_m=0.004`, `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`, `diagnostic_tip_load_{peak_n,frequency_hz,start_s,duration_s,ramp_s}`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` (`:444-454`) requires the ramp finite and ≥0, requires a duration if non-zero, and raises when `ramp > duration/2` → admissible fraction `(0, 0.5]`.** Probe local time is `time_s - diagnostic_tip_load_start_s` (466, 488).
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **No RNG anywhere in the file (verified S37).** **A structural fault does `dataclasses.replace(config, structural_ei_remaining=severity)` → `self._physical_config` (`:99-103`) and builds a SECOND softened MuJoCo model at `:118-121`; the healthy plant has `_soft_model is None`. The `structural_ei_remaining=0.50` dataclass default is INERT in the healthy branch (built with `softened=False`) — do not quote it as a healthy stiffness (S40).** Fault severity **is** the remaining-EI fraction. **`cable_plant.py:124-125` (validator) restricts structural faults to location `{-1,1}` and severity to `(0,1]`** (verified S30 — a genuine plant constraint; do not re-litigate). Actuator severity = remaining gain fraction, location = joint index; applied at `:333-336`.
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
10. **[S36] The yardstick discontinuity (D)** — a per-gauge five-sigma threshold at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax.
11. **[S36] The run-to-run range statement (E)** — delivered fault−healthy gauge differences fall inside the range spanned by fault-free healthy pairs. **Report as a range statement, never as a test.** *(S39 Finding L identifies the mechanism: the rows differ in identity as well as fault.)*
12. **[S36] Margin coverage is trajectory-partial** — the rule certifies only diagnostic-trajectory rows; ordinary-trajectory structural rows stay in the estimand, **not certified by the diagnostic margin**. Trajectory-stratified secondary report accompanies it.
13. **[S37] The operation mismatch (F)** — a threshold measured on a single window applied to a difference of two; and **a matched-seed difference admits no sensor-only threshold at all** because CRN cancels the sensor term.
14. **[S37→S38 CORRECTED] Thermal near-invariance (G)** — a *property*, not a defect: `D`'s null is essentially unchanged across 0–3 °C per-window excursion. **NOT exact cancellation** — thermal enters inside the 0.5 µε quantizer (`sensor_model.py:429-431`). Mechanism: `[ones, centered_time]` span a linear ramp (exact zero for a single window in exact arithmetic), matched differencing removes shared non-linear residue, quantization breaks both.
15. **[S37] The amplitude ceiling (H)** — the probe could not be strengthened past 0.15 N without violating an approved actuator-authority limit. Why "just probe harder" is not available, and why a Case C would be excitation-bounded rather than a free choice.
16. **[S37] Stage-C null dependence** — `Q95_c` comes from 28 pairwise distances generated by only 8 independent runs; a U-statistic. **[S38] Under `method="higher"` it is the 27th of 28 order statistics.**
17. **[S38] The window-origin discontinuity (J)** — the screens place the probe at onset, the generator places it at `onset + start_offset_s`; a window from onset captures 43% of the probe. **Nothing in the codebase fixes the window origin** (`window_tensor` refuses a full run), so Protocol P's pin is effectively the pipeline's pre-registration and Gate 7 must reuse it. **[S40] The measured 2.37–3.64× is the ratio of TOTAL unmatched-row differences between two windows — NOT a fault-effect multiplier. The origin is retained on prospective grounds only.**
18. **[S38] The matched/unmatched asymmetry** — Stage A/B signal is seed-matched (noise cancels), Stage C null is not. Favours S. `TESTABLE` is therefore **necessary, not sufficient**; the unmatched secondary is a **conditional descriptive sensitivity, not a bound**.
19. **[S38] Task motion leaks into the synchronous statistic** — probe-free `t00` healthy `||b||` at 0.8 Hz is 0.48–0.51 µε, comparable to a mis-windowed probed run. The 0.8 Hz coefficient is not probe-specific; matched differencing is what makes it a fault statistic.
20. **[S39] The construction path (K)** — the closed loop is driven by a **C0** session and S gauges are produced **post-hoc** by replaying the privileged record. An "obvious" online-S construction is a different, untested instrument. Protocol P and the Gate-7 driver must both build/read by the verified path. **Positive result attached: ONE delivered row reproduces bit-for-bit from committed inputs (verified independently by both agents) — put this in the packet at that exact scope.**
21. **[S39] The unmatched-identity confound (L)** — delivered fault and healthy rows do not share `(sensor_seed, pair_id)`, so **every** delivered-row magnitude (privileged or observed) is `||fault + closed-loop divergence||`. Ratios over the same row pair are **not** clean either (S40, Codex pin D: different windows reduce different samples). Absolute magnitudes do not transfer to Protocol P's matched `D`.
22. **[S39] The observed path is nearly free on a matched difference** — 0.937×–1.148× of the privileged result, mean ≈0.996. A measured property; it moves either direction at small `D`.
23. **[NEW S40] The realized-vs-base identity distinction** — `ScenarioReservation.base_pair_id` is NOT the RNG key; `_generate_reservation` appends `_dataset0` unconditionally and that string is the identity. Any protocol, audit, join, or leak guard that names "pair_id" must say **which one**. My v2.2 leak guard was inverted by exactly this and would have passed a leak through.
24. **[NEW S40] The ramp fraction is unreachable through the assignment document** — `duration/2.0` is computed, not read. Any claim that the delivered ramp "could have been configured" is false; a code change was always required.
25. **[NEW S40] `Q95_c^gauge` and M2 are conditional healthy-null diagnostics only** — one fixed trace identifies no population decomposition, and components can interact or partially cancel. No mechanism attribution for a Case C.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** (`utils/rng.py:76-78`) — changing either field changes the stream; collapse requires reusing the SAME tuple. **Measured S39: a `pair_id` change alone moves `gauge_obs` by up to 6.50 µε**, against `D` values of order 0.1–0.5.
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path (privileged vs observed), the operation (single vs difference, matched vs unmatched), the construction (which session drives the loop, which produces the channel), *and the identity* (base vs realized). The SIGNAL it is compared against depends on excitation, task and plant.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**.
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. Full suite **399 tests green** (Codex re-ran S39). Set `PYTHONIOENCODING=utf-8`; use ASCII in probe scripts.
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`. **In my PowerShell tool the working directory is not the repo root — use `Set-Location` or absolute paths. My Bash tool's cwd PERSISTS between calls (a `cd` in one call carries to the next) — prefer absolute paths or re-`cd` every time.**
- **To import packet utils from a scratchpad probe:** `sys.path.insert(0, "<repo>/Reproducibility Packet/scripts")` then `from utils.X import Y`.
- **Timings (measured S35–S40):** full packet suite ~10 s; one MuJoCo rollout (3000 steps) **26.4–26.9 s**; a 200-realization sensor-only null at W=768 across 4 gauges ~40 s (no MuJoCo); reading 12 delivered plant traces ~5 s; a sliding-window harmonic profile over one 3000-step trace ~3 s; **an offline re-observation of one delivered plant trace ≈ instantaneous (no MuJoCo)**.
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — poll the results JSON, not the log.**
- **STANDING LESSON 1 — dry-run the analysis path before spending a rollout budget.** *(S39 and S40 were both entirely this.)*
- **STANDING LESSON 2 — self-audit from row artifacts / raw bytes, not the summary.**
- **STANDING LESSON 3 — restate a proxy in the contract's units before comparing to the bar.**
- **STANDING LESSON 4 — for a MuJoCo screen, re-run to scratch + diff against committed.**
- **STANDING LESSON 5 — verify the live git state before trusting continuity** (S28–S40: the startup snapshot lagged EVERY time, **thirteen running**).
- **STANDING LESSON 6 — review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
- **STANDING LESSON 7 — for any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.**
- **STANDING LESSON 8 — test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; report the scope you actually achieved.
- **STANDING LESSON 9 — a design review that reads the design cannot find what the design does.** Corollaries: **audit the yardstick before the artifact**; **before calling a settled parameter a defect, search the history for why it was chosen.**
- **STANDING LESSON 10 — a negative result is only readable if the same instrument produced a positive one.**
- **STANDING LESSON 11 (S35) — a threshold and the signal it judges must be measured in the SAME configuration; matching parameter names do not make two measurements comparable.**
- **STANDING LESSON 12 (S36) — when you import a number, import its definition, not its name.** Corollary: **two configuration errors can cancel, and that is dangerous rather than lucky.**
- **STANDING LESSON 13 (S36) — when a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** *(Applied six times now.)*
- **STANDING LESSON 14 (S36) — a pre-registered protocol must be executable by someone who did not write it.** **Corollary (S37, reconfirmed S38/S39/S40): the act of making it executable is itself the defect-finding technique.** Findings F, G, H, J, K, the label-stamp gap, and the leak-guard inversion all came out of pinning or building; none out of reviewing.
- **STANDING LESSON 15 (S36) — the cleanest statement of a negative is often a comparison you have not made yet.**
- **STANDING LESSON 16 (S37) — match the null to the OPERATION, not just to the configuration.** **And: common random numbers can void an entire class of threshold.**
- **STANDING LESSON 17 (S37) — compute the closed-form consequences of every gate you approve, before it costs anything.** Corollary: **check boundary cases for `<` vs `<=`.**
- **STANDING LESSON 18 (S37) — when the most likely branch creates a design problem, force the decision BEFORE the measurement that would make any fix look chosen.**
- **STANDING LESSON 19 (S38) — when you import a convention, import the CONFIGURATION THAT MAKES IT TRUE, and re-check each assumption.** Lessons 11/12 at increasing depth: window length → aggregation → operation → time origin → construction path → **realized identity (S40)**.
- **STANDING LESSON 20 (S38) — a guard that checks a NECESSARY condition will silently license the SUFFICIENT one.** *(Three instances now: S38, the S39 rank guard, the S40 leak-guard inversion.)*
- **STANDING LESSON 21 (S38) — check your own published claim against your own published table.**
- **STANDING LESSON 22 (S39) — a specification can be complete about the MEASUREMENT and silent about the INSTRUMENT.** Ask of any protocol: *does it say how to construct the thing it measures, or only what to do once it exists?*
- **STANDING LESSON 23 (S39) — two independent errors that point the SAME way are the dangerous case.** When auditing an estimate, check the *direction* of every error, not just its size.
- **STANDING LESSON 24 (S39) — cheap exact reproduction is a measurement instrument, not just a confidence check.** When something is deterministic, find out.
- **STANDING LESSON 25 (NEW, S40) — a guard's claimed scope must be tested against the construction that will actually run, not the one you had in mind.** A guard is a claim about a *specific* input distribution, and naming a construction changes that distribution. My leak guard was not mislabeled but **inverted**, because two things I had each written correctly in isolation disagreed at their seam. Corollary: **the cheapest regression test for an extension is the one behaviour the old code could already express** (ramp fraction 0.5 proves the seam is a superset).
- **PowerShell 5.1** primary (no ternary/`??`; **`^` is not a continuation — use a backtick or a single line**); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/` (line 19), `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `schema.json` to LF. **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked — correct). Verified S40; no change needed.

## Pointers

- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C, S36 D, S37 F, S38 J, S39 K/L and S40's narrowings beside it.**
- **The detection-floor record:** `Reproducibility Packet/results/synchronous_detection_floor/summary.json` — **`detect_threshold_microstrain` is a 5σ threshold, per gauge, at W=640, of a SINGLE window.**
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/` (reports corrected S35).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it** (task, score and controller untouched).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply. **Nothing else is blocked on the director.**
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S40 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32, **S40**). **NEXT DUE: MY SESSION 48.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-29**. **S40 added one running-log entry** (nine corrections accepted; the inverted leak guard; the seam built and verified). Codex's S39 entry narrowing my S39 headline to a one-row replay is **correct and undisputed**.
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**7,769 lines**; my S40 turn header at line 7,108, `+662/−0`; **`PROTOCOL_P_V2.3` is OPEN and Codex owns the next turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; unchanged in S40 — no recurrence; **streak six**).
- **Scratchpad (S40, NOT committed — recreate what you need):** `probe_s40_seam.py` (**the full seam prototype + all three verification classes — rebuild from the spec section above**), `append_turn.py` (**working** binary EOF-append with 4 gates + rollback, now `argparse`-driven: `--transcript --turn --header`), `turn_s40.md`.
