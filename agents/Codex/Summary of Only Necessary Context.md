# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 133 on 2026-08-14.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1, 2 and 3 are closed / both approved.
- Step 4a connection-record design review is **open**.
- Claude accepted Codex finding CZ and the authority-scoped branch-B ruling, then repaired findings
  DA and DB and explicitly approved owner blob `806d6fb9f2320ae9d44c758c18cb74a387828335`.
- Codex accepted DA/DB in substance, found one missing positive branch test as finding DC, repaired
  the document and explicitly approved reviewer blob
  `b968886f9bc4edcde0e5013256a8e95633ababb4` / raw SHA-256
  `73ca1be39dd37eb06f42446a3b20a1d203057bb97fa65260790d746a9679b464`.
- Claude owner re-review of that exact reviewer state is required. Step 4a is not closed until
  Claude explicitly approves the same bytes.
- Step 4b has not begun and is not yet authorized. Steps 4c–4f remain blocked.
- No production connection record, real-role adapter read, capacity/threshold selection, final
  config, scientific result or C1-versus-S statement is authorized.

## Current Step-4 design state

Artifact:
`Reproducibility Packet/protocol/slot8-connection-record-v0.1.md`

Exact reviewer state:

```text
Git blob     b968886f9bc4edcde0e5013256a8e95633ababb4
raw SHA-256  73ca1be39dd37eb06f42446a3b20a1d203057bb97fa65260790d746a9679b464
bytes        67,942
format       UTF-8, no BOM, LF-only, final newline
review audit DESIGN_REVIEW_OK: 44 checks
```

The header says `REVIEWER-REPAIRED AFTER SECOND OWNER RE-REVIEW AND CODEX APPROVED`. Claude's
approval names `806d6fb9...`. Do not infer same-state owner approval from the handoff, downstream
use or silence.

## Session-133 findings and rulings

### Findings DA and DB — accepted in substance

- **DA:** the frozen design's `--config` gloss is `FINAL`-only. Under `DEVELOPMENT_ONLY`,
  `--config` names an exact approved versioned draft file; `require_frozen` is selected from the
  authenticated record authority, never constant.
- The live tracked draft reproduces DA's source facts: it validates with
  `load_config(require_frozen=False)`, carries `status = draft`, `dev-712abf27...`, and null
  `values.models`, `values.calibration` and `values.evaluation`; it refuses under
  `require_frozen=True` with `confirmatory operation refuses draft configuration`.
- **DB:** B1 must remain portable. It proves the current production path unreachable from packet
  bytes and must not depend on the external 3.86 GB role tree. The external dataset label appears
  under `tests/` only three times, all as name-validation strings. No connection record is tracked.

### Finding DC — reviewer repair now awaiting owner re-review

DA repaired the runtime prose but did not make branch B positively testable. B1 validates the
tracked draft outside the adapter, B2's complete synthetic accept path never opens a config, and
B3's refusal cases can pass on an implementation that rejects every development config.

New **B8** requires, in the temporary complete synthetic validation harness:

1. an authenticated `DEVELOPMENT_ONLY` record/versioned-draft pair passes step 4 and then refuses
   only at a deliberately corrupted step-5 source;
2. that draft config under `FINAL` refuses at step 4;
3. a separately generated synthetic-frozen/`FINAL` pair passes step 4 and reaches the same later
   refusal; and
4. that frozen config under `DEVELOPMENT_ONLY` refuses at step 4.

These are validator-path tests using temporary synthetic documents. They do not author a production
record, create a public production accept path or open a real role byte. Branch B, DA, DB, CX, CY,
CZ, the six CLI arguments and every later authorization gate remain unchanged.

## Load-bearing Step-4 decisions still in force

### Preconditions and current data truth

- Final P1 and P2–P5 are false today. No complete `DEVELOPMENT_ONLY` precondition set exists.
- The current draft validates structurally as a development config, but its model and calibration
  fields are null and the design grants it no connection-record approval.
- P6 is uninstantiated, not false because no pairs exist. The delivered base manifest has 944 rows
  and 472 complete C1/S pairs: 152 dev, 152 pilot and 168 val.
- What is absent is an approved established-result artifact selecting exact menu cases/run
  identities and the downstream estimator/controller role material needed to render them.
- A production record may be authored only at 4c after the authority-appropriate config state,
  capacity selection, threshold calibration, separately established result and geometry validation
  all exist and are separately approved.

### Approval and authorization

1. Both-agent approval of the exact design closes 4a and licenses only the bounded synthetic
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
- The record names the packet schema, established result, model-selection artifact, two threshold
  sources, generated-geometry producer, geometry-validation artifact, manifest, both dataset
  audits, role-index/payload paths and checkpoint identities.
- Packet artifacts are packet-relative; payloads are role-root-relative; checkpoints are
  checkpoint-root-relative. No scan, glob, default or path-domain substitution is allowed.
- The record contains no approval/authorization field. Digests identify bytes, not social state.

### Geometry and synthetic fixtures

- There is no static MJCF model file. `scripts/utils/cable_mechanics.py::model_xml` constructs it
  in memory, and `extract_deformation_coordinates` emits ordered ball-joint log maps from
  `body_ids[1:]` for each link.
- The existing contract fixture's deformation and endpoint use independent synthetic maps. It
  cannot set the real adapter tolerance.
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
- `DEVELOPMENT_ONLY` remains a future production state for an explicitly reviewed draft-config
  record. Its exact output parent is `results/verification_connection_development` and is ignored
  only to prevent accidental tracking.
- `FINAL` bundles write below `results/verification_connection/bundles`; connection records live
  below sibling `results/verification_connection/records`.
- `.gitignore` is not an access-control mechanism.
- D3 stays open and the current adapter design contains no cross-arm derived scalar.

## Public Live-Run README

No successor entry was added in Codex Session 133. The connection-record design remains in an open
review round, so no artifact finished and no phase or distinct public milestone closed. The
Phase-2/In-Progress banner remains current. Do not rewrite the append-only 2026-08-13 entry. Keep
future public heartbeats to the playbook's lean one-or-two-sentence form.

## Closed Slot-8 state that still controls

- Step 1 design: closed / both approved at blob `0753d4ed...`.
- Step 2 implementation/tests: closed / both approved at source/test blobs `c12745ab`, `0ae5b19d`,
  `cf61e5aa` and `1833a472`.
- Step 3 fixture figure set/runbook: closed / both approved at ten fixture blobs plus packet README
  `4bc07f18`, packet `.gitattributes` `70ec4e7b`, packet `.gitignore` `ad29de35`, root
  `.gitattributes` `5a7720bc` and root README `3ab96e38`.
- The synthetic figure set is not a scientific result. The role path continues to refuse before
  opening a scientific file.
- The clean packet suite count is 2,267 passed. Sessions 131–133 changed documentation only and did
  not rerun it.

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

After Codex Session 133's append:

```text
bytes       2,282,252
LF          37,048
CR          19,709
SHA-256     8519836edeb7885042d2d5f3ce414a404ad92d80bbf75788470962eac6655e78
tail diff   +74 / -0
```

The 2,277,858-byte pre-write state remains the exact prefix at SHA-256
`7643418cf846f75bd4f3c0cb6c4434bd9672911d9ca092aba5d3f4f91ceaba1f`. The Codex Session-133
header occurs exactly once after that boundary, Codex is physically last, and the 4,394 added bytes
are LF-only. No append-order recurrence occurred; Transcript Order Monitoring was not changed.

For every future append: authenticate the physical UTF-8 bytes, record the pre-write boundary,
verify a complete unique EOF anchor programmatically, use the exact complete anchor as the write
boundary, and then assert the old bytes remain the exact prefix, the new header occurs once after
the boundary, the new author is physically last and Git is additions-only. If any assertion fails,
preserve the misplaced copy, append a dated physical-tail correction and disclose it in Transcript
Order Monitoring.

## Smart App Control

Smart App Control stays on by the director's decision. Before treating a future native-import
failure as project code, run:

`powershell -ExecutionPolicy Bypass -File "C:\Users\cresp\Documents\Dandelion Engineering\tools\Check-NativeImportBlocks.ps1"`

Do not propose turning SAC off.

## Next Codex session

Expected Codex Session 134:

1. Authenticate the newest transcript suffix against the Session-133 state above.
2. Read Claude's exact owner re-review of blob `b968886f...` and finding DC/B8.
3. If Claude approves those exact bytes unchanged, acknowledge Step 4a closure. Only Claude's
   bounded 4b adapter-and-test build becomes eligible; no scientific read or run follows.
4. If Claude edits, review the new exact state and preserve the owner/reviewer loop.
5. When reviewing 4b, require B8's two positive and two wrong-authority branch drives in temporary
   synthetic documents. An unconditional `require_frozen=True` implementation must fail.
6. Do not let 4b claim production-path acceptance, author a production record, open real roles or
   set the production geometry tolerance.
7. Preserve every data split, capacity, threshold, config-freeze and result boundary above.

## Workflow rules

- Follow `AgentPrompt.md` and obey `.agent-turn` / `.agent-session.lock` before any project work.
- Live transcript and current repository bytes outrank this continuity file.
- Require explicit same-state approval. Creation, edits, handoff, downstream use and silence are
  not approval.
- Before closeout, check the Live-Run README obligation, review/stage only intentional paths,
  commit and push, then delete `.agent-session.lock` and only afterward write `Claude` to
  `.agent-turn`.
