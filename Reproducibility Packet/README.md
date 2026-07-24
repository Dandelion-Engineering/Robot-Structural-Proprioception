# Reproducibility Packet

This is the self-contained working packet for the Robot Structural Proprioception project. The current runnable surface reproduces the mechanics feasibility gate, emits a schema-v1.0 privileged trace from the selected MuJoCo cable plant, and turns that trace into a deployable sensor suite's noisy observations. Later pipeline stages will be added here as they become final.

## Requirements

- Python 3.12
- A 64-bit Windows, Linux, or macOS machine supported by the pinned MuJoCo wheel

The feasibility spike is CPU-only and does not require a GPU or an external dataset.

## Step 1 — Create the environment

Creates a local virtual environment and installs the exact dependency versions used for the recorded result.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --requirement requirements.txt
```

Produces: `.venv/` (local, ignored).

## Step 2 — Run the test suite

Runs the packet's whole test suite. Every module, screen, metric, and seam in this packet is covered here, so this is the single command that tells a reader whether the packet is sound on their machine before they spend any compute on Steps 3 onward.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\ -q
```

The suite covers model compilation, independent deformation-state availability, localized stiffness-fault construction, schema-facing output shapes, synchronous-feature and coefficient-reference correctness, the safe-probe, optional-contact-profile, matched-contact-pilot, bounded-task/contact, bounded noisy held-decision, structural-recovery-action, fault-tracking-deficit, severity-estimation-quality, cap-boundary, class-probability-channel, and actuator-recovery-action screen functions, the noisy healthy-reference pilot's causal window/reference logic, the estimator front and severity read-out, the interpretable recovery controller and its shared seam regression, the linear system-ID residual baseline's role separation, suite-leakage guard, and real causal-seam integration, the plant/sensor interfaces, and the two-layer evaluation metrics and paired bootstrap.

It also covers the pre-confirmatory data contract: strict config canonicalization and self-hashing, draft/frozen lifecycle refusal, whole-group split integrity, matched C1/S common-random-number identity, role-file hashes, suite-scoped deployable loading, unavailable-channel masking, and rejection of labels, privileged truth, provenance, or extra payload keys at the observation boundary. The tracked draft can be checked directly:

```powershell
.\.venv\Scripts\python.exe scripts\validate_data_contract.py --schema schema\schema.json --config config\draft-config-v0.1.json
```

This command must report `status=draft` and `confirmatory=False`. It deliberately refuses confirmatory use. A future frozen `config.json` will be accepted only after every freeze field and manifest assignment is populated, all readiness gates are closed, and its raw canonical hash matches its filename-governed lifecycle state.

This deliberately runs the directory rather than an enumerated file list: an enumerated list goes stale silently every time a screen is added, and a test file the runbook never names is a test file an outside reader never runs. Step 18 is a focused subset for anyone debugging one area; it is not a substitute for this step.

Produces: terminal test and contract-validation results.

## Step 3 — Reproduce the mechanics gate

Runs healthy, localized structural-fault, actuator-gain-fault, and encoder-bias scenarios at three mesh/timestep settings; performs an independent cantilever-beam check; probes the reserve volumetric-flex candidate; and writes the gate artifacts.

```powershell
.\.venv\Scripts\python.exe scripts\run_feasibility_spike.py --output-dir results\feasibility_spike
```

Produces:

- `results/feasibility_spike/summary.json`
- `results/feasibility_spike/signature_metrics.csv`
- `results/feasibility_spike/feasibility_spike_report.md`
- `results/feasibility_spike/gauge_fault_signatures.png`
- `results/feasibility_spike/feature_signature_heatmap.png`

The command exits with code 0 only when every full-run gate passes. `--quick` is available for a smoke test, but it deliberately does not issue a PASS verdict.

## Step 4 — Reproduce the ordinary-excitation negative control

Repeats the same gate with the distal diagnostic load disabled. This condition is expected to block because its structural and actuator gauge signatures remain below the declared 10 µε credibility floor; exit code 2 is therefore the expected result, not a script failure.

```powershell
& .\.venv\Scripts\python.exe scripts\run_feasibility_spike.py --diagnostic-tip-load-peak-n 0 --output-dir results\feasibility_spike_ordinary_excitation_blocked
$ordinaryGateExit = $LASTEXITCODE
if ($ordinaryGateExit -ne 2) { throw "Expected BLOCK exit code 2; received $ordinaryGateExit." }
```

Produces the same five artifact types under `results/feasibility_spike_ordinary_excitation_blocked/`.

## Step 5 — Reproduce the original bounded-burst blocker

Replays ordinary, continuous, one-cycle, and two-cycle excitation through the selected mechanics and checks the unchanged per-sample mechanics floor plus the development safety envelope across every scenario. It preserves why the original 1.0 N bounded probes were not acceptable.

```powershell
.\.venv\Scripts\python.exe scripts\run_bounded_burst_sensitivity.py
```

Produces:

- `results/bounded_burst_sensitivity/summary.json`
- `results/bounded_burst_sensitivity/burst_sensitivity.csv`
- `results/bounded_burst_sensitivity/bounded_burst_report.md`

## Step 6 — Reproduce the synchronous detector floor

Runs the real gauge pathology stack over a 640-sample full-cycle window and measures the phase-invariant 0.8 Hz harmonic-regression floor. The injected target waveforms are detector surrogates; they do not replace the actual-mechanics screen in Step 7.

```powershell
.\.venv\Scripts\python.exe scripts\analyze_synchronous_detection_floor.py
```

Produces:

- `results/synchronous_detection_floor/summary.json`
- `results/synchronous_detection_floor/synchronous_detection_floor_report.md`

## Step 7 — Reproduce the safe-probe co-design screen

Uses the Step-6 development threshold on actual four-gauge MuJoCo fault-minus-healthy histories, checks safety across healthy, structural, actuator, and encoder cases, and identifies the lowest-force row in the focused grid that is eligible for a later pilot sweep. This is a development decision only; it does not freeze configuration or establish fault attribution.

```powershell
.\.venv\Scripts\python.exe scripts\screen_synchronous_safe_probe.py
```

Produces:

- `results/synchronous_safe_probe/summary.json`
- `results/synchronous_safe_probe/candidate_comparison.csv`
- `results/synchronous_safe_probe/synchronous_safe_probe_report.md`

## Step 8 — Reproduce the noisy healthy-reference pilot

Replaces the clean privileged fault-minus-healthy comparison with noisy deployable `ObservedRecord` data. The broad development sweep compares C1 and S over task/probe scale, W, stride, and onset-to-decision alignment using disjoint calibration and held-out sensor seeds. It deliberately preserves W=512 as an inert sub-cycle negative control.

```powershell
.\.venv\Scripts\python.exe scripts\run_noisy_reference_pilot.py
```

The broad sweep showed that the selected 0.50-task / 0.05 N candidate retained strong S-side fault signal, but eight calibration seeds did not resolve the requested 5% healthy false-alarm tail. The following separately seeded, prospective follow-up changes only calibration/evaluation sample size; it does not retune the threshold rule on the first sweep's held-out rows:

```powershell
.\.venv\Scripts\python.exe scripts\run_noisy_reference_pilot.py --output-dir results\noisy_reference_pilot_threshold_followup --task-torque-scales 0.5 --peak-loads-n 0.05 --calibration-seeds 32 --evaluation-seeds 48 --seed 5000
```

Produces the following under both `results/noisy_reference_pilot/` and `results/noisy_reference_pilot_threshold_followup/`:

- `summary.json`
- `pilot_results.csv`
- `pilot_aggregate.csv`
- `noisy_reference_pilot_report.md`

The prospective follow-up advances W=768 / stride=16 for **reference-rung implementation review only**: S's worst per-fault detection was 97.9%, prototype attribution 100%, pooled healthy false alarms 0.7% (2.1% worst alignment), while matched C1's minimum fault detection was 0%. These are pilot-development figures, not the confirmatory C1-vs-S result; W, stride, thresholds, sensor constants, and probe settings remain unfrozen.

## Step 9 — Reproduce the optional endpoint-contact profile screen

Screens an ascending horizontal-plane grid under the pilot-advanced 0.50-task / 0.05 N one-cycle condition. The predeclared rule selects the lowest plane above a zero-contact control that produces one brief post-onset contact episode in every canonical scenario without any A1 safety flag. The sensor scenario reuses healthy physical truth because encoder corruption is observation-side under this open-loop screen; its closed-loop contact effect remains for the later matched controller evaluation.

```powershell
.\.venv\Scripts\python.exe scripts\screen_optional_contact_profile.py
```

Produces:

- `results/optional_contact_profile_screen/summary.json`
- `results/optional_contact_profile_screen/contact_profile_grid.csv`
- `results/optional_contact_profile_screen/optional_contact_profile_report.md`

The grid advances **z = 0.100 m** to matched optional-contact pilot review: healthy/structure/sensor have 19 active steps and actuator has 23, all in one episode, with 1.08–1.41 N peak force and zero A1 safety flags. This is an open-loop development profile candidate, not a frozen height or a C1-vs-S result. The 0.498 m low-level extraction fixture remains excluded from the candidate grid.

## Step 10 — Reproduce the matched contact-enabled C1/S pilot

Applies z = 0.100 m identically to matched C1/S pairs. It fits contact-conditioned coefficient references on 32 calibration seeds, evaluates 48 disjoint held-out seeds at the exact observation window owned by the first online post-probe decision, drives one held-out pair per source through the real causal plant→sensor→estimator→controller seam, and separately audits both z = 0.100 m and the former z = 0.050 m control over the required onset+5 s horizon.

```powershell
.\.venv\Scripts\python.exe scripts\run_matched_contact_pilot.py
```

Produces:

- `results/matched_contact_enabled_pilot/summary.json`
- `results/matched_contact_enabled_pilot/contact_information_rows.csv`
- `results/matched_contact_enabled_pilot/online_seam_rows.csv`
- `results/matched_contact_enabled_pilot/extended_horizon_rows.csv`
- `results/matched_contact_enabled_pilot/matched_contact_pilot_report.md`

The recorded development decision is **BLOCK**. S retains 100% minimum per-fault detection and 100% prototype attribution at the scheduled contact-conditioned decision, but its 8.3% held-out healthy false-alarm rate exceeds the 5% screen. In the short causal continuation the single-decision prototype becomes phase/reference-unstable and every representative arm ends on an actuator call, including healthy and observation-side sensor-fault cases. Over onset+5 s, z = 0.100 m produces three contact episodes and joint-angle safety violations in every physical source scenario; z = 0.050 m also ceases to be a no-contact control. These are development blockers, not confirmatory results. The profile, W/stride, prototype, thresholds, controller settings, faults, sensor constants, and `config.json` remain unfrozen.

## Step 11 — Reproduce the bounded task/contact/controller redesign screen

Replaces the matched pilot's perpetual open-loop task torque with a low-authority controller that reads only delivered encoder position/velocity. The one-cycle probe completes first; one fixed source-correct diagnosis stand-in is then evaluated and held; only afterward does a smooth finite task excursion create contact under controller authority. The screen audits a predeclared five-plane bracket across healthy, structural, actuator, and observation-side sensor faults over the full onset+5 s horizon.

```powershell
.\.venv\Scripts\python.exe scripts\screen_bounded_task_contact.py
```

Produces:

- `results/bounded_task_contact_screen/summary.json`
- `results/bounded_task_contact_screen/bounded_task_contact_rows.csv`
- `results/bounded_task_contact_screen/bounded_task_contact_report.md`

The recorded mechanics/lifecycle screen advances **z = 0.200 m** to matched information/reference-lifecycle review. The held decision occurs at 2.272 s, the contact excursion begins at 2.400 s, and every selected-plane arm produces exactly one contact episode at 4.618–5.194 s with 0.476–2.125 N peak force and zero A1 safety steps. z = 0.100 m is the all-source no-contact control. Structural derating and actuator inverse-gain scheduling begin at the held decision and therefore precede contact; healthy and sensor arms preserve their nominal feedback command. The stand-ins use known development sources, so this is **not** an attribution, tracking-recovery, C1-vs-S, or frozen-config result.

## Step 12 — Reproduce the bounded noisy held-decision information review

Replaces the fixed source-correct mechanics stand-ins with suite-specific noisy coefficient references at the exact first causal post-probe decision. It fits detection and prototype-margin abstention separately for C1 and S on 100 calibration-only sensor seeds, evaluates 48 disjoint held-out seeds, reports false alarms, per-fault detection/attribution, known-class abstention, and recovery-action gating, then holds one predeclared held-out diagnosis through the full six-second bounded task for each source/suite. Information, action authorization, representative tracking, and A1 safety remain separate gates.

```powershell
.\.venv\Scripts\python.exe scripts\run_bounded_noisy_information_review.py
```

Produces:

- `results/bounded_noisy_information_review/summary.json`
- `results/bounded_noisy_information_review/information_rows.csv`
- `results/bounded_noisy_information_review/heldout_decision_rows.csv`
- `results/bounded_noisy_information_review/representative_online_rows.csv`
- `results/bounded_noisy_information_review/bounded_noisy_information_report.md`

The recorded decision is split: **advance the information/reference lifecycle only; block the current recovery-control profile.** S reaches 0.995 held-out four-way macro-F1 versus C1's 0.704, with 100% versus 8.3% structural recall, 100% minimum per-fault detection, and 2.1% held-out healthy false alarms. C1 and S share bit-identical pre-decision physical/shared-observation histories, and every representative six-second arm keeps one bounded contact episode with zero A1 safety steps. But the only suite-informed representative action — S correctly calling the structural fault while C1 stays healthy/no-action — worsens `J_5s` by 18.6% (1.0184 versus 0.8589 m·s), so the structural derating policy fails the control-sensitivity gate. The probabilities are one-hot mechanism instruments and the full-horizon continuation uses one held-out seed per source/suite; this is neither confirmatory evidence nor permission to freeze any setting.

## Step 13 — Reproduce the structural recovery action-family screen

Keeps the approved six-second bounded mechanics, task/contact profile, and one-held-decision lifecycle fixed while comparing the old 0.75 derate, no action, and a predeclared family of global/local severity-conditioned inverse-stiffness multipliers. Three tuning-only sensor seeds select a candidate; four disjoint assessment seeds then test structural tracking, healthy false authorization, A1 safety, saturation, source specificity, and exact pre-decision CRN matching. Fixed source-correct outputs isolate the controller mechanism, so this is not attribution evidence or a frozen setting.

```powershell
.\.venv\Scripts\python.exe scripts\screen_structural_recovery_action.py --workers 8
```

Produces:

- `results/structural_recovery_action_screen/summary.json`
- `results/structural_recovery_action_screen/candidate_rows.csv`
- `results/structural_recovery_action_screen/tuning_rows.csv`
- `results/structural_recovery_action_screen/assessment_rows.csv`
- `results/structural_recovery_action_screen/structural_recovery_action_report.md`

The recorded decision is **BLOCK**. Global 1.5× and 2.0× candidates clear the 10% per-seed structural tracking gate with zero A1 or saturation events, and the selected 2.0× action retains a 19.4–20.2% reduction on disjoint structural seeds. But the same false-authorized action improves healthy tracking slightly more on average (20.15% versus 19.88%), so the source-specificity gate blocks: this is evidence that the nominal bounded controller is under-authorized, not that inverse-stiffness scheduling recovered a structural deficit. The default 0.75 derate remains the approved transparent safety floor; the nominal controller and task/fault sensitivity must be redesigned before another structural action advances.

The report's generated "What the recorded decision does and does not establish" section carries the measured bounds on that block, and one of them decides the ordering of the redesign: on this condition the structural fault's *own* no-action tracking deficit is only +0.05% of the healthy arm's — 0.18× the widest within-source seed spread, so it is not resolved above seed noise, and it is roughly 200× smaller than the 10% gate a structural action would have to clear. The binding constraint is therefore the task/fault severity rather than the controller tuning or the action family, so the fault condition must be shown to produce a measurable per-class tracking deficit **before** another action family is screened against it. The `-0.26` percentage-point specificity margin itself is smaller than the 1.0–1.3 percentage-point per-seed spread of the reductions it is built from and carries no computed uncertainty; the block rests instead on the within-role contrast that ~70% of the selected action's benefit is produced at the joint carrying no fault.

## Step 14 — Reproduce the per-class fault tracking-deficit screen

Runs before any further recovery-action design. It keeps the approved bounded task, z = 0.200 m contact plane, observed-state controller, diagnostic probe, and no-recovery lifecycle fixed while sweeping remaining link-2 stiffness and joint-1 actuator gain. Three tuning-only seeds select the mildest physical setting whose no-action `J_5s` deficit is large enough to *admit* the Claim Sheet's 10% bar plus a predeclared 2-point margin on every seed; four disjoint assessment seeds must reproduce the same headroom with exact paired pre-fault histories, one held healthy decision, zero recovery-command changes, zero A1 incidents, and zero saturation. A fixed 0.05 rad observation-side encoder-bias control is reported separately.

The gate converts between two quantities that do not share a denominator. The contract's bar is a **reduction** against the degraded arm (`100·(J_C1 − J_S)/J_C1`); this screen measures a **deficit** against the healthy arm (`100·(J_fault − J_healthy)/J_healthy`). A source-specific action that exactly restored healthy tracking would turn a deficit `D` into a reduction `D/(1 + D)`, so a deficit gate set numerically equal to the reduction target under-delivers it — a 12% deficit admits at most a 10.71% reduction, which would leave 0.71 points of the declared 2-point margin. The gate therefore inverts the relation and requires a **13.64%** per-seed deficit for a 12% reduction target.

```powershell
.\.venv\Scripts\python.exe scripts\screen_fault_tracking_deficit.py --workers 8
```

Produces:

- `results/fault_tracking_deficit_screen/summary.json`
- `results/fault_tracking_deficit_screen/candidate_summary.csv`
- `results/fault_tracking_deficit_screen/tuning_rows.csv`
- `results/fault_tracking_deficit_screen/assessment_rows.csv`
- `results/fault_tracking_deficit_screen/fault_tracking_deficit_report.md`

The recorded decision is **advance actuator deficit only; block structural deficit.** The mildest advancing physical setting is 0.25 remaining actuator gain: its disjoint mean/min no-action tracking deficit is 23.16% / 23.03%, above the 13.64% development gate (0.50 remaining gain reaches 13.20% / 13.12% and therefore admits only an 11.66% / 11.60% reduction, short of the 12% target). No structural setting advances. Across 0.75→0.05 remaining EI, the disjoint mean structural deficit ranges from +0.11% to −5.00%; progressively softer link-2 mechanics eventually improve rather than harm this task's tracking, even while strain remains structurally informative. The fixed 0.05 rad encoder-bias control creates a 15.69% mean deficit but is not a selected severity grid. All 84 arms preserve exact seed-paired pre-fault histories, one held healthy decision, no recovery action, zero A1 incidents, zero saturation, and at most one bounded contact episode. This establishes control headroom only; it is not attribution, action-efficacy, validation-sized, or frozen-config evidence.

The report's generated "What the recorded headroom does and does not license" section carries the bounds that decide how this advance may be used. Two of them matter most. First, the advancing setting admits at most an 18.72% reduction at its worst seed for an action that restores healthy tracking exactly. Performance above that exact-restoration ceiling is not attributable to fault restoration alone: it could be fault-specific overcompensation or generic nominal-controller under-authority, so the action screen must distinguish them with a healthy false-authorization arm and report the source-specific margin separately. Second, no-action headroom is **not** S-over-C1 headroom: the contract's control quantity is the paired difference between the suites on the same fault, and the bounded noisy information review already records that difference as exactly 0.0000% on the actuator and sensor classes (both suites act identically because C1 detects them at 100% recall) and non-zero only on the structural class, where there is no deficit to recover. An advancing class here licenses an action screen; it does not open a path to the Slot-11 control comparison.

## Step 15 — Reproduce the severity-estimation-quality screen

Runs after the deficit screen, whose recorded per-class deficits it reads. Every recovery number recorded before this one was produced with a severity that came from a privileged oracle or a pinned stand-in constant, while the controller's actuator action is severity-*conditioned* — so severity-estimation quality was an unmeasured term sitting underneath every control result, and one route by which the contract's paired S-minus-C1 difference could be non-zero on a class the conventional suite already detects. This screen measures it in two parts that have to be read together.

Part A is analytic and needs no rollouts. The actuator multiplier is `min(1 / max(severity, minimum_gain_remaining), maximum_gain_compensation)`, which is **flat** below `1 / cap`: over that whole interval every severity estimate commands identically, so two suites cannot differ there however far apart their numbers are. `minimum_gain_remaining` bounds that interval from below, so raising the cap alone cannot make the most severe settings severity-sensitive. Part A locates the interval, crosses it against the recorded per-class deficits, and reports — per compensation cap — which severities are both severity-sensitive *and* carry an exact-restoration ceiling above the Claim Sheet bar. A severity advantage can only reach the contract where both hold.

Part B fits a matched `SeverityRidgeHead` per suite on tuning seeds and scores it on disjoint assessment seeds across an actuator-gain severity grid, on the same bounded task, contact plane, observed-state controller, diagnostic probe, and single-held-decision lifecycle as Steps 11–14. One S observation is generated per arm and physically projected to C1, so the suites see the same trajectory and bitwise-identical shared channels; the projection is verified against real C1 sessions on a spread of grid points rather than assumed. The ridge penalty is chosen by leave-one-seed-out cross-validation on tuning rows only. Both suites' held-out estimates are then pushed back through Part A's multiplier, because the commanded action — not the severity number — is what the contract's paired quantity is made of.

```powershell
.\.venv\Scripts\python.exe scripts\screen_severity_estimation_quality.py --workers 8
```

Produces:

- `results/severity_estimation_quality/summary.json`
- `results/severity_estimation_quality/arm_rows.csv`
- `results/severity_estimation_quality/window_features.csv`
- `results/severity_estimation_quality/severity_estimation_quality_report.md`

`window_features.csv` carries the extracted per-arm, per-suite window feature vectors. The rollouts are the expensive part of this screen and those vectors are their only durable product, so the read-out comparison can be refitted with a different model, penalty, or split without re-running the physics.

The recorded outcome is narrower: **both suites estimate actuator severity almost exactly, but severity quality remains a live control route at the action's cap boundary.** Held-out mean absolute error is **0.0065 for C1 and 0.0076 for S**, so the 32 additional gauge feature columns do not improve the matched linear read-out. This is expected mechanically: C0 already carries commanded actuation, the fault acts downstream of it, and commanded torque with the resulting encoder motion brackets remaining gain directly. But the 0.50 remaining-gain condition from Step 14 sits exactly at the recorded cap-2 kink and has an 11.66% exact-restoration ceiling, above the Claim-Sheet bar. The screen therefore includes that boundary explicitly. Its held-out estimates straddle the kink, and C1/S command multipliers differ on **3 of 4** paired 0.50-gain arms (mean absolute difference 0.0331; worst 0.0694). The strictly capped interior remains behaviourally identical across suites, but the paired actuator-control effect is **not structurally zero**: it must be measured in the action screen. At caps of 4 and above the corresponding boundary is the 0.25 gain floor and all four paired boundary arms differ, while 0.10 remains in the strictly flat interior. On healthy arms S still reproduces the no-action command on 75% of arms against C1's 25%, a false-authorization difference rather than a control-bar result. This is development-sized evidence about a linear read-out with `p` pinned at 1 for both suites; it is not validation-sized, not frozen-config, not evidence about the structural or sensor classes, and it does not measure the class-probability channel, which remains a separate untested route to a paired difference.

## Step 16 — Reproduce the cap-boundary action screen

Runs after the severity-estimation-quality screen, whose recorded held-out estimates and window features it reads. Step 15 closes on an open question: at the recorded cap the `0.50` remaining-gain setting sits exactly on the multiplier's kink, where the action is one-sidedly severity-sensitive and the exact-restoration ceiling clears the Claim Sheet bar, and the two suites' held-out estimates straddle that kink on 3 of 4 paired arms. Step 15 states the honest consequence — the paired actuator-control effect there is **not structurally zero** and must be measured. This screen measures it.

Part 1 computes **severity-uncertainty diagnostics** and needs no rollouts. The recovery controller's confidence gate rejects a diagnosis whose severity uncertainty exceeds `maximum_severity_uncertainty`, and `SeverityRidgeHead` only reports an in-sample residual dispersion. A fixed-penalty leave-one-seed-out estimate on Step 15's tuning role supplies a calibration-only value without consuming the disjoint assessment role; the actual disjoint assessment residual dispersion is reported beside it. The fixed penalty was selected on those same tuning groups, so the calibration cross-seed number is development guidance, not a nested post-selection uncertainty or a frozen confidence margin.

Part 2 runs the boundary arms. On the same bounded task, contact plane, observed-state controller, probe, and single-held-decision lifecycle as Steps 11–15, at remaining gain `0.50`, each disjoint assessment seed is run under: no action, a healthy-plant reference, a privileged oracle severity, each suite's *recorded held-out estimate*, and a sweep of fixed commanded multipliers. The estimator decides once, before the action fires, so everything up to the decision step is bitwise identical to Step 15's arm at the same seed — which is what licenses commanding an estimate that was produced in a different run. The screen does not assume that: the no-action and healthy arms re-run those trajectories and their `J_5s` values are checked against Step 15's committed rows. CRN reuse, the one-decision lifecycle, action/no-action behavior, A1 safety, saturation, and commanded-versus-applied multipliers are all fail-loud gates; a false integrity field cannot survive into the generated narrative.

Part 3 is the **measured conversion envelope**. Every severity result in this packet is stated in multiplier units while the contract is stated in tracking units; the sweep is the missing conversion factor. Its 1.50–2.00 range is far wider than the errors of the recorded linear read-outs, but it is not a universal bound on an arbitrary future read-out that could command below 1.50.

```powershell
.\.venv\Scripts\python.exe scripts\screen_severity_action_boundary.py --workers 8
```

Produces:

- `results/severity_action_boundary/summary.json`
- `results/severity_action_boundary/arm_rows.csv`
- `results/severity_action_boundary/severity_action_boundary_report.md`

The recorded outcome closes the **recorded linear-read-out severity route** on the actuator class at the recorded cap, on this condition. The action is real — a **+13.11%** no-action deficit, of which a privileged oracle recovers **+10.81%** — but the **paired S-minus-C1 reduction is −0.1177% on average and at most 0.5154% on any seed**, against a 10% bar, with C1 ahead on two seeds, S on one, and one pair exactly identical. Across the wider swept multiplier range 1.50–2.00 the reduction moves by only **3.81 percentage points**, and the sweep's extreme point corresponds to a severity error roughly fifteen times the larger calibration cross-seed residual standard deviation while still recovering 7.00%. This envelope covers the recorded heads generously; it does not license a claim about every possible future read-out. Reaching a 10-point paired difference on this curve would require one suite to command essentially no action at all, which is a class-call-scale failure rather than the observed severity-precision difference.

Two further recorded results. **The in-sample severity dispersion is optimistic for both suites.** Against the calibration-role cross-seed estimate it understates C1 by 1.59x and S by 5.72x; against the genuinely disjoint assessment residual dispersion it understates C1 by 1.98x and S by 4.12x. The absolute suite ranking does *not* survive across those two diagnostics: S has the larger internal cross-seed dispersion but a slightly smaller disjoint-assessment standard deviation, while Step 15's S mean absolute error remains larger because its bias is larger. The safe conclusion is that training dispersion must never reach the confidence gate; both calibration-only values clear the gate regardless. And **exact restoration of the gain does not exactly restore the tracking on this boundary condition**: the oracle realizes 93.2% of the analytic `deficit -> reduction` ceiling, in the same direction on every seed, because the error the fault produces before the single held decision fires is not recoverable by any later multiplier. Whether the same shortfall applies at Step 14's selected 0.25 condition remains unmeasured.

This is development-sized evidence on four assessment seeds, one bounded condition, one fault location and setting, held out over sensor noise only, at an unfrozen config. It does not close the actuator class, an arbitrary future severity read-out outside the swept envelope, or the cap-4 boundary — action-versus-no-action benefit, healthy false authorization, cap and floor sensitivity, and the source-specific margin belong to the action screen — and it does not measure the class-probability channel, which pins `p = 1` on every arm here.

## Step 17 — Reproduce the class-probability sensitivity screen

Runs after Steps 14 and 15, whose committed rows it reads. The recovery controller weights its correction by the estimated class probability, while every prior action arm pins that probability at one. This screen isolates that graded probability response at the condition Step 14 actually **selected** — `actuator_gain_remaining_0p25` — while class, location, severity, severity uncertainty, and abstention are held fixed.

Two structural facts define the fixture. First, the compensation is `min(1 / max(severity, minimum_gain_remaining), maximum_gain_compensation)`, so at the recorded cap **every severity estimate at or below `0.50` yields the identical capped compensation**; the true `0.25` sits about 25x its recorded linear read-out error scale inside that flat region. Second, recorded controller constants close the probability input interval: the confidence gate below and probability one above, with the compensation cap fixing the upper multiplier. The reachable commanded-multiplier interval is therefore exactly `[1.50, 2.00]`. The simulations sample that continuous interval at six probabilities. They provide an empirical response envelope over the recorded grid, not an exhaustive mathematical bound between grid points.

The screen also answers the question Step 16 left open — whether its 93.2% realized-versus-analytic ratio carries to the selected condition. It does not, and the reason is structural: at `0.25` remaining gain exact restoration needs a multiplier of `4.00` while the cap allows `2.00`, so the action is **cap-saturated throughout** and even a maximally confident diagnosis under-restores by a factor of two.

Reported quantities are in the contract's own units — `100 x (J_C1 - J_S) / J_C1` — not in differences of no-action reductions, which would understate the quantity the bar is written in. The analysis searches every ordered pair on the sampled gate-clearing grid rather than assuming the endpoints are extrema. A sub-threshold probe that keeps the actuator as the unique argmax verifies that the probability gate withholds the action entirely. CRN reuse against Step 14's committed rows, arm-grid completeness, the one-decision lifecycle, withheld/acting behavior, A1 safety, saturation, and the commanded-versus-applied multiplier identity are all fail-loud gates.

```powershell
.\.venv\Scripts\python.exe scripts\screen_actuator_probability_channel.py --workers 8
```

Produces:

- `results/actuator_probability_channel/summary.json`
- `results/actuator_probability_channel/arm_rows.csv`
- `results/actuator_probability_channel/actuator_probability_channel_report.md`

The recorded six-point response is monotone on all four assessment seeds. Searching every sampled pair finds a largest gate-clearing S-over-C1 comparison of **5.07 percentage points** (mean 5.02), against a 10-point bar. This is a sampled development sensitivity, not closure of every unsampled probability or of a future calibrated estimator. The gate crossing is reported separately at **10.82 points**, because one suite withholding while the other acts is an authorization difference, not a graded probability-precision result. Calibrated probability, abstention, and uncertainty-gate behavior remain validation-owned.

Two further recorded results. The action's benefit is real and steeply cap-limited: mean no-action deficit **23.16%**, analytic exact-restoration ceiling **18.81%**, realized at the cap **10.82%** — **57.5% of the ceiling**, in the same direction on every seed. That is a far larger shortfall than Step 16's 93.2% at the `0.50` boundary, and it is attributable to cap saturation rather than to pre-decision error alone; `maximum_gain_compensation` is therefore the binding limit on recoverable tracking at the condition the action screen will run on. The fixture supplies every acting arm the same conservative **bias-inclusive RMS** severity error scale so uncertainty does not become a second varied channel. That development choice does not define a frozen per-example uncertainty statistic.

This is development-sized evidence on four assessment seeds, one bounded condition, one fault location and setting, held out over sensor noise only, at an unfrozen config. It does not close the actuator class or the continuous probability response between sampled points; action-versus-no-action benefit, healthy false authorization, calibrated authorization/uncertainty, cap and floor sensitivity, and the source-specific margin remain open. It also does not extend to a different cap, since both the flat severity region and the multiplier interval change with `maximum_gain_compensation`.

## Step 17A — Reproduce the actuator recovery-action screen

Runs after Steps 14–17 at the selected 0.25 remaining actuator-gain condition. Three tuning seeds choose from the predeclared cap/floor family without reading assessment. Four disjoint assessment seeds then compare the selected profile under oracle severity and the exact recorded C1/S held-out severity estimates. Every fault-action benefit is paired with the identical actuator diagnosis falsely authorized on a healthy arm, so the primary quantity credits only recovery beyond generic controller improvement.

The screen requires a 12% tuning recovery target, the Claim Sheet's 10% assessment recovery bar, a 10-point source-specific margin, and a clean action lifecycle. The paired four-seed bootstrap is a development sign-stability guard, not validation-sized uncertainty. Reference arms must reproduce Step 15's committed no-action `J_5s` exactly and remain A1/saturation/multiplier clean. Candidate safety incidents remain visible scientific block evidence rather than being erased as run corruption.

```powershell
.\.venv\Scripts\python.exe scripts\screen_actuator_recovery_action.py --workers 8
```

Produces:

- `results/actuator_recovery_action_screen/summary.json`
- `results/actuator_recovery_action_screen/tuning_rows.csv`
- `results/actuator_recovery_action_screen/assessment_rows.csv`
- `results/actuator_recovery_action_screen/candidate_summary.csv`
- `results/actuator_recovery_action_screen/actuator_recovery_action_report.md`

The recorded 100-arm development result is `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`. Cap-3/floor-0.25 is the best lifecycle-safe tuning candidate. On disjoint assessment, oracle, C1, and S are action-identical at that cap: 16.576% mean fault reduction minus 8.322% healthy false-authorization benefit leaves an 8.254-point source-specific margin, with a paired interval of [8.093, 8.532], below the 10-point gate. Cap-4/5 reach about 19.7% raw fault recovery but violate A1 safety. This does not measure calibrated false-authorization rates or establish a C1-versus-S control result.

## Step 18 — Run the plant-interface and sensor-model tests

Checks the lossless `PlantStepState` → privileged-trace interface, real MuJoCo deformation-coordinate and optional endpoint-contact-force extraction, the contact-profile selection rule, plant/sensor fault boundary, three-torque semantics, privileged/observed leakage boundary, common-random-number substreams, suite masks, sensor-fault relational signature, thermal apparent strain, dropout/derived-velocity validity, latency causality, and deterministic persistence.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_cable_plant.py tests\test_optional_contact_profile.py tests\test_sensor_model.py -q
```

Produces: terminal test results.

## Step 19 — Generate a real privileged trace from the selected MuJoCo plant

Advances the selected 17-point-per-link cable plant at 500 Hz control / 10 kHz simulation, extracts the frozen 90-wide internal ball-joint log-map deformation vector, and persists every schema-B field under the isolated `plant/` role. The command uses the bounded 1.0 N, 0.8 Hz diagnostic condition that cleared the mechanics gate. Its `config_hash` is deliberately prefixed `dev-`: the shared immutable `config.json` has not been frozen, so this output is for development/integration and cannot be mistaken for confirmatory data.

```powershell
.\.venv\Scripts\python.exe scripts\make_mujoco_plant_trace.py --output-root results\mujoco_plant --run-id healthy_dev --duration-s 3 --thermal-ramp-c 5
```

For a low-level development check of the A1 endpoint-contact role, supply the original
extraction-fixture plane height. This enables only the distal endpoint-segment/plane
collision pair and records MuJoCo constraint-force truth. It is distinct from Step 9's
screened 0.100 m profile candidate and does not freeze either value:

```powershell
.\.venv\Scripts\python.exe scripts\make_mujoco_plant_trace.py --output-root results\mujoco_contact_dev --run-id contact_dev --duration-s 0.2 --endpoint-contact-plane-z-m 0.498
```

Produces:

- `results/mujoco_plant/plant/healthy_dev.npz` — role-separated privileged plant payload.
- `results/mujoco_plant/plant/index.csv` — plant-role index (`run_id, schema_version, config_hash, npz_path, sha256`).
- Optional contact command: `results/mujoco_contact_dev/plant/contact_dev.npz` and its
  adjacent `index.csv`, with the same role/index schema.

Use `--scenario structure --fault-severity 0.50` or `--scenario actuator --fault-severity 0.70` for a physical-fault development trace. Sensor faults are rejected here and must be injected only in Step 20.

## Step 20 — Apply the sensor-realism + fault-injection model

Maps the real privileged plant trace to one deployable sensor suite's observed record: encoder/IMU/current-proxy/gauge channels with additive noise, thermal apparent strain, bias, drift, hysteresis, quantization, dropout, and latency, plus optional injection of a sensor-class encoder fault into the observation path only. Channels a suite does not carry are written as `NaN` and masked off, so the suites differ only by available information.

```powershell
.\.venv\Scripts\python.exe scripts\run_sensor_model.py --plant-npz results\mujoco_plant\plant\healthy_dev.npz --suite S --run-id healthy_S --pair-id 1 --sensor-seed 7 --split dev
```

Produces:

- `results/sensor_model/observations/S/healthy_S.npz` — the observed record for suite `S`.
- `results/sensor_model/observations/S/index.csv` — the per-suite index row (`run_id, schema_version, config_hash, npz_path, sha256, split`).

Use `--suite C0` or `--suite C1` for the leaner conventional suites, and `--fault-class sensor --fault-subtype encoder_bias --fault-location 0 --fault-severity 0.05 --fault-onset 499` to inject a sensor fault at the 1.000 s sample of this 500 Hz post-integration trace.

## Step 21 — Generate the optional analytic plant fixture

Writes a schema-conforming privileged plant record built from analytic signals. This is a **development stand-in** used to exercise the sensor model on its own; it is not integrated mechanics and makes no physical claim. The `--thermal-ramp-c` option adds a temperature rise so the gauge channel's thermal apparent-strain pathology is visible.

```powershell
.\.venv\Scripts\python.exe scripts\make_synthetic_plant_trace.py --output-npz results\synthetic_plant\healthy.npz --thermal-ramp-c 5
```

Produces: `results/synthetic_plant/healthy.npz`

## Data

No external dataset is required. The simulator generates every value used by the spike. See [`DATA.md`](DATA.md) for the data and licensing boundary.

## Dependency licenses

| Dependency | Version | License | Role |
|---|---:|---|---|
| MuJoCo | 3.10.0 | Apache-2.0 | Cable/rod and volumetric-flex dynamics |
| NumPy | 2.5.1 | BSD-3-Clause and bundled permissive notices | Numeric arrays and metrics |
| Matplotlib | 3.11.0 | PSF-based/BSD-compatible | 300-DPI figures |
| pytest | 9.1.1 | MIT | Focused tests |

All are free and commercial-use-permitting. Project-owned code and configurations are MIT-licensed; packet prose and figures are CC BY 4.0. The copy-ready attribution and exact scope statement are in [`DATA.md`](DATA.md).

## Historical boundary (superseded in part)

This packet reproduces the mechanics gate, detector-floor correction, safe-probe co-design screen, noisy healthy-reference pilot, optional endpoint-contact profile screen, matched contact-enabled development pilot, bounded task/contact/controller redesign, bounded noisy held-decision information review, structural recovery action-family screen, and the per-class fault tracking-deficit screen, and it connects the selected MuJoCo plant's **real persisted privileged output** to the sensor-realism model. Schema Amendment A1 is jointly in force. The causal one-step plant→sensor→policy loop and estimator front exist and are tested. The permanent `CoefficientReferenceDetector` uses the pilot's canonical score statistic with fail-loud reference/threshold lifecycle guards, and the jointly approved interpretable gain-scheduled recovery-controller floor plugs into the same seam; neither is a completed control result. A new `LinearResidualAttributionEstimator` supplies the Claim-Sheet-required interpretable baseline: it fits healthy deployable one-step ARX dynamics, builds four transparent residual-pattern prototypes in a separate development role, and calibrates off-prototype abstention on a third role. Its synthetic separation and real-seam checks are mechanism tests only. The learned attribution and RMA heads are still unbuilt. The fixed two-field contact role enables collision solely between the distal endpoint segment and an explicit plane, extracts MuJoCo's constraint-force truth, and drives the seventh privileged safety flag; the default model remains collision-disabled. The earlier short open-loop grid advanced z = 0.100 m to matched pilot review, but the matched pilot **blocked** it: S's contact-conditioned scheduled-decision signal came with 8.3% healthy false alarms, the pilot-only continuous prototype was phase/reference-unstable, and the selected plane produced repeated contacts plus privileged joint-angle safety violations over onset+5 s. The bounded redesign advanced z = 0.200 m as the lowest all-source mechanics/lifecycle candidate under deployable encoder feedback, one held scheduled diagnosis, a post-decision finite contact excursion, and zero A1 flags over onset+5 s. Replacing its fixed diagnoses with resolved-tail noisy references now advances the **information/reference lifecycle only**: S reaches 0.995 held-out macro-F1 and 100% structural recall versus C1's 0.704 and 8.3%, with 2.1% versus 4.2% healthy false alarms. The old structural derate remains blocked because it worsens `J_5s` by 18.6%. A predeclared inverse-stiffness multiplier family then found 19–20% structural tracking reductions with no A1 or saturation events, but the selected 2.0× multiplier improved healthy tracking slightly more than the structural-fault case; the source-specificity gate therefore **blocks** it as a generic nominal-controller retune, not structural recovery. The follow-on no-recovery headroom screen now shows why: no structural severity from 0.75 down to 0.05 remaining EI reaches the development gate — its deficit falls to zero and then turns negative while peak strain rises monotonically from 19.2 to 259.7 µε — while 0.25 remaining actuator gain advances with a 23.03% minimum disjoint deficit and the fixed 0.05 rad encoder-bias control produces a 15.69% mean deficit. The structural control path is therefore blocked on this bounded task even though its strain signature remains informative; the next action screen belongs to the actuator condition, not to another structural multiplier family. That advance authorizes an action screen only: the contract's paired S-minus-C1 tracking difference is already recorded as exactly zero on the actuator and sensor classes under a pinned severity, so control-layer headroom on a class C1 also detects does not by itself become a Slot-11 win. The severity-estimation-quality screen narrows but does **not** close the severity route. Both suites estimate remaining gain accurately (held-out MAE 0.0065 C1 / 0.0076 S), and every strictly capped-interior arm commands identically, but the above-bar 0.50 remaining-gain condition sits exactly at the recorded cap-2 kink. Held-out estimates straddle it, producing different C1/S multipliers on 3 of 4 paired boundary arms. The cap-boundary action screen, jointly approved in its reviewer-corrected state, measured what that difference is worth in tracking, and it is small: the paired S-minus-C1 reduction is **−0.12% on average and at most 0.52% on any seed** against a 10% bar, on a condition where the action itself is real (+13.11% no-action deficit, +10.81% recovered by a privileged oracle). Across the measured multiplier range 1.50–2.00, the reduction moves by only **3.81 percentage points**. That is an empirical envelope for the recorded linear heads, not a universal bound on an arbitrary future linear or learned read-out that could command outside the sweep. The screen closes the **recorded linear-read-out severity route** on the actuator class at the recorded cap and condition; it does not close arbitrary future read-outs, the actuator class, or the cap-4 / 0.25-floor boundary. The uncertainty diagnostics also require distinct roles. A fixed-penalty leave-one-tuning-seed-out calibration estimate exceeds the in-sample dispersion by 1.59x for C1 and 5.72x for S, while the genuinely disjoint assessment residual dispersion exceeds it by 1.98x for C1 and 4.12x for S. The absolute suite ranking does not survive across those diagnostics: S has the larger internal calibration dispersion but a slightly smaller assessment standard deviation, while its assessment mean absolute error remains larger because its bias is larger. The safe conclusion is that the training residual must not be handed to the confidence gate; both calibration-role values clear that gate, but they are development estimates rather than frozen margins. Finally, exact restoration of the gain does not exactly restore the tracking on this boundary condition — the oracle realizes 93.2% of the analytic `deficit -> reduction` ceiling, in the same direction on every seed — because error accumulated before the held decision cannot be recovered later. The class-probability channel screen then measured both of the things that left open. At the selected 0.25 condition the severity channel is **structurally flat** — the cap binds for every estimate at or below 0.50, roughly 25x the recorded error scale away from the true value — so class probability is the only channel that can still separate two suites there. That channel is closed at both ends by recorded controller constants, the confidence gate below and the compensation cap above, which makes its sweep a **reachable-set span rather than a chosen-range envelope**: the widest paired difference two gate-clearing suites can produce through it is **5.07 percentage points**, mean 5.02, against a 10-point bar, reported in the contract's own `100 x (J_C1 - J_S) / J_C1` units rather than as a difference of no-action reductions, which would understate it by about 6.5%. The gate crossing is reported separately at 10.82 points because one suite withholding while the other acts is an authorization difference, not a probability-precision one, and both suites call this class correctly. That screen also answers the 0.25 question: the realization is **57.5%** of the analytic ceiling there, not 93.2%, because at 0.25 remaining gain exact restoration needs a 4.00 multiplier and the cap allows 2.00 — the action is cap-saturated throughout, and `maximum_gain_compensation` is therefore the binding limit on recoverable tracking at the condition the action screen will run on. Raising that cap would recover more but would re-open the severity channel it currently closes, so it is a joint control surface rather than a free parameter. **Detection, classification, severity accuracy, the severity-to-tracking conversion, and now the class-probability channel are all closed on the actuator class**; action-versus-no-action benefit, healthy false authorization, cap and floor sensitivity, and the source-specific margin remain the action screen's questions. Validation-sized multi-setting evidence, sensor-fault recovery design, the actuator action review, and the evaluation-sized paired control comparison remain open. The prospective non-contact noisy-reference follow-up still advances W=768 / stride=16 only as a development proposal; the shared immutable `config.json` remains unfrozen. The packet therefore does **not** yet implement the confirmatory experiment or the interactive verification artifact; neither a research result nor a frozen configuration may be inferred from these development sensitivities.

**Reviewer correction (2026-07-22):** The probability-channel claims in the final portion of the paragraph above are superseded by the narrower Step 17 interpretation. The continuous `[0.50, 1.00]` probability interval is sampled at six points; the **5.07-point** maximum is a monotone sampled development envelope, not an exact reachable-set bound or closure of every probability between grid points. A separate 0.025-spaced reviewer audit found the same maximum and monotone curves on all four seeds, which strengthens the empirical finding without turning it into a proof. Because the fixture holds abstention and a common RMS uncertainty fixed, calibrated probability-gate crossings, abstention, uncertainty authorization, and cap/floor sensitivity remain open. The class-probability channel and the actuator class are therefore not closed. `config.json` remains unfrozen.

**Current actuator-action status (2026-07-23):** Step 17A now measures the cap/floor and healthy false-authorization consequences that the earlier boundary left open. The lifecycle-safe selected cap-3 profile clears raw recovery but misses the source-specific magnitude gate; higher caps cross A1 safety. The bounded inverse-gain action family therefore blocks in development. This closes neither calibrated authorization rates nor the actuator class as a whole, and it is not validation or confirmatory evidence. The proposed different-task amendment was withdrawn before approval, so the existing Claim Sheet remains in force and `config.json` remains unfrozen.

## Current boundary

This packet reproduces the selected MuJoCo cable/rod mechanics, schema-v1.0 plant and sensor interfaces, causal online loop, evaluation core, detector/reference lifecycle, interpretable residual baseline, bounded task/contact controller, and the development screens through Step 17A. Schema Amendment A1 is jointly in force. A machine-readable schema, self-hashed draft-config contract, whole-group identity-manifest audit, role-file hash audit, and suite-scoped deployable observation loader now form the Gate 1–2 pre-confirmatory foundation. The tracked draft is explicitly non-confirmatory; no frozen `config.json`, populated live identity manifest, data generator, learned attribution head, or RMA head exists yet.

On the current bounded task, the structural suite has strong development information evidence, but structural recovery is blocked because the task has no structural tracking deficit and the tested action behaves like a generic controller retune. The actuator condition has headroom, yet the new source-specific action screen also blocks: safe cap-3 misses the 10-point specificity gate and higher caps violate A1 safety. The probability result remains a sampled empirical envelope; calibrated class-probability, abstention, and uncertainty authorization, sensor-fault recovery, and evaluation-sized paired control remain open.

The proposed different-task amendment was withdrawn before approval. The existing Claim Sheet remains in force, `config.json` remains unfrozen, and no development screen here is a confirmatory research result. Gate 2 still requires the live manifest/data-building path, Gate 3 requires a jointly approved draft assignment manifest before headline-model fitting, and the packet does not yet implement the full evaluation or interactive verification artifact.
