# Codex — Human Report, Session 106

**Date and time:** 2026-08-10 02:06 PDT

**Phase:** Phase 2 — Execution, with limited Phase-3 packet assembly

**Progress-report session:** No. The next regular Codex progress report is Session 112 unless a phase transition or approved Claim Sheet amendment fires one sooner.

---

## Summary

Claude Session 106 genuinely re-reviewed the packet runbook state returned in Codex Session
105. Claude accepted Findings AX and AY, approved the packet README unchanged at Codex's bytes,
and added four omitted runbook scratch-output directories to `Reproducibility Packet/.gitignore`
as Finding AZ. I independently reviewed that returned state against the full runbook destination
set and the real writers.

The four AZ rules are correct and are kept unchanged. The README review loop is now closed at
blob `a985108ec4fecb028a7c2636424aaa0ea0128feb`. The packet-ignore loop did not close, because the
claimed complete enumeration still omitted Step 20's `results/sensor_model/` tree. The `.npz`
payload was covered by the generic payload rule, but the writer's required `index.csv` was
neither tracked nor ignored. I added one directory-scoped packet rule, approved the resulting
exact state, and handed it back to Claude for genuine owner re-review.

This is a documentation/packaging control only. Stage 1 remains complete as scoped. No capacity,
threshold, Stage 2 action, later-role read, or final configuration is authorized.

## What was accomplished

### 1. Accepted Finding AZ's four additions

I checked the exact returned packet-ignore blob `fd106b959be8da4a2e817c1122f79746c00a29ef`
against the runbook commands and the corresponding output writers. These four directories are
real untracked outputs produced by copy-paste packet steps and belong in the packet-local ignore
file:

- `results/data_contract_fixture/` — Step 2A writes the manifest, indexes and build summary;
- `results/mujoco_plant/` — Step 19 writes a plant payload plus `index.csv`;
- `results/mujoco_contact_dev/` — Step 19's optional contact command writes the same shape; and
- `results/protocol_p_plan/` — Step 25 plan mode writes the Protocol-P screen plan.

All four rules are rooted and directory-terminated, so they do not swallow neighboring tracked
evidence trees such as `results/protocol_p/`. Their implementation is retained unchanged.

### 2. Found and repaired Finding BA

A broader census of every runbook destination exposed one remaining hole. Step 20 runs
`scripts/run_sensor_model.py` without an explicit output root, so the parser defaults to
`results/sensor_model`. The writer creates:

```text
results/sensor_model/observations/<suite>/<run_id>.npz
results/sensor_model/observations/<suite>/index.csv
```

The generic `*.npz` rule already ignored the payload. It did not cover `index.csv`, no file in
that output tree is tracked, and `git check-ignore` confirmed the CSV remained visible. This had
the same mechanism as Findings AY/AZ: the runbook creates a local reproduction artifact that the
packet's own ignore file must carry.

I added exactly one rule in runbook-step order:

```gitignore
/results/sensor_model/
```

I deliberately did not add `results/synthetic_plant/`: Step 21 writes only one `.npz`, already
covered by the payload rule, and Git does not track empty directories.

### 3. Closed the README loop and preserved the separate ignore loop

Claude explicitly approved the exact README bytes already approved by Codex, so that file now
has same-state approval from both agents and its review loop is closed:

```text
Reproducibility Packet/README.md
  Git blob                 a985108ec4fecb028a7c2636424aaa0ea0128feb
  raw/canonical SHA-256    526e24cb37b91746986f23e28c6ec786566d8de8cb813ba0fb2fe1764b9cb800
```

The packet-ignore file is a new reviewer-edited state and therefore remains open on Claude:

```text
Reproducibility Packet/.gitignore
  Git blob                 5082c2fc2c2277eef586c442b50a52881f6e5c95
  raw SHA-256              5120235af01356adac29a32424d2a6e18dde4ff1b3ac80dd1338b99aabbdee64
  size / encoding          576 bytes / UTF-8 / LF / no CR / no BOM / final newline

repository-root .gitignore
  Git blob                 e388028cf9b2254c164e3b300c50e5f781a99f1a
```

Codex explicitly approves packet-ignore blob `5082c2fc...`; Claude must approve those same bytes
or return another exact state before the ignore loop closes.

## Verification

The decision-bearing checks were Git's ignore matcher and tracked-file audit:

```text
positive scratch controls                 10/10 ignored by the intended packet rule
negative neighboring evidence controls     7/7 visible
tracked-and-ignored files                   0
runbook destination census                 complete for non-payload scratch trees
root .gitignore                            unchanged at e388028c...
packet README                              unchanged at a985108e...
diff hygiene                               clean
```

The negative set included the tracked `dev_fit`, `capacity_sweep`,
`capacity_sweep_analysis`, `protocol_p`, `structural_separability`, and
`feasibility_spike` trees plus a same-prefix `sensor_model_reference` control. No packet test run
was warranted for a one-line ignore-only correction; no executable behavior changed.

## Transcript integrity

The Session-106 handoff used the stored append-only hard gate:

```text
pre-write bytes / lines       1,836,684 / 29,626
pre-write SHA-256             c626492b...3a64e45
verified EOF anchor           16 lines / one occurrence
Codex header                  unique at line 29,628
old prefix                    byte-identical
transcript diff               +65 / -0
last agent                    Codex
```

The first prefix-verifier command used a .NET method unavailable in this PowerShell runtime and
printed no hash. I did not treat that as a pass or a content failure. The compatible rerun
computed the full prefix SHA-256 and matched the recorded digest exactly. No correction append
was needed.

## Decisions and reasoning

1. **Accept AZ, but not its completeness claim.** Each of Claude's four rules is correct; the
   defect was that Step 20 remained outside the enumerated set.
2. **Ignore the whole Step-20 scratch tree.** Its `.npz` and append-only local `index.csv` are a
   single reproduction output, and neither is tracked evidence.
3. **Keep synthetic-plant handling extension-based.** Its only output is already covered by
   `*.npz`; a directory rule would add no protection.
4. **Close only the README loop.** Claude approved the exact README bytes Codex approved. The
   edited packet-ignore state is different and requires its own same-state approval.
5. **Do not update the public Live-Run README.** This packaging correction neither changes the
   scientific result nor completes the packet or phase.

## Resource and evidence boundary

No fit, checkpoint write, simulator generation, physical rollout, C7 invocation, plan
publication, or pilot/validation/test read occurred. No observation payload, label payload, or
checkpoint was opened. Lifetime Protocol-P-related physical rollouts remain 278. The final
`Reproducibility Packet/config/config.json` remains absent.

## Files created or updated

- `Reproducibility Packet/.gitignore` — added the Step-20 `sensor_model` scratch tree rule.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the exact-state review, Finding BA, approval and owner handback.
- `agents/Codex/Session Summaries/HumanReport106.md` — this report.
- `agents/Codex/README.md` — updated current authority text, session index and tree.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the new exact-state review gate.

Not changed: the packet README, root `.gitignore`, scripts, tests, protocol, plans, results,
checkpoint bytes, Claim Sheet, director requests, final config, or public Live-Run README.

## Next steps

1. Claude genuinely re-opens and reviews packet-ignore blob `5082c2fc...`, then explicitly
   approves those same bytes or returns a corrected state.
2. Keep the packet README closed at blob `a985108e...` unless a genuinely new finding requires a
   forward revision.
3. Preserve the disclosed clean-machine checkpoint limitation and the distinction between
   tracked JSON consistency and unavailable exact checkpoint restoration.
4. Do not infer capacity selection, threshold selection, Stage 2, later-role reads, or final
   configuration from this packaging review.
5. The next Codex session number is 107. The next regular progress report is Session 112.
