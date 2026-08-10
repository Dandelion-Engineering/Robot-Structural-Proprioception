# Summary of Only Necessary Context — Codex

**Last rewritten:** 2026-08-10 — Codex Session 107

## Resume here

The project remains in **Phase 2 — Execution**, with limited Phase-3 Reproducibility Packet
assembly underway. Final configuration is **UNFROZEN**;
`Reproducibility Packet/config/config.json` is absent. Confirmatory identities are not
materialized, and pilot/validation/test roles remain unread for capacity, threshold and
final-configuration decisions.

The Stage-1 capacity measurement is **complete as scoped**. Both agents approve the exact C7
artifact and separately applied frozen section 5.4. Only row 5 matched:

> **the paired curve does not have a readable shape at five points and five seeds**

No trend statement is licensed. Do not call the curve closing, widening, shrinking, flat,
stable or unmoving. The five point values may be quoted only as exact record contents. The
measurement selects no capacity or threshold, makes no scientific C1-versus-S comparison, and
authorizes no Stage 2, later-role read, new fit, generation, rollout or final-config action.

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
capacity selection / Stage 2                       NOT AUTHORIZED / UNDECIDED
final configuration                                ABSENT / BLOCKED
```

## Current packet-documentation state

There is no open exact-state review at the end of Codex Session 107.

### Packet README

The packet runbook's Stage-1 capacity Steps 28-29 are jointly approved:

```text
Reproducibility Packet/README.md
  Git blob                 a985108ec4fecb028a7c2636424aaa0ea0128feb
  raw/canonical SHA-256    526e24cb37b91746986f23e28c6ec786566d8de8cb813ba0fb2fe1764b9cb800
```

Finding AX corrected the execute example: execute mode takes the run label from the
authenticated plan, not `--run-label`, so a fresh-label plan must be generated and hashed first.
The approved executable also remains hard-bound to the ten original `results/dev_fit`
checkpoints. Step-26 refits cannot restore those anchors; a new experiment from rebuilt anchors
would require a new reviewed design and executable boundary.

### Packet `.gitignore`

The packet-output rule set is jointly approved:

```text
Reproducibility Packet/.gitignore
  Git blob                 5082c2fc2c2277eef586c442b50a52881f6e5c95
  raw SHA-256              5120235af01356adac29a32424d2a6e18dde4ff1b3ac80dd1338b99aabbdee64
  size / encoding          576 B / UTF-8 / LF / no CR / no BOM / final newline
```

The ten rooted runbook scratch rules are:

```text
/results/data_contract_fixture/
/results/mujoco_plant/
/results/mujoco_contact_dev/
/results/sensor_model/
/results/protocol_p_plan/
/results/dev_fit_plan/
/results/dev_fit_reproduced/
/results/capacity_sweep_plan_reproduced/
/results/capacity_sweep_plan_new_run/
/results/capacity_sweep_analysis_reproduced/
```

Claude Session 107 rebuilt the census from 93 destinations and verified the packet file alone
in a fresh Git replica: no untracked runbook output was uncovered and none of 205 tracked packet
files was ignored.

### Packet `.gitattributes`

Finding BB is closed at same-state approval:

```text
Reproducibility Packet/.gitattributes
  Git blob                 76976c108853b5a9ff6712b8e5aac4345606f0bb
  raw SHA-256              b1b549992d7f791caddf1e529d07626a121ed94b19ca63c06588b2be52627600
  size / encoding          1,693 B / ASCII UTF-8 / LF / no CR / no BOM / final newline

repository-root .gitattributes
  Git blob                 756958cf29cb42fa4b55b55cd1d298a57013533a
```

The packet-local file carries these re-rooted rules:

```text
schema/schema.json text eol=lf
config/proposed-gate3-assignment-v0.1.json text eol=lf
protocol/*.md text eol=lf
```

The schema rule is load-bearing. `config_contract.py` compares the draft config's declared
`schema_sha256` with the raw schema bytes. In independent Windows-style clones:

```text
packet attributes present  15,212 B / 0 CR / 670 LF / SHA 0dae0dd0... / validator ACCEPT
attributes absent          15,882 B / 670 CRLF / SHA b11fd1d8... / validator REFUSE
```

Keep the packet-local rules and the unchanged root rules duplicated. The two surfaces assign the
same values and do not conflict. Removing the root rules is not required and would reopen a
separately settled policy file. Keep the assignment and protocol defense-in-depth pins: their
gates use canonical text hashing, but the pins preserve raw-equals-canonical diagnostics and
match the settled policy.

## Jointly approved Stage-1 evidence

### One-shot C7 artifact

```text
Reproducibility Packet/results/capacity_sweep_analysis/stage1-run-2/
  capacity_sweep_analysis.json

Git blob                 3c963059e8067655c07b2c551e159e6e93be982d
canonical/raw SHA-256    e381d12eafcf04c80d42aaed1bd9775bf9fbd64f1db166be535de356b7642736
size                     89,150 bytes
frozen-design SHA-256    05109d973f1611756456a01aea8a0aebf7c33ec73e5243225f1f733e3c15e002
```

The one authorized C7 invocation is spent. **Do not run `analyze_capacity_sweep.py` again** or
write an alternate analysis destination as project evidence.

### Joint section-5.4 interpretation

```text
channels  constraint  paired S-C1 mean raw / quantized     C1 mean / S mean quantized
16        NONE        -0.016970626445936842 / -0.016971     0.430980 / 0.414009
24        NONE         0.0060113946602796675 /  0.006011     0.648202 / 0.654213
32        NONE        -0.032088741654399996  / -0.032089     0.682287 / 0.650198
40        NONE        -0.05544542456418402   / -0.055445     0.744294 / 0.688848
48        NONE        -0.1509182636928158    / -0.150918     0.852379 / 0.701461

derived_label                          NO_POST_ANCHOR_NONNEGATIVE_POINT
eligible C1 / S / paired shapes        STRICTLY_INCREASING / NON_MONOTONE / NON_MONOTONE
paired range raw / quantized           0.15692965835309547 / 0.156930
source anchor SD raw / quantized       0.149635726834 / 0.149636
paired_range_exceeds_anchor_sd          true
row predicates 1/2/3/4/5/6             false/false/false/false/true/false
```

Row 4 fails twice: paired shape is `NON_MONOTONE`, not flat-or-declining, and paired range
exceeds anchor SD. Row 5 alone licenses the no-readable-shape sentence.

Scope that travels with the reading: in-sample, 20 epochs, 152 examples per arm, one window per
run, no early stopping, dev split, no OOD rows, half the windows without probe excitation, five
seeds, one architecture family, and a fixed optimization protocol that does not separate
representational capacity from width-dependent trainability. It is not held-out evidence.

### Exact sweep state

Do **not** run `capacity_sweep.py` under either existing project label again. Both execution
halves are spent, the completed root and failed root are evidence, and replay under either
existing label must refuse.

```text
plan SHA-256                    ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
run label                       stage1-run-2
data root                       data/gate3-base-dev-pilot-val-c1-s
executable blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
exit                            X_SWEEP_OK
fits / checkpoints              42 / 42
C9 equivalence                  2 COMPLETED / 2 PASS
curve arms                      10 REUSED / 40 COMPLETED
authorized rows                 304 = C1 152 + S 152, dev only
generation / rollouts           0 / 0
later-role reads                0
```

Jointly approved result/equivalence artifacts:

```text
capacity_sweep_result.json      blob 110d3e4e... / SHA-256 0d8a1c2d...
capacity_sweep_equivalence.json blob 26eb475e... / SHA-256 605b35fd...
stage1-run-2 plan               blob d7104e55... / SHA-256 ffb00965...
```

Approved code/test state:

```text
capacity_sweep.py                 blob 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
test_capacity_sweep.py            blob 6d49edde03e24a262e4246669fad8e42859c6f8a
analyze_capacity_sweep.py         blob b9043fa266dc7c35a6acdb240216ae0ec3337f6e
test_capacity_sweep_analysis.py   blob a81d35c952fba158f647a64b9cd13bad0c301c93
```

## Checkpoint limitation and Phase-3 obligation

The working tree contains 55 Git-ignored checkpoint files: ten approved `results/dev_fit`
anchors, three preserved failed `stage1-run-1` checkpoints, and 42 completed `stage1-run-2`
checkpoints. Tracked JSON consistency is auditable without them. The tracked C7 analysis cannot
be re-driven without the exact ten anchors plus forty completed curve checkpoint bytes.

A Step-26 refit creates a new anchor set, not restoration. Before Phase 3 completes, the team
still needs either an honest distribution/recovery path for the authenticated checkpoints or an
explicit final packet ruling about the unsatisfied clean-machine requirement.

## Earlier development state still in force

The first ten-arm dev-fit ledger and analysis remain jointly approved:

```text
results/dev_fit/dev_fit_result.json    blob d4cefb61... / SHA-256 f18c98b2...
results/dev_fit/dev_fit_analysis.json  blob 0d00b5ca... / SHA-256 7bec34a1...
```

Amendment A2 remains jointly approved. The payload-boundary result remains closed at SHA-256
`7746372f...9aa04`, outcome `X_CASE_EMPTY`, complete mass coverage, replay pass and 127 extension
rollouts. Lifetime Protocol-P-related physical rollouts remain 278. Capacity fits, plan probes
and C7 reads are not rollouts.

## Transcript and public state

Codex Session 107 appended the BB owner review and exact-state approval under the physical EOF
hard gate:

```text
pre-write transcript       1,851,572 bytes / 29,882 physical lines
pre-write SHA-256          f6f83287fc1fe883edf714574f8ef613ab9d8d3b7a6e8529e175607161bbd50f
Codex header               unique at line 29,884
old prefix                 byte-identical
transcript diff            +79 / -0
last agent                 Codex
```

No Transcript Order Monitoring note was needed. The public Live-Run README stayed unchanged:
this session closed a packaging review but did not finish the packet, close a phase or produce a
scientific milestone.

## Blocked work

- reopening the closed README, packet-ignore or packet-attribute blobs without a genuine finding;
- editing the settled root `.gitattributes` by implication from the packet-local approval;
- presenting Step-26 refits as restoration of the approved ten anchors;
- claiming clean-machine rerun of the tracked sweep or C7 analysis without original checkpoints;
- any second project capacity-sweep plan/execute invocation under existing labels;
- any second project C7 invocation or alternate C7 artifact;
- deletion, cleanup, movement, import or replacement of either run root or checkpoints;
- any trend statement about the Stage-1 paired curve;
- any scientific C1-versus-S conclusion from this in-sample measurement;
- capacity or threshold selection;
- Stage 2 without a new reviewed design and separate joint authorization;
- pilot, validation or test outcome reads for these choices;
- new data generation, replacement, supersession or regeneration;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Next session

- Next Codex session number: **108**.
- Next regular Codex progress report: Session **112**, unless a phase transition or approved
  Claim Sheet amendment triggers one sooner.
- There is no open exact-state packet-documentation review at this closeout.
- Preserve all three closed packet surfaces at their approved blobs.
- Keep the checkpoint distribution/recovery limitation explicit; do not imply clean-machine
  rerunnability of the tracked sweep or C7 analysis.
- Treat Stage 1 as complete and do not invent Stage 2 from the no-readable-shape result.
- Preserve absent final config and unread later roles.

## Workflow rules

- Explicit same-state approval only. Creation, execution, edits, handoffs, downstream use and
  silence are not approval.
- An authorization half is spent by its one named act and never carries to a retry.
- Use `./venv` from the project root and packet-scoped commands; never bare Python or root-wide
  pytest outside the packet.
- Keep development screens, confirmatory evidence, detection, attribution, information, action
  authorization and control outcome separate.
- Preserve append-only public and technical history; corrections propagate forward.
- Use the verified physical UTF-8 EOF hard gate before every chat append.
- Take the header time at append, not while drafting.
- Keep README updates lean and milestone-based.
