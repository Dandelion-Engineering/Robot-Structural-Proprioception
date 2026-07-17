# Human Report 3 — Codex

**Date/time:** 2026-07-16 21:49 PDT

**Agent:** Codex · **Session:** 3 · **Project phase:** Phase 1 — Sharpening (companion-artifact and schema review open)

## Summary

This session completed Codex's required review of the Accessible Claim Sheet and Study Guide Pass 1, repaired material scope and contract-fidelity defects in both, regenerated and visually verified the Study Guide PDF, and explicitly approved the two edited artifact states. The active Claude–Codex thread now hands those states back to Claude for genuine owner re-review.

The session also converted Claude's shared-schema v0.1 sketch into a plant-side v0.2 contract that distinguishes matched specifications from diverging closed-loop rollouts, locks split/pairing semantics, prevents privilege leakage, fixes the four structural channels as signed surface strain, makes causality/latency explicit, and chooses dependency-light storage. Codex explicitly approved v0.2 and handed it to Claude; the exact task-space tracking vector is the one named decision Claude must approve or counter.

Phase 1 remains open. The technical Claim Sheet is jointly approved, but the two companion artifacts still need Claude's same-state approval and the shared schema must be approved and written as v1.0 before either implementation lane starts. No director request, phase flip, progress report, implementation code, or dependency was introduced prematurely.

## What was accomplished

1. **Reconstructed the current live state.** Read the controlling `AgentPrompt.md`, all Project Details, Codex continuity, both Codex-including chat records, Claude's latest Human Report, the current technical/accessible/study-guide artifacts, the relevant artifact and review-cycle playbooks, both Phase-0 foundations, and both source ledgers. Claude's Session-3 message proved that the technical Claim Sheet review loop had closed on Codex's Session-2 state and that both companion artifacts plus schema v0.1 were ready for review.

2. **Confirmed the technical Claim Sheet is now closed.** Claude genuinely re-reviewed Codex's changes and explicitly approved the same state. The labor split and schema-first sequencing are also agreed. The technical sheet was therefore used as the binding contract for reviewing the two translations.

3. **Repaired the Accessible Claim Sheet's source boundaries.** The original translation used Wensing et al.'s rigid-body inertial observability theorem as if it proved this project's stiffness, actuator, and encoder faults could be invisible to C1. The edited text limits the theorem to rigid-body inertial parameters and makes separability of this project's fault library an empirical spike/ablation question. It also labels Sravani & Venkata accurately as a process-control example rather than a robotics proof.

4. **Restored metrics omitted during plain-language translation.** The accessible artifact now preserves the technical sheet's balanced accuracy; per-cause precision and recall; detection delay; calibration scores and reliability diagrams; fixed selective-risk working points; false-abstention metric; OOD metrics; control effort/saturation measures; and the exact lower-95%-bound > −0.02 per-cause recall guard. It also states the actual paired hierarchical resampling order rather than implying that SciPy supplies it automatically.

5. **Restored physics and reproducibility commitments.** The accessible artifact now links directly to first-party MuJoCo elasticity documentation and distinguishes generic line flex from the bending/twisting cable candidate. It again names approximate gauge resolution and thermal cross-sensitivity bounds, Windows/hardware/environment constraints, mandatory CLI/config inputs, licenses, and 300-dpi publication output.

6. **Corrected the Study Guide without changing its teaching role.** The revised guide:
   - acknowledges robust/adaptive control instead of saying robots trust fixed models completely;
   - narrows the Wensing connection to an observation-map lesson;
   - presents analytical redundancy as an illustrative connection, not imported proof;
   - preserves the MuJoCo spike and independent-validation requirement, including the rule that a fallback PyElastica plant cannot validate itself;
   - prevents known-class abstention from becoming a scoring loophole;
   - preserves the single tracking-error equation while making the still-unfrozen tracking space/units/norm/integration rule explicit;
   - replaces inaccurate “pre-registration” language with pre-specification plus a versioned configuration freeze; and
   - restores the exact full-success statistics.

7. **Rebuilt and visually verified the PDF.** Compiled the `.tex` repeatedly with MiKTeX `pdflatex` until the table of contents and body stabilized. The first revision produced a 14-page file with one TOC entry orphaned on an otherwise blank page. Compact TOC typography removed that defect. The final PDF is 13 letter-size pages, has no LaTeX overfull/underfull or package warnings, and every final page was visually inspected. MiKTeX emitted only its installation update-reminder message.

8. **Proposed and approved schema v0.2.** The active thread now specifies:
   - separate `scenario_spec_id`, `pair_id`, and `run_id` semantics so a matched C1/S pair may diverge after adaptation without losing its statistical pairing;
   - rollout-level manifests, grouped split keys, separate seeds, immutable config hashes, and no suite-based split decisions;
   - fixed-grid privileged plant arrays with declared shapes and units;
   - exactly four deployable signed surface-strain channels, separate privileged curvature, static suite masks, dynamic validity masks, latency/age, and causal derivative handling;
   - fault-injection boundaries that keep sensor faults in observations and the current proxy upstream of actuator loss;
   - separated labels, estimator outputs, and controller logs plus an automated privilege-leakage test;
   - past-only windows and measurement/availability timestamps;
   - a separately allowlisted oracle interface; and
   - dependency-light `manifest.csv` + numeric non-pickled `.npz` + immutable JSON + SHA-256 storage.

   Codex recommends distal-endpoint planar position error in metres, L2 norm, control-grid sampling, and trapezoidal integration over `[onset, onset + 5 s]`. Claude must explicitly approve or counter that choice before the schema is versioned as v1.0.

9. **Recorded the review and handoff.** Appended a timestamped Session-3 response to the authoritative active transcript, explicitly approved both edited companion-artifact states and schema v0.2, identified what changed and why, and left the phase-close triggers unfired. Re-read the tail immediately after writing to confirm the transcript remained append-only and chronological.

## Important decisions and reasoning

### 1. Source connections must be scoped, not merely cited

A credible paper can still be used incorrectly. Wensing et al. supplies a rigorous example of an observation map with a nullspace; it does not transfer a proof of non-identifiability to a different parameter/fault family. The director-facing artifacts now teach the general lesson while naming the boundary clearly.

### 2. Plain language must preserve testable commitments

The Accessible Claim Sheet is not a summary. Removing metrics or turning a precise confidence-bound guard into “no class gets worse” changes the project contract. The review restored the complete evaluation and reproducibility surface while keeping the explanations readable.

### 3. Pair specifications, not necessarily closed-loop state histories

Once C1 and S drive different adaptation or recovery decisions, their trajectories can legitimately diverge. The statistical pair is the matched exogenous scenario/fault specification. Distinguishing `pair_id` from `run_id` prevents the implementation from either losing the pairing or falsely requiring identical time-series states.

### 4. Keep privileged truth structurally unavailable

A single all-fields record with a mask is too easy to misuse. Deployable loaders must be unable to import privileged arrays or labels, and O must be a separate allowlisted interface. This turns “no leakage” from a convention into something testable.

### 5. Avoid unnecessary interface dependencies

CSV, numeric NPZ, and JSON meet the foreseeable schema need and are readable with the standard library plus the already-permitted numerical stack. Parquet/YAML can be introduced later only if a measured need justifies the added dependency and portability cost.

## Challenges and how they were handled

- **A good draft hid non-equivalent compression.** The companion artifacts were coherent and polished, so the review compared every important bound back to the technical sheet rather than treating readability as fidelity.
- **The PDF passed compilation but not layout review.** LaTeX reported no box warnings, yet visual inspection found a nearly blank TOC overflow page. The TOC was compacted and the PDF rebuilt and re-rendered until both machine and visual checks passed.
- **Generic bootstrap documentation could be overread.** SciPy documents a bootstrap primitive, not this project's nested paired procedure. Both artifacts now say exactly which levels are resampled and what pairing is preserved.
- **Tracking error remained underspecified.** The guide correctly exposes the integral but could not choose the metric's vector implicitly. Schema v0.2 names a concrete recommendation and makes Claude's explicit review the remaining gate.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport3.md`

Updated:

- `Accessible Claim Sheet.md`
- `Study Guide/Pass 1 - Conceptual Foundation.tex`
- `Study Guide/Pass 1 - Conceptual Foundation.pdf`
- `agents/Codex/references.md`
- `chats/Claude-Codex/Claim Sheet Review and Division of Labor/Claim Sheet Review and Division of Labor - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

Reviewed without change:

- `README.md` — no phase close or fully approved companion artifact occurred, so another public heartbeat entry would be noise.
- `.gitignore` — generated LaTeX and temporary PDF-review outputs are already covered or removed; no new secret, environment, or dependency artifact needs a rule.

## Verification performed

- Verified the key external claims against the Wensing paper record, official MuJoCo elasticity documentation, SciPy bootstrap documentation, official FDA non-inferiority guidance, and the FBG temperature/strain source already in the project ledger.
- Rebuilt the Study Guide with MiKTeX `pdflatex`; final result: 13 pages, letter size, no LaTeX layout/package warnings.
- Rendered the PDF to PNG with Poppler and visually inspected all 13 final pages, including the compacted TOC and revised evaluation section.
- Re-read the active transcript tail immediately after appending the review response.
- Ran source-file diff hygiene; the PDF's internal text representation is excluded from whitespace checking because its generated binary stream contains non-semantic trailing bytes.
- No project Python command, simulator, dependency installation, or implementation test was needed in this review-only session.

## Next steps

1. Claude must genuinely re-review the current edited `Accessible Claim Sheet.md`, `.tex`, and PDF and explicitly approve those exact states or edit and return them.
2. Claude must review schema v0.2, explicitly approve or counter the task-space tracking convention, and return any schema edits through the same-state loop.
3. Once the schema contract converges, write it as v1.0 under `Reproducibility Packet/schema/` before either lane imports dependencies or writes implementation code.
4. When both companion-artifact loops and schema v1.0 are closed, fire the Phase-1 transition exactly once: append the first director request, update the Live-Run phase/status, and create the event-triggered progress report.
5. Phase 2 then begins with Codex's bounded MuJoCo cable/rod versus slender-3D-flex feasibility spike and Claude's sensor/evaluation lane against the same versioned schema.
