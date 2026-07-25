# Summary of Only Necessary Context — Codex

**Last completed Codex session:** 34
**Date:** 2026-07-25
**Current phase:** Phase 2 — Integration and Reproducibility Build
**Primary active thread:** `chats/Claude-Codex/Phase 2 Integration and Config
Freeze/Phase 2 Integration and Config Freeze - Active.md`

## Resume here

Gate 4 is stopped on a corrected Claim-Sheet amendment proposal:

```text
BLOCK_AMENDMENT_A2_PROPOSAL
BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION
```

Claude's Session-34 proposal correctly identified that the current structural
fault settings do not support an interpretable hypothesis test. Codex
independently reproduced that finding. Codex nevertheless blocked the exact
proposal because:

1. it promoted an eight-context **development-only** diagnostic into a stated
   result for all 472 delivered development/pilot/validation reservations; and
2. it declared four-way macro-F1 “per band” even though only the structural
   class has proposed mild/severe membership.

Claude's next required action is a corrected short A2 proposal, not an
implementation. Codex should review the exact replacement and return an
explicit approval or specific block. No Claim-Sheet edit, replacement
assignment, data regeneration, Gate-4 fit, or final-config work is authorized
until that proposal converges and the later written amendment is jointly
approved at the same state.

## Gate state

```text
Gate 1:
  complete and jointly approved

Gate-2 generic role write/load/join path:
  complete and jointly approved

Gate-2 real primary C1/S generator/base roles:
  complete and exact-state review closed

Gate-2 bounded generator hardening:
  complete and exact-state review closed by Claude Session 34 token
  APPROVE_GATE2_GENERATOR_HARDENING

Gate 2 overall:
  open only for later Gate-4 estimator-output/controller-log roles

Gate 3:
  complete and jointly approved at the current pre-A2 assignment
  any A2 replacement will require a new exact assignment/review loop

Gate 4:
  BLOCKED on corrected AMENDMENT_A2

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

It is approximately 3.86 GB. Do not call it a final amended dataset. If a
corrected A2 amendment and replacement assignment receive joint approval,
Codex has chosen **full regeneration from zero** rather than changing the
expansion order or silently reusing these payloads under a new config hash.
The present set should then be recorded as a superseded pre-amendment set in
the packet exclusion trail. Do not delete it before the replacement is approved
and the provenance/retention action is explicit.

## Session-34 separability reproduction

Claude added:

- `Reproducibility Packet/scripts/screen_structural_separability.py`;
- pooled results under
  `Reproducibility Packet/results/structural_separability/pooled_trajectories/`;
  and
- diagnostic-only results under
  `Reproducibility Packet/results/structural_separability/diagnostic_trajectory_only/`.

Codex regenerated both analyses from the retained dataset with:

`.\venv\Scripts\python.exe`

The independent outputs were written under the ignored root:

`tmp/codex-session34-a2-review/`

After excluding only `generated_utc` and the absolute `dataset_root` string,
every substantive top-level JSON field exactly matched the tracked output for
both variants:

```text
config_hash
contrast_order
contrasts
n_cells
screen
split
stride
suites
trajectory_filter
window_steps
windows_per_run
```

Decision-relevant pooled results:

```text
contrast / suite              interpretable AUROC   learned AUROC
structure EI 0.75 / C1        0.453                  0.250
structure EI 0.75 / S         0.469                  0.172
structure EI 0.50 / C1        0.469                  0.750
structure EI 0.50 / S         0.578                  0.703
actuator gain 0.50 / C1       0.594                  0.891
actuator gain 0.50 / S        0.500                  0.859
```

The structural result is not convincing at either development severity, S does
not beat C1, the actuator positive control separates, and the pooled
per-channel structural effects clearing the sign test are IMU rather than gauge
channels. No validation or test payload was read.

Interpret this as:

```text
current structural settings fail the prerequisite feasibility gate
```

Do not interpret it as:

```text
the project hypothesis is false
the whole mild band has a negative result
pilot/validation confirms the development result
```

## Exact A2 proposal review boundary

Codex supports these directions:

- retain the current severity settings as a mild structural stratum;
- add a prospectively specified severe structural stratum where the mechanism
  can clear the predeclared detection margin;
- re-derive the diagnostic probe amplitude inside the unchanged A1 ceiling;
- decide the confirmatory contact profile deliberately;
- keep the joint-space task, score, controller question, and project hypothesis
  unchanged; and
- regenerate from zero under one coherent amended expansion/assignment.

The corrected proposal must replace two formulations.

### Correct mild-stratum evidence statement

The current defensible statement is:

> In the assigned development contexts at remaining EI 0.75 and 0.50, the
> current excitation does not provide a gauge-borne structural signature that
> supports the planned S-versus-C1 hypothesis test; the detectable structural
> effect is instead in C1 IMU channels.

The development screen is the disclosed reason for A2. It is not the final
result of the complete mild stratum. The amended mild stratum requires its own
later role-authorized analysis.

### Define any per-band four-class estimand

Before four-way macro-F1 can be called “per band,” the design must specify for
every split:

1. which healthy, actuator, and sensor reservations accompany each structural
   stratum;
2. whether non-structural rows are shared;
3. how pairing, weighting, confidence intervals, and multiplicity preserve any
   shared-row dependence;
4. exact manifest membership and sample weight; and
5. which outcome is project-level primary versus structural
   severity-stratified secondary.

The severe stratum may carry a headline complete four-class comparison only if
that entire comparison is prospectively defined. Otherwise, severe may carry a
headline **structural sub-comparison**, while project-level macro-F1 uses one
fully specified manifest.

### Prospective selection requirements

The corrected proposal/written amendment must:

- use development-authorized mechanics for severity/probe selection;
- avoid observing replacement pilot, validation, or test outcomes during that
  selection;
- predeclare the candidate severity/probe grid;
- define the 2.0x synchronous-margin rule across the assigned context
  distribution, not a single favorable payload/contact/seed cell;
- keep the A1 angular-rate ceiling as a hard failure boundary;
- predeclare the no-candidate-clears action;
- choose the replacement test contact profile without generating or reading
  confirmatory identities/payloads;
- synchronize Claim-Sheet Slots 11–13, split/manifest semantics, exclusion
  trail, packet instructions, and `Accessible Claim Sheet.md`; and
- require explicit same-state approval of the written amendment and replacement
  assignment before generation.

## Contact-design fact that remains live

The pre-A2 472-run set assigned contact to 236 runs but realized actual plane
contact in only 11 pilot encoder-bias/drift runs:

```text
development / pilot / validation actual-contact runs:
0 / 11 / 0
```

Assigned contact is balanced, but realized contact is fault-coupled and loudest
in an S-exclusive gauge channel. This is not a headline result. It makes the
confirmatory contact profile a deliberate pre-freeze decision and a Gate-7/
Technical-Report audit item.

## Forward corrections that must not be lost

### Session-33 severity row

`agents/Codex/Session Summaries/HumanReport33.md` contains an incorrect first
row in its measured severity table. The concluded report stays unchanged, but
the Technical Report/limitations record must use:

```text
0.90 | 0.0544 microstrain | 0.13x | validation
```

not `0.95 | 0.0090 | 0.02x | development`.

### Diagnostic sign-test report label

`Reproducibility Packet/scripts/screen_structural_separability.py` line 742
hard-codes “exact 8-cell floor (p = 0.0078)” into both reports.

- It is correct for the pooled screen (`n_cells = 8`).
- It is incorrect for the diagnostic screen (`n_cells = 4`), where a two-sided
  sign test cannot reach 0.05.

Claude should correct the report wording forward before packet lock. This is a
label defect, not a change to the exact reproduced results or pooled no-gauge
conclusion.

## Verification baseline

Use the repository venv, not bare system Python.

Latest authoritative packet test:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

Session-34 result:

```text
399 passed in 10.53 s
```

Do not use root-wide `pytest -q` as the clean packet command: ignored
`tmp/session6_packet_copy/tests` duplicates three test module names and causes
collection mismatch errors. This is workspace discovery, not a packet test
failure.

The separability scripts emit NumPy warnings for NaN-padded channels absent
from one suite. Outputs still complete and reproduce exactly.

## Transcript-order state

Session 34 had a caught same-session append-placement recurrence:

- the first patch matched a generic Claude separator and placed the new turn at
  line 2,320;
- the immediate physical-tail assertion caught it;
- only Codex's new misplaced copy was removed before commit;
- the original 3,969-line transcript state was restored;
- the identical turn was appended with Claude's complete final EOF block; and
- the final technical diff is `+137 / -0`.

Final technical-transcript proof:

```text
pre-write lines:       3969
post-write lines:      4106
Session-34 header:     line 3971
header count:          1
physical last author:  Codex
```

The incident is disclosed at the physical tail of
`chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
with its own `+31 / -0` append proof. The clean-append streak is over.

For future transcript writes:

1. read the UTF-8 physical tail;
2. record the pre-write line count;
3. use the **complete verified EOF block in the actual patch**, not a shorter
   generic subset;
4. prove the new header occurs exactly once after that boundary;
5. re-read the physical tail; and
6. require `+N / -0` before closeout.

## Public record

Root `README.md` now preserves Claude's prior proposal entry and appends a
correction:

- the negative screen is development-only;
- no result exists for all 472 delivered rows or a complete mild band;
- per-band four-class accuracy is undefined until all class membership and
  weighting are specified;
- coherent regeneration is pending a corrected/approved amendment; and
- final config and confirmatory test remain untouched.

Do not silently rewrite the older public entry; the correction is the operative
later record.

## Review-cycle state and next actions

The active technical thread is physically last with Codex's narrow block.

Next:

1. Read any new Claude turn and Claude's latest HumanReport before acting.
2. Review the exact corrected short A2 proposal.
3. Approve only if it fixes both the evidence statement and complete estimand.
4. After proposal approval, review the written Claim-Sheet and Accessible
   Claim-Sheet amendment at the exact same state.
5. Review a replacement hash-bound assignment that implements the approved
   severity bands/contact rule without context leakage.
6. Only then authorize full from-zero non-test regeneration and repeat the
   independent identity/role/CRN audit.
7. Resume Gate 4 only after the amended development feasibility gate clears.
8. Keep final `config.json` absent and confirmatory identity/payload count at
   zero until Gates 2–7 close.

No regular Codex progress report is due until Session 40 unless a playbook
trigger requires an earlier report.

## Key files

- `agents/Codex/Session Summaries/HumanReport34.md`
- `agents/Claude/Session Summaries/HumanReport34.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration
  and Config Freeze - Active.md`
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order
  Monitoring - Active.md`
- `Claim Sheet.md`
- `Accessible Claim Sheet.md`
- `Reproducibility Packet/config/proposed-gate3-assignment-v0.1.json`
- `Reproducibility Packet/config/draft-config-v0.1.json`
- `Reproducibility Packet/scripts/screen_structural_separability.py`
- `Reproducibility Packet/results/structural_separability/`
- `README.md`

## Non-negotiable boundaries

- Development/pilot screens are not confirmatory results.
- The current separability failure is a feasibility result, not a hypothesis
  failure.
- Do not call the unobserved mild stratum negative.
- Do not call a metric per band until every class and weight in the metric is
  defined.
- Do not inspect validation/test to choose the amended design.
- Do not materialize confirmatory identities or payloads before final freeze.
- Reviewer edits or silence are not approval; require explicit same-state
  approval.
- Keep detection, attribution, information/action authorization, and control
  outcome separate.
- Keep `config.json` absent until all remaining gates close.
