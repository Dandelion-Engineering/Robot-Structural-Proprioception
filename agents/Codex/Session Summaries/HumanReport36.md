# Human Report — Codex Session 36

**Current date and time:** 2026-07-25 16:05 PDT
**Phase:** Phase 2 — Integration and Reproducibility Build
**Session role:** Exact-state review of Claude's Amendment A2 proposal v3 and
unrun Protocol P v2
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)
**Governing decision:**
`BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Session decision:**
`BLOCK_AMENDMENT_A2_PROPOSAL_V3_PENDING_BRANCH_COMPLETE_SELECTION_AND_CELLWISE_NULL`

---

## Summary

### Complete startup and cross-review

I followed the complete `AgentPrompt.md` route before acting:

- all of `Project Details/Project Details.md`;
- the prior Codex continuity summary and workspace index;
- every summary in every Codex-inclusive chat;
- both active Codex-inclusive transcripts;
- Claude's complete Session-36 turn at the physical tail;
- `agents/Claude/Session Summaries/HumanReport36.md`;
- the review-cycle and Claim-Sheet playbooks;
- the approved Gate-3 assignment, its split/OOD rules, and its generator;
- the CRN implementation;
- the synchronous detection-floor and safe-probe implementations/results; and
- the current public running log.

The separate transcript-order monitoring thread required no reply.

### Claude's v3 proposal resolves the Session-35 requests in principle

Claude's replacement text made the four decisions requested in Session 35:

1. Protocol P is restricted to the assigned development diagnostic trajectory;
   the canonical ordinary trajectory remains probe-free.
2. The selected candidate is evaluated at all ten structural remaining-EI
   values reserved anywhere in the assignment, under development conditions,
   with direct value-by-value mapping and no monotonic cutoff.
3. The exact statistic is the vector L2 norm over all four gauges' cosine/sine
   coefficient differences at W=768 and 0.8 Hz; “gentlest” means the largest
   ramp fraction.
4. Test contact is pinned to the full validation offset pair `[1.8, 3.3]`.

Claude also audited the old threshold and correctly found that the committed
`0.4053 microstrain` value is a five-sigma **per-gauge W=640 detection
threshold**, not a generic floor. Protocol P had applied it to a four-gauge,
W=768 statistic. The coherent vector-8 W=768 five-sigma threshold in Claude's
text is `0.4388`; doubling it would be `0.878`, 7.7% above the former `0.810`
rule.

The same audit showed that the downstream problem needs a run-to-run null.
Claude reports that the delivered development fault-versus-healthy vector
distances fall inside the range of healthy-versus-healthy pairs that differ in
both seed and context. That is a development range statement, not a
distributional test, pilot result, or project result.

## Decisions on the choices handed to Codex

### Vector-8 approved

I approved vector-8 rather than max-across-gauges. The structural signal is
distributed across stations, the planned estimator receives the full station
set, and a statistic-matched null removes the prior scalar mismatch. Claude's
disclosure that vector-8 has roughly 1.20x better development signal-to-noise
than max-gauge remains part of the amendment record; it is relevant but does
not invalidate the pre-execution architectural choice.

### Diagnostic-only screening universe approved

Protocol P may screen only `trajectory_dev_diagnostic_b` and its four balanced
development context cells. There are no probe-overlay clones. The canonical
ordinary trajectory remains the pre-registered probe-free negative control.

### Ten-value development-condition ladder approved in concept

The ladder:

```text
0.35, 0.40, 0.45, 0.50, 0.55,
0.60, 0.65, 0.75, 0.85, 0.90
```

is an acceptable way to classify every reserved remaining-EI value without
reading a non-development payload. Direct lookup avoids a hidden monotonicity
assumption and avoids later-role relabeling. The current exact protocol remains
blocked on its pre-ladder branches, cellwise null, and OOD scope.

### Contact pair approved

The proposed test rule is exact:

```text
contact_test_sustained.contact_window_offset_s = [1.8, 3.3]
```

It copies validation timing and duration. It does not claim constant duration
across all roles.

### Protocol P v2 is a rewrite/supersession

The v1-to-v2 change is not a small correction. The statistic, null, selection,
severity map, and cost all changed. The next proposal should present one clean
Protocol P v2 and state that it supersedes unapproved v1. The append-only chat
retains the audit history.

### Ordinary structural rows stay in the primary estimand

I approved retaining the ordinary-trajectory structural rows in the primary
estimand. Removing them after learning that only diagnostic excitation can be
certified would redefine the population on excitation grounds.

I did **not** accept the claim that these rows “can only shrink” and “never
inflate” the S-minus-C1 contrast. A per-sample mechanics BLOCK does not prove
that a windowed estimator obtains no information, and it does not determine
the sign of a finite-sample suite contrast. The amendment must call the rows
uncertified by the diagnostic margin and retain a trajectory-stratified
secondary result for interpretation.

## Exact proposal decision

I returned:

```text
BLOCK_AMENDMENT_A2_PROPOSAL_V3_PENDING_BRANCH_COMPLETE_SELECTION_AND_CELLWISE_NULL
```

Protocol P remains deliberately unrun. Two issues are load-bearing; exact
identity and metric-role pins also remain.

### Blocking issue 1: Stage A can terminate before the ten-value ladder

Protocol P v2 currently says:

```text
select using worst-cell D at remaining EI 0.75
candidate is ineligible if D(0.75) < T1
run the ten-value ladder only after selection
nothing passes anywhere -> Case C
```

If every safe candidate has `D(0.75) < T1`, no candidate is selected and
Stages B–C never run. More severe values could still pass the operative
run-to-run margin. Because the protocol explicitly avoids a monotonicity
assumption, those unmeasured values cannot be inferred from `0.75`.

“No candidate cleared T1 at 0.75” is not “nothing passes anywhere.” It cannot
assign Case C or label all ten values sub-threshold.

The requested repair is:

- if at least one candidate is admissible, select the maximum worst-cell
  `D(0.75)` candidate using the stated tie-break, without a T1 eligibility
  cutoff;
- always run Stages B–C for that candidate;
- assign Case C only after all ten values are measured and none passes M2; and
- if every candidate fails a hard safety gate, define a separate
  `NO_ADMISSIBLE_PROBE` terminal branch and its prospective dataset/config
  action. This is a safety/method failure, not a measured Case C.

T1 may remain a development sensor-noise reference and sanity check. It does
not rank candidates; worst-cell D does.

### Blocking issue 2: pooled Q95 does not give a context-robust null

Stage C proposes 15 healthy/healthy distances in each of four context cells,
pooling all 60 to form one Q95. It reports the four cell-specific Q95 values
but does not use them in the gate.

A pooled 95th percentile can be lower than the 95th percentile in the noisiest
cell. Reporting that fact does not prevent the threshold from under-covering
that cell.

I gave two acceptable exact rules:

```text
Q95_c = within-cell healthy/healthy 95th percentile
pass(v) iff D(v,c) >= 2 * Q95_c for every cell c
```

or:

```text
T2 = 2 * max_c Q95_c
pass(v) iff min_c D(v,c) >= T2
```

The first uses cell-specific calibration; the second retains one conservative
scalar. A pooled Q95 may remain descriptive but cannot be the operative gate
alone.

### Exact execution identities remain unpinned

The packet's CRN streams are keyed by both:

```text
(sensor_seed, pair_id)
```

Stage C currently pins only six distinct development sensor seeds per cell.
That does not reproduce its run-to-run null. The next text must provide a
deterministic identity table or derivation for every Stage 0/A/B/C
`sensor_seed` and `pair_id`, including the five new healthy replicates per cell
implied by the stated 20-new-rollout cost.

Stage 0 must also pin its command/arguments and define one vector-8 sample as
one four-gauge window per realization. Otherwise the 200-realization null can
accidentally become 800 per-gauge samples. The current committed detector path
uses base seed 0, 200 realizations, a 3 °C window ramp, and fixed `pair_id=1`;
the extension may retain those choices explicitly.

### OOD mechanics labels must not change metric roles

The ladder's `0.45` and `0.55` values come from structural components of two
compound/OOD settings. The approved assignment says every `ood_flag=true` row
is excluded from four-way known-class metrics and enters only the
preregistered abstention/unknown/OOD metrics.

Therefore:

- a ladder result may characterize the component's mechanics testability;
- it may not turn a compound/OOD row into a known structural row; and
- Cases A/B must preserve the OOD rows' original metric role.

The next proposal must state this explicitly and pin the exact across-cell
aggregation in its outcome table.

## What this review approves and withholds

Approved for the next proposal state:

- vector-8 with the disclosed development advantage;
- diagnostic-only Protocol-P screening;
- the ten-value direct mapping in concept;
- exact test contact `[1.8, 3.3]`;
- Protocol P v2 as a clean superseding rewrite;
- ordinary structural rows remaining in the primary estimand, with no
  directional guarantee;
- the corrected mild-stratum wording from Session 35;
- the Case-B row-set/weight/dependence/one-decision structure from Session 35;
- full regeneration from zero only after written amendment and replacement
  assignment approval; and
- the forward sign-test correction.

Not approved:

- Protocol P execution;
- the written Amendment A2;
- a replacement assignment;
- amended dataset generation;
- Gate-4 model fitting;
- config freeze; or
- any pilot/validation/test payload generation or read for design selection.

Claude's next task is another **text-only** clean Protocol P v2 proposal. No
mechanics run or packet implementation is needed before its same-state review.

## Verification

All Python commands used the repository virtual environment.

The authoritative scoped command passes:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

```text
399 passed in 9.80 s
```

Additional checks:

```text
HEAD / origin/main before Codex edits: 76bb506 / 76bb506
config.json:                           absent
Protocol P:                            not run
non-development payloads read:         0
confirmatory identities/payloads:      0 / 0
retained ignored data:                 2,839 files / 3,857,663,628 bytes
```

I read the approved assignment's design values and already-committed
development evidence to audit the prospective protocol. I opened no pilot,
validation, test, or confirmatory payload/outcome.

## Transcript handling

The technical reply used the physical UTF-8 tail hard gate.

Before the write:

```text
physical lines:       4,982
Session-36 header:    absent
EOF-anchor matches:   1
physical last author: Claude
```

After the write:

```text
physical lines:         5,127
new header line:        4,984
new header count:       1
header after boundary:  yes
technical diff:         +145 / -0
physical last author:   Codex
git diff --check:       clean
```

The complete verified Claude EOF block was the patch anchor. No prior line was
deleted or moved. No transcript-order recurrence occurred, so the monitoring
thread was left unchanged.

## Public live-run status

Claude Session 36 already added the public running-log correction that the
old yardstick was misapplied by about 8% and that fault-versus-healthy
development distances lie inside the observed healthy-pair range, with
appropriate boundaries.

This session added a same-state internal design block, not a scientific result
or completed milestone. Per the public log's lean rule, I did not add another
root-README entry.

## Claim boundaries

This session:

- independently verifies the exact assignment/OOD and CRN-key contracts;
- accepts the vector-8, diagnostic-only, direct-ladder, contact, rewrite, and
  ordinary-row decisions at proposal level;
- finds a branch-incomplete T1 eligibility rule;
- finds an under-covering pooled-null rule;
- requires deterministic Stage 0/A/B/C identities and preservation of OOD
  metric roles; and
- keeps the correction loop text-only.

It does not:

- run Protocol P;
- establish T1 or T2 as a committed new packet result;
- establish which structural values are testable;
- independently reproduce Claude's Session-36 numeric null table;
- prove healthy and fault distributions indistinguishable;
- read non-development outcomes;
- approve Amendment A2 or a replacement assignment;
- generate amended data;
- fit or select a model;
- authorize control;
- freeze `config.json`;
- materialize confirmatory test identities/payloads; or
- answer the project hypothesis.

## Files created

- `agents/Codex/Session Summaries/HumanReport36.md`

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only exact-state block, approvals, and replacement requirements.
- `agents/Codex/README.md` — workspace index through Session 36.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  resume state.

## Files deliberately unchanged

- `README.md`, because Claude's current same-day public correction already
  covers the new evidence and this review is internal;
- `Claim Sheet.md` and `Accessible Claim Sheet.md`, because A2 remains
  unapproved;
- every Reproducibility Packet script, result, assignment, and config;
- the retained ignored pre-amendment dataset;
- the transcript-order monitoring thread;
- source ledgers; and
- `Reproducibility Packet/config.json`, which remains absent.

## `.gitignore` review

The root `/data/` rule still covers the retained 3.86 GB pre-amendment dataset.
The `/tmp/` rule still covers the duplicate Session-6 packet copy and scratch
outputs. Existing venv, cache, log, model, secret, LaTeX, OS, and IDE rules
remain appropriate. No new untracked artifact or sensitive file appeared, so
`.gitignore` requires no change.

## Next steps

1. Claude posts one clean **text-only** Protocol P v2 replacement that:
   - removes the T1 eligibility cutoff or otherwise makes the pre-ladder
     branch complete without inferring unmeasured values;
   - defines `NO_ADMISSIBLE_PROBE` and its prospective action;
   - uses a cellwise or max-cell M2 null;
   - pins every Stage 0/A/B/C `sensor_seed` and `pair_id`;
   - pins the Stage-0 null command/sample unit;
   - preserves compound/OOD rows' OOD metric role;
   - pins the across-cell outcome aggregation; and
   - removes the unsupported “can only shrink / never inflate” sentence while
     retaining ordinary structural rows.
2. Codex gives explicit same-state approval or a specific block on that exact
   text.
3. Only after proposal approval, Claude implements and runs Protocol P on the
   authorized development-only screening universe.
4. Codex reviews the exact implementation, result, and selected branch.
5. Only after that result, Claude writes the synchronized Claim Sheet,
   Accessible Claim Sheet, manifest/exclusion, packet amendment, and
   replacement hash-bound assignment.
6. Both agents review that written amendment and assignment at exact state.
7. If the approved branch advances, regenerate the non-test study from zero,
   repeat the identity/role/CRN audit, and resume Gate 4 only after amended
   feasibility clears.
8. Keep `config.json` absent and confirmatory identities/payloads at zero until
   Gates 2–7 close.

No regular Codex progress report is due until Session 40 unless a playbook
event trigger fires earlier.

## End state

```text
Gate 1: complete and jointly approved
Gate-2 generic write/load/join foundation: complete and jointly approved
Gate-2 original generator/base roles: exact-state review closed
Gate-2 generator hardening: exact-state review closed
Gate 2 overall: open pending Gate-4 estimator/controller roles
Gate 3: complete and jointly approved at the pre-A2 assignment
Gate 4: BLOCKED on branch-complete Protocol P v2 / corrected Amendment A2
Gates 5–7: open
Final config: UNFROZEN
Research result: none
Confirmatory identity/payload materialized: 0 / 0
```
