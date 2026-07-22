# Human Report 16 — Codex

**Current Date and Time:** 2026-07-21 17:37 PDT

**Agent:** Codex · **Session:** 16 · **Project phase:** Phase 2 — Execution

---

## Summary

This session closed the optional-contact profile screen's review loop, built and ran the first matched contact-enabled C1/S development pilot, recorded a three-part BLOCK, and wrote the regular every-eighth-session director progress report.

Claude Session 16 independently reproduced Codex Session 15's open-loop contact grid and explicitly approved the exact handed-off state. Codex accepted that same-state approval in the active Phase-2 thread, so the prior loop is closed. Claude's two forward notes became hard requirements for the next increment: extend beyond the 2.274 s screening horizon to re-check release/re-contact, and keep the privileged plant's three-dimensional workspace flag as the safety gate rather than treating the grid's two-dimensional readout as its margin.

The new pilot applies the screened z = 0.100 m plane identically to matched C1/S common-random-number pairs. It evaluates noisy contact-conditioned coefficient references on disjoint calibration/held-out seeds, exercises the observation-side encoder fault through the real causal plant→sensor→estimator→controller path, and audits the contact profile over the Claim Sheet's full onset+5 s control horizon.

All three decision surfaces block:

1. **Scheduled contact-conditioned information gate:** S detects all three held-out faults and attributes their prototype shapes at 100%, but its held-out healthy false-alarm rate is **8.3%**, above the 5% development screen. C1 has 4.2% false alarms and only 20.8% structural-fault detection. The structural signal remains directionally useful, but the S operating point does not advance.
2. **Short causal prototype lifecycle gate:** every representative run preserves nominal commands before the first online decision, and the observation-side sensor fault genuinely reaches the policy. But the single-decision reference is unstable when reused continuously after the probe changes phase in the sliding window. By the final decision all eight C1/S arms call **actuator**, including healthy and sensor cases, producing inappropriate compensation.
3. **Onset+5 s contact/safety gate:** z = 0.100 m produces three contact episodes in healthy, structural, and actuator scenarios and crosses the unchanged joint-angle limit for 1,111–1,658 steps. The former z = 0.050 m control also contacts later; healthy and structural runs cross the angle limit there too.

The exact overall decision is `BLOCK_MATCHED_CONTACT_PILOT_AND_CONTACT_PROFILE_CONFIG_FREEZE`. The earlier 2.274 s profile screen remains correct within its stated horizon; it simply does not transfer to the longer pilot/evaluation contract. Nothing was frozen, no confirmatory data were generated, and the central research question remains open.

Codex explicitly approved the complete new artifact state and handed it to Claude for genuine first review. That new review loop is open.

## What was accomplished

### 1. Completed startup, cross-review, and the prior review closure

The full `AgentPrompt.md` workflow was followed:

- read all of `Project Details/Project Details.md`;
- read Codex continuity;
- ingested all Codex-participant chat summaries and the complete 1,036-line active Phase-2 transcript before replying;
- read Claude's latest `HumanReport16.md` and its independently reproduced contact-grid evidence;
- read the Reproducibility Packet, review-cycle, progress-report, and Live-Run README playbooks before acting; and
- used the stored append-only hard-gate procedure for both Session-16 chat appends.

Claude's first review found no defect in the z = 0.100 m profile screen. Codex acknowledged the exact approval and closed the loop. The first transcript append passed the hard gate: pre-write 1,036 lines; new header once at line 1,040, after the old tail; Codex physically last.

### 2. Preflighted the longer horizon before writing the pilot contract

The first read-only mechanics probe extended z = 0.100 m to 6.0 s. It immediately exposed three contact episodes and many angle-safety steps. A companion run showed that z = 0.050 m also contacts later and is therefore only a no-contact control within the original short horizon.

That changed the pilot design. Instead of letting a short-window pass imply evaluation readiness, the new artifact declares three independent layers:

- the exact scheduled coefficient decision;
- a short 2.6 s causal seam check that extends beyond probe release but remains before the open-loop angle failure; and
- a mandatory 6.0 s onset+5 s contact/safety audit that the short layer cannot override.

### 3. Built the portable matched contact pilot

New `Reproducibility Packet/scripts/run_matched_contact_pilot.py` is a self-contained packet command with `argparse`, project-relative outputs, fail-loud validation, deterministic seed roles, shared utilities, and explicit honesty boundaries.

The exact-window layer:

- uses z = 0.100 m, 50% task torque, the 0.05 N / 0.8 Hz one-cycle raised-cosine probe, W=768, stride=16, and the selected 17-point / 0.1 ms mechanics;
- ends its coefficient window at observation index **1135**, the newest row actually available to the online policy before decision step 1136;
- fits suite-specific references/prototypes on sensor seeds 9000–9031;
- evaluates disjoint held-out seeds 9032–9079;
- applies the same physical trace and CRN source to C1/S and removes the S-only role from C1; and
- preserves the maximum-based 99th-percentile pilot threshold rather than retuning on held-out false alarms.

The short causal layer uses a deliberately labeled pilot-only `PilotPrototypeEstimator`. It consumes only delivered `ObservedRecord` history. Its fixed canonical location/severity lookup is attached to the **predicted** class, not run truth; its one-hot probability is a mechanism instrument rather than a calibrated claim. It drives the already-approved `GainScheduledRecoveryController` through the production `EstimatorCommandPolicy` seam.

The extended layer runs z = 0.050 and z = 0.100 over 6.0 s across healthy, structural, and actuator scenarios, scoring contact and all seven A1 flags from privileged truth.

### 4. Added focused regressions

New `Reproducibility Packet/tests/test_matched_contact_pilot.py` adds five tests:

- the exact probe-end / online-decision / newest-owned-observation boundary;
- the requirement that the audit cover a full five seconds after onset;
- the no-action-before-first-decision gate and predicted actuator location/severity mapping;
- the current controller's nominal fail-safe behavior for a correctly predicted sensor class; and
- the rule that a short-horizon pass cannot override an extended-horizon block.

### 5. Generated and interpreted the recorded artifact

New `Reproducibility Packet/results/matched_contact_enabled_pilot/` contains:

- `summary.json` — full spec, seed roles, rows, and three-layer decisions;
- `contact_information_rows.csv` — held-out C1/S exact-window metrics;
- `online_seam_rows.csv` — eight representative causal source/suite cases;
- `extended_horizon_rows.csv` — both planes × three physical source scenarios over 6.0 s; and
- `matched_contact_pilot_report.md` — concise human-readable BLOCK and boundaries.

The selected-plane long-horizon rows are:

| Scenario | Contact episodes | Last contact | Peak force | Angle-safety steps |
|---|---:|---:|---:|---:|
| healthy | 3 | 4.146 s | 4.178 N | 1,111 |
| structure | 3 | 4.748 s | 4.462 N | 1,658 |
| actuator | 3 | 3.458 s | 3.211 N | 1,651 |

Peak contact force stays below the unchanged 5 N limit. The block is repeated contact plus the joint-angle flag, not a force-limit failure.

### 6. Updated packet and public status surfaces

`Reproducibility Packet/README.md` now has a copy-paste matched-contact pilot step, exact output paths, the three blockers, and renumbered downstream steps. The current-boundary section no longer says that no matched contact pilot has run; it records the BLOCK without calling it a research result.

The root public `README.md` heartbeat was updated because this is a genuinely noteworthy negative method event. The banner remains Phase 2 / In Progress; the running log now states the false-alarm, unstable-prototype, repeated-contact, and safety findings, with `config.json` explicitly unfrozen.

### 7. Wrote the regular Session-16 progress report

`agents/Codex/Progress Reports/Progress Report Session 16.md` gives the director an Accessible-Piece-level update from Session 8 through the current BLOCK: the gentler synchronous probe, noisy-reference signal and calibration limits, real contact/safety integration, the new matched pilot failure, what is working, what is not, and the next redesign.

A verified Stanford Research Systems lock-in application note was added as the director-facing teaching source for synchronous detection, and `agents/Codex/references.md` was updated with its summary, project use, link, and copy-ready citation.

## Challenges and how they were handled

### The short contact candidate failed when the horizon became honest

The z = 0.100 m profile looked safe and single-contact over 2.274 s, but the required 6.0 s view showed repeated contact and angle violations. Rather than treating the earlier result as wrong or weakening its safety thresholds, the new artifact preserves its short-horizon validity and records the longer-horizon non-transfer as the blocking result.

### The contact-conditioned signal changed with the exact online timing convention

An exploratory contact follow-up using the older post-probe indexing produced a favorable S false-alarm rate on one seed range. The implemented pilot instead pins the newest observation the real policy owns before decision step 1136 (index 1135) and uses a new prospective seed range. That exact causal convention produced 8.3% S false alarms. The implementation keeps the BLOCK; it does not select the friendlier exploratory convention.

### A scheduled prototype did not survive continuous reuse

At the single scheduled decision, the nearest-centroid shapes were correct. Sliding the same prototype across later stride decisions changed which parts of the probe occupied the window. The instrument drifted to actuator calls for every arm. The initial generated report described how a *correct* sensor call would leave the controller nominal, but inspection of the actual CSV showed that the sensor call did not remain correct and the command changed. The gate and report were corrected to state the real result: phase/reference lifecycle failure and inappropriate compensation.

### Reproducibility first appeared to fail on the Markdown report

A scratch default-command rerun matched the JSON and all three CSV hashes, but the report hash differed. Content comparison showed no line difference; three lines in the committed report had LF endings inside an otherwise CRLF file because of a later formatting patch. The report was mechanically normalized to the generator's CRLF form, after which all five artifact hashes matched byte-for-byte. The verified scratch directory was then removed.

## Important decisions and reasoning

- **Keep three gates separate.** Signal at one scheduled decision, causal command behavior, and five-second physical safety answer different questions. None can stand in for another.
- **Block on S false alarms even with perfect fault-shape attribution.** A detector that catches every fault but falsely trips healthy runs above the declared operating screen is not ready to advance.
- **Treat post-probe reference lifecycle as load-bearing.** A reference conditioned on one decision phase cannot be applied continuously without evidence. Future work must make one declared decision, condition on phase/time, or train a temporal model over the full trajectory.
- **Do not hide action errors behind the “pilot-only” label.** The one-hot prototype was allowed to drive the real controller specifically to reveal whether a plausible diagnosis error would create bad commands. It did, so the pilot blocks.
- **Do not retune A1 safety limits.** The long-horizon task/contact profile must change; the unchanged limit exposed the method failure it was meant to catch.
- **Keep the central claim open.** S retains a strong scheduled structural signal, but no safe frozen closed-loop comparison exists. This is not evidence of adaptive-control advantage.
- **Update the public heartbeat.** Unlike the prior candidate screen, the matched pilot changed the public method state by blocking the candidate and identifying concrete redesign needs.

## Files created

- `Reproducibility Packet/scripts/run_matched_contact_pilot.py`
- `Reproducibility Packet/tests/test_matched_contact_pilot.py`
- `Reproducibility Packet/results/matched_contact_enabled_pilot/summary.json`
- `Reproducibility Packet/results/matched_contact_enabled_pilot/contact_information_rows.csv`
- `Reproducibility Packet/results/matched_contact_enabled_pilot/online_seam_rows.csv`
- `Reproducibility Packet/results/matched_contact_enabled_pilot/extended_horizon_rows.csv`
- `Reproducibility Packet/results/matched_contact_enabled_pilot/matched_contact_pilot_report.md`
- `agents/Codex/Progress Reports/Progress Report Session 16.md`
- `agents/Codex/Session Summaries/HumanReport16.md`

## Files updated

- `Reproducibility Packet/README.md` — added the matched pilot runbook/results and updated the current boundary.
- `README.md` — appended the lean public matched-pilot BLOCK and updated the date.
- `agents/Codex/references.md` — added the verified Stanford Research Systems lock-in note.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the prior-loop acknowledgment and the exact new owner-approved pilot handoff under the transcript hard gate.
- `agents/Codex/README.md` — updated workspace map, reports, artifact/test status, and open review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 17.

No `.gitignore` change is required: the session added only source, tests, small text/CSV/JSON artifacts, and project documentation. No secret, environment, cache, scratch, or large binary is being tracked.

## Verification performed

- New focused matched-contact tests: **5 passed**.
- Full Reproducibility Packet: **148 passed**.
- `compileall -q scripts tests`: passed.
- New CLI `--help`: passed.
- Default packet-root matched-pilot command: passed and returned the exact BLOCK.
- JSON audit: no NaN/Infinity tokens; decision parsed exactly.
- Scratch default-command reproduction: all five output files matched byte-for-byte.
- Generated Markdown/CSV/JSON inspected; report and decisions agree with the rows.
- First chat append hard gate: pre-write 1,036 lines; header once at line 1,040; after old tail; Codex physically last.
- Handoff append hard gate: pre-write 1,048 lines; header once at line 1,052; after old tail; Codex physically last.
- Root Live-Run README heartbeat: updated with one lean, noteworthy BLOCK entry.
- `git diff --check`: clean apart from repository line-ending warnings.

## Next steps / pending actions

1. **Claude first-reviews the exact new state.** The open loop covers `run_matched_contact_pilot.py`, its tests, all five result artifacts, packet/public wording, and the explicit BLOCK. If Claude edits, Codex must genuinely owner-re-review the actual files before approving or returning them.
2. **Redesign the bounded task/contact/controller condition.** The static plane and current open-loop task are not safe for onset+5 s. A stabilized finite trajectory or explicitly scheduled contact profile must clear unchanged A1 limits across healthy and physical-fault scenarios.
3. **Fix the reference lifecycle before active recovery.** Choose and predeclare one of: a single scheduled diagnosis that is held; phase/time-conditioned references for later decisions; or a temporal model trained across the complete post-probe trajectory. Do not reuse the current single-decision prototype continuously.
4. **Add calibrated action gating.** Class probabilities, abstention/selective thresholds, persistence, and per-suite probability calibration must prevent a drifting pilot call from triggering false actuator compensation.
5. **Complete remaining pre-freeze roles and audits:** validation-sized healthy/four-class calibration, severity/onset grids, non-load-bearing sensor constants, class/selective/OOD thresholds, final analysis window, whole-trajectory/fault-setting split, deployable-loader leakage, role hashes, multi-run storage, and immutable config/schema gates.
6. **Keep learned attribution/RMA post-freeze.** The current prototype is not the trained head and must not become one by repeated use or stronger wording.
7. **Next regular Codex progress report:** Session 24, unless a Claim Sheet amendment or phase transition triggers an additional report first.

The central research question remains open. This session did not show that structural sensing improves control; it found that a promising short-window structural signal is not yet embedded in a safe, stable closed-loop experiment.
