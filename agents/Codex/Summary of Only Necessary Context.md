# Summary of Only Necessary Context — Codex

**Last completed Codex session:** 35
**Date:** 2026-07-25
**Current phase:** Phase 2 — Integration and Reproducibility Build
**Primary active thread:** `chats/Claude-Codex/Phase 2 Integration and Config
Freeze/Phase 2 Integration and Config Freeze - Active.md`

## Resume here

Gate 4 is stopped on a third, text-only Amendment-A2 proposal state:

```text
BLOCK_AMENDMENT_A2_PROPOSAL_V2_PENDING_EXECUTABLE_PROTOCOL_AND_STRATUM_MAP
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Claude Session 35 corrected the two formulations Codex blocked in Session 34:

1. the mild-stratum evidence statement is now limited to the assigned
   development contexts at remaining EI 0.75 and 0.50; and
2. conditional Case B now defines the four-way row population, shared
   non-structural rows, weights, dependence, one model per suite, one
   confirmatory decision, and non-confirmatory secondary result.

Those components are accepted for reuse.

Codex Session 35 still blocked the exact proposal because the unrun Protocol P
does not yet define an executable trajectory universe or a prospective mapping
from its two development severities to the different pilot/validation/test
severity grids. Its four-gauge scalar and its proposed test-contact offsets
also require exact pinning.

Claude's next action is a corrected **proposal text only**. Do not run Protocol
P, edit the Claim Sheet, build a replacement assignment, generate amended data,
fit Gate-4 models, or create final config before that text converges.

## Gate state

```text
Gate 1:
  complete and jointly approved

Gate-2 generic role write/load/join path:
  complete and jointly approved

Gate-2 real primary C1/S generator/base roles:
  complete and exact-state review closed

Gate-2 bounded generator hardening:
  complete and exact-state review closed

Gate 2 overall:
  open only for later Gate-4 estimator-output/controller-log roles

Gate 3:
  complete and jointly approved at the current pre-A2 assignment
  any A2 replacement requires a new exact assignment/review loop

Gate 4:
  BLOCKED on executable Protocol P and corrected AMENDMENT A2

Gates 5–7:
  open

Reproducibility Packet/config.json:
  absent; final configuration is UNFROZEN

Confirmatory test identities/payloads:
  0 / 0

Research result:
  none
```

## Current approved machine/data state

The exact pre-A2 authorities remain:

```text
approved Gate-3 assignment:
dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1

current embedded draft config:
dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56

retained reservations / manifest rows:
472 / 944

retained plant and label payloads:
944 / 944

byte-identical C1/S plant pairs:
472 / 472

bitwise shared-channel pairs:
472 / 472

test identities or payloads:
0
```

The ignored local dataset root is:

`data/gate3-base-dev-pilot-val-c1-s`

It is approximately 3.86 GB. It is a pre-amendment non-test dataset, not a
final amended dataset. Do not delete or relabel it while A2 is unresolved.

If a written A2 amendment and replacement assignment later receive joint
same-state approval, the selected provenance policy is **full regeneration
from zero**. The current set then becomes a named superseded pre-amendment set
in the exclusion trail. No current payload is silently reused under a changed
config hash.

## What Claude Session 35 changed

### Ramp audit

Claude found that the approved assignment pins probe strength, frequency,
cycles and raised-cosine envelope but not ramp width.

The mismatch is confirmed in code:

```text
screen_synchronous_safe_probe.py:
  default ramp_period_fraction = 0.125

assignment_generator.py:
  finite delivered ramp = duration / 2
  equivalent ramp fraction = 0.5
```

Claude reports that the delivered 0.5-fraction ramp produces a much weaker
structural signal at the same 0.05 N than the screened 0.125-fraction ramp, but
permits more amplitude before closed-loop instability. Claude therefore
withdrew the Session-34 “2x–40x too mild” characterization and proposed
development-only Protocol P to jointly select ramp, amplitude and which
structural severities clear the margin.

Codex independently verified the field/code mismatch, but did not replay the 32
mechanics rollouts behind Claude's numerical Findings B–C. Retain those findings
only at their stated development-mechanics scope until further independent
verification is needed.

The Session-34 structural-separability result itself remains valid for the data
that were actually delivered. Both suites saw the same excitation, the current
development structural settings do not support the planned S-versus-C1
hypothesis test, and the actuator positive control separates. This is a method
feasibility stop, not a hypothesis result.

### Sign-test report correction

Claude corrected `screen_structural_separability.py` so the exact two-sided
sign-test floor is derived from `n_cells`.

```text
pooled screen:
  n_cells = 8
  exact floor = 0.0078

diagnostic-only screen:
  n_cells = 4
  exact floor = 0.125
```

The diagnostic report now explicitly says no channel can reach `p <= 0.05` and
that its empty attribution table is forced by cell count, not evidence of no
channel effect. Codex reviewed and accepts this forward correction.

## Corrected components now accepted

### Mild-stratum evidence statement

The accepted wording is:

> In the assigned development contexts at remaining EI 0.75 and 0.50, the
> current excitation does not provide a gauge-borne structural signature that
> supports the planned S-versus-C1 hypothesis test; the detectable structural
> effect is instead in C1 IMU channels.

The existing settings may be retained as a stratum in a future amendment, but
the development screen is not the final result of that complete stratum.

### Conditional Case-B estimand structure

The accepted structure is:

- primary four-way macro-F1 over all healthy, actuator and sensor rows plus
  testable-stratum structural rows;
- every non-structural row has weight 1 and is shared across strata;
- one model per suite is trained on the complete manifest;
- S and C1 use identical reservations;
- the hierarchical bootstrap draws each shared reservation once so dependence
  is preserved;
- there is one confirmatory decision; and
- the same metric on the sub-threshold stratum is secondary,
  predeclared and non-confirmatory, not a second success route.

This structure is accepted only after the structural membership mapping below
is fully defined.

## Why Protocol P is still blocked

### 1. Trajectory/screening universe is contradictory

The approved development trajectories are:

```text
trajectory_dev_ordinary_a:
  excitation = ordinary
  diagnostic_probe = null

trajectory_dev_diagnostic_b:
  excitation = diagnostic
  diagnostic_probe = 0.05 N
```

`gate3_assignment.py` requires ordinary trajectories to carry no probe.
Protocol P varies probe ramp and amplitude and requires the 0.8 Hz margin on
**both** development trajectories.

The next proposal must choose one exact contract:

1. run P only on the assigned diagnostic trajectory; or
2. define development-only probe-overlay clones of the task paths, label them
   mechanics-screen conditions rather than dataset trajectories, and state
   whether the canonical ordinary trajectory remains probe-free in the
   regenerated manifest.

Do not let implementation silently reinterpret “both trajectories.”

### 2. Development P outcomes do not classify the other split settings

The approved remaining-EI grids differ:

```text
dev:    0.50, 0.75
pilot:  0.60, 0.85
val:    0.40, 0.90
test:   0.35, 0.65
```

P measures only development 0.50 and 0.75. Cases A/B nevertheless refer to all
reserved severities and to testable versus sub-threshold structural rows.

Before P runs, the next proposal must assign every role's listed setting for
every possible P outcome. Acceptable forms:

- an explicit role-by-role, branch-by-branch membership table; or
- a numeric cutoff rule with direction, equality handling, monotonicity
  assumption and a predeclared response to a contradictory pilot margin.

The pilot may stop or bound transfer. It may not retrospectively relabel
validation/test rows after seeing later-role results. If the current grids
cannot support the rule, propose complete replacement grids without generating
or reading non-development payloads.

Until this exists, Case A “no stratification” and Case B's confirmatory
population are not fully defined.

### 3. Four-gauge scalar is ambiguous

Protocol P says “synchronous gauge coefficient L2 distance” but does not specify
four-gauge aggregation.

The existing safe-probe statistic:

1. fits intercept, trend, cosine and sine per gauge;
2. takes the L2 norm of the cosine/sine coefficient difference per gauge; and
3. takes the maximum across gauges.

Pin the exact scalar compared with `>= 0.810 microstrain`. If the existing
statistic is intended, state the worst-context maximum per-gauge coefficient
norm explicitly. A joint vector norm across all gauges is different.

Also define “gentlest ramp” mechanically. In the proposed set, the largest
fraction, 0.5, appears gentlest.

### 4. Contact offsets are incomplete

Current assigned contact windows:

```text
dev:    [2.0, 2.5]   duration 0.5 s
pilot:  [2.6, 3.2]   duration 0.6 s
val:    [1.8, 3.3]   duration 1.5 s
test:   [1.6, 3.8]   duration 2.2 s
```

The proposal says test inherits validation's **length**, but does not pin the
test start phase and incorrectly says duration then becomes constant “across
rungs.”

The next proposal must give the exact test `contact_window_offset_s`. If only
validation/test duration is matched, say so. If timing also matches, copy the
full validation offset pair.

## Protocol-P elements not otherwise objected to

The current text proposes:

```text
ramp fractions:
  0.125, 0.25, 0.5

amplitudes:
  0.05, 0.10, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30 N

hard per-development-cell checks:
  zero A1 safety flags
  max |qd_true| <= 8 rad/s
  max |q_true| <= 2.5 rad
  max |gauge_true| <= 400 microstrain
  peak joint-0 probe torque <= 60% of torque_abs_limit[0]
  no saturated-step increase versus zero-probe control

margin:
  W = 768 from onset
  f = 0.8 Hz
  matched sensor seed
  healthy versus fault
  every authorized development context must reach >= 0.810 microstrain

selection:
  maximize number of passing reserved development severities
  then smallest amplitude
  then gentlest ramp

no pass:
  Case C method failure / excitation-bounded transfer shape
```

These items remain proposal text, not an approved or executed protocol.

## Current separability evidence boundary

Codex Session 34 independently regenerated both tracked development analyses
from the retained dataset and matched every substantive top-level JSON field.
Decision-relevant pooled learned AUROCs:

```text
contrast / suite                 C1      S
structure remaining EI 0.75      0.250   0.172
structure remaining EI 0.50      0.750   0.703
actuator remaining gain 0.50     0.891   0.859
```

Pooled structural effects clearing the paired channel sign test are IMU rather
than gauge channels. Interpret this as:

```text
current delivered structural settings/excitation fail the prerequisite
development feasibility gate
```

Do not interpret it as:

```text
the project hypothesis is false
the whole mild band has a negative result
pilot or validation confirms the development result
the withdrawn 2x–40x severity claim remains valid
```

## Contact-design fact that remains live

The pre-A2 472-run set assigned contact to 236 runs but realized actual plane
contact in only 11 pilot encoder-bias/drift runs:

```text
development / pilot / validation actual-contact runs:
0 / 11 / 0
```

Assigned contact is balanced, but realized contact is fault-coupled and loudest
in an S-exclusive gauge channel. This is not a headline result. It makes the
confirmatory contact schedule a deliberate pre-freeze decision and later
Gate-7/Technical-Report audit item.

## Forward correction that must not be lost

`agents/Codex/Session Summaries/HumanReport33.md` contains an incorrect first
row in its measured severity table. The concluded report stays unchanged, but
the Technical Report/limitations record must use:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

not `0.95 | 0.0090 | 0.02x | development`.

The former diagnostic sign-test labeling problem is now fixed in Claude Session
35 and does not need another handback.

## Verification baseline

Use the repository venv, never bare system Python:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Codex Session-35 result:

```text
399 passed in 9.61 s
```

Do not use root-wide `pytest -q` as the clean packet command. Ignored
`tmp/session6_packet_copy/tests` duplicates three test module names and causes
collection mismatch errors. That is workspace discovery, not a packet test
failure.

Session 35 read the approved assignment's non-development design fields to
audit prospective mapping, but opened no pilot, validation or test payload or
outcome.

## Transcript-order state

Codex Session 35 appended cleanly to the technical thread:

```text
pre-write lines:        4380
post-write lines:       4541
Session-35 header:      line 4382
header count:           1
old prefix:             line-identical to HEAD
technical diff:         +161 / -0
physical last author:   Codex
```

The complete verified Claude EOF block was used in the actual patch. No
recurrence occurred, so the monitoring thread was not updated.

For every future transcript append:

1. read the UTF-8 physical tail;
2. record the pre-write line count;
3. use the complete unique EOF block in the actual patch;
4. prove the new header occurs exactly once after that boundary;
5. compare the old prefix and re-read the physical tail; and
6. require `+N / -0` before closeout.

## Public record

Root `README.md` already has Claude's append-only Session-35 correction:

- the ramp width was not pinned;
- the delivered probe differed from the screened probe;
- the “2x–40x too mild” characterization is withdrawn;
- probe and severity selection are proposed jointly; and
- config/test remain untouched.

Codex Session 35 added no public entry because the exact proposal block is an
internal review state, not a new scientific result or completed milestone. Keep
the public log lean unless the design actually converges or a new result lands.

## Review-cycle state and next actions

The active technical thread is physically last with Codex's explicit block.

Next:

1. Read any new Claude turn and Claude's latest HumanReport before acting.
2. Review the replacement text for exactly:
   - Protocol-P trajectory/screen universe;
   - branch-complete mapping of P outcomes to every role's structural settings;
   - exact four-gauge statistic and ramp tie-break; and
   - exact test contact offsets with accurate scope.
3. Approve or block that exact proposal state explicitly.
4. Only after proposal approval, Claude may implement and run Protocol P on the
   authorized development-only screening universe with zero non-development
   payload/outcome reads.
5. Review the exact Protocol-P implementation, result and selected branch.
6. Then review the branch-specific synchronized written Claim Sheet, Accessible
   Claim Sheet, manifest/exclusion and packet amendment.
7. Review the replacement hash-bound assignment at exact state.
8. Only after the written amendment and assignment receive same-state approval
   may the selected branch be implemented; if it advances, regenerate the
   non-test study from zero and repeat the independent identity/role/CRN audit.
9. Resume Gate 4 only after the amended development feasibility gate clears.
10. Keep final `config.json` absent and confirmatory identities/payloads at zero
   until Gates 2–7 close.

No regular Codex progress report is due until Session 40 unless a playbook
trigger requires one earlier.

## Key files

- `agents/Codex/Session Summaries/HumanReport35.md`
- `agents/Claude/Session Summaries/HumanReport35.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration
  and Config Freeze - Active.md`
- `Claim Sheet.md`
- `Accessible Claim Sheet.md`
- `Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json`
- `Reproducibility Packet/config/draft-config-v0.1.json`
- `Reproducibility Packet/scripts/utils/gate3_assignment.py`
- `Reproducibility Packet/scripts/utils/assignment_generator.py`
- `Reproducibility Packet/scripts/screen_synchronous_safe_probe.py`
- `Reproducibility Packet/scripts/screen_structural_separability.py`
- `Reproducibility Packet/results/structural_separability/`
- `README.md`

## Non-negotiable boundaries

- Development mechanics/screens are not confirmatory results.
- The current separability failure is a feasibility result, not a hypothesis
  failure.
- Do not restore the withdrawn “2x–40x too mild” characterization.
- Do not run Protocol P before its exact proposal is approved.
- Do not let pilot outcomes retroactively define confirmatory stratum
  membership.
- Do not call a metric per stratum until every class, row and weight is
  defined.
- Do not inspect non-development outcomes to choose the amended design.
- Do not materialize confirmatory identities or payloads before final freeze.
- Reviewer edits, handoffs or silence are not approval; require explicit
  same-state approval.
- Keep detection, attribution, information/action authorization, and control
  outcome separate.
- Keep `config.json` absent until all remaining gates close.
