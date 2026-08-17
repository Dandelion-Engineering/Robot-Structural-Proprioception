# Human Report — Codex Session 149

**Current date and time:** 2026-08-17 13:10 PDT (measured with the shell immediately before closeout writing)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

This session completed the required general recent-work review of Claude Session 149's
third partial Step-4b-ii-b build. Claude corrected the false Session-148 claim that the
fixture's `0.040 s` window was maximal, made its intended row-16 interpretation explicit,
and added read-order row 18's coherent centerline derivation and distal-point check.
Rows 19–21, the audit-hook observer, bundle/output/CLI wiring and the two-pass mutation
sweep remain unfinished. There is still no stable candidate, Review Card, subject chat or
formal approval.

The row-18 implementation itself follows the approved design's fact ownership: row 5
continues to authenticate the tolerance source and bind its value, while row 18 calls the
shared dependency-light forward map and checks the authenticated tip without importing
MuJoCo or inventing a tolerance. The corrected window test now measures the real boundary:
`0.040 s` and `0.042 s` close, while `0.044 s` refuses.

I found two blocking forward corrections that the finished candidate must resolve before
handoff. Both are contract gaps that the green aggregate suites do not exercise.

1. **The geometry source's `model_id` is never joined to the authenticated config.** The
   approved Step-4a design says `render_geometry.source` hashes the producer and *echoes
   the config's `model_id`*. The adapter authenticates the config and hashes the named
   producer, but nothing compares
   `record.render_geometry.source.model_id` with
   `config.document["values"]["plant"]["model_id"]`. An isolated end-to-end probe changed
   only the record's geometry `model_id` to `not-the-config-model`; rows 1–18 accepted,
   returned one case and reported the contradictory values side by side. The finished
   candidate must make that equality fail closed and pin it with an end-to-end test.
2. **The new row-16 “time only” ruling contradicts the live producer on both axes.** The
   schema declares estimator `step` in units of `control_step_index`.
   `run_online_rollout` calls the command policy with `step_index` from
   `range(n_steps)`, and `EstimatorCommandPolicy` persists that exact value in every
   `EstimatorOutput`; therefore a faithful trace uses `0 <= step < T`, and the new test
   that deliberately accepts `step == T` pins an impossible producer state. Conversely,
   the policy emits its first decision at step 0 / time `0.0 s` before the first plant
   advance, while `CablePlant` records its first playback sample after the advance at
   one control interval. The current lower time bound uses
   `playback_t_s[0]`, so a live-shaped isolated probe with first playback sample
   `0.002 s` refused the faithful step-0 / time-0 decision as outside
   `[0.002, 0.064] s`. The finished candidate must bind estimator steps to the real
   control-step domain and define the time containment against the decision/display
   chronology without rejecting the pre-step initial decision.

No project implementation byte was edited. Claude owns the unfinished build, and these
findings propagate forward through this report and the completely rewritten Codex
continuity. They are not a Review Card round and do not reopen the historically approved
Step-4b-ii-a blobs.

## Exact state reviewed

Claude Session 149 is commit `47df02fa5bc7c93281d7ca1dc189133b050f94cd`.
The two current owner-work files authenticate exactly:

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — Git blob
  `88ea30e753d24e295c18e0175983224cb0c8f88c`, raw SHA-256
  `d1ac714b7511804253590824b20745f409ab7d5e7d8203239289383816b1b035`,
  136,290 bytes / 2,922 LF / 0 CR;
- `Reproducibility Packet/tests/test_connection_adapter.py` — Git blob
  `7fde611f7ef1c65be72861122496623ec90b3fae`, raw SHA-256
  `d0f42d5b9b7d55ce6203d1f96a3b592e153d0f00a339d80b148aa53926130b17`,
  171,732 bytes / 4,180 LF / 0 CR.

Git reproduces Claude's Session-149 `+214/-7` module delta and `+448/-23` test delta
from Codex Session 148. These are unapproved Step-4b-ii-b owner bytes; the exact
Step-4b-ii-a approvals remain historical states and are not transferred to them.

## Review evidence

### Row 18 and the corrected fixture window

I read the complete Session-149 report, the updated build plan through Appendix C, the
approved Step-4a design's geometry/read-order sections, the module and test deltas, the
shared centerline derivation and coherent fixture, and the live estimator/online-loop/
plant contracts needed to resolve the timing claim.

The row-18 accept path remains synthetic and dependency-light. It installs the coherent
plant and geometry-validation bytes over the temporary contract harness, regenerates the
moved identities, derives both arms through `utils.centerline_geometry`, freezes the
resulting arrays and carries the measured distal deviations without computing a
cross-arm scalar. A perturbed tip carried consistently with its tracking error reaches
row 18 and refuses with `X_GEOMETRY_UNSUPPORTED`, which is the intended seam.

The fixture-window correction is accepted as accurate context, not as formal approval.
The test now drives all three values and the prose explicitly says `0.040 s` is the
largest whole multiple of `0.01 s` strictly inside the measured `0.042 s` bound, not the
maximum itself.

### Adversarial probe 1 — unbound geometry model identity

The approved design's section 3.5 states that the geometry source echoes the config's
`model_id`. Current source search found no consumer of
`record.render_geometry.source.model_id` after parsing. In a fresh temporary harness I
installed the coherent fixture but changed only the serialized geometry source to
`not-the-config-model`. The exact result was:

```text
ACCEPTED
record_model_id=not-the-config-model
config_model_id=mujoco-cable-rod-development-candidate
cases=1
```

The producer digest, coherent derivation and distal comparison all remained valid, so
the gap is specifically the missing identity join rather than a malformed fixture.

### Adversarial probe 2 — live decision chronology

The production source establishes the chronology without opening any role payload:

- `run_online_rollout` iterates `step_index in range(n_steps)`, measures
  `decision_time_s = plant.data.time`, and calls the policy before `plant.advance`;
- `EstimatorCommandPolicy` always emits on its first call because `_last_output is
  None`, and persists the supplied `step_index` and time;
- `CablePlant.advance` records `PlantStepState.t_s` from `data.time` after the control
  interval and then increments the step counter; and
- `schema/schema.json` names estimator `step`'s unit `control_step_index`.

I then shifted the isolated harness's plant grid to the live post-integration shape and
inserted the faithful first decision. Current row 16 returned:

```text
playback_first=0.002
REFUSED=X_DECISION_UNSUPPORTED
X_DECISION_UNSUPPORTED: case 'fixture-dev' arm C1 decision 0 at t=0.0 s lies outside the playback extent [0.002, 0.064] s
```

This is the inverse of the new `step == T` acceptance test: the implementation accepts a
step the producer cannot emit and rejects the first step it necessarily emits. The
finding is therefore a producer/consumer contract mismatch, not a preference over how
the phrase “inside the playback extent” should read.

## Verification

All commands used the required project interpreter and only tracked code plus isolated
temporary synthetic fixtures. No scientific role, checkpoint contents, MuJoCo model,
fit, rollout or result was opened or run.

- focused adapter/authenticated-storage suite: **243 passed in 6.42 s**;
- the same suite under `PYTHONOPTIMIZE=1`: **243 passed in 6.60 s**, with the expected
  pytest optimized-assertion warning;
- packet-wide suite: **2,901 passed in 155.62 s**;
- the two adversarial probes ran in temporary roots and left no artifact.

The counts reproduce Claude's report. Their coexistence with both accepted bad states is
the evidence that these are missing contract cases, not aggregate regressions.

## Reasoning and decisions

- I treated this as the general recent-work review required by the project constitution,
  not as a formal review. The owner explicitly says the integrated candidate is not
  stable and has created no card or subject chat.
- I did not patch Claude's files. Both corrections are local and reachable while the
  owner is already moving the same module/test pair; taking over an unfinished build
  would create a second ownership surface without improving the evidence.
- I upgraded the Session-148 row-16 question to a definite forward blocker only after
  reading the live producer, schema unit and plant timing source and reproducing the
  rejected faithful initial state. The conclusion is evidence-based rather than a
  stricter-by-default preference.
- The only active Codex-participant chat is Transcript Order Monitoring. Its tail still
  requires no reply; a clean check is not a reason to post.
- The Live-Run README heartbeat was checked and correctly left unchanged. An unfinished,
  unreviewed internal build plus two pre-handoff corrections is not a public milestone.

## Scientific and authorization boundary

Project counters remain **278 rollouts, 67 fits, 67 checkpoints and zero
pilot/validation/test reads**. No production connection record, real role/index/payload,
checkpoint content, estimator result, controller log, final configuration or scientific
result was opened. No capacity, threshold or C1-versus-S choice was made.

Slot-8 Steps 1–3, Step 4a, Step 4b-i and Step 4b-ii-a remain closed / both approved at
their recorded historical bytes. Step 4b-ii-b remains Claude-owned, incomplete and
unapproved. Full Step 4b, production adapter execution, Steps 4c–4f and every later
scientific gate remain closed.

## Files created or updated by Codex

- `agents/Codex/Session Summaries/HumanReport149.md` — this detailed session record.
- `agents/Codex/README.md` — added Session 149 and the current partial-build boundary.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the
  next Codex session.

No packet code, packet test, Review Card, chat transcript, root README or scientific
artifact was changed by Codex.

## Next steps

1. Claude should add the geometry-source/config `model_id` join and an end-to-end
   mismatch refusal before the stable handoff.
2. Claude should replace the current row-16 ruling with one that accepts the live
   step-0/time-0 decision, refuses steps outside the producer's `0..T-1` control grid,
   and records which time axis owns the display-containment bound.
3. Claude should then finish rows 19–21, the observer, bundle/output/CLI wiring and the
   two-pass mutation sweep.
4. Only after one complete stable candidate exists should Claude create the
   Step-4b-ii-b Review Card and matching subject chat and explicitly approve the exact
   handed-off state.
5. The next Codex session should run the full Round-1 Review Card review only after that
   handoff; otherwise it should continue the required general recent-work review without
   inventing downstream work.
