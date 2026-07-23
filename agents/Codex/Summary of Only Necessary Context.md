# Codex — Only Necessary Context

## Resume state

- Project: **Robot Structural Proprioception**
- Phase: **Phase 2 — Execution**
- Public state: **In Progress**
- Current Codex session: **25**
- Expected closeout commit: `Codex Session 25`
- Shared `config.json`: **unfrozen**
- Controlling scope: the jointly approved Claim Sheet. Randy withdrew the proposed task redesign before any amendment; a different task belongs to a separately scoped follow-on project.

At the next session, follow `AgentPrompt.md` from the top. Read the complete physical UTF-8 tails of every active transcript before relying on this continuity file.

## Immediate live gates

1. **Actuator action-mechanism owner review is open.** Codex handed the exact new script, regression, artifacts, and BLOCK interpretation to Claude at the physical tail of `Phase 2 Integration and Config Freeze - Active.md`. Do not treat silence, downstream use, or edits as approval. Require explicit same-state approval or review edits.
2. **`Better Suited Task` awaits Claude's acknowledgement.** Randy withdrew his redesign request. Codex acknowledged. The chat can conclude only after Claude also acknowledges; do not rename/conclude it early.
3. **Calibrated authorization remains open.** The action screen forces the same diagnosis on healthy to measure consequence; it does not estimate future false-authorization rates from suite-specific class probability, abstention, or uncertainty.
4. **Configuration remains unfrozen.** No Session-25 screen is validation-sized or confirmatory.

## Session-25 actuator action result

New executable:

- `Reproducibility Packet/scripts/screen_actuator_recovery_action.py`
- regression: `Reproducibility Packet/tests/test_actuator_recovery_action.py`
- artifacts: `Reproducibility Packet/results/actuator_recovery_action_screen/`

Design:

- selected physical condition: actuator location 1, 0.25 remaining gain, bounded z = 0.200 m task;
- tuning seeds: 18000–18002;
- assessment seeds: 17100–17103;
- 36 tuning arms + 64 assessment arms;
- cap/floor family: 2/0.25, 3/0.25, 4/0.25, 5/0.25, 5/0.20;
- tuning target: 12% fault reduction;
- assessment bars: 10% fault reduction and 10-pp source-specific margin;
- source-specific margin: fault-action benefit minus identical healthy false-authorization benefit;
- assessment includes oracle severity and exact recorded held-out C1/S severities from Step 15;
- deterministic 20,000-replicate paired seed bootstrap.

Decision:

`BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`

Selected cap-3/floor-0.25 disjoint result:

- fault reduction: 16.5764759355% mean, 16.4891729362% minimum;
- healthy false-authorization benefit: 8.3224227983% mean;
- source-specific margin: 8.2540531371 pp;
- four-seed development interval: [8.0926910414, 8.5316317311] pp;
- oracle, C1, and S are action-identical because all saturate at multiplier 3.0;
- lifecycle/safety: pass.

Higher-cap boundary:

- cap-4/5 reach about 19.711% tuning fault recovery and 9.723 pp mean margin;
- S cap-5 sensitivity reaches 10.179 pp in assessment;
- those profiles fail the A1 lifecycle gate;
- complete candidate audit: 19 A1-incident arms, zero saturation, zero multiplier mismatch;
- all reference arms remain A1-clean and exactly reproduce committed Step-15 no-action `J_5s` (`max delta = 0.0`).

Interpretation:

- Safe cap-3 recovers tracking but misses the source-specific magnitude bar.
- Raising the cap reaches more raw recovery only by crossing the safety boundary; it is not a free performance improvement.
- C1 versus S control is not established by the selected cap because they command identically.
- This is development action-mechanism evidence only.

## Audit lesson preserved in code

The first 100-arm run aborted artifact creation because candidate A1 incidents were included in a global integrity condition. That was wrong: candidate unsafety is a valid negative result.

The corrected audit:

- requires reference A1, saturation, and multiplier cleanliness as run integrity;
- records candidate A1/saturation/multiplier violations;
- feeds candidate violations into lifecycle advancement;
- writes the negative artifact when references and execution integrity remain sound.

`test_candidate_a1_incident_is_a_scientific_block_not_audit_corruption` protects this distinction.

## Prior loop state

### Actuator probability screen — closed

Claude explicitly approved the exact Session-24 reviewer-corrected state:

- six-point maximum sampled S-over-C1 difference: 5.0698636256 pp;
- six-point mean: 5.0162118584 pp;
- result is a sampled empirical envelope, not a continuous proof;
- separate gate-crossing authorization difference: 10.8508760759 pp maximum;
- class probability, abstention, uncertainty authorization, and continuous response remain open;
- common RMS is a development fixture, not frozen predictive uncertainty.

Do not reopen this loop without new evidence or an owner edit.

### Severity/action boundary — closed

The jointly approved cap-2 boundary result remains:

- paired C1/S action difference below the 10-point bar for the recorded linear heads;
- arbitrary read-outs outside the measured envelope, cap-4 behavior, class probability, abstention, uncertainty, and calibrated authorization were not closed by that screen.

The new action-family screen measures cap/floor and false-authorization consequences but does not close calibrated authorization rates.

### Fault headroom — closed as development direction

- 0.25 remaining actuator gain has sufficient no-action headroom under the corrected deficit/reduction conversion.
- Structural settings do not produce the required tracking deficit on the current bounded joint-space task.
- Structural sensing remains diagnostic-only on this task unless a new in-scope mechanism and evidence change that conclusion.

## Evidence boundaries that must remain separate

- Development screens are not pilot, validation, frozen, or confirmatory evidence.
- Detection, attribution, calibrated authorization, action-mechanism efficacy, and control outcome are separate gates.
- A forced false authorization measures consequence, not false-authorization rate.
- Positive raw recovery is not source-specific recovery.
- An interval excluding zero does not clear a predeclared magnitude bar.
- Unsafe high-cap recovery does not advance.
- C1/S severity differences are irrelevant when the selected cap makes their commands identical.
- Four physical seeds provide a sign-stability guard, not confirmatory uncertainty.
- The current joint-space task stays in force; the withdrawn Cartesian-task proposal is preserved only as public history.

## Verification at Session-25 closeout

- Focused new regressions: **27 passed**
- Full Reproducibility Packet: **329 passed**
- New-file `compileall`: passed
- Strict JSON parse: passed
- Required audit fields: all passed
- Official action screen: 100 arms, 8 workers
- `summary.json` SHA-256: `B9D50165F0712CCCF6F6CB63B25A37BFCFBEF07E95DE22F3D58EDC6A3D38433F`

## Key live files

- `Claim Sheet.md`
- `README.md`
- `Reproducibility Packet/scripts/screen_actuator_recovery_action.py`
- `Reproducibility Packet/tests/test_actuator_recovery_action.py`
- `Reproducibility Packet/results/actuator_recovery_action_screen/summary.json`
- `Reproducibility Packet/results/actuator_recovery_action_screen/actuator_recovery_action_report.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `chats/Claude-Codex-Human/Better Suited Task/Better Suited Task - Active.md`
- `agents/Codex/Session Summaries/HumanReport25.md`

## Closeout/process invariants

- Use only the project venv: `.\venv\Scripts\python.exe` from repo root or `..\venv\Scripts\python.exe` from `Reproducibility Packet`.
- Active transcript appends require the hard gate: physical UTF-8 EOF, recorded pre-line count, verified unique multi-line EOF anchor, `apply_patch`, then exact post-boundary header/signature assertions.
- Preserve append-only public and transcript history; add corrections instead of rewriting prior entries.
- Require explicit same-state approval for review closure.
- Run `git diff --cached --check` before committing.
- Do not freeze config or promote a development result without the required gates.
