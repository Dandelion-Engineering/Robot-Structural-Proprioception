# Codex — Summary of Only Necessary Context

**Last completed session:** Codex Session 24, 2026-07-22

**Phase:** Phase 2 — Execution

**Branch:** `main`

**Session-24 starting commit:** `8eb3557` (`Claude Session 24`)

**Expected closeout commit:** `Codex Session 24`

**Shared configuration:** **UNFROZEN**

## Resume here

The active coordination surface is:

`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Its physical last turn is **Codex Session 24**. Read it to EOF before doing work.

The immediate live loop is:

- **Cap-boundary loop: CLOSED.** Claude Session 24 explicitly approved the exact Codex Session-23 corrected state.
- **Actuator class-probability screen: Codex-approved after corrections; Claude owner re-review OPEN.**
- Claude must explicitly approve the exact reviewer-corrected executable, tests, regenerated summary/report, packet Step 17, packet Current-boundary correction, and root Live-Run correction. Silence, downstream use, or handoff is not same-state approval.

Do not begin a new probability or actuator action surface until that re-review is resolved unless the human explicitly redirects the work.

## Authoritative Session-24 result

Claude's new screen sampled the actuator class probability at:

`p = 0.50, 0.60, 0.70, 0.80, 0.90, 1.00`

while holding actuator class, location, severity, common RMS severity uncertainty, and non-abstention fixed.

The reviewer-corrected result is:

- largest sampled gate-clearing S-over-C1 tracking difference: **5.0698636256 percentage points**;
- mean sampled gate-clearing difference: **5.0162118584 points**;
- maximum separate gate-crossing authorization difference: **10.8508760759 points**;
- mean gate-crossing difference: **10.8203657342 points**;
- all four sampled per-seed curves are strictly monotone;
- cap realization at the selected 0.25 remaining-gain condition: **57.5%** of the analytic exact-restoration ceiling.

The first-review correction is load-bearing:

1. The controller constants exactly define the continuous input/multiplier endpoints, but six rollouts do **not** exhaust the nonlinear response between them.
2. The implementation now searches every ordered sampled pair instead of assuming the endpoints are extrema.
3. The complete expected arm grid is now a fail-loud audit condition.
4. The fixture isolates graded probability only. Calibrated probability-gate, abstention, and `severity_uncertainty` crossings remain authorization questions.
5. The common RMS uncertainty is a development fixture choice, not a frozen per-example uncertainty definition.
6. Cap/floor sensitivity remains open because changing the cap changes both recoverable tracking and the flat severity region.

Therefore:

- the six-point graded development result is below the 10-point bar;
- the continuous probability response is **not closed**;
- calibrated authorization is **not closed**;
- the actuator class is **not closed**.

## Independent reviewer evidence

Codex ran an ignored dense audit at p = 0.50 through 1.00 in increments of 0.025:

- 21 acting probabilities per seed;
- four assessment seeds;
- 84 MuJoCo arms;
- every dense curve strictly monotone;
- the maximum remains exactly **5.0698636256 points**.

This strengthens the empirical envelope but is not an analytical proof or a committed approval artifact.

The official 36-arm artifacts were regenerated with 8 workers and independently reproduced to ignored scratch output with 4 workers. All three are byte-identical:

- `summary.json`: `EA377BD0BCCD23CE3D7BDDC17B9C0107F16D9C36D8D2D0AB58AC10506D76AE3A`
- `arm_rows.csv`: `F4E2D43B998BA9CAA46470E7313DBF6D2422D4CFC734E141887206F2751DDB60`
- `actuator_probability_channel_report.md`: `44F39F4B665B7A4EB5DF9274D5A511508FBF1AE179376D8ED7508240C07D414B`

Verification at closeout:

- focused probability screen: **54 passed**;
- full packet: **302 passed**;
- `compileall -q scripts tests`: passed;
- CLI help: passed;
- strict JSON parse: passed;
- no dependency installed.

## Current technical boundary

Keep these evidence lanes separate:

- **Structural information:** on the bounded noisy development fixture, S macro-F1 is 0.995 versus C1 0.704, with structural recall 100% versus 8.3%.
- **Structural action:** the old derate worsens tracking by 18.6%; the inverse-stiffness family improves healthy tracking slightly more than structural tracking and is blocked as a generic nominal retune.
- **Structural headroom:** no tested structural severity reaches the development tracking-deficit gate on this task, even though strain rises strongly.
- **Actuator headroom:** 0.25 remaining gain advances after the deficit/reduction denominator correction.
- **Recorded linear severity route:** the 0.50/cap-2 paired suite effect is small (mean −0.12 points; max absolute 0.52), but arbitrary future read-outs and cap-4/0.25-floor behavior are open.
- **Sampled graded probability:** maximum 5.07 points on the six-point grid.
- **Authorization:** the fixed-fixture gate crossing reaches 10.85 points and remains separate.
- **Control outcome:** action-versus-no-action benefit, healthy false authorization, source specificity, cap/floor sensitivity, sensor-fault recovery, and evaluation-sized paired control remain open.

None of these development screens is validation-sized, confirmatory, a Slot-11 win, or a frozen decision margin.

## Public and packet correction state

The root `README.md` Live-Run log is append-only. Claude's earlier “last/final channel closed” entry remains as history, immediately followed by a dated Codex reviewer correction.

The packet's Step 17 and regenerated report use the narrow sampled interpretation. Its long Current-boundary paragraph still contains the superseded pre-review language but is immediately followed by an explicit reviewer-correction paragraph. Do not quote the stale paragraph without the correction.

## Files changed in Session 24

- `Reproducibility Packet/scripts/screen_actuator_probability_channel.py`
- `Reproducibility Packet/tests/test_actuator_probability_channel.py`
- `Reproducibility Packet/results/actuator_probability_channel/summary.json`
- `Reproducibility Packet/results/actuator_probability_channel/actuator_probability_channel_report.md`
- `Reproducibility Packet/README.md`
- `README.md`
- active Claude–Codex Phase-2 transcript
- `agents/Codex/Progress Reports/Progress Report Session 24.md`
- `agents/Codex/Session Summaries/HumanReport24.md`
- `agents/Codex/references.md`
- `agents/Codex/README.md`
- this continuity file

`arm_rows.csv` is tracked but byte-identical and therefore does not appear in the diff. Reviewer-only dense and reproduction files are under ignored `/tmp/`.

## Next-session instructions

1. Follow `AgentPrompt.md` startup again and read all active transcripts to physical EOF.
2. Verify repository synchronization and inspect any Claude re-review turn.
3. If Claude explicitly approves the exact Session-24 corrected state, close the probability-screen loop.
4. If Claude edits, review the new exact state; reviewer edits reset approval.
5. Preserve the distinction between:
   - an exact input interval;
   - a finite sampled response envelope;
   - calibrated authorization;
   - control outcome.
6. Keep `config.json` unfrozen until the remaining action/controller, calibration, validation, leakage/storage/hash, learned-head, and Phase-3 gates close.
7. Use only `.\venv\Scripts\python.exe`; never use bare `python`.
8. Apply the append-only transcript hard gate before the next chat write.

The next regular Codex progress report is Session 32 unless a phase transition or approved Claim Sheet amendment triggers one earlier.
