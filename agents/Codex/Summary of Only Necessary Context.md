# Summary of Only Necessary Context

**Last completed Codex session:** 26
**Next Codex session:** 27
**Expected next commit message:** `Codex Session 27`
**Project phase:** Phase 2 — Integration and Reproducibility Build
**Final config state:** **UNFROZEN**

## Resume from the live sources

Follow `AgentPrompt.md` from the beginning. Before doing substantive work, read:

1. `Project Details/Project Details.md`;
2. this file;
3. all chat summaries that include Codex;
4. the complete physical tail/current state of every active Codex chat;
5. Claude's latest human report and continuity summary; and
6. the actual repository state.

The authoritative active technical thread is:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

At Codex Session-26 closeout it had 2,408 physical UTF-8 lines. Codex's last header was:

- `**Codex (Session 26, 2026-07-23 18:05 PDT):**` at line 2,392.

Do not assume this remains the tail. Claude may have appended after closeout.

## Current review state

### Open: config-freeze readiness review

Codex created:

- `agents/Codex/Config Freeze Readiness Review.md`

Owner decision:

- `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

Codex handed the review to Claude for genuine first review in the active Phase-2 chat. **No same-state Claude approval existed at Session-26 closeout.**

Next action:

- If Claude explicitly approves the exact current review state, acknowledge and close the loop, then begin the first jointly approved implementation gate.
- If Claude edits the review, inspect the actual changes and perform genuine owner re-review. Do not infer approval from edits, downstream use, or silence.

### Closed: actuator recovery-action screen

Claude Session 26 reran and explicitly approved the exact Codex Session-25 state. The loop is closed.

Recorded development decision:

- `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`
- cap 3 is the strongest safe tuning-selected profile;
- actuator-fault recovery = 16.576%;
- healthy false-authorization benefit = 8.322%;
- source-specific margin = 8.254 percentage points;
- reported interval = `[8.093, 8.532]`;
- the margin misses the fixed 10-percentage-point gate; and
- cap 4/5 violate Amendment-A1 safety.

Do not reinterpret fault recovery alone as source-specific action evidence. No actuator action family advances.

### Closed: Better Suited Task redesign

The proposed task redesign was withdrawn. The append-only correction is preserved, the coordination thread is concluded, and the Claim Sheet was not amended.

## Config-freeze readiness result

The packet is not ready for final `config.json` freeze.

### Sequencing rule

Use two distinct configuration states:

- **DRAFT:** versioned and machine-validated for development/validation, including dataset construction, model training, hyperparameter selection, calibration, and controller-family screening.
- **FROZEN:** complete and immutable, including the selected model/training/calibration/controller/evaluation contract, created before untouched confirmatory test generation.

The old shorthand “learned heads post-freeze” cannot mean after final Claim-Sheet freeze. The Claim Sheet requires model/hyperparameter and class/abstention thresholds to be frozen before confirmatory generation.

### Evidence-backed draft candidates

Current development evidence supports draft candidates including:

- MuJoCo cable/rod plant;
- 17 points per link;
- 0.1 ms physics step;
- 500 Hz sensing;
- `n_def = 90`;
- gauge anchors 0.25 and 0.75;
- 0.05 N / 0.8 Hz / one-cycle probe;
- `W = 768`, stride 16;
- task/contact `z = 0.200 m`;
- no-contact reference `z = 0.100 m`;
- Amendment-A1 roles and thresholds;
- existing sensor-realism anchors; and
- onset plus 5 seconds for the complete post-onset analysis horizon.

These are not final confirmatory claims or a frozen config.

### Seven gates before final freeze

1. Machine-readable schema and draft/frozen config authority.
2. Role-separated storage, deployable loader, split audit, and leakage audit.
3. Multi-setting scenario/split/seed manifest including compound OOD.
4. `TemporalAttributionNet`, `RMALatentEncoder`, capacity ladder, and five training seeds.
5. Learned calibration, class thresholds, abstention, OOD, and uncertainty authorization.
6. Confirmatory controller protocol after both tested action families blocked.
7. Complete evaluation driver and auditable confirmatory manifest.

At Session-26 audit time there was no machine schema JSON, frozen config JSON, identity manifest, learned temporal/RMA implementation, deployable loader, split-audit function, confirmatory CLI, complete evaluation driver, or verification artifact. Existing development outputs use `dev-*` config hashes.

No `config.json` should be created until the pre-confirmatory build/validation gates close and Claude/Codex jointly approve the complete freeze state.

## Recommended next implementation sequence

Once the readiness review is jointly approved:

1. implement the machine schema, versioned draft-config contract, role-separated persistence, deployable loading, and split/leakage audit foundation;
2. instantiate the complete multi-setting scenario/split/seed manifest;
3. implement and validation-select the learned models, capacity ladder, calibration, OOD, abstention, and uncertainty rules;
4. resolve the confirmatory controller protocol and final sample size;
5. jointly freeze the complete immutable config;
6. generate/evaluate the untouched confirmatory roles; and
7. proceed to Phase-3 statistics and figures.

If the project chooses an information-only/detection-only confirmatory scope instead of a new recovery-action family, narrow control-outcome claims explicitly. Detection, attribution, information authorization, action authorization, and control outcome remain separate gates.

## Durable technical boundaries

- Development screens are not confirmatory results.
- Shared statistics or candidate values are not a frozen config.
- Information authorization is not action authorization.
- Fault improvement is not source-specific recovery unless it exceeds the matched healthy false-authorization benefit under the predeclared gate.
- A1 safety is a hard boundary.
- C1 and S action equivalence at a selected cap does not establish general model equivalence.
- Physical fault truth, delivered observations, estimator state, and controller authorization remain separate interfaces.
- Confirmatory test roles must remain untouched until after the complete freeze.

## Transcript append hard gate

The active Phase-2 transcript has a history of mid-file insertion failure. For every append:

1. read the physical UTF-8 tail;
2. record the pre-write line count;
3. verify the complete multi-line EOF anchor is unique;
4. use `apply_patch` only against that exact anchor;
5. verify the new session header occurs exactly once after the pre-write boundary; and
6. require `git diff --numstat` to show `+N/-0` for that transcript.

If any condition fails, stop and use the transcript-order monitoring workflow. Do not append using a short or non-unique anchor.

## Verification and environment

- Use only `.\venv\Scripts\python.exe` for Python/test commands.
- Claude Session 26 recorded 329 passing tests while reproducing the actuator screen. Codex Session 26 did not independently rerun the suite because it changed documentation only.
- Codex Session 26's chat delta was `+32/-0`.
- Root `README.md` was heartbeat-checked and deliberately left unchanged: the readiness review is an internal implementation gate, not a new public technical milestone.
- Next regular Codex progress report is Session 32.

## Session-26 durable files

- `agents/Codex/Config Freeze Readiness Review.md`
- `agents/Codex/Session Summaries/HumanReport26.md`
- `agents/Codex/README.md`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

Read `HumanReport26.md` for the detailed audit record and exact closeout rationale.
