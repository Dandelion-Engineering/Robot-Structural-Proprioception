# Codex — Human Report, Session 105

**Date and time:** 2026-08-09 22:13 PDT

**Phase:** Phase 2 — Execution, with Phase-3 packet assembly work

**Progress-report session:** No. The next regular Codex progress report is Session 112 unless a phase transition or approved Claim Sheet amendment fires one sooner.

---

## Summary

Claude Session 105 added the previously missing Stage-1 capacity-sweep instructions to the Reproducibility Packet runbook. I reviewed the exact handed-off README against the packet playbook, the real command-line parsers, and the checkpoint-loading path. The five-point means table and its no-trend boundary were sound, but the displayed execute/recovery path was not executable as described and the new ignore rules did not travel with a packet-only copy.

I corrected both issues directly and explicitly approved the resulting exact state. The owner re-review is now open: Claude must genuinely re-open and approve the returned README and packet `.gitignore` blobs before this documentation loop closes. This is not a scientific or execution gate. Stage 1 remains complete as scoped; no capacity, threshold, Stage 2, later-role read, or final configuration is authorized.

## What was accomplished

### 1. Reviewed Claude's Stage-1 runbook handoff

I re-opened Claude's approved README blob `16afd81b74e94d3641737688a3ff84c76bf35eb6` and checked Steps 28–29 against:

- `Playbooks/reproducibility-packet.md`;
- `Playbooks/review-cycle.md`;
- `scripts/utils/capacity_sweep.py` argument consumption, plan identity, run-root claim, and fixed anchor paths;
- `scripts/analyze_capacity_sweep.py` required arguments and exclusive output writer; and
- the actual checkpoint tree and ignore state.

The table of five per-point means remains appropriate. They are exact reference record contents, the surrounding text states the only licensed row-5 reading, and the prose explicitly forbids trend interpretation.

### 2. Corrected the execute-label and recovery overclaim (Finding AX)

The handed-off execute command supplied `--run-label <a new, unused label>` while also supplying the tracked `stage1-run-2` plan. Static inspection established that execute mode never reads `args.run_label`; it takes the run label from the authenticated plan. The displayed command would therefore try the already-spent `stage1-run-2` root and refuse, regardless of the placeholder.

I replaced it with a copy-paste PowerShell sequence that:

1. generates a plan at a fresh label;
2. hashes that exact plan;
3. passes the new plan and digest to execute mode; and
4. omits the misleading execute-mode label argument.

The deeper clean-machine limitation also needed narrowing. Step 26 can build a new ten-anchor set under `results/dev_fit_reproduced/`, but the approved sweep executable is hard-bound to the tracked ledger, analysis, directory, and checkpoint digests under `results/dev_fit/`. It has no argument for a replacement anchor ledger. Different rebuilt bytes cannot be substituted as the approved anchors. The revised runbook now states that:

- the new-run command is conditional on the exact original ten anchor checkpoint bytes being present;
- a fresh packet clone cannot rerun the sweep or tracked analysis from its contents alone;
- a new capacity experiment from rebuilt anchors needs a new reviewed executable/design boundary; and
- Step 29 needs the ten original anchors plus forty completed curve checkpoints at their recorded digests.

This makes the packet limitation weaker but accurate. The recorded run's equivalence result establishes bitwise reproduction on the recorded machine, not cross-machine checkpoint restoration.

### 3. Moved run-output ignores into the packet (Finding AY)

Claude's three new rules were in the repository-root `.gitignore`. Those rules disappear when `Reproducibility Packet/` is copied alone, contrary to the packet's self-containment requirement.

I restored the repository-root `.gitignore` to its pre-Session-105 blob and placed all five current runbook scratch-output rules in `Reproducibility Packet/.gitignore`:

- `results/dev_fit_plan/`;
- `results/dev_fit_reproduced/`;
- `results/capacity_sweep_plan_reproduced/`;
- `results/capacity_sweep_plan_new_run/`; and
- `results/capacity_sweep_analysis_reproduced/`.

The rules work in the live repository and now travel with a packet-only copy.

### 4. Recorded the review under the append-only hard gate

I appended the review decision and exact-state handoff to the active Phase-2 transcript from a programmatically verified unique physical EOF block.

```text
pre-write transcript       1,822,376 bytes / 29,386 lines
pre-write SHA-256          733e0d63dfaac82b7142e84db228c88ce1df249c1adf3a6819208a2b7bae4023
Codex header               unique at line 29,388
old prefix                 byte-identical
transcript diff            +91 / -0
last agent                 Codex
```

No order-monitoring note was required.

## Exact reviewer-edited state

```text
Reproducibility Packet/README.md
  Git blob                 a985108ec4fecb028a7c2636424aaa0ea0128feb
  raw/canonical SHA-256    526e24cb37b91746986f23e28c6ec786566d8de8cb813ba0fb2fe1764b9cb800
  size                     106,504 bytes
  encoding                 UTF-8 / LF / no CR / no BOM / final newline

Reproducibility Packet/.gitignore
  Git blob                 b3d1a2c973dfe4de9f400ecf8c3ffab2a0b27830
  raw SHA-256              22e1328a609d3277c2aabb0066e98954f8ee53bb4005b4ac1adaeabc655a23bb

repository-root .gitignore
  restored Git blob        e388028cf9b2254c164e3b300c50e5f781a99f1a
```

## Verification

```text
fresh-label plan probe        X_PLAN_OK; 40 new + 2 equivalence arms; zero fits
probe label                   stage1-reproduction
probe plan SHA-256            4feddeac03f51c728b41efc3c83fdfa5f7d91fed438d0dd02afca2c26ae1af42
local checkpoint census       55 present / 0 tracked / 55 packet-ignored
focused normal                241 passed
focused python -O             241 passed; expected pytest warning
full packet                 1,792 passed
compileall                    clean
diff hygiene                  clean
```

The plan probe wrote to a temporary directory outside the repository and that directory was safely removed. The failed first PowerShell probe attempts were tooling-only: one used an unsupported `New-Item -LiteralPath` spelling and one looked for the packet's not-yet-created `.venv`; neither changed the repository or decision state. The successful probe used the required project-root `venv`.

## Decisions and reasoning

1. **Keep the five means table.** It materially helps reference comparison, and the pre-registered row interpretation directly prohibits turning the values into a trend.
2. **Do not strengthen the cross-machine claim.** The current executable authenticates exact original anchors; a newly fitted anchor set is a different experiment and cannot enter the approved sweep boundary.
3. **Show a real fresh-label plan sequence.** The plan, not an ignored execute argument, owns the run label. The command now matches that contract.
4. **Keep the missing-checkpoint state as an explicit packet limitation.** No checkpoint archive or approved new-anchor executable exists, so the packet is not yet end-to-end reproducible from a clean copy.
5. **Leave the public Live-Run README unchanged.** This session corrected internal packet documentation. It did not finish the packet, close a phase, or produce a new scientific milestone.

## Resource and evidence boundary

No model fit, checkpoint write, simulator generation run, physical rollout, real C7 invocation, plan publication, or pilot/validation/test read occurred. The successful plan probe was zero-fit and data-free. The lifetime physical-rollout count remains 278, and the existing capacity-fit records remain unchanged.

## Files created or updated

- `Reproducibility Packet/README.md` — corrected Steps 28–29 and clean-machine boundary.
- `Reproducibility Packet/.gitignore` — packet-local scratch-output rules.
- `.gitignore` — restored to its pre-Session-105 content by moving packet rules to the packet.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — append-only review and exact-state handoff.
- `agents/Codex/Session Summaries/HumanReport105.md` — this report.
- `agents/Codex/README.md` — session index and current runbook-review status.
- `agents/Codex/Summary of Only Necessary Context.md` — rewritten resume state.

Not changed: packet scripts, tests, protocol, plans, results, checkpoint bytes, the Claim Sheet, final config, director requests, or the public Live-Run README.

## Next steps

1. Claude must genuinely re-open and review README blob `a985108e...` and packet-ignore blob `b3d1a2c9...`, then explicitly approve them or return a new exact state.
2. Preserve the distinction between tracked JSON consistency and unavailable clean-machine checkpoint restoration.
3. Do not infer Stage 2, capacity selection, threshold selection, later-role reads, or final configuration from this documentation review.
4. The next Codex session number is 106. The next regular Codex progress report is Session 112.
