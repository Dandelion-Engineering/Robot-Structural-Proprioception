# Human Report 21 — Codex

**Session date and time:** 2026-07-22 17:11 PDT (checked at the shell immediately before creating this report)
**Phase:** Phase 2 — Execution
**Session type:** Genuine owner re-review of Claude's deficit-screen edits, one interpretation correction, and review-cycle handback

---

## Summary

This session processed Claude's first review of the Session-20 per-class fault tracking-deficit screen. Claude reproduced the screen, found that its 12% no-action deficit gate did not actually preserve the declared 12% reduction target, corrected the conversion, moved the selected actuator condition from 0.50 to 0.25 remaining gain, expanded the generated interpretation section, and handed the edited state back for Codex owner re-review.

I genuinely re-opened the implementation, regression, derived artifacts, report, packet runbook, Claim Sheet control definition, and Claude's review evidence. Claude's units diagnosis is correct. The Claim Sheet control quantity is a reduction against the degraded arm,

`(J_degraded - J_recovered) / J_degraded`,

while the screen measures a deficit against healthy,

`(J_fault - J_healthy) / J_healthy`.

If an ideal action restores healthy tracking exactly, a deficit `D` becomes a reduction `D / (1 + D)`. A 12% reduction target therefore requires a 13.636% healthy-relative deficit, not 12%. The corrected gate is a conservative implementation of the screen's predeclared intent—10% Claim Sheet bar plus a two-point development margin in reduction units—and no observed result enters the conversion.

The corrected state now selects **0.25 remaining actuator gain**, with 23.16% mean / 23.03% minimum disjoint deficit. No structural severity advances; the overall decision remains:

`ADVANCE_ACTUATOR_DEFICIT_ONLY_BLOCK_STRUCTURAL_DEFICIT`

I did not approve Claude's handed-back prose unchanged. The generated scope section treated performance beyond exact restoration as automatically generic command authority. That inference is not guaranteed: better-than-healthy performance could be fault-specific overcompensation or generic nominal-controller under-authority, and a no-action deficit screen cannot distinguish them. I narrowed the wording in the generator, regenerated the report, and applied the same interpretation correction to packet Step 14. The later action screen must include a healthy false-authorization arm and report the source-specific margin separately.

I explicitly approved the resulting edited state and handed it back to Claude. Because I changed Claude's review wording, the loop remains open until Claude genuinely re-reviews and explicitly approves this exact state or edits it again. `config.json` remains explicitly unfrozen.

---

## Startup and context ingestion

I followed `AgentPrompt.md` in its required order:

1. Read all of `Project Details/Project Details.md`.
2. Read Codex's prior `Summary of Only Necessary Context.md`.
3. Read every concluded-chat `Summary.md` in Codex channels.
4. Read both active Codex-channel transcripts completely to physical EOF before replying.
5. Read Claude's latest continuity and `HumanReport21.md`.
6. Read the in-force `Claim Sheet.md` and `Playbooks/review-cycle.md`.
7. Inspected git status and HEAD before trusting continuity. The repo began clean on `main` at `2d7539c` (`Claude Session 21`), aligned with `origin/main`.

The active Phase-2 tail superseded Codex's prior continuity: Claude had edited the deficit screen rather than approving it same-state, so owner re-review was the first obligation.

---

## Owner re-review: what I accepted

### Units conversion

I independently checked the conversion and its round trip:

- required reduction: 12.0%;
- equivalent required deficit: 13.6363636%;
- converted back through `D / (1 + D)`: 12.0000000%.

The new `required_reduction_pct` / `required_deficit_pct` split correctly keeps the declared target in reduction units and applies the transformed threshold to the deficit summaries. The validation guard correctly rejects a bar-plus-margin at or above 100% reduction.

### Selection and raw-data boundary

The corrected gate changes only derived selection state:

- 0.50 remaining actuator gain: assessment mean/min deficit 13.20% / 13.12% — now BLOCK;
- 0.25 remaining actuator gain: assessment mean/min deficit 23.16% / 23.03% — PASS / selected;
- all structural settings remain BLOCK;
- overall decision string remains unchanged.

The raw per-arm artifacts remain byte-identical to Session 20:

- `tuning_rows.csv`: `bfe0eb660e76a47702462a1bafd2477b3633bd3f32a94d8abbf0e976350c92df`
- `assessment_rows.csv`: `7cfcc104487d45a56ca316332dfcc563b9bdaaec94a32cf1d09d5003e680c293`

Claude's regenerated derived artifacts are internally coherent:

- `summary.json`: `ed265cfb1ac0cf8fa37678024203de3dcf049af70f0c85cf6fde4decec6191bf`
- `candidate_summary.csv`: `a7e2998d0ac986b803a6c535aa72b612960aa255f33caa7d0df259dc191e1b97`

### Structural interpretation

Claude's added side-by-side result is appropriate and important. Across the same structural-severity sweep, mean peak strain rises monotonically from 19.2 µε healthy to 259.7 µε at 0.05 remaining EI, while tracking deficit falls to zero and then becomes −5.00%. The structural sensing channel becomes more informative as the control deficit moves in the opposite direction. That is a measured Slot-13 diagnostic-only shape, not a sensing failure.

---

## Interpretation correction I made

Claude's new generated section correctly calls no-action headroom a ceiling for exact restoration, but two sentences overreached:

- they said any real action necessarily recovers less than the entire deficit; and
- they classified any result above the exact-restoration ceiling as generic command authority.

An action can outperform the healthy arm. If it does, the excess could be caused by fault-specific overcompensation, generic nominal-controller under-authority, or a mixture. The no-action screen has no arm capable of attributing that excess.

I changed the generated report language to state the defensible boundary:

- exact restoration defines the restoration headroom;
- performance above it is not licensed or attributed by this screen;
- the later action review must compare the same action against a healthy false-authorization arm and report the source-specific margin separately.

The same correction appears in packet Step 14. The regenerated report is byte-identical to a fresh call of its own `write_report()` and has SHA-256:

`f8ee1dfda070f220153fca2d5ea55e696722ac2b5e699728659ebecc2b2eaa62`

This edit changes interpretation only. It does not alter the converted gate, selected condition, raw rows, derived summaries, or overall decision.

---

## Transcript append recurrence and repair

The Phase-2 transcript's append failure mode recurred during this session.

I first read and verified the physical EOF, recorded the 1,673-line pre-write boundary, and confirmed an eight-line EOF block was unique. However, the actual patch used only the final two lines of that block as context. Those two lines had an earlier match, so the 17:08 PDT owner-re-review turn landed at line 1,331 instead of the physical tail.

The post-write hard-gate assertions caught the failure immediately:

- the new header was not after the pre-write boundary;
- Claude remained physically last; and
- the transcript diff showed a pure insertion.

I preserved the misplaced turn and appended a dated correction from the complete verified EOF block. Post-repair assertions pass:

- correction pre-write boundary: 1,689 lines;
- correction header exactly once at line 1,693;
- Codex physically last at line 1,705; and
- transcript diff: **+32 lines / −0 lines**.

No prior content was deleted, moved, truncated, or rewritten. I also appended the recurrence and its cause to `chats/Claude-Codex-Human/Transcript Order Monitoring/`; that append passed its own hard gate at line 31 after a 27-line boundary, with Codex physically last at line 41. No director action is needed.

The operational lesson is now explicit: verifying a unique multi-line EOF block is insufficient unless the patch itself uses that complete verified block as context.

---

## Verification

- Focused deficit-screen tests: **16 passed**.
- Full Reproducibility Packet: **199 passed**.
- `compileall -q scripts tests`: passed.
- Gate round trip: 13.6363636% deficit converts to 12.0000000% reduction.
- Selected assessment exact-restoration ceiling: 18.81% mean / 18.72% minimum.
- Generated report: byte-identical to a fresh generator call.
- `git diff --check`: clean aside from expected line-ending conversion warnings.
- Both chat transcript changes are append-only by `git diff --numstat`.

No new dependency was installed. `requirements.txt`, the root `.gitignore`, and the packet `.gitignore` required no change.

---

## Files created or updated

### Created

- `agents/Codex/Session Summaries/HumanReport21.md` — this report.

### Updated during technical/review work

- `Reproducibility Packet/scripts/screen_fault_tracking_deficit.py` — narrowed the generated exact-restoration interpretation without changing the accepted conversion or decision logic.
- `Reproducibility Packet/results/fault_tracking_deficit_screen/fault_tracking_deficit_report.md` — regenerated from the edited generator.
- `Reproducibility Packet/README.md` — applied the same scope correction to Step 14.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — preserved the misplaced turn and appended the verified operative correction/handoff.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md` — transparently recorded the recurrence, successful repair, and sharpened rule.

### Closeout files

- `agents/Codex/README.md` — added Session 21 and updated the deficit-screen/review pointers.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 22.

### Deliberately not updated

- Root `README.md`. This session corrected an active review state but did not produce a new technical milestone, close a phase, or change the public decision. The Live-Run log remains lean and append-only.
- `agents/Codex/references.md`. No external source was read; the session was an internal reproduction and review.

---

## Decisions and next steps

1. **Accept the converted gate.** The current no-action screen uses a 12% reduction target and the equivalent 13.636% deficit gate. The mildest advancing actuator condition is 0.25 remaining gain.
2. **Keep the evidence boundary narrow.** This is no-action headroom only. It does not establish action efficacy, source specificity, deployable severity estimation, S-over-C1 control improvement, or a frozen setting.
3. **Review loop remains open.** Claude must genuinely re-review Codex's wording correction and explicitly approve the exact state or edit and hand it back. Silence and downstream use are not approval.
4. **Next technical gate:** achievable source-specific reduction, not deficit alone. Candidate review must include paired action-versus-no-action benefit, the same multiplier falsely authorized on healthy, compensation-cap sensitivity, an oracle-severity ceiling arm, a separate deployable-severity arm, and a real uncertainty interval on the source-specific margin.
5. **The full control claim remains structurally constrained.** On the current development library, S has exclusive information on the structural class, which has no tracking deficit to recover; actuator and sensor have control headroom, but C1 already detects them. An actuator action can be useful recovery engineering without creating the Claim Sheet's paired S-over-C1 control win.
6. **Do not freeze partial configuration.** The compensation cap, severity-estimation quality, validation roles, thresholds, fault/onset grids, non-load-bearing sensor constants, task/contact/controller profile, W/stride, learned attribution/RMA, storage/leakage/hash audits, and evaluation-sized comparison remain unresolved.

No progress report was due. The next regular Codex progress report is Session 24 unless a phase transition or approved Claim Sheet amendment occurs earlier.
