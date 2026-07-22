# Human Report 18 — Codex

**Current Date and Time:** 2026-07-21 22:43 PDT

**Agent:** Codex · **Session:** 18 · **Project phase:** Phase 2 — Execution

---

## Summary

This session closed the Session-17 bounded task/contact/controller review loop and completed the matched noisy held-decision C1-vs-S information/reference-lifecycle review on that approved bounded condition.

Claude Session 18 genuinely first-reviewed the complete Session-17 state, independently drove the selected and negative-control planes, reproduced every selection gate, obtained 155 passing tests and byte-identical artifacts, found no defect, and explicitly approved Codex's exact handed-off state. Codex accepted that same-state approval in the active Phase-2 transcript, closing the old review loop.

The new review replaces fixed source-correct diagnoses with real noisy coefficient-reference decisions at the exact first causal post-probe decision. It uses 100 calibration-only sensor seeds per source to resolve the declared 5% healthy tail, 48 disjoint held-out seeds per source for all information/action-gate rates, suite-specific references, one held decision at step 1136 / 2.272 s, and a matched full-horizon representative continuation. Detection, attribution/action authorization, and control consequence are reported as separate evidence layers.

The S suite clears the held-out information and transparent action-authorization gates: macro-F1 0.995, 2.1% healthy false alarms/false-actionable calls, 100% per-fault detection and recall, and 100% correct action authorization for the actionable structure and actuator faults. C1 blocks because structural detection/recall is only 8.3%, despite 100% actuator and sensor recall.

The current recovery-control profile does not advance. In the only representative pair where S's extra information changes the action, S correctly identifies structure and applies the structural derate, but `J_5s` worsens from 0.8589 to 1.0184, an 18.6% degradation relative to C1's withheld action. Peak force drops from 2.051 N to 0.499 N, but both arms already have zero A1 safety incidents, so this does not establish a safety benefit.

The exact split decision is:

`ADVANCE_INFORMATION_REFERENCE_LIFECYCLE_ONLY_BLOCK_RECOVERY_CONTROL_PROFILE`

This is development information/reference-lifecycle evidence only. It is not an evaluation-sized C1-vs-S control result, does not calibrate learned probabilities, does not close compound/OOD abstention, and does not authorize a configuration freeze. `config.json` remains unfrozen.

Codex appended the exact state and boundary to the active Phase-2 transcript and requested Claude's genuine first review. That new review loop is open.

## What was accomplished

### 1. Followed the controlling workflow and closed the prior review loop

The full `AgentPrompt.md` workflow was followed:

- read all of `Project Details/Project Details.md`;
- read Codex's continuity file and every relevant Codex-including chat summary;
- ingested the complete 1,227-line active Phase-2 transcript before writing;
- read Claude's latest Human Report and continuity, the Claim Sheet, and the relevant reproducibility, review-cycle, and Live-Run README playbooks;
- verified the clean synchronized `main...origin/main` starting state; and
- required Claude's explicit same-state Session-17 approval before closing the bounded-redesign loop.

Claude's two forward notes were incorporated directly: the review records correct/false/withheld recovery authorization at the held decision and separately checks whether suite-informed action improves the representative outcome.

### 2. Built a role-separated noisy held-decision review

New `Reproducibility Packet/scripts/run_bounded_noisy_information_review.py` pins the exact approved bounded mechanics and causal schedule:

- selected plane `z=0.200 m`;
- W=768 and stride=16;
- fault/probe onset `1.000 s`;
- first held decision at step 1136 / `2.272 s`;
- movement begins at `2.400 s`; and
- the audit continues to `6.000 s`, five seconds after onset.

The seed roles are disjoint and explicit:

- calibration: 100 seeds, 14000-14099, for suite-specific healthy references, higher-method 95th-percentile leave-one-out detection thresholds, fault prototypes, and leave-one-out selective-margin thresholds;
- evaluation: 48 seeds, 14100-14147, for every held-out false-alarm, detection, attribution, abstention, and action-gate rate; and
- representative full-horizon continuation: predeclared held-out seed 14100, one row per source/suite, used only as a mechanics/safety/control sensitivity.

The minimum calibration size is computed from the declared 5% tail and five required tail observations; fewer than 100 calibration seeds fail loudly. The representative seed must belong to the held-out role.

### 3. Preserved exact matched causal histories

Each calibration/evaluation source-seed case is driven through the real noisy feedback path:

`CablePlant -> OnlineSensorSession(S) -> ObservedJointPDController`

The causal window at the scheduled decision is captured once. C1 is projected from that exact S window, so the two suites share plant state, nominal commands, sensor seed, and every common observed channel. Suite-specific references are then fit independently. This avoids a second controller trajectory becoming a hidden suite difference while preserving the intended gauge ablation.

All 592 physical calibration/evaluation pre-decision histories have zero contact and zero A1 safety flags. Exact array hashes also show matched C1/S pre-decision plant and shared-observation histories for every representative source pair.

### 4. Added selective prototype/reference lifecycle logic

The review fits each suite's healthy reference and standardization only on calibration data. Fault centroids use the separate labeled calibration role. Type abstention is selected by leave-one-out fault classification at a declared maximum 5% selective error, maximizing coverage among passing thresholds.

At the held decision:

- the healthy-reference score determines detected versus healthy;
- the nearest fault prototype supplies a mechanism type only after detection;
- prototype-distance margin determines explicit type abstention; and
- only confident structure/actuator calls authorize recovery.

Accepted prototype calls are emitted as one-hot mechanism probabilities solely to exercise the existing schema-D recovery seam. They are not calibrated class probabilities and cannot be promoted to learned-head evidence.

### 5. Measured held-out information and action gating

Across 48 held-out seeds for each canonical source, the suite-level result is:

| Suite | Macro-F1 | Balanced accuracy | Healthy FA | Min fault detect | Structure recall | Actuator recall | Sensor recall | Healthy false-actionable | Information | Action gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| C1 | 0.704 | 0.760 | 4.2% | 8.3% | 8.3% | 100% | 100% | 4.2% | BLOCK | BLOCK |
| S | 0.995 | 0.995 | 2.1% | 100% | 100% | 100% | 100% | 2.1% | PASS | PASS |

The false-actionable held-out healthy cases are:

- C1 seed 14137, called structure;
- C1 seed 14141, called structure; and
- S seed 14141, called structure.

Calibration leave-one-out selective coverage is 100% with 0% error for both suites, so the selected margin threshold is zero. Held-out known-fault selective accuracy is 100% and no known development fault abstains. This is kept as a limitation: the development faults separate cleanly, but compound/OOD faults, calibrated probabilities, and validation-frozen selective thresholds remain unresolved.

### 6. Kept action authorization separate from control benefit

The eight representative full-horizon online rows each evaluate the classifier once, hold that result, begin no source-specific action before the decision, produce exactly one contact episode, and produce zero A1 safety flags.

| Source | C1 held action | S held action | C1 `J_5s` | S `J_5s` | S change | A1 incidents |
|---|---|---|---:|---:|---:|---:|
| healthy | no action | no action | 0.8604 | 0.8604 | 0.0% | 0 / 0 |
| structure | withheld | correct structural action | 0.8589 | 1.0184 | -18.6% | 0 / 0 |
| actuator | correct actuator action | correct actuator action | 0.8667 | 0.8667 | 0.0% | 0 / 0 |
| sensor | no controller action | no controller action | 0.9937 | 0.9937 | 0.0% | 0 / 0 |

Only the structural pair tests an S-only action. The correct S authorization lowers peak contact force but worsens tracking and cannot claim a safety advantage because neither arm is unsafe. The representative control-sensitivity gate therefore blocks the current recovery profile even though the S information and held-out action gates pass.

### 7. Added tests and reproducibility artifacts

New `Reproducibility Packet/tests/test_bounded_noisy_information_review.py` adds four focused tests for:

- the resolved calibration tail, disjoint seed roles, and exact decision timing;
- calibration-only detection/selective thresholds;
- ambiguous-fault abstention and no recovery authorization; and
- strict separation of information, action, representative mechanics, and control-sensitivity gates.

New `Reproducibility Packet/results/bounded_noisy_information_review/` contains:

- `summary.json` — complete specification, roles, metrics, representative rows, gates, and decision;
- `information_rows.csv` — the two suite-level information/action rows;
- `heldout_decision_rows.csv` — all 384 held-out source/suite/seed decisions;
- `representative_online_rows.csv` — all eight full-horizon mechanism/safety rows; and
- `bounded_noisy_information_report.md` — the concise split decision and evidence boundary.

Final artifact SHA-256 values are:

- summary: `053b97237eae4f3c99b39af40643971415229488d20220a3df5e471b72c20d37`;
- information rows: `d3e62eb797131b6690c725b77d847da406c585e208a7c92d93a89767964ec90a`;
- held-out decisions: `71b044e6459e65ffc4ddef3eafa5aa460cb07166ecaf5825e7e7ee7a340709b8`;
- representative online rows: `25187670191540f5fd91930471aabe70048c795edefbe497aa309e36298a17ee`; and
- report: `7248d802aabc42880637378b58708fa7fbc2ae691b5baeda0067dd389a8277fd`.

### 8. Updated packet and public status surfaces

`Reproducibility Packet/README.md` now includes a copy-paste Step 12 command, output paths, the information/control split, and corrected downstream numbering through Step 16. Its current boundary distinguishes the S information advance from the blocked recovery profile and the still-unfrozen confirmatory state.

The root public `README.md` received one lean Live Run Status entry because the information/reference-lifecycle milestone is noteworthy. It reports the S-versus-C1 held-decision separation and the blocked representative control consequence without turning either into a confirmatory result.

## Challenges and how they were handled

### The complete role-resolved run is computationally expensive

The first four-worker command exceeded a 20-minute execution window before artifacts were written. No partial outputs were accepted. The worker default was raised to eight, and the recorded runs used 12 process workers. The final clean run completed in 704.5 seconds.

### A preliminary decision rule would have merged information and safety

The first completed full run reproduced the strong S information separation, but inspection showed the structurally correct S action worsened tracking. The decision logic was tightened so information/action authorization, representative A1 safety, and representative control sensitivity are separate gates. A fresh complete run with the final logic produced the recorded information-only advance and controller block.

### The known development faults did not exercise abstention

Leave-one-out fault prototypes separated without error, selecting a zero margin threshold and yielding no held-out known-fault abstentions. The artifact reports that fact directly and retains compound/OOD faults, calibrated probabilities, and validation-frozen selective thresholds as open work.

### A generated report contained a mojibaked dash

The seed-range dash in the report generator and generated Markdown was corrected to an ASCII hyphen. A repository scan confirmed no remaining matching mojibake in the new code, tests, artifacts, or README edits.

## Important decisions and reasoning

- **Advance information without advancing control.** Strong S attribution at the held decision is valuable, but it does not rescue a recovery action that worsens the measured representative outcome.
- **Use a resolved healthy tail.** One hundred calibration seeds are the minimum declared role for five observations in a 5% tail; the earlier eight-seed limitation is not repeated.
- **Keep calibration and evaluation disjoint.** No held-out seed tunes the detection threshold, prototype, or abstention margin.
- **Hold one exact causal decision.** This is the lifecycle approved after the continuous out-of-phase reference failure; it is evaluated before movement and used consistently through the contact audit.
- **Match the controller history across suites.** C1 projection from the same noisy S-driven history makes gauges the relevant information difference rather than allowing suite-specific feedback trajectories to confound the decision window.
- **Report false authorization, not classification alone.** Recovery depends on which decisions actually authorize structural or actuator actions.
- **Treat the one-seed continuation as sensitivity only.** It can block a harmful controller profile; it cannot establish an evaluation-sized recovery advantage.
- **Keep probability and configuration claims open.** One-hot prototype calls are schema instruments, not probability calibration. All development task/contact/controller and reference values remain unfrozen.

## Files created

- `Reproducibility Packet/scripts/run_bounded_noisy_information_review.py`
- `Reproducibility Packet/tests/test_bounded_noisy_information_review.py`
- `Reproducibility Packet/results/bounded_noisy_information_review/summary.json`
- `Reproducibility Packet/results/bounded_noisy_information_review/information_rows.csv`
- `Reproducibility Packet/results/bounded_noisy_information_review/heldout_decision_rows.csv`
- `Reproducibility Packet/results/bounded_noisy_information_review/representative_online_rows.csv`
- `Reproducibility Packet/results/bounded_noisy_information_review/bounded_noisy_information_report.md`
- `agents/Codex/Session Summaries/HumanReport18.md`

## Files updated

- `Reproducibility Packet/README.md` — added the noisy held-decision runbook, split result, evidence boundary, and downstream numbering.
- `README.md` — appended one lean development-only information/control split entry.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — accepted Claude's approval and appended the exact new handoff under the transcript hard gate.
- `agents/Codex/README.md` — updated the workspace map and active review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 19.

No `.gitignore` change is required: all new source, tests, compact text/CSV/JSON results, and documentation are intentional tracked project records. No environment, cache, secret, scratch rerun, or large binary belongs in the commit.

## Verification performed

- Focused new tests: **4 passed**.
- Full Reproducibility Packet: **159 passed**.
- `compileall -q scripts tests`: passed.
- New CLI `--help`: passed.
- Fresh complete final command with 12 workers: passed in 704.5 s and returned the recorded split decision.
- Strict-JSON audit: no `NaN` or `Infinity` tokens.
- Artifact consistency: 2 information rows, 384 held-out decision rows, 8 representative online rows, and 592 clean physical pre-decision histories; CSV/JSON/Markdown values agree.
- Generator/artifact audit: all five outputs reproduce byte-for-byte from the recorded strict JSON and final writers.
- Matched representative histories: exact C1/S pre-decision plant and shared-observation hashes agree for all four sources.
- Transcript hard gate: pre-write 1,227 lines; the new header occurs exactly once after the old tail at line 1,229; Codex is physically last at line 1,261.
- Root Live-Run README heartbeat: updated with one lean development-only split decision.
- Final staged diff hygiene and repository synchronization are completed at closeout.

## Next steps / pending actions

1. **Claude first-reviews the exact Session-18 state.** The open loop covers the new script, four tests, five result artifacts, packet/public wording, and evidence boundary. If Claude edits, Codex must genuinely owner-re-review the actual files before approval.
2. **After approval, redesign the structural recovery action/control sensitivity.** Preserve the bounded mechanics condition and real held-decision information path, but require the suite-informed action to improve a declared tracking or safety outcome before it can advance.
3. **Do not enlarge the information claim.** The S result is a development held-decision reference/prototype result, not calibrated learned attribution, an OOD result, or a confirmatory C1-vs-S comparison.
4. **Complete validation-sized calibration.** Healthy/four-class probability calibration, compound/OOD faults, class/abstention/selective thresholds, persistence, severity/onset grids, and uncertainty reporting remain open.
5. **Complete remaining pre-freeze audits.** Non-load-bearing sensor constants, final analysis window, whole-trajectory/fault-setting split, deployable-loader leakage, role hashes, multi-run storage, and immutable config/schema gates remain unresolved.
6. **Keep learned attribution and RMA post-freeze.** The prototype instrument is not the learned head and cannot be promoted by wording or reuse.
7. **Keep `config.json` unfrozen.** The information/reference lifecycle may advance, but the recovery-control profile is blocked and all development values remain candidates.
8. **Next regular Codex progress report:** Session 24, unless a Claim Sheet amendment or phase transition triggers an additional report first.

The central research question remains open. This session shows that the structural suite can support a strong noisy held-decision information/action-authorization gate on one bounded development condition, while also demonstrating why that information must not be conflated with successful recovery control.
