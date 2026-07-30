# Summary of Only Necessary Context — Claude

*Rewritten every session. Restores my working context for the next session. Excludes anything already in `Project Details/Project Details.md` and `AgentPrompt.md` (I re-read those in full at session start). Last rewritten: end of Session 45, 2026-07-29 19:40 PDT.*

## READ THIS FIRST — Protocol P lives in a file, not in this summary

```text
Reproducibility Packet/protocol/protocol-p-v2.3.3.md
canonical sha256   5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f
54,621 bytes, LF, no BOM, raw == canonical, pinned text eol=lf
JOINTLY APPROVED — Claude S43, Codex S43. The specification loop is CLOSED.
RE-VERIFIED BY MEASUREMENT in S45: the replay gate recomputes this digest at run time
and it matched. A permanent test now pins it too (see below), so drift fails loud.
```

**Read that file before doing anything on Protocol P. Do not reconstruct the protocol from this summary — this summary is deliberately not a second copy of it.** The spec contains the universe, the two hash domains, the terms block, the provenance scope, the seam (§3), the construction path (§4), the screen reservation (§5), the identity table (§6), the replay gate (§7), the window table, the statistic, Stages 0/A/B/C (§8), both secondaries, the outcome cases (§9), role coverage, the terminal branches, the fail-loud invariants I1–I12, I13a, I13b (§10), and the cost (§11).

**Version discipline — three versions deep. If this file ever needs correcting again, bump the version and `git mv`; do not edit in place.** v2.3.1 (`8c268f8f…401d76`) and v2.3.2 (`9d257017…738ba6e5`) are superseded, were each approved by me and blocked by Codex, and **neither was ever executed**. Their bytes are recoverable from the `Claude Session 41` / `Claude Session 42` commits. **A version bump now also has to update `PROTOCOL_FILENAME` and `PROTOCOL_CANONICAL_SHA256` in `scripts/protocol_p_replay_gate.py`** — the gate refuses a filename it was not approved for, which is deliberate.

## Where the project is

- **Phase 2 (Execution) is OPEN.** All Phase-1 gates in force. **Schema v1.0 + Amendment A1 in force.** Contract changes run through the **amendment protocol**.
- I am **Claude**; last session was **Session 45**; next session I run is **Session 46**.
- **`config.json` is deliberately NOT frozen** and does not exist. All hashes are `dev-`; no `dev-` trace may enter confirmatory analysis.
- Real data exists: `data/gate3-base-dev-pilot-val-c1-s` (3.86 GB, git-ignored, local only). 472 reservations / 944 manifest rows / C1+S / dev 152, pilot 152, val 168. **Test untouched: 0 identities, 0 payloads.** **Slated for full regeneration from zero after A2 — these 472 payloads become a superseded pre-amendment set in the packet exclusion trail. Read them; do not build on them.**

### THE REPLAY GATE RAN AND PASSED. A NEW LOOP IS OPEN AND CODEX OWNS THE NEXT TURN.

My S45 turn is at transcript line 9,340. I explicitly approved the exact bytes of two new files:

```text
Reproducibility Packet/scripts/protocol_p_replay_gate.py       (the executable §7 gate)
  raw sha256  02554cbe571f028e6271ce4a3128a64a42828a1bffb293eed28db61166f73fdb
  git blob    947d39d02104b79b03bca2a1a93b0e15fa6258e8     30,760 B, LF, no BOM

Reproducibility Packet/tests/test_protocol_p_replay_gate.py    (30 tests, 0.24 s)
  raw sha256  182145a42aaf99c30f8e7a1c637c7ced8b8c16b3a9b074b039d8b91580da9dbd
  git blob    887e4e784a1c3f8bf03c79c53ebdc07f4e27999e     14,283 B, LF, no BOM
```

**Do NOT run Stage 0 or Stage A/B/C, generate any Protocol-P identity, or compute any statistic until Codex reviews the replay evidence and approves an exact state.** Codex's S44 words: "Stage 0 and Stages A/B/C remain unauthorized until that replay result is reviewed."

**TWO QUESTIONS I HANDED CODEX IN S45:**
1. **`_plant_payload` is imported across the module boundary.** §4 pins `_generate_reservation`, so that import is specified; `_plant_payload` is not. I import it so the plant comparison *shares* production's serialization instead of agreeing with a second copy (the same reasoning that made the seam reuse `re_full_sha256`). Codex's file, Codex's private name, Codex's call: keep the shared import, or promote it to a public name?
2. **No skip-if-absent integration test for the gate itself.** I argued against one: it would skip on every clean checkout, and a test green-by-skipping everywhere except one machine reads as coverage while providing none (the S44 vacuous-test failure). The split I shipped is script-as-gate + portable comparator tests. Codex's call if it wants the integration test anyway.

Also flagged, not acted on: **`MIN_WATCHED_FILES = 100`** in the gate is a floor I chose rather than derived (the real snapshot is 3,119). Say if it should be derived.

### CODEX ANSWERED ALL THREE S44 QUESTIONS
1. **Keep the inactive-with-provenance raise.** It extends §3's fail-loud principle to a state the spec did not enumerate; unreachable in Protocol P and it prevents a caller believing a discarded provenance took effect.
2. **I13a and the §9 persistence-boundary test belong with the Stage driver.** My scope note was correct.
3. **Do NOT change `.gitattributes`.** Protocol P hashes no source file; the git blobs are the checkout-EOL-stable identifiers. **This answer also covers the two S45 files — do not pin them either.**

### CODEX'S ENUMERATED STAGE-DRIVER REQUIREMENTS — carry these verbatim
Before any Stage-A/B/C rollout, the driver review must show fail-loud coverage that:
- constructs the full `ScreenOverrides` bundle from an explicit condition;
- enforces I3 and suffix-free I4 rather than allowing the dataset fallback;
- enforces I5–I8 and I13a before the rollout;
- keys results from the explicit Protocol-P condition, never the stale returned label;
- persists no `ObservedRecord`, label payload, manifest, role index, or dataset payload; and
- **tests the actual results-only output root so the no-dataset-artifact check can fail on a real wrong write.**

- **Progress report DONE at S40** (regular, covered S33–S40). **Next regular: my Session 48.** Event triggers still stack: a phase transition, or an approved **written** amendment to the Claim Sheet (not approval of a protocol revision, not approval of an implementation state, not approval of a proposal text). None fired in S41–S45.

## Session 45 in one block — the gate, what it proved, and the report I had to fix

**Codex closed the seam loop** (S44), approving `assignment_generator.py` (blob `1c565888…`) and `test_assignment_generator_screen_overrides.py` (blob `2ec96c9f…`) at exact state, independently reproducing every measurement, and authorizing **only** the one-row replay gate.

**I built `scripts/protocol_p_replay_gate.py` and ran it. It PASSED.** Exact evidence, as posted:

```text
I1   protocol      54,621 B  5689dad7…bdf421f   canonical text; raw == canonical
     assignment    22,760 B  76255a80…3514ae    canonical text; raw == canonical
     plant ref  3,176,122 B  ed5b1f39…b65e45    RAW bytes (18 CRLF pairs inside)
     obs ref      929,068 B  cdde17f6…bb4c83    RAW bytes ( 1 CRLF pair  inside)
     domain diagnostic reproduced §0's two text-folded digests exactly
I2   plant        20/20 fields equal   observation  38/38 entries equal
     531 NaNs matched position for position, across 5 entries
identity  all 20 manifest fields equal; base config hash stamped per §0
ephemerality  3,119 files watched across 15 roots; 0 added / 0 modified / 0 removed
cost  26.37 s (and 25.58 s on the first of two runs) — both 58/58
```

**THE FINDING — the gate is also a bit-level regression test on the S44 seam.** The two pinned references were generated **2026-07-24**, five days and one patch before this run, so they predate the seam entirely. Codex verified the `overrides=None` branch by tracing it against the parent source. The replay says the same thing **by measurement, through the whole stack**: every float across 3,000 MuJoCo steps and all 531 NaN positions are unchanged. **A source review can establish a branch is not taken; only this establishes that nothing downstream of it moved.** Reuse this: any future patch to the generator can be regression-checked for free by re-running the gate.

**Two smaller measured properties.** (a) Production observed `("C1","S")` in one call; §4 pins `("S",)` and my replay observed **S alone** and still reproduced exactly — `SensorModel.observe` carries **no state across suites**, so CRN keying really is `(sensor_seed, pair_id, channel, stream)` and nothing else. (b) Contact steps 0 on a `contact_dev_brief` reservation — consistent with S33 Finding 2 (dev 0/76 touched), recorded so the zero is not read as a surprise.

**THE DEFECT I INTRODUCED AND REMOVED.** My first ephemerality check printed `added 0 / modified 0 / removed 0` — true, and **indistinguishable from a check that watched nothing**. Not a test that cannot go red; a *report* that cannot be told apart from a vacuous one, so the reader cannot even ask. Fixed twice over: the report prints its denominator (`watched 3,119 files across 15 roots`) and `inventory()` **raises** below `MIN_WATCHED_FILES`. Both states tested. Cost: one extra 26 s run, because the evidence handed to a reviewer must come from the committed bytes.

**Verification before trusting the gate: 21 injected-defect cases against the REAL retained payloads, 19 defects + 2 controls, all 21 behaved as required.** Caught: 1-ULP moves (plant and observed), NaN→number, number→NaN, float64→float32, truncated array, `config_hash` swapped for a screen hash, missing key, extra key, wrong entry count, wrong binary file in a pinned slot, protocol filename drift, identity field drift, identity field-set drift. **The NaN pair is load-bearing: `values__gauge_obs` carries 531 real dropout/latency NaNs, so the comparison MUST treat matched NaN positions as equal or it fails a correct replay — and making it NaN-tolerant is exactly how it could become NaN-blind.**

**The permanent test file is the portable form of that sweep** — synthetic payloads, no dependence on the git-ignored references. Beyond re-covering the comparators it: binds `N_PRIVILEGED_FIELDS` to `dataclasses.fields(PrivilegedRecord)` and `N_OBSERVATION_ENTRIES` to `5*len(CHANNEL_NAMES)+8` (schema growth fails loud instead of silently comparing 20 of 21); **checks the committed protocol and assignment files against their approved digests, making "the pre-registration has not drifted" a permanent automated check**; and covers the binary/text domain split by its *property* on a synthetic file so it is portable.

**One test-writing note:** my first filename-drift test failed with the *wrong* error — the absence guard fires before the filename guard, so placeholder paths tripped absence first. Give the binary slots real files when testing a later guard.

**Verified in S45 (do not re-do):** all four pinned digests; both §0 text-folded diagnostics and the 18/1 CRLF pair counts; the two new files pure LF, no BOM, `text/eol: unspecified` (correct per Codex's answer); focused gate tests **30 passed 0.24 s**; packet suite **472 passed 11.21 s**; the 21-case injection sweep; Codex's S44 append `+129/−0`, header once at 9,211, Codex physically last (**STREAK ELEVEN**); my S45 append `+230/−0`, header once at 9,340, 4/4 gates; transcript now **9,566 lines**. **Protocol-P rollouts spent: ONE — exactly the one authorized.**

## Scratchpad (S45, NOT committed)

`append_turn.py` (the 4-gate binary EOF appender — `--transcript --turn --header --repo`; **copied forward from S44's session dir and reused unchanged**), `turn_s45.md`, `probe_s45_refs.py` (npz key/manifest probe), `verify_s45_gate_catches_defects.py` (the 21-case sweep — **rebuild this for any future patch or gate review; it is the technique that found D5 in S44 and that validated the gate here**). **Scratchpads live under `…/Temp/claude/C--Users-…/<session-uuid>/scratchpad/` and DO NOT RELIABLY SURVIVE. Check `ls -lt */scratchpad/append_turn.py` before rebuilding it — it has survived the last three sessions.**

## The escalation trigger — content-based, and it has now held twice

**The binding rule: escalate to the director when a round re-litigates a point already settled, or when we disagree on a judgment neither of us can resolve from source — NOT when a round finds a new, verifiable defect.** The protocol-specification loop ran seven rounds and closed at Codex's S43 approval; every round found something new, none repeated. **The seam-implementation loop closed in ONE round** (my S44 handoff → Codex's S44 approval). **A third loop is now open on the replay gate; my S45 handoff is round one.** The rule carries over unchanged: if a round repeats a settled point — the two-domain hashing split, the window origin, the statistic, the ladder, the driver-vs-seam scope boundary — escalate on the spot regardless of count.

## HONEST ODDS — unchanged since S40

Against the S39 gauge-only measurement's bar, projecting the S35 amplitude ratio ×3.15 over 0.05 → 0.15 N (**importing that ratio across configurations remains the weakest link — the exact Lesson-11/12 move**):

```text
remEI 0.50   c4 1.502 vs 0.711 x2.11    remEI 0.75   c4 0.491 vs 0.711 x0.69
             c5 1.475 vs 0.850 x1.74                 c5 0.470 vs 0.850 x0.55
             c6 0.856 vs 0.635 x1.35                 c6 0.315 vs 0.635 x0.50
             c7 0.853 vs 0.771 x1.11                 c7 0.294 vs 0.771 x0.38
```

**remEI 0.75 fails everywhere by a wide margin — the one robust statement.** remEI 0.50 clears the binding cell by only **1.11×**, computed with an **inflated signal** (Finding L) against a **deflated bar** (the gauge-only decomposition omits closed-loop divergence) — both errors favour the hypothesis. **Case B (dev coverage 1) and Case C remain roughly comparable.** Stage C settles it.

**The success bar is UNTOUCHED** (≥0.05 macro-F1, −0.02 per-class recall non-inferiority, ≥10% tracking reduction, paired hierarchical bootstrap, ≥5 seeds).

*Naming note: "M2" is **retired inside the protocol file**, where it was ambiguous. Below it still labels **my** S39 measurement — the gauge-path-only decomposition. Keep the two straight; if writing anything Codex will read, spell it out.*

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
**A decomposition, NOT a bound.** It **validates Stage 0** (synthetic no-plant ~0.39 sits inside the real-plant 0.318–0.425 — written into spec §8) and identifies **cell 7 (payload + warm + contact) as the binding cell**. **Conditional healthy-null diagnostic only — no mechanism attribution.**

**The enabling tool (S39, reconfirmed S40/S41/S45).** `SensorModel().observe(delivered_plant, "S", pair_id=<manifest>, sensor_seed=<manifest>)` reproduces the delivered row **bit-for-bit with no MuJoCo**; a perturbed `pair_id` moves `gauge_obs` by up to **6.50 µε** (against `D` of order 0.1–0.5). **Any stored plant trace can be re-drawn on the observed path at any identity for free.** S45 extended this: the whole rollout, plant included, also reproduces exactly.

## GATE STATUS — the freeze path (central reference)

**Governing decision: `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`.** A **versioned DRAFT config** governs dev/val generation; the **final immutable `config.json` freeze comes AFTER model implementation + validation-only hyperparameter/threshold selection and BEFORE any untouched `test` payload.**

1. **Machine schema + config authority** — **DONE, APPROVED S28.** *(Codex/shared.)*
2. **Role-separated storage, deployable loader, leakage/split audits** — foundation DONE (S28), role-write DONE (S29), **real generator + base roles APPROVED (my S33)**, **generator hardening APPROVED (my S34)**. **STILL OPEN OVERALL:** `estimator_outputs` + `controller_logs` roles await the Gate-4 fits. *(Codex/shared.)*
3. **Multi-setting design + manifest** — was CLOSED at 808 reservations; **A2 reopens it** (full regeneration, new assignment, new hash). *(shared)*
4. **Matched learned models** — **MINE. GATED BY Protocol P v2.3.3, then the written A2.** `TemporalAttributionNet` + `RMALatentEncoder` behind shared `[W,D]`; within-suite capacity ladder; ≥5 seeds; identical protocol IDs across C0/C1/S. Toolchain verified (torch cu128 / sm_120).
5. **Calibration/abstention/OOD/uncertainty** — **MINE.** Per-suite calibrated probs (Brier/NLL/ECE), abstention + OOD thresholds on validation, `severity_uncertainty` as a **bias-inclusive predictive error scale** (NOT in-sample residual dispersion — S24: understates true by 5.72× for S). **Validation must NOT be touched until Gate 4 opens.**
6. **Confirmatory controller protocol** — **DECIDED S27 (both agents):** freeze the fair four-arm comparison (no-action/detection-only · transparent attribution-driven · RMA · oracle) and **RUN the pre-registered paired C1-vs-S comparison**; do NOT narrow to information-only, do NOT retune blocked families post-hoc. *(Codex owns controller; diagnosis→control seam shared.)*
7. **Evaluation driver + confirmatory manifest** — **MINE.** One CLI owning the `[t_c,t_c+5s]` slice, role joins, paired C1/S table, exclusions, CIs; rejects `dev-`/wrong-hash/cross-role/incomplete-pair/truncated. **Must implement pre-registered statements:** (a) `ood_flag` exclusion from known-class metrics; (b) the **degradation-ladder rule** (S30/S31); (c) **pilot→val moves one variable while val→test additionally moves half-fraction → complete factorial** — *and, under A2 pin 4, no longer moves the contact window*; (d) S33's two findings; (e) the mild-stratum development diagnostic **at its true scope** (dev contexts, EI 0.75/0.50) and the per-channel attribution; (f) **[S35]** the excitation discontinuity; (g) **[S36]** the yardstick discontinuity (D) + the run-to-run range statement (E) + trajectory-partial margin coverage; (h) **[S37]** the operation mismatch (F), thermal near-invariance (G) as a *property*, the amplitude ceiling (H); (i) **[S38]** the **window origin (J)** — the driver MUST use the same origin the protocol pins, since nothing in the codebase fixes it; plus the matched/unmatched asymmetry and role-coverage counts; (j) **[S39]** the **construction path (K)** — build/read records by the same C0-loop-then-post-hoc-observe path — and the **unmatched-identity confound (L)**, which governs how any delivered-row magnitude may be quoted; (k) **[S40]** if the seam ships, the driver must distinguish **`base_pair_id` from realized `pair_id`** in every identity join and audit, and must never stamp an overridden run with the base config hash; (l) **[S41]** any file whose **raw bytes** enter an identity or a verification pin must be hashed through the correct-domain helper; (m) **[S42]** and that helper must be chosen **by file domain** — text files fold CRLF, binary files never do; any driver-side byte pin must name its domain explicitly; (n) **[S43]** every identity expression in the driver must **name the object it hashes**, and the recorded canonical string must be the *same object* that was hashed; (o) **[S44]** the driver must be tested for the **wires between its stages**, not only for each stage's own behaviour — a unit test that supplies the input a caller is supposed to supply proves the callee works and says nothing about whether the caller ever calls it that way; (p) **[NEW S45]** every driver check that reports a clean result must **disclose its denominator** — how many objects it examined — and must refuse to report at all when that denominator cannot support the claim. A driver that prints "0 leaked identities" or "0 stray artifacts" without saying how many it looked at is indistinguishable from one that looked at none.

**Order:** (1)✓ → (2 foundation)✓ → (2 role-write)✓ → (3 assignment)✓✓ → (2 generator + base roles)✓✓ → (2 hardening)✓✓ → (dev separability check)✓ **[NEGATIVE]** → Protocol P v2.3.3 spec ✓✓ **[JOINTLY APPROVED]** → seam patch + 37 tests ✓✓ **[JOINTLY APPROVED, Codex S44]** → **replay gate RUN AND PASSED; gate implementation posted [I APPROVED; CODEX OWNS THE TURN] ← WE ARE HERE** → Stage 0 → Stage A/B/C → Codex reviews implementation + result + branch → written amendment + replacement assignment (both approve) → **full regeneration from zero** → re-audit → (4/5 models+calibration) [me] → (2 remaining roles) [Codex] → (6 controller + sample-size) [shared] → **joint immutable freeze** → one-shot confirmatory generation + eval (7) → Phase 3.

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
- **Generated with `splits=("dev","pilot","val")`, `suites=("C1","S")`** — pass these explicitly to `build_identity_manifest`, whose *default* suites are `("C0","C1","S")` and which **requires `{"C1","S"} ⊆ suites`**. `_generate_reservation` has no such constraint and accepts `("S",)`, which is what §4 pins.
- **Manifest columns** (= `IdentityManifestRow` fields, 20): `schema_version, config_hash, scenario_spec_id, pair_id, run_id, trajectory_spec_id, fault_setting_id, split_group_id, split, suite, estimator_id, controller_id, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed, train_seed`. **Note `trajectory_spec_id`, not `trajectory_id`; `fault_setting_id`, not `source_class`. `pair_id` here is the REALIZED id (with `_dataset0`), not `base_pair_id`.**
- **`run_id` carries the suite:** `scenario_dev_t01_f000_r00_S_dataset0`. The **plant** role is stored per suite too (C1 and S share a byte-identical payload — documented duplication), so a plant path is `plant/{run_id}.npz` with the suite suffix included.
- **Load one observation:** `ObservedRecord.load_npz(root/"observations"/suite/f"{run_id}.npz")`. Fields: `suite, run_id, pair_id, config_hash, values, valid_mask, measurement_time_s, availability_time_s, latency_age_s, suite_available_mask, schema_version, split`. **`values` and `valid_mask` are DICTs** channel → `[T, width]`. **`measurement_time_s` / `availability_time_s` / `latency_age_s` are DICTs of RANK-1 `[T]` arrays.** Gauges are `values["gauge_obs"]` `[T,4]`. **`config_hash` is a STORED field — what gets stamped changes the artifact's bytes (this is why the replay must stamp base).**
- **`ObservedRecord.to_npz_dict()` is the 38-entry serializer** (8 metadata + 5 per-channel dicts × 6 channels). npz keys are prefixed: `values__`, `valid__`, `meas_time__`, `avail_time__`, `latency__`. **`_plant_payload(record)` in the generator is the 20-key plant serializer** — use it rather than re-deriving from `dataclasses.fields`, so a comparison shares production's path.
- **Load one plant trace:** `PrivilegedRecord.load_npz(root/"plant"/f"{run_id}.npz")` (`utils.schema_types`).
- **Re-observe any plant trace offline, NO MuJoCo:** `SensorModel().observe(plant, "S", pair_id=..., sensor_seed=..., fault=None, run_id=..., config_hash=..., split=...)` — verified bit-identical at the manifest identity (S39/S40) and confirmed suite-order-independent (S45).
- **These `.npz` are ZIP archives and DO contain CRLF byte pairs as payload (18 and 1 in the two pinned replay references — re-measured S45). Never hash one through a text canonicalizer.**
- **Plant fields (20):** step, t_s, q_true, qd_true, qdd_true, tau_cmd, tau_delivered_true, deform_coords[90], curvature_true[4], gauge_true[4], imu_true[6], temperature_true[4], contact_state[2], task_reference, true_task_output, tracking_error, tracking_error_norm, control_effort, saturation_flag[2], safety_flag[7]. **`contact_state[:,0]` = summed force N, `[:,1]` = active flag.**
- **Registry D = 18:** q_obs[2], qd_obs[2], tau_cmd[2], current_proxy_obs[2], imu_obs[6], gauge_obs[4]. **C1's `gauge_obs` is all-NaN, mask False. S `gauge_obs` CONTAINS NaNs (dropout/latency) — use nan-aware statistics.** Measured S45 on one delivered S row: **531 NaN values across 5 of the 38 entries.**
- **Label fields:** source_class, subtype, location, severity, onset_index, onset_time_s, compound_flag, ood_flag.
- **Run lengths / timing:** `trajectory_dev_ordinary_a` (`t00`) 2900 steps, onset 400, **no probe**; `trajectory_dev_diagnostic_b` (`t01`) 3000 steps, onset 500, **probe steps 1000→1625**. Both carry 76 rows per suite. **Only `t01` has a probe.**
- **`assignment["trajectory_specs"]` is a LIST of dicts keyed by `"id"`, not a dict** (`_catalog()` builds the mapping). Same for `context_profiles`, whose keys are `payloads` / `environments` / `contacts`.
- **dev fault settings (t01):** `fault_dev_healthy` (f000); `fault_dev_structure_link_stiffness_loss_loc1_sev0p5` (f001); `..._sev0p75` (f002); then actuator loc0/loc1 × {0.5,0.75}; then sensor bias/drift/dropout × loc{0,1} × 2 sev. **Severity strings use `sev0p05`, not `sev0p5`, for 0.05 — query the assignment, do not recall it.**
- **The replayed reference row:** `scenario_dev_t01_f000_r00` → `pair_id basepair_dev_t01_f000_r00_dataset0`, `run_id scenario_dev_t01_f000_r00_S_dataset0`, `sim/fault/sensor/controller = 110760/110761/110762/110763`, `payload_dev_nominal`, `env_dev_iso25c`, `contact_dev_brief`, `fault_dev_healthy`, 3000 steps, 0 safety events, **0 contact steps**.
- **Two runs in the same context cell differ in sensor_seed, and the closed loop amplifies that into gauge variation that EXCEEDS the structural fault signature (S36 Finding E).** Any fault-effect *magnitude* measurement MUST match both `sensor_seed` AND realized `pair_id`. Separability measurement must NOT (that is the point). **Delivered fault and healthy rows do NOT share identity (S39 Finding L) — so any delivered-row magnitude is `||fault + divergence||`, on BOTH the privileged and observed paths.**

## Codex's Gate-1/2/3 layer — reference

`Reproducibility Packet/`:
- **`schema/schema.json`** (S28) — machine schema v1.0 + A1. Roles: identity_manifest, plant (20 fields = `PrivilegedRecord`), observations (deployable, fixed 6-channel registry + static suite mask), labels (8), estimator_outputs (9), controller_logs (6). `schema_sha256 = 0dae0dd0fec4269180139efc9a4c9ce38e7f8f23d890d182dc8eb063803e942f` (LF-pinned via root `.gitattributes`).
- **A1 safety envelope (schema-v1.0.md §Amendment A1):** `|q| ≤ π rad`, `|qd| ≤ 10 rad/s`, tip radius ≤ 0.82 m, `|gauge_true| ≤ 500 µε`, tip contact force ≤ 5 N; `safety_flag[T,7]` fixed order (joint_angle_0/1, joint_speed_0/1, tip_workspace, gauge_abs, tip_contact_force) computed in `cable_plant.py:_safety_flags` (line 272, called 377); `saturation_flag[T,2]` separate. Computed from privileged truth, never from a corrupted observed channel.
- **`config/draft-config-v0.1.json`** — the DRAFT, **CRLF in the working tree**. **`config_hash = dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56`** (parent `dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180`), computed over `canonical_json_bytes(document)` so it is EOL-immune — **which is exactly why it is deliberately NOT byte-pinned**. Embedded assignment hash at `/values/scenario_manifest/approved_assignment_hash`. Frozen candidates: plant (`n_def=90`, gauges [0.25,0.75], A1 thresholds, `point_count_per_link=17`, `simulation_timestep_s=1e-4`, `endpoint_contact_plane_z_m=0.2`), timing (`f_ctrl=500`, `control_dt_s=0.002`, `window_steps=768`, `stride=16`, **probe 0.05 N / 0.8 Hz / 1 cyc raised_cosine — RAMP UNPINNED, S35 Finding A**, `analysis_window_s=5.0`), sensor_model (**gauge noise 1.0 µε, thermal 10 µε/°C, ref 25 °C, bias 0.5 µε, drift 0.2 µε/√s, hysteresis 0.15, quant 0.5 µε, latency 0.002 s**).
- **`config/proposed-gate3-assignment-v0.1.json`** — **LF-pinned (S41)**. Canonical/raw SHA-256 `76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae` (22,760 bytes; independently reproduced by Codex S42 and by the replay gate S45); **its CRLF rendering is `00dacaf6277d6b274e3690ab3d3f68607eb61a22fe0df75ea8688fe4c7d4f87f`** — always hash through `canonical_text_sha256`. `assignment_hash = dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1`. Top keys include `trajectory_specs`, `fault_grid_by_split`, `compound_ood_settings`, `context_profiles`, `generation_plan`. **Superseded, never approve:** `dev-70832daa…765de` (656) and `dev-5939ff5f…0cedb` (blocked S30). Probe `start_offset_s` per split: **dev 1.0, pilot 1.2, val 0.9, test 1.1 — offsets FROM ONSET (Finding J).**
- **`scripts/utils/assignment_binding.py`** — `embed_approved_assignment_document` / `validate_approved_assignment_binding(config, *, expected_assignment)` — **`expected_assignment` is REQUIRED.** `AUTHORIZED_RESEARCH_SPLITS = ("dev","pilot","val")`.
- **`scripts/utils/assignment_generator.py`** — `RESEARCH_SPLITS=("dev","pilot","val")`, `BASE_DATASET_SUITES=("C0","C1","S")`; `GenerationRuntimeParameters(control_dt_s, f_ctrl_hz, simulation_timestep_s, point_count)` + `_runtime_parameters(binding)`; **the S44 seam at the top: `ScreenOverrides` (frozen, 5 fields, `is_active()`), `screen_pair_id` (105), `_screen_stamped_hash` (122)**; `_step_index` (217) fails loud off-grid; `build_identity_manifest` (261) — **requires `{"C1","S"} ⊆ suites`**; **`audit_manifest_against_assignment` (321) — the two tested leak tripwires**; `_profile` (382), **`_physical_config` (401; `overrides=`; the ramp default `duration/2.0`)**, `_temperature_function` (474), `_fault_components` (500), `shared_channels_equal` (542), `preflight_assigned_mechanics` (560), **`_plant_payload` (600) — the 20-key plant serializer**, **`_generate_reservation` (607; 7 positional + keyword-only `overrides`; RETURNS a 6-tuple `(control_pair_id, result.plant, observations, label_payload, safety_count, contact_count)` — the CablePlant is NOT returned)**, `materialize_base_dataset` (731), `audit_materialized_base_dataset` (838). `ESTIMATOR_ID="gate4_unfit_shared_capacity_v1"`, `CONTROLLER_ID="bounded_observed_pd_no_recovery_v1"`, `DATASET_IDENTITY_TRAIN_SEED=0`.
- **`scripts/utils/gate3_assignment.py`** — `load_assignment`; `expand_reservations(document)` → `list[ScenarioReservation]` (fields: schema_version, draft_config_hash, scenario_spec_id, base_pair_id, trajectory_spec_id, fault_setting_id, split_group_id, split, payload_id, env_profile_id, contact_profile_id, sim_seed, fault_seed, sensor_seed, controller_seed). **Lines 648-697** are the seed/ordinal/context-cell derivation: `seed = seed_base + 10*ordinal`, `sim/fault/sensor/controller = seed+0/1/2/3`, `base_pair_id = basepair_{split}_t{ti:02d}_f{fi:03d}_r{rr:02d}`, realized dataset `pair_id = base + "_dataset0"`. Ordinal nests (trajectory, fault, replicate), resets per split.
- **`scripts/utils/storage_contract.py`** — `IdentityManifestRow` (20 fields), `IDENTITY_MANIFEST_FIELDS`, `DeployableObservationLoader`, **`_valid_config_hash` (103-109) strips exactly `dev-` then `re_full_sha256` (364-367) requires 64 lowercase hex.**
- **`utils/config_contract.py`: loader is `load_config(config_path, schema_path, *, require_frozen=False)`.** `ValidatedConfig`: `source_path, schema_path, document, config_hash, status`. `file_sha256` (45) is a **RAW-byte** hash — do not use it on an unpinned text file; `canonical_json_bytes` (78) + `sort_keys`/`separators`/`ensure_ascii=False`/**`allow_nan=False`** is the document path and the canonical-JSON precedent Protocol P matches; `config_hash` at 99.
- **`utils/sensor_model.py`** — `config_hash` is **free-form provenance, never validated** (`:235, :253, :612, :641`), which is what makes the derived screen-provenance stamp safe. Temperature reaches the gauges at `:423-424` (10 µε/°C); the 0.5 µε quantizer is at `:429-431`. **Carries no state across `observe` calls (measured S45).**
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
- **`utils/synchronous.py`** (Codex, S9) — `harmonic_coefficients(window, valid, time_s, frequency_hz)` returns `[cos, sin]` from a **least-squares fit with intercept + centred linear trend** (design `[ones, centered_time, cos, sin]`); `harmonic_amplitude` is the L2 norm of that **single-channel** pair. Requires ≥5 finite valid samples; fails loud on rank deficiency or non-increasing time. **Because `[ones, centered_time]` span a linear-in-time thermal ramp, such a ramp contributes exactly zero to `(cos,sin)` in exact arithmetic — quantization is what breaks it (S38 correction to Finding G).**
- **`utils/metrics.py` + `utils/stats.py`** (approved through S11): `tracking_reduction_pct`, `j_5s` fail-loud on full `[t_c,t_c+5s]`, `safety_incident_rate`, `safety_flag_rates`, `safety_regression_delta`, `hierarchical_bootstrap_ci` (crossed pair×seed). **Eval driver (Gate 7) — build once the frozen layout exists.**
- **Screens (all closed):** `screen_severity_estimation_quality.py`, `screen_severity_action_boundary.py`, `screen_actuator_probability_channel.py`, `tests/test_recovery_seam.py`, **`screen_structural_separability.py` (S34, report corrected S35; now packet-README Step 22)**.
- **`analyze_synchronous_detection_floor.py`** — mine, and carries **two** usage corrections. Publishes `detect_threshold_microstrain = nes_mean + 5*nes_std`, **per gauge**, at `--window 640`, `--thermal-ramp-c 3.0`, 200 realizations, `--seed 0`, `pair_id=1` hard-coded at line 183. **It is a threshold, not a floor (S36); and it is the null of a SINGLE window, not of a difference (S37).**
- **Mine, Codex reviews: `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`** — the pre-registration artifact. Also mine to maintain: the **two-domain hashing convention** in its §0 and Corrections 3/4, the `CANONICAL_JSON` rule in Correction 2, and the **identifier-binding discipline** in Correction 8.
- **Co-owned with Codex (S43): `tests/test_cable_plant_softening_boundary.py`** — the permanent I13b guard. I wrote it; it tests **Codex's** plant contract and Codex approved both its location and its exact state, so **Codex's call if the two ever conflict.** 6 tests, 0.59 s.
- **The S44 seam inside Codex's file: `scripts/utils/assignment_generator.py` + `tests/test_assignment_generator_screen_overrides.py` (37 tests).** **APPROVED AT EXACT STATE BY CODEX (S44).** I own the seam implementation; Codex owns the file. Blobs `1c565888…` and `2ec96c9f…`.
- **NEW (S45), mine: `scripts/protocol_p_replay_gate.py` + `tests/test_protocol_p_replay_gate.py` (30 tests).** The executable §7 gate and its portable comparison-layer tests. **AWAITING CODEX'S REVIEW.** Public API worth knowing: `canonical_text_sha256`, `raw_file_sha256`, `check_pinned_digests`, `load_npz_entries`, `compare_entry`, `compare_payload`, `compare_manifest_row`, `inventory`, `diff_inventory`, `read_manifest_row`, `run_replay`, `ProtocolPError`, `MIN_WATCHED_FILES`. **Re-run it after any generator change — it is a free bit-level regression test on the ordinary path.**
- **Also mine now: packet README Steps 22 and 23.** `scripts/embed_approved_assignment.py` remains the one undocumented packet script; it is Codex's and I flagged it rather than editing it.
- **Not yet built (Protocol P, after Codex approves the gate):** `screen_physical_faults` + the I13a runtime check (driver-side, per Codex's S44 answer); `scripts/analyze_synchronous_difference_null.py` → `results/protocol_p/sensor_only_difference_null.json` (Stage 0); the Stage A/B/C driver; and the §9 label-stamp scope-condition test, which Codex agreed belongs with that driver.

## Codex's OTHER lanes — current state

- `utils/cable_mechanics.py` — `CableModelConfig`: `link_length_m=0.40`, `link_thickness_m=0.004`, `distal_payload_mass_kg`, optional absolute `endpoint_contact_window_s`, `diagnostic_tip_load_{peak_n,frequency_hz,start_s,duration_s,ramp_s}`; `structural_ei_remaining` default **0.50**; `control_dt_s` default **0.002**; `endpoint_contact_plane_z_m` default 0.498 (assignment uses 0.2). **`diagnostic_tip_load_envelope` (`:444-454`) requires the ramp finite and ≥0, requires a duration if non-zero, and raises when `ramp > duration/2` → admissible fraction `(0, 0.5]`.** Probe local time is `time_s - diagnostic_tip_load_start_s` (466, 488).
- `utils/cable_plant.py` — `CablePlant(config, *, point_count=17, simulation_timestep_s=1e-4, fault=None, additional_faults=())`; scheduled contact; compound physical faults. **No RNG anywhere in the file (verified S37)** — which is why S41's gate measurement is identity-independent. **A structural fault does `dataclasses.replace(config, structural_ei_remaining=severity)` → `self._physical_config` (`:99-103`) and builds a SECOND softened MuJoCo model at `:118-121`; the healthy plant has `_soft_model is None`. `_softened` initialized False at `:117`, set True in `_activate_structural_fault_if_needed` (`:186-198`), which is called from `advance` at `:328` BEFORE the physics step and BEFORE `_step_index += 1` at `:405`. `_fault_active` (`:179-184`): `onset = max(int(fault.onset_index), 0); return self._step_index >= onset`.** The `structural_ei_remaining=0.50` dataclass default is INERT in the healthy branch — do not quote it as a healthy stiffness (S40). Fault severity **is** the remaining-EI fraction. **`cable_plant.py:124-125` restricts structural faults to location `{-1,1}` and severity to `(0,1]`** (verified S30 — a genuine plant constraint; do not re-litigate). Actuator severity = remaining gain fraction, location = joint index; applied at `:333-336`. **`rollout(n)` cannot be called twice on one plant** — `PrivilegedRecord`'s validator requires a contiguous 0-based step grid (S43).
- **`utils/schema_types.py`** — `N_JOINTS = 2` (line 38); `FaultSpec` (65-79): `source_class="healthy", subtype="none", location=-1, severity=0.0, **onset_index=-1**, compound_flag=False, ood_flag=False`. **That `-1` default is the S41 defect's origin, and is now pinned as behaviour by the S43 test.** `PrivilegedRecord` (123; 20 fields; `save_npz` 284, `load_npz` 297), `ObservedRecord` (`to_npz_dict` 443, `save_npz` 466, `from_npz_dict` 474, `load_npz` 496).
- `utils/task_control.py`: `BoundedTaskProfile`, `ObservedJointPDController` — **`proportional_gain=(0.05,0.03)`, `derivative_gain=(0.005,0.003)`, `torque_abs_limit=(0.20,0.10)`**; reads ONLY `q_obs`/`qd_obs`. (`torque_abs_limit[0]=0.20` is what makes Finding H's 0.15 N ceiling.)
- `utils/recovery_control.py` — `GainScheduledRecoveryController`; `screen_actuator_recovery_action.py` (S25) → `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`; `screen_structural_recovery_action.py` (S20) → `BLOCK_STRUCTURAL_RECOVERY_ACTION_FAMILY`; `screen_fault_tracking_deficit.py` (S22); `run_bounded_noisy_information_review.py` (S19): S macro-F1 0.995 / C1 0.704.
- **`screen_synchronous_safe_probe.py`** — loads `window_samples` AND `detect_threshold_microstrain` from the floor summary JSON, so it is **internally coherent** (W=640, per-gauge, max-across-gauges). `--ramp-period-fraction` default **0.125**; **`--peak-loads-n` default `[0.05, 0.1, 0.15]`**; `--fault-onset-s` default 1.0 and it slices `post[:window_samples]` from onset — **correct there, because this screen puts the probe AT onset (Finding J)**. It measures the **privileged** `gauge_microstrain` difference, not the observed path.
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
7. **[S33] Finding 2 (contact), non-blocking.** 236 runs assigned a contact profile; **11 actually touched** (4.7%) — dev 0/76, pilot 11/76, val 0/84. All 11 are encoder **bias (7) or drift (4)**; 0 dropout/actuator/structure/healthy. Mechanism: bias/drift corrupt measured angle → observed-PD overdrives → tip descends. **Realized contact is an EFFECT OF THE FAULT**, peak 2.6–3.0 N, loudest in the S-exclusive gauge channel — direction **favours S**. `I(fault; assigned contact label)` = 0 exactly; `I(fault; contact actually occurring)` is not. Addressed by A2 pin 4. **Re-confirmed S45 on the replayed dev row: 0 contact steps despite `contact_dev_brief`.**
8. **[S34] The mild-stratum development diagnostic** — at dev EI 0.75/0.50 neither suite separates structure; no gauge column significant; the only consistent structural signature is a C1 IMU channel. **State at that scope only.**
9. **[S35] The excitation discontinuity** — the delivered probe is ~5.8× weaker than the screen that justified its amplitude, because the ramp was never pinned in config.
10. **[S36] The yardstick discontinuity (D)** — a per-gauge five-sigma threshold at W=640 applied to a four-gauge statistic at W=768; error 7.7%, direction lax.
11. **[S36] The run-to-run range statement (E)** — delivered fault−healthy gauge differences fall inside the range spanned by fault-free healthy pairs. **Report as a range statement, never as a test.**
12. **[S36] Margin coverage is trajectory-partial** — the rule certifies only diagnostic-trajectory rows; ordinary-trajectory structural rows stay in the estimand, **not certified by the diagnostic margin**.
13. **[S37] The operation mismatch (F)** — a threshold measured on a single window applied to a difference of two; and **a matched-seed difference admits no sensor-only threshold at all** because CRN cancels the sensor term.
14. **[S37→S38 CORRECTED] Thermal near-invariance (G)** — a *property*, not a defect: `D`'s null is essentially unchanged across 0–3 °C per-window excursion. **NOT exact cancellation** — thermal enters inside the 0.5 µε quantizer.
15. **[S37] The amplitude ceiling (H)** — the probe could not be strengthened past 0.15 N without violating an approved actuator-authority limit.
16. **[S37] Stage-C null dependence** — `Q95_c` comes from 28 pairwise distances generated by only 8 independent runs; a U-statistic. **[S38] Under `method="higher"` it is the 27th of 28 order statistics.**
17. **[S38] The window-origin discontinuity (J)** — the screens place the probe at onset, the generator places it at `onset + start_offset_s`; a window from onset captures 43% of the probe. **Nothing in the codebase fixes the window origin**, so the protocol's pin is effectively the pipeline's pre-registration and Gate 7 must reuse it. **[S40] The measured 2.37–3.64× is the ratio of TOTAL unmatched-row differences between two windows — NOT a fault-effect multiplier.**
18. **[S38] The matched/unmatched asymmetry** — Stage A/B signal is seed-matched (noise cancels), Stage C null is not. Favours S. `TESTABLE` is therefore **necessary, not sufficient**.
19. **[S38] Task motion leaks into the synchronous statistic** — probe-free `t00` healthy `||b||` at 0.8 Hz is 0.48–0.51 µε. The 0.8 Hz coefficient is not probe-specific; matched differencing is what makes it a fault statistic.
20. **[S39] The construction path (K)** — the closed loop is driven by a **C0** session and S gauges are produced **post-hoc** by replaying the privileged record. Both the protocol and the Gate-7 driver must build/read by the verified path. **Positive result, now automated and re-verified (S45): ONE delivered row reproduces bit-for-bit from committed inputs — put this in the packet at that exact scope, and cite `scripts/protocol_p_replay_gate.py` as the artifact that demonstrates it.**
21. **[S39] The unmatched-identity confound (L)** — delivered fault and healthy rows do not share `(sensor_seed, pair_id)`, so **every** delivered-row magnitude is `||fault + closed-loop divergence||`. Absolute magnitudes do not transfer to the protocol's matched `D`.
22. **[S39] The observed path is nearly free on a matched difference** — 0.937×–1.148× of the privileged result, mean ≈0.996.
23. **[S40] The realized-vs-base identity distinction** — `ScenarioReservation.base_pair_id` is NOT the RNG key; the `_dataset0` suffix makes the identity. Any protocol, audit, join, or leak guard that names "pair_id" must say **which one**.
24. **[S40] The ramp fraction is unreachable through the assignment document** — `duration/2.0` is computed, not read. A code change was always required.
25. **[S40] `Q95_c^gauge` and the S39 gauge-only measurement are conditional healthy-null diagnostics only.** No mechanism attribution for a Case C.
26. **[S41] The Stage-A safety gates are not a construction check.** A gate with a large margin certifies safety, not that the constructed experiment is the specified one. **[S43] Now covered by a permanent automated test rather than by vigilance.**
27. **[S41] A terminal branch that attributes a failure to physics must first exclude the construction.** Now fenced by **I13a AND I13b** as explicit preconditions.
28. **[S41] Raw-byte file pins are cross-platform contracts.** `core.autocrlf=true` here. Once bytes enter a scientific identity, line-ending policy is part of the protocol.
29. **[S42] A byte pin must name its DOMAIN, and a fix generalized past its domain is a new defect.** **Any file whose raw bytes enter an identity must be classified text-or-binary first.** Also: **a `.npz` is a ZIP, so byte-identity of a *regenerated* archive is not a claim to make** — pin the retained input by bytes, guard the reproduction by array equality. **[S45] Both halves executed exactly this way, and the gate reproduces §0's wrong-domain digests as a live diagnostic so the split is demonstrated, not asserted.**
30. **[S42] An undefined or overloaded token in a pre-registration is a scientific defect, not a style problem.**
31. **[S42] A specification can name an invariant its own architecture cannot express.** **Ask of every invariant: is this property reachable from the place I am asserting it?**
32. **[S43] A pre-registration's variable names are part of its executable surface.**
33. **[S44] The seam's own coverage history is part of the packet's honesty record.** The probe-override wire was untested in the first version of the seam's suite, and the gap closed only because the patch was adversarially mutated. Worth stating in the Technical Report's methods or the packet README. **If the Gate-7 driver reuses this seam, it inherits the same wire and needs the same class of test.**
34. **[S44] The two seam files are not byte-pinned, deliberately** — and **[S45] Codex confirmed this is the policy, not an oversight**: Protocol P hashes no source file, so git blob hashes are the EOL-stable identifiers. The two S45 files are in the same state for the same reason. **Any future claim about these files' bytes must quote the blob hash or say which EOL rendering it means.**
35. **[NEW S45] The one-row replay scope is exact and must be stated as such everywhere.** ONE row, ONE suite, reproduced exactly: 20 privileged fields + 38 observed entries. The 472-reservation / 944-pair dataset was **never regenerated** and no dataset-wide reproduction claim exists in the protocol or in anything derived from it. The Technical Report and the packet README must both carry that boundary. What the row *does* license is stronger than it looks, though: because the references predate the S44 seam, it also certifies that the seam perturbed nothing on the ordinary path.
36. **[NEW S45] The replay gate is not runnable by an outside reader, and the packet says so.** The two pinned references are local artifacts of the Step-2C generation and are git-ignored, so packet README Step 23 states plainly that the step cannot be run from the distributed packet, that regenerating from Step 2C reproduces the references, and that the gate's comparison layer is covered portably by `tests/test_protocol_p_replay_gate.py` instead. **`DATA.md` must repeat this at Phase-3 curation** — a runbook step a reader cannot execute is a reproducibility failure unless it is labelled.

## Coherence / honesty bounds (keep loud)

- **Sensor RNG keyed on `(sensor_seed, pair_id, channel, stream)` jointly** (`utils/rng.py:76-78`) — changing either field changes the stream. **Measured S39: a `pair_id` change alone moves `gauge_obs` by up to 6.50 µε**, against `D` values of order 0.1–0.5. **S45 adds: nothing else is in the key — suite call order does not enter it.**
- Deployable floors are *detection*, not learned attribution; all S19 rates from ONE fixed fault setting per class; abstention untestable on this fault library; one-hot prototype probabilities NOT calibrated; **every joint-space control number comes from a condition where the structural fault causes no measurable JOINT deficit.**
- **A noise threshold is a property of the SENSOR MODEL, the window LENGTH, the window ORIGIN, the aggregation, the path (privileged vs observed), the operation (single vs difference, matched vs unmatched), the construction (which session drives the loop, which produces the channel), the identity (base vs realized), and the fault's activation step. The SIGNAL it is compared against depends on excitation, task and plant.** Never quote a µε number without naming all of these.

## Constraints / environment / ops (load-bearing)

- **Simulation-only, one desktop:** Windows 11, Ryzen 7 8700F (8C/16T), RTX 5060 Ti **16 GB VRAM** (sm_120), 32 GB RAM, Python **3.12.10** in `./venv`. Free/OSS, commercial-use-friendly only.
- **venv has:** numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, matplotlib 3.11.0, mujoco 3.10.0, pandas 3.0.3, control 0.10.2, gymnasium 1.3.0, pytest 9.1.1, **torch 2.11.0+cu128**.
- **Running packet tests:** from the REPO ROOT, `./venv/Scripts/python.exe -m pytest -q "Reproducibility Packet/tests"`. **Scope pytest to that path** — a root-wide invocation collides on duplicate test module names in the ignored `tmp/session6_packet_copy/`. Full suite **472 tests green** (S45, 11.21 s). **Set `PYTHONIOENCODING=utf-8` for anything that prints non-ASCII** — the console is cp1252 and a bare `print` of `µ`/`ε`/`→` raises `UnicodeEncodeError` *after* useful output, which looks like a failure but is not. **Use ASCII in probe scripts and in anything the gate prints.**
- **Packet scripts are invoked FROM the packet directory** (`scripts\<name>.py`, `--output-dir results\<name>`), per its README. From the packet dir the project venv is `..\venv\Scripts\python.exe`. **In my PowerShell tool the working directory is not the repo root — use `Set-Location` or absolute paths. My Bash tool's cwd PERSISTS between calls — prefer absolute paths or re-`cd` every time.**
- **Timings (measured S35–S45):** full packet suite ~11 s; one MuJoCo rollout (3000 steps) **25.6–27.5 s**; **a PARTIAL rollout is proportionally cheap — 480 steps ≈ 3.0 s**; **at reduced fidelity (`point_count=9`, `simulation_timestep_s=2e-4`) 501 control steps ≈ 0.37 s — roughly 8× cheaper, legitimate whenever the property under test is not fidelity-dependent (S43)**; a 200-realization sensor-only null at W=768 across 4 gauges ~40 s (no MuJoCo); **an offline re-observation of one delivered plant trace ≈ instantaneous**; **hashing both replay references ≈ instantaneous**; **a 3,119-file inventory ≈ instantaneous**.
- **Background jobs:** `run_in_background: true` and wait for the notification. **Python buffers stdout when redirected — poll the results JSON, not the log.**
- **PowerShell 5.1** primary (no ternary/`??`; **`^` is not a continuation — use a backtick or a single line**); Bash tool also available. Use `git diff --numstat` to confirm `+N/−0` after every chat turn.
- **Root `.gitignore`** covers `venv/`, `/data/` (line 19), `tmp/`, `MUJOCO_LOG.TXT`, caches, model files, LaTeX aux, OS/IDE noise. **Root `.gitattributes`** pins `schema.json`, the assignment JSON, and **`Reproducibility?Packet/protocol/*.md`** to LF (the `?` wildcard matches the space in the folder name; **the wildcard covers each renamed protocol file — verified S42/S43 via `git check-attr`, no edit needed on a version bump**). **Packet `.gitignore`** ignores `*.npz` + caches/logs (so `results/*.json` and `*.md` ARE tracked). **Verified again S45; no change needed, and per Codex's S44 answer no source file should be added.**

## STANDING LESSONS

1. **Dry-run the analysis path before spending a rollout budget.** *(S39–S45 were all essentially this; S45 spent exactly one rollout and only after the analysis layer was proven.)*
2. **Self-audit from row artifacts / raw bytes, not the summary.**
3. **Restate a proxy in the contract's units before comparing to the bar.**
4. **For a MuJoCo screen, re-run to scratch + diff against committed.**
5. **Verify the live git state before trusting continuity** (S28–S45; the startup snapshot has lagged or been stale often. **In S45 it showed `Codex Session 44` as HEAD and was accurate — but only because I checked.**)
6. **Review a design by simulating its consequences, not by verifying its internal consistency.** Corollaries: dead arithmetic hides in small catalogs; **the dangerous confound is the one that favours you**.
7. **For any pre-registration, check that the pre-registered TEXT generates the pre-registered DATA.** *(This is why the protocol lives in one hashable file — and why a permanent test now pins that file's digest.)*
8. **Test a guard by feeding it the exact state it was written to catch.** Corollaries: check a flaw is REAL before reporting it; **and check a REPORTED flaw is real before fixing it**; report the scope you actually achieved. *(S45: applied to the gate before it was allowed to certify anything.)*
9. **A design review that reads the design cannot find what the design does.** Corollaries: **audit the yardstick before the artifact**; **before calling a settled parameter a defect, search the history for why it was chosen.**
10. **A negative result is only readable if the same instrument produced a positive one.**
11. **(S35) A threshold and the signal it judges must be measured in the SAME configuration**; matching parameter names do not make two measurements comparable.
12. **(S36) When you import a number, import its definition, not its name.** Corollary: **two configuration errors can cancel, and that is dangerous rather than lucky.**
13. **(S36) When a choice you must make favours you, measure how much, say so, and hand the decision to the reviewer.** *(Applied eight times now.)*
14. **(S36) A pre-registered protocol must be executable by someone who did not write it.** **Corollary (S37, reconfirmed S38–S45): the act of making it executable is itself the defect-finding technique.** Findings F, G, H, J, K, the label-stamp gap, the leak-guard inversion, the onset defect, S42's binary-domain and undefined-token defects, S43's identity-binding defect, S44's D5 wiring hole, and S45's vacuous-report shape all came out of pinning or building; none out of reviewing.
15. **(S36) The cleanest statement of a negative is often a comparison you have not made yet.**
16. **(S37) Match the null to the OPERATION, not just to the configuration.** And: common random numbers can void an entire class of threshold.
17. **(S37) Compute the closed-form consequences of every gate you approve, before it costs anything.** Corollary: **check boundary cases for `<` vs `<=`.**
18. **(S37) When the most likely branch creates a design problem, force the decision BEFORE the measurement that would make any fix look chosen.**
19. **(S38) When you import a convention, import the CONFIGURATION THAT MAKES IT TRUE, and re-check each assumption.** Lessons 11/12 at increasing depth: window length → aggregation → operation → time origin → construction path → realized identity (S40) → fault activation step (S41) → file byte-domain (S42) → the name an expression actually binds (S43) → **the denominator a clean report is computed over (S45)**.
20. **(S38) A guard that checks a NECESSARY condition will silently license the SUFFICIENT one.**
21. **(S38) Check your own published claim against your own published table.**
22. **(S39) A specification can be complete about the MEASUREMENT and silent about the INSTRUMENT.**
23. **(S39) Two independent errors that point the SAME way are the dangerous case.** Check the *direction* of every error, not just its size.
24. **(S39) Cheap exact reproduction is a measurement instrument, not just a confidence check.** When something is deterministic, find out. *(S45 is the strongest instance: a 26-second replay settled a question about a patch that a source review could only bound.)*
25. **(S40) A guard's claimed scope must be tested against the construction that will actually run.**
26. **(S41) A check that passes with a large margin is evidence about the property it measures, not about the construction that produced it.** **(a) Invariants that catch construction defects must assert the construction.** **(b) The quiet failure is the one a large margin produces.**
27. **(S41) An escalation trigger should be content-based, not count-based.** **And: if you decline to honour your own written commitment, say so explicitly and give the criterion.**
28. **(S42) Generalizing a fix is making a new claim about a new domain — check it there.**
29. **(S42) Name a tool for its domain, because the name is part of the interface.**
30. **(S42) Ask of every invariant: is this property reachable from where I am asserting it?**
31. **(S42) Verify a reported flaw before fixing it, and audit its class before calling it fixed.** **One instance reported usually means a class present.**
32. **(S43) A generic name in an operative expression is an open invitation, and something eventually accepts it.**
33. **(S43) A constant that looks authoritative and drives nothing is the same trap pointed the other way.** **Dead definitions are as dangerous as wrong references.**
34. **(S43) When you deviate from a collaborator's stated sequencing, say so at the top, give the reasoning, and hand them the decision.** *(Vindicated S44: Codex accepted the deviation explicitly and nothing was reverted. Disclosure was the whole cost.)*
35. **(S44) Unit-testing both ends of a wire does not test the wire.** **For any seam, write at least one test that observes the value arriving at its destination rather than placing it there.** When the destination is unreachable from the return value, capture it at the construction site.
36. **(S44) Injecting defects into your own finished patch is cheap and it is not optional.** Mutate one anchor at a time, assert the anchor matched exactly once, run the focused file, restore from a pristine byte copy, assert the restoration. **Rebuild the sweep for any future patch or gate review.** *(S45: 21 cases, and the technique is now what licenses the gate to certify anything.)*
37. **(S44) Deleting a vacuously-passing test is a contribution, not a gap.** **Ask of every new green test: what exact state would make this red?** If there is no answer, delete it and say why.
38. **(S44) Extending a stated principle to an unenumerated case is still a deviation — lead with it.** **The distinction that matters is not "am I improving it" but "did they authorize this decision."** *(Vindicated S44/S45: Codex approved the extension precisely because it was surfaced.)*
39. **(NEW S45) A clean report must disclose its denominator.** `added 0 / modified 0 / removed 0` is true and is **indistinguishable from a check that examined nothing**. This is worse than a test that cannot go red, because the reader cannot even formulate the question. Two-part remedy, both required: **print the count of things examined, and refuse to make the claim when that count is too small to support it.** Generalize it — any "0 leaks", "0 violations", "0 stray artifacts" line owes the reader its denominator.
40. **(NEW S45) Ask what else a reproduction check happens to hold fixed.** The §7 gate was specified to verify the construction path. Because its retained references predate the S44 patch, the same run also certified that the patch perturbed nothing — a question a source review could bound but not settle. **A comparison against an artifact from time T certifies everything that changed between T and now.** Look for that dividend before writing a separate check.
41. **(NEW S45) NaN tolerance and NaN blindness are one line apart.** Any exact comparison that must accept genuinely missing data needs **both** directions tested — a NaN that became a number, and a number that became a NaN — or the tolerance silently becomes a hole. The same shape applies to any "treat X as equivalent" rule: test that it still discriminates.

## Pointers

- **Protocol P (in force, JOINTLY APPROVED): `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`, canonical sha256 `5689dad7…8bdf421f`. READ THE FILE.** Superseded: v2.3.2 `9d257017…738ba6e5` and v2.3.1 `8c268f8f…401d76` (both blocked, never executed, recoverable from the `Claude Session 42` / `Claude Session 41` commits).
- **The replay gate (awaiting Codex's review): `Reproducibility Packet/scripts/protocol_p_replay_gate.py` (blob `947d39d0…`) + `Reproducibility Packet/tests/test_protocol_p_replay_gate.py` (blob `887e4e78…`).** Run it from the packet dir: `..\venv\Scripts\python.exe scripts\protocol_p_replay_gate.py --data-root ..\data\gate3-base-dev-pilot-val-c1-s`. **It PASSED in S45.**
- **The seam (APPROVED, Codex S44): `ScreenOverrides` in `Reproducibility Packet/scripts/utils/assignment_generator.py`, git blob `1c565888…`, and its tests, git blob `2ec96c9f…`.** Read spec §3 beside them.
- **The I13b guard: `Reproducibility Packet/tests/test_cable_plant_softening_boundary.py`** — 6 tests, co-owned, **approved in place by Codex (S43)**.
- Claim Sheet (in-force contract): `Claim Sheet.md` · plain-language: `Accessible Claim Sheet.md` · Study Guide Pass 1: `Study Guide/Pass 1 - Conceptual Foundation.tex`
- **Shared schema (in force, +A1):** prose `Reproducibility Packet/schema/schema-v1.0.md`; machine `schema.json`.
- **The freeze plan:** `agents/Codex/Config Freeze Readiness Review.md`.
- **The probe-amplitude record:** `Reproducibility Packet/results/synchronous_safe_probe/synchronous_safe_probe_report.md` — **read S35 Findings A–C, S36 D, S37 F, S38 J, S39 K/L, and S40/S41's narrowings beside it.**
- **The detection-floor record:** `Reproducibility Packet/results/synchronous_detection_floor/summary.json` — **`detect_threshold_microstrain` is a 5σ threshold, per gauge, at W=640, of a SINGLE window.**
- **My S34 screen:** `Reproducibility Packet/scripts/screen_structural_separability.py` + `results/structural_separability/` (packet README Step 22).
- **CONCLUDED director chat:** `chats/Claude-Codex-Human/Better Suited Task/…- Concluded.md` + `Summary.md` — the withdrawn task-redesign directive. **A2 must stay clear of it** (task, score and controller untouched).
- Director requests: `director_requests.md` (root) — entry 1 (Claim Sheet review) non-blocking, awaiting director reply. **Nothing else is blocked on the director.**
- My foundation `agents/Claude/Literature Foundation.md` · ledger `agents/Claude/references.md` (**no S20–S45 entries — reproduction/construction/measurement/review sessions, no external sources read**) · progress reports `agents/Claude/Progress Reports/` (Phase 0/1 Close, S8, S16, S24, S32, S40). **NEXT DUE: MY SESSION 48.**
- Live-Run README (co-maintained): root `README.md` — **Phase 2 / In Progress**, banner **2026-07-29**. **S43, S44 and S45 all ran the heartbeat and deliberately added NOTHING.** Codex published at approval in its S43 (protocol) and S44 (seam). **S45 was the closest call: the replay PASSED, which is a real milestone, but its validity rests on a script Codex has not reviewed, and publishing would have been the first time an agent announced ahead of its reviewer.** The entry belongs on the log one Codex turn from now — **and whoever writes it must also correct the S44 entry's phrase "no replay or screen stage has run yet," which S45 made false.**
- **Phase-2 chat:** `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` (**9,566 lines**; Codex's S44 approval header at 9,211, my S45 replay handoff at 9,340, `+230/−0`; **the replay evidence and the gate implementation are APPROVED BY ME and Codex owns the next turn**).
- **Monitoring chat:** `chats/Claude-Codex-Human/Transcript Order Monitoring/…- Active.md` (88 lines; unchanged in S43/S44/S45 — no recurrence; **streak eleven**). The duty is to flag recurrences, so a clean session adds no note; verify at the git level regardless.
