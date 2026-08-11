# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-11 — Codex Session 116

## Resume here

The project remains in **Phase 2 — Execution**, with limited Phase-3 Reproducibility Packet
assembly underway. Final configuration is **UNFROZEN** and
`Reproducibility Packet/config/config.json` is absent. Pilot, validation and test roles remain
unread for capacity, threshold, final-configuration and confirmatory decisions.

The seven-step rung-2 sequence is now through **Step 4**:

```text
1. design review/freeze                 CLOSED / BOTH APPROVED
2. module/test build/review             CLOSED / BOTH APPROVED
3. executable/test build/review         CLOSED / BOTH APPROVED
4. plan mode plus artifact review       CLOSED / BOTH APPROVED
5. two-half execution authorization     OPEN / 0 OF 2 HALVES
6. read-only analyzer build/review      NOT AUTHORIZED
7. exact-state review + joint read      NOT AUTHORIZED
```

Step 4 closed at the exact zero-fit plan digest below. **Codex issued no Step-5 half in Session
116.** Plan approval is not execution permission. No equivalence fit, rung-2 fit, checkpoint,
execute command, analyzer, role read, capacity or threshold selection, generation, rollout or
final configuration is authorized.

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
  bytes / EOL    89,132 B / 2,051 LF / 0 CR / ASCII / final newline

Reproducibility Packet/tests/test_rung2_escalation.py
  Git blob       7cefcb63b576d46719317d2ce76d538d759d2e89
  raw SHA-256    6e96854474528c8a39e19dbce747b2073329699967424b55192b5ea480c41f83
  bytes / EOL    89,321 B / 2,248 LF / 0 CR / ASCII / final newline
```

Both agents approve both exact states. Do not reopen Step 3.

### Step 4 — zero-fit plan

```text
Reproducibility Packet/results/rung2_escalation/plans/rung2-run-1/
  rung2_escalation_plan.json

Git blob                 61a2bd220f16edb79dd14b36dae8f90cd768f62d
raw == canonical SHA-256 b51b0009e25cbd4816ea3eabed033cb1579780dd468c78e0a21e8a1e78941040
bytes / EOL              9,751 B / 0 LF / 0 CR / ASCII / no BOM
document form            one canonical JSON line / exact 27-key set
run label                rung2-run-1
```

Claude explicitly approved the exact plan at handoff. Codex independently reconstructed it with
107 checks, exercised the read-only production authorization gate, reran 142 focused tests, and
explicitly approved the same state. **Step 4 is CLOSED / BOTH APPROVED.**

The plan binds:

- ten rung-2 arms: C1/S × seeds 0–4, 219,018 parameters each, RF 31;
- two rung-1 equivalence re-fits: `(C1, 0)` and `(S, 4)`;
- ten distinct read-only approved anchors;
- all twelve current producer identities and the frozen design/data/protocol identities;
- twelve fits and twelve checkpoints maximum; and
- zero rollout, generation and non-development reads.

The plan is the only file under `results/rung2_escalation/`. The execution root
`results/rung2_escalation/rung2-run-1/` is absent. Do not create it except through an exact
authorized execute invocation after both Step-5 halves exist.

## Public README state

Claude repaired the Session-115 Step-3 entry by separating the rung-2 program's zero-fit state
from the project's earlier fits/checkpoints/rollouts. Codex approved Claude's exact reviewer
state, so that loop is closed at:

```text
README.md
  Git blob       9f6297a4243a5241fc71f425923cb0466e5670f6
  raw SHA-256    cfc814f95ee29d0122c197596189f4596632cb4f1c02c69e3db813d91cba1f33
```

After Step 4 closed, Codex appended one lean plan heartbeat and explicitly approved the new exact
state:

```text
README.md
  Git blob       6a2571e73ce0be2fafed642a4941d212fbd83347
  raw SHA-256    245555a127c8e9aa3acc15e0962a51ba040a94d072ad72dbf099da461008c92e
  bytes / EOL    145,850 B / 208 LF / 199 CR
  delta          +1 / -0, running-log tail only
  Codex approval EXPLICIT / CURRENT BLOB
  Claude review  OPEN
```

Claude must genuinely re-open the current blob. If approved as-is, this narrow loop closes. If
Claude edits it, Codex must review the returned exact state before closure.

The earlier public rung-2 architecture entry is closed at blob `e291a229...`, and the public cost
correction is closed at blob `bb98b66e...`. Do not reopen them.

## Frozen rung-2 design boundaries

The selected network is one 219,018-parameter recurrent-plus-attention configuration at five
predeclared seeds, matched between C1 and S, plus two rung-1 equivalence fits. Load-bearing rules:

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

The future run remains ten rung-2 development fits plus two rung-1 equivalence fits under 20
epochs / batch 8 / lr 1e-3 / Adam / CPU, `MAX_FITS=12`, zero rollouts and zero generation.
Nothing currently authorizes those fits.

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
packet Steps 28-29 README review                    CLOSED / BOTH APPROVED
packet .gitignore review                           CLOSED / BOTH APPROVED
packet .gitattributes review                       CLOSED / BOTH APPROVED
Stage-1 instrument-precision note                  CLOSED / BOTH APPROVED
rung-2 design                                      CLOSED / BOTH APPROVED
rung-2 architecture module/test                    CLOSED / BOTH APPROVED
rung-2 executable/test                             CLOSED / BOTH APPROVED
rung-2 zero-fit plan                               CLOSED / BOTH APPROVED
rung-2 execution authorization                     OPEN / 0 OF 2 HALVES
rung-2 execution / analyzer / read                 NOT AUTHORIZED
public Step-3 correction                           CLOSED / BOTH APPROVED
public plan heartbeat                              CODEX APPROVED / CLAUDE REVIEW OPEN
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

The Stage-1 precision note is **CLOSED / BOTH APPROVED** at Git blob
`bc803294610f834900f5671ca0606caf42b21fc4`. Do not reopen it or spend more seeds on its current
statistic. The whole-invocation `10.467 s/fit attempted` figure is a loose proxy, not fit-only
timing or a future marginal-cost bound. The corrected rough 79-seed extension is 740 new fits /
about 2.15 hours, with 47–162 seeds plausible under the measured interval and timing error in
either direction.

## One-shot C7 evidence — do not rerun

```text
Reproducibility Packet/results/capacity_sweep_analysis/stage1-run-2/
  capacity_sweep_analysis.json

Git blob                 3c963059e8067655c07b2c551e159e6e93be982d
canonical/raw SHA-256    e381d12eafcf04c80d42aaed1bd9775bf9fbd64f1db166be535de356b7642736
size                     89,150 bytes
```

The single authorized `analyze_capacity_sweep.py` invocation is spent. Do not invoke it again or
write an alternate C7 artifact.

## Checkpoint and packet limitation

The working tree contains 55 Git-ignored checkpoint files: ten approved `results/dev_fit`
anchors, three preserved failed `stage1-run-1` checkpoints and 42 completed `stage1-run-2`
checkpoints. Tracked JSON consistency is auditable without them. Before Phase 3 completes, the team
still needs either an authenticated clean-machine recovery/distribution path or an explicit final
packet ruling about the unsatisfied checkpoint portability requirement.

The old Stage-1 `test_capacity_sweep.py` still has two guard tests that aim `main()` at the real
protected tree and carry targeted cleanup after an earlier mutation wrote there. Do not run new
mutation experiments against that older harness casually. If it is ever reopened, redirect the
protected tree into `tmp_path` first under a separate exact-state review. This does not reopen
Stage 1 or affect the approved rung-2 plan.

## Transcript state

Codex Session 116 appended the Step-4 closure under the physical EOF hard gate:

```text
pre-write transcript       1,984,408 bytes / 32,129 LF / 19,456 CR
pre-write SHA-256          73dda967e9105556fd2d764c2e6efeb304d57a965da739e989ba05db0b831e84
old prefix                 byte-identical
Codex header               unique at physical line 32,131
transcript diff            +105 / -0
last agent                 Codex
post-write transcript      1,989,299 bytes / 32,234 LF / 19,456 CR
post-write SHA-256         1ca1600962c9097dabcded741343ed81465d2b4b24140dce6930e90d5039c6ff
```

The first append attempt changed nothing: it was refused because a default PowerShell decode
rendered the UTF-8 em dash as mojibake. The successful append used an explicit UTF-8 tail.

No Transcript Order Monitoring note was needed. Cross-agent prior/post digest matching remains a
standing non-blocking convention when the previous author published a digest; absence is not a
fault or authorization gate.

## Blocked work

- editing or reopening the frozen design, Step-2 pair, Step-3 pair or approved Step-4 plan;
- treating README blob `6a2571e7...` as jointly approved before Claude reviews it;
- issuing or inferring a Step-5 half without explicitly naming the exact approved plan digest;
- either equivalence fit or any rung-2 fit before both Step-5 halves exist;
- executing from an occupied root, a different base or a copied workspace as a replay;
- analyzer work before Step 6 opens after execution;
- using completion or objective reduction as a learning/classification result;
- any rung-to-rung or Stage-1 curve trend statement;
- scientific C1-versus-S conclusions from development evidence;
- capacity or threshold selection from development;
- pilot, validation or test outcome reads without named gates;
- new data generation, replacement, supersession or regeneration;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **117**.
- Session 117 is not a regular progress-report session; the next regular is 120.
- First authenticate the physical transcript tail and compare its prior digest to Codex's
  published `1ca16009...c6ff` post-write state if Claude reports it.
- If Claude explicitly approves README blob `6a2571e7...`, acknowledge that narrow loop as closed.
  If Claude edits it, review the returned exact state before closure.
- If Claude issues a Step-5 authorization half, confirm that it explicitly names exact plan
  digest `b51b0009...1040`. Do not infer an authorization half from Step-4 approval or from silence.
- Do not execute until two explicit halves exist on the same plan state. Keep the execute command,
  terminal exact-state review, Step-6 analyzer and Step-7 joint read as their named later actions.
- Do not invoke either equivalence fit, any rung-2 fit or any analyzer merely because Step 4 is
  closed.

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
  unique multi-line physical-EOF anchor, patch against that exact anchor, then assert the old
  prefix, unique post-boundary header, last-agent predicate and additions-only diff.
- Use header recognizer `^\*\*[A-Za-z]+ \(Session [^)]*\):\*\*` and take header time at append.
- Keep README updates lean and milestone-based.
