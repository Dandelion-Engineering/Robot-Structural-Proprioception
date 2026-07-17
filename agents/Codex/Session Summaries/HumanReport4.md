# Human Report 4 — Codex

**Date/time:** 2026-07-16 22:35 PDT

**Agent:** Codex · **Session:** 4 · **Project phase:** Phase 1 — Sharpening (schema edited review state awaiting Claude same-state approval)

## Summary

This was the final-review turn on the shared Phase-2 data contract. Claude's Session 4 closed both remaining companion-artifact loops by genuinely re-reviewing and explicitly approving Codex's edited Accessible Claim Sheet and Study Guide Pass 1 states. Claude also accepted schema v0.2, resolved its one open tracking decision, added four clarifications, and wrote the result as `Reproducibility Packet/schema/schema-v1.0.md` for Codex's same-state review.

Codex accepted the proposed tracking metric and all four Claude additions, but found implementation ambiguities that could still have invalidated the intended comparison. The schema was edited directly to make the online closed-loop execution order explicit, realize the privileged/label boundary in the persisted file layout, prevent target leakage through identity metadata, make whole-group splitting and common-random-number behavior executable rather than aspirational, and distinguish requested, saturated, and delivered actuator effort. Codex explicitly approves this edited state and handed it back to Claude for genuine owner re-review.

Phase 1 remains open. The technical Claim Sheet, Accessible Claim Sheet, and Study Guide Pass 1 are jointly approved; only the schema loop remains. No implementation code or dependency was introduced, and the director request, Phase-2 README flip, and phase-transition progress report remain correctly unfired until Claude approves this exact schema state or returns another edit.

## What was accomplished

1. **Reconstructed the authoritative live state.** Read `AgentPrompt.md`; all of `Project Details/`; Codex's continuity; the concluded Phase-0 summary; the full active Claim Sheet/schema thread; Claude's latest `HumanReport4.md`; the review-cycle and Reproducibility Packet playbooks; the current schema; the binding Claim Sheet sections; and the live-run README/playbook. The true chat tail established that Claude had closed both companion loops and handed schema v1.0 to Codex.

2. **Closed Codex's cross-review obligation on Claude Session 4.** Claude's report and the exact artifacts it named were reviewed. The report's claims about companion approvals, the deformed-tip decision, the four schema additions, and the still-open phase gate matched the live transcript and current files.

3. **Accepted Claude's tracking decision and four v1.0 additions.** The proposed headline control metric is now accepted by Codex: distal-endpoint planar position error in metres, using the L2 norm on the control grid and trapezoidal integration over `[t_c, t_c + 5 s]`. The endpoint is the true deformed tip, not rigid forward kinematics from joint angles. Codex also accepted:
   - common random numbers within each C1/S pair;
   - fixed estimator/controller architecture-and-protocol identities across the compared suites;
   - true-deformed-tip task output and task-space reference; and
   - NaN/mask/availability handling plus an automated leakage test.

4. **Corrected the runtime dataflow.** The handoff described the plant lane as emitting a plant record that the sensor lane then consumed. That wording was safe for storage but ambiguous for execution: in a closed-loop rollout, observations affect the controller, the controller affects the next plant state, and C1/S may diverge. The edited schema now requires the plant, sensor model, estimator, and controller to interleave at every control step. Privileged/observed/label/output records are persisted traces of that online loop, not an offline pipeline where a complete plant trajectory exists first.

5. **Made storage separation real.** The prior contract combined “one NPZ per rollout” with a single manifest path/hash even though plant truth, observations, labels, estimator outputs, and controller logs were supposed to be physically separate. The edited state now defines:
   - a path-free identity/split manifest;
   - separate roots and indexes for plant, per-suite observations, labels, per-suite estimator outputs, and per-suite controller logs; and
   - one non-pickled numeric NPZ per rollout per applicable role, each with its own hash.

   A deployable loader receives only its suite's observation index/root. It cannot resolve privileged, label, oracle, or other-suite payloads.

6. **Closed an identity-metadata target leak.** `fault_setting_id`, scenario provenance, and related fields can reveal the supervised target even if the label arrays themselves are separate. The identity manifest is therefore explicitly non-deployable. Inference loaders cannot receive it; supervised training joins labels in a separate allowlisted builder and passes them only as targets, never feature columns. Identifiers are opaque and non-semantic.

7. **Made split integrity executable.** Before fitting any model, the schema now requires an audit proving that each `pair_id`, `trajectory_spec_id`, and `fault_setting_id` maps to exactly one split and that no `run_id` is divided by time. This matches the Claim Sheet's requirement to separate partitions by whole trajectories and whole fault settings; grouping only a trajectory/fault Cartesian combination would not have been sufficient.

8. **Made common random numbers robust to the extra S channels.** Reusing one sequential sensor RNG seed is not enough: drawing gauge noise only for S can advance the RNG and change later encoder/current/IMU draws, defeating the matched comparison. Shared-channel innovations must now come from deterministic channel/time substreams (or an equivalent counter-based construction). State-dependent sensor values may still differ after legitimate closed-loop divergence; the matched quantity is the exogenous innovation, not a forced-identical observation.

9. **Disambiguated actuator and timing fields.** The schema now distinguishes:
   - `tau_cmd`: the controller's requested pre-limit torque;
   - `control_effort`: the saturated actuator-side effort upstream of the gain fault and current proxy; and
   - `tau_delivered_true`: post-fault physical torque.

   Temperature truth is fixed to the four gauge stations. Validity, measurement time, availability time, and latency age are explicitly per time and per channel, which is necessary when channels have different delays or dropout.

10. **Recorded the review-cycle handoff.** A timestamped Session-4 response was added to the authoritative active transcript, naming every edit, accepting Claude's decisions, explicitly approving the current edited schema state, and handing it back for genuine owner re-review. A patch anchor placed that new turn after Claude's Session-2 sign-off instead of at the live tail; because the transcript is append-only, the misplaced new content was not deleted. A timestamped tail correction identifies it as the latest substantive turn and preserves all prior content.

11. **Made the live-run heartbeat decision.** The root README was reviewed under its playbook and left unchanged. Its latest entry already says the schema is proposed v1.0 and in final review. This session advanced that review but did not finish the artifact or close the phase, so another public log entry would have turned the lean heartbeat into a session journal.

## Important decisions and reasoning

### 1. Deformed-tip error is the right headline control quantity

A compliant arm can keep its joint angles near the nominal target while link bending moves the real endpoint. Joint-space error or rigid-model forward kinematics would therefore hide the failure this project is designed to test. The accepted metric measures the true deformed tip in task space and preserves the Claim Sheet's five-second control bar.

### 2. “Separated” must describe storage and loader authority, not just prose

A label/privilege boundary is not real if all roles share one payload or if the deployable loader receives a manifest that names target-revealing fields. The role-specific roots/indexes and explicit loader inputs convert the boundary into something the automated leakage test can actually check.

### 3. Common seeds do not guarantee common random numbers

The S suite has extra random draws for its gauges. Without named substreams, those draws can shift every later shared-channel draw. The schema now binds the stronger invariant the statistical comparison needs: matched shared-channel innovations that remain matched even when S has additional channels.

### 4. Preserve the agreed Claim Sheet and propagate the Wensing scope forward

Claude correctly noted that the derived artifacts now scope the Wensing theorem more precisely than two broad narrative lines in the agreed technical sheet. Those lines remain defensible because rigid-body inertial redistributions are structural changes. Reopening the concluded contract would add process without changing a commitment; the precise rigid-body-inertial scope will instead carry forward into the Technical Report.

## Challenges and how they were handled

- **A structurally strong schema still hid implementable leakage paths.** The review traced what exact files and metadata an inference loader would receive, rather than accepting “stored separately” at face value. That exposed both the single-path storage ambiguity and the target-bearing identity-manifest issue.
- **Closed-loop causality conflicted with an offline reading of the lane handoff.** The persisted records and runtime loop were separated conceptually: runtime interleaves each step; storage writes role-separated traces. This keeps the labor split while preventing an impossible “plant first, sensing later” implementation.
- **The transcript append landed at the wrong sign-off.** A generic patch anchor matched the first Claude closing line. No old content was altered, but the new Codex turn was not chronological. The append-only rule prohibited silently deleting or moving it, so a clear timestamped correction was appended at the actual tail and the issue is documented here for continuity.
- **The split rule needed a testable interpretation.** The edited contract adopts the stricter literal Claim Sheet reading: whole trajectory IDs and whole fault-setting IDs do not cross splits, and the suite never determines the split.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport4.md` — this detailed session record.

Updated:

- `Reproducibility Packet/schema/schema-v1.0.md` — edited review state, Codex-approved and awaiting Claude same-state approval.
- `chats/Claude-Codex/Claim Sheet Review and Division of Labor/Claim Sheet Review and Division of Labor - Active.md` — Codex's schema review/handoff plus appended transcript-order correction.
- `agents/Codex/README.md` — workspace map updated for Session 4 and the current shared-artifact states.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 5.

Reviewed without change:

- `Claim Sheet.md` — binding contract used for schema review; the Wensing narrative is left concluded and its sharper scope propagates forward.
- `Accessible Claim Sheet.md` and `Study Guide/Pass 1 - Conceptual Foundation.tex` / `.pdf` — Claude's same-state approvals closed both review loops.
- `README.md` — no new qualifying public heartbeat event beyond the existing “schema in final review” entry.
- `agents/Codex/references.md` — no new external source was ingested; this was a contract and implementation-consistency review.
- `.gitignore` — no new dependency, secret, local environment, generated build output, or binary artifact required another ignore rule.

## Verification performed

- Re-read the complete edited schema after all patches rather than relying on the diff alone.
- Compared the schema to the Claim Sheet's sensor suites, fault boundaries, split/statistical contract, five-second control bar, leakage failure shape, and Reproducibility Packet requirements.
- Verified the active transcript's true tail and appended a transparent order correction after the patch-anchor mismatch.
- Ran `git diff --check`; only Windows line-ending conversion notices appeared, with no whitespace errors.
- Confirmed the worktree was clean before this session and that no unrelated user changes were overwritten.
- No project Python command, simulation, model training, dependency installation, or external-source fetch was needed or permitted before schema convergence.

## Next steps

1. Claude must genuinely re-review the current edited `Reproducibility Packet/schema/schema-v1.0.md` state and either explicitly approve it unchanged or edit and return it.
2. If Claude approves this exact state, the schema loop and Phase 1 close. That session must fire the transition exactly once: create/append the non-blocking Claim Sheet director-review request, flip the live-run README to Phase 2, and write the phase-transition progress report.
3. Only after same-state schema approval may either lane import dependencies or write implementation code.
4. Phase 2 then starts with Codex's bounded MuJoCo cable/rod-versus-slender-3D-flex feasibility spike and Claude's sensor/fault/evaluation work against the same schema.
5. Preserve the active transcript as append-only; the Session-4 tail correction explains the one misplaced Codex turn and should not be “cleaned up” by deleting history.
