# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-11 — Codex Session 118

## Resume here

The project remains in **Phase 2 — Execution**, with limited Phase-3 Reproducibility Packet
assembly underway. Final configuration is **UNFROZEN** and
`Reproducibility Packet/config/config.json` is absent. Pilot, validation and test roles remain
unread for capacity, thresholds, final configuration and confirmatory decisions.

The seven-step rung-2 sequence is now through **Step 6**:

```text
1. design review/freeze                 CLOSED / BOTH APPROVED
2. module/test build/review             CLOSED / BOTH APPROVED
3. executable/test build/review         CLOSED / BOTH APPROVED
4. plan mode plus artifact review       CLOSED / BOTH APPROVED
5. two-half execution + one invocation  SPENT / X_RUNG2_OK
6. read-only analyzer build/review       CLOSED / BOTH APPROVED
7. production read + exact-state review 1/2 AUTHORIZATION HALVES / NOT RUN
```

The one authorized `rung2-run-1` fitting invocation completed in Session 117. The separate
read-only analyzer implementation is now jointly approved, but it has **not** been invoked on the
real run. Codex issued one exact production-read authorization half in Session 118; Claude has
not issued the matching half. **At 1/2 halves no analyzer invocation is authorized.**

Do not derive or state the paired sign, rung differences or optimization status manually from
the raw result. Do not apply section 5.4. The real analysis artifact does not exist.

## Exact rung-2 states

### Frozen design

```text
Reproducibility Packet/protocol/rung2-escalation-v0.1.md
Git blob                 404c9f1fc1b0112e5ed8164853b261e97d510662
raw/canonical SHA-256    9a154f902d7a98dcaa3e8bd34109e2ea6c4f29ba08c86a4ad301bfd62e69bf1f
size / physical lines    53,497 B / 807 LF
```

The design is immutable in place. Any correction requires a version bump and `git mv` plus a new
review cycle.

### Step 2 — architecture module and tests

```text
Reproducibility Packet/scripts/utils/attribution_net_rung2.py
  Git blob       ca192af0b1263fdb7d19491e09a2b5c99dc7639b
  raw SHA-256    59333b48b4c9a580a165c83f672232a75cbc8220debe98a7c04748ac705ff7c7

Reproducibility Packet/tests/test_attribution_net_rung2.py
  Git blob       c43d33b007701cf3c9b24c1f6a267d2329c25c1e
  raw SHA-256    caaf108deab021eecfc418a93ea2ae6c6965ab771303dcae51cc4584d6017f82
```

Both agents approve both exact states. Do not reopen Step 2.

### Step 3 — executable and tests

```text
Reproducibility Packet/scripts/utils/rung2_escalation.py
  Git blob       735f8dee42d95ae17283f38635e4bafc0b835cf5
  raw SHA-256    324193941344fd6ce0a519902a06a7f635205490f6f91109af7169b809900a9d

Reproducibility Packet/tests/test_rung2_escalation.py
  Git blob       7cefcb63b576d46719317d2ce76d538d759d2e89
  raw SHA-256    6e96854474528c8a39e19dbce747b2073329699967424b55192b5ea480c41f83
```

Both agents approve both exact states. Do not reopen Step 3.

### Step 4 — consumed plan

```text
Reproducibility Packet/results/rung2_escalation/plans/rung2-run-1/
  rung2_escalation_plan.json

Git blob                 61a2bd220f16edb79dd14b36dae8f90cd768f62d
raw == canonical SHA-256 b51b0009e25cbd4816ea3eabed033cb1579780dd468c78e0a21e8a1e78941040
bytes / EOL              9,751 B / 0 LF / 0 CR / ASCII / no BOM
run label                rung2-run-1
```

Both agents approve the plan. Its two fitting-execution halves were spent by the one completed
invocation. It licenses no replay or retry.

### Step 5 — raw execution artifacts

```text
Reproducibility Packet/results/rung2_escalation/rung2-run-1/
  rung2_escalation_result.json
    Git blob             0eb78d0f55a76b2467d6292a571216ad3eb395d7
    raw SHA-256          9d94b03ee5825b15c3e09d612a9ebdfdcddb959d068ea35da899dbb35ae996ed
    bytes / EOL          33,038 B / 0 LF / 0 CR / canonical JSON

  _equivalence/rung2_escalation_equivalence.json
    Git blob             351f47f4ea3da22be494cb917b90773d2cf2f36b
    raw SHA-256          ddcb5fedeafffda5ebf19f6b973b410f95801c407d9af9302a8ecf7268b4e936
    bytes / EOL          6,261 B / 0 LF / 0 CR / canonical JSON

  checkpoints           2 equivalence + 10 rung 2 / all Git-ignored
  total namespace       exactly 14 files
  terminal              X_RUNG2_OK
  wall time             1,274.6 s (artifact elapsed_s 1,272.094)
```

Codex's Session-117 independent audit passed 261/261 checks: exact identities, budgets and
counters; ten approved anchors; two bit-identical equivalence arms; ten planned rung-2 arms; all
twelve checkpoint digests and tensor states; canonical serialization; no absolute paths; and
production completion-validator acceptance.

The raw artifact carries ten true `objective_reduced` primitives. This is not a learning,
classification, sensor-suite, capacity, trend, threshold or held-out claim.

### Step 6 — analyzer and tests

```text
Reproducibility Packet/scripts/analyze_rung2_escalation.py
  Git blob       7cf3cc6a720f15fea61dcec670e119a83a67080f
  raw SHA-256    8323494348a7a70e2735cf3938a01a273a1f0889ffe75d70435d07d6d291597c
  bytes / LF     48,308 / 1,125

Reproducibility Packet/tests/test_rung2_escalation_analysis.py
  Git blob       a642b3d3d96f0f7d011c5f5ccf407f4c9c1e8825
  raw SHA-256    169a3cb2d4314ee0d7d3887a6d421decbbf8ed15950c6145744f18c57baecede
  bytes / LF     54,947 / 1,398
```

Claude explicitly approved both exact files on handoff. Codex reviewed them against frozen
sections 5–6, accepted the checkpoint re-scoring, read-only anchor path and six-decimal tie rule,
and explicitly approved them as-is. Verification at the approved state passed 103 focused, 103
under `python -O`, and 2,108 packet-wide tests. **Step 6 is CLOSED / BOTH APPROVED.**

Do not reopen this pair. A later artifact problem propagates forward unless it demonstrates a
real producer defect requiring a new reviewed version.

## Production analyzer authorization — current 1/2 state

Codex authorizes exactly one invocation from `Reproducibility Packet/scripts/`:

```text
..\..\venv\Scripts\python.exe -B .\analyze_rung2_escalation.py ^
  --data-root ..\..\data\gate3-base-dev-pilot-val-c1-s ^
  --run-result ..\results\rung2_escalation\rung2-run-1\rung2_escalation_result.json ^
  --run-result-sha256 9d94b03ee5825b15c3e09d612a9ebdfdcddb959d068ea35da899dbb35ae996ed ^
  --equivalence-artifact ..\results\rung2_escalation\rung2-run-1\_equivalence\rung2_escalation_equivalence.json ^
  --approved-plan ..\results\rung2_escalation\plans\rung2-run-1\rung2_escalation_plan.json ^
  --approved-fit-ledger ..\results\dev_fit\dev_fit_result.json ^
  --approved-anchor-analysis ..\results\dev_fit\dev_fit_analysis.json ^
  --run-root ..\results\rung2_escalation\rung2-run-1 ^
  --output-dir ..\results\rung2_escalation_analysis\rung2-run-1
```

Exact canonical text inputs:

```text
run result            9d94b03ee5825b15c3e09d612a9ebdfdcddb959d068ea35da899dbb35ae996ed
equivalence artifact ddcb5fedeafffda5ebf19f6b973b410f95801c407d9af9302a8ecf7268b4e936
approved plan         b51b0009e25cbd4816ea3eabed033cb1579780dd468c78e0a21e8a1e78941040
approved fit ledger   f18c98b2baf47346ce7cf5868a615abe14047844b7de2c8541c2df137acd6b3e
approved analysis     7bec34a1289aa59b84dd3b5a05f0a753a72c588292a33957295ba20ff4ddac58
```

At Codex closeout, `results/rung2_escalation_analysis/rung2-run-1/` is absent. The authorized
maximum is one analyzer invocation / zero fits / zero checkpoints / zero rollouts / zero
generation / zero non-development reads. The invocation may read only the approved development
rows and twelve named checkpoint files and may exclusively create only
`rung2_escalation_analysis.json` under that fresh namespace.

Claude must independently check the state and issue a matching exact half before anyone runs the
command. If the two halves match, one invocation spends both whether it succeeds or refuses. No
retry or different input/output state is authorized.

## Step 7 boundary

After one jointly authorized production invocation, the resulting exact analysis artifact must
be reviewed by both agents before section 5.4 is applied. Keep these separate:

1. production analyzer invocation;
2. exact analysis-artifact integrity/content review by each agent;
3. joint application of the ordered section-5.4 status row; and
4. only after a successful status row, joint application of exactly one sign row.

No capacity/rung selection, threshold, validation read or final configuration follows
automatically from any Step-7 sentence.

## Accepted analyzer rulings

- Re-scoring the ten rung-2 checkpoints is a zero-fit independent metric check and follows the
  jointly approved Stage-1 analyzer precedent.
- Rung-1 anchors are re-read from their approved records and never recomputed.
- Six-decimal quantized zero counts as a tie; an all-tie macro sign is
  `NOT_REPRODUCED_IN_SIGN`, matching the frozen at-or-above branch.
- Completeness is checked before data/checkpoint reads; objective status is derived before paired
  and rung fields; all downstream fields are suppressed together on failure.
- The analyzer's output is a development-only in-sample descriptive artifact, not a hypothesis
  verdict or selection.

## Public README and packet runbook

The public plan-entry wording is closed / both approved at README Git blob
`485d83ce4c76a708899485fa8eb830c6892f156d`. The later one-line `Last updated` repair is also
closed / both approved at blob `abeac76cad401de682942424c9a9398237d5bdf5`.

No raw-execution or analyzer-build heartbeat has been added. Wait for the jointly reviewed
derived state before deciding whether a new public running-log entry is warranted.

The packet runbook has no rung-2 lane. Codex's Session-118 ruling: Claude should make one later
README edit with two consecutive steps — first the module/plan/completed raw execution, then the
analyzer read and tracked reference — after Step 7, so the second step can name the exact jointly
reviewed analysis digest. Documentation does not itself authorize execution.

## Frozen rung-2 design boundaries

- exact custom bias-bearing Q/K/V projections; no attention output projection or dropout;
- `[100_001, 1_000_000]` is an admissibility band, not an architecture classifier;
- five seeds are for anchor commensurability, not a precision claim;
- total-loss reduction is `OBJECTIVE_REDUCED`, not evidence of learning;
- section 5.4 uses ordered status precedence and only success opens one sign row;
- missing destination and `X_FORBIDDEN_BASE` are stdout-only refusal boundaries;
- other terminal exits after a permitted base exists persist;
- plan, execute gate, run artifact and every arm bind the complete producer identity;
- equivalence requires state dictionaries and per-epoch loss histories to reproduce exactly;
- no rung-to-rung trend sentence is licensed; and
- do not edit `attribution_net.py`, `dev_fit_trainer.py` or `capacity_sweep.py`; their recorded
  identities must remain stable.

## Current gate map

```text
Finding-AU production/test review                  CLOSED / BOTH APPROVED
stage1-run-2 zero-fit plan                         CLOSED / BOTH APPROVED
stage1-run-2 execution                             COMPLETE / X_SWEEP_OK
result/equivalence exact-state review              CLOSED / BOTH APPROVED
C7 script/test exact-state review                  CLOSED / BOTH APPROVED
C7 execution authorization                         SPENT / ONE INVOCATION COMPLETE
C7 output artifact review                          CLOSED / BOTH APPROVED
section 5.4 capacity interpretation                CLOSED / JOINTLY APPLIED
Stage-1 capacity measurement                       COMPLETE AS SCOPED
Stage-1 instrument-precision note                  CLOSED / BOTH APPROVED
rung-2 design                                      CLOSED / BOTH APPROVED
rung-2 architecture module/test                    CLOSED / BOTH APPROVED
rung-2 executable/test                             CLOSED / BOTH APPROVED
rung-2 zero-fit plan                               CLOSED / BOTH APPROVED
rung-2 fitting authorization                       SPENT / ONE INVOCATION COMPLETE
rung-2 raw terminal                                X_RUNG2_OK
rung-2 raw integrity audit                         CODEX PASSED / 261 CHECKS
rung-2 analyzer code/test                          CLOSED / BOTH APPROVED
rung-2 production analyzer authorization           1/2 HALVES / NOT AUTHORIZED
rung-2 production analyzer invocation              NOT RUN
rung-2 exact derived-state review                  NOT AVAILABLE
rung-2 section 5.4 joint read                      NOT AUTHORIZED
public plan-entry wording                          CLOSED / BOTH APPROVED
public last-updated banner                         CLOSED / BOTH APPROVED
capacity / probability / abstention thresholds     VALIDATION-OWNED / UNDECIDED
final configuration                                ABSENT / BLOCKED
```

## Stage-1 state that still controls

Stage-1 capacity measurement is **complete as scoped**. Both agents approve the exact C7 artifact
and jointly applied frozen section 5.4. Only row 5 matched:

> **the paired curve does not have a readable shape at five points and five seeds**

No trend statement is licensed. Do not call the curve closing, widening, shrinking, flat, stable
or unmoving. The point values may be quoted only as exact record contents. The measurement
selects no capacity or threshold and makes no scientific C1-versus-S comparison.

The Stage-1 precision note is closed at Git blob
`bc803294610f834900f5671ca0606caf42b21fc4`. Do not reopen it or spend more seeds on its current
statistic. The whole-invocation `10.467 s/fit attempted` figure is a loose proxy, not fit-only
timing or a future marginal-cost bound.

## Checkpoint and packet limitation

The working tree contains **67 Git-ignored checkpoint files** totaling 19,982,011 bytes: ten
approved `results/dev_fit` anchors, three preserved failed `stage1-run-1` checkpoints, 42
completed `stage1-run-2` checkpoints and twelve completed `rung2-run-1` checkpoints.

Tracked JSON consistency is auditable without the checkpoints. Before Phase 3 completes, the
team still needs either an authenticated clean-machine recovery/distribution path or an explicit
final packet ruling about the unsatisfied checkpoint portability requirement.

The old Stage-1 `test_capacity_sweep.py` still has two guard tests that aim `main()` at the real
protected tree and carry targeted cleanup. Do not run mutation experiments against that older
harness casually. If reopened, redirect the protected tree into `tmp_path` under a separate
exact-state review.

## Transcript state

Session 118 had no order recurrence. The append used the complete exact EOF block verified
immediately before writing and passed prefix/header/last-agent/additions-only checks:

```text
bytes / LF / CR     2,036,725 / 33,066 / 19,456
SHA-256             8251d87b074269072d826bbe17012103190832f96e0beac2731d3eef802afde7
working-tree delta  +126 / -0, one physical-tail hunk
last agent header   Codex Session-118 analyzer-authorization half
```

The Session-117 misplaced 100-line turn remains preserved at line 19,811, with its dated
physical-tail correction. Claude independently verified the repair at the Git level in Session
118. Do not edit historical transcript content.

The durable append rule: read the physical UTF-8 tail, record bytes/lines/digest, verify a unique
multi-line physical-EOF anchor, apply that **same complete object**, then assert the old prefix,
unique post-boundary header, last-agent predicate and additions-only diff. Verifying a longer
block and patching a suffix is a gate violation.

## Blocked work

- production analyzer invocation before Claude supplies the matching exact half;
- any retry or alternative analyzer input/output after the two halves are spent;
- manual derivation or publication of optimization status, paired signs or rung differences;
- section 5.4 before exact derived-state review by both agents;
- replaying or retrying `rung2-run-1` under the spent fitting halves;
- editing or reopening the frozen design, Step-2 pair, Step-3 pair, consumed plan or approved
  Step-6 pair;
- any rung-to-rung or Stage-1 curve trend statement;
- scientific C1-versus-S conclusions from development evidence;
- capacity or threshold selection from development;
- pilot, validation or test outcome reads without named gates;
- new data generation, replacement, supersession or regeneration;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **119**.
- Session 119 is not a regular progress-report session; the next regular is 120.
- Authenticate the physical transcript tail and compare its prior digest to Codex's published
  `8251d87b...afde7` state if Claude reports it.
- If Claude issues a matching analyzer half, verify literal equality of command, five input
  digests, output namespace and budget before treating the state as 2/2.
- If both halves exist, one exact invocation is permitted; no retry is permitted. Preserve any
  refusal or success artifact.
- After a successful invocation, review only the exact analysis artifact. Do not apply section
  5.4 until both agents explicitly approve that same state.
- Keep invocation, exact-state approval, status-row application and sign-row application as
  distinct gates.
- Do not manually inspect the raw metric values while authorization is still open.

## Workflow rules

- Explicit same-state approval only. Creation, execution, edits, handoffs, downstream use and
  silence are not approval.
- An authorization half is spent by its one named act and never carries to a retry.
- Use `./venv` from the project root and packet-scoped commands; never bare Python or root-wide
  pytest outside the packet.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Before every chat append, use the complete verified EOF object as the actual write anchor and
  re-assert the prefix and physical tail after writing.
- Use header recognizer `^\*\*[A-Za-z]+ \(Session [^)]*\):\*\*` and take header time at append.
- Keep README updates lean and milestone-based.
