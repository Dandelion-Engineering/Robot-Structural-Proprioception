# Codex - Human Report, Session 97

**Date and time:** 2026-08-08 14:10 PDT

**Phase:** Phase 2 - Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains
**278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Data generated: 0. Pilot /
validation / test reads: 0.** This session recorded one half of a future joint execution
authorization; it did not execute the plan.

**Progress-report session:** no. The next regular Codex report is Session 104 unless a phase
transition or approved Claim Sheet amendment triggers one sooner.

---

## Summary

Claude Session 97 independently approved the corrected capacity plan unchanged, closing Step 3
at exact plan blob `c048b54b...` / SHA-256 `bdf674d5...`. Claude also surfaced a real but
separate clean-machine limitation: the ten approved 32-channel anchor checkpoints are ignored by
Git, while the sweep reads them only from the fixed `results/dev_fit` namespace and the packet's
current regeneration instructions write to `results/dev_fit_reproduced`. I ruled that this is an
agent-side Phase-3 packet obligation, not a `director_requests.md` item. Disclosure alone cannot
satisfy the packet's fresh-environment gate; the agents must provide an authenticated way to
reconstruct or obtain the exact approved checkpoint bytes before calling the packet complete.

I also reviewed and explicitly approved Claude's Session-96 progress report unchanged. After an
independent ten-checkpoint audit and a green 1,765-test packet run, I issued Codex's half of the
separate Step-4 authorization for the jointly approved plan. Claude's matching half remains
absent. No execute command, fit, checkpoint, non-development read, generation or rollout is
authorized yet.

## Startup and current-state reconciliation

I first checked `.agent-session.lock`. It was absent, so I created it before reading any project
file. `CODEX_HOME` was unset in the shell, so I used the configured Codex home path
`C:\Users\cresp\.codex` for the required automation memory.

I then followed `AgentPrompt.md`: read the project details, Codex continuity, every
Codex-participating chat summary and active-chat state, Claude's HumanReport97, the latest
physical Phase-2 transcript tail, and the review-cycle, reproducibility-packet,
director-requests, research-progress-report and live-run README playbooks. I also applied the
stored append-only-chat hard gate before writing to the live transcript.

The live branch had advanced past the automation note to Claude Session 97 at commit `e2a09cf`,
so the repository and physical transcript tail controlled. The worktree was clean except for the
ignored session lock.

## Step-3 closure intake

Claude's independent review explicitly approved the same plan bytes Codex approved in Session
96:

```text
Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json
  Git blob                 c048b54b8081271d76a6adacf8526d201c446c17
  canonical/raw SHA-256    bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5
  physical state           13,786 B / one canonical JSON line / no final newline
```

Claude independently re-derived the plan without importing its producer, measured byte
determinism across two scratch destinations plus the published artifact, and drove the
authorization gate against one valid plan plus twenty-one neighbouring mutations. The exact
state is unchanged and both approvals now name it, so Step 3 is closed. I did not treat that
closure as fit authorization.

## Checkpoint-portability ruling

I confirmed Claude's measurements at source and on disk:

- no `.pt` file is tracked by Git;
- the packet `.gitignore` excludes all `.pt` files;
- execute mode reads approved anchors only from `results/dev_fit`;
- the CLI offers no arbitrary checkpoint-directory override;
- the packet's current regeneration and analysis steps use `results/dev_fit_reproduced`; and
- the ten approved checkpoint files are present only in the current working tree.

The ruling is:

1. **No director request.** Nothing requires Randy's identity, access, account or judgment, so
   `director_requests.md` remains unchanged.
2. **No local-execution block.** The current development measurement may run locally once both
   authorization halves exist, because all ten exact approved anchors are present and bound.
3. **A real Phase-3 packet obligation remains.** Before fresh-environment completion, the agents
   must either prove that regeneration reproduces all ten raw checkpoint digests and install
   them into the fixed approved namespace through an authenticated step, or provide the exact
   approved bytes through a documented authenticated packet data path.
4. **Disclosure alone is insufficient for packet completion.** If neither route works, the
   limitation must be disclosed and the packet must remain explicitly incomplete for the clean-
   machine capacity-sweep path. C9 should not be weakened with a free path override.

## Claude Session-96 progress report review

I reviewed `agents/Claude/Progress Reports/Progress Report Session 96.md` against the progress-
report and review-cycle playbooks:

```text
Git blob                 c824173cb0d75bd7e10ca5b20567004af89a0ba7
raw SHA-256              eeeaf53d8ef8074fb74c4b58bd4c374e88462386844154eae6246bbc3f27e157
physical state           13,935 B / 231 lines
```

The report is correctly triggered at Claude Session 96, is readable at the director-facing bar,
explains finding AT and its authorization impact accurately, states the twelve-session gap since
the last new scientific number rather than hiding it, gives the Slot-8 artifact an honest no-
update, and preserves every reserved-data and confirmatory boundary. I explicitly approved the
exact report bytes unchanged in the Phase-2 chat. The report loop is closed.

## Local Step-4 preflight and Codex authorization half

I independently compared every plan anchor with both the approved fit ledger and the physical
checkpoint bytes:

```text
approved plan SHA-256                  bdf674d5...1c0a5
plan / ledger / physical anchors       10 / 10 exact matches
all packet .pt files                   10, all under results/dev_fit
foreign .pt files                      0
delivered data root                    present
results/capacity_sweep/stage1-run-1    absent
config/config.json                     absent
full packet suite                      1,765 passed in 119.21 s
```

I then issued Codex's half of the separate Step-4 authorization for exactly one execution of
plan SHA-256 `bdf674d5f717e5256904ca12d9670a8e02ca0351fb9b5d625a38809d1bf1c0a5`,
run label `stage1-run-1`, in the current tree with packet-relative base
`results/capacity_sweep` and the ten pre-existing approved checkpoints.

The maximum authorized budget is two C9 equivalence fits plus forty curve fits, 42 checkpoint
writes, zero generation, zero rollouts and zero non-development reads. C9 must pass before any
curve arm. This half is conditional on a final immediate recheck of the exact anchors, absent run
root, unchanged plan/code state and absence of another packet/root writer.

**Claude's matching authorization half does not exist. No execute command is currently
authorized.** C7 construction, later-role reads, capacity selection, threshold work, Stage 2,
final config, generation, rollouts and confirmatory use remain blocked.

## Transcript hard gate

The Phase-2 transcript append used Claude's exact physical EOF state as the boundary:

```text
pre-write bytes       1,676,645
pre-write lines       26,909
pre-write SHA-256     dd317527adb02326de68ea5c49db6f7b85b9ea10e28cb0f7e15296f8d8fdcf01
post-write bytes      1,680,736
post-write lines      26,984
post-write SHA-256    99b4a43fa56fd957f440d16bc3c2ab69ce1ff307c8a699a6721aede7df4ac526
prefix retained       exact
new header            unique at line 26,911, after the recorded boundary
Git diff              +75 / -0
physically last       Codex
```

No Transcript Order Monitoring note was required.

## Public communication

I appended one lean Live-Run README milestone. It records that one of two authorization halves
now exists, training is still blocked, the ten-anchor preflight passed, and the clean-machine
anchor path is an open Phase-3 packet obligation. It does not imply that a fit or result exists.

## Files created or updated

Created:

- `agents/Codex/Session Summaries/HumanReport97.md` - this report.

Updated:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  - append-only portability ruling, Claude progress-report approval and Codex Step-4 half.
- `README.md` - one lean one-of-two-authorization milestone.
- `agents/Codex/README.md` - current navigation and exact-state corrections.
- `agents/Codex/Summary of Only Necessary Context.md` - completely rewritten resume state.

Reviewed and deliberately unchanged:

- `Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json`.
- `Reproducibility Packet/scripts/utils/capacity_sweep.py`.
- `Reproducibility Packet/tests/test_capacity_sweep.py`.
- `Reproducibility Packet/protocol/capacity-escalation-v0.1.md`.
- `Reproducibility Packet/README.md` - the portability gap is recorded for Phase 3; the current
  Phase-2 runbook was not silently amended during an execution-authorization decision.
- `director_requests.md` - no director-only work was found.
- `.gitignore` and `Reproducibility Packet/.gitignore` - existing rules cover the lock, caches,
  environments and generated checkpoints.

## Next steps

1. Claude independently decides whether to issue the matching Step-4 authorization half naming
   plan SHA-256 `bdf674d5...1c0a5`.
2. Until that exact half is physically recorded, no execute command may run.
3. If both halves exist, the runner rechecks anchors, plan/code identity, absent run root and
   writer isolation, then performs the single authorized invocation.
4. The exact result and equivalence artifacts require two-agent same-state review before C7 or
   any interpretation.
5. Phase 3 must resolve the clean-machine approved-checkpoint path before the packet can claim
   fresh-environment completion.
6. The next Codex session is Session 98. The next regular progress report is Session 104 unless
   an event trigger fires sooner.

-- Codex
