# Human Report — Claude, Session 24

**Date and time (recorded at report creation):** 2026-07-22 21:47 PDT
**Phase:** Phase 2 — Execution
**Session type:** Owner re-review closing a loop + new screen + regular-cadence progress report (my session 24)

---

## Summary

Three things happened this session. I closed the open review loop on my cap-boundary screen by genuinely re-reviewing Codex's three corrections and agreeing with all of them — one of which I confirmed by finding the counterexample inside my own data. I then built and measured the **class-probability channel**, the last unexamined route by which the strain suite could still beat the conventional suite on control, and it closed. And I wrote the Session-24 progress report, which was due on the regular cadence.

The headline: **the actuator class is now closed on every channel the recovery action can spend** — detection, classification, severity accuracy, the severity→tracking conversion, and now class probability.

---

## 1. Owner re-review — Codex was right three times, and the third one hurt

Codex's S23 review of my cap-boundary screen made three corrections and handed the edited state back. I re-derived each from the upstream artifacts rather than reading its summary fields (`s24_verify.py`, **40/40 checks**, all figures reproducing to 1e-12), reproduced its reproduction (**248 tests passing**, `arm_rows.csv` byte-identical to my S23 commit), and **approved the same state without editing it. The loop is closed.**

**(a) The uncertainty ranking.** I had reported a leave-one-seed-out "held-out" severity dispersion and claimed it *inverted* the suites' apparent reliability. Codex pointed out the fixed ridge penalty was selected on the same tuning groups the folds hold out, so the number is a **calibration-role diagnostic**, not a disjoint held-out estimate. It recomputed the genuinely disjoint assessment role. Verified: the tuning seeds `{17000…17005}` and assessment seeds `{17100…17103}` are disjoint in the data, and its assessment MAEs equal Step 15's own already-approved recorded fields exactly. Its narrower conclusion — *never hand the in-sample residual to the confidence gate* — is what the data supports.

**(b) "Envelope," not "bound." This is the one that mattered.** I had written that my multiplier sweep bounded what *any* severity read-out difference could be worth. Codex said that was overreach. It is, and the counterexample was in my own `arm_rows.csv`:

| range | span | vs 10 pp bar |
|---|---:|---|
| swept [1.50, 2.00] | 3.8083 pp | below |
| full [1.00, 2.00] | **10.8093 pp** | **above** |

The action's full attainable range starts at no-action, where the reduction is zero by construction. Extend the range to where a read-out can actually go and the span is above the bar, not below it. That wasn't a small overstatement of a true claim — it was false.

**(c) Non-gating audit booleans.** My screen computed seven integrity checks and aborted on one. Codex added a seven-way `require_passing_audit` plus seven parameterized false-field tests. This is the same defect class I had twice caught in *its* work — a check that doesn't gate is decoration — and I shipped it.

**One refinement I contributed but deliberately did NOT edit in.** Codex said the absolute suite ranking is not role-stable. I checked *which statistic* makes that true:

| statistic | C1 | S | better |
|---|---:|---:|---|
| in-sample std | 0.004237 | 0.001951 | S |
| calibration std | 0.006741 | 0.011160 | C1 |
| **assessment std** | 0.008393 | **0.008029** | **S** |
| calibration / assessment MAE | 0.005306 / 0.006472 | 0.009029 / 0.007633 | C1 / C1 |
| calibration / assessment RMS | 0.006897 / 0.008585 | 0.011394 / 0.010183 | C1 / C1 |

**Standard deviation is the only statistic that flips**, because it discards the bias — and S's assessment bias is 2.75× C1's. On every bias-inclusive statistic, both out-of-sample roles agree with each other and with Step 15's approved MAE result. That gives a concrete freeze proposal: **`severity_uncertainty` should be a bias-inclusive RMS, not a residual standard deviation**, because a biased-but-tight estimator passes an std gate it should fail. I carried it forward into the new screen's code rather than spending a third round-trip on an artifact whose numbers don't change.

I also updated two now-stale status phrases in Codex's packet prose ("pending owner re-review"), flagging them in chat rather than editing silently.

---

## 2. New work — the class-probability channel screen

**Files:** [`scripts/screen_actuator_probability_channel.py`](Reproducibility%20Packet/scripts/screen_actuator_probability_channel.py), [`tests/test_actuator_probability_channel.py`](Reproducibility%20Packet/tests/test_actuator_probability_channel.py) (51 tests), `results/actuator_probability_channel/` (3 artifacts), packet **Step 17** + the 17→21 renumbering.

### The structural setup

The recovery controller's actuator branch is, verbatim, `multiplier = 1 + p·(capped − 1)`, and it withholds the action below `p = 0.5`. Two facts make the channel exactly measurable at the deficit screen's **selected** condition (`actuator_gain_remaining_0p25`) rather than at the S23 boundary:

1. **The severity channel is structurally dead there.** `capped = min(1/max(ŝ, 0.25), 2.0)`, so at the recorded cap *every* estimate at or below **0.50** returns exactly 2.0. The true 0.25 sits **24.6×** the recorded severity error scale below that boundary. Verified against the shipped controller across ŝ ∈ {0.01…0.50} — one identical multiplier — with 0.55 leaving the flat region.
2. **The probability channel is closed at both ends by recorded constants** — the gate below, the cap above. So `m = 1 + p`, and the reachable multiplier set is exactly `[1.50, 2.00]`.

That second point is why this is a **reachable-set** span and not an envelope. Codex's correction is what let me state the difference, and it constrains me here as much as it licenses me: if either constant moves, the claim moves.

*(A side observation worth recording: my S23 sweep range of [1.50, 2.00], which I picked as "generously wide," is **exactly** the reachable probability range at that condition. I had already measured the probability channel there without noticing.)*

### The result

| p | 0.50 | 0.60 | 0.70 | 0.80 | 0.90 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|
| reduction vs no-action | +6.11% | +7.17% | +8.17% | +9.14% | +10.00% | +10.82% |

**In the contract's units** (`100·(J_C1−J_S)/J_C1`):

| paired quantity | worst seed | mean | vs 10 pp bar |
|---|---:|---:|---|
| graded — both suites past the gate | **5.0699 pp** | 5.0162 pp | below |
| gate-crossing — one suite withholds | 10.8204 pp | 10.8204 pp | clears |

**⇒ The class-probability channel is CLOSED on the actuator class at the selected condition.** The gate crossing is reported separately and deliberately: one suite authorizing while the other doesn't is a class-call-scale quantity already screened elsewhere, and both suites call this class correctly with one-hot recorded probabilities.

### Codex's open §5 question, answered

It had said the 93.2% realized-versus-analytic ratio was scoped to the 0.50 condition. It does **not** carry:

| condition | deficit | analytic ceiling | realized | realization |
|---|---:|---:|---:|---:|
| 0.50 | 13.11% | 11.59% | 10.81% | **93.2%** |
| **0.25 (selected)** | 23.16% | 18.81% | 10.82% | **57.5%** |

Same direction on all four seeds. The mechanism is structural: at 0.25 exact restoration needs **m = 4.00** and the cap allows **2.00**, so the action is cap-saturated throughout. **`maximum_gain_compensation` is therefore the binding limit on recoverable tracking at the condition Codex's action screen will run on — 42% of the recoverable error is unrecovered.** Flagged, not proposed: raising the cap to 4 would recover more *and* re-open the severity channel this screen closes, so `(cap, floor, probability_threshold)` is a joint surface.

---

## 3. Challenges, and one I created myself

**I nearly shipped a units error — the same class I caught in Codex's work in S21, pointing the other way.** The response curve is reduction-vs-no-action; the contract divides by the *conventional arm*, not the no-action arm. A difference of two reductions is smaller by `1/(1 − r_low/100)`: **4.7097 pp versus the true 5.0162 pp, understating by 6.5%.** I caught it before handing off, added `paired_channel_extremes`, re-ran the screen, and the artifacts now report contract units throughout. The conclusion never changed; the number the bar is written in did.

**My own prose scan caught an overreach pattern.** The self-audit greps the generated report for the phrasing Codex had just corrected, and it fired on a sentence of mine: "Any read-out that lands anywhere in the plausible range commands an identical multiplier." Replaced with the constant-derived bound and the error-scale margin — *plausible* is a judgement, *0.5000* is a number.

**The dry-run discipline paid off again.** `s24_dryrun.py` exercised the entire post-rollout path on synthetic rows in the exact returned shape — **70/70 checks** — before any simulation ran.

---

## 4. Verification performed

- Full packet **299 passed** (248 + 51 new). `compileall` clean, CLI help clean, strict JSON, no NaN/Inf.
- **Two independent 8-worker runs → byte-identical `arm_rows.csv`.**
- **CRN reuse checked, not assumed:** 8/8 reference arms reproduce the deficit screen's committed `J_5s` at exactly **0.000e+00**, and `main()` aborts otherwise.
- **The gate probe (p = 0.49, still the unique argmax) is bitwise identical to no-action on all four seeds** — the gate discontinuity is measured, not inferred.
- Seven fail-loud gates, all seven parameterized-tested false, plus a missing-key test so a dropped condition cannot default-pass.
- `m = 1 + p` verified to 2.2e-16 on the real rollouts *and* independently against the shipped `GainScheduledRecoveryController`.
- Self-audit **55/55** (`s24_selfaudit.py`), recomputing every derived table from `arm_rows.csv` rather than reading summary fields.

---

## 5. Decisions made

1. **Approve Codex's corrected state same-state rather than edit.** All three corrections are right and the state is better than what I handed off. Editing would have cost a fourth round-trip on an artifact whose numbers don't move.
2. **Carry the RMS refinement forward into new code rather than into the closed artifact.** This is the project's forward-propagation rule applied to a refinement rather than a defect.
3. **Screen at the *selected* condition, not the boundary condition.** It is where Codex's action screen will run, and it answers its open question at no extra rollout cost.
4. **Report the gate discontinuity separately from the graded channel.** Collapsing them would let an authorization difference masquerade as a probability-precision result.

---

## 6. Files created or updated

**Created**
- `Reproducibility Packet/scripts/screen_actuator_probability_channel.py`
- `Reproducibility Packet/tests/test_actuator_probability_channel.py`
- `Reproducibility Packet/results/actuator_probability_channel/{summary.json, arm_rows.csv, actuator_probability_channel_report.md}`
- `agents/Claude/Progress Reports/Progress Report Session 24.md`
- `agents/Claude/Session Summaries/HumanReport24.md` (this file)

**Updated**
- `Reproducibility Packet/README.md` — new Step 17, 17→21 renumbering, two stale cross-references, Step 2 coverage line, Current boundary, and the two stale "pending owner re-review" markers
- `README.md` (root Live-Run) — running-log entry for the closed channel
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — two turns (+96/−0 and +175/−0, both at the verified physical tail)
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`

---

## 7. Next steps

1. **Read Codex's review of the probability-channel screen** — first job next session. Approve same-state, or genuinely re-review its edits and diagnosis.
2. **The actuator class has no unexamined channels left.** Any future claim that the strain suite helps control on this class has to come from somewhere other than the action's own parameters.
3. **Codex's actuator action screen** is the remaining control work; this screen removed one term from its design and flagged the cap as its binding limit.
4. **Still blocked, correctly:** the learned attribution rungs (need PyTorch CUDA + frozen config + confirmatory data), the deployable-loader leakage test, and the evaluation driver.

**Nothing is frozen. `config.json` remains unfrozen and every config hash is `dev-` prefixed.**

— Claude
