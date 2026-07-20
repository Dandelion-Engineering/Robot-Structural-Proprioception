# Human Report 11 — Codex

**Current Date and Time:** 2026-07-20 11:35 PDT

**Agent:** Codex · **Session:** 11 · **Project phase:** Phase 2 — Execution

---

## Summary

This session closed the prior estimator/safety review gate, built and ran the first
deployable noisy healthy-reference pilot, preserved its initial threshold-calibration
BLOCK, and then ran a separately seeded prospective follow-up that advanced a concrete
coefficient-reference convention to Claude for estimator-owner review.

Claude Session 11 genuinely re-reviewed Codex Session 10's cosine/sine/amplitude feature
and safety-pairing guard and explicitly approved the exact edited state. That combined
loop is closed. The pilot therefore used the retained coefficient pair on causal noisy
`ObservedRecord` windows rather than promoting the clean 2.22× privileged
fault-minus-healthy screen as a deployed margin.

The new `run_noisy_reference_pilot.py` keeps the estimator lane boundary intact: it is a
pilot instrument, not the permanent estimator rung. It generates matched C1/S
observations, sweeps task/probe scale, W, stride, and onset-to-decision alignment, fits a
healthy coefficient reference and pilot-only fault-shape centroids on calibration sensor
seeds, and evaluates false alarms, per-fault detection, and prototype attribution on
disjoint held-out seeds. The tested convention is a scheduled phase-reset one-cycle
0.8 Hz probe; the first global stride-grid decision at or after probe end; a healthy
reference conditioned on task/probe, W, and decision lag; and a
dimension-normalized, healthy-standardized Euclidean distance on retained cosine/sine
coefficients. W=512 is deliberately preserved as an inert sub-cycle negative control.

The broad sweep used eight calibration and twelve held-out seeds per class/suite. Its
closest cell — task 0.50, probe 0.05 N, W=640, stride=8 — retained strong S-side signal:
100% minimum per-fault detection and 100% prototype attribution across the three tested
alignments, versus 8.3% matched-C1 minimum detection. But S healthy false alarms were
8.3% pooled and 16.7% in the worst alignment, above the 5% development screen. The
result is preserved as a BLOCK; the threshold was not retuned on those held-out rows.
With only eight healthy calibration values, the higher-method 99th percentile is just
the maximum leave-one-out score and cannot resolve the requested tail.

A separate prospective follow-up then used new non-overlapping seeds, with 32 healthy
calibration and 48 held-out seeds per class/suite, without changing the statistic or
threshold rule. The advancing setting is task 0.50 / probe 0.05 N, W=768, stride=16:

- S worst per-fault detection across tested alignments: **97.9%**;
- S worst prototype attribution: **100%**;
- S healthy false alarms: **0.7% pooled**, **2.1% worst alignment**;
- matched C1 minimum fault detection: **0%**;
- no healthy/structural/actuator development safety flag.

This advances W=768 / stride=16 only as a development proposal for Claude's permanent
coefficient-distance reference rung. It does not freeze W, stride, threshold, probe,
fault grids, sensor constants, or `config.json`; it is not the confirmatory C1-vs-S
result. Unscheduled phase drift, probe-band thermal interference, learned attribution,
recovery control, and contact-enabled cases remain open.

## What was accomplished

1. **Completed the AgentPrompt startup and context-first chat pass.** Read all of
   `Project Details/Project Details.md`, Codex continuity, every Codex-including chat
   summary, and the complete active Phase-2 transcript before replying.

2. **Performed the required cross-review.** Read Claude Human Report 11 and the exact
   current repository state. Confirmed Claude's genuine same-state approval closed the
   Session-10 cosine/sine/amplitude and safety-pairing loop; no further estimator or
   metric edit was required.

3. **Read the required playbooks.** Read `Playbooks/review-cycle.md` before handing the
   new pilot artifact into review and `Playbooks/live-run-readme.md` before updating the
   public heartbeat.

4. **Reproduced the handoff baseline.** Ran the complete packet suite before pilot work:
   **102 passed**.

5. **Built a portable pilot CLI.** Added
   `Reproducibility Packet/scripts/run_noisy_reference_pilot.py` with `argparse`,
   fail-loud grid validation, causal delivered-window masking, shared production
   coefficient extraction, healthy-reference fitting, disjoint calibration/evaluation
   seeds, prototype nearest-centroid attribution, CSV/JSON/Markdown artifacts, and a
   bounded multi-process sensor-seed path.

6. **Kept C1 genuinely gauge-free.** The pilot generates S once per source/seed and
   projects C1 by removing gauge values, masks, measurement times, availability times,
   and latency metadata. A focused regression compares that projection to an independently
   generated C1 `SensorModel` record and proves every value/mask/timing array and suite
   flag is bit-for-bit identical under CRN.

7. **Added five pilot regressions.** Tests pin global stride alignment, causal withholding
   of the latest latent gauge row, W=512's all-zero synchronous negative control,
   W=640's live coefficient path, exact C1 projection, and calibration-only
   reference/held-out scoring behavior.

8. **Ran and preserved the broad pilot BLOCK.** Swept C1/S over task scales {0.4,0.5},
   probes {0.025,0.05 N}, W {512,640,768}, stride {4,8,16}, and onset offsets
   {0,5,11}. Wrote the complete result to
   `Reproducibility Packet/results/noisy_reference_pilot/` without changing the
   threshold after observing its false alarms.

9. **Ran the prospective calibration follow-up.** Used new seeds (base 5000), 32
   calibration and 48 held-out seeds per class/suite, the already-selected
   task-0.50/probe-0.05 N candidate, and the same statistic/threshold rule. Wrote the
   advancing result to
   `Reproducibility Packet/results/noisy_reference_pilot_threshold_followup/`.

10. **Made the packet runbook self-contained.** Added both exact commands, outputs,
    interpretation, and honesty boundaries to `Reproducibility Packet/README.md`;
    corrected the stale A1 state and renumbered later steps.

11. **Updated the public live-run heartbeat.** Appended one lean 2026-07-20 entry to the
    root `README.md`: the pilot first exposed under-sized calibration, then a separately
    seeded follow-up advanced a reference convention. The entry states the bounded
    figures and explicitly says no research result or config freeze follows.

12. **Handed the exact state to Claude.** Appended the Session-11 message at the verified
    physical tail of the active Phase-2 chat using a unique multi-line anchor, re-read
    the tail, and confirmed the header appears once and physically last. Explicitly
    approved the pilot script, tests, both result directories, and documentation, leaving
    Claude's genuine review open.

## Important decisions and reasoning

- **Use a calibration reference, not a counterfactual trajectory.** A deployable
  detector cannot observe the faulted robot and a matched healthy robot simultaneously.
  The pilot therefore compares the live coefficient vector to a healthy calibration
  model conditioned on the known scheduled probe and decision alignment. This is the
  smallest honest bridge from the clean mechanics screen to a deployable statistic.

- **Retain phase and use the joint vector.** The pilot consumes the already-approved
  cosine/sine pair and computes a joint standardized distance. It does not fall back to
  amplitude difference or generic independent feature z-scores, both of which can lose
  the screen's phase-bearing separation.

- **Preserve the first false-alarm BLOCK.** The eight-seed sweep showed excellent fault
  signal but insufficient healthy-tail calibration. That is a method finding, not a
  nuisance to tune away. The original held-out rows remain untouched, and the follow-up
  used a new seed range with only sample size changed.

- **Advance W=768 / stride=16 only to owner review.** The follow-up cleared the declared
  development false-alarm and minimum-detection screens across all tested alignments, but
  those values are not validation-frozen and the prototype centroid is not the headline
  learned head. The correct next state is a reviewed estimator implementation, not a
  config freeze or a success claim.

- **Keep W=512 as an executable negative control.** The production extractor emits no
  synchronous coefficient before one full period is available. Keeping W=512 in every
  result proves the pilot is using the actual feature gate rather than silently computing
  an off-contract partial-cycle statistic.

- **Parallelize independent seed work without changing semantics.** A first full attempt
  hit the shell command's two-minute timeout before writing artifacts. Instead of reducing
  the plant resolution or grid, the pilot now distributes independent source/seed cells
  across four processes. The mechanics, random seeds, coefficient functions, and outputs
  are unchanged.

## Challenges and how they were handled

- **The first full command timed out.** The shell wrapper killed the first serial run at
  two minutes. No result directory had been written, so no partial artifact was promoted.
  A four-worker `ProcessPoolExecutor` was added around the independent sensor-seed work,
  with a serial path retained for deterministic focused testing. The complete broad grid
  then finished in about 211 seconds.

- **Small calibration made a 5% tail unresolvable.** The apparent near-pass was not a
  reason to relax the screen. The broad BLOCK was recorded, then a prospective larger
  calibration/evaluation run used new seeds and the exact same threshold rule.

- **Efficient C1 generation risked a metadata leak.** The first projection copied S gauge
  timing metadata even though values/masks were removed. A strengthened regression caught
  the mismatch against the real C1 path. The projection now removes unavailable timing
  metadata too and is exactly equal to native C1 output across every registry field.

- **A generated report initially described the highest-signal cell rather than the
  eligible advancing cell.** The report selector was corrected to use the actual
  recommendation when a cell clears the screen and only use the closest cell on BLOCK.
  The numeric JSON/CSV evidence was unchanged, and both reports were regenerated from the
  preserved rows.

## Files created

- `Reproducibility Packet/scripts/run_noisy_reference_pilot.py`
- `Reproducibility Packet/tests/test_noisy_reference_pilot.py`
- `Reproducibility Packet/results/noisy_reference_pilot/summary.json`
- `Reproducibility Packet/results/noisy_reference_pilot/pilot_results.csv`
- `Reproducibility Packet/results/noisy_reference_pilot/pilot_aggregate.csv`
- `Reproducibility Packet/results/noisy_reference_pilot/noisy_reference_pilot_report.md`
- `Reproducibility Packet/results/noisy_reference_pilot_threshold_followup/summary.json`
- `Reproducibility Packet/results/noisy_reference_pilot_threshold_followup/pilot_results.csv`
- `Reproducibility Packet/results/noisy_reference_pilot_threshold_followup/pilot_aggregate.csv`
- `Reproducibility Packet/results/noisy_reference_pilot_threshold_followup/noisy_reference_pilot_report.md`
- `agents/Codex/Session Summaries/HumanReport11.md`

## Files updated

- `Reproducibility Packet/README.md`
- `README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

No dependency or external source was added; `requirements.txt` and
`agents/Codex/references.md` are unchanged.

## Verification performed

- Pre-work handoff baseline: **102 passed**.
- Current full packet: **107 passed**.
- `compileall` over packet scripts: passed.
- Pilot CLI `--help`: passed.
- Broad pilot: 216 suite/window/stride/onset rows, complete JSON/CSV/Markdown artifacts,
  no NaN/Infinity JSON tokens.
- Prospective follow-up: 54 suite/window/stride/onset rows, complete artifacts, no
  NaN/Infinity JSON tokens.
- W=512 negative control: all synchronous vectors zero.
- Projected C1 vs native C1: bit-for-bit equality for values, masks, all timing metadata,
  and suite flags.
- All generated plant records used by advancing cells: no development safety flag.
- `git diff --check`: clean (line-ending conversion warnings only).
- Active-chat tail: Session-11 header appears exactly once and the transcript ends with
  the new Codex signature.

## Next steps / pending actions

1. **Claude pilot review:** genuinely review the pilot script, tests, broad BLOCK,
   prospective follow-up, and reference/alignment convention; explicitly approve the
   exact state or edit and hand back.
2. **Claude estimator lane:** if the convention is approved, implement the permanent
   coefficient-distance healthy-reference rung against W=768 / stride=16 as a pilot
   proposal, keeping final thresholds validation-frozen and config open.
3. **Threshold and fault-grid gates:** establish validation-sized healthy calibration,
   severity/onset grids, and class/abstention/selective/OOD thresholds without reusing
   pilot held-out rows.
4. **Codex plant lane:** continue the interpretable residual/linear-system-ID baseline
   and recovery controller; implement MuJoCo endpoint-contact extraction before any
   optional-contact pilot.
5. **Shared freeze gates:** jointly sanity-check the non-load-bearing sensor constants;
   complete leakage, whole-trajectory/fault-setting split, role-hash, and storage audits;
   then freeze/hash the full schema/config before confirmatory generation.

The next regular Codex progress report remains Session 16; this session closed no phase
and approved no Claim-Sheet amendment.
