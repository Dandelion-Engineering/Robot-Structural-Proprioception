# Human Report 8 — Claude

**Date/time:** 2026-07-17 16:21 PDT

**Agent:** Claude · **Session:** 8 · **Project phase:** Phase 2 — Execution (both open review loops closed; diagnosis-estimator detection/abstention front + window contract built on the causal seam; config freeze still pending; learned attribution rungs and their training remain post-freeze)

## Summary

This session did three things: closed the two review-cycle loops Codex handed back at the end of Session 7 (the evaluation core and the online interface) with genuine owner re-review and same-state approval; built my next Phase-2 deliverable, the **diagnosis-estimator lane** (schema §D) — its output contract, past-only windowed front-end, interpretable detection-and-calibrated-abstention rung, allowlisted oracle interface, and the online-seam adapter; and, because it is a per-agent session-8, wrote the regular director progress report in addition to the normal session work.

The re-review was substantive, not a rubber stamp. Codex's four evaluation-core corrections and the online-interface edits were all correct in both diagnosis and implementation; I verified the most consequential one (the OOD operating point) directly against the Claim Sheet rather than accepting Codex's read, reproduced the full test suite (59 passing at session start), and ran a standalone 17-check script exercising each load-bearing claim of both loops before approving. Both loops are now closed at the same state Codex approved.

The estimator lane is the *consumer* of the causal online seam and the *producer* of the §D estimator outputs the metrics score, so building it also let me propose the frozen windowing constants `W` and `stride`, which fill the estimator column of the config-freeze table. I made a deliberate scope decision: I built the parts that can be honestly built and tested now (detection, calibrated abstention, the interface, the window contract) and did **not** build the learned "which fault is it" attribution head or the RMA-style latent as untrained neural shells, because they require the frozen config and confirmatory data to train — standing them up now would be capacity we cannot yet use and a guess dressed as a result. They are specified against the same front-end and are the next build once the config freezes.

The packet went from **59 to 74 passing tests**. Python compilation passes. No confirmatory configuration was created; `config.json` remains deliberately unfrozen; all current data remain development-only.

## What was accomplished

1. **Completed the ordered context pass.** Read `AgentPrompt.md` and `Project Details/Project Details.md` in full; my continuity summary; every Claude-including chat (the three concluded summaries and the active Phase-2 transcript); Codex's Human Report 7 and its continuity; the in-force schema; the Claim Sheet (Slot 7 / line 118 specifically for the OOD adjudication); and the review-cycle and research-progress-report playbooks. Reproduced the clean 59-test baseline before touching anything.

2. **Closed the evaluation-core review loop (same-state approval).** Re-reviewed Codex's four Session-7 corrections against Claim Sheet Slot 7 and schema §G, not just against the tests:
   - **Truncated-`J_5s` guard** — correct; a trace ending before `onset+window` was silently scored, now fails loud with a uniform-grid + exact-endpoint check.
   - **Tie-safe risk–coverage** — correct; emitting only tie-group endpoints makes the curve invariant to within-tie input order.
   - **OOD operating point** — correct, and I confirmed it against the contract: **Claim Sheet line 118 specifies false-acceptance at 95% unknown-detection *sensitivity*.** My Session-7 `false_accept_at_id_acceptance` used the wrong 95% (in-distribution acceptance). Codex's `unknown_threshold_at_sensitivity` (validation) → frozen threshold → `ood_false_acceptance_rate` (held-out) is right, and splitting calibration from held-out prevents the operating point leaking into the confirmatory result.
   - **Crossed pair×seed bootstrap** — correct; a trained seed is evaluated across all pair units, so seed is a global crossed axis, not nested. Resampling pair rows and seed columns independently and applying the same sampled seed columns across all sampled pair rows preserves both variance sources and the C1/S pairing.

3. **Closed the online-interface review loop (same-state approval).** Re-reviewed the one-step observable adapter (`schema_types.py`), `OnlineSensorSession` + the batch-wrapper refactor (`sensor_model.py`), and `run_online_rollout` (`online_loop.py`). Confirmed the causal ordering (the decision uses `plant.data.time` before the advance; the observation is emitted after), the CRN consistency, the `qd_valid = q_valid & prev_q_valid` fix, the `control_effort`-upstream current proxy, and the bounded `available_record` window. One authoritative pathology path (the batch wrapper now feeds the online session step by step).

4. **Ran independent verification (reproduced evidence, did not trust it).** Full packet **59 passed** on my machine, plus a standalone script (`s8_reverify.py`, 17 checks): `j_5s` raises on a 2 s trace; risk–coverage identical under a tied-score shuffle and emits only tie-group endpoints; the OOD threshold detects ≥95% of validation OOD and false-acceptance is computed on held-out at the frozen threshold; the crossed bootstrap excludes zero on a clear S>C1 signal, includes zero on a null, and rejects a ragged grid; and, on a real short MuJoCo online rollout, shared C1/S channels are bitwise-identical under CRN, C1 gauges are all-NaN, and the 2 ms gauge is withheld one control step while the zero-latency encoder is delivered immediately. All 17 passed.

5. **Built the diagnosis-estimator lane** (`utils/estimator.py` + `tests/test_estimator.py`):
   - **`EstimatorOutput` / `EstimatorTrace`** — the §D output contract as validated carriers, in the canonical class order matching `metrics.SOURCE_CLASS_ORDER`, with run-level reductions and §E-shaped stacking.
   - **`WindowFeatureExtractor`** — the past-only window front-end, suite-agnostic by construction (fixed shapes over the full 18-wide registry for C0/C1/S): a `[W, D]` tensor with a validity mask (no silent imputation) for the learned rungs, and a summary-feature vector for the interpretable rung.
   - **`WindowNoveltyDetector`** — the interpretable detection + calibrated-abstention rung. A top-k sparse-change statistic standardized against a leave-one-out healthy reference (thresholds in sigma-above-healthy), persistence-latched detection time, and an honest healthy-vs-not simplex that abstains on the fault type and makes no source attribution.
   - **`OracleInterface`** — the separate allowlisted §D oracle, reading privileged `PlantStepState` explicitly, never importable by a deployable loader.
   - **`EstimatorCommandPolicy`** — the `run_online_rollout` seam adapter that accumulates the §D trace and runs the estimator every `stride` decisions with a zero-order hold; the recovery command is injected (Codex's lane) and defaults to passive.
   - **`RECOMMENDED_WINDOW`** = `W=512`, `stride=8`, with rationale.

6. **Closed a contract gap in my own earlier work.** Claim Sheet line 118 pre-registers "coverage at a pre-registered 5% selective-error ceiling," which `metrics.py` did not render (only its dual, `selective_risk_at_coverage`). Added `coverage_at_risk(...)` with a hand-computed test.

7. **Proposed `W`/`stride`** and updated the config-freeze table in the chat: the estimator column is now filled; the remaining open fields are Codex's plant-side ones (diagnostic envelope, contact/safety widths), the shared pilot-informed grids, and the joint sanity-check of the non-load-bearing sensor constants.

8. **Wrote the Session-8 progress report** (`Progress Reports/Progress Report Session 8.md`) at the Accessible-Piece bar — the due per-agent-session-8 report.

9. **Session closeout:** posted my Session-8 chat turn at the verified physical tail (via append, honoring the standing monitoring duty), updated my references ledger, added the Live-Run README running-log line, updated both READMEs, rewrote the continuity summary, and committed/pushed.

## Important decisions and reasoning

### 1. Build the estimator's honest front, specify (don't fake) its learned head

The estimator's attribution ladder is detect → classify-or-abstain → localize/size → use. Detection and the abstention/unknown layer can be built and tested now with a well-understood, dependency-light method (novelty detection against a healthy baseline, standard in structural health monitoring). The *naming* rung (structure vs. actuator vs. sensor) requires supervised training on labeled runs — which do not exist until the config freezes and confirmatory data is generated. Building an untrained neural classifier now would violate the project's "don't build around absent evidence" discipline and the efficiency standard (capacity we cannot yet use). So I built the detection/abstention front, the output contract, the window front-end, and the seam adapter, and I *specified* the learned temporal-attribution net and the RMA-style latent against that same front-end with the same `W`. This also keeps the honest boundary visible: the detector abstains on the fault type rather than inventing an attribution.

### 2. Verify the OOD operating point against the contract, not against Codex's word

Genuine owner re-review means checking the diagnosis, not deferring to the reviewer. The OOD correction hinged on which "95%" the contract meant, so I read Claim Sheet line 118 directly: it fixes false acceptance at 95% *unknown-detection sensitivity*. That confirmed my Session-7 implementation was wrong and Codex's correction was right. This is the kind of thing that must be checked at the source, because both agents can otherwise converge on a plausible-but-wrong shared reading.

### 3. A self-calibrating detector, in sigma-above-healthy units

My first detector used a raw RMS-over-all-features novelty score with absolute thresholds. That failed on two counts: a localized fault (an encoder bias touches a few of ~90 features) is diluted by the many unaffected features, and the healthy baseline of a many-feature score is not near zero, so absolute thresholds are meaningless. I reworked it to a top-k sparse-change statistic (sensitive to a localized change) standardized against the healthy score distribution estimated leave-one-out at fit time, so thresholds read in interpretable sigma-above-healthy units and are robust to the feature dimensionality — the same discipline as freezing the OOD threshold on healthy calibration. This surfaced during testing and made the rung genuinely honest rather than merely passing.

### 4. Keep lane boundaries crisp

My detection rung is an observation-statistics novelty gate; Codex owns the interpretable *residual/linear-sysID* baseline (a physics-model residual in the plant lane). I flagged the distinction in code and in the chat so we do not build the same thing twice. Likewise, the recovery controller stays Codex's lane — my seam adapter injects it as a callback and defaults to a passive command, so the estimator can drive the loop before the controller exists without my claiming the controller.

### 5. Do not install PyTorch this session

The learned rungs need PyTorch, and the RTX 5060 Ti is a Blackwell (sm_120) card that needs a recent CUDA wheel. Since I cannot train anything before the config freeze, installing a possibly-fragile CUDA build to ship an untrained forward pass would spend the session's risk budget for no honest deliverable. Torch install (with a real sm_120 kernel check, not just `cuda.is_available()`) is the first step of the post-freeze learned-rung build.

## Challenges and how they were handled

- **The novelty detector was too trigger-happy at first.** A fresh healthy window scored as "changed" because the raw statistic diluted localized faults and had a non-zero healthy baseline. Fixed by the top-k sparse-change statistic and the leave-one-out sigma standardization above; also fixed a test that had wrongly fit the healthy reference across different trajectory phases (mixing operating conditions), which I corrected to fit on noise realizations of one trajectory.
- **A composition test asserted an unrealistically clean OOD separation.** My honest detector gives known faults and an OOD compound similar novelty scores (both are "not healthy"), so AUROC was not 1.0. Rather than weaken the detector, I fixed the test to reflect reality — the OOD run carries a distinctly higher score — since the test's purpose is to prove the estimator's §D outputs feed the metrics scorer, not to claim perfect OOD separation.
- **A logistic overflow warning.** The healthy-probability logistic overflowed `exp` for very novel windows (harmless — the result is 0 — but noisy); clamped the exponent.
- **Chat append quoting.** A heredoc append tripped on the message's apostrophes/backticks; I wrote the turn to a temp file and appended it with `cat >>`, which also guarantees physical-tail placement (the robust guard against the anchor-matching misplacement the team has been watching for). Verified the tail lands with my turn.

## Files created or updated

Created:

- `Reproducibility Packet/scripts/utils/estimator.py` — the diagnosis-estimator lane (§D output contract, windowed front-end, detection/abstention rung, oracle interface, seam adapter, `W`/stride recommendation).
- `Reproducibility Packet/tests/test_estimator.py` — 15 tests: output-contract validation, suite-agnostic front-end shapes and NaN-safety, detection/abstention behaviour, oracle ceiling, online-seam integration on the real cable plant, and estimator→metrics composition.
- `agents/Claude/Progress Reports/Progress Report Session 8.md` — the due director progress report (Accessible-Piece bar).
- `agents/Claude/Session Summaries/HumanReport8.md` — this report.

Updated:

- `Reproducibility Packet/scripts/utils/metrics.py` — added `coverage_at_risk` (Claim Sheet line 118).
- `Reproducibility Packet/tests/test_metrics.py` — added the `coverage_at_risk` test.
- `Reproducibility Packet/scripts/utils/__init__.py` — documented the new `estimator` module.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/…- Active.md` — my Session-8 turn: same-state approval of both loops, independent verification, estimator delivery, `W`/stride proposal, `coverage_at_risk` note, updated config-freeze table.
- `agents/Claude/references.md` — Phase-2 Session-8 subsection: estimator-lane source→implementation mapping and forward corrections (OOD operating point; `coverage_at_risk`).
- `README.md` (Live-Run) — one running-log entry for the estimator front + the evaluation-core review.
- `agents/Claude/README.md` — workspace map: estimator lane, both loops closed, 74-test count, progress-report cadence.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten for Session 9.

## Verification performed

- Baseline before any change: `pytest Reproducibility Packet/tests` — **59 passed**.
- Independent re-review script `s8_reverify.py` — **17/17 checks passed** (both loops).
- Full packet suite after the estimator lane + metric addition — **74 passed**.
- `compileall` over `scripts` and `tests` — passed.
- `.gitignore` review — the packet's rules already ignore generated bytecode, caches, and `*.npz`; no new development artifact needs an ignore rule; scratchpad files (`s8_reverify.py`, `s8_chat_turn.md`) live outside the repo.

## Progress-report and cadence note

Claude Session 8 is a per-agent every-eighth-session trigger, so the regular director progress report was written in addition to the normal session work. No phase transition or Claim-Sheet amendment was closed this session, so no extra event-triggered report is due. My next regular progress report is Session 16.

## Next steps / pending actions

1. **Build the learned attribution rungs** (my lane): the matched temporal-attribution net and the RMA-style latent, sharing the `WindowFeatureExtractor` front-end and the `EstimatorOutput` contract. Install the PyTorch CUDA build first (verify an sm_120 kernel actually runs, not just that CUDA loads; pin immediately). Architecture and forward/backward can be built and shape-tested now; **training waits on the config freeze and confirmatory data** — no performance claims before then.
2. **Converge the config freeze** with Codex: my estimator column is filled (`W`/stride proposed). Remaining: Codex's diagnostic duration/envelope and contact/safety widths/thresholds; the shared pilot-informed severity/onset grids; and the joint sanity-check of the non-load-bearing sensor constants. Do not freeze a partial config. Check Codex's reply to my Session-8 chat turn.
3. **Post-freeze, before pilot/confirmatory generation** (deferred, mine): the §D deployable-loader leakage test and the whole-trajectory/fault-setting split audit; both must fail the build if a deployable loader can reach identity/privileged/labels/other-suite arrays.
4. **Cross-review:** read Codex's next human report and the recovery-controller/plant-side work it points to when it lands, and respond where called for.
