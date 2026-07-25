# Human Report — Codex Session 34

**Current date and time:** 2026-07-25 12:51 PDT
**Phase:** Phase 2 — Integration and Reproducibility Build
**Session role:** Independent structural-separability reproduction and Amendment
A2 proposal review
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)
**Governing decision:**
`BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Session decision:** `BLOCK_AMENDMENT_A2_PROPOSAL` on two narrow
evidentiary/estimand defects; the amendment direction remains supported

---

## Summary

### Complete startup and cross-review

I followed the complete `AgentPrompt.md` startup route before acting:

- all of `Project Details/Project Details.md`;
- the prior Codex continuity summary and workspace index;
- every summary in every Codex-inclusive chat;
- both active Codex-inclusive transcripts;
- Claude's complete Session-34 turn at the physical tail;
- `agents/Claude/Session Summaries/HumanReport34.md`;
- Claude's rewritten continuity summary;
- the review-cycle and Claim-Sheet playbooks;
- the current Claim Sheet and its accessible companion; and
- the complete structural-separability script and both tracked result pairs.

Claude's exact Session-34 approval closes the separate Session-33 generator
hardening review:

```text
APPROVE_GATE2_GENERATOR_HARDENING
```

Gate 2 remains open overall only because the Gate-4 model/controller build must
still create the estimator-output and controller-log roles.

### The separability result independently reproduces

Claude's development-only check asked whether the current structural fault
settings contain enough signal to support the planned hypothesis test before
the team spends validation or confirmatory test.

I regenerated both shipped variants with the repository venv:

- the eight-context, pooled-trajectory screen; and
- the four-context, diagnostic-trajectory-only screen.

For each regenerated JSON I compared every top-level field to the tracked
result, excluding only the run timestamp and absolute dataset-root string.
Every substantive object was exactly equal:

```text
config_hash        exact
contrast_order     exact
contrasts          exact
n_cells            exact
screen             exact
split              exact
stride             exact
suites             exact
trajectory_filter  exact
window_steps       exact
windows_per_run    exact
```

The reproduction confirms:

- at development remaining EI 0.75, C1 reaches 0.453 interpretable / 0.250
  learned AUROC and S reaches 0.469 / 0.172;
- at development remaining EI 0.50, C1 reaches 0.469 / 0.750 and S reaches
  0.578 / 0.703;
- the actuator positive control reaches 0.891 learned AUROC for C1 and 0.859
  for S;
- the pooled structural channels clearing the paired sign test are IMU
  channels, not gauges; and
- no validation or confirmatory-test payload is used.

The Gate-4 stop is therefore real. The current settings fail the predeclared
feasibility condition needed to interpret a later null result. They do not
establish that the project hypothesis is false.

### Amendment A2 direction supported, exact proposal blocked

Claude proposed:

1. retaining the current mild structural region;
2. adding a severe structural region;
3. re-deriving the diagnostic probe inside the A1 envelope;
4. choosing the confirmatory contact profile deliberately; and
5. regenerating the amended study coherently.

Those directions are warranted. I nevertheless returned:

```text
BLOCK_AMENDMENT_A2_PROPOSAL
```

because two load-bearing formulations were not yet defensible.

#### Objection 1: the development diagnostic was promoted into a 472-run result

The proposal said the delivered 472 runs would carry the finding that
structural sensing adds nothing at remaining EI `>= 0.50`. The screen examined
only eight development contexts at development severities 0.75 and 0.50. It
did not analyze pilot or validation, and no confirmatory payload exists.

The current defensible statement is narrower: under the assigned development
contexts and current excitation, those two severities do not provide a
gauge-borne signature capable of supporting the planned S-versus-C1 test; the
detectable structural effect is in conventional-suite IMU channels.

The corrected amendment should preserve the existing severity **settings** as a
mild stratum. It should not treat the development diagnostic as the result of
that complete stratum. Under the amended study, the mild stratum receives its
own later split-authorized analysis.

#### Objection 2: four-way macro-F1 per structural band is undefined

Only the structural class naturally divides into mild and severe severities.
Healthy, actuator, and sensor rows have no proposed band membership. A four-way
macro-F1 cannot be declared per band until the written design specifies:

- the non-structural rows accompanying each structural stratum;
- whether any rows are shared;
- the dependence-aware pairing, weighting, confidence interval, and
  multiplicity treatment;
- exact per-split manifest membership; and
- the project-level primary versus severity-stratified secondary estimands.

A severe region can carry the headline only if its complete four-class
comparison is prospectively defined. Otherwise it can carry the headline
structural sub-comparison while project-level macro-F1 uses one completely
specified manifest.

### Full regeneration chosen

Adding structural severities under the current expansion order shifts later
actuator and sensor ordinals and therefore their seeds. I chose Claude's
recommended coherent option:

```text
full regeneration from zero after exact amendment and assignment approval
```

The current 472 payloads should become a superseded pre-amendment set in the
packet exclusion trail. The reproduced development screen remains the disclosed
reason for A2. No current payload should be silently reused under a changed
config hash.

### Requirements handed back for the corrected proposal

The replacement text must:

- select severe settings and probe amplitude from development-authorized
  mechanics before observing replacement pilot, validation, or test outcomes;
- state an exact candidate grid, a context-robust 2.0x margin rule, the A1
  ceiling, and the failure action before selection;
- avoid choosing from one favorable payload/contact/seed cell, because fixed
  severity varies materially by context;
- define the confirmatory contact profile prospectively without generating or
  reading confirmatory identities or payloads;
- synchronize Claim-Sheet Slots 11–13, the split/manifest contract, exclusion
  trail, packet instructions, and Accessible Claim Sheet; and
- keep generation and final config blocked until the written amendment and its
  replacement assignment have explicit same-state approval.

This does not reopen the task, score, controller, or project hypothesis.

## Forward corrections

### Session-33 severity table

Claude correctly flagged an error in
`agents/Codex/Session Summaries/HumanReport33.md`. The limitations record must
use:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

not the report's erroneous 0.95 development row. The concluded report remains
unchanged, but the incorrect row is explicitly blocked from propagating into
the Technical Report.

### Diagnostic report's sign-test sentence

`Reproducibility Packet/scripts/screen_structural_separability.py` line 742
hard-codes:

```text
exact 8-cell floor (p = 0.0078)
```

into both rendered reports. That is correct for the pooled eight-cell analysis,
but not the diagnostic analysis with four cells. A two-sided four-cell sign
test cannot reach 0.05. I handed this back as a forward report-label correction.
It does not alter the exact reproduced JSON, the pooled test, or the pooled
no-gauge conclusion.

## Verification

All research Python commands used the repository virtual environment.

```text
pooled screen regeneration:      complete
diagnostic screen regeneration:  complete
substantive pooled JSON:          exact match
substantive diagnostic JSON:      exact match
packet tests:                     399 passed in 10.53 s
test identities/payloads read:    0
```

Both runs emitted NumPy warnings while aggregating columns absent from one
suite. The warnings are also consistent with the script's NaN-padded
cross-suite column table; they did not prevent output and the complete
substantive results reproduced exactly.

A root-wide `pytest -q` invocation initially stopped during collection because
the ignored `tmp/session6_packet_copy/tests` directory contains duplicate test
module names. That is a workspace-discovery issue, not a packet test failure.
The authoritative scoped invocation:

```text
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

passes all 399 packet tests.

## Transcript handling challenge and repair

My first attempt to append the Session-34 technical review used a generic
Claude sign-off/separator anchor. It matched an earlier turn and placed the new
block at line 2,320 rather than after the recorded 3,969-line physical tail.

The immediate post-write assertion caught the violation. Before closeout or
commit I:

1. removed only my newly inserted misplaced copy;
2. restored the exact 3,969-line pre-write state;
3. reapplied the identical turn using Claude's complete final
   status/order/sign-off block as context; and
4. re-ran the uniqueness, boundary, tail, and git-diff checks.

Final technical-transcript proof:

```text
pre-write lines:         3969
post-write lines:        4106
Session-34 header:       line 3971
header count:            1
header after boundary:   yes
physical last author:    Codex
final transcript diff:   +137 / -0
```

Because Randy's standing monitoring request covers caught recurrences too, I
appended a transparent incident note to the monitoring thread. Its independent
append proof is:

```text
pre-write lines:         57
post-write lines:        88
Session-34 header:       line 61
header count:            1
header after boundary:   yes
monitoring diff:         +31 / -0
```

The recurrence ends the clean-append streak but does not change the technical
decision.

## Public live-run status

The prior public entry said the proposal would preserve the mild levels “and
their negative result.” Because only the development cells were analyzed, I
preserved that old entry and added an explicit append-only correction. The new
entry records the exact evidence boundary, the undefined per-band four-class
estimand, the need for coherent regeneration, and the continuing untouched-test
state.

## Claim boundaries

This session:

- closes the generator-hardening exact-state review;
- independently reproduces the development structural-separability failure;
- supports the need for a design amendment;
- blocks two overreaching/undefined proposal formulations;
- chooses coherent full regeneration after approval;
- records two forward corrections; and
- keeps Gate 4 stopped before model fitting.

It does not:

- establish a result for the full mild structural band;
- inspect pilot, validation, or confirmatory outcomes for the A2 decision;
- define or approve the severe grid;
- define or approve a per-band four-class estimand;
- regenerate or invalidate data yet;
- fit or select the headline model;
- authorize controller action;
- create final `config.json`;
- materialize confirmatory test; or
- answer the research question.

## Files created

- `agents/Codex/Session Summaries/HumanReport34.md`

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only independent reproduction and A2 proposal review.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — transparent same-session recurrence record and verified repair.
- `README.md` — append-only public correction to the A2 evidence boundary.
- `agents/Codex/README.md` — workspace index through Session 34.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  resume state.

## Files deliberately unchanged

- `Claim Sheet.md` and `Accessible Claim Sheet.md`, because A2 is not approved;
- all Reproducibility Packet scripts and tracked result artifacts;
- the approved Gate-3 assignment and embedded draft config;
- the ignored retained dataset;
- `Reproducibility Packet/config.json`, which remains absent; and
- source ledgers.

## `.gitignore` review

The root `/data/` and `/tmp/` rules correctly keep the retained 3.86 GB dataset,
independent regenerated outputs, logs, caches, and the Session-6 packet copy out
of the commit. Existing venv/cache/log rules also remain effective. No secret,
credential, generated binary, or other newly unignored artifact appeared in
`git status`, so `.gitignore` requires no change.

## Next steps

1. Claude replaces the two blocked A2 formulations and returns a corrected
   short proposal.
2. Codex reviews that exact proposal; only explicit approval authorizes a
   written Claim-Sheet/Accessible-Claim-Sheet amendment.
3. The written amendment defines the severe grid, complete per-band estimand,
   context-robust probe rule, contact profile, full-regeneration/exclusion
   treatment, and replacement assignment.
4. Both agents review and approve the exact amendment and assignment before any
   amended payload generation.
5. After coherent regeneration, re-audit the non-test data and resume Gate 4
   only if the amended feasibility gate passes.
6. Keep pilot/validation use role-bound and confirmatory identities/payloads at
   zero until Gates 2–7 and final config freeze are complete.

## End state

```text
Gate 1: complete and jointly approved
Gate-2 generic write/load/join foundation: complete and jointly approved
Gate-2 original generator/base roles: exact-state review closed
Gate-2 generator hardening: exact-state review closed
Gate 2 overall: open pending Gate-4 estimator/controller roles
Gate 3: complete and jointly approved at the pre-A2 assignment
Gate 4: BLOCKED on corrected AMENDMENT_A2
Gates 5–7: open
Final config: UNFROZEN
Research result: none
Confirmatory identity/payload materialized: 0
```
