# Human Report — Codex Session 33

**Current date and time:** 2026-07-24 18:59 PDT
**Phase:** Phase 2 — Integration and Reproducibility Build
**Session role:** Gate-2 base-role approval close, generator hardening, and exact-state review handoff
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Additional Gate-4 stop:** `BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK`
**Session decision:** Preserve the closed original generator/data approval while handing a bounded hardening state back for separate exact-state review

---

## Summary

### Complete startup and cross-review

I followed the complete `AgentPrompt.md` startup route before acting:

- all of `Project Details/Project Details.md`;
- the prior Codex continuity summary;
- every Codex chat summary;
- both active Codex chat transcripts;
- Claude's latest active-thread response; and
- `agents/Claude/Session Summaries/HumanReport33.md`.

I also read the project review-cycle and reproducibility-packet playbooks before
changing the shared packet. No transcript-order recurrence was present, so the
monitoring thread required no reply.

### Original Gate-2 generator/base-role review closed

Claude returned the required exact-state token:

```text
APPROVE_GATE2_GENERATOR_BASE_ROLES
```

with no review-target edits. Claude independently audited the generated state
rather than accepting the Session-32 audit summary. The reviewed implementation
and the retained local primary C1/S base roles are therefore jointly approved
at the exact Session-32 handoff state.

That approval closes only the original generator/data review. Gate 2 remains
open overall because Gate-4 model fits must still produce the
estimator-output/controller-log roles.

The continuing state is:

```text
approved Gate-3 assignment:
dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1

current embedded draft:
dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56

retained reservations / manifest rows: 472 / 944
test identities or payloads:           0
```

### Claude's measured design findings accepted at their actual boundary

Claude approved the artifact but measured two facts that govern what happens
next.

#### Structural separability requires a development-only stop/go check

Claude isolated the structural effect using matched seeds and found the
largest diagnostic-gauge separation at each reserved remaining-EI severity:

```text
remaining EI   peak separation   multiple of 0.405 µstrain floor   role
0.95           0.0090 µstrain    0.02x                             development
0.85           0.0864 µstrain    0.21x                             pilot
0.75           0.1614 µstrain    0.40x                             development
0.60           0.3267 µstrain    0.81x                             pilot
0.50           0.4873 µstrain    1.20x                             development
0.40           0.7266 µstrain    1.79x                             validation
required bar: 0.810 µstrain
```

Every reserved structural severity is below the existing synchronous
interpretable margin. That does not establish that the learned raw-tensor path
is unusable. It does establish that the Gate-4 capacity ladder must not proceed
blindly. I accepted Claude's stop:

```text
BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK
```

Claude owns a development-only structure-versus-healthy separability check for
both suites and both development severities, using an interpretable rung plus a
small learned probe. Validation and test remain untouched. Depending on the
result, the project either records a mild-end limitation and proceeds, or
reviews an amendment to excitation/severity before spending validation or
test.

#### Assigned contact is balanced; realized contact is fault-coupled

The 472-run data contain:

```text
contact profile assigned:       236 runs
actual plane contact:            11 runs
development / pilot / val:       0 / 11 / 0
contact-active steps:           243
scheduled-window duty cycle: 0.232%
```

All 11 actual-contact runs are pilot encoder-bias or encoder-drift cases:
7 bias and 4 drift. No healthy, structural, actuator, dropout, development, or
validation run touches the plane. Assigned contact remains independent of
fault, but realized contact is an effect of the faulty encoder/controller loop
and is loudest in the S-only gauge channel. This is a potential S-favouring
shortcut if the coupling reappears under the longer, heavier confirmatory test
profile.

The finding is currently non-blocking because it is confined to pilot, which
feeds neither fitting, calibration, nor the headline comparison. Gate 7 and
the Technical Report must preserve the assigned-versus-realized distinction,
and the test contact profile is now a deliberate pre-freeze decision rather
than an inherited constant.

## Work performed

### Approval binding now requires the exact assignment pin

`validate_approved_assignment_binding` previously allowed
`expected_assignment=None`. That mode still validated the embedded wrapper,
but it let a caller omit the explicit comparison to the tracked approved
assignment.

I removed the optional mode:

- `expected_assignment` is now a required argument;
- the embedded assignment is always exact-compared to the caller-provided
  tracked assignment;
- every shipped caller supplies that assignment; and
- a regression proves omission raises `TypeError` at the API boundary.

This is fail-loud hardening. It does not change the assignment, draft config,
or retained generated rows.

### Generator runtime values now come from the bound config

The generator had three duplicated `0.002` control-step literals plus duplicated
plant point-count and physics-timestep literals. The values matched the current
config, so the retained dataset was semantically correct, but those duplicates
could drift from future reviewed configuration values.

I added one frozen runtime-parameter authority derived from the validated bound
draft:

```text
control_dt_s
f_ctrl_hz
simulation_timestep_s
point_count_per_link
```

It fail-loud checks:

- finite positive timing values;
- reciprocal consistency between `f_ctrl_hz` and `control_dt_s`;
- an integer physics-step ratio;
- exact control-grid alignment for trajectory and fault onsets; and
- a physically valid point count.

Fault onset, rollout length, label onset, mechanics preflight, and the real
plant now consume that single authority. Regressions exercise a non-default
control step and prove the mechanics/timing values follow configuration rather
than the current constants.

### Packet storage and exclusion provenance documented

`Reproducibility Packet/README.md` now records:

- the suite-specific plant payloads are intentionally byte-identical duplicates
  so each suite retains a self-contained role set and its own manifest identity;
- the current duplicate storage cost is approximately 1.4 GB; and
- the first full generation attempt was stopped at 193/472 reservations because
  its preflight had checked only the six research-owned masses before the run,
  not the two test-owned scalar masses.

The exclusion record states that the partial attempt contained no test
identity/payload, its ignored partial output was removed, all eight masses were
then preflighted, and only the from-zero second run is downstream eligible.

The packet's current boundary now records both the closed original base-role
review and the structural-separability stop before Gate-4 fitting.

## Verification

All Python commands used the repository virtual environment:

```text
focused binding/Gate-3/generator tests: 37 passed
full packet suite:                      399 passed in 9.34 s
compileall:                             pass
generator CLI help:                     pass
read-only approved-assignment CLI:      pass
retained independent full audit:        pass
git diff --check:                       pass
```

The read-only assignment validator still reports:

```text
assignment:
dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1

current draft:
dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56

research generation permissions: false
test materialized:              0
```

The 3.86 GB retained dataset was not regenerated because the bound config still
resolves to the same 500 Hz / 0.002 s / 0.0001 s / 17-point state. The
independent audit reloaded the complete retained root and returned:

```text
reservations / manifest rows:       472 / 944
plant and label payloads:           944 / 944
byte-identical C1/S plant pairs:     472 / 472
bitwise shared-channel pairs:       472 / 472
test identity/payload rows:           0
```

One focused test initially failed because the new assertion expected a generic
1.0 s fault onset while the approved validation trajectory starts at 0.85 s.
The implementation was correct. I fixed the regression to derive the expected
onset from the actual approved trajectory, then reran both focused and full
suites to green.

The line-ending diagnostics contain only the repository's recurring LF/CRLF
warnings; no whitespace error is reported.

## Review-cycle and transcript handling

Both Session-33 appends used the append-only hard gate:

1. read the physical UTF-8 tail;
2. record the pre-write line count;
3. capture a complete multi-line EOF anchor;
4. prove the anchor occurs once;
5. patch only against that exact anchor;
6. prove the new header occurs once after the pre-write boundary;
7. re-read the physical tail; and
8. prove the transcript diff has zero deletions.

The first append accepted the original approval and the Gate-4 stop. The second
created a separate exact-state hardening handoff:

```text
APPROVE_GATE2_GENERATOR_HARDENING
```

or a file/line-specific block.

The final append proof was:

```text
pre-write lines: 3560
post-write lines: 3643
new header line: 3564
header count after boundary: 1
last author: Codex
transcript diff: +126 / -0
```

This new loop does not reopen the already-closed original generator/data
approval.

## Exact hardening review state

```text
assignment_binding.py
f189a2b35b364393e56293792c60f56ec203cd44455a6b786fd4ed05b7be217d

assignment_generator.py
e321966fd1e96f7cf3ee63db26205ac88898c03c1af513b37ea8150a18967a85

test_assignment_binding.py
1deb2921b889d5992d7b9e8e1625ac462a5794fc93fb109d957d7007cdfd99c3

test_assignment_generator.py
b61554de143229b4a52c5e10f93a633769ce2b74c295518ff0036fd7acaf8aa7

test_gate3_assignment.py
1a7c910e5910ce8b9038c4546ffc761176ff95d96bbce4a47df89d873d811efe

Reproducibility Packet/README.md
16105f153379ec8898de1fc23c407dea3ebb5ff7656054373fdf1b027ee62516
```

## Public live-run status

Claude's Session-33 public milestone already records the approved generator/data
state and the measured design findings. The bounded implementation hardening is
not a new scientific milestone, so I did not add another root-README entry or
duplicate Claude's update.

## Claim boundaries

This session:

- closes the original generator/base-role exact-state review;
- hardens future binding and configuration consistency;
- records two measured design risks; and
- opens a separate review of the hardening state.

It does not:

- complete Gate 2 before Gate-4-produced roles exist;
- establish structural separability;
- fit or select a model;
- infer a validation result;
- authorize controller action;
- create final `config.json`;
- materialize test;
- establish the headline C1-versus-S result; or
- close Phase 2.

## Files created

- `agents/Codex/Session Summaries/HumanReport33.md`

## Files updated

- `Reproducibility Packet/scripts/utils/assignment_binding.py` — required exact
  assignment pin.
- `Reproducibility Packet/scripts/utils/assignment_generator.py` — bound
  config-derived runtime timing and mechanics parameters.
- `Reproducibility Packet/tests/test_assignment_binding.py` — pinned callers and
  omitted-pin failure regression.
- `Reproducibility Packet/tests/test_assignment_generator.py` — configuration
  authority and non-default-timing regressions.
- `Reproducibility Packet/tests/test_gate3_assignment.py` — exact assignment pin
  at the approval-validation call site.
- `Reproducibility Packet/README.md` — duplicate-storage rationale, exclusion
  provenance, and current gate boundary.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only approval receipt and hardening handoff.
- `agents/Codex/README.md` — workspace index through Session 33.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  resume state.

## Files deliberately unchanged

- the approved assignment JSON;
- `Reproducibility Packet/config/draft-config-v0.1.json`;
- the ignored retained dataset;
- root `README.md`;
- `Reproducibility Packet/config.json`, which remains absent;
- Claim Sheet artifacts;
- source ledgers; and
- transcript-order monitoring thread.

## `.gitignore` review

The root `/data/` rule still correctly ignores the retained dataset and other
rebuildable data. Packet-local numeric-array/model/cache rules remain adequate.
No new generated or secret file appeared in `git status`, so no `.gitignore`
change was needed.

## Next steps

1. Claude reviews the exact hardening state and returns
   `APPROVE_GATE2_GENERATOR_HARDENING` or a file/line-specific block.
2. Independently of that implementation loop, Claude runs the development-only
   structural separability stop/go check.
3. If structure separates, proceed to the Gate-4 ladder with the mild-end
   limitation recorded. If it does not, review an excitation/severity amendment
   before validation or test are spent.
4. Decide the confirmatory test contact profile deliberately in light of the
   realized-contact coupling.
5. Complete Gate-4 estimator-output/controller-log roles, then Gate-5
   calibration, Gate-6 controller protocol, and Gate-7 driver.
6. Create immutable `config.json` only after Gates 2–7 close and immediately
   before untouched test materialization.

## End state

```text
Gate 1: complete and jointly approved
Gate-2 generic write/load/join foundation: complete and jointly approved
Gate-2 original primary C1/S generator/base roles: exact-state review closed
Gate-2 generator hardening: exact-state review open
Gate 2 overall: open pending Gate-4 estimator/controller roles
Gate 3: complete and jointly approved
Gate 4: BLOCKED pending the development structural-separability check
Gates 5–7: open
Final config: UNFROZEN
Research result: none
Test identity/payload materialized: 0
```
