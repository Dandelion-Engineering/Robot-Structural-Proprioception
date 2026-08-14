# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 131 on 2026-08-13.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1, 2 and 3 are closed / both approved.
- Step 4a connection-record design review is **open**. Claude authored and approved owner blob
  `d9ad21696902b413556c1cb29bcc5da7a373e849`; Codex found material defects, repaired it and
  explicitly approved reviewer blob `8d06792cdaa38e9e3df374f9ec1dca109ededc19` / raw SHA-256
  `c21eabff703432a791bbb3ab76b0c43ef30ad334d790289900271fcaafdf960e`.
- Claude owner re-review of that exact repaired state is required. Step 4a is not closed until
  Claude explicitly approves the same bytes.
- Step 4b has not begun and is not yet authorized. Steps 4c–4f remain blocked.
- No production connection record, real-role adapter read, capacity/threshold selection, final
  config, scientific result or C1-versus-S statement is authorized.

## Current Step-4 design state

Artifact:
`Reproducibility Packet/protocol/slot8-connection-record-v0.1.md`

Exact reviewer state:

```text
Git blob     8d06792cdaa38e9e3df374f9ec1dca109ededc19
raw SHA-256  c21eabff703432a791bbb3ab76b0c43ef30ad334d790289900271fcaafdf960e
bytes        53,441
format       UTF-8, no BOM, LF-only
review audit DESIGN_REVIEW_OK: 36 checks
```

The header says `REVIEWER-REPAIRED AND CODEX APPROVED; owner re-review ... required`. Do not
change that status or infer same-state owner approval from a handoff, implementation, silence or
downstream use.

## Load-bearing design decisions

### Preconditions and current data truth

- P1–P5 are false today.
- P6 is uninstantiated, not false because no pairs exist. The delivered base manifest has 944 rows
  and 472 complete C1/S pairs: 152 dev, 152 pilot and 168 val.
- What is absent is an approved established-result artifact selecting exact menu cases/run
  identities and the downstream estimator/controller role material needed to render them.
- The record may be authored only at 4c, after config freeze, model selection, threshold
  calibration, a separately established development/final result and geometry validation.

### Approval and authorization

1. Both-agent approval of this exact design closes 4a and licenses only the bounded synthetic
   adapter/test build in 4b.
2. A later production record's exact-state approval closes 4d but authorizes no run.
3. Two separately recorded 4e authorization halves must name the exact record digest, split,
   command, all six arguments, budget and P1–P6 checks. Together they authorize one invocation.
4. An earlier result read does not make the later rendering read free; the adapter's role re-open
   needs its own 4e authorization.

### Authentication and allowlist

- The record is authenticated before parsing.
- Packet schema, config, every source/result/audit, every role index, every payload and every
  checkpoint are hashed before parsing/loading.
- The record names the packet schema, established result, model-selection artifact, two distinct
  threshold sources, generated-geometry producer, geometry-validation artifact, manifest, both
  dataset audits, role-index/payload paths and checkpoint identities.
- Packet artifacts are packet-relative; payloads are role-root-relative; checkpoints are
  checkpoint-root-relative. No scan, glob, default or path-domain substitution is allowed.
- The record contains no approval/authorization field. Digests identify bytes, not social state.

### Geometry and synthetic fixtures

- There is no static MJCF model file. `scripts/utils/cable_mechanics.py::model_xml` constructs it in
  memory, and `extract_deformation_coordinates` emits ordered ball-joint log maps from
  `body_ids[1:]` for each link.
- The existing contract fixture's deformation and endpoint use independent synthetic maps. A
  plausible reconstruction misses by 2.81–6.20 mm (mean 5.31 mm), so it cannot set the real
  adapter tolerance.
- Step 4b uses the existing fixture only for storage/index/authentication/refusal plumbing and a
  separate coherent deterministic fixture for geometry/rendering.
- The synthetic accept path reaches only the private `SYNTHETIC_FIXTURE` seam. It cannot create
  production `DEVELOPMENT_ONLY` or `FINAL` authority.
- The 1 nm `CENTERLINE_TASK_OUTPUT_TOL_M` remains the closed fixture-construction check. A later
  reviewed geometry-validation artifact sources the production tolerance.
- Geometry failure receives additive `X_GEOMETRY_UNSUPPORTED`, exit 15; existing codes do not move.

### Provenance and output

- Schema-conformant fixture bytes are not research provenance.
- Production provenance requires strict semantic agreement among both dataset audits, manifest,
  config and exact established-result artifact.
- `DEVELOPMENT_ONLY` remains a future production state for an explicitly reviewed development
  record. The exact dev output parent is `results/verification_connection_development`; the final
  parent is `results/verification_connection`.
- `.gitignore` limits accidental tracking only; it is not an access-control mechanism.
- D3 stays open and the current adapter design contains no cross-arm derived scalar.

## E1–E4 rulings

- E1: yes, build only after 4a closes, with split fixture responsibilities as above.
- E2: use exact established-result artifact/digest/field binding plus separate transcript closure
  and 4e read authorization.
- E3: retain future reviewed `DEVELOPMENT_ONLY`; present synthetic acceptance is separate.
- E4: no cross-arm scalar; D3 remains open.

## Public Live-Run README

No successor entry was added in Codex Session 131. The 2026-08-13 entry is a dated historical
record, the Phase-2/In-Progress banner remains current, and Step-3 peer-review closure does not add
a second public artifact or phase milestone beyond the verification-surface event already logged.
Do not rewrite the append-only entry. Keep future public heartbeats to the playbook's lean
one-or-two-sentence form.

## Closed Slot-8 state that still controls

- Step 1 design: closed / both approved at blob `0753d4ed...`.
- Step 2 implementation/tests: closed / both approved at source/test blobs `c12745ab`, `0ae5b19d`,
  `cf61e5aa` and `1833a472`.
- Step 3 fixture figure set/runbook: closed / both approved at ten fixture blobs plus packet README
  `4bc07f18`, packet `.gitattributes` `70ec4e7b`, packet `.gitignore` `ad29de35`, root
  `.gitattributes` `5a7720bc` and root README `3ab96e38`.
- The synthetic figure set is not a scientific result. The role path continues to refuse before
  opening a scientific file.
- The clean packet suite count is 2,267 passed. Claude Session 131 most recently reproduced it in
  204.35 s; Codex Session 131 changed documentation only and did not rerun it.

## Other scientific boundaries still controlling

- Stage 1 is complete as scoped: no readable five-point/five-seed curve shape and no trend,
  capacity or threshold statement licensed.
- Literal Slot-9 rung 2 is complete as scoped. Its fit/analyzer invocations are spent; exact
  analysis blob `a2fa857b...` / raw SHA-256 `604d7272...` is jointly approved.
- All ten rung-2 arms have zero healthy and structure F1; this persisted-value observation must
  accompany the weak objective/sign description without causal attribution.
- Checkpoint 67 is development-only. No validation, generalization, threshold, final-config or
  engineering-usability claim follows.
- Amendment A2 and every development/pilot/validation/confirmatory/test/final boundary remain in
  force.
- Current counters remain 278 rollouts, 67 fits and 67 checkpoints; zero pilot/val/test reads.

## Transcript state

Authoritative active thread:
`chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

After Codex Session 131's append:

```text
bytes       2,251,344
LF          36,578
SHA-256     29e3207bb9869028db2119d3eae547fe94aa78258b59f0a7dd5b1b4a590d751f
tail diff   +109 / -0
```

The 2,244,241-byte pre-write state remains the exact prefix at SHA-256
`625167d1101e6a4ffd4dbc2b44f59638446d98f9999926914572310100a61d45`. The Codex Session-131
header occurs exactly once, Codex is physically last, and the 7,103 added bytes are LF-only. No
append-order recurrence occurred; Transcript Order Monitoring was not changed.

For every future append: authenticate the physical UTF-8 bytes, record the pre-write boundary,
verify a complete unique EOF anchor programmatically, use it as patch context, and then assert the
old bytes remain the exact prefix, the new header occurs once, the new author is physically last
and Git is additions-only. If any assertion fails, preserve the misplaced copy, append a dated
physical-tail correction and disclose it in Transcript Order Monitoring.

## Smart App Control

Smart App Control stays on by the director's decision. Before treating a future native-import
failure as project code, run:

`powershell -ExecutionPolicy Bypass -File "C:\Users\cresp\Documents\Dandelion Engineering\tools\Check-NativeImportBlocks.ps1"`

Do not propose turning SAC off.

## Next Codex session

Expected Codex Session 132:

1. Authenticate the newest transcript suffix against the Session-131 state above.
2. Read Claude's exact owner re-review of blob `8d06792c...`.
3. If Claude approves those exact bytes unchanged, acknowledge Step 4a closure. Only the bounded
   4b synthetic adapter/test build becomes eligible; no scientific read or run follows.
4. If Claude edits, review the new exact state and preserve the owner/reviewer loop.
5. Do not let 4b claim production-path acceptance. Production mutation/record controls wait for
   the exact 4d record state.
6. Preserve every data split, capacity, threshold, config-freeze and result boundary above.

## Workflow rules

- Follow `AgentPrompt.md` and obey `.agent-turn` / `.agent-session.lock` before any project work.
- Live transcript and current repository bytes outrank this continuity file.
- Require explicit same-state approval. Creation, edits, handoff, downstream use and silence are
  not approval.
- Before closeout, check the Live-Run README obligation, review/stage only intentional paths,
  commit and push, then delete `.agent-session.lock` and only afterward write `Claude` to
  `.agent-turn`.
