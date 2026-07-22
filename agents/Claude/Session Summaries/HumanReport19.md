# Human Report 19 — Claude

**Current Date and Time:** 2026-07-22 13:28 PDT

**Agent:** Claude · **Session:** 19 · **Project phase:** Phase 2 — Execution

---

## Summary

This was a cross-review session in my lane's usual shape: Codex handed over a substantial new development artifact, I reproduced its result independently from scratch, and I decided whether to approve it or correct it. This time I corrected it. The numbers were all right; the *gate logic that turns those numbers into a recorded verdict* was under-guarded, and the artifact's own honesty section was missing the bound that most limits its headline figure.

Codex's Session-18 artifact is the **bounded noisy held-decision information review**. It takes the bounded task/contact condition I approved last session and replaces the fake diagnoses ("stand-ins" that were simply told the right answer) with a real, noisy instrument that has to work the answer out from sensor data. Its result splits in two, and the split is the interesting part:

- **The information half passed.** The structural-sensing suite (S) correctly identified what had changed 99.5% of the time (macro-F1 0.995); the matched conventional suite (C1) managed 0.704. The whole gap is one fault type: C1 caught the structural fault 8.3% of the time, S caught it 100%.
- **The control half blocked.** In the one case where S's extra information actually changed what the robot *did* — S correctly diagnoses the structural fault and acts on it, C1 misses it and does nothing — acting made tracking **18.6% worse**, not better. Codex blocked the recovery-control profile rather than shipping that as progress.

I reproduced all of it. I drove all 592 simulation runs myself, refit both suites' references with my own code, and recomputed every reported number with independently written implementations: **53 of 53 checks passed, zero mismatches**, on the first pass. All five result files regenerate byte-for-byte identically, matching the fingerprints Codex reported — and I ran with a different number of parallel workers than Codex did, so the result doesn't depend on machine scheduling.

Then I made two corrections, so this is an **edit-and-hand-back, not an approval**. The review loop stays open until Codex re-reviews my edits.

**The correction that mattered.** Every one of these development gates ends in a single recorded verdict string, and that string is what the runbook, the public README, our chat, and every future session quote as "what was decided." Codex's script had five separate pass/fail gates but the advancing verdict was tested against only one of them. I ran the counterfactuals rather than arguing from reading the code, and the script would have emitted the same advancing string when the two suites' histories were not properly matched (which would confound the entire comparison), when a run raised a safety flag, when the diagnosis lifecycle the verdict *names* was broken, when recovery acted before it was allowed to, and when every single decision window was contaminated by contact. One of the five gates — "were all 592 decision windows clean?" — was computed, printed, and gated nothing at all. I tightened it so that only the control-sensitivity verdict can separate the two advancing labels; everything else failing is a block. **This changed none of Codex's numbers**: I re-ran the decision function on the committed data and got a key-for-key identical result, so four of the five result files are byte-unchanged.

**The second correction** was an honesty bound. "0.995 accuracy on 48 held-out seeds" reads like generalization. It isn't: every run in the study uses the *same single fault setting* per class — same severity, same location, same onset — and the held-out seeds vary only the sensor noise. That is separation under noise at one operating point, which is a real and useful thing to have measured, but it is not the same claim. I added a paragraph to the report saying so, and quantified a limitation Codex had honestly flagged in prose: the mechanism's "I'm not sure" option can never trigger on this fault library, because the smallest observed decision margin is 0.90 and the threshold would have to be below that to ever bind.

**Where I did not edit:** the public running log. That file is append-only by playbook rule and the entry is Codex's, so I recommended a seven-word qualifier in chat and left the decision to Codex.

Finally, I raised three forward notes, one of which I think is the most consequential thing this session produced. **The structural recovery action and our own headline success metric point in opposite directions by construction.** When the robot concludes "my structure has weakened," the action it takes is to back off — a bounded 25% torque derate, which is the honest response to a stiffness loss you cannot invert. But our Claim Sheet scores the control half of the project on *tracking accuracy*, with safety entering only as a "don't get worse" side-constraint. Backing off trades accuracy for margin. So the 18.6% regression is not a tuning mistake that better gains would fix — it is the direction of the action. On the current design, the best a *correct* structural diagnosis can do on our headline metric is break even. Meanwhile the thing it demonstrably *did* achieve — cutting peak contact force by 76%, from 2.05 N to 0.50 N — our metric set scores as literally nothing, because safety is counted as threshold crossings and both arms were at zero. So the project has a real fork in front of it: redesign the structural action to compensate rather than retreat, or amend the contract so a graded safety-margin win counts. Both are legitimate; picking neither and discovering it at the final comparison is not. The value of finding this now, on a cheap development condition, is exactly what these gates are for.

## What was accomplished

### 1. Workflow followed in order

Read `Project Details/Project Details.md` in full, then my continuity file, then every chat summary and the active Phase-2 transcript. Codex had opened a new review loop in its Session-18 turn. Read `Playbooks/review-cycle.md` before reviewing and `Playbooks/live-run-readme.md` before deciding the heartbeat. Cross-review duty satisfied by reading Codex's `HumanReport18.md` and the work it points to.

### 2. Independent reproduction (53/53 checks, first pass)

I wrote `s19_information_reproduce.py` (scratchpad, outside the repo). Independence discipline: my own causal-schedule arithmetic; my own collection loop and window-capture policy; my own reference fit (healthy mean/scale, leave-one-out detection threshold, prototype centroids, leave-one-out selective margin); the standardized distance, classification, and action-gate mapping written out from their stated definitions rather than imported from the artifact under review; and my own macro-F1 (abstention scored as error), per-class recall, and tracking integral.

What reproduced:

- **Causal schedule from scratch** — onset index 500, one-cycle probe 625 steps, first decision step **1136 = 2.272 s**, an exact multiple of the 16-step decision stride, before movement at 2.400 s. Seed roles disjoint (14000–14099 calibration, 14100–14147 held-out); the declared 5% false-alarm tail requires ≥100 calibration values and gets exactly 100.
- **All 592 pre-decision histories** contact-free and safety-flag clean under my own audit.
- **Both detection thresholds to 1e-12** (C1 1.281200511392, S 1.263399593694), each strictly below its own calibration maximum.
- **All 384 held-out decision rows field-by-field** — score, detected, predicted source, margin, abstained, headline call, action-gate category. Zero mismatches. Macro-F1 0.703704 / 0.994791, every recall, false-alarm rates 4.17% / 2.08%, minimum per-fault detection 8.33% / 100%, and both gate verdicts. The three false-actionable healthy cases are exactly C1/14137, C1/14141, S/14141.
- **All 8 representative full-horizon rows**, driven off *my* references rather than Codex's — tracking integral, peak force, contact steps and episodes, changed-command counts, held call, action-gate state, and the pre-decision history fingerprint. Every arm evaluates the classifier exactly once, none acts before the decision, and **all seven safety flags are zero** (six recomputed directly from raw privileged truth; the 3-D tip-workspace flag taken from the plant's own column, per the harness lesson I recorded in Session 18). Maximum joint angle 0.3599 rad against a π limit.
- **Matched histories bit-identical** across suites for all four sources — the empirical proof that projecting the conventional suite from the structural suite's run is equivalent to a separately matched run, rather than an assumption.
- **The block reproduces** — structure is the only pair where the extra information changes the action; the other three pairs are bit-identical across suites; tracking goes 0.8589 → 1.0184 (−18.6%) while peak force goes 2.051 → 0.499 N with zero safety incidents in either arm.

A detail worth recording because it strengthens the finding beyond the headline number: **C1 is not weakly sighted on structural faults, it is blind.** Its structural scores (median 0.955, max 1.560) sit on top of its healthy scores (median 0.972, max 1.574) — the few "detections" are the same distribution tail the false alarms come from. S separates completely, with a genuine gap: healthy max 1.457 below structural minimum 1.724. And the two suites' healthy distributions are nearly identical with near-equal thresholds, so the dimension normalization is genuinely putting the suites on one scale — the comparison is fair by measurement, not by assertion.

### 3. Byte-determinism and tests

Regenerated all five artifacts from scratch into the scratchpad and compared SHA-256: **all five identical** to committed and to Codex's reported hashes (`053b9723…`, `d3e62eb7…`, `71b044e6…`, `25187670…`, `7248d802…`). I used 10 process workers against Codex's 12, so determinism is independent of parallel scheduling. Full packet: **159 passed** before my edits, **160 passed** after. `compileall` clean.

### 4. Corrections made (loop stays open)

- **`scripts/run_bounded_noisy_information_review.py` — decision-gate completeness.** Introduced a `lifecycle_pass` conjunction requiring the information gate, the action gate, representative safety/lifecycle, matched pre-decision histories, and clean decision windows; only the control-sensitivity verdict may now separate the two advancing labels. All five flags are still reported individually and unchanged, so Codex's three-layer separation is preserved. Verified the recorded decision dict is key-for-key identical, so `summary.json` and all three CSVs are byte-unchanged.
- **Same file — report interpretation boundary.** Added the single-fault-setting bound and the quantified abstention limitation (smallest held-out margin computed from the rows, 0.90). Regenerated `bounded_noisy_information_report.md` deterministically from the committed `summary.json`; the diff is purely additive.
- **`tests/test_bounded_noisy_information_review.py`.** The fourth test's docstring claimed "an information pass cannot silently override an unsafe action/mechanics path" while its assertion pinned the opposite. Rewrote it to assert what it says and split it in two: one test for the split-advance case exactly as committed, one that walks all five failure modes and requires a block for each while confirming the information gate still passes.

### 5. Not edited, raised instead

The root Live-Run README entry. `Playbooks/live-run-readme.md` makes that log append-only and names rewriting it as a failure mode, and the entry is Codex's. I recommended a seven-word qualifier in chat ("at one development fault setting per class") and left the call to Codex, noting the packet README's boundary section already carries the equivalent statement.

## Challenges and how they were handled

**Deciding whether the decision-logic gap was a defect or a design choice.** Codex had a test pinning the existing behaviour, so it was deliberate, and there is a defensible reading — the three questions are meant to be reported separately. I resolved it by running the counterfactuals instead of arguing from the code: five distinct failure states, each of which would still have produced an advancing verdict string, including one gate that fed nothing at all. That converted a style disagreement into a demonstrable misstatement risk. I also checked the fix could not disturb the recorded result before applying it.

**Keeping the reviewer edits from disturbing the evidence.** The whole value of a byte-deterministic artifact is that it can be checked. I sequenced deliberately: regenerate and hash-verify the committed state *first*, then edit, then prove invariance by re-running the decision function on the committed rows and regenerating the report from the committed summary rather than re-running a 12-minute simulation. The result is that four of five artifacts are provably untouched and the fifth differs by exactly two added lines.

**Scope discipline on edits.** I considered three edits and made two. Editing the append-only public log would have violated a standing playbook rule to fix a wording issue already covered elsewhere in the record; I raised it as a recommendation instead. Being a reviewer does not mean editing everything I would have written differently.

**Compute time.** The review is expensive — 592 simulation runs plus 8 six-second rollouts, about 20 minutes per full pass, and I needed two independent passes. I ran them in the background and did the code review, cross-checks, and consistency audits while they ran.

## Important decisions and reasoning

- **Correct rather than approve.** The numbers were flawless, and it would have been easy to approve on that basis. But the artifact's job is to *record a verdict*, and the verdict logic was weaker than the verdict claimed. Approving would have left a latent misstatement in the one string everything downstream quotes.
- **Fix the gate without touching the result.** A reviewer who changes the recorded numbers while "fixing" the logic destroys the audit trail. Proving byte-invariance was part of the correction, not an afterthought.
- **Make the test assert its own docstring.** The old test was not wrong so much as mislabelled — it described a property it did not check. That is worse than a missing test, because it reads as coverage.
- **Quantify the abstention limitation rather than restate it.** Codex had honestly said abstention was untested. "The smallest observed margin is 0.90, so no threshold below 0.90 can ever bind" makes it a fact a reader can act on, and makes clear it is a property of the fault library rather than of the mechanism.
- **Raise the metric-direction conflict now, prominently.** This is the session's most consequential observation and it is not a defect in Codex's work — it is a consequence of two independently reasonable choices (an honest derate as the structural action; tracking error as the control metric) that interact badly. Surfacing it on a cheap development condition is worth far more than discovering it at the confirmatory comparison.
- **Leave the Live-Run README alone.** Two standards were in tension (the reviewer may edit an artifact under review; the running log is append-only). The log's own standard is the more specific one, and the entry belongs to Codex.

## Files created or updated

**Updated (my corrections to Codex's artifact, now in review):**
- `Reproducibility Packet/scripts/run_bounded_noisy_information_review.py` — decision-gate completeness; report interpretation boundary.
- `Reproducibility Packet/tests/test_bounded_noisy_information_review.py` — rewrote and split the gate-separation test (4 → 5 tests).
- `Reproducibility Packet/results/bounded_noisy_information_review/bounded_noisy_information_report.md` — regenerated deterministically; purely additive diff.

**Updated (session record):**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended my Session-19 review turn at the verified physical tail.
- `agents/Claude/Session Summaries/HumanReport19.md` — this report (created).
- `agents/Claude/README.md` — workspace map and review state.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 20.

**Deliberately unchanged:** root `README.md` (Live-Run heartbeat checked; a confirming review with in-review corrections is not a new public event, and the split-decision entry Codex logged still stands), `agents/Claude/references.md` (no new external sources — reproduction session), `Reproducibility Packet/README.md` (runbook numbering and cross-references verified consistent 1–16; the decision string is unchanged), `config.json` (unfrozen).

**Scratchpad, outside the repo:** `s19_information_reproduce.py` (53-check independent reproduction), `regen/` (byte-determinism regeneration).

## Next steps / pending actions

1. **Codex owner-re-reviews my two corrections and the split test.** Per the review-cycle playbook, accepting the diagnosis but not my implementation is a real disagreement worth stating rather than swallowing. The loop closes only when we both explicitly approve the same state.
2. **The structural-action direction decision (my forward note 1)** now sits in front of the evaluation-sized comparison: re-aim the structural action at tracking, or amend the Claim Sheet so a graded safety-margin win is first-class. The amendment path runs through the protocol, not through a controller tweak.
3. **Build the ambiguous-case fault library before validation-sized calibration**, not after — the abstention thresholds on the freeze list cannot be frozen on a library where they never bind.
4. **`config.json` stays unfrozen.** Open items unchanged.
5. **My own lane stays post-freeze** — the learned attribution head and the adaptation latent need PyTorch and frozen confirmatory data.
6. **Next regular progress report: my Session 24.** Session 19 closed no phase and wrote no approved Claim-Sheet amendment, so no report was triggered.

The central research question remains open. What this session adds is that the structural suite's information advantage now survives a genuinely noisy, role-separated, independently reproduced test — and that the project has a concrete, nameable fork in how it must define a control win, discovered early enough to choose deliberately.
