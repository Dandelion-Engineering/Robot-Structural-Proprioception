# Codex — Human Report, Session 73

**Date and time:** 2026-08-04 15:17 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **127**. Project lifetime Protocol-P-related total is now **278**.

---

## Summary

This session closed the payload-boundary execution-authorization gate, ran the single
authorized invocation, and independently audited its persisted development result.

Claude Session 73 issued the first half of Step 4. I re-opened the frozen protocol,
official plan, executable, current Claim Sheet, and Claude's pre-rollout evidence. My
zero-rollout probe independently confirmed the named plan digest, a byte-identical X0E
recomputation, all four pinned replay inputs, the unique replay reservation and manifest
row, the 20/38 reference shapes, and the 3,203-file inventory floor. The 170 focused
tests also passed normally and under optimized Python. I then issued a matching half:
one Step-5 invocation, once, in `X0E/XR/XA/XM-C/XL/XM-B/XZ` order, with 0–127 physical
rollouts exactly as the pre-registered exit table schedules and the Section-3.3 replay
rollout authorized by name. A second invocation would require a new joint authorization.

The executor ran as a hidden background process. During its run I performed no tests,
Git operations, editor writes, or repository diagnostics; I polled only for the canonical
result artifact. The run completed at the full 127-rollout cost:

```text
Reproducibility Packet/results/payload_boundary_extension/payload_boundary.json
canonical SHA-256  7746372f1adea931722cf547adee36489971493c4e1b5217f588d4c6d1c9aa04
Git blob          2cf19daa385ec3f96c91acca9de3747d7ba0f115   388,550 bytes

outcome           X_CASE_EMPTY (R10)
mass coverage     COMPLETE
replay            PASS, 1 rollout
anchor            X_ANCHOR_PASS
extension         126 rollouts
total             127 rollouts
```

I independently reconstructed and explicitly approved this exact result state. Claude
still owes the required second audit and same-state approval. Therefore the measurement
may not yet inform Amendment A2, assignment replacement, final config materialization,
or confirmatory work. No further payload-extension execution is authorized.

## What the result says at its exact development boundary

All seven payload masses produced safe, valid, complete ladders. No mass was excluded;
all within-mass sets are prefixes and the sets shrink monotonically with payload:

```text
mass kg   TESTABLE_SET
0.025     {0.35, 0.40, 0.45, 0.50}
0.050     {0.35, 0.40, 0.45}
0.075     {0.35, 0.40}
0.100     {0.35}
0.125     {0.35}
0.150     EMPTY
0.200     EMPTY
```

The ordered classifier reaches `X_CASE_EMPTY` because the two heaviest measured masses
have empty sets. `role_retained` is false for every mass: even the nonempty sets contain
none of that mass's own split-reserved severities. The persisted Option-B cap is null.

This is still development evidence from the fixed dev context, one environment, one
contact profile, one trajectory, and one probe. It does not establish the project
hypothesis, a confirmatory result, a mechanism for payload attenuation, or a fitted curve.
Read only through the pre-registered Section-9.5 table—and only after Claude agrees with
the exact bytes—the result would license Option C with a payload-bounded non-transfer
shape that names 0.150 and 0.200 kg as empty. It does not license Option A and does not
satisfy Option B's initial role-retaining-prefix rule. I did not make the separate joint
Amendment-A2 design choice in this session.

## Independent artifact audit

The audit parsed the result without importing the payload-extension executable and
rebuilt its claims directly from the persisted ledger:

- raw bytes equal canonical UTF-8 JSON and hash to `7746372f...9aa04`;
- all 126 physical keys and all 126 provenance stamps are distinct;
- the eight identity classes reproduce the exact `77/7/7/7/7/7/7/7` sharing partition;
- every provenance digest recomputes from its persisted canonical identity payload;
- every one of the 28 null distances per mass, higher-method Q95, doubled threshold,
  70 ladder distances, margins, verdicts, prefix flags, role-retention flags, and the
  R10 classifier recompute from the 126 coefficient vectors;
- all 532 logical references join to physical-ledger keys, with stage counts
  `XA=18`, `XM-C=48`, and `XM-B=60`;
- X8's 168 cross-mass comparisons recompute with minimum distance
  `0.135079151914`, confirming that the payload override was live;
- the ordinary-path replay and all nine constrained anchor comparisons pass;
- persisted rollout time is `3680.708815 s` including replay, and the artifact reports
  the exact 127-rollout count; and
- all 11,015 decoded JSON string positions are free of detected absolute paths, while
  final `Reproducibility Packet/config/config.json` remains absent.

Post-result verification:

```text
focused normal              170 passed in 3.05 s
focused python -O           170 passed in 3.04 s (expected pytest warning only)
full packet               1,306 passed in 121.83 s
compileall                   clean
```

## Cross-review and decisions

I read Claude's `HumanReport73.md` and its Session-73 authorization turn. Claude found
that the replay gate's ephemerality bracket would consume the authorized rollout before
detecting an incidental file write. Its zero-rollout measurements closed the normal
lazy-import and MuJoCo-log mechanisms, but a concurrent writer remained an operational
risk. I accepted that analysis and enforced the resulting no-writer rule throughout the
run. The gate passed, so no incidental write occurred inside its watched inventory.

I also accepted Claude's correction to the earlier shorthand "authorize one replay
rollout." Step 4 authorizes one execute invocation and *also* names the replay rollout;
otherwise Step 5's 126 extension measurements would remain unlicensed. My authorization
half states the same scope explicitly, so the two halves agree.

## Challenges and how they were handled

The first version of my zero-rollout authorization probe asked the executable module for
`MIN_WATCHED_FILES`, but that constant belongs to the imported replay helper. I corrected
the probe to use the protocol's literal floor of 100 and reran the entire zero-rollout
batch; it measured 3,203 watched files and all checks passed. This was a probe error and
did not touch execution state.

The long-running executor was deliberately not attached to a console pipe. It ran hidden
with redirected logs outside the repository, while the session polled only the result
path. Once the result appeared, I confirmed the executor had exited before resuming tests
or Git operations.

## Transcript and public-state handling

The Step-4 authorization append used a unique verified physical EOF block and landed once
after the recorded 19,332-line boundary. The result-audit append used the same hard gate
after a new 19,391-line boundary and landed once at line 19,395. The transcript's final
session diff is additions-only at `+147/-0`; Codex is physically last at line 19,479.

The payload run is a noteworthy public milestone, so I appended one lean Live-Run README
entry. It reports the complete development result, the two empty masses, the full
127-rollout cost, and the exact boundary that the second audit and any A2/config decision
remain open. The Phase-2 `In Progress` banner remains correct.

## Files created or updated

- `Reproducibility Packet/results/payload_boundary_extension/payload_boundary.json`
- `README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/Session Summaries/HumanReport73.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

## Next steps

1. Claude independently audits exact result digest `7746372f...9aa04` and explicitly
   approves or blocks the same bytes.
2. Only after that result loop closes may the agents make the separate joint Amendment-A2
   design choice. No further payload-extension execution is authorized.
3. Assignment replacement, final `config/config.json`, and all confirmatory work remain
   downstream and blocked.
