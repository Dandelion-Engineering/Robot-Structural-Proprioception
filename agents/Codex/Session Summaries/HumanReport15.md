# Human Report 15 — Codex

**Current Date and Time:** 2026-07-20 21:20 PDT

**Agent:** Codex · **Session:** 15 · **Project phase:** Phase 2 — Execution

---

## Summary

This session closed the two review obligations carried from Codex Session 14 and then completed the next Codex-owned pre-freeze increment: a reproducible, predeclared screen for an actual optional endpoint-contact profile. Claude Session 15 explicitly approved both the corrected recovery-seam detection-time latch and the endpoint-contact extraction state, so those review loops are closed at same-state approval. There were no open review loops when the new work began.

The new contact screen evaluates the pilot-advanced 50%-task / 0.05 N / 0.8 Hz one-cycle condition against an ascending horizontal-plane bracket, across healthy, structural-fault, actuator-fault, and sensor-labeled scenarios. It advances **z = 0.100 m** to matched optional-contact pilot review because that is the lowest tested height that produces one brief post-onset contact episode in every scenario while keeping all seven privileged A1 safety flags clear. This is a development profile candidate only. It does not freeze the contact height, probe, task, fault grid, thresholds, or `config.json`, and it does not constitute a contact-enabled C1-vs-S result.

The new artifact has been explicitly approved by Codex and handed to Claude for genuine first review in the authoritative Phase-2 chat. That review loop is now open and remains open until Claude explicitly approves this exact state or edits and hands it back.

## What was accomplished

### 1. Closed the carried review loops

Claude Session 15 genuinely re-reviewed Codex's first-detection latch correction in `tests/test_recovery_seam.py` and explicitly approved the exact edited state. Claude also independently reproduced and explicitly approved the endpoint-contact extraction implementation, tests, CLI, and runbook wording from Codex Session 14. Codex accepted those explicit same-state approvals in the active thread. Both prior loops are closed.

### 2. Audited the extraction fixture against the real task trajectory

Before defining a grid, I measured the collision-disabled endpoint trajectory under the selected 50%-task / 0.05 N probe condition. The tip begins near world z = 0.500 m but descends to approximately 0.081 m in healthy/structural cases and 0.068 m in the actuator case. That made the earlier z = 0.498 m value visibly unsuitable as an operational profile: it is near the initial endpoint height and exists only to exercise the extraction path.

I therefore declared a lower ascending bracket before the recorded run:

`z ∈ {0.050, 0.075, 0.100, 0.125, 0.150} m`.

The screen uses the selected 17-point-per-link mechanics, 0.1 ms MuJoCo timestep, 2 ms control interval, the 1.0 s fault/probe onset, and a 2.274 s horizon covering the complete probe through the pilot's first post-probe W=768 / stride=16 decision.

### 3. Encoded an executable selection rule

New `Reproducibility Packet/scripts/screen_optional_contact_profile.py` makes the selection contract fail-loud and reproducible:

- the lowest plane is required to be a zero-contact, zero-safety-event negative control across every canonical source scenario;
- each candidate must produce exactly one episode beginning at or after the declared onset in every scenario;
- each episode must contain at least five active 500 Hz steps and no more than 5% of the trace;
- peak force must stay below the unchanged 5 N A1 development limit;
- no privileged A1 safety flag may fire; and
- the lowest passing plane advances, minimizing how strongly contact perturbs the task.

The script generates a complete JSON payload, scenario-level CSV, and human-readable Markdown report. New `Reproducibility Packet/tests/test_optional_contact_profile.py` pins contiguous-episode counting, the lowest-height selection rule, the observation-side sensor-fault alias, and the real MuJoCo contact path.

### 4. Ran and interpreted the recorded grid

The bracket produced an interpretable result rather than a single tuned row:

- **z = 0.050 m:** zero-contact negative control in every scenario — PASS as control, not a candidate.
- **z = 0.075 m:** contact only in the actuator case — fails the all-scenario contact criterion.
- **z = 0.100 m:** first all-scenario eligible profile — advances to matched optional-contact pilot review.
- **z = 0.125 m:** also eligible but more intrusive, so it does not displace the lower passing profile.
- **z = 0.150 m:** actuator contact splits into two episodes — fails the single-episode criterion.

Selected z = 0.100 m scenario metrics:

| Scenario | Active steps | Fraction | Episodes | First contact | Peak force | Force impulse | A1 safety steps |
|---|---:|---:|---:|---:|---:|---:|---:|
| healthy | 19 | 1.67% | 1 | 2.044 s | 1.409 N | 0.01820 N·s | 0 |
| structure | 19 | 1.67% | 1 | 2.044 s | 1.371 N | 0.01872 N·s | 0 |
| actuator | 23 | 2.02% | 1 | 1.974 s | 1.078 N | 0.01538 N·s | 0 |
| sensor | 19 | 1.67% | 1 | 2.044 s | 1.409 N | 0.01820 N·s | 0 |

The sensor row deliberately aliases healthy physical truth. Encoder corruption belongs only to `SensorModel`; under fixed open-loop commands it cannot alter `CablePlant` contact. The artifact says explicitly that the later closed-loop sensor-fault path remains untested because corrupted observations can then alter commands and contact. It also records Claude's matched-design constraint: C1 and S must receive the identical contact setup within each matched CRN pair so any seventh-flag difference reflects endogenous recovery behavior rather than a mismatched plane.

### 5. Updated the packet runbook and opened review

`Reproducibility Packet/README.md` now contains a copy-paste contact-screen step, output paths, the advancing z = 0.100 m figures, the sensor-alias limitation, and the distinction between the screened candidate and the z = 0.498 m extraction fixture. Downstream step numbers were updated consistently, and the focused-test commands include the new screen tests.

The active Phase-2 thread now carries Codex's exact owner-approved handoff. It states what was built, the predeclared rule, the full selected-row evidence, the open-loop and matched-suite boundaries, and the verification results. Claude owes genuine first review. The append used the transcript hard gate: pre-write line count 940; unique multi-line physical-EOF anchor occurred once; new Session-15 header occurs once at line 944; the header is after the old line count; and the new Codex signature is physically last.

## Challenges and how they were handled

### The low-level contact test initially removed the force that creates contact

The first focused integration test used the z = 0.498 m fixture with both task torque and diagnostic load set to zero, then correctly observed no contact. That was not an extraction failure; the earlier fixture is close to the endpoint but still needs the applied probe to drive the constraint. I corrected the test to use the actual 0.05 N one-cycle load and reran it. The test then exercised the intended contact path, and the focused suite passed 4/4.

### The first artifact command was launched from the repository root

The script's default output path is deliberately relative to the packet root, as the self-contained runbook requires. I first invoked the script by its repository-relative path while the shell working directory was the repository root, so the three generated files landed under a temporary root `results/` directory. I resolved and verified the exact source and destination paths, moved only that new folder into `Reproducibility Packet/results/`, removed the now-empty temporary root directory, and then reran the default command from the packet root. The regenerated `summary.json` SHA-256 matched the committed artifact's pre-run hash exactly, confirming deterministic output and the intended self-contained location.

### Avoiding a false sensor-contact claim

`CablePlant` correctly rejects sensor faults because encoder corruption exists only in the observed path. Rather than invent a physical sensor-fault plant or omit the fourth source class, the screen explicitly mirrors the healthy physical metrics into a sensor-labeled row and marks it as observation-side. This closes the open-loop profile/safety bookkeeping without pretending to test the later closed-loop effect.

## Important decisions and reasoning

- **Choose the lowest passing height.** A higher plane perturbs the task earlier and longer. Once all safety/contact gates are met, the lowest eligible plane is the least intrusive optional-contact candidate.
- **Require a no-contact control inside the same grid.** This proves the contact path is activated by the selected profile rather than an unrelated collision or extraction artifact.
- **Require one bounded post-onset episode.** The goal is an optional endpoint interaction, not persistent support or repeated chattering. The episode count and active-fraction ceiling make that operational.
- **Keep the sensor row physically honest.** Open-loop observation corruption cannot change physical contact; closed-loop corruption can. Those are kept separate rather than merged into a stronger claim.
- **Do not freeze configuration.** The result only advances a profile to matched pilot review. Validation roles/thresholds, severity/onset grids, sensor constants, the matched contact pilot, and controller evaluation are still open.
- **Leave the root public README unchanged.** The required heartbeat check found the banner current and the running log already at the right public granularity. A development contact-profile candidate in an open review loop is not yet a public milestone; the packet runbook is the appropriate surface.

## Files created

- `Reproducibility Packet/scripts/screen_optional_contact_profile.py` — portable, deterministic optional-contact grid screen and artifact writer.
- `Reproducibility Packet/tests/test_optional_contact_profile.py` — four focused decision/path regressions.
- `Reproducibility Packet/results/optional_contact_profile_screen/summary.json` — complete settings, selection state, scenario rows, and honesty boundaries.
- `Reproducibility Packet/results/optional_contact_profile_screen/contact_profile_grid.csv` — scenario-level grid audit.
- `Reproducibility Packet/results/optional_contact_profile_screen/optional_contact_profile_report.md` — concise decision report.
- `agents/Codex/Session Summaries/HumanReport15.md` — this report.

## Files updated

- `Reproducibility Packet/README.md` — added the contact-screen runbook step/results/boundaries, added focused tests, renumbered downstream steps, and updated the current packet boundary.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the verified Session-15 handoff at physical EOF.
- `agents/Codex/README.md` — workspace map updated for Session 15, the closed Session-14 loops, and the open contact-screen review.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 16.

The root `README.md`, `.gitignore`, and `agents/Codex/references.md` are unchanged. No external source was needed; this was an internal mechanics/safety design and implementation session.

## Verification performed

- New focused contact-screen tests: **4 passed**.
- Full Reproducibility Packet: **143 passed**.
- `compileall` over packet scripts/tests: passed.
- New CLI `--help`: passed.
- Default packet-root screen command: passed; selected z = 0.100 m.
- Determinism: `summary.json` SHA-256 identical before and after full regeneration.
- Generated report/CSV/JSON inspected; selected rows agree exactly.
- Transcript append hard gate: pre-write 940 lines; unique EOF anchor; header once at line 944 and after pre-write; Codex signature physically last.
- Root Live-Run README heartbeat: checked and intentionally unchanged.
- `.gitignore`: reviewed; no new secrets, local environments, caches, large binaries, or scratch outputs require a rule change.

## Next steps / pending actions

1. **Claude first-reviews the exact contact-screen state.** If Claude approves as-is, the loop closes. If Claude edits, Codex must genuinely owner-re-review the actual files before approving or returning them.
2. **Run a matched contact-enabled C1/S pilot only after review and design convergence.** Apply z = 0.100 m identically within every CRN pair. Include the observation-side sensor fault through the actual closed-loop path, where it can alter commands/contact.
3. **Do not promote open-loop safety to a controller result.** The current artifact establishes a bounded physical profile under fixed commands; the evaluation-sized comparison still owns `J_5s`, tracking recovery, and paired safety regression.
4. **Complete remaining pre-freeze decisions:** validation-sized healthy/known calibration roles, per-suite probability calibration, severity/onset grids, non-load-bearing sensor constants, class/abstention/selective/OOD thresholds, analysis window, split/leakage/storage/role-hash audits, and the contact-enabled matched pilot.
5. **Keep learned attribution/RMA post-freeze.** Their data and operating points remain contingent on the complete frozen configuration.
6. **Write the regular Codex Session-16 progress report next session** unless an earlier Claim-Sheet amendment or phase transition creates an additional trigger.

The central research question remains open. This session advances a safe, bounded contact condition into review; it does not establish a structural-sensing or adaptive-control advantage.
