# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-11 — Codex Session 117

## Resume here

The project remains in **Phase 2 — Execution**, with limited Phase-3 Reproducibility Packet
assembly underway. Final configuration is **UNFROZEN** and
`Reproducibility Packet/config/config.json` is absent. Pilot, validation and test roles remain
unread for capacity, threshold, final-configuration and confirmatory decisions.

The seven-step rung-2 sequence is now through **Step 5**:

```text
1. design review/freeze                 CLOSED / BOTH APPROVED
2. module/test build/review             CLOSED / BOTH APPROVED
3. executable/test build/review         CLOSED / BOTH APPROVED
4. plan mode plus artifact review       CLOSED / BOTH APPROVED
5. two-half execution + one invocation  SPENT / X_RUNG2_OK
6. read-only analyzer build/review       OPEN FOR BUILD / NOT APPROVED
7. exact derived-state review + read     NOT AUTHORIZED
```

The one authorized `rung2-run-1` invocation completed. Both equivalence arms passed, all ten
rung-2 arms completed, and the raw terminal artifact records 12 fits / 12 checkpoints / 0
rollouts / 0 generation / 0 non-development reads. Codex's independent raw-state audit passed
261 checks.

**Do not treat that as the derived read.** No analyzer exists, no production analyzer was
invoked, and section 5.4 was not applied. All ten raw `objective_reduced` primitives are `true`,
but `OPTIMIZATION_CHECK_PASSED`, paired signs and rung differences remain analyzer-derived
quantities. They have not been computed or approved.

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

Both agents approve the exact plan. Its two Step-5 authorization halves were spent by the one
completed invocation. The plan licenses no replay or retry.

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

Codex's separate audit passed **261/261** checks: exact identities/counters/census, canonical
serialization, ten approved anchors, two bit-identical equivalence arms, ten planned rung-2
records, all twelve checkpoint digests, rung-2 tensor key/shape/dtype/parameter/finite checks,
no absolute paths, and production completion-validator acceptance.

The raw artifact carries ten true `objective_reduced` primitives. This is not a learning,
classification, C1-versus-S, capacity, trend, threshold or held-out claim.

## Step 6 boundary

The next allowed technical act is **Claude's implementation of the new read-only
`Reproducibility Packet/scripts/analyze_rung2_escalation.py` plus focused tests**, following
frozen design sections 5–6. Synthetic/in-memory fixtures may exercise the analyzer during build.

The following are **not** authorized merely because the build is open:

- invoking the production analyzer on `rung2-run-1`;
- writing the real derived analysis artifact;
- reading pilot, validation or test roles;
- applying section 5.4;
- stating paired signs, rung differences or `OPTIMIZATION_CHECK_PASSED` from an unapproved
  implementation; or
- selecting capacity, thresholds or final configuration.

The analyzer code/test pair must first complete an exact same-state review loop. Preserve code
construction, production invocation, exact derived-state review and joint interpretation as
separate gates.

## Public README state

Claude's Session-117 reviewer edit to the plan heartbeat is closed at:

```text
README.md
  Git blob          485d83ce4c76a708899485fa8eb830c6892f156d
  cleaned SHA-256   efee887595f830c27810d4935ba6555990649c580012611761ebb06b45004586
  Claude approval   explicit
  Codex approval    explicit
```

That wording correctly names the separate 132-check author and 107-check reviewer audits, their
independence from the plan producer, the direct authorization-gate drive and Claude's 23-mutant
calibration.

Codex later repaired the stale `Last updated` banner from 2026-08-10 to 2026-08-11 and approves:

```text
README.md
  Git blob          abeac76cad401de682942424c9a9398237d5bdf5
  cleaned SHA-256   488c2531bfd81028c5513d3e6c281ba93808fcb1020aaa385b7196af33a14731
  cleaned form      145,938 B / 208 LF / 0 CR
  delta vs 485d83ce +1 / -1, banner date only
  Codex approval    explicit
  Claude review     OPEN
```

Claude must genuinely re-open exact blob `abeac76c...`. If approved as-is, the narrow banner
loop closes. If Claude edits it, review the returned exact state.

No public raw-execution heartbeat was added. Wait for an approved analyzer-derived read before
deciding whether a new running-log entry is warranted; do not narrate an unreviewed terminal as a
result.

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
rung-2 execution authorization                     SPENT / ONE INVOCATION COMPLETE
rung-2 raw terminal                                X_RUNG2_OK
rung-2 raw integrity audit                         CODEX PASSED / 261 CHECKS
rung-2 analyzer code/test                          OPEN FOR BUILD / NOT APPROVED
rung-2 production analyzer / joint read            NOT AUTHORIZED
public plan-entry wording                          CLOSED / BOTH APPROVED
public last-updated banner                         CODEX APPROVED / CLAUDE REVIEW OPEN
capacity / probability / abstention thresholds     VALIDATION-OWNED / UNDECIDED
final configuration                                ABSENT / BLOCKED
```

## Stage-1 state that still controls

Stage-1 capacity measurement is **complete as scoped**. Both agents approve the exact C7 artifact
and jointly applied frozen section 5.4. Only row 5 matched:

> **the paired curve does not have a readable shape at five points and five seeds**

No trend statement is licensed. Do not call the curve closing, widening, shrinking, flat, stable
or unmoving. The point values may be quoted only as exact record contents. The measurement selects
no capacity or threshold and makes no scientific C1-versus-S comparison.

The Stage-1 precision note is closed at Git blob
`bc803294610f834900f5671ca0606caf42b21fc4`. Do not reopen it or spend more seeds on its current
statistic. The whole-invocation `10.467 s/fit attempted` figure is a loose proxy, not fit-only
timing or a future marginal-cost bound.

## Checkpoint and packet limitation

The working tree now contains **67 Git-ignored checkpoint files** totaling 19,982,011 bytes:
ten approved `results/dev_fit` anchors, three preserved failed `stage1-run-1` checkpoints, 42
completed `stage1-run-2` checkpoints, and twelve completed `rung2-run-1` checkpoints.

Tracked JSON consistency is auditable without the checkpoints. Before Phase 3 completes, the
team still needs either an authenticated clean-machine recovery/distribution path or an explicit
final packet ruling about the unsatisfied checkpoint portability requirement.

The old Stage-1 `test_capacity_sweep.py` still has two guard tests that aim `main()` at the real
protected tree and carry targeted cleanup. Do not run mutation experiments against that older
harness casually. If reopened, redirect the protected tree into `tmp_path` under a separate
exact-state review.

## Transcript state and Session-117 recurrence

Codex's first authorization append in Session 117 landed at line 19,811, not the physical tail.
The cause was exact: Codex verified a longer unique EOF anchor, then applied a patch using only
the repeated `— Claude` signature and separator. Immediate prefix/header/last-agent assertions
caught it before the project run began.

The misplaced 100-line turn remains preserved. A 52-line dated correction at the physical tail
restated the exact README approval, 36-check preflight, command, plan digest, base, run label,
budget, authorization half and non-authorization boundaries. Its complete 2,010,849-byte prior
state was preserved under SHA-256
`5667e933f62119e67e599c1b990d7889667ae5dd819a6404900aac55ea28fa09`.

The recurrence is also recorded in the director-visible Transcript Order Monitoring thread. The
result handoff and banner-correction appends then used complete pre-verified EOF blocks and passed
all gates. Final technical transcript state:

```text
bytes / LF / CR     2,020,093 / 32,776 / 19,456
SHA-256             615b9df58ab868cc3425c057d096db9ca68d497122c1931ff3a946f940e4a1b9
working-tree delta  +277 / -0, two disclosed hunks
last agent header   Codex Session-117 README banner correction
```

Monitoring transcript final state:

```text
bytes / LF / CR     32,226 / 560 / 127
SHA-256             385daa3d3a9b2fd2cc7cf71ab559b889d65d5ce529c3de993f4323d843c05d85
working-tree delta  +33 / -0
last agent header   Codex Session 117
```

The durable rule remains: verify a unique multi-line physical EOF anchor, and apply that **same
complete object**. Verifying a longer block and patching a suffix is a gate violation even if the
suffix looks like the tail.

## Blocked work

- replaying or retrying `rung2-run-1` under the spent Step-5 halves;
- editing or reopening the frozen design, Step-2 pair, Step-3 pair or consumed plan;
- production analyzer invocation before analyzer code/tests are jointly approved and separately
  authorized;
- treating raw true objective flags as an approved derived status or learning result;
- applying section 5.4 before exact derived-state review by both agents;
- any rung-to-rung or Stage-1 curve trend statement;
- scientific C1-versus-S conclusions from development evidence;
- capacity or threshold selection from development;
- pilot, validation or test outcome reads without named gates;
- new data generation, replacement, supersession or regeneration;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **118**.
- Session 118 is not a regular progress-report session; the next regular is 120.
- First authenticate the physical transcript tail and compare its prior digest to Codex's
  published `615b9df5...e4a1b9` state if Claude reports it.
- If Claude approves README blob `abeac76c...`, close that narrow banner loop. If Claude edits
  it, review the returned exact state.
- If Claude hands over analyzer code/tests, review only that exact pair against frozen sections
  5–6. Do not run the production analyzer merely because the code exists.
- Keep analyzer implementation review, production invocation, exact derived-artifact review and
  joint section-5.4 application as separate gates.
- Do not derive or publish paired signs/rung comparisons manually from the raw result while the
  analyzer gate is open.

## Workflow rules

- Explicit same-state approval only. Creation, execution, edits, handoffs, downstream use and
  silence are not approval.
- An authorization half is spent by its one named act and never carries to a retry.
- Use `./venv` from the project root and packet-scoped commands; never bare Python or root-wide
  pytest outside the packet.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Before every chat append: read the physical UTF-8 tail, record bytes/lines/digest, verify a
  unique multi-line physical-EOF anchor, patch against that **entire exact anchor**, then assert
  the old prefix, unique post-boundary header, last-agent predicate and additions-only diff.
- Use header recognizer `^\*\*[A-Za-z]+ \(Session [^)]*\):\*\*` and take header time at append.
- Keep README updates lean and milestone-based.
