# Human Report 20 — Claude

**Session date and time:** 2026-07-22 15:16 PDT (checked at the shell when this report was created)
**Phase:** Phase 2 — Execution
**Session type:** Cross-review of Codex's Session-19 build, with corrections and two adversarial probes of my own

---

## The one-paragraph version

Codex spent its Session 19 doing exactly what I asked for in Session 19: it accepted my diagnosis that the structural "recovery" action was pointed away from the metric it is judged on, and it built a screen to find a better action. The screen honestly blocked its own candidate. I reviewed that screen, reproduced every number in it, and found one real defect (the baselines every percentage is measured against were themselves ungated) which I fixed. Then I ran two experiments the screen did not run, and they changed the picture more than the screen itself did. **First: the gate that produced the screen's headline verdict cannot actually resolve the quantity it gates — I re-ran the identical design with a different noise realization and the verdict flipped from BLOCK to ADVANCE.** The block is still correct, but for a different and much more robust reason, which I found and put in the report. **Second, and this is the important one: I measured how much tracking error each fault actually causes, and the structural fault causes essentially none — 0.08%, against a contract that requires a 10% improvement.** There has never been anything for a structural recovery action to recover on this test condition. The actuator fault, by contrast, causes 6.4%, and the recovery code we already have fixes 86% of it. So the project's control question has a live path, it is just not the path either of us was looking at.

---

## What I did, step by step

### 1. Read in

Re-read `AgentPrompt.md`, `Project Details/Project Details.md`, my `Summary of Only Necessary Context.md`, the three concluded chat summaries, and the active Phase-2 chat. The review loop I opened in Session 19 had been **closed** — Codex genuinely re-reviewed my three edits and explicitly approved that exact state. It then handed me a new one: a bounded structural-action family screen, plus a self-correction turn tightening one of its own guards.

### 2. Reproduced Codex's screen independently

Three separate checks, deliberately not sharing code with the artifact where it mattered:

- **Decision arithmetic — 50/50 checks, zero mismatches, first pass.** I re-derived the paired tracking reductions, all four candidate gates, the selection rule, both assessment gates and the source-specificity margin from their written definitions rather than importing Codex's functions, and checked them against the committed data files. Everything reproduced: all nine candidate rows, the eligible set, the selection of the 2× action, the structural mean/min of 19.88% / 19.40%, the healthy 20.15%, the −0.263 margin, both gate verdicts, and every number printed in the report.
- **Byte-determinism — 5/5.** All five artifacts regenerate SHA-256-identical to the committed ones and to the hashes Codex reported, at 10 workers against Codex's 8. Determinism is worker-count independent.
- **My own 84-arm drive.** I wrote my own rollout runner and my own implementation of the tracking metric from the schema definition. Against the packet's own metric function across all 84 arms: **maximum absolute difference 0.000e+00.** Zero lifecycle violations, zero safety or saturation incidents.

Full packet: **173 tests passing** before my edits.

### 3. Found and fixed one real defect

`decide_assessment` checks the *acting* arms of each comparison for safety, saturation, one-evaluation lifecycle, and correct timing. It never checks the **no-action baseline rows** — and every percentage in the report, including the entire source-specificity margin, is computed *against* those baselines. A baseline that had itself acted, evaluated the classifier twice, moved before the scheduled decision, saturated, or raised a safety flag would still have supported an ADVANCE, with every visible gate green. The acting case is the worst: measure a "reduction" against an already-acting baseline and the number means nothing.

This is the same shape as the gap Codex closed in its own correction turn, and the *tuning* half of the same script already holds its baseline to this standard — the assessment half was simply the weaker of the two. I added a `_baseline_comparison_sound` check and folded it into each source's existing gate, following the pattern Codex used in its correction (strengthen a flag in place rather than add a new one, so the recorded output is unchanged).

I also added a parameterized regression, 2 sources × 5 broken conditions, that asserts the advancing fixture really advances and then breaks each baseline condition independently and requires a block. Focused tests 27 → 37; full packet **173 → 183 passing**.

### 4. Two probes the screen did not run

This is where the session earned its keep.

**Probe A — is the block a property of the action family, or of the way the winner was chosen?** The screen's tuning stage only ever runs the structural fault, so candidate selection is blind to source specificity and ranks purely on how much tracking improves. Only the winner was ever stressed on a healthy body. I ran all eight non-baseline candidates on both a structural fault and a false-authorized healthy body, on the four assessment seeds.

**Probe B — does the control layer have any live path at all?** Before designing another action, I measured what any action could possibly recover: the tracking deficit each fault causes with no action taken.

### 5. Wrote the review turn, edited the report, closed out

Posted a detailed review to the Phase-2 chat, verified against the file's exact physical tail before and after writing (my standing monitoring duty — the transcript was clean, Codex's turns were physically last). Added a generated section to the screen's report carrying the bounds its own data establishes, and one paragraph to the packet runbook.

---

## Findings

### Finding 1 — the screen's headline gate is a coin flip

The source-specificity gate asks whether the action helps the faulted body more than a healthy one. Conceptually that is exactly the right question, and it is the reason this screen produced a useful negative instead of a false advance. But as built it compares two **unpaired** four-seed averages with no uncertainty estimate, and the quantity it is measuring is much smaller than the noise in its own inputs.

I demonstrated this rather than argued it. I re-ran the identical design — same seeds, same physics, same candidate — changing only the text label that seeds the simulated sensor noise, which is one equally legitimate noise realization of the same experiment:

| | Codex's run | My replicate |
|---|---:|---:|
| Structural improvement | 19.88% | 20.33% |
| Healthy improvement | 20.15% | 20.02% |
| **Specificity margin** | **−0.263 pp** | **+0.311 pp** |
| **Verdict** | **BLOCK** | **ADVANCE** |

Same design, opposite decision. The per-seed spreads inside each arm are 1.0 and 1.3 percentage points — four to five times the margin being gated. The gate also has no floor to fail against: in my replicate, the old 0.75 derate, which makes tracking **18.5% worse**, scores a positive "source-specific" margin. Any gate that certifies the derate as source-specific is not measuring anything.

**The block is still right.** It is right for two reasons that are far outside noise, and I moved the report onto those:

- At an identical 2× multiplier, the action applied *only at the joint the diagnosis blames* recovers 6.16%, while the same action applied everywhere recovers 20.37%. **About 70% of the benefit is produced at the joint carrying no fault** — and the same ~70% holds at every multiplier in the family. That comparison is inside one seed role at a 14-point effect size against ~0.1 point spread. It needed no extra runs; it was already sitting in Codex's tuning data, unread by the selection rule.
- Algebraically, nothing in this setup ever hits a torque limit. I instrumented a rollout to check: peak commanded torque is 9–10% of the controller's own limit and under 4% of the recovery limit, and the applied-to-nominal peak ratio is exactly 2.000000. With no limit active and a linear controller, **the winning "structural recovery action" is mathematically identical to doubling the controller's gains.** It is not *like* a generic retune; it *is* one. Every member of the screened family is a constant scalar gain, which is why the healthy stress could not have failed to fire.

### Finding 2 — the structural fault is loud in strain and silent in motion

This is the finding that matters most, and it is embarrassingly simple: nobody had measured how much tracking error the faults actually cause. I did, with no recovery action running at all.

| Fault | Tracking error, no action | Deficit vs healthy | Relative to seed noise | Peak strain |
|---|---:|---:|---:|---:|
| healthy | 0.859842 | — | — | 19.0 µε |
| **structure** | 0.860499 | **+0.076%** | 0.18× | 38.3 µε (2.0×) |
| **actuator** | 0.914482 | **+6.355%** | 15.0× | 17.2 µε (0.9×) |

The structural fault's tracking deficit is 0.18× the seed-to-seed spread — **indistinguishable from zero.** I get the same 0.18× independently from Codex's committed data. It is roughly **200× smaller than the 10% improvement the project's contract requires.** There has never been anything for a structural recovery action to recover on this test condition, which is why every candidate's improvement had to come from somewhere else, and why it did.

The actuator fault is the exact mirror: **quieter than healthy in the strain sensors, but 83× louder in tracking.**

Two consequences follow, and they reorder what we do next:

- **Retuning the controller is not the binding lever.** I can bound this from Codex's own data: with the 2× multiplier applied to *both* arms — i.e. a retuned controller — the structural deficit rises from 0.049% to 0.378%. Retuning helps by 7.7×, because it shrinks the large common error underneath. It still leaves the structural class **26× short** of the bar. Retune if the controller deserves it, but it will not make a structural action screenable.
- **The actuator class is where the control question is alive, and the code we already have works there.** I ran the existing inverse-gain compensation on the actuator fault: it recovers **85.7% of that fault's entire tracking deficit**, landing within 0.9% of the healthy trajectory, with a source-specificity margin 4.5× larger than any structural one and consistent across all four seeds — no sign-flipping. That is a genuine, near-complete, source-faithful recovery.

But its ceiling is the deficit itself: a *perfect* actuator recovery is a 5.98% improvement, and the bar is 10%. So **on this test condition, no correct diagnosis of any class can meet the contract's control requirement** — structure because there is no deficit, actuator because the deficit is smaller than the bar. That is a property of the fault severities and the task, and it was invisible until someone measured it.

### Finding 3 — the safety gates carried no information, and the action is not free

Every arm in the family reports "zero safety incidents, zero saturation." But the limits sit far from where the system actually operates: joint angles reach 9% of their limit, strain 11% of its, actuator commands under 4% of range. Those gates could not have discriminated between any two candidates.

Meanwhile the selected action raises mean peak contact force from **2.08 to 3.05 N** (42% → 61% of the 5 N limit) and peak strain from **37.9 to 56.9 µε** — on the very link the diagnosis says has lost stiffness. The safety metric scores all of that as zero, because it counts threshold crossings. This is the same blind spot I flagged in Session 19 with the sign reversed: the derate gave up 18.5% tracking to cut peak force 76%; this action buys 20% tracking at 48% more peak force. **We now have two candidate actions trading against each other on an axis the project has no metric that can see.**

---

## Decisions I made, and why

- **Edited and handed back rather than approving.** The baseline gap is a real correctness defect in a decision function whose output string is quoted by the runbook, the public README, and every future session. Same reasoning I used in Session 19, and Codex accepted it then.
- **Folded the new check into the existing gates instead of adding a reported flag.** Adding a key would have changed `summary.json` and broken the byte-determinism claim. Codex used exactly this pattern in its own correction. I verified the result: a full end-to-end re-run with my edits produces the four data artifacts **byte-identical to Codex's original hashes**; only the report moves.
- **Put the bounds in the generated report rather than only in chat.** Everything I added is recomputed from the recorded rows, so it regenerates deterministically and cannot drift from the data. A reader of the artifact alone now gets the deficit number, the margin-versus-noise problem, the unfaulted-joint contrast, and the margin the action consumes.
- **Did not redesign the specificity gate.** Giving it real statistical power is a design choice in Codex's lane, and Codex is about to rebuild this screen anyway. I measured the problem and handed it over rather than imposing my fix.
- **Did not touch the public Live-Run README.** That log is append-only by playbook and the entry is Codex's. Its existing entry already contains the right clause about requiring a measurable deficit. My argument is that the clause should be *promoted ahead of* the retune, not added — and that belongs in the record once the review loop closes, not while it is contested.
- **Did not propose a Claim Sheet amendment yet.** The deficit screen (below) is what tells us whether one is needed.

---

## Reasoning paths explored

- I initially expected the interesting question to be "is the inverse-stiffness action tuned wrong?" Reading the code closed that off quickly: the stand-in estimator pins the severity at a fixed value, so the "severity-conditioned" multiplier never varies and every candidate collapses to a constant gain. That reframed the question from tuning to *form*.
- I then expected the block to be an artifact of the selection rule — pick the strongest candidate on a family of pure gains and you must pick the most generic one. Probe A was designed to test that. It found something more interesting: no candidate is specific beyond noise, so the conclusion is right, but the *gate* that produced it has no resolving power.
- The deficit measurement was not on my plan at the start of the session. It came from staring at the baseline column of Codex's own data and noticing the structural and healthy no-action numbers were the same to four decimal places. That single observation is the session's main result.

---

## Insights worth carrying

- **Measure the headroom before designing the intervention.** Three sessions of work have now gone into structural recovery actions on a condition where the structural fault costs 0.08% of tracking. One cheap experiment — run the faults with no action and look — would have caught it. That is a general lesson about this project, not a criticism of any session.
- **A gate whose verdict flips under a different random seed is a decision, not a measurement.** Worth checking any gate we intend to freeze by re-running it with a different noise realization before we trust its sign.
- **The two fault classes are complementary in a way that is itself a result.** The class where distributed structural sensing wins on diagnosis is the class with no control headroom; the class with control headroom is the one conventional sensing already detects perfectly. If that survives a proper deficit screen, it is an honest, publishable finding about where this kind of sensing does and does not pay — and it is exactly the "diagnostic-only" outcome the Claim Sheet pre-declared a slot for. That would be a real result, not a failure.

---

## Files created or updated

**Edited (in Codex's lane, under review — awaiting its owner re-review):**
- `Reproducibility Packet/scripts/screen_structural_recovery_action.py` — added `_baseline_comparison_sound()` and conjoined it into both assessment gates; added `_scope_lines()`, a generated report section stating the measured bounds on the recorded decision.
- `Reproducibility Packet/tests/test_structural_recovery_action.py` — added `_advancing_assessment_rows()` helper and a 2×5 parameterized regression on baseline integrity (27 → 37 focused tests).
- `Reproducibility Packet/results/structural_recovery_action_screen/structural_recovery_action_report.md` — regenerated; the diff is purely additive. The other four artifacts in that folder are byte-unchanged.
- `Reproducibility Packet/README.md` — one added paragraph to runbook Step 13 carrying the deficit finding and the resulting ordering.

**Appended (co-owned, append-only):**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — my Session-20 review turn (1397 → 1490 lines; tail verified before and after writing).

**Rewritten:**
- `agents/Claude/Summary of Only Necessary Context.md`
- `agents/Claude/README.md`

**Created:**
- `agents/Claude/Session Summaries/HumanReport20.md` (this file)

**Not changed, deliberately:** the root `README.md` Live-Run log (append-only, Codex's entry, and the finding is mid-loop); `agents/Claude/references.md` (no external sources read this session — it was reproduction and measurement).

**Scratchpad, outside the repository, not committed:** `s20_decision_audit.py` (the 50-check arithmetic audit), `s20_probe.py` (the 84-arm probe driver), `s20_probe_rows.json`, and two full regenerations of the screen for hash comparison.

---

## Verification summary

| Check | Result |
|---|---|
| Independent decision arithmetic | 50/50, zero mismatches |
| Independent 84-arm drive, my metric vs the packet's | max difference 0.000e+00 |
| Byte-determinism, 5 artifacts, 10 workers vs Codex's 8 | 5/5 SHA-256 identical to Codex's reported hashes |
| Full end-to-end re-run **after** my edits | 4/5 artifacts byte-identical to the originals; only the report moves, and it regenerates deterministically |
| Recorded decision recomputed under my edited gate | identical key-for-key **and** value-for-value |
| Full packet test suite | 173 passing before, **183 passing** after |
| `compileall`, CLI help | clean |
| Chat transcript tail | verified before and after writing; clean |

---

## Next steps

**For Codex (the open loop):** genuinely re-review my three edits — the baseline gate, the regressions, and the report section — and either approve that same state or edit and hand back. If it accepts the diagnosis but not my implementation, that is a real disagreement and the playbook asks it to say so.

**The concrete proposal I put in front of its next build**, in order:

1. **Run a deficit screen before any further action screen.** Sweep fault severity, and task speed and amplitude if needed, and record the no-action tracking deficit for each fault class. Advance only a condition where the deficit clears the 10% bar with margin. It is cheap — three sources × a few seeds × a severity grid, with no action arms at all — and it turns "the condition must show a measurable deficit" from a hope into a gate. Severity grids are already on the freeze list, so this is work the project owes anyway.
2. **Then screen actions on a condition that can actually discriminate them**, with the specificity comparison moved into *selection* rather than left in assessment, and given a real uncertainty estimate.
3. **If no admissible severity produces a ≥10% structural deficit inside the safety limits, that is the answer** — the structural class lands on the Claim Sheet's pre-declared "diagnostic-only" outcome, and we say so plainly.

**For me:** nothing in my own lane is unblocked yet — the learned attribution head and the RMA latent still need PyTorch and frozen confirmatory data, and the evaluation driver still needs a frozen data layout. My next session's work is most likely the review of whatever Codex builds next, plus the carried `null_std` floor consistency fix the next time I touch the estimator.

**Not due:** no progress report this session. The next regular one is my Session 24; Sessions 17–20 closed no phase and approved no Claim Sheet amendment.

**Nothing is frozen.** `config.json` remains unfrozen, and this session added a prerequisite to the open freeze list rather than removing one.
