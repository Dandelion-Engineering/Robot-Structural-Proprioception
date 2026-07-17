# Human Report 2 — Codex

**Date/time:** 2026-07-16 20:50 PDT
**Agent:** Codex · **Session:** 2 · **Project phase:** Phase 1 — Sharpening (Claim Sheet review remains open)

## Summary

This session completed Codex's required review of the Phase-1 `Claim Sheet.md`, directly improved the contract, explicitly approved the edited state, and handed it back to Claude for the owning-agent re-review required by the review-cycle playbook. The review also accepted Claude's proposed division of labor, with one sequencing clarification: the shared plant→signals→estimator schema must be agreed and versioned before either Phase-2 implementation lane writes code.

The Claim Sheet is **not yet jointly approved**. Codex has approved the current edited state; Claude must re-open the artifact, review both the feedback and the edits, then explicitly approve that same state or edit and return it. Accordingly, this session did not start Phase 2, create `director_requests.md`, or update the public live-run README's phase/status.

## What was accomplished

1. **Loaded the controlling workflow and live state.** Read `AgentPrompt.md`, all of `Project Details/Project Details.md`, Codex continuity, every Codex-including chat summary and active transcript, the Claim Sheet and review-cycle playbooks, both agents' Literature Foundations and source ledgers, and Claude's latest Human Report and continuity. The live repository correctly outranked Codex's stale Session-1 handoff: Phase 0 had closed, Phase 1 had opened, and Claude had handed off the Claim Sheet for review.

2. **Reviewed the full Claim Sheet against its required inputs.** Checked the orientation on-ramp, all fifteen slots, the matched C0/C1/S/O comparison, the success/failure/inconclusive shapes, the verification artifact, the two capacity/fidelity ladders, licensing, portability, and the project standards. The overall research seam and staged claim were sound, but four contract-level ambiguities and one formatting violation required correction.

3. **Made the sensor comparison executable rather than optional.** Replaced the unresolved C1 alternatives (`current/torque`, `IMU/endpoint`) with a fixed suite:
   - C0: joint encoders + commanded actuation.
   - C1: C0 + noisy motor current converted with the nominal factory motor constant to an estimated torque + one distal-link six-axis IMU.
   - S: C1 + four fixed local bending-strain/curvature stations, two per link.
   - O: privileged simulator state only.
   Direct delivered torque and external endpoint pose/vision are excluded online. The actuator-gain loss acts downstream of the current proxy, so the conventional suite is not handed the answer to the actuator-fault class.

4. **Corrected the MuJoCo/encoder-bias feasibility logic.** Current official MuJoCo documentation distinguishes generic 1-D flexes (primarily extensible line elements) from cable/rod bending mechanics and 3-D solid flexes. Slot 9 now requires the spike to test the actual native candidates instead of assuming any `flex` is a bending beam or a built-in strain sensor. Virtual gauges must come from simulator-integrated deformation coordinates and be checked against an independent beam/Cosserat calculation.

   The earlier gate also required an encoder bias to create a distinguishable gauge response. That is physically wrong under matched open-loop excitation: a corrupted measurement need not change the body. The corrected gate requires plant faults to produce repeatable gauge responses above the modeled noise floor, while encoder corruption is identified through a repeatable disagreement between the corrupted encoder and the independently evolved physical/gauge history.

5. **Separated calibration, abstention, and unknown detection.** Known-class abstentions now count as errors in the headline macro-F1/balanced-accuracy result. Probability calibration (Brier, NLL, ECE, reliability diagrams), selective prediction (risk/coverage, fixed working points, false abstention), and held-out-compound OOD detection (AUROC/AUPRC/false acceptance) are reported separately. This prevents a model from manufacturing a high headline score by rejecting difficult known cases.

6. **Locked the confirmatory analysis before the pilot.** Added disjoint development/pilot, validation, and confirmatory partitions grouped by whole trajectories and fault settings; a versioned freeze of gauge placement, model/hyperparameters, thresholds, analysis window, seeds, and scenarios before confirmatory generation; at least five independent training seeds; and paired 95% hierarchical-bootstrap intervals over whole scenario/trajectory units and seeds.

   Full success now requires all of the following under realistic confounds:
   - S-minus-C1 macro-F1 improvement ≥0.05 absolute, with the paired 95% interval excluding zero.
   - The lower 95% bound on every source-class recall difference remains above a −0.02 non-inferiority margin.
   - At least 10% reduction in the five-second post-change integral of absolute tracking error, with the paired 95% interval excluding zero and no safety regression.

   These are project design minima fixed before any pilot result. The pilot may determine sample size and expose method failure; it may not choose what result will be called success.

7. **Removed prohibited construction scaffolding.** Deleted the closing paragraph that described the sheet as a Phase-1 draft handed to Codex. The Claim Sheet playbook requires the contract itself to read as one clean current state; the review history belongs in the active transcript and git history.

8. **Recorded new source use.** Updated Codex's MuJoCo ledger entry with the current flex/cable distinction and added Traub et al. (NeurIPS 2024) for selective-classification evaluation. No dependency was installed and no simulator was run.

9. **Completed the file-based handoff.** Appended a timestamped reply to the active Claim Sheet transcript naming every material edit and its reason, explicitly approving the current edited state, and requesting Claude's genuine owner re-review. The same message approved Claude's proposed labor split, including Claude ownership of the RMA-style comparator and evaluation harness, while requiring the shared interface schema to precede implementation.

## Important decisions and reasoning

### 1. Choose a rich but not privileged conventional suite

The meaningful comparison is not structural sensing against encoders alone. C1 therefore carries a plausible fixed onboard suite: motor-current-derived nominal effort plus an IMU. It does **not** carry direct delivered torque, because that could reveal the actuator-gain fault by construction, and it does not carry external endpoint pose/vision, because Phase 0 deliberately kept external vision outside the embedded-sensing comparison. The oracle may still use privileged simulator state as a ceiling.

### 2. Treat sensor faults as cross-signal inconsistencies

A sensor fault is not a plant fault. Requiring the structure to deform differently when only the encoder is biased would force the simulation to manufacture a signature. The physically legitimate information is the relationship among command, inertial/structural evolution, and the corrupted measurement. This preserves the project's central analytical-redundancy thesis without embedding the label in the plant.

### 3. Fix practical effect sizes before seeing pilot data

Neither literature foundation supplies a directly transferable effect-size threshold for this new benchmark. Leaving the bars until after a pilot, however, would let the observed separation determine what counts as success. The review therefore chose explicit project-level minima (0.05 macro-F1, −0.02 per-class non-inferiority, 10% integrated-error improvement) now and made Claude's owner re-review of those judgments explicit in the handoff.

### 4. Keep the review cycle open

Codex's direct edits and approval are only one side of the required same-state approval. Claude created and initially approved the prior state, not Codex's edited state. Phase 1 therefore remains open until Claude re-reviews and explicitly approves or returns a new edit. Starting the spike now would front-run the contract and the shared schema.

## Challenges and how they were handled

- **Continuity drift:** Codex's Session-1 summary still said Phase 0 was open. The concluded Phase-0 chat, new active Phase-1 chat, Claude's Session-2 report, and current git history proved otherwise. The live tree was treated as authoritative.
- **Simulator terminology:** “native flex” had been used as though it guaranteed a bending beam and strain output. Current official documentation showed a more specific distinction among 1-D stretch, cable/rod bending, and 3-D solid elasticity. The contract now makes that uncertainty the bounded purpose of the spike.
- **Abstention metric coupling:** The draft grouped calibration and abstention together. The review separated probability quality, selective operating behavior, and unknown detection so each failure mode is visible.
- **Precision without false certainty:** The experiment still needs mechanics-only feasibility work to fix exact gauge locations and a pilot to size the test. The contract allows those tasks while freezing effect sizes before the pilot and freezing all learned-model/test choices before confirmatory generation.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport2.md`

Updated:

- `Claim Sheet.md`
- `agents/Codex/references.md`
- `chats/Claude-Codex/Claim Sheet Review and Division of Labor/Claim Sheet Review and Division of Labor - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

Reviewed without change:

- `README.md` — heartbeat checked; the Claim Sheet remains in cross-review, so no phase/artifact milestone warranted another public log entry.
- `.gitignore` — no new generated, secret, environment, or binary artifact requires an ignore rule.

## Verification performed

- Re-read `Claim Sheet.md` after editing and confirmed the orientation header and all fifteen slots remain present.
- Confirmed the contract-at-a-glance suite and success bar match Slots 1, 7, 9, and 11.
- Confirmed the unresolved `current/torque`, `IMU/endpoint`, post-pilot threshold, and in-file draft-status language are gone.
- Re-read the active transcript tail immediately after the append and confirmed Claude's existing message remained intact and Codex's reply landed at the true tail in chronological order.
- Ran `git diff --check`; only expected Windows LF→CRLF conversion warnings appeared, with no whitespace errors.
- No code, environment, dependency, or simulation was changed or executed; software tests are not applicable to this review-only session.

## Next steps

1. Claude must re-open `Claim Sheet.md`, genuinely review Codex's edits, and explicitly approve the same state or edit and return it in the active transcript.
2. Claude should explicitly accept or amend the schema-first sequencing clarification. The substantive diagnosis-vs-plant/control labor split is otherwise accepted.
3. Once the technical Claim Sheet converges, Claude writes the Accessible Claim Sheet and Study Guide Pass 1; Codex reviews each through the same explicit approval cycle.
4. At the Phase-1 gate, create `director_requests.md` and append the non-blocking Claim Sheet review request, then update the phase/live-run artifacts as required.
5. Before Phase-2 code, agree and version the shared plant→signals→estimator schema. Then Codex begins the MuJoCo cable/rod versus slender-3D-flex feasibility spike while Claude begins the sensor-realism/evaluation lane.
