# Summary of Only Necessary Context

**Rewritten:** 2026-07-21 22:43 PDT

**Last completed Codex session:** 18

**Next Codex session:** 19

**Current branch:** `main`

**Project phase:** Phase 2 — Execution

**Configuration:** explicitly **unfrozen**

## Resume state

Codex Session 18 closed the Session-17 bounded task/contact/controller review loop after Claude Session 18 independently reproduced and explicitly approved the exact handed-off state. Codex then completed the matched noisy held-decision C1-vs-S information/reference-lifecycle review on that approved bounded development condition.

The new exact decision is:

`ADVANCE_INFORMATION_REFERENCE_LIFECYCLE_ONLY_BLOCK_RECOVERY_CONTROL_PROFILE`

The S suite clears the held-out information and transparent action-authorization gates at the one pre-movement decision. The current structural recovery action nevertheless worsens the only representative suite-informed tracking outcome, so recovery control remains blocked. This is not an evaluation-sized C1-vs-S result, learned attribution, probability calibration, OOD evidence, or permission to freeze `config.json`.

Codex explicitly approved the exact Session-18 implementation and appended the handoff to the active Phase-2 transcript. **Claude now owes genuine first review of this new state.** If Claude edits any handed-off artifact, Codex must inspect the actual edited files and provide a genuine owner re-review before the loop can close.

## What changed in Session 18

- Added `Reproducibility Packet/scripts/run_bounded_noisy_information_review.py`.
- Added four focused regressions in `Reproducibility Packet/tests/test_bounded_noisy_information_review.py`.
- Added five recorded artifacts under `Reproducibility Packet/results/bounded_noisy_information_review/`.
- Updated the packet runbook with Step 12, renumbered downstream steps through Step 16, and rewrote the current evidence boundary.
- Added one lean root Live Run Status entry for the information/control split.
- Accepted Claude's explicit same-state Session-17 approval, closing the bounded-redesign loop.

## Exact development condition and roles

The review inherits the approved bounded mechanics/controller schedule:

- contact plane: `z=0.200 m`;
- W=768 and stride=16;
- fault/probe onset: `1.000 s`;
- one held decision: step `1136`, time `2.272 s`;
- movement begins: `2.400 s`;
- full horizon ends: `6.000 s`.

Seed roles are disjoint:

- calibration-only sensor seeds: 14000-14099, 100 per canonical source;
- held-out evaluation sensor seeds: 14100-14147, 48 per canonical source;
- representative full-horizon seed: 14100, predeclared within the held-out role.

One hundred calibration seeds resolve five observations in the declared 5% healthy tail. Suite-specific references use calibration-only healthy mean/scale, a higher-method 95th-percentile leave-one-out detection threshold, labeled fault centroids, and a leave-one-out selective-margin threshold at no more than 5% selective error. Held-out seeds never tune these values.

Every window is captured from a real noisy `CablePlant -> OnlineSensorSession(S) -> ObservedJointPDController` trajectory. C1 is projected from the exact same S window, so C1/S share plant history, commands, sensor seed, and common observation channels while differing in gauge availability. References remain suite-specific.

## Held-out information/action result

| Suite | Macro-F1 | Balanced accuracy | Healthy FA | Min fault detect | Structure recall | Actuator recall | Sensor recall | Healthy false-actionable | Information | Action |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| C1 | 0.704 | 0.760 | 4.2% | 8.3% | 8.3% | 100% | 100% | 4.2% | BLOCK | BLOCK |
| S | 0.995 | 0.995 | 2.1% | 100% | 100% | 100% | 100% | 2.1% | PASS | PASS |

False-actionable healthy decisions are C1 seeds 14137 and 14141 and S seed 14141, all called structure.

Both suites' leave-one-out fault prototypes have 100% calibration selective coverage and 0% error, selecting margin threshold 0. Held-out known-fault selective accuracy is 100%, and no known fault abstains. This means the known development faults do not stress abstention; compound/OOD faults, calibrated probabilities, and validation-frozen selective thresholds remain open.

Accepted prototype calls are one-hot schema/recovery instruments. They are not calibrated learned-head probabilities.

## Separate representative control sensitivity

All eight representative source/suite rows have:

- one classifier evaluation held through the run;
- no source-specific command change before the decision;
- exactly one bounded contact episode;
- zero A1 safety flags; and
- exact matched C1/S pre-decision plant and shared-observation hashes.

Representative paired `J_5s`:

| Source | C1 gate | S gate | C1 `J_5s` | S `J_5s` | S change | Control implication |
|---|---|---|---:|---:|---:|---|
| healthy | correct no action | correct no action | 0.8604 | 0.8604 | 0.0% | no suite-informed difference |
| structure | withheld | correct structural action | 0.8589 | 1.0184 | -18.6% | BLOCK current structural action |
| actuator | correct action | correct action | 0.8667 | 0.8667 | 0.0% | no suite-informed difference |
| sensor | correct no action | correct no action | 0.9937 | 0.9937 | 0.0% | no suite-informed difference |

The structural S action lowers peak force from 2.051 N to 0.499 N, but both arms already have zero safety incidents. It therefore does not establish a safety benefit and cannot offset the worse tracking result. This is a one-seed sensitivity that may block a harmful controller profile; it cannot establish a recovery advantage.

## Evidence boundary that must survive review

- Information/reference lifecycle advances; recovery control does not.
- Detection, attribution/action authorization, representative mechanics, and control consequence are separate gates.
- C1/S decision windows are common-random-number matched; suite references are fit independently.
- The prototype instrument is not the learned attribution head or RMA.
- Zero abstentions on known faults do not establish compound/OOD behavior.
- The representative continuation has one seed per source/suite and no paired uncertainty interval.
- `z=0.200 m`, W/stride, controller gains/limits/timing, sensor constants, severity/onset grids, references, and thresholds remain development candidates.
- The central Claim Sheet question remains open, and `config.json` remains unfrozen.

## Verification state

- Focused new tests: **4 passed**.
- Full Reproducibility Packet: **159 passed**.
- `compileall -q scripts tests`: passed.
- New CLI `--help`: passed.
- Fresh final full run with 12 workers: passed in 704.5 s and returned the recorded split decision.
- Strict JSON: no `NaN` or `Infinity` tokens.
- Generator/artifact audit: all five outputs reproduce byte-for-byte from the recorded strict JSON and final writers.
- Recorded row counts: 2 suite information rows, 384 held-out decision rows, 8 representative online rows.
- Pre-decision histories: 592 physical calibration/evaluation histories, zero contact and zero A1 safety rows.
- Artifact SHA-256:
  - summary: `053b97237eae4f3c99b39af40643971415229488d20220a3df5e471b72c20d37`
  - information rows: `d3e62eb797131b6690c725b77d847da406c585e208a7c92d93a89767964ec90a`
  - held-out decisions: `71b044e6459e65ffc4ddef3eafa5aa460cb07166ecaf5825e7e7ee7a340709b8`
  - representative rows: `25187670191540f5fd91930471aabe70048c795edefbe497aa309e36298a17ee`
  - report: `7248d802aabc42880637378b58708fa7fbc2ae691b5baeda0067dd389a8277fd`
- Transcript hard gate: pre-write 1,227 lines; new header exactly once at line 1,229; Codex physically last at line 1,261.

## Open review loop

Claude must first-review this exact state:

- `Reproducibility Packet/scripts/run_bounded_noisy_information_review.py`
- `Reproducibility Packet/tests/test_bounded_noisy_information_review.py`
- `Reproducibility Packet/results/bounded_noisy_information_review/*`
- `Reproducibility Packet/README.md`
- root `README.md` wording
- Codex's appended Session-18 handoff in the active Phase-2 transcript

Silence, a handoff, continuity text, or unrelated edits are not approval. The loop closes only on explicit same-state approval or owner approval after genuine review of reviewer edits.

## Next technical gate after approval

Redesign the structural recovery action/control sensitivity before any freeze or evaluation-sized comparison:

1. preserve the exact bounded mechanics condition and real noisy held-decision information path;
2. define a predeclared structural action family or bounded tuning role without using evaluation data;
3. require suite-informed action to improve a declared tracking or safety readout rather than merely change torque/force;
4. preserve action-gate false-authorization and withholding accounting;
5. retain the full onset+5 s A1 safety audit and exact C1/S pre-decision matching; and
6. keep any small screen or one-seed continuation labeled development sensitivity.

Validation-sized healthy/four-class calibration, per-suite probability calibration, compound/OOD faults, severity/onset grids, non-load-bearing sensor constants, class/abstention/selective/OOD thresholds, learned attribution + RMA, whole-trajectory/fault-setting split, deployable-loader leakage, role hashes, multi-run storage, immutable config/schema gates, and the evaluation-sized closed-loop comparison all remain unresolved.

## Required startup sequence for Session 19

1. Re-read `AgentPrompt.md` and follow it exactly.
2. Read all of `Project Details/Project Details.md`.
3. Read this file.
4. Read every relevant `Summary.md`, then the complete active Phase-2 transcript to physical EOF.
5. Read Claude's latest Human Report and continuity.
6. Inspect git status/HEAD and the actual files before trusting this summary if the repo has advanced.
7. Process Claude's review first. If it is explicit same-state approval, close the loop; if Claude edited, genuinely re-review those edits.
8. Keep `config.json` unfrozen unless all remaining gates actually close.

## Closeout conventions to preserve

- Active chat is append-only: read the UTF-8 physical tail, record the pre-write line count, patch only a unique multi-line EOF anchor, then assert the new header occurs exactly once after the old tail and the intended agent is physically last.
- Rewrite this continuity file completely at each Codex closeout.
- Add the next `HumanReportN.md`; keep `agents/Codex/README.md` purpose-oriented.
- Keep public Live Run Status lean and milestone-based.
- Run staged diff hygiene, then commit exactly `Codex Session N` and push.
- Next regular Codex progress report: Session 24 unless a Claim Sheet amendment or phase transition triggers one earlier.
