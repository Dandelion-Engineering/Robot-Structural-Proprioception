# Human Report — Codex Session 49

**Current date and time:** 2026-07-31 14:11 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state re-review of Claude's returned Session-48 progress report;
first review of Reproducibility Packet README Step 24; review of Claude Session 49's
public Stage-0 claims; closeout of the executed Stage-0 result loop

**Final config state:** **UNFROZEN**; no final `config.json` exists

**Protocol-P execution state:** Stage 0 has run exactly once and is now jointly approved
at the same exact result artifact. Protocol P has spent one plant rollout total, the
Session-45 replay. Stages A/B/C remain unbuilt and unauthorized. The confirmatory test
split remains untouched.

---

## Summary

Claude Session 49 performed the missing owner re-review of the executed Stage-0 result,
explicitly approved the unchanged artifact, independently re-derived its distribution
with standard-library Python rather than NumPy, and closed the result review loop at Git
blob `31c1e6d1824c10bd5978d12c377f76cf556af03f`.

This session accepted that closure after a read-only independent audit. It also accepted
Claude's finding that `stage_0_identity` binds the run's approved inputs and output shape,
not its measured distances or summary values. That is a documentation boundary, not a
Protocol-P defect: the approved specification pins exactly the seven-key provenance
payload the implementation hashes and claims only that the identity is recomputable from
the artifact. No protocol version change is warranted.

Two active artifact reviews then moved:

1. Claude's returned Session-48 progress report is approved at blob
   `f01aa7d7b56b9b30e8279bc221a5f0e60613ab3f`. Its owner and reviewer now explicitly
   approve the same state, so that loop is closed.
2. Reproducibility Packet README Step 24 required three narrow reviewer edits before
   approval. The reviewer-edited state is blob
   `9363e144a0c0e957b5c0a201d3abbf47c68fe837`; Codex explicitly approves it and returned
   it to Claude for genuine owner re-review. That loop remains open.

Claude's new public running-log entry also contained two precise overstatements. The entry
was preserved unchanged and a dated append-only correction was added. Codex approves the
forward-corrected public README at blob
`f3f76f27f48e2ed228917328bbc0462d34addc23`; Claude's owner re-review is still required.

No Stage-0 re-execution, plant rollout, protocol edit, result edit, assignment edit,
draft-config edit, payload write, or test-split access occurred.

---

## 1. Executed Stage-0 result loop closed

The approved result artifact remains unchanged:

```text
Reproducibility Packet/results/protocol_p/sensor_only_difference_null.json
  git blob    31c1e6d1824c10bd5978d12c377f76cf556af03f
  raw sha256  4101c0b8dcc1c3ee01b37433ccb3563d4c1e15e5e22cd8094979645d36a40cae
  identity    dev-71b332893d007036625f666589f8c74b0ac3b946b47b5186ddf8de6a2d8ce31e
```

Claude's owner re-review was substantive rather than ceremonial. It used Python's
standard-library `statistics` module plus hand-indexed order statistics instead of the
NumPy path that produced the artifact and that Codex had used in Session 48. It reproduced
the quantile, population standard deviation, minimum, median, maximum, and the exact
upper-tail counts. `statistics.fmean` differed from the recorded NumPy mean by one unit in
the last place because of summation order; NumPy reproduces the written mean exactly.

Codex independently parsed the tracked artifact again without calling `main()` or
`run_null()` and reproduced:

```text
n                            100
finite and nonnegative       100 / 100
population std               0.0747731492497055
Q95, method="higher"         0.4008810868833315
values > Q95                 4
values >= Q95                5
identity recomputation       PASS
```

The only supported corroboration remains conditional upper-tail containment within the
prior fixed-trace per-cell range `[0.3176, 0.4251]`. Stage 0 sets no threshold, has no
mechanics, and has no authority over any verdict. The operative development null remains
Stage C's per-cell `Q95_c`.

---

## 2. Identity-scope narrowing accepted

Claude demonstrated in memory that changing a recorded distance and the headline Q95
does not change `stage_0_identity` when the inputs and top-level schema remain fixed.
Codex traced that construction to both Protocol P and the implementation.

The canonical payload contains exactly:

- stage label;
- base configuration hash;
- assignment canonical digest;
- assignment document hash;
- protocol canonical digest;
- the seven pinned CLI values; and
- the sorted top-level output schema.

It does not contain measured values. Therefore the identity is a provenance identity over
inputs and shape, not a tamper seal over results. The specification already defines that
scope correctly. The proper response is to document the boundary wherever the identity is
described, not to edit or version-bump an approved protocol to satisfy an intuition carried
by the word “identity.” Result values are verified by recomputing them from the artifact's
recorded `samples.distances`.

---

## 3. Session-48 progress report loop closed

Claude accepted all three Session-48 reviewer corrections, found the same claim families
still present elsewhere in the director-facing report, and edited them forward. Codex read
the complete returned report and approved:

```text
agents/Claude/Progress Reports/Progress Report Session 48.md
  git blob  f01aa7d7b56b9b30e8279bc221a5f0e60613ab3f
```

The final same-state report now:

- describes Stage 0 as a healthy-difference diagnostic that sets no threshold;
- calls the mutation target an input-binding integrity check and explicitly separates it
  from physical safety;
- avoids claiming that a reviewed line performs a verification it does not perform; and
- reports the Q95 order statistic as five values at or above, four strictly above.

Claude explicitly approved this blob as owner and Codex explicitly approved it as
reviewer. The loop is closed.

---

## 4. Packet README Step 24 review

Claude's first Step-24 state was scientifically careful but had one dependency overclaim,
one outsider-facing style leak, and one imprecise JSON field path. Codex edited all three:

```text
Reproducibility Packet/README.md
  owner handoff blob       e525c7bea92eb259f62368b75c5ecb950e5fd370
  reviewer-edited blob     9363e144a0c0e957b5c0a201d3abbf47c68fe837
  review diff              +3 / -3
```

### Dependency correction

Step 24 said it needed neither a dataset nor MuJoCo. The measurement performs no MuJoCo
simulation and spends no rollout, but importing
`analyze_synchronous_difference_null.py` loads `mujoco` transitively through:

```text
protocol_p_replay_gate -> assignment_generator -> cable_plant
```

An import-only check reported `mujoco_imported=True` without executing Stage 0. Step 1
installs the package, so the command remains runnable from a clean packet checkout after
environment setup. The corrected runbook says it needs no dataset and performs no MuJoCo
simulation; it no longer claims package independence.

### Outsider-clean elapsed-time correction

The original paragraph referred to internal session records. The packet playbook forbids
Collaboration Station and session-history narration in the outsider runbook. The edited
paragraph states only the auditable facts: no trustworthy first-run timing was captured,
Protocol P binds no elapsed time, and any later timing must be labeled as a separate
reproduction.

### Exact field path

The authority string lives at `corroboration.authority`, not in a top-level `authority`
field. The runbook now names the exact path.

The command, pins, result values, identity, zero-rollout count, and scientific boundaries
are unchanged. Codex explicitly approves blob `9363e144...`. Claude must genuinely
owner-review and explicitly approve or edit-and-return that exact state.

---

## 5. Public README correction

Claude's dated 2026-07-31 entry correctly announced joint approval and the identity-scope
finding, but two phrases exceeded the evidence:

1. “needs no physics engine” ignored the transitive MuJoCo package import; and
2. “every summary figure reproduced exactly” ignored the one-ULP alternate-mean
   difference Claude had already documented.

The live running log is append-only, so the original entry remains untouched. Codex added
one dated forward correction covering both issues:

```text
README.md
  reviewer-edited blob  f3f76f27f48e2ed228917328bbc0462d34addc23
  review diff           +2 / -0
```

The correction preserves the result approval, measured values, zero-rollout fact, and
scientific boundary. Codex explicitly approves the corrected public README state. Claude
must owner-review it; routine same-state approval need not create another public milestone.

---

## 6. Verification

The repository's authoritative packet suite and compile gate passed after the documentation
edits:

```text
full packet suite              595 passed in 12.26 s
compileall                     clean
config.json                    absent
test-named .npz files          0
.npz under results/            0
Protocol-P rollouts spent      1, unchanged
```

No code or tracked result artifact changed. `git diff --check` was clean before closeout;
Windows LF/CRLF warnings were informational and did not justify line-ending churn.

---

## 7. Transcript append verification

The active Phase-2 transcript was appended under the physical-tail hard gate:

```text
pre-write lines       11,185
pre-write bytes       811,471
pre-write sha256      3a13cf6563ce62957a927e161d63ba49dac0aef301ea80f948daaac01f79c66f
Codex header line     11,189
Codex header count    1
technical diff        +150 / -0
post-write lines      11,335
post-write bytes      818,050
post-write sha256     c64ef573966464af8fb2c71c4fe48188e0943a81e955cd12db997b3ba0828f4b
old byte prefix       exact
physical last author  Codex
```

No transcript-order recurrence occurred, so the standing monitoring thread was not
updated.

---

## Important decisions

1. Close the Stage-0 result loop only after Claude's explicit owner approval of the exact
   unchanged result blob.
2. Treat the identity-scope finding as a write-up boundary, not a reason to reopen the
   approved protocol.
3. Approve the returned progress report and close that loop.
4. Edit Step 24 to distinguish zero simulation from zero package dependency, keep it
   outsider-clean, and name the exact authority path.
5. Preserve the public log entry and correct its two overstatements forward.
6. Keep Stages A/B/C unauthorized until a separate driver implementation reaches explicit
   same-state approval.
7. Keep final `config.json` absent and the confirmatory test split untouched.

---

## Challenges and how they were handled

**Zero-simulation was easy to overread as zero dependency.** Static import tracing showed
that shared validators pull in `assignment_generator`, which pulls in the MuJoCo plant. An
import-only process proved the package is loaded without executing the stage. The runbook
now states both sides precisely.

**A public sentence contradicted its own supporting report.** Claude correctly disclosed
the one-ULP `fmean` difference in the report while the public entry said every summary
figure reproduced exactly. A forward correction preserves the dated record and narrows the
claim without changing the result.

**The packet had to stay outsider-facing.** An internal session-note explanation of the
missing first-run timing was useful in team continuity but did not belong in the packet
runbook. It was replaced with the externally auditable fact and disposition.

---

## Files created or updated

**Created:**

- `agents/Codex/Session Summaries/HumanReport49.md` — this report.

**Updated:**

- `Reproducibility Packet/README.md` — reviewer corrections to Step 24; approved and
  returned to Claude.
- `README.md` — dated append-only correction to Claude's new Stage-0 entry.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — Session-49 decision and handoff, appended at the physical tail.
- `agents/Codex/README.md` — workspace index and current shared-state descriptions.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the next
  session.

**Deliberately unchanged:** the Stage-0 result artifact; Stage-0 implementation and tests;
shared gauge helper; detection-floor script; replay gate; Protocol P; Gate-3 assignment;
draft config; `.gitattributes`; every payload; the test split.

---

## Next steps

Claude owns two exact-state re-reviews:

1. Reproducibility Packet README Step 24 at blob `9363e144...`; and
2. the forward-corrected public README at blob `f3f76f27...`.

After those loops close, the next technical artifact is the Stage-A/B/C driver. It must
receive explicit same-state approval before any Stage A execution. Stages A, B, and C must
then run in order. Amendment A2, replacement assignment approval, from-zero non-test
regeneration, Gates 4–7, joint immutable freeze, and untouched confirmatory evaluation all
remain later work.

The next Codex session is Session 50. The next regular Codex progress report is Session 56
unless a phase transition or approved Claim Sheet amendment triggers one earlier.
