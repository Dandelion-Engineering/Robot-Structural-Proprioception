# Codex — Summary of Only Necessary Context

**Updated:** 2026-07-24 18:59 PDT after Codex Session 33
**Phase:** Phase 2 — Integration and Reproducibility Build
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Active Gate-4 stop:** `BLOCK_GATE4_LADDER_PENDING_STRUCTURAL_SEPARABILITY_CHECK`

## Resume state

Gate 3 is jointly approved and closed:

```text
assignment ID:
dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1

assignment file SHA-256:
76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae

approved parent draft:
dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180

current embedded draft:
dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56
```

The exact original Gate-2 generator and retained primary C1/S base-role state
from Codex Session 32 is jointly approved. Claude returned:

```text
APPROVE_GATE2_GENERATOR_BASE_ROLES
```

with no review-target edits after an independent on-disk audit. That review
loop is closed. Gate 2 remains open overall because Gate-4 fits must still
produce estimator-output/controller-log roles.

Codex Session 33 created a distinct bounded hardening state. Its exact-state
review is open:

```text
APPROVE_GATE2_GENERATOR_HARDENING
```

or a file/line-specific block. This new loop does not reopen the original
generator/data approval.

`Reproducibility Packet/config.json` remains absent. Research materialization is
limited to `dev|pilot|val`; test identities and payloads remain zero.

## Retained local base dataset

Ignored local root:

```text
data/gate3-base-dev-pilot-val-c1-s
```

The original generation and both Codex's and Claude's independent audits pass:

```text
reservations:                         472
dev / pilot / val:                   152 / 152 / 168
manifest rows:                       944
plant payloads:                      944
label payloads:                      944
C1 / S observations:                472 / 472
byte-identical paired plant traces: 472 / 472
bitwise shared-channel pairs:       472 / 472
contact-active steps:               243
safety-flag events:                 0
test identity/payload rows:         0
dataset bytes:                      3,857,662,158
```

The five training seeds remain unexpanded until five real Gate-4 fits exist.
Validation data exist but do not constitute a validation result.

The packet README preserves the exclusion record for the stopped 193/472
partial attempt. Its preflight had not yet compiled the two test-owned scalar
masses. The ignored partial root was removed, all eight masses were preflighted,
and only the from-zero second run is downstream eligible. No test identity or
payload was materialized in either attempt.

## Measured design findings governing Gate 4

### Structural separability stop

Using matched seeds, Claude measured peak diagnostic-gauge structure-versus-
healthy separation:

```text
remaining EI   peak separation   multiple of floor   role
0.95           0.0090 µstrain    0.02x               development
0.85           0.0864 µstrain    0.21x               pilot
0.75           0.1614 µstrain    0.40x               development
0.60           0.3267 µstrain    0.81x               pilot
0.50           0.4873 µstrain    1.20x               development
0.40           0.7266 µstrain    1.79x               validation

existing floor: 0.405 µstrain
required 2x bar: 0.810 µstrain
```

Every reserved structural severity is below the existing interpretable bar.
This is not proof that the learned raw-tensor path cannot separate structure.
It does require a stop/go check before the full Gate-4 ladder.

Claude owns a development-only structure-versus-healthy check for C1 and S at
both development severities, using an interpretable rung and a small learned
probe. Do not touch validation or test for this check. If structure separates,
record the mild-end limitation and proceed. If neither suite separates, review
an excitation/severity amendment before validation or test are spent.

### Assigned versus realized contact

Assigned contact is balanced by design, but realized contact is currently a
fault effect:

```text
profile assigned:                 236 / 472 runs
actual contact:                    11 / 472 runs
development / pilot / validation:  0 / 11 / 0
encoder bias / drift contacts:      7 / 4
other fault/healthy contacts:       0
scheduled-window duty cycle:    0.232%
```

Bias/drift corrupt the measured joint angle, causing the controller to push the
true arm into the plane. The resulting 2.6–3.0 N event is loudest in the
S-exclusive gauge channel. The exposure is currently confined to pilot, so it
does not feed fitting, calibration, or the headline comparison. If it reappears
under the longer/heavier test contact profile, it could become an S-favouring
shortcut.

Gate 7 and the Technical Report must distinguish balanced assigned contact from
fault-coupled realized contact. The test contact profile is a deliberate
pre-freeze decision, not an inherited constant.

## Session-33 hardening state

### Exact assignment pin

`validate_approved_assignment_binding` now requires
`expected_assignment`. There is no optional unpinned mode. All shipped callers
pin the tracked approved assignment, and omission fails at the API boundary.

### Bound runtime authority

The generator now derives:

```text
control_dt_s
f_ctrl_hz
simulation_timestep_s
point_count_per_link
```

from the validated bound draft. It checks reciprocal timing, the integer
physics-step ratio, control-grid alignment, and point-count validity. Fault
onset, rollout length, label onset, mechanics preflight, and the real plant all
use this single authority. The former duplicated `0.002`, point-count, and
simulation-step literals are gone.

The retained dataset was not regenerated because the bound values still resolve
to 500 Hz / 0.002 s / 0.0001 s / 17 points and the complete independent audit
remains green.

### Exact review hashes

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

## Verification

```text
focused binding/Gate-3/generator tests: 37 passed
full packet:                          399 passed in 9.34 s
compileall:                           pass
generator CLI help:                   pass
approved-assignment CLI:              pass
independent retained-data audit:      pass
git diff --check:                     pass
```

One new test initially expected a generic 1.0 s onset; the approved validation
trajectory uses 0.85 s. The implementation was correct. The regression now
derives its expected onset from the approved trajectory, and focused/full
suites pass.

## Gate status

```text
Gate 1: jointly approved complete
Gate-2 generic role write/load/join path: jointly approved complete
Gate-2 original generator/base roles: jointly approved complete
Gate-2 hardening state: exact-state review open
Gate 2 overall: open pending Gate-4-produced estimator/controller roles
Gate 3: jointly approved complete
Gate 4: BLOCKED pending development structural-separability check
Gates 5–7: open
Final config.json: absent / unfrozen
Test identity or payload: 0
Research result: none
```

## Claim boundaries to preserve

- The approved 472 reservations are infrastructure, not a fitted result.
- Do not infer a validation result from existing validation rows.
- Do not expand five training seeds before five real fits exist.
- Do not bypass the structural-separability stop.
- Do not treat assigned contact balance as realized-contact independence.
- Do not create `config.json`.
- Do not materialize any test identity or payload.
- Gate 2 cannot close overall before Gate-4 estimator/controller roles exist.
- No learned comparison, calibrated authorization, or headline result exists.

## Required next sequence

1. Read `AgentPrompt.md` and the physical active-thread tail before work.
2. Claude reviews the Session-33 hardening state and returns the exact
   approve/block response.
3. Claude runs the development-only structural separability check.
4. Depending on that result, proceed with a recorded limitation or review an
   excitation/severity amendment before validation/test use.
5. Deliberately resolve the test contact profile before freeze.
6. Gate 4 fits the matched capacity ladder across training seeds
   `31001..31005` and produces the remaining Gate-2 roles.
7. Gate 5 freezes validation calibration/abstention/OOD/action authorization.
8. Gate 6 freezes the controller protocol.
9. Gate 7 builds/reviews the evaluation driver and final test manifest.
10. Only then create immutable `config.json` and materialize untouched test.

## Session record and live interfaces

- `agents/Codex/Session Summaries/HumanReport33.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Claude's Session-33 root-README milestone already records the base-role approval
and measured design findings. Codex did not add a duplicate public entry for the
bounded implementation hardening. The root `/data/` ignore remains adequate.
