# Codex — Human Report, Session 82

**Date and time:** 2026-08-06 02:19 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.
**Progress-report session:** no. The next regular Codex progress report is Session **88**.

---

## Summary

Claude Session 82 genuinely re-reviewed and preserved all six trainer corrections Codex
made in Session 81, found and repaired one exception-classification defect, and supplied
the missing ordinary/diagnostic development-window policy. I independently checked that
policy against the approved assignment and Protocol P v2.3.3 rather than accepting the
handoff arithmetic.

I **approve the policy**:

```text
diagnostic dev window   [1000, 1768)  — exact Protocol P §8 reproduction
ordinary dev window     [ 900, 1668)  — same 500-step post-onset lead
windows per run         1             — no unregistered stride
```

Using the split diagnostic offset as the prospective anchor avoids a second chosen lead;
using one window per persisted run avoids a new stride and correlated-window inflation.
The same arithmetic is total over the reserved pilot/validation/test designs, but this
does not authorize those role reads. I narrowed one overstatement: equal lead removes an
avoidable time-since-onset difference, but it does not make excitation the only difference
between trajectories because the assignment also changes target joints and task timing.

The exact submitted executable was not yet approval-ready. I reproduced four surrounding
refusal/provenance defects, corrected them, added five focused tests, and explicitly
approved the reviewer-edited state. Because those edits changed executable bytes, Claude's
genuine same-state re-review remains open and no development fit is authorized yet.

No fit, checkpoint, observation-payload read, later-role outcome read, generation,
rollout, threshold choice or final-config action occurred.

## Exact review input and decision

Claude handed off and explicitly approved:

```text
Reproducibility Packet/scripts/utils/dev_fit_trainer.py
  100546962409f49560ef8670001b20bcbe5de456
Reproducibility Packet/tests/test_dev_fit_trainer.py
  9e76923cdf0e34e03f6b7bcb812233f869cbfcc1
```

I approve the scientific window rule but block those exact executable bytes on the four
findings below. The reviewer-edited handback, which I explicitly approve, is:

```text
Reproducibility Packet/scripts/utils/dev_fit_trainer.py
  788fc240c404797f883c08fc843296f277412643
Reproducibility Packet/tests/test_dev_fit_trainer.py
  c95bd8fbb5cf3dcb5d99bfb7f22799d738dcb0f7
```

These bytes remain a review handoff, not permission to execute. Claude must approve or
contest the exact same state before any real fit begins.

## Window-policy ruling

The approved assignment reserves the development diagnostic trajectory at onset step 500
with a 500-step probe offset. Protocol P §8 prospectively fixes its 768-sample slice at
`[1000,1768)`. Claude's derivation lands on that window exactly. The ordinary trajectory
starts at step 400 and receives the same post-onset lead, yielding `[900,1668)`.

This is preferable to a caller-supplied origin for three reasons:

1. The diagnostic anchor predates the trainer question and was not selected from model
   outcomes.
2. The ordinary rule adds no separate lead and aligns elapsed time after onset.
3. One window per row leaves the auditable example count equal to the persisted row count:
   152 examples per suite/arm, 76 from each trajectory.

The rule does not erase the two trajectories' other design differences. It therefore
supports the training census without licensing a claim that ordinary and diagnostic rows
differ only by excitation.

## Findings and corrections

### Finding O — equal counts were not matched identities

The submitted `require_matched_trajectory_census()` accepted two states that contradicted
its paired-comparison claim:

- one scheduled trajectory absent from both C1 and S; and
- equal per-trajectory C1/S counts built from disjoint `pair_id` sets.

The corrected state requires the selected rows to cover every scheduled trajectory and
requires exact C1/S `pair_id` set equality for each trajectory, in addition to equal
counts. The real delivered manifest passes: both trajectories have 76 exact C1/S pairs.

### Finding P — assignment timing was not bound back to the label payload

The trainer checked assignment duration against observation length, but it never checked
the independent persisted `onset_index` / `onset_time_s`. A label onset could move while
the assignment-derived window stayed fixed and still reach training.

The corrected `build_example()` requires both label onset fields to equal the
assignment-derived trajectory onset before slicing. I read all 304 authorized dev label
payloads to check the real seam: every ordinary label carries 400 / 0.8 s and every
diagnostic label carries 500 / 1.0 s, with 76 C1 and 76 S rows per trajectory. No
observation payload was opened.

### Finding Q — malformed schedule controls escaped or changed meaning

Direct probes against Claude's exact blob measured:

```text
window_steps=True       accepted as a one-step window
empty diagnostic probe  raw TypeError from np.isfinite(None)
control_dt_s=0          raw ZeroDivisionError
```

The corrected policy parser validates the assignment mapping, non-empty trajectory ids,
probe object/null shape, positive non-bool integer window length, fixed positive
development control period and boolean probe flag. These states now produce the named
`DevFitContractError` boundary.

### Finding R — output reuse could mix checkpoint generations

Checkpoint names are deterministic and the submitted trainer overwrote them arm by arm.
After a partial attempt, a rerun into the same directory could leave old checkpoints for
arms the current invocation never completed. The current result document would name only
current arms, but any later directory enumeration would see a mixed population.

The corrected trainer refuses any existing `dev_fit_result.json` or
`dev_fit_*_seed*.pt` before the first fit. A `dev_fit_plan.json` alone remains allowed so
an operator can plan and then fit in one fresh directory.

## Verification and evidence boundary

```text
focused trainer tests                37 passed
focused trainer tests under -O       37 passed; expected pytest warning only
full packet suite                    1,504 passed in 128.96 s
compileall                           clean
git diff --check                     clean
production plan probe                X_PLAN_OK; 10 arms; 0 fits; 0 rollouts
real selected manifest rows          304 dev rows; 640 withheld
real exact pairing                   76 C1 / 76 S pairs per trajectory
real label payload reads             304 dev labels
real observation payload reads       0
pilot / validation / test outcomes   0 reads
fits / checkpoints / results         0 / 0 / 0
generation / rollouts                0 / 0
final config/config.json             absent
```

The focused suite grew from 32 to 37 tests. The full packet suite grew from Claude's
1,499 to 1,504 with no regression. The production plan was written only to a temporary
directory outside the repository and removed after inspection.

## Transcript-order recurrence and repair

The first Session-82 technical reply did not use the complete 18-line EOF block I had
programmatically verified. Its applied patch matched an older repeated `— Claude`
signature and inserted the 105-line review at physical line 19,334 instead of after the
22,206-line tail. The immediate verifier caught the changed prefix, pre-boundary header
and non-last author before commit.

Per the append-only rule I did not remove or move the misplaced text. I appended a dated
forward correction from a newly verified unique EOF block, restating every
decision-bearing part. Final technical-thread checks:

```text
repair boundary bytes    1,412,434
repair boundary lines    22,311
repair boundary SHA-256  7ef90c086909253d423058b2b08393a8b14d481e224395c1520f2904bd256e09
final bytes              1,414,699
final lines              22,349
final SHA-256            dca21bf5406e4dda735d986a66257111c3a3c50a6c78f715ba7cc81072c625ae
correction header        unique at line 22,313
technical diff           +143 / -0
physical last author     Codex
```

Because this was a genuine recurrence, I reported it in the director-visible Transcript
Order Monitoring thread. Its first monitoring append landed in order and remained
content-additions-only, but its byte-prefix assertion detected CRLF-to-LF normalization
inside the applied EOF context. I preserved that state and appended a second-order byte
correction from a fresh verified LF boundary. Final monitoring-thread checks:

```text
repair boundary bytes    11,696
repair boundary lines    185
repair boundary SHA-256  4cef7390552300dd0d5997c8d8dfac70b2e56f95ab42b5bc3083f2af50b9640f
final bytes              12,617
final lines              204
final SHA-256            a76596a0788013b0e54f02533069c96bd758b097e249e4c97d75a9e51210335f
byte-correction header   unique at line 189
monitoring diff          +51 / -0
physical last author     Codex
```

Both incidents are disclosed rather than waved through. Neither changes the technical
decision or authorization state.

## Public README heartbeat and boundaries

The root Live-Run README and packet README are unchanged. The trainer loop remains open,
so this is not yet a finished executable artifact or a fit result. The packet README owes
its trainer step only after the exact executable loop closes. The public log should wait
for that closure and preferably the first bounded development fit.

All of the following remain blocked absent separate explicit authorization:

- any development fit until Claude approves the exact reviewer-edited trainer bytes;
- pilot, validation or test outcome reads;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation or further payload measurement;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Files created or updated

- `Reproducibility Packet/scripts/utils/dev_fit_trainer.py` — accepted window policy plus
  strict control parsing, exact paired-identity/coverage checks, independent label-onset
  binding and stale-output refusal.
- `Reproducibility Packet/tests/test_dev_fit_trainer.py` — five new focused regressions and
  onset-aware synthetic fixtures.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — append-only substantive review plus physical-tail correction.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring -
  Active.md` — director-visible recurrence report plus byte-prefix correction.
- `agents/Codex/Session Summaries/HumanReport82.md` — this report.
- `agents/Codex/README.md` — workspace index and active-state descriptions refreshed.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten resume state.

## Next steps

1. Claude genuinely re-opens and reviews trainer blobs `788fc240...` / `c95bd8fb...`.
2. Claude explicitly preserves or contests Findings O–R and the exact reviewer edits.
3. If Claude approves the same bytes, the trainer executable loop closes.
4. Only after that closure may the ten predeclared development-only C1/S fits run, in a
   fresh output directory, with zero new data generation and zero physical rollouts.
5. The resulting dev evidence may establish learnability or an implementation failure; it
   may not read later roles, set validation-owned thresholds or become a confirmatory
   result.

The central learned-model measurement still has not run. This session settled the window
policy and made its executable boundary stricter; it produced no evidence about the
structural-proprioception hypothesis.
