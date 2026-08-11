# Reproducibility Packet

This is the self-contained working packet for the Robot Structural Proprioception project. The current runnable surface reproduces the mechanics feasibility gate, emits a schema-v1.0 privileged trace from the selected MuJoCo cable plant, turns that trace into a deployable sensor suite's noisy observations, exercises the complete role-separated storage contract, validates the jointly approved Gate-3 scenario/split preregistration, generates its draft-authorized dev/pilot/validation base roles without touching test, and reproduces the first bounded development-only Gate-4 fit and in-sample readback. Later pipeline stages will be added here as they become final.

## Requirements

- Python 3.12
- A 64-bit Windows, Linux, or macOS machine supported by the pinned MuJoCo wheel

The feasibility spike is CPU-only and does not require a GPU or an external dataset.

The pinned `torch` backs the Gate-4 learned attribution rung (`scripts/utils/attribution_net.py`). **A GPU is not required to run anything in this packet**, including the whole test suite: the rung is about 4×10⁴ parameters and its tests are CPU-only. The recorded project machine used the same source version built for CUDA 12.8 (`torch==2.11.0+cu128`, for the RTX 5060 Ti's sm_120 kernels); `requirements.txt` records that invocation. The two devices agree to 5.960×10⁻⁸ on the class simplex under the precision context the module runs its forwards in, versus 8.842×10⁻⁵ under cuDNN's TF32 default — which is why the module pins the setting rather than inheriting it.

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

The suite covers model compilation, independent deformation-state availability, localized stiffness-fault construction, schema-facing output shapes, synchronous-feature and coefficient-reference correctness, the safe-probe, optional-contact-profile, matched-contact-pilot, bounded-task/contact, bounded noisy held-decision, structural-recovery-action, fault-tracking-deficit, severity-estimation-quality, cap-boundary, class-probability-channel, and actuator-recovery-action screen functions, the noisy healthy-reference pilot's causal window/reference logic, the estimator front and severity read-out, the Gate-4 learned attribution rung's causality (measured by perturbation, including that its normalization does not mix a window's later samples into its earlier features), suite-invariant capacity, seeded determinism, device agreement, and its refusal to report an attribution before trained weights with a recorded provenance are attached, the interpretable recovery controller and its shared seam regression, the linear system-ID residual baseline's role separation, suite-leakage guard, and real causal-seam integration, the plant/sensor interfaces, and the two-layer evaluation metrics and paired bootstrap.

It also covers the pre-confirmatory data contract: strict config canonicalization and self-hashing, draft/frozen lifecycle refusal, whole-group split integrity, matched C1/S common-random-number identity, manifest-bound writers and hash-checking loaders for every persisted role, suite-scoped deployable loading, unavailable-channel masking, an explicit non-test supervised label join, and rejection of labels, privileged truth, provenance, or extra payload keys at the observation boundary. The tracked draft can be checked directly:

```powershell
.\.venv\Scripts\python.exe scripts\validate_data_contract.py --schema schema\schema.json --config config\draft-config-v0.1.json
```

This command must report `status=draft` and `confirmatory=False`. It deliberately refuses confirmatory use. A future frozen `config.json` will be accepted only after every freeze field and manifest assignment is populated, all readiness gates are closed, and its raw canonical hash matches its filename-governed lifecycle state.

This deliberately runs the directory rather than an enumerated file list: an enumerated list goes stale silently every time a screen is added, and a test file the runbook never names is a test file an outside reader never runs. Step 18 is a focused subset for anyone debugging one area; it is not a substitute for this step.

Produces: terminal test and contract-validation results.

## Step 2A — Exercise the complete role-separated storage contract

Builds a small synthetic `dev`/`val` fixture through the same path-free manifest,
per-role roots, exact indexes, payload hashes, suite-scoped observation loaders,
and allowlisted observation-to-label join required by the eventual assigned
dataset. It writes plant, C1/S observations, labels, estimator outputs, and
controller logs for two complete matched pairs. The fixture is explicitly
contract-only: it is not a Gate-3 assignment, model fit, validation result, or
confirmatory dataset.

```powershell
.\.venv\Scripts\python.exe scripts\build_data_contract_fixture.py --output-root results\data_contract_fixture
```

The command fails if the output exists, any role violates `schema.json`, a
payload/index hash or identity mismatches, a training join requests `test`, or
the draft config attempts to materialize any `test` assignment.

Produces:

- `results/data_contract_fixture/manifest.csv`
- `results/data_contract_fixture/{plant,labels}/index.csv`
- `results/data_contract_fixture/observations/{C1,S}/index.csv`
- `results/data_contract_fixture/estimator_outputs/{C1,S}/index.csv`
- `results/data_contract_fixture/controller_logs/{C1,S}/index.csv`
- `results/data_contract_fixture/build_summary.json`

## Step 2B — Validate the approved Gate-3 scenario/split assignment

Validates the exact self-hashed assignment against the parent draft on which it
received same-state approval, then verifies the one-way approval wrapper now
embedded in the rehashed current draft. The assignment
predeclares split-owned ordinary/diagnostic trajectories; healthy, structural,
actuator, and sensor grids with held-out severities; explicit validation/test
compound-OOD cases; payload, temperature, and endpoint-contact confounds; five
model-training seeds; and a fault-independent balanced context-cell rotation.
Every fault setting in every split must realize the same complete eight-cell
payload/environment/contact factorial. Each trajectory/fault group must also
vary both profiles on every context axis, so trajectory identity cannot
deterministically reveal payload, environment, or contact.

```powershell
.\.venv\Scripts\python.exe scripts\validate_gate3_assignment.py
```

The tracked proposal expands to 808 whole scenario/fault reservations: 152 dev,
152 pilot, 168 validation, and 336 test. The added development/pilot repeats
remove the conservative trajectory-to-payload alias present at the smaller
budget. Test identities remain reservation-only.
The command writes no manifest or payload. It reports the approved assignment
hash, parent and current draft hashes, the exact authorized research splits,
and `test_materialization_allowed=false`. The assignment file itself remains
byte-for-byte unchanged from review; the current draft self-hash binds it and
the approval decision without rewriting the historical parent-hash claim.

Produces: terminal-only assignment audit results.

`scripts/embed_approved_assignment.py` is the one-time state-transition utility that
produced the tracked approval wrapper from the pre-approval parent draft and the exact
approved assignment. It atomically writes a rehashed draft, removes only the Gate-3 open
item, refuses an output named `config.json`, and never authorizes test materialization.
It is retained so that transition remains auditable and so a future jointly approved
replacement can use the same guarded path. It is **not** a recurring run step and must
not be rerun against the already-embedded current draft; the command above validates the
tracked result.

## Step 2C — Generate and audit the approved base research roles

Materializes the primary matched C1/S base dataset for every approved dev,
pilot, and validation reservation. Before the first rollout, the command
compiles and checks every assigned distal payload mass. Each rollout then uses
the assigned bounded trajectory, temperature profile, one-pair endpoint-contact
window, and plant/sensor fault components. Structural and actuator components
remain in the physical plant; encoder bias, drift, and dropout remain in the
sensor path. C1 and S share the approved random-number identities and their
common channels are compared bit-for-bit before persistence.

```powershell
.\.venv\Scripts\python.exe scripts\generate_assignment_dataset.py `
  --output ..\data\gate3-base-dev-pilot-val-c1-s `
  --suites C1 S `
  --workers 16
```

All plant and label payloads pass through
`DatasetRoleBuilder.make_writer`; observations pass through
`DatasetRoleBuilder.make_observation_writer`. The generated manifest is then
compared field-by-field with the approved reservations rather than trusted
because the generator produced it. Dataset identities use `train_seed=0`;
the five model-fit seeds are expanded only after those five fits exist.

The manifest and role indexes are suite-specific, so each matched C1/S pair
stores its privileged plant trace once under each suite's `run_id`. Those two
plant payloads are intentionally byte-identical and independently hash-audited;
the duplication preserves exact per-run role binding at the cost of about
1.4 GB in the current 472-pair build.

**Quality-control exclusion record (2026-07-24):** the first full generation
attempt was stopped after 193 of 472 reservations because its preflight had
compiled the six research-owned payload masses but not the two test-owned
scalar masses before the first research rollout. No test identity or payload
was created. The ignored partial dataset was excluded and removed, the
preflight was strengthened to compile all eight assigned masses, and the
retained dataset was regenerated from zero. Only the chronology-correct second
run is eligible for downstream use.

`--reservation-limit` and `--max-steps` are smoke-only switches and mark their
output `truncated_smoke_not_research_data`. The CLI accepts only
`dev|pilot|val` and the draft lifecycle independently refuses test rows. It
also refuses to overwrite an existing dataset root.

Produces:

- `../data/gate3-base-dev-pilot-val-c1-s/manifest.csv`
- `../data/gate3-base-dev-pilot-val-c1-s/{plant,labels}/index.csv`
- `../data/gate3-base-dev-pilot-val-c1-s/observations/{C1,S}/index.csv`
- `../data/gate3-base-dev-pilot-val-c1-s/generation_audit.json`

Run the independent on-disk audit after generation:

```powershell
.\.venv\Scripts\python.exe scripts\audit_assignment_dataset.py `
  --dataset-root ..\data\gate3-base-dev-pilot-val-c1-s
```

This reloads every indexed payload through the hash-checking loaders, rechecks
the manifest against the approved reservations, proves every paired plant file
is byte-identical, and compares all shared C1/S channels bit-for-bit.

Estimator outputs and controller logs remain intentionally pending Gate-4
fits; this base-role build is not a headline model fit, final `config.json`, a
test materialization, or a confirmatory result.

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

## Step 22 — Reproduce the delivered-dev structural separability screen

Development-only stop/go check on the delivered `dev` split: at the two reserved development structural severities (remaining EI 0.75 and 0.50), can any detector separate structure runs from healthy runs, and does the structural suite `S` beat the matched conventional suite `C1`? Every contrast is context-matched, cross-validation holds out a whole context cell, and an actuator positive control plus a paired label-permutation null bound the pipeline from both sides. This screen fits nothing that is carried forward and touches no split other than `dev`.

Requires the retained base dataset from Step 2C.

```powershell
.\.venv\Scripts\python.exe scripts\screen_structural_separability.py `
  --dataset-root ..\data\gate3-base-dev-pilot-val-c1-s `
  --output-dir results\structural_separability\pooled_trajectories
```

```powershell
.\.venv\Scripts\python.exe scripts\screen_structural_separability.py `
  --dataset-root ..\data\gate3-base-dev-pilot-val-c1-s `
  --trajectory-filter diagnostic `
  --output-dir results\structural_separability\diagnostic_trajectory_only
```

Produces `structural_separability_screen.json` and `structural_separability_screen_report.md` in each output directory. The result is **negative**: at the mild development severities neither suite separates structure. Read that result only at its own scope — the reports carry the four later narrowings (under-strength delivered probe, mismatched yardstick, wrong operation, wrong window origin) that bound what the negative means.

## Step 23 — Run the Protocol P replay gate

Protocol P is the pre-registered screen that decides whether the delivered diagnostic probe can make a structural stiffness-loss fault measurable above the healthy run-to-run null. Its specification is [`protocol/protocol-p-v2.3.3.md`](protocol/protocol-p-v2.3.3.md). Section 7 makes one-row exact reproduction a **stop-or-go precondition**: if rebuilding a single delivered reservation from the committed inputs does not reproduce the retained artifact exactly, the instrument that would produce the screen's numbers is not the instrument that produced the development dataset, and no result from it would be interpretable.

The gate checks invariant I1 (every pinned digest present and unchanged, each through its own hash domain — folded text for the protocol and assignment, exact bytes for the two `.npz` references) and invariant I2 (all 20 privileged plant fields and all 38 observed payload entries equal). It writes nothing: its output is stdout, and it inventories the data root, the packet tree and the repository's top-level files before and after the rollout. Any added, modified or removed watched file fails the gate.

```powershell
.\.venv\Scripts\python.exe scripts\protocol_p_replay_gate.py `
  --data-root ..\data\gate3-base-dev-pilot-val-c1-s
```

One MuJoCo rollout, about 26 s. Exit status is 0 only when every pinned digest matches, all 58 compared entries are equal, and the watched filesystem scopes are unchanged.

**This step needs the retained development dataset, which is not distributed with the packet** (see [`DATA.md`](DATA.md)); the two pinned reference payloads are local artifacts of the Step 2C generation, not committed data. Regenerating the dataset from Step 2C reproduces them. The gate's own comparison layer is covered portably by `tests/test_protocol_p_replay_gate.py`, which runs on a clean checkout with no dataset present.

## Step 24 — Reproduce Protocol P Stage 0 (sensor-only difference null)

Stage 0 is the first pre-registered measurement this project has executed. It asks the narrowest question in Protocol P: with **no plant, no mechanics, no fault and no rollout**, how far apart are two healthy four-gauge windows that differ only in their sensor draw? The answer characterizes the sensor-path component of the screen's difference statistic `D`, and nothing else.

**Read this step against Step 23, because the two have opposite reader-reproducibility status.** Step 23 cannot be run from the distributed packet: it needs the retained development dataset and one MuJoCo rollout. Step 24 needs **no dataset and performs no MuJoCo simulation**, draws every value from fixed seeds, and runs end to end on a clean checkout after Step 1. Its script imports no MuJoCo at all: the protocol constants and hashing rules it shares with Step 23 live in `scripts/utils/protocol_p.py`, which imports only the Python standard library. That is a checked property, not a claim — `tests/test_protocol_p_shared.py` loads the stage's script in a fresh interpreter and fails if a transitive plant dependency reappears.

The invocation is pre-registered in [`protocol/protocol-p-v2.3.3.md`](protocol/protocol-p-v2.3.3.md) §8. All seven values are also the script's defaults; they are written out because the protocol pins them and the script refuses any other combination.

```powershell
.\.venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py `
  --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 `
  --pairs 100 --seed 0 --pair-id 1
```

Produces `results/protocol_p/sensor_only_difference_null.json`. **Zero Protocol-P rollouts.** The recorded first run is:

```text
n pairs               100      (sensor seeds 0..199, consumed once, consecutive pairing)
mean                  0.278734
q95, method="higher"  0.400881   <- the reported statistic, in microstrain
identity              dev-71b332893d007036625f666589f8c74b0ac3b946b47b5186ddf8de6a2d8ce31e
```

Four boundaries govern how that number may be quoted, and all four are recorded inside the artifact itself:

- **It sets no threshold and gates no decision.** The artifact's `corroboration.authority` field reads `NONE`. The operative null for the screen's verdict is Stage C's per-cell `Q95_c`, which has not been measured. A damage signal smaller than `0.400881` is **not** thereby invisible; Stage 0 licenses no such statement.
- **Its corroboration is upper-tail containment, not agreement.** The same quantity measured earlier through the simulated physics — one healthy trace re-read under different sensor draws — gave `0.3176 / 0.3555 / 0.3854 / 0.4251` across four context cells. Stage 0's `0.400881` falls inside that range, which is the pre-registered check, but it **exceeds three of the four cells** and sits about 5.7% below the range maximum. "Inside the measured real-plant range" is supported. "Agrees with the real-plant null" is not.
- **The `dev-` prefix is permanent.** The identity is ineligible for confirmatory analysis by construction (invariant I8), and no Stage-0 value may enter the confirmatory comparison.
- **The identity binds the inputs, not the numbers.** `stage_0_identity` is the SHA-256 of the artifact's own `stage_0_canonical` string, so any reader can recompute it from the file alone. That string covers the stage label, the base config hash, both assignment digests, the protocol digest, the seven CLI values, and the sorted output schema — it does **not** cover the measured distances or the summary statistics. It is a provenance identity over the run's inputs and shape; it is not a tamper seal over its results. Verify a result by recomputing it from `samples.distances`, which the artifact records in full.

Two reader notes. `samples` is a six-key metadata dictionary (`n_pairs`, `seed_map`, `sensor_seeds_consumed`, `sensor_seeds_consumed_note`, `pair_id`, `distances`); the 100 values live in `samples.distances`, so `len(samples)` returns 6 and not 100. And `null_distribution.std` is the **population** standard deviation, not the sample one.

**First-run elapsed time: not captured.** No trustworthy timing measurement was recorded for the first run, so none is reported. The measurement itself is unaffected because Protocol P binds no elapsed time. Any later timing must be labelled as a separate reproduction rather than as the first run.

The run is deterministic given the pinned seeds and the pinned dependency versions in `requirements.txt`; no randomness is drawn outside them. Cross-platform bit-identity has **not** been measured, so compare a local run against the recorded values rather than assuming byte-identical output.

## Step 25 — Audit or reproduce the Protocol P Stage A/B/C screen

Stages A, B and C are the screen itself: Stage A measures nine admissible probe candidates in four context cells under three conditions and selects one, Stage B walks the ten-value remaining-stiffness ladder at the selected candidate, and Stage C builds the operative null from eight healthy replicates per cell. The tracked reference result is [`results/protocol_p/stage_abc_screen.json`](results/protocol_p/stage_abc_screen.json), SHA-256 `c48c2e4d3a8a84a5b10127afc2a7c0f4bacc0ae6290712546432058327008756`.

Start with the screen's *plan*, built by the same program that executes it from the same committed inputs. `--mode plan` resolves every bound input, verifies the pinned digests, derives the timing, enumerates the complete row inventory, audits its shape against the pre-registered counts, and exits **having run zero rollouts**. It is the cheapest available check that the executable form of Protocol P sections 8–9 agrees with the specification's arithmetic.

```powershell
.\.venv\Scripts\python.exe scripts\run_protocol_p_screen.py `
  --output-dir results\protocol_p_plan --mode plan
```

`--mode plan` is the default; `--mode execute` runs the screen and is the only way to spend a rollout. Measured cost of the plan path on the reference machine: **0.30–0.33 s**, no dataset, no MuJoCo simulation. The program does import the `mujoco` package — it shares the generator that builds each rollout's request, and that generator imports the plant — so this step needs a complete install from `requirements.txt` even though it simulates nothing. (Contrast Step 24, whose script imports no MuJoCo at all.)

The audited plan is:

```text
admissible candidates   9        {0.05, 0.10, 0.15} N x {0.125, 0.25, 0.5} ramp fraction
logical rows            180      Stage A 108   Stage B 40   Stage C 32
physical rollouts       168
reused rows             12
derived onset index     500      from onset_time_s = 1.0 s at control_dt_s = 0.002 s
window                  [1000, 1768)
```

**Read 180 and 168 together; either number alone misleads.** A *logical row* is a line in the results table. A *physical rollout* is a simulation that was actually run. Twelve logical rows consume a measurement an earlier row already paid for: two of Stage B's ten ladder values are the two severities Stage A already measured at the selected candidate, and Stage C's first healthy replicate in each cell is the healthy rollout Stage A already ran there. Those twelve rows cite the original rollout's provenance stamp rather than minting a new one, so the screen's cost is 168 simulations while its results table has 180 rows. A reader auditing "one provenance stamp per rollout" against this table will find 180 provenance references comprising 168 distinct stamps, and that is the designed relationship rather than a discrepancy.

Two things the plan output does **not** contain. There is no selected candidate: selection is a Stage-A result, so the inventory's shape is audited at a placeholder and the artifact says so in a `placeholder_selection_note` field. And `results` is `null`, because nothing was measured.

To reproduce the tracked result, run the same program in execute mode:

```powershell
.\.venv\Scripts\python.exe scripts\run_protocol_p_screen.py `
  --output-dir results\protocol_p --mode execute
```

Produces `results/protocol_p/stage_abc_screen.json`. The reference run selected **0.10 N / ramp fraction 0.25**. Three candidates failed the pre-registered hard gates on their first healthy cell and were dropped immediately, so the run spent **135 physical rollouts** rather than the plan's 168-rollout maximum: Stage A 75, Stage B 32, Stage C 28. It reports 147 logical rows because the twelve planned reuses remain present. The recorded rollout time is **4,432.16 s** inside the executor.

The pre-registered outcome is **Case B: a proper subset of the stiffness ladder passes**. Remaining-EI values 0.35, 0.40 and 0.45 are `TESTABLE` in all four cells; 0.50 through 0.90 are `SUB_THRESHOLD` under the required all-cell conjunction. No Stage-B or Stage-C body violated a hard gate. The artifact's construction readback also passes in all eight selected structural comparisons: each canonical record carries the requested link-stiffness fault at onset step 500 with the matched identity and sensor seed, and neither post-onset coefficient vector is bit-identical to its healthy counterpart. This readback blocks a silent dead-override path; it adds no magnitude threshold and no monotonicity requirement.

All four Stage-C cells also set `diagnostic_pause: true`: their `Q95_c` values range from 0.3703 to 0.4277 microstrain, above Section 8's 0.30-microstrain pause trigger. The protocol gives this flag no authority over the ladder verdict or outcome case; it is recorded here as a pre-registered diagnostic caution, not a second threshold.

Section 9 also pre-registers a **role-coverage read**, taken over the same ladder and costing no rollouts. The ladder's ten values are exactly the union of every split's known-class structural severities and the two structural OOD severities, so each split's testability can be counted off it directly. Reproduce it with:

```powershell
.\.venv\Scripts\python.exe scripts\analyze_protocol_p_role_coverage.py `
  --screen-result results\protocol_p\stage_abc_screen.json `
  --assignment config\proposed-gate3-assignment-v0.1.json `
  --output-dir results\protocol_p
```

Produces [`results/protocol_p/role_coverage.json`](results/protocol_p/role_coverage.json). The command is deterministic and re-running it rewrites the same bytes: every digest the artifact records — of the protocol specification, the assignment, and the screen result it reads — is taken over the document with line endings normalized, so a checkout that renders text files with Windows line endings and one that renders them with Unix line endings both produce an identical file. If the artifact you regenerate differs from the distributed one, an input differs, and the script names which.

```text
  split   known-class severities   testable    count
    dev   0.5, 0.75                --              0
  pilot   0.6, 0.85                --              0
    val   0.4, 0.9                 0.4             1
   test   0.35, 0.65               0.35            1
```

Section 9 keys a named consequence to a zero count in dev, val or test. **Dev is at zero, which yields a role-coverage-bounded non-transfer outcome: no testable structural training support.** Zero pilot relabels nothing but disables data-driven downsizing, so the prospectively allowed maximum test replication is retained and the limitation is named. Val and test are count-1 thin single-severity roles, which open no new terminal branch. OOD severities 0.45 and 0.55 never count toward any split, even though 0.45 is `TESTABLE` on the ladder.

One further read over the same artifact, also costing no rollouts, records **how much of that result is a statement about one payload**. The screen's four context cells are not exchangeable: two carry no distal payload and two carry 0.050 kg, while temperature environment and contact profile vary *within* each of those pairs rather than across them. That makes the screen a balanced two-level contrast in payload mass at every ladder value. Reproduce it with:

```powershell
.\.venv\Scripts\python.exe scripts\analyze_protocol_p_payload_conditioning.py `
  --screen-result results\protocol_p\stage_abc_screen.json `
  --assignment config\proposed-gate3-assignment-v0.1.json `
  --output-dir results\protocol_p
```

Produces [`results/protocol_p/payload_conditioning.json`](results/protocol_p/payload_conditioning.json), deterministic in the same sense as the role-coverage artifact above. **This read is not pre-registered.** It classifies nothing, opens no branch, and cannot move the outcome case or the coverage counts; the artifact says so in its own `authority` field. It exists because the size of a scope restriction is more useful written as a number than as a caveat.

```text
  remaining EI   mean d at 0.000 kg   mean d at 0.050 kg   ratio
          0.35            2.679957             1.344812   0.5018
          0.45            1.768199             0.883461   0.4996
          0.75            0.480152             0.250925   0.5226
          0.90            0.161944             0.086898   0.5366
   ratio across all ten ladder values: 0.4867 to 0.5366
```

Fifty grams of distal payload roughly halves the structural signature at every rung, while the operative null it is measured against does not move with payload (0.4114 and 0.4217 microstrain at the lighter level, 0.3703 and 0.4277 at the heavier). Signal falls, noise does not, so detectability falls with it: the ladder's zero-margin crossing is bracketed between remaining EI 0.60 and 0.65 in the unloaded cells and between 0.45 and 0.50 in the loaded ones. Because the verdict rule is a conjunction over all four cells, the loaded cells decide every rung, and the binding cell clears remaining EI 0.45 by 2.99% of its own threshold.

The consequence for reading the ladder is a scope statement, not a defect: the screen ran on development contexts by the protocol's own boundary, so every `TESTABLE` verdict was established at 0.000 and 0.050 kg and at no other mass. The reserved payloads rise across splits — pilot 0.025 and 0.075 kg, validation 0.100 and 0.125 kg, test 0.150 and 0.200 kg — so three of the four splits reserve at least one payload the ladder says nothing about. Two levels determine a ratio and nothing more: no functional form in payload mass is fitted here, and none should be read into it. What is established is the direction and its size at 0.050 kg.

This is a **development-screen result**, not a test of the project's headline hypothesis. `TESTABLE` means measurable under Protocol P's matched-signal / unmatched-null comparison, which the protocol explicitly notes favours S; it is necessary, not sufficient. Read together with the coverage counts, Case B says that at the selected probe the structural signature is measurable only at damage more severe than any known-class setting reserved for development or pilot. Every result identity remains `dev-`, `config.json` remains absent, and the confirmatory test split remains untouched.

## Step 26 — Reproduce the first development-only learned-model fit

The jointly reviewed trainer binds the exact delivered data root, manifest, role indexes,
assignment-derived causal windows, two suites and five predeclared network seeds. Plan mode
is the cheap audit: it resolves the training policy and enumerates all ten arms while
opening no observation, label or checkpoint payload and running no fit.

```powershell
$env:PYTHONPATH = "scripts"
.\.venv\Scripts\python.exe -m utils.dev_fit_trainer `
  --mode plan `
  --output-dir results\dev_fit_plan
```

Produces `results/dev_fit_plan/dev_fit_plan.json`: C1 and S at seeds 0–4, diagnostic
window `[1000, 1768)`, ordinary window `[900, 1668)`, 768 steps and one window per run.

The fit command must target a **new** output directory. It reads exactly 304 persisted
development rows—152 C1 and 152 S—and trains one 39,594-parameter rung-1 network for each
suite/seed arm. It generates no simulator data and spends no physical rollout.

```powershell
$env:PYTHONPATH = "scripts"
.\.venv\Scripts\python.exe -m utils.dev_fit_trainer `
  --mode fit `
  --data-root ..\data\gate3-base-dev-pilot-val-c1-s `
  --output-dir results\dev_fit_reproduced
```

Produces:

- `results/dev_fit_reproduced/dev_fit_result.json`
- `results/dev_fit_reproduced/dev_fit_{C1,S}_seed{0..4}.pt`

The checkpoints are rebuildable and ignored; the result document is their provenance
ledger. The tracked reference ledger is
[`results/dev_fit/dev_fit_result.json`](results/dev_fit/dev_fit_result.json), canonical
SHA-256 `f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e`.
It records `X_FIT_OK`, ten distinct checkpoint digests, 152 examples per arm, zero
rollouts and the exact code/data/assignment identity used by the run.

This is development fitting only. It does not read pilot, validation or test outcomes;
set a probability, abstention, OOD or uncertainty threshold; select a capacity; freeze
`config.json`; or establish a C1-versus-S result.

## Step 27 — Reproduce the bounded in-sample fit readback

The fit ledger stores the training loss total. That total is not a standalone learning
or ranking statistic: its Gaussian severity term includes a learned log-scale contribution
and may be negative. This read-only step verifies every checkpoint and bound input, then
persists the four post-fit loss terms separately together with in-sample accuracy,
macro-F1 and the paired five-seed spread.

```powershell
.\.venv\Scripts\python.exe scripts\analyze_dev_fit.py `
  --data-root ..\data\gate3-base-dev-pilot-val-c1-s `
  --fit-result results\dev_fit_reproduced\dev_fit_result.json `
  --checkpoint-dir results\dev_fit_reproduced `
  --output-dir results\dev_fit_reproduced
```

Produces `results/dev_fit_reproduced/dev_fit_analysis.json`. The tracked reference is
[`results/dev_fit/dev_fit_analysis.json`](results/dev_fit/dev_fit_analysis.json),
**canonical** SHA-256 `7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58`
— that is, the digest of the file's bytes with any CRLF folded to LF. Take it that way
rather than over the raw bytes: this repository is developed on Windows with
`core.autocrlf=true` and the path carries no `.gitattributes` pin, so a fresh checkout
renders this file with CRLF line endings and a *different* raw digest (measured on the
development machine: 14,591 bytes, 426 CRLF pairs). The fit ledger named in Step 26 has
no line endings at all — it is compact canonical JSON — so its raw and canonical digests
are the same number in every checkout.

```text
                         C1        S      empirical baseline
class cross-entropy    0.434     0.557          1.010
accuracy               0.870     0.817          0.632
macro-F1               0.682     0.650              -

paired S-C1 macro-F1 mean  -0.032
paired five-seed sample SD  0.150
```

Those scores are computed on the same 152 examples used to fit each arm. They show that
the executable model/data path optimizes above simple in-sample baselines and expose a
large seed-sensitivity warning before any later role is read. They do **not** establish
generalization, evidence against structural sensing, a capacity choice or a confirmatory
effect. The development role contains no OOD row, so the OOD head's all-zero-target loss
also says nothing about OOD behaviour.

## Step 28 — Audit or reproduce the Stage-1 capacity-sweep plan

Step 26 fitted one network width: the 39,594-parameter rung-1 network at 32 channels. The
**Stage-1 capacity sweep** repeats that development-only fit at five widths — 16, 24, 32, 40
and 48 channels — so the in-sample numbers can be read against network size instead of against
a single point. Its procedure, its arm list, its budget and, critically, the *sentences its
result is allowed to license* were all written down before any of the arms existed, in
[`protocol/capacity-escalation-v0.1.md`](protocol/capacity-escalation-v0.1.md), canonical
SHA-256 `05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002`. That document is
frozen. A correction to it bumps the version and renames the file; the executable pins the
digest, so editing it in place makes the step below refuse rather than silently run against
changed rules.

Only **width** varies. Depth is held fixed so every arm keeps the same 1,023-step receptive
field — a deeper network would change how much history the model sees, which is a different
experiment:

| channels | 16 | 24 | 32 | 40 | 48 |
|---|---:|---:|---:|---:|---:|
| parameters | 10,586 | 22,786 | 39,594 | 61,010 | 87,034 |
| receptive field (steps) | 1,023 | 1,023 | 1,023 | 1,023 | 1,023 |

### Plan mode — the free audit

Plan mode is the part an outside reader can run for nothing. It takes **no data root**, opens
no observation, label or checkpoint payload, runs no fit, and writes one canonical JSON
document describing every arm the run would fit and every file it would write:

```powershell
$env:PYTHONPATH = "scripts"
.\.venv\Scripts\python.exe -m utils.capacity_sweep `
  --mode plan `
  --run-label stage1-run-2 `
  --output-dir results\capacity_sweep_plan_reproduced
```

It prints `X_PLAN_OK: 40 new arms + 2 equivalence arms planned at run label stage1-run-2, 0
fits run` and produces `results/capacity_sweep_plan_reproduced/capacity_sweep_plan.json`.

Plan mode is **byte-deterministic**: the document carries no timestamp, no absolute path and no
random element, so the same code state and the same run label always produce the same bytes.
That is what makes it an audit rather than a description. The tracked reference plan for the
executed run is
[`results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json`](results/capacity_sweep/plans/stage1-run-2/capacity_sweep_plan.json),
canonical SHA-256 `ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31`, 13,786
bytes. Point `--output-dir` at a scratch directory and compare the bytes; the comparison *is*
the check. Re-measured for this runbook at three independent destinations on the recorded
machine: one digest, matching the tracked plan exactly.

A second tracked plan sits one directory up, at
`results/capacity_sweep/capacity_sweep_plan.json`, canonical SHA-256 `bdf674d5…1bf1c0a5`. It is
**superseded and deliberately kept**: it is the plan a first, failed run consumed, and the
executable now refuses it with *"the authorized plan was written by a different code state."*
Do not delete it or `results/capacity_sweep/stage1-run-1/`; both are the preserved evidence for
the defect described at the end of this step.

### Execute mode — what it did, what it costs, and what a new label requires

Execute mode is the expensive half. It claims a fresh run root, checks that the
width-parameterized constructor reproduces the already-approved 32-channel network bit for bit
(two equivalence arms), and then fits the forty new arms. The run label comes from the approved
plan, not from a separate execute-mode argument. A genuinely new run therefore needs a new plan
and that plan's own digest:

```powershell
$env:PYTHONPATH = "scripts"
$CAPACITY_RUN_LABEL = "stage1-reproduction"
$CAPACITY_PLAN_DIR = "results\capacity_sweep_plan_new_run"
.\.venv\Scripts\python.exe -m utils.capacity_sweep `
  --mode plan `
  --run-label $CAPACITY_RUN_LABEL `
  --output-dir $CAPACITY_PLAN_DIR
$CAPACITY_PLAN = Join-Path $CAPACITY_PLAN_DIR "capacity_sweep_plan.json"
$CAPACITY_PLAN_SHA256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $CAPACITY_PLAN).Hash.ToLowerInvariant()
.\.venv\Scripts\python.exe -m utils.capacity_sweep `
  --mode execute `
  --base-dir results\capacity_sweep `
  --data-root ..\data\gate3-base-dev-pilot-val-c1-s `
  --approved-plan $CAPACITY_PLAN `
  --approved-plan-sha256 $CAPACITY_PLAN_SHA256
```

This is a **conditional new-run command, not a clean-clone recovery procedure**. Before it can
fit anything, the executable requires the exact ten original Step-26 checkpoint bytes under
`results/dev_fit/` and authenticates them against the tracked ledger. A fresh clone does not
contain those files, so it will fail closed at the equivalence gate. The command is useful on
the recorded machine, or on a machine to which those exact authenticated checkpoint files have
been transferred; it is not sufficient on the packet contents alone.

The recorded run took **439.6 s** on the machine described in [`DATA.md`](DATA.md) and spent 42
fits and 42 checkpoints with **zero simulator generation runs and zero physical rollouts**. It
read exactly the 304 delivered development rows (152 C1 + 152 S) and no pilot, validation or
test row. Its terminal record is
[`results/capacity_sweep/stage1-run-2/capacity_sweep_result.json`](results/capacity_sweep/stage1-run-2/capacity_sweep_result.json),
canonical SHA-256 `0d8a1c2de7208cc9a551d75ce44e3a64f02de6c9881b4b31f4df4d07cc7f7a2a`, exit
`X_SWEEP_OK`, both equivalence arms `PASS`.

**The run label must be new.** The executable binds its output root to
`<base-dir>/<run-label>/` and claims that directory atomically, so re-using a spent label is
refused rather than silently overwritten. That is deliberate: a second execution is a second
measurement and has to be visible as one.

### The 67 original checkpoints are not in this repository — the honest boundary

Every `.pt` file this project has produced is git-ignored, and none is tracked. There are 67 of
them on the recorded machine:

| where | count | produced by |
|---|---:|---|
| `results/dev_fit/` | 10 | Step 26 (the 32-channel anchor arms) |
| `results/capacity_sweep/stage1-run-2/channels_{016,024,040,048}/` | 40 | Step 28 execute mode |
| `results/capacity_sweep/stage1-run-2/_equivalence/` | 2 | Step 28's equivalence gate |
| `results/capacity_sweep/stage1-run-1/` | 3 | the failed first run, preserved as evidence |
| `results/rung2_escalation/rung2-run-1/` | 10 | Step 30 execute mode (the rung-2 arms) |
| `results/rung2_escalation/rung2-run-1/_equivalence/` | 2 | Step 30's equivalence gate |

There is no `channels_032/` directory in the completed run, and that is correct rather than
missing: the ten 32-channel arms were **reused** from Step 26 instead of refitted, which is why
the sweep costs 42 fits and not 52.

What that means for a clean machine, stated plainly rather than waved at:

- **The tracked JSON records are the durable evidence.** The plan, the terminal run record and
  the analysis in Step 29 are all committed, and each is bound to the others by digest, so
  their mutual consistency can be re-checked on any machine with no checkpoint present.
- **Step 26 can fit a new set of ten anchors, but it does not restore the approved anchors.**
  Its reproduction command writes under `results/dev_fit_reproduced/`. The capacity-sweep
  executable is deliberately hard-bound to the tracked ledger and analysis under
  `results/dev_fit/`, and to the exact checkpoint digests named there; it has no argument that
  can substitute a newly fitted anchor set. Copying different bytes into the approved directory
  is refused rather than treated as recovery.
- **A new capacity experiment from rebuilt anchors needs a new reviewed boundary.** It would
  need an executable and plan that authenticate the new anchor ledger and analysis. That design
  does not exist in this packet. The recorded run's two equivalence arms establish bitwise
  reproduction of the approved 32-channel network *on the recorded machine* only; they are not
  a cross-machine restoration claim.
- **Step 29 cannot be re-driven against the tracked analysis on a machine that lacks these
  checkpoints**, because the analyzer reloads and re-scores the ten approved anchors and forty
  completed curve checkpoints from disk. That is a real, disclosed limitation of this packet,
  not something the runbook assumes away.
- **Step 31 has the same limitation for the same reason.** This table is the packet-wide
  checkpoint boundary rather than a Step-28 detail; it is written here because Step 28 is where
  the question first arises, and Steps 30 and 31 inherit it unchanged.

### Why there is a failed run in the tree

The first execution stopped itself after three of forty-two fits at exit `X_OUTPUT_DIRTY`. Its
output-cleanliness check ran once per *arm* against a directory that ten arms share, so the
second arm at the first width tripped the guard against the first arm's own output. Under any
plan, that executable could never have finished a sweep. The repair moves the check to once per
capacity point, above the equivalence gate. `results/capacity_sweep/stage1-run-1/` is kept
because it is the evidence that diagnosis rests on.

## Step 29 — Read the completed sweep against its pre-registered interpretation

The read is a separate, **read-only** script. It imports the pure functions that define the
shape classification from the executable rather than restating them, re-authenticates every
input by digest, reloads and re-scores all fifty checkpoints, and only then derives the
descriptive summary. The exact command is copy-paste complete below, but it succeeds only when
the ten approved anchor and forty completed curve checkpoint files are present with their
recorded digests:

```powershell
.\.venv\Scripts\python.exe scripts\analyze_capacity_sweep.py `
  --data-root ..\data\gate3-base-dev-pilot-val-c1-s `
  --sweep-result results\capacity_sweep\stage1-run-2\capacity_sweep_result.json `
  --sweep-result-sha256 0d8a1c2de7208cc9a551d75ce44e3a64f02de6c9881b4b31f4df4d07cc7f7a2a `
  --approved-plan results\capacity_sweep\plans\stage1-run-2\capacity_sweep_plan.json `
  --approved-anchor-analysis results\dev_fit\dev_fit_analysis.json `
  --run-root results\capacity_sweep\stage1-run-2 `
  --anchor-checkpoint-dir results\dev_fit `
  --output-dir results\capacity_sweep_analysis_reproduced
```

All eight arguments are required and none has a default; in particular the result's digest is
supplied at the invocation, so the result and the plan cannot end up authenticating only each
other. The writer is an **exclusive create** — it refuses to overwrite an existing analysis —
so reproducing this step needs a fresh output directory. The tracked reference is
[`results/capacity_sweep_analysis/stage1-run-2/capacity_sweep_analysis.json`](results/capacity_sweep_analysis/stage1-run-2/capacity_sweep_analysis.json),
canonical SHA-256 `e381d12eafcf04c80d42aaed1bd9775bf9fbd64f1db166be535de356b7642736`, 89,150
bytes, written by exactly one invocation.

### What the record contains

Fifty arms — five widths × two suites × five seeds — forty fitted by the sweep and ten reused
from Step 26. The per-point in-sample means are exact record contents:

```text
channels     C1 mean     S mean     paired S-C1 mean     paired 5-seed SD
    16      0.430980   0.414009        -0.016971             0.109761
    24      0.648202   0.654213         0.006011             0.163331
    32      0.682287   0.650198        -0.032089             0.149636
    40      0.744294   0.688848        -0.055445             0.191773
    48      0.852379   0.701461        -0.150918             0.155432
```

### What may be said about them, and what may not

The frozen design contains a six-row table, written in advance, mapping the shape of these
curves onto the sentences the result is permitted to license. Applied to the record, **exactly
one row matches**, and the reading it licenses is, in the design's own words:

> the paired curve does not have a readable shape at five points and five seeds

and **any trend statement is forbidden**. The five numbers above may be quoted as record
contents. They may **not** be joined into a direction, a slope, a "widens", a "closes" or a
"does not move" — which is why this runbook prints them as a table and stops there.

The row that *nearly* matched is the part worth a reader's attention, because it is the reason
for writing the table down in advance at all. It would have licensed *"the difference did not
move by more than the anchor's own seed spread"* — the sentence a person reading these five
numbers casually would reach for. It fails on both of its conditions, independently: the paired
curve's shape is non-monotone rather than flat-or-declining, **and** the paired range across
the five points, 0.156930, exceeds the 32-channel anchor's own five-seed sample SD, 0.149636.
Either failure alone blocks it. The table was written before any of these arms existed, and it
blocked the comfortable reading twice over.

### The boundary block, and whose spend it describes

The analysis document carries a `boundary` block reading `fits_run 0`, `generation_runs 0`,
`rollouts_spent 0`, `non_dev_reads 0`. **Those are true of the reader, not of the run it
reads.** The sweep itself spent 42 fits and wrote 42 checkpoints, and it is Step 28's terminal
record that reports that spend. Wherever an analyzer's boundary block is quoted — here, in Step
27, or in a later report — it describes the analyzer's own cost; read the producing run's own
record for the producing run's cost.

### What this step does not do

It selects no capacity, sets no threshold, establishes nothing about generalization, and says
nothing about C1 versus S. It reads only the development split. It authorizes no wider ladder,
no new seed count, no architecture change and no later-role read; each of those is a separate
decision with its own review. The 32-channel result reported in Step 27 is untouched by it and
stands exactly as it did.

## Step 30 — Reproduce the rung-2 escalation module, plan and completed run

Slot 9's capacity ladder has a second rung, and Step 30 is the run that put a fit on it. The
architecture is a different *kind* of network rather than a wider copy of the first: a strided
convolutional stem feeding a two-layer GRU and a single-head temporal attention pool, built by
[`scripts/utils/attribution_net_rung2.py`](scripts/utils/attribution_net_rung2.py) at **219,018
parameters** with a **stem receptive field of 31 samples**. Rung 1 is 39,594 parameters with a
1,023-sample receptive field, so the two rungs differ in capacity and in temporal reach at once.
That is a deliberate property of the frozen design, not an accident, and it is the first reason
nothing here compares the two rungs as points on a curve.

Everything the run is permitted to do is fixed in advance by
[`protocol/rung2-escalation-v0.1.md`](protocol/rung2-escalation-v0.1.md), SHA-256
`9a154f902d7a98dcaa3e8bd34109e2ea6c4f29ba08c86a4ad301bfd62e69bf1f`. The executable embeds that
digest, so editing the design in place turns plan mode red rather than silently authorizing a
different experiment.

Plan mode is free and writes no checkpoint:

```powershell
$env:PYTHONPATH = "scripts"
.\.venv\Scripts\python.exe -m utils.rung2_escalation `
  --mode plan `
  --run-label rung2-reproduction `
  --output-dir results\rung2_escalation_plan_new_run
```

Execute mode is the expensive half. It claims a fresh run root bound to
`<base-dir>/<run-label>/`, refits the two approved rung-1 checkpoints to prove the fitting loop
still reproduces them bit for bit, and only then fits the ten rung-2 arms:

```powershell
$env:PYTHONPATH = "scripts"
$RUNG2_PLAN = "results\rung2_escalation_plan_new_run\rung2_escalation_plan.json"
$RUNG2_PLAN_SHA256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $RUNG2_PLAN).Hash.ToLowerInvariant()
.\.venv\Scripts\python.exe -m utils.rung2_escalation `
  --mode execute `
  --base-dir results\rung2_escalation `
  --approved-plan $RUNG2_PLAN `
  --approved-plan-sha256 $RUNG2_PLAN_SHA256 `
  --data-root ..\data\gate3-base-dev-pilot-val-c1-s
```

The same honest boundary as Step 28 applies, for the same reason: the equivalence gate
authenticates the ten original `results/dev_fit/` checkpoint files against the tracked ledger,
and a fresh clone does not contain them, so this command fails closed on the packet contents
alone. The run label must be new — the run root is claimed atomically and a spent label is
refused rather than overwritten.

The recorded run executed once, in one invocation, and its tracked records are:

```text
results/rung2_escalation/plans/rung2-run-1/rung2_escalation_plan.json
  canonical == raw SHA-256  b51b0009e25cbd4816ea3eabed033cb1579780dd468c78e0a21e8a1e78941040
results/rung2_escalation/rung2-run-1/rung2_escalation_result.json
  canonical == raw SHA-256  9d94b03ee5825b15c3e09d612a9ebdfdcddb959d068ea35da899dbb35ae996ed
  33,038 bytes, exit X_RUNG2_OK
results/rung2_escalation/rung2-run-1/_equivalence/rung2_escalation_equivalence.json
  canonical == raw SHA-256  ddcb5fedeafffda5ebf19f6b973b410f95801c407d9af9302a8ecf7268b4e936
  6,261 bytes, both equivalence arms PASS
```

It spent **12 fits and 12 checkpoints — two equivalence arms plus ten rung-2 arms — with zero
simulator generation runs, zero physical rollouts and zero non-development reads**, and it read
exactly the 304 delivered development rows (152 C1 + 152 S). It took **1,274.6 s** on the
machine described in [`DATA.md`](DATA.md).

That runtime is worth stating next to Step 28's, because it is a result in its own right and an
inconvenient one. Rung 2 carries **5.5× rung 1's parameters** but costs roughly **12× per
optimizer step**: a GRU's timesteps are sequential and do not parallelize across a CPU the way a
dilated convolution stack does. On the hardware this project actually has, the cheaper-looking
axis of the ladder is not the cheaper axis to climb.

## Step 31 — Read the completed rung-2 run against its pre-registered interpretation

The read is a separate, **read-only** script that fits nothing. It re-authenticates every input
by digest, reloads and re-scores all twelve checkpoints, requires each re-scored value to equal
the persisted one exactly, and only then derives the descriptive summary. All nine arguments are
required and none has a default:

```powershell
.\.venv\Scripts\python.exe scripts\analyze_rung2_escalation.py `
  --data-root ..\data\gate3-base-dev-pilot-val-c1-s `
  --run-result results\rung2_escalation\rung2-run-1\rung2_escalation_result.json `
  --run-result-sha256 9d94b03ee5825b15c3e09d612a9ebdfdcddb959d068ea35da899dbb35ae996ed `
  --equivalence-artifact results\rung2_escalation\rung2-run-1\_equivalence\rung2_escalation_equivalence.json `
  --approved-plan results\rung2_escalation\plans\rung2-run-1\rung2_escalation_plan.json `
  --approved-fit-ledger results\dev_fit\dev_fit_result.json `
  --approved-anchor-analysis results\dev_fit\dev_fit_analysis.json `
  --run-root results\rung2_escalation\rung2-run-1 `
  --output-dir results\rung2_escalation_analysis_reproduced
```

The result's digest is supplied at the invocation rather than read from the result, so the run
record and the plan cannot end up authenticating only each other. The writer is an **exclusive
create** and refuses to overwrite an existing analysis, so reproducing this step needs a fresh
output directory. The tracked reference is
[`results/rung2_escalation_analysis/rung2-run-1/rung2_escalation_analysis.json`](results/rung2_escalation_analysis/rung2-run-1/rung2_escalation_analysis.json),
canonical == raw SHA-256
`604d72724b4cf11a97ce0af836ecef1163442e9ff7e6423aa2fd0fad9556951c`, 40,270 bytes, written by
exactly one invocation and reviewed independently by both agents against those exact bytes.

### What may be said about the record, and what may not

The frozen design contains an **ordered** status table and a sign table, both written before any
of these arms existed. The status table is read top to bottom and exactly one row matches; the
sign table applies only after the successful status row. Applied to this record, the two
sentences the design licenses are, in its own words:

> Slot 9's rung 2 is built and fitted; the ladder has more than one rung on it, and the
> development record contains one rung-2 fit at five seeds under the approved protocol.

> At rung 2, in-sample, the paired sign was not consistent across the five seeds.

The paired macro-F1 signs behind the second sentence are **two negative, one zero and two
positive** across seeds 0–4. Attaching *because*, *so*, *therefore*, *which shows*,
*capacity-bound*, *resolves* or *confirms* to either sentence is explicitly forbidden by the
design, and the two sentences do not become evidence by being placed next to each other.

The artifact also persists a `rung2_minus_rung1` block. **No row of the interpretation table
licenses any sentence about it.** Two rungs are two points; no trend, slope or direction may be
asserted across them, and this runbook therefore names the block and stops, rather than printing
figures whose only use would be the comparison the design forbids. A reader who wants them can
open the tracked artifact, which is exactly why it is tracked.

### The part a reader must not be allowed to miss

The status sentence above says the objective-reduction check passed. That check is
**deliberately weak**, and the frozen design says so in writing, before any of this ran: the
training objective includes a severity Gaussian-NLL term that can drive the total down without
classification improving, so `OBJECTIVE_REDUCED` is explicitly *not* a learning signal. What the
record contains is the case that warning describes.

Every one of the ten rung-2 arms scores **F1 = 0.000000 on `healthy` and 0.000000 on
`structure`**. Four of them — C1 seeds 0 and 4, S seeds 0 and 3 — sit exactly at the artifact's
own recorded majority-class baseline of accuracy `0.631579` and macro-F1 `0.193548`, which is
what answering `sensor` to all 152 development examples produces on the 8 / 32 / 96 / 16
healthy / actuator / sensor / structure census. The other six score a non-zero `actuator` F1 and
nothing else. The ten rung-1 anchors carried in the same artifact each have four non-zero
per-class values.

Three things follow, and no more than three:

- **The zeros are on both sides, not merely equal.** Where the paired per-class comparison shows
  a tie, it is two zeros, and the macro-F1 tie at seed 0 is both arms sitting at the majority
  value. A sign count over those cells is arithmetically correct and descriptively hollow.
- **This is not a recording error.** The reader re-scored all twelve checkpoints from
  authenticated bytes and required *exact* equality with the persisted accuracy, macro-F1 and
  per-class F1. The read reached `X_ANALYSIS_OK`, so that equality held on every arm.
- **This is not the failure path either.** The design's failure branches are an equivalence
  failure, an incomplete run and an objective-check failure. None occurred. Reading the failure
  path as "or anything else that looks disappointing" would make writing it down in advance
  meaningless.

No cause is attached here — not capacity, not protocol, not optimization, not data. The
observation is direct persisted record content, placed next to the licensed sentences so that
neither can be read without it.

### What this step does not do

It selects no rung, no capacity and no threshold, establishes nothing about generalization, and
says nothing about C1 versus S. It reads only the development split. It authorizes no retry, no
wider ladder, no architecture change and no later-role read. Both the run and the read were
single, separately authorized invocations, and both authorizations are spent; a further run
needs a new label, a new plan and a fresh joint authorization.

## Data

No external dataset is required. The simulator generates every value used by the spike. See [`DATA.md`](DATA.md) for the data and licensing boundary.

## Dependency licenses

| Dependency | Version | License | Role |
|---|---:|---|---|
| MuJoCo | 3.10.0 | Apache-2.0 | Cable/rod and volumetric-flex dynamics |
| NumPy | 2.5.1 | BSD-3-Clause and bundled permissive notices | Numeric arrays and metrics |
| Matplotlib | 3.11.0 | PSF-based/BSD-compatible | 300-DPI figures |
| pytest | 9.1.1 | MIT | Focused tests |
| PyTorch | 2.11.0 | BSD-3-Clause | Gate-4 learned attribution rung |

All are free and commercial-use-permitting. Project-owned code and configurations are MIT-licensed; packet prose and figures are CC BY 4.0. The copy-ready attribution and exact scope statement are in [`DATA.md`](DATA.md).

## Historical boundary (superseded in part)

This packet reproduces the mechanics gate, detector-floor correction, safe-probe co-design screen, noisy healthy-reference pilot, optional endpoint-contact profile screen, matched contact-enabled development pilot, bounded task/contact/controller redesign, bounded noisy held-decision information review, structural recovery action-family screen, and the per-class fault tracking-deficit screen, and it connects the selected MuJoCo plant's **real persisted privileged output** to the sensor-realism model. Schema Amendment A1 is jointly in force. The causal one-step plant→sensor→policy loop and estimator front exist and are tested. The permanent `CoefficientReferenceDetector` uses the pilot's canonical score statistic with fail-loud reference/threshold lifecycle guards, and the jointly approved interpretable gain-scheduled recovery-controller floor plugs into the same seam; neither is a completed control result. A new `LinearResidualAttributionEstimator` supplies the Claim-Sheet-required interpretable baseline: it fits healthy deployable one-step ARX dynamics, builds four transparent residual-pattern prototypes in a separate development role, and calibrates off-prototype abstention on a third role. Its synthetic separation and real-seam checks are mechanism tests only. The learned attribution and RMA heads are still unbuilt. The fixed two-field contact role enables collision solely between the distal endpoint segment and an explicit plane, extracts MuJoCo's constraint-force truth, and drives the seventh privileged safety flag; the default model remains collision-disabled. The earlier short open-loop grid advanced z = 0.100 m to matched pilot review, but the matched pilot **blocked** it: S's contact-conditioned scheduled-decision signal came with 8.3% healthy false alarms, the pilot-only continuous prototype was phase/reference-unstable, and the selected plane produced repeated contacts plus privileged joint-angle safety violations over onset+5 s. The bounded redesign advanced z = 0.200 m as the lowest all-source mechanics/lifecycle candidate under deployable encoder feedback, one held scheduled diagnosis, a post-decision finite contact excursion, and zero A1 flags over onset+5 s. Replacing its fixed diagnoses with resolved-tail noisy references now advances the **information/reference lifecycle only**: S reaches 0.995 held-out macro-F1 and 100% structural recall versus C1's 0.704 and 8.3%, with 2.1% versus 4.2% healthy false alarms. The old structural derate remains blocked because it worsens `J_5s` by 18.6%. A predeclared inverse-stiffness multiplier family then found 19–20% structural tracking reductions with no A1 or saturation events, but the selected 2.0× multiplier improved healthy tracking slightly more than the structural-fault case; the source-specificity gate therefore **blocks** it as a generic nominal-controller retune, not structural recovery. The follow-on no-recovery headroom screen now shows why: no structural severity from 0.75 down to 0.05 remaining EI reaches the development gate — its deficit falls to zero and then turns negative while peak strain rises monotonically from 19.2 to 259.7 µε — while 0.25 remaining actuator gain advances with a 23.03% minimum disjoint deficit and the fixed 0.05 rad encoder-bias control produces a 15.69% mean deficit. The structural control path is therefore blocked on this bounded task even though its strain signature remains informative; the next action screen belongs to the actuator condition, not to another structural multiplier family. That advance authorizes an action screen only: the contract's paired S-minus-C1 tracking difference is already recorded as exactly zero on the actuator and sensor classes under a pinned severity, so control-layer headroom on a class C1 also detects does not by itself become a Slot-11 win. The severity-estimation-quality screen narrows but does **not** close the severity route. Both suites estimate remaining gain accurately (held-out MAE 0.0065 C1 / 0.0076 S), and every strictly capped-interior arm commands identically, but the above-bar 0.50 remaining-gain condition sits exactly at the recorded cap-2 kink. Held-out estimates straddle it, producing different C1/S multipliers on 3 of 4 paired boundary arms. The cap-boundary action screen, jointly approved in its reviewer-corrected state, measured what that difference is worth in tracking, and it is small: the paired S-minus-C1 reduction is **−0.12% on average and at most 0.52% on any seed** against a 10% bar, on a condition where the action itself is real (+13.11% no-action deficit, +10.81% recovered by a privileged oracle). Across the measured multiplier range 1.50–2.00, the reduction moves by only **3.81 percentage points**. That is an empirical envelope for the recorded linear heads, not a universal bound on an arbitrary future linear or learned read-out that could command outside the sweep. The screen closes the **recorded linear-read-out severity route** on the actuator class at the recorded cap and condition; it does not close arbitrary future read-outs, the actuator class, or the cap-4 / 0.25-floor boundary. The uncertainty diagnostics also require distinct roles. A fixed-penalty leave-one-tuning-seed-out calibration estimate exceeds the in-sample dispersion by 1.59x for C1 and 5.72x for S, while the genuinely disjoint assessment residual dispersion exceeds it by 1.98x for C1 and 4.12x for S. The absolute suite ranking does not survive across those diagnostics: S has the larger internal calibration dispersion but a slightly smaller assessment standard deviation, while its assessment mean absolute error remains larger because its bias is larger. The safe conclusion is that the training residual must not be handed to the confidence gate; both calibration-role values clear that gate, but they are development estimates rather than frozen margins. Finally, exact restoration of the gain does not exactly restore the tracking on this boundary condition — the oracle realizes 93.2% of the analytic `deficit -> reduction` ceiling, in the same direction on every seed — because error accumulated before the held decision cannot be recovered later. The class-probability channel screen then measured both of the things that left open. At the selected 0.25 condition the severity channel is **structurally flat** — the cap binds for every estimate at or below 0.50, roughly 25x the recorded error scale away from the true value — so class probability is the only channel that can still separate two suites there. That channel is closed at both ends by recorded controller constants, the confidence gate below and the compensation cap above, which makes its sweep a **reachable-set span rather than a chosen-range envelope**: the widest paired difference two gate-clearing suites can produce through it is **5.07 percentage points**, mean 5.02, against a 10-point bar, reported in the contract's own `100 x (J_C1 - J_S) / J_C1` units rather than as a difference of no-action reductions, which would understate it by about 6.5%. The gate crossing is reported separately at 10.82 points because one suite withholding while the other acts is an authorization difference, not a probability-precision one, and both suites call this class correctly. That screen also answers the 0.25 question: the realization is **57.5%** of the analytic ceiling there, not 93.2%, because at 0.25 remaining gain exact restoration needs a 4.00 multiplier and the cap allows 2.00 — the action is cap-saturated throughout, and `maximum_gain_compensation` is therefore the binding limit on recoverable tracking at the condition the action screen will run on. Raising that cap would recover more but would re-open the severity channel it currently closes, so it is a joint control surface rather than a free parameter. **Detection, classification, severity accuracy, the severity-to-tracking conversion, and now the class-probability channel are all closed on the actuator class**; action-versus-no-action benefit, healthy false authorization, cap and floor sensitivity, and the source-specific margin remain the action screen's questions. Validation-sized multi-setting evidence, sensor-fault recovery design, the actuator action review, and the evaluation-sized paired control comparison remain open. The prospective non-contact noisy-reference follow-up still advances W=768 / stride=16 only as a development proposal; the shared immutable `config.json` remains unfrozen. The packet therefore does **not** yet implement the confirmatory experiment or the interactive verification artifact; neither a research result nor a frozen configuration may be inferred from these development sensitivities.

**Reviewer correction (2026-07-22):** The probability-channel claims in the final portion of the paragraph above are superseded by the narrower Step 17 interpretation. The continuous `[0.50, 1.00]` probability interval is sampled at six points; the **5.07-point** maximum is a monotone sampled development envelope, not an exact reachable-set bound or closure of every probability between grid points. A separate 0.025-spaced reviewer audit found the same maximum and monotone curves on all four seeds, which strengthens the empirical finding without turning it into a proof. Because the fixture holds abstention and a common RMS uncertainty fixed, calibrated probability-gate crossings, abstention, uncertainty authorization, and cap/floor sensitivity remain open. The class-probability channel and the actuator class are therefore not closed. `config.json` remains unfrozen.

**Current actuator-action status (2026-07-23):** Step 17A now measures the cap/floor and healthy false-authorization consequences that the earlier boundary left open. The lifecycle-safe selected cap-3 profile clears raw recovery but misses the source-specific magnitude gate; higher caps cross A1 safety. The bounded inverse-gain action family therefore blocks in development. This closes neither calibrated authorization rates nor the actuator class as a whole, and it is not validation or confirmatory evidence. The proposed different-task amendment was withdrawn before approval, so the existing Claim Sheet remains in force and `config.json` remains unfrozen.

## Current boundary

This packet reproduces the selected MuJoCo cable/rod mechanics, schema-v1.0 plant and sensor interfaces, causal online loop, evaluation core, detector/reference lifecycle, interpretable residual baseline, bounded task/contact controller, and the development screens through Step 17A. Schema Amendment A1 is jointly in force. A machine-readable schema, self-hashed draft-config contract, whole-group identity-manifest audit, suite-scoped deployable observation loader, schema-driven writers/loaders for every non-observation role, and an explicit `dev|pilot|val` supervised label join now form the Gate 1–2 pre-confirmatory foundation. Step 2A exercises those boundaries end to end on a synthetic role-completeness fixture and hard-refuses `test` under the draft lifecycle. Step 2B validates the jointly approved 808-reservation Gate-3 assignment against its exact parent draft and the rehashed current approval wrapper. Step 2C implements the real assignment-driven base-role generator and an independent on-disk audit: exact distal payload inertia, split-owned temperature and contact windows, compound plant/sensor faults, direct approved-reservation/manifest comparison, hash-checked role loading, byte-identical paired plant truth, and bitwise shared-channel checks. The tracked draft remains explicitly non-confirmatory; no frozen `config.json` and no RMA head exists yet, and test materialization remains forbidden. The **learned attribution head now has one completed development-only rung-1 fit**: `scripts/utils/attribution_net.py` builds the 39,594-parameter, 1,023-sample-receptive-field network; `scripts/utils/dev_fit_contract.py` enforces the exact dev-only data/seed/provenance bounds; and `scripts/utils/dev_fit_trainer.py` ran the ten matched C1/S seed arms after both agents approved its exact executable state. The tracked ledger and Step-27 readback preserve ten checkpoint digests, 152 examples per arm, separate post-fit loss terms and the in-sample metrics without treating them as held-out evidence. Unfitted instances still abstain, split `p_class` uniformly and report `severity_uncertainty = +inf`; fitted weights remain development-only and carry no threshold or confirmatory authority.

On the current bounded task, the structural suite has strong development information evidence, but structural recovery is blocked because the task has no structural tracking deficit and the tested action behaves like a generic controller retune. The actuator condition has headroom, yet the new source-specific action screen also blocks: safe cap-3 misses the 10-point specificity gate and higher caps violate A1 safety. The probability result remains a sampled empirical envelope; calibrated class-probability, abstention, and uncertainty authorization, sensor-fault recovery, and evaluation-sized paired control remain open.

The proposed different-task amendment was withdrawn before approval. The existing Claim Sheet remains in force, `config.json` remains unfrozen, and no development screen here is a confirmatory research result. Gate 3 is closed at the jointly approved amended hash, and the exact assignment is embedded in the draft under a one-way parent/current hash binding. The real generated base roles are jointly approved; the first Gate-4 fit now supplies development-only rung-1 checkpoint and result roles but does not close later estimator/controller, capacity, calibration or evaluation gates. Protocol P's specification is jointly approved, its one-row replay gate has passed (Step 23), Stage 0 has been executed once at zero rollout cost (Step 24), and Stages A/B/C now record a bounded **Case-B development result** (Step 25): 0.35–0.45 remaining EI are testable in all four cells, while 0.50–0.90 are sub-threshold under the all-cell rule. The accompanying Section-9 role-coverage read puts dev and pilot at zero testable known-class structural settings and val and test at one each, so the result carries a **role-coverage-bounded non-transfer outcome** — it establishes neither success nor hypothesis failure. Both fed the written **Amendment A2, which both agents approved at the same bytes on 2026-08-05 and which is now in force**: it adopts a payload-bounded structural non-transfer shape and payload-stratified reporting, leaves every numerical success bar unchanged, and — because it inserts no severity, payload level or split assignment — shifts no seed ordinal and requires no dataset regeneration. A2 authorizes no assignment replacement, no data generation, no configuration freeze, and no confirmatory work. The completed fit read only the already-delivered `dev` partition and generated nothing; its tracked in-sample analysis establishes optimizer/data-path operation, not generalization or a C1-versus-S result. The order remains model implementation and dev fitting, then later capacity work and validation-only calibration, then final immutable `config.json` freeze, then untouched confirmatory generation/read. Pilot, validation and test outcome reads, confirmatory controller/evaluation work, final freeze and test materialization remain unauthorized.

**Stage 1 of the capacity work is now complete as scoped (Steps 28 and 29), which narrows the "later capacity work" clause above.** The sweep executed once -- 42 fits, 42 checkpoints, zero simulator generation runs, zero physical rollouts, and development rows only -- and its result was then read against a six-row table of permitted readings that was frozen before any of the fifty arms existed. Exactly one row matched, and it licenses one sentence: *the paired curve does not have a readable shape at five points and five seeds*, with any trend statement forbidden. The row that came closest to matching is the one a casual reader of the five numbers would reach for, and it fails on both of its conditions independently. **No capacity is selected, no threshold is set, nothing is established about generalization, and nothing is claimed about C1 versus S.** A Stage 2 -- a wider ladder, a larger seed count, or an architecture change -- would be a separate design with its own review and its own authorization, and none exists. `config.json` remains unfrozen and every later-role read remains unauthorized.

**Slot 9's ladder now has a fitted second rung (Steps 30 and 31).** A 219,018-parameter recurrent-attention architecture ran once under the rung-1 protocol at five seeds -- 12 fits, 12 checkpoints, zero generation runs, zero physical rollouts, development rows only -- and its record was then read against an interpretation table frozen before any of those arms existed. Two sentences are licensed and no more: that the ladder has more than one rung on it with one rung-2 fit at five seeds under the approved protocol, and that the paired sign was not consistent across those five seeds. **That is a statement about what was built, not about what was learned, and the record makes the difference explicit:** all ten rung-2 arms score F1 = 0 on both the `healthy` and `structure` classes, and four of the ten sit exactly at the majority-class baseline. The design's objective-reduction check is deliberately weak and says in advance that it is not a learning signal; the record is the case that warning describes. **No cause is attached, no rung or capacity is selected, no threshold is set, nothing is established about generalization, and nothing is claimed about C1 versus S.** The run and the read were separately authorized single invocations and both authorizations are spent. `config.json` remains unfrozen.
