# Human Report — Codex Session 35

**Current date and time:** 2026-07-25 15:19 PDT
**Phase:** Phase 2 — Integration and Reproducibility Build
**Session role:** Exact-state review of Claude's corrected Amendment A2 proposal
and unrun Protocol P
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json`
remains absent)
**Governing decision:**
`BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Session decision:**
`BLOCK_AMENDMENT_A2_PROPOSAL_V2_PENDING_EXECUTABLE_PROTOCOL_AND_STRATUM_MAP`

---

## Summary

### Complete startup and cross-review

I followed the complete `AgentPrompt.md` startup route before acting:

- all of `Project Details/Project Details.md`;
- the prior Codex continuity summary and workspace index;
- every summary in every Codex-inclusive chat;
- both active Codex-inclusive transcripts;
- Claude's complete Session-35 turn at the physical tail;
- `agents/Claude/Session Summaries/HumanReport35.md`;
- the review-cycle playbook;
- the Claim Sheet's locked evaluation bars;
- the approved Gate-3 assignment and its validators/generator;
- the structural-separability and synchronous safe-probe implementations; and
- the current public running log.

The separate transcript-order monitoring thread required no reply.

### Claude's corrected proposal closes the original two objections

Claude accepted the Session-34 block and corrected both formulations that
caused it.

First, the mild-stratum statement now says exactly:

> In the assigned development contexts at remaining EI 0.75 and 0.50, the
> current excitation does not provide a gauge-borne structural signature that
> supports the planned S-versus-C1 hypothesis test; the detectable structural
> effect is instead in C1 IMU channels.

That sentence no longer promotes an eight-cell development diagnostic into a
result for all 472 delivered reservations or for a complete mild band.

Second, the conditional Case-B estimand now defines:

- the primary four-way population;
- shared healthy, actuator, and sensor rows;
- row weight 1;
- one model per suite trained on the complete manifest;
- paired dependence across shared rows;
- one project-level confirmatory decision; and
- a separately labeled non-confirmatory sub-threshold result.

This removes the undefined “four-way macro-F1 per band” formulation. I approved
those two corrected components for reuse in the next proposal state.

### The ramp mismatch and sign-test correction check out

I independently checked the committed Session-35 correction and its motivating
implementation state.

The ramp mismatch is real:

```text
approved assignment field:
  envelope = raised_cosine
  ramp fraction = absent

screen_synchronous_safe_probe.py default:
  ramp_period_fraction = 0.125

assignment_generator.py delivered finite burst:
  diagnostic_tip_load_ramp_s = duration / 2
```

The current assignment therefore did not pin the quantity that differed
between the screen and delivered data. This supports pinning the envelope ramp
before any amended generation.

The sign-test forward correction is also correct. The diagnostic-only report
has four paired cells, so the exact two-sided sign-test floor is:

```text
2^(1 - 4) = 0.125
```

The updated report now says that no channel can reach `p <= 0.05` with four
cells and that the empty table is arithmetically forced rather than evidence of
no channel effect. The pooled eight-cell report retains its correct 0.0078
floor. The code derives the floor from `n_cells`.

I did not replay Claude's 32 development-mechanics rollouts for Findings B and
C. I raised no objection to retaining their stated development-only role as
motivation, but this review does not independently certify their numerical
values.

## Exact proposal decision

I returned:

```text
BLOCK_AMENDMENT_A2_PROPOSAL_V2_PENDING_EXECUTABLE_PROTOCOL_AND_STRATUM_MAP
```

Protocol P remains deliberately unrun. The block has two load-bearing design
issues and two exact-definition requirements.

### Blocking issue 1: “both development trajectories” conflicts with the assignment

The approved assignment says:

```text
trajectory_dev_ordinary_a:
  excitation = ordinary
  diagnostic_probe = null

trajectory_dev_diagnostic_b:
  excitation = diagnostic
  diagnostic_probe = 0.05 N
```

The assignment validator requires ordinary trajectories to carry no probe.
Protocol P nevertheless varies ramp and amplitude, requires the 0.8 Hz
synchronous margin in **both** development trajectories, and requires each
candidate to clear every development cell.

Those statements are not jointly executable. Leaving the ordinary trajectory
canonical gives it no candidate probe to vary. Overlaying a probe turns it into
a diagnostic mechanics condition rather than the assigned ordinary trajectory.

The replacement proposal must therefore either:

1. restrict P to the assigned diagnostic trajectory; or
2. define probe-overlay clones of the development task paths, explicitly label
   them development-only mechanics-screen conditions rather than dataset
   trajectories, and preserve or replace the canonical ordinary condition
   deliberately.

The implementation cannot be left to choose this after amendment approval.

### Blocking issue 2: development outcomes do not assign other-role severities

Protocol P measures only the development structural settings, while the
approved assignment reserves different remaining-EI values by role:

```text
dev:    0.50, 0.75
pilot:  0.60, 0.85
val:    0.40, 0.90
test:   0.35, 0.65
```

Cases A and B refer to every reserved structural severity and to a partition
of structural settings into testable and sub-threshold strata. P does not
classify any pilot, validation, or test setting.

The pilot cannot serve as the first out-of-development check and also
retroactively determine which confirmatory rows enter the primary estimand.
Before P runs, the proposal must give a branch-complete development-only rule
that assigns every role's listed severity for every possible P outcome. An
explicit role-by-role table is sufficient. A numerical cutoff is also possible
if its direction, equality handling, monotonicity assumption, and response to
a contradictory pilot margin are predeclared.

If the present grids cannot support that rule, a complete replacement grid can
be proposed without generating or reading non-development payloads. The pilot
may stop or bound transfer; it may not relabel validation/test rows after
observing later-role results.

### Exact pin 3: the P margin lacks a four-gauge aggregation rule

“Observed-path synchronous gauge coefficient L2 distance” says how to combine
the cosine and sine coefficients within a gauge, but not how to combine four
gauges.

The existing safe-probe code:

1. fits the known-frequency coefficients per gauge;
2. takes the L2 norm of each gauge's cosine/sine pair; and
3. uses the maximum amplitude across gauges.

Protocol P must state the exact scalar it compares with `0.810 microstrain`.
If the intended rule is the existing one, the branch should explicitly use the
worst context of the maximum per-gauge coefficient norm. A vector norm across
all gauges is a different yardstick and must be named if intended.

The replacement should retain matched sensor seeds, W=768 from onset,
0.8 Hz, and the worst-context comparison. It must also define “gentlest ramp”;
for the proposed grid that appears to mean the largest ramp fraction, 0.5, but
the tie-break cannot depend on interpretation.

### Exact pin 4: contact duration is not constant “across rungs”

The assignment's current contact offsets are:

```text
dev:    [2.0, 2.5]   0.5 s
pilot:  [2.6, 3.2]   0.6 s
val:    [1.8, 3.3]   1.5 s
test:   [1.6, 3.8]   2.2 s
```

Having test inherit only validation's **length** leaves the test start phase
undefined and does not make duration constant across all four rungs. The
replacement must give the exact test `contact_window_offset_s` pair and scope
the rationale correctly. If the control is only equal duration between
validation and test, it should say that. If timing as well as duration is meant
to match, the full validation offset pair should be copied.

## What this review approves and withholds

Approved for the next proposal state:

- the corrected mild-stratum evidence statement;
- the Case-B row-set, weighting, dependence and one-decision estimand
  structure;
- the sign-test report correction; and
- full regeneration from zero only after the written amendment and replacement
  assignment receive explicit same-state approval.

Not approved:

- Protocol P execution;
- the written Amendment A2;
- a replacement assignment;
- amended data generation;
- Gate-4 model fitting;
- config freeze; or
- any pilot, validation, or confirmatory test generation/read for this
  selection decision.

Claude's next task is another **text-only proposal state** pinning the four
items above. No implementation or P run is needed before that review.

## Verification

All Python commands used the repository virtual environment.

The first root-wide `pytest -q` invocation found the ignored
`tmp/session6_packet_copy/tests` duplicate modules and stopped with three
collection mismatches. This is the documented workspace-discovery problem, not
a packet failure.

The authoritative scoped command passes:

```powershell
.\venv\Scripts\python.exe -m pytest -q "Reproducibility Packet\tests"
```

```text
399 passed in 9.61 s
```

Additional checks:

```text
HEAD / origin/main before Codex edits: 8673eab / 8673eab
config.json:                           absent
Protocol P:                            not run
non-development payloads read:         0
confirmatory identities/payloads:      0 / 0
```

Reading the approved assignment's pilot/validation/test **design values** was
necessary to audit the prospective mapping. No pilot, validation, or test
payload or outcome was opened.

## Transcript handling

The technical reply used the physical-tail hard gate.

Before the write:

```text
physical lines:       4380
Session-35 header:    absent
SHA-256:
156154A9A692BE05035B251ED4804A9A49E47D014B032775FFF3FAE14990E70A
```

After the write:

```text
physical lines:         4541
new header line:        4382
new header count:       1
header after boundary:  yes
old 4380-line prefix:   line-identical to HEAD
transcript diff:        +161 / -0
physical last author:   Codex
```

The complete verified Claude EOF block was the patch anchor. No
transcript-order recurrence occurred, so the monitoring thread was left
unchanged.

## Public live-run status

The public README already contains Claude's same-day correction that the ramp
was unpinned, the prior “2x–40x too mild” characterization was withdrawn, and
joint probe/severity selection remains proposed rather than run.

This session produced no new scientific result or finished artifact; it kept an
internal design proposal blocked on exact executability. Per the live-run
README's lean, milestone-only rule, I did not add another public entry. The
technical transcript and agent continuity carry the exact review state.

## Claim boundaries

This session:

- verifies the ramp-field mismatch and sign-test correction;
- closes the two original proposal objections at the text/estimand level;
- finds two new load-bearing executability gaps in Protocol P;
- requires exact pinning of the gauge statistic and contact offsets;
- preserves full-regeneration and final-config gates; and
- keeps the correction loop text-only.

It does not:

- run Protocol P;
- establish which structural severities are testable;
- independently certify Findings B–C numerically;
- read non-development payloads or outcomes;
- approve Amendment A2 or a replacement assignment;
- generate amended data;
- fit or select a model;
- authorize control;
- freeze `config.json`;
- materialize confirmatory test; or
- answer the project hypothesis.

## Files created

- `agents/Codex/Session Summaries/HumanReport35.md`

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only exact-state block and repair conditions.
- `agents/Codex/README.md` — workspace index through Session 35.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten
  resume state.

## Files deliberately unchanged

- `README.md`, because no new public milestone occurred;
- `Claim Sheet.md` and `Accessible Claim Sheet.md`, because A2 is not approved;
- all Reproducibility Packet scripts, results, assignments, and configs;
- the retained ignored pre-amendment dataset;
- the transcript-order monitoring thread;
- source ledgers; and
- `Reproducibility Packet/config.json`, which remains absent.

## `.gitignore` review

The root `/data/` rule still covers the retained 3.86 GB pre-amendment dataset.
The `/tmp/` rule still covers the duplicate Session-6 packet copy and local
scratch outputs. Existing venv, cache, log, model and secret rules remain
appropriate. No new untracked artifact or sensitive file appeared, so
`.gitignore` requires no change.

## Next steps

1. Claude posts a replacement **text-only** A2 proposal defining:
   - the exact Protocol-P trajectory/screening universe;
   - the exact four-gauge scalar and ramp tie-break;
   - the branch-complete mapping from development outcomes to every role's
     structural settings; and
   - the exact test contact offsets and correctly scoped rationale.
2. Codex gives explicit same-state approval or a specific block on that text.
3. Only after proposal approval, Claude implements and runs Protocol P on the
   authorized development-only screening universe, with zero non-development
   payload or outcome reads.
4. Codex reviews the exact Protocol-P implementation, result and selected
   branch.
5. After that branch is established, Claude writes the synchronized Claim
   Sheet, Accessible Claim Sheet, manifest/exclusion and packet amendment plus
   replacement hash-bound assignment.
6. Both agents review that written amendment and assignment at exact state.
7. If the approved branch advances, regenerate the non-test study from zero,
   re-audit
   identity/role/CRN invariants, and resume Gate 4 only after its amended
   feasibility condition clears.
8. Keep `config.json` absent and confirmatory identities/payloads at zero until
   Gates 2–7 close.

## End state

```text
Gate 1: complete and jointly approved
Gate-2 generic write/load/join foundation: complete and jointly approved
Gate-2 original generator/base roles: exact-state review closed
Gate-2 generator hardening: exact-state review closed
Gate 2 overall: open pending Gate-4 estimator/controller roles
Gate 3: complete and jointly approved at the pre-A2 assignment
Gate 4: BLOCKED on executable Protocol P / corrected AMENDMENT A2 proposal
Gates 5–7: open
Final config: UNFROZEN
Research result: none
Confirmatory identity/payload materialized: 0
```
