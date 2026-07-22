# Human Report 21 — Claude

**Current date and time:** 2026-07-22 16:51 PDT *(checked at the shell at the moment this report was created)*
**Phase:** Phase 2 — Execution
**Session type:** Genuine first review of Codex's per-class fault tracking-deficit screen, plus the measurement that decides what the screen's result licenses

---

## The one-paragraph version

Codex built the screen I asked for last session: hold the task fixed, apply no recovery action at all, sweep fault severity, and measure how much tracking error each fault actually causes. Its answer is right and important — **no amount of structural softening produces a tracking deficit on this task**, so there has never been anything for a structural recovery action to fix here. I reproduced every number in it (42 independent checks, then 36 simulation arms I drove myself, with my own tracking metric matching the packet's to zero difference). Then I did the thing the screen was built to enable: I ran the recovery action on the condition the screen advanced. **It does not survive.** The screen advanced a setting on which the best possible outcome is barely over the contract's bar, and more than half of even that comes from an action that helps a perfectly healthy robot just as much. I corrected one real defect in the gate — it converted the contract's target into the wrong units and quietly gave away two-thirds of its own safety margin — regenerated the artifacts (the raw per-run data came back byte-identical, so only the derived conclusions moved), and handed the whole thing back to Codex with the measurement and a proposal for what the next gate should actually test.

---

## What I did, in order

### 1. Startup and context (per `AgentPrompt.md`)

Read `Project Details/Project Details.md` in full; my own `Summary of Only Necessary Context.md`; the three concluded-chat `Summary.md` files; the complete recent span of the active Phase-2 transcript. Checked `git log` and the working tree (clean, on `main`, at Codex's Session-20 commit `163dade`). Read Codex's `HumanReport20.md` and the Claim Sheet's Slots 7, 11, 12 and 13 to confirm the exact wording of the control bar before relying on it.

### 2. Two housekeeping confirmations

- **My Session-20 review loop is closed.** Codex genuinely owner-re-reviewed my four edits to its structural-action screen and explicitly approved my exact handed-back state. Both approvals name the same state.
- **The transcript-order failure mode recurred, and the repair holds.** Codex's Session-20 approval turn was inserted at line 1,331 in the middle of the chat file instead of at the end — the same anchor-matching failure Randy flagged in Session 6. Codex's own verifier caught it and appended a dated correction at the true end of the file. I did not take that on trust: at the git level, Codex's commit changed that transcript by **+72 lines and −0 lines**, so the misplacement was a pure insertion and nothing was deleted, moved, or rewritten. Per my standing monitoring duty I opened `chats/Claude-Codex-Human/Transcript Order Monitoring/` and logged the occurrence and the verification, stating explicitly that no action is needed from Randy.

### 3. Independent reproduction of the screen

I wrote my own audit that recomputes the paired deficits, all three per-case gates, the selection rule and the decision from their stated definitions rather than importing Codex's code, and ran it against the committed artifacts.

- **42/42 checks passed, zero mismatches, first pass.** All 20 candidate-summary rows field by field; both sensor-control summaries; the selection; the decision string; JSON↔CSV agreement on every field; no `NaN`/`Infinity` token; all ten report table rows regenerated from the JSON that produced them.
- **All 84 recorded arms audited raw:** exactly one classifier evaluation each, zero recovery-command changes, no pre-decision change, zero safety-flag steps on all seven flags, zero saturation, exactly one contact episode, tracking integral finite and positive.
- **The common-random-number pairing verifies rather than asserts:** within each (role, seed) all twelve fault settings share one identical pre-fault history hash, and the seven (role, seed) pairs produce seven distinct hashes. That is what makes the deficits genuinely paired.
- **Codex's quoted worst-case operating values reproduce exactly** and sit well inside the safety limits.
- **36 arms I drove myself**, with my own trapezoidal implementation of the tracking metric written from the schema definition: **maximum difference from the packet's implementation, 0.000e+00**, and the deficits match Codex's to four decimal places.
- Codex's report regenerates byte-for-byte from its own `summary.json`.

### 4. The defect I found: the gate converted the contract's target into the wrong units

This is the correction I made, and it is worth explaining plainly because the arithmetic is the whole point.

The Claim Sheet's control bar is a **reduction**: the structural robot's tracking error must be at least 10% *lower than* the conventional robot's, measured against the conventional robot's error. Codex's screen measures a different quantity — a **deficit**: how much worse the faulted robot is *than a healthy one*, measured against the healthy robot's error. Those two percentages have different denominators, so they are not interchangeable.

If an ideal recovery action restored healthy tracking exactly, a deficit of `D` would show up as a reduction of `D / (1 + D)`. Run that through the numbers: Codex's gate demanded a **12% deficit** (the 10% bar plus a declared 2-point development margin), but a 12% deficit can only ever produce a **10.71% reduction**. Of the two margin points, **0.71 survives the change of units**. And the setting the gate actually selected has a ceiling of 11.60% — below the 12% the margin was supposed to buy, before any real action falls short of the ideal.

I fixed the conversion rather than the number. The declared target stays exactly what Codex predeclared (10% bar + 2 points); the gate now inverts the relationship and requires a 13.64% deficit to deliver a 12% reduction. Both values are computed only from the two predeclared constants — no observed result enters — and the correction makes the gate stricter, not looser.

Consequence: the mildest setting that clears moves from 0.50 remaining actuator gain to 0.25. **The overall decision string is unchanged** — the actuator class still advances, the structural class still blocks everywhere. I re-ran the entire 84-arm grid with my correction in place, at a different worker count than Codex used: **both per-arm data files came back byte-identical to Codex's committed hashes.** Only the three derived files (the summary, the candidate table, the report) move, which is exactly the footprint a decision-logic correction should have.

I also stated the counter-argument in the handoff, because it is a fair one: 12% was predeclared, and changing a gate after seeing results is precisely what this project is disciplined against. My answer is that the predeclaration was written in reduction units and the code did not carry it into deficit units, so this is an implementation being corrected to its own stated intent — in the conservative direction, with no data-dependent input. Codex may disagree, and I said which resolution I would accept if it does.

### 5. The measurement that matters: the advanced condition does not survive its own action

A deficit screen exists to make the *next* screen meaningful. So rather than wait a session to find out, I ran the next screen's core arm now — the already-approved inverse-gain recovery action, on the advanced condition, with a perfect-knowledge diagnosis (the most favourable case that action family can have), plus the control arm where the same action is wrongly applied to a healthy robot.

| condition | deficit with no action | best possible reduction | **reduction actually achieved** | same action on a healthy robot | **genuinely source-specific part** |
|---|---:|---:|---:|---:|---:|
| 0.50 remaining gain (Codex's selection) | 13.20% | 11.66% | **10.77%** | 6.11% | **+4.67 points** |
| 0.25 remaining gain (corrected selection) | 23.16% | 18.80% | **10.82%** | 6.11% | **+4.71 points** |
| 0.10 remaining gain | 65.73% | 39.66% | **3.10%** | 6.11% | **−3.01 points** |

Four conclusions, none of which the deficit alone predicts:

1. **The units defect was about to become load-bearing.** On the selected setting, the best outcome of the next screen would have been 10.77% against a 10% bar — 0.77 points of margin, with a perfect diagnosis, not the 2 points the screen declared.
2. **Correcting the units does not rescue the advance.** The corrected selection delivers 10.82% — the same. The reason is in the controller, not the fault: the compensation multiplier is capped at 2×, so against a 4× gain loss it only lands the robot at the 0.50-equivalent operating point. Deficit is not the binding variable; the *achievable source-specific reduction* is, and that depends jointly on the deficit, the action family, its cap, and how well the severity is estimated. A deficit gate can only see one of the four.
3. **The specificity standard that blocked the structural action costs the actuator action more than half its benefit.** The same 2× multiplier, wrongly applied to a healthy robot, improves healthy tracking by 6.11%. So only +4.67 points of the 10.77% is more than the action does to a robot with nothing wrong with it. Unlike the structural margin I measured last session (which flipped sign under a different noise draw), this one is stable to ±0.1 points across four seeds — a real source-specific effect, and less than half the bar.
4. **The contract's own comparison is already recorded as zero on this class.** Codex's Session-18 review contains the four representative structural-vs-conventional pairs. On the actuator class both suites diagnose correctly, both act identically, and the paired tracking difference is **exactly 0.0000%**. Same for the sensor class. The only class where the structural suite moves the contract's control metric is the structural class — which has no deficit to recover. Both suites' per-class recall confirms it: the conventional suite detects actuator and sensor faults at 100% and structural faults at 8.3%.

That last point is the honest shape of the project's control layer, and it is not a new claim — it is Codex's Session-18 artifact read against Codex's Session-20 artifact. Where the structural suite has exclusive information, there is no control headroom. Where there is control headroom, the structural suite has no exclusive information.

### 6. The strongest version of the structural result was already in Codex's rows

Two columns from the same 84 runs, which nobody had put side by side:

| remaining stiffness | mean peak strain | mean tracking deficit |
|---:|---:|---:|
| healthy | 19.2 µε | — |
| 0.75 | 25.0 µε | +0.11% |
| 0.50 | 38.4 µε | +0.08% |
| 0.25 | 72.4 µε | −0.89% |
| 0.10 | 152.8 µε | −2.23% |
| 0.05 | 259.7 µε | −5.00% |

**Monotone in information; monotone the wrong way in control.** At the most severe softening the strain signature is 13.5× the healthy one while tracking is 5% *better* than healthy. That is not a sensing failure and not a weak signal — it is precisely the "diagnostic-only" outcome the Claim Sheet reserved a slot for, now measured across a fifteen-fold stiffness sweep instead of inferred from a single setting. I put this into the generated report, computed from the recorded rows so it regenerates deterministically.

---

## Challenges and how they were handled

- **Deciding whether to edit the gate at all.** Changing which condition advances is a substantive move inside Codex's lane. I resolved it by asking whether the change was data-dependent: it is not — the corrected gate is a pure function of the two predeclared constants, and it tightens rather than loosens. I made the edit, verified the raw data files were untouched by it, stated the counter-argument in the handoff, and named the alternative resolution I would accept.
- **Not letting a correct fix hide an incorrect conclusion.** My units fix moves the selection to a setting my own measurement shows is no better. Reporting only the fix would have implied the advance was now sound. The handoff says explicitly that the fix is necessary and not sufficient, and that a deficit gate is the wrong gate.
- **Keeping externally measured numbers out of the artifact.** My action-efficacy measurements come from my own probe, not from the screen's recorded rows, so they cannot regenerate deterministically from the artifact. They live in the chat handoff and this report; only row-derived figures went into the generated report — the same discipline I asked Codex to hold to last session.
- **A long-running verification budget.** The full grid re-run is ~20 minutes of wall time and the probe another ~10. I ran them in the background and did the static review, the runbook edits and my workspace cleanup while they ran, so nothing waited on nothing.

---

## Files created or updated

**Created**
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md` — the monitoring note for Randy described in §2.
- `agents/Claude/Session Summaries/HumanReport21.md` — this report.

**Updated (my review edits, in Codex's lane, awaiting its owner re-review)**
- `Reproducibility Packet/scripts/screen_fault_tracking_deficit.py` — the units conversion (`required_reduction_pct` / corrected `required_deficit_pct`), a validation guard, the reduction target carried in the decision record, corrected gate wording in the report, and a new generated "What the recorded headroom does and does not license" section.
- `Reproducibility Packet/tests/test_fault_tracking_deficit.py` — a conversion regression, plus the two fixtures that encoded the old gate value (15 → 16 tests).
- `Reproducibility Packet/results/fault_tracking_deficit_screen/summary.json`, `candidate_summary.csv`, `fault_tracking_deficit_report.md` — regenerated. **`tuning_rows.csv` and `assessment_rows.csv` are byte-identical to Codex's committed versions.**
- `Reproducibility Packet/README.md` — Step 14 gains the units explanation and the two bounds; the Current-boundary paragraph updated.

**Updated (mine)**
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — my Session-21 review turn, appended at the verified physical tail (1,562 → 1,673 lines; my header appears exactly once, at line 1,566, and is physically last).
- `agents/Claude/README.md` — workspace index: the chat bullet's accumulated turn-by-turn history was compressed into a purpose statement plus pointers (the detail is fully carried by the transcript and by HumanReports 7–20), the open-review-edits bullet now describes this session's edits, the test count is current, and the new director chat is listed.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 22.

**Deliberately not updated**
- The root Live-Run `README.md`. The public log is append-only by playbook, the current entry is Codex's, and my findings are mid-review-loop. Publishing an unreviewed result would be the wrong move; the next public entry should carry whatever we jointly conclude.
- `agents/Claude/references.md`. No external sources were read this session — it was reproduction and measurement — so there is nothing honest to add.
- Both `.gitignore` files. Reviewed the session's outputs before staging: everything produced is either small tracked result text (JSON/CSV/Markdown) or scratchpad files outside the repository. No new artefact class needs excluding.

---

## Verification summary

- Independent audit: **42/42 checks** against Codex's artifacts, then **42/42** again against the regenerated ones.
- **36 independent simulation arms**; my own tracking metric matches the packet's to **0.000e+00** on every one.
- Full grid re-run at 10 workers against Codex's 8: **both per-arm row files byte-identical** (`bfe0eb66…`, `7cfcc104…`).
- Report regenerates deterministically from its own summary — verified for Codex's version (`e4c7df4e…`) and mine (`c2924e5d…`).
- Full Reproducibility Packet test suite: **199 passed** (198 before my edits). `compileall` clean. CLI `--help` clean. `git diff --check` clean apart from expected line-ending warnings.

---

## Next steps

1. **Codex owner-re-reviews my edits** — the units correction, the regression, the generated report section, the runbook paragraphs, and the three regenerated artifacts. It either approves that exact state or edits and hands back. If it accepts the diagnosis but not the implementation, that is a real disagreement to state rather than absorb; if a specific point has not converged after about two round-trips, it goes to Randy.
2. **The next gate should be achievable source-specific reduction, not deficit.** I proposed three concrete steps in the handoff: re-measure with the compensation cap raised (to find out whether the cap or the physics is binding), screen under the real noisy estimator's severity output rather than a perfect one (the screen's own stand-in yields 6.27% on the same condition — below the bar), and then decide honestly whether the control layer has a live path at all.
3. **No progress report was due.** My next regular one is Session 24; this session closed no phase and wrote no approved Claim-Sheet amendment.
4. **Nothing is frozen.** `config.json` remains unfrozen, and the freeze list gained two items this session: the actuator action's compensation cap, and the severity-estimation quality term that no artifact has yet measured.

---

## A note on where this leaves the project

Two sessions ago the open question was whether the structural recovery action could be re-aimed at tracking. One session ago the answer became: there is nothing to recover on this condition. This session the question moved one step further out — *is there any condition, action, and diagnosis combination on this task that clears the contract's control bar in a source-specific way?* — and the measured answer so far is no: the best source-specific reduction I can produce anywhere in the screened grid is about 4.7%, against a 10% bar.

That is not a failure of the work. It is the Claim Sheet's pre-declared "diagnostic-only" outcome arriving with evidence behind it, at the stage where it is cheap rather than at the confirmatory stage where it would be expensive. The information result stands and is strong: the structural suite sees a fault the conventional suite is blind to, and sees it more loudly the worse the fault gets. What we now know — and can show — is that on this task that fault does not cost the robot anything a controller could win back. Both halves are true, and reporting both is the honest result.
