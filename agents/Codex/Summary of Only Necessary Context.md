# Codex — Summary of Only Necessary Context

**Updated:** 2026-07-24 17:42 PDT after Codex Session 32
**Phase:** Phase 2 — Integration and Reproducibility Build
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

## Resume state

Gate 3 is jointly approved and closed at:

```text
dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1
```

The approved assignment file is unchanged from review:

```text
SHA-256 76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae
```

It is embedded under `values.scenario_manifest` in the still-draft config
through a one-way approval wrapper:

```text
approved parent draft:
dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180

current embedded draft:
dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56
```

Validation reconstructs the exact parent, validates the unchanged assignment
against it, removes only Gate 3, and uses the current self-hash to bind the
approval wrapper. Research materialization is limited to `dev|pilot|val`;
`test_materialization_allowed=false`.

## What Session 32 built

- exact assignment/config binding:
  - `Reproducibility Packet/scripts/utils/assignment_binding.py`
  - `Reproducibility Packet/scripts/embed_approved_assignment.py`
- real approved base-role generator:
  - `Reproducibility Packet/scripts/utils/assignment_generator.py`
  - `Reproducibility Packet/scripts/generate_assignment_dataset.py`
- independent on-disk audit:
  - `Reproducibility Packet/scripts/audit_assignment_dataset.py`
- new physical paths:
  - exact distal point mass with COM/inertia recomputation;
  - absolute time-windowed endpoint contact without widening the A1 pair;
  - compound structure+actuator plant faults;
  - compound plant+sensor realization at the existing injection boundary.

All eight assignment masses are compiled before the retained full run.
Bias/drift sign is balanced by `fault_seed`. Full compound component lists
remain non-deployable in the embedded assignment.

## Generated local base dataset

Ignored local root:

```text
data/gate3-base-dev-pilot-val-c1-s
```

Generation and independent audit both pass:

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

Dataset identity uses `train_seed=0`. The five model-training seeds remain
unexpanded until five Gate-4 fits exist. Estimator-output and controller-log
roles are intentionally pending those fits.

One earlier partial run was stopped and removed after Codex noticed its
preflight checked the six research-owned masses before generation but not the
two test-owned scalar values. The retained dataset was regenerated from zero
after an all-eight-mass preflight.

## Verification

```text
full packet:                 397 passed in 9.33 s
focused generator:          6 passed
compileall:                 pass
approved-assignment CLI:    pass
independent full data audit: pass
git diff --check:           pass
```

Audit artifacts:

```text
generation_audit.json
SHA-256 7db736e3508a4c8550b47b816ae448f17ee3b7193c8727c26a49dca6a9a211d7

independent_audit.json
SHA-256 40c37551e01a39379366837878e658b1927b7edf3427c342f6878c45768357ad
```

## Review gate now open

The exact-state handoff is appended to:

```text
chats/Claude-Codex/Phase 2 Integration and Config Freeze/
Phase 2 Integration and Config Freeze - Active.md
```

Requested response:

```text
APPROVE_GATE2_GENERATOR_BASE_ROLES
```

with no review-target edits, or
`BLOCK_GATE2_GENERATOR_BASE_ROLES` with artifact/file-specific findings.

Claude owns Gate 4 and should independently inspect the embedded binding,
generator, generated manifest/roles, and audit. Gate 2 must not be called
complete before explicit same-state approval and later estimator/controller
role completion.

## Gate status

```text
Gate 1: jointly approved complete
Gate-2 generic role write/load/join path: jointly approved complete
Gate-2 primary C1/S base roles: generated/audited; review open
Gate 2 overall: blocked pending review and Gate-4-produced remaining roles
Gate 3: jointly approved complete
Gate 4: open; Claude owns five-seed matched model fits
Gates 5–7: open
Final config.json: absent / unfrozen
Test identity or payload: 0
Research result: none
```

## Claim boundaries to preserve

- The 472 reservations are design/materialization infrastructure, not a fitted
  result.
- Do not infer a validation result from the presence of validation data.
- Do not expand the five training seeds before five real fits exist.
- Do not create `config.json`.
- Do not materialize any test identity or payload.
- The pilot→validation rung changes confound severity cleanly.
- Validation→test also moves from a per-trajectory half fraction to the complete
  factorial; Gate 7 and the Technical Report must say so.

## Required next sequence

1. Read `AgentPrompt.md` and all routed active context before work.
2. Read the newest Phase-2 physical transcript tail; Claude's review may have
   advanced beyond this summary.
3. Claude reviews and returns the exact approve/block token.
4. If approved, Gate 4 fits the matched learned attribution/RMA and interpretable
   models across training seeds `31001..31005`.
5. Complete estimator-output/controller-log roles from those real fits.
6. Gate 5 selects validation calibration, abstention, OOD, and authorization
   thresholds.
7. Gate 6 freezes the controller protocol.
8. Gate 7 builds/reviews the evaluation driver and final test manifest.
9. Only then create immutable `config.json` and materialize untouched test.

## Session records

- `agents/Codex/Session Summaries/HumanReport32.md`
- `agents/Codex/Progress Reports/Progress Report Session 32.md`

The root README running log has one lean generated-data milestone. The packet
README now documents Steps 2B–2C and the independent audit. `.gitignore` already
covers the generated `data/` root; no ignore change was needed.
