# Codex — Human Report, Session 81

**Date and time:** 2026-08-05 22:31 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.
**Progress-report session:** no. The next regular Codex progress report is Session **88**.

---

## Summary

Claude Session 81 explicitly approved the development-fit contract blobs Codex returned
in Session 80. I accept that same-state approval, so the four-round contract loop is
**closed** at:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py
  bd2c0d080f3046837af6fc38232b530749238e4c
Reproducibility Packet/tests/test_dev_fit_contract.py
  fbd941b592436d0303b2ddd6ec6c69906d08bd88
```

I ruled Claude's Finding G as option **(b)**: keep the already-closed contract's generic
`row_disclosure` field free-text, while the trainer passes only
`DevRowCensus.disclosure()`. The trainer test pins that producer behavior and the absence
of `/` and `\`. I did not reopen or edit the contract.

I then reviewed Claude's new trainer and tests. I reproduced a causal future-information
leak and blocked the original state. The review also found missing dataset authorization,
payload-integrity, code-identity, partial-failure provenance, runtime-protocol and
terminal-exit guards. I corrected those executable defects and added five focused tests.

One scientific design question cannot be repaired by implementation judgment: the
delivered development role spans both an ordinary trajectory and a diagnostic trajectory,
but the trainer applies one global window to every row. The 1,136 held-decision step is
from a later bounded-contact screen and is not authority for the whole delivered base
dataset. The reviewer state therefore leaves the production training-window policy unset
and refuses even plan mode until Claude proposes and both agents review an explicit
ordinary/diagnostic policy.

No fit, checkpoint, data generation, rollout, later-role outcome read, threshold choice or
final-config action occurred.

## Exact review input and decision

Claude handed off:

```text
dev_fit_trainer.py       275a7a50752bd1ab5508ee85594dc733c1e284dd
test_dev_fit_trainer.py  80d9722fdbedb04b2ad6d6b2cd755a1eeec749da
focused tests            15 passed
full packet suite        1,482 passed in Claude's session
fits / checkpoints       0 / 0
```

I **block** those exact blobs. The reviewer-edited state is:

```text
Reproducibility Packet/scripts/utils/dev_fit_trainer.py
  fd2c8c9b5ce87f701e78b2bd08d21285799d3afd
Reproducibility Packet/tests/test_dev_fit_trainer.py
  9d9455b712367a8fbfcf92225889a355f43b892b
```

These bytes are intentionally fail-closed and require Claude owner re-review. They are not
approval to fit: their production origin/decision authorization is unset, so plan and fit
both refuse with zero fits.

## Findings and corrections

### Finding H — persisted future delivery crossed the training boundary

`ObservedRecord` intentionally retains measurements whose `availability_time_s` is after
an earlier decision. The original `window_record()` sliced the stored arrays but did not
reapply the online availability cutoff. A direct probe placed a valid `q_obs` value one
second after the held decision; it remained valid and visible to the network.

The corrected window path masks every channel with
`availability_time_s <= decision_time_s`, combines that predicate with the persisted
validity mask, and replaces unavailable values with NaN. The regression proves the
future-delivered sample is invalid and absent from the training tensor.

### Finding I — the trainer described arbitrary data instead of enforcing authorized data

The original accepted whichever data root and manifest it was given, recorded the
manifest digest and first selected row's config, and then loaded `.npz` files directly.
It neither pinned the delivered partition nor used the packet's role-index/payload hashes.

The correction pins and checks, before payload access:

```text
root name            gate3-base-dev-pilot-val-c1-s
manifest raw SHA256  55ea5f0e74ddd24b05eafc51a2b9fc424eda99eac1901534946f42b6012ebe12
config identity      dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56
labels index         a7c700e53d917f2ddb256521af3c23bba6f7ec6d6f3af967d14ca9aad3a559f8
C1 index             f0cc92bf33f7e06f8ac09e4ac0dffd86d567b445de07b049a9475b01f5dff716
S index              fa790f9d03b38d246c7e656164cbbee1ebe33f51c122d91edbf3dc72d526dd00
```

Production payload access now goes through `DeployableObservationLoader` and
`RolePayloadLoader`, which check every payload against those role indexes. A well-formed
lookalike dataset refuses before fitting.

### Finding J — checkpoint code identity was incomplete

Only trainer, contract and network files were named even though config validation, window
semantics, role loading, record shapes and storage hashes also determine the fit. The
identity now covers eight runtime modules and is computed once for the plan and all ten
arms:

```text
dev_fit_trainer.py  dev_fit_contract.py  attribution_net.py  config_contract.py
estimator.py        role_contract.py     schema_types.py     storage_contract.py
```

### Finding K — partial checkpoints could lack recorded provenance

The original wrote the checkpoint before provenance validation. On a later arm failure,
the result document named completed `(suite, seed)` pairs but omitted their checkpoint
records. The correction serializes the checkpoint in memory, computes its raw digest,
builds and validates provenance, then writes it. Every partial result now includes the full
record for every completed arm, including checkpoint digest, example count, loss history,
role-index hashes, code identity and training protocol.

### Finding L — runtime training choices and failures were under-specified

Epochs, batch size, learning rate, device, decision step/time and availability cutoff
were runtime choices without per-checkpoint provenance. A non-finite loss could proceed
to serialization, and several device/runtime/serialization failures could escape without
a named result artifact.

The correction records one validated `TrainingProtocol` identically in the plan, every
arm and every terminal document; refuses non-finite losses and weights; accepts only
available CPU/CUDA devices; and converts training and checkpoint serialization runtime
failures into named fail-loud exits without persisting caller-controlled messages.

### Finding M — the incomplete-plan terminal path was not actually driven

The original test called `require_complete_matched_plan()` directly even though the module
claims each `main()` exit is driven and its artifact read back. The replacement mutates
the executable iterator to omit the S arms while leaving the contract's independent
expected plan intact, then verifies the real `X_PLAN_INCOMPLETE` artifact and all five
completed C1 provenance records.

## Blocking training-window finding

The authorized manifest metadata contains:

```text
trajectory_dev_ordinary_a      C1 76 / S 76
trajectory_dev_diagnostic_b    C1 76 / S 76
total                          C1 152 / S 152
```

`trajectory_dev_ordinary_a` has no diagnostic probe. The later bounded-contact held
decision at step 1,136 does not define this base dataset's global training slice. Protocol
P's prospectively fixed diagnostic window `[1000, 1768)` is a different object and applies
to the diagnostic universe. The earlier model wire check's slice ending at 1,600 was
explicitly illustrative. None licenses `[368, 1136)` across all 304 rows.

The production constants `DEVELOPMENT_WINDOW_ORIGIN_STEP` and
`DEVELOPMENT_DECISION_STEP` therefore remain `None`. A focused regression proves that a
caller-supplied origin cannot convert an unset scientific policy into an executable plan.
Synthetic tests monkeypatch a fixture policy only to exercise the downstream mechanics.

Claude's next revision must propose and implement a jointly reviewable policy that:

- maps both ordinary and diagnostic trajectories to causal training examples, or
  explicitly justifies a narrower census;
- keeps C1/S windows and counts matched;
- reproduces the online availability boundary;
- states how many windows each persisted run contributes; and
- records the exact schedule in every checkpoint/result.

## Verification and evidence boundary

```text
future-availability probe            reproduced before correction; masked after
focused trainer tests                20 passed in 3.13 s
focused tests under python -O        20 passed in 3.12 s; expected warning only
full packet suite                    1,487 passed in 124.66 s
compileall                           clean
git diff --check                     clean
source diff from Claude              +436 / -102
test diff from Claude                +272 / -27
real metadata reads                  manifest/config/schema/three role-index CSVs
real .npz payload reads              0
fits / checkpoints / generation     0 / 0 / 0
rollouts this session                0
final config/config.json             absent
```

The metadata hashes above were checked read-only against the delivered files. Production
loader construction read the role indexes but opened no outcome payload.

## Transcript integrity

The exact handoff was appended to the active Phase-2 transcript against a complete,
programmatically verified unique EOF anchor. Before the write:

```text
physical bytes    1,385,061
physical lines    21,820
SHA-256           74cadceead8998f1078868165941aaecc4cd9b1693f029b261735bb9109df893
```

After the write:

```text
physical bytes    1,393,189
physical lines    21,963
SHA-256           fb7129644f56d27f2c30ff546ab61d9b863b583a62b0ee213f5cdd6680c41051
transcript diff   +143 / -0
```

The complete pre-write byte prefix retained the exact pre-write SHA-256; the Session-81
header occurs exactly once after that boundary; Codex is physically last; and
`git diff --check` is clean. No ordering repair or monitoring-thread entry was needed.

## Public README heartbeat and boundaries

The root Live-Run README is unchanged. A blocked internal trainer review is not a finished
artifact, phase closure, noteworthy research result or public claim. The project remains
Phase 2 / `In Progress`.

All of the following remain blocked absent separate explicit authorization:

- any development fit until the trainer executable loop closes;
- pilot, validation or test outcome reads;
- new data generation, replacement, supersession or regeneration;
- a second payload-extension invocation or further payload measurement;
- final `config/config.json` materialization; and
- confirmatory identities, generation, reads or claims.

## Files created or updated

- `Reproducibility Packet/scripts/utils/dev_fit_trainer.py` — causal masking, exact data
  authorization, production hash loaders, full code/protocol/provenance recording,
  fail-loud runtime guards and an unset production window-policy gate.
- `Reproducibility Packet/tests/test_dev_fit_trainer.py` — five new regressions and stronger
  exit/provenance assertions.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — append-only review decision and owner handoff.
- `agents/Codex/Session Summaries/HumanReport81.md` — this report.
- `agents/Codex/README.md` — workspace index and active-state descriptions refreshed.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten resume state.

## Next steps

1. Claude genuinely owner-reviews trainer blobs `fd2c8c9b...` / `9d9455b7...`.
2. Claude explicitly preserves or contests each reviewer correction.
3. Claude proposes and implements the missing ordinary/diagnostic training-window policy.
4. Claude hands the resulting executable/test blobs back for Codex same-state review.
5. Only after that exact executable loop closes may the ten predeclared development-only
   C1/S fits run.

The central learned-model measurement still has not run. This session made the fitting
boundary safer and exposed a missing design decision; it did not produce evidence about
the structural-proprioception hypothesis.
