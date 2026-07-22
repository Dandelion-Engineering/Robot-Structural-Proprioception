# Human Report 17 — Claude

**Current Date and Time:** 2026-07-21 18:05 PDT

**Agent:** Claude · **Session:** 17 · **Project phase:** Phase 2 — Execution

---

## Summary

This was a pure cross-review session. Codex's Session 16 built and ran the project's first **matched contact-enabled C1/S development pilot** — the experiment that applies the previously-screened z = 0.100 m endpoint-contact plane identically to matched conventional (C1) and structural-sensing (S) sensor suites, and asks whether the structural signal survives real contact, a real closed-loop sensor-fault path, and the full five-second post-fault horizon. Codex's pilot **blocked** on all three of its decision surfaces and Codex handed the artifact to me for genuine first review. My whole session was that review, done the way I've done every review this phase: by reproducing the result independently rather than re-running Codex's code, then approving the exact state or handing back edits.

**Outcome: I found no defect. I reproduced all three block gates independently, confirmed the artifact is byte-for-byte deterministic, and explicitly approved Codex's exact handed-off state — closing the review loop.** I also raised two non-blocking forward notes for the redesign that this block now requires. Nothing was frozen; the central research question remains open; `config.json` stays unfrozen.

### What the pilot found (and I confirmed)

The pilot has three independent gates, and each one blocks for a different, real reason:

1. **The structural signal is genuinely there, but the detector trips too often on healthy runs.** At the single scheduled post-probe decision, the S suite detected all three fault types and correctly named their shapes 100 % of the time, while the conventional C1 suite was structurally blind (it caught only ~21 % of the structural faults). That is exactly the advantage the whole project is chasing — the strain gauges see link-stiffness loss that conventional sensing misses. **But** S also raised false alarms on **8.3 %** of healthy held-out runs, above the 5 % development screen, so the operating point cannot advance yet.
2. **A one-shot diagnosis can't be reused continuously.** When the pilot's simple nearest-prototype diagnosis (a deliberately labeled stand-in, not the real learned model) was applied not once but at every step as the diagnostic probe slid out of its measurement window, it drifted — by the last decision, every arm was calling "actuator fault," including the healthy and the sensor-fault runs, which then received inappropriate corrective commands.
3. **The static contact profile isn't safe over five seconds.** Over the required onset+5 s horizon the arm re-contacted the plane three times and swung a joint past its unchanged angle limit for over a thousand steps. The former "no-contact control" plane also started contacting on the longer horizon.

None of these is evidence against the research hypothesis — they are method/configuration problems that tell us precisely what the next redesign must fix.

### How I verified it independently

I wrote my own reproduction harness (outside the packet) that drove the physics myself and recomputed every gated number with my own logic:

- **The five-second safety audit reproduced bit-for-bit.** I re-ran the plant at both contact heights across the three physical scenarios and recomputed contact episodes, forces, and the joint-angle safety flag from scratch — including recomputing the angle flag as "|joint-1 angle| > π" and checking it against the plant's own flag column. Every number matched (1111 / 1658 / 1651 angle-violation steps at z = 0.100). I also confirmed the block is the joint-angle limit alone: the contact-force flag never fires (peak forces 3.2–4.5 N, under the 5 N limit).
- **The false-alarm gate reproduced.** I collected the detector's feature vectors at the exact causal decision index myself for all 80 seeds and recomputed the threshold and the 8.3 % (4/48) S false-alarm rate and the 4.2 % (2/48) C1 rate independently.
- **The drift reproduced.** I re-ran two arms through the real closed-loop seam and reproduced the exact changed-command counts and the drift to "actuator."
- **Determinism.** I regenerated the whole artifact with the default command to a scratch directory; all five output files were SHA-256 identical to the committed ones.
- **Tests.** The full Reproducibility Packet suite is **148 passed** on my machine.

## Challenges and how they were overcome

**My first reproduction pass disagreed with Codex — and the bug was mine.** On the first run, my independent false-alarm numbers came out looser than the committed ones (S 1/48 instead of 4/48, a higher detector threshold). Rather than assume either side was right, I traced it: the sensor-noise generator is keyed on a text `pair_id`, and I had abbreviated the split label to `cal`/`eval` in my harness where the real pipeline uses `calibration`/`evaluation`. That single string difference reseeded the simulated sensor noise, changing the numbers. I fixed the label and everything matched exactly. This is worth recording for two reasons: it is honest about where the discrepancy came from (my harness, not Codex's artifact), and it is a genuine reminder that these pilot numbers depend on the exact seed-substream identity — which is why the byte-identical regeneration is the real proof of determinism. The decisive safety-audit gate was immune to this because it doesn't use the sensor noise at all, which is why it reproduced perfectly on the first pass.

**Keeping the review genuinely independent.** The temptation in a review is to re-run the author's script and check it doesn't crash. That is not a review. I drove the physics with my own code, recomputed metrics with my own logic, and re-derived the pass/fail decision from the committed rows independently, so that agreement means two independent computations landed on the same answer — not that one computation ran twice.

## Important decisions and reasoning

- **Same-state approval, no edits.** The artifact is correct, honest, well-tested (five focused new tests), reproducible, and its wording (report, packet runbook, public status log) matches the numbers and calls the result a development block rather than a research result. There was nothing to fix, so I explicitly approved the exact state Codex handed me and the loop is closed.
- **Two forward notes instead of edits.** Because corrections in this project propagate *forward* (into the next piece of work, not by reopening finished work), I recorded two observations for the redesign the block now requires (below) rather than changing Codex's artifact.
- **Left the public status page untouched.** Codex already logged the matched-pilot block in the public Live-Run README during its Session 16. My session confirmed that block; a confirming internal review is not itself a new public-facing event, so adding a second entry would only add noise to a log that is lean by design. (Same call I made in Sessions 15 and 16.)
- **No progress report this session.** My next scheduled director progress report is Session 24; this session closed no phase and approved no amendment to the contract, so no report was triggered.

## Reasoning paths and insights

The two forward notes are the session's substantive contribution beyond confirming the block:

1. **No part of this pilot actually lets the closed-loop recovery affect safety — so the redesign must fix that, not just lower the contact plane.** In the short closed-loop check, the first contact happens (~2.0 s) *before* the first diagnosis decision (~2.27 s), so the single contact episode is entirely pre-recovery; and the five-second safety audit is pure open-loop with no controller at all. So neither gate exercises whether recovery *helps* with contact or safety. For the eventual "does structural sensing improve control" comparison to even be *able* to show an advantage on the safety axis, the diagnosis has to land before — and the controller must have authority over — the safety-relevant window. This sharpens *why* Codex's called-for redesign matters.
2. **The joint-angle violation is a property of the open-loop task, not of the contact.** The angle limit is exceeded even at the low control plane for the healthy and structural runs (311 / 334 steps), while the low-plane actuator run *with* real contact has zero angle violations. So the thousand-plus-step violations at the higher plane come from the open-loop task command swinging the joint past π over six seconds — not from the contact. The practical consequence: a gentler or lower contact profile will not fix it; the first-order fix is a **stabilized, bounded task trajectory**, with the contact profile chosen underneath it.

The broader insight, unchanged and reinforced: the structural-sensing advantage keeps showing up cleanly (S sees the structural fault where C1 is blind), but the project's honest bottleneck is no longer *detecting* the signal — it is embedding that signal in a **safe, stable closed-loop experiment** whose result we could trust. That is now the explicit next block of work.

## Files created or updated during the session

**Created:**
- `agents/Claude/Session Summaries/HumanReport17.md` (this report)

**Updated:**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended my Session-17 same-state review approval (loop closed) + two forward notes, under the append-only transcript hard gate (verified: my header appears once at line 1108, after Codex's handoff at line 1052, physically last).
- `agents/Claude/README.md` — recorded the Session-17 review-loop closure and the 148-test packet count.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 18.

**Reviewed but deliberately not changed** (Codex's Session-16 artifact, approved as-is): `Reproducibility Packet/scripts/run_matched_contact_pilot.py`, `Reproducibility Packet/tests/test_matched_contact_pilot.py`, `Reproducibility Packet/results/matched_contact_enabled_pilot/` (summary.json + three CSVs + report), `Reproducibility Packet/README.md` (runbook Steps 10–14), root `README.md` (Live-Run blocker entry).

No new external sources were read (a review/reproduction session), so `agents/Claude/references.md` was not changed. No `.gitignore` change is required — the session touched only markdown documentation and a chat transcript; my reproduction scripts live in the session scratchpad outside the repository.

## Verification performed

- Independent three-gate reproduction (my own plant drive + metric recompute): **all checks passed** after the harness fix — safety audit bit-for-bit, info gate (S 8.3 % / C1 4.2 % false alarms, thresholds, per-class detection), and the closed-loop drift.
- Byte-for-byte determinism: all five committed artifacts regenerated SHA-256 identical.
- Full Reproducibility Packet test suite: **148 passed**.
- `summary.json` scanned: no NaN/Infinity tokens.
- Packet runbook step numbering: consistent (Steps 1–14), cross-references updated.
- Chat append hard gate: pre-write 1104 lines; my header once at line 1108, after Codex's handoff (line 1052), physically last; post-write 1140 lines.

## Next steps / pending actions

1. **Codex's next increment (its lane):** the bounded task / contact / controller redesign that the block requires — a stabilized finite trajectory that keeps every scenario inside the unchanged safety limits over onset+5 s, plus a fix for the diagnosis reference lifecycle (make one held decision, condition the reference on phase/time, or train a temporal model over the full post-probe trajectory). My two forward notes feed this directly.
2. **My lane (still post-config-freeze, do not build early):** the learned attribution head + the RMA latent (need a GPU PyTorch build + frozen config + confirmatory data); the leakage test and whole-trajectory split audit (need real multi-run storage); the evaluation driver that slices the [t_c, t_c+5 s] window for the paired C1-vs-S comparison (needs the frozen data layout). On my next touch of the estimator I will also fold in the carried `null_std` floor consistency nit.
3. **Config freeze remains the gate.** Still open before any confirmatory data can be generated: validation-sized healthy/four-class calibration (with per-suite probability calibration), severity/onset grids, non-load-bearing sensor constants, class/abstention/selective/OOD thresholds, the bounded task/contact/controller profile, the reference-lifecycle choice, and the split/leakage/storage/hash audits.
4. **No progress report due until my Session 24**, unless a phase closes or a contract amendment is approved before then.

The central research question — whether distributed structural sensing gives a real adaptive-control advantage — remains open. This session confirmed, independently, that a promising structural detection signal is not yet embedded in a safe, stable closed-loop experiment, and pinned two specific reasons the next redesign has to address.
