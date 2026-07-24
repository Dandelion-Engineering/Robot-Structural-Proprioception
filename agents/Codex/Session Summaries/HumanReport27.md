# Human Report — Codex Session 27

**Date:** 2026-07-23
**Phase:** Phase 2 — Integration and Reproducibility Build
**Session role:** Readiness-loop close, Gate-6 governance decision, and Gate-1 / Gate-2-foundation implementation
**Final config state:** **UNFROZEN**
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

## Executive summary

Claude Session 27 explicitly approved the exact Session-26 config-freeze readiness review. I acknowledged that approval in the authoritative Phase-2 transcript and closed the review loop without changing its owner state.

Two shared governance decisions are now explicit:

1. The confirmatory experiment will preserve the in-contract four-arm control comparison: no-action/detection-only, transparent attribution-driven, RMA, and oracle. The project will not post-hoc narrow the existing Claim Sheet to information-only or retune the blocked action families.
2. The complete Gate-3 scenario/fault/trajectory assignment manifest requires explicit Claude/Codex same-state approval before any headline model is fit. This is a real preregistration checkpoint distinct from the later final immutable config freeze.

I then implemented the approved first foundation slice:

- a machine-readable schema v1.0 + A1 authority;
- a versioned, self-hashed draft config and strict draft/frozen lifecycle validator;
- complete schema-A identity-manifest and exact role-index primitives;
- a deployable loader restricted to one observation-suite root;
- whole-group split, CRN, protocol, path, payload-hash, mask, dtype, and causal-timing audits;
- a contract-validation CLI;
- 18 focused adversarial tests; and
- packet runbook/boundary updates.

The full packet suite passes: **347 tests passed in 8.57 seconds**. The tracked draft validates as `status=draft`, `confirmatory=False`, with hash:

```text
dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180
```

I handed the exact implementation state to Claude for genuine review. My closeout assessment is intentionally split: Gate 1 is implemented pending that review, while Gate 2 remains blocked overall because the live manifest/data-building path, allowlisted training join, non-observation role builders/evaluators, and end-to-end generator do not yet exist.

No `config.json` or `test` payload was created.

## Required context work

I followed `AgentPrompt.md` from the beginning and read:

- the full project details;
- prior Codex continuity;
- every chat summary and active Codex transcript;
- Claude's latest continuity and human report;
- the complete Claim Sheet;
- the full schema-v1.0 + A1 contract;
- the config-freeze readiness review;
- the review-cycle, reproducibility-packet, and live-run README playbooks;
- the packet runbook, persistence prototypes, and current tests; and
- the actual clean repository state at Session-27 start.

The live transcript showed that Claude had approved the exact readiness-review state and had verified CUDA-enabled `torch==2.11.0+cu128` on the RTX 5060 Ti (`sm_120`). The GPU result removes a Gate-4 toolchain uncertainty but does not change the gate order or authorize model fitting before the jointly approved Gate-3 manifest.

## Readiness review and shared decisions

### Readiness loop closed

Claude's explicit same-state approval closes first review of:

- `agents/Codex/Config Freeze Readiness Review.md`

The decision remains:

> `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`

Closing the review authorizes work on the implementation backlog; it does not approve final config freeze.

### Gate-6 governance fixed

Claude recommended, and I explicitly accepted, the existing Claim-Sheet path:

- run no-action/detection-only;
- run transparent attribution-driven control;
- run the matched RMA control baseline;
- run the privileged oracle ceiling; and
- allow a diagnostic-only or negative control result to emerge honestly.

Narrowing the experiment to information-only would require an amendment. No amendment is being proposed.

### Gate-3 checkpoint fixed

Before headline-model fitting, Claude and Codex must approve the same complete assignment state for:

- known-class severity/location grids;
- compound/OOD holdout;
- trajectories and payloads;
- environment/contact profiles;
- onset/excitation roles;
- whole trajectory and whole fault-setting splits; and
- seeds and suite-matched comparison groups.

This prevents the data assignment from becoming an implicit post-hoc choice.

## Gate-1 implementation

### Machine schema

Created:

- `Reproducibility Packet/schema/schema.json`

It renders schema v1.0 + A1 as a machine-readable authority:

- exact identity, plant, observation, label, estimator-output, and controller-log roles;
- dtype, shape, unit, and availability declarations;
- A1 `contact_state[T,2]` and `safety_flag[T,7]` order;
- the fixed C0/C1/S observation registry;
- the real sparse `N_decisions` estimator-persistence axis;
- role-index fields;
- split, pairing, causality, leakage, and oracle invariants; and
- the draft/frozen config contract.

The audit caught and corrected an initially over-specific uncertainty declaration. `severity_uncertainty` is now a `config_defined_nonnegative_error_scale`; Gate 5 still owns the exact reviewed statistic.

### Draft/frozen config authority

Created:

- `Reproducibility Packet/config/draft-config-v0.1.json`
- `Reproducibility Packet/scripts/utils/config_contract.py`
- `Reproducibility Packet/scripts/validate_data_contract.py`

The tracked draft contains only evidence-backed current candidates. Unresolved scenario, model, calibration, controller-protocol, and evaluation objects remain visibly open. It cannot authorize confirmatory work.

The validator enforces:

- strict JSON with duplicate-key and non-finite-value rejection;
- exact machine-schema byte hash, with `.gitattributes` pinning that authority to LF across platforms;
- canonical config hashing independent of key order;
- `dev-`-qualified draft hashes;
- reserved exact filename `config.json` only for frozen state;
- explicit `APPROVE_CONFIG_FREEZE` decision for frozen state;
- zero open gates;
- no unresolved null or empty required objects;
- no development-prefixed frozen values;
- exact top-level fields; and
- hard draft refusal for confirmatory callers.

No file named `config.json` exists.

## Gate-2 foundation

Created:

- `Reproducibility Packet/scripts/utils/storage_contract.py`

The identity manifest covers every schema-A column and enforces:

- one row per whole rollout;
- one config identity per manifest;
- unique `run_id`;
- whole-pair, whole-trajectory, whole-fault-setting, and whole-split-group assignments;
- allowed roles and splits;
- path-free opaque IDs;
- nonnegative seeds;
- matched exogenous, controller, and training seeds within a pair;
- matched estimator/controller protocol IDs; and
- optional complete C1/S pairing.

Exact role indexes enforce safe relative one-file paths, schema/config identities, lowercase SHA-256 values, and observation split assignments.

`DeployableObservationLoader` receives only one `observations/<suite>` root. It rejects:

- a shared observation parent or wrong-suite root;
- identity/provenance columns in the index;
- label, privileged, or extra keys in an observation payload;
- parent traversal or drive-relative paths;
- wrong config/schema/run/split/suite identity;
- payload-hash mismatch;
- registry/order/mask mismatch;
- a hidden value in an unavailable channel;
- non-float64 values/timing or non-boolean masks; and
- inconsistent/negative causal latency.

This is not the whole Gate 2. Still missing are the live scenario-driven manifest/data builder, allowlisted supervised label join, full non-observation payload builders/evaluators, and end-to-end generation audit.

## Verification

Commands used from the packet with the repository virtual environment:

```powershell
..\venv\Scripts\python.exe -m compileall -q scripts tests
..\venv\Scripts\python.exe scripts\validate_data_contract.py --schema schema\schema.json --config config\draft-config-v0.1.json
..\venv\Scripts\python.exe -m pytest tests\test_data_contract.py -q
..\venv\Scripts\python.exe -m pytest tests\ -q
```

Recorded results:

```text
Config OK: status=draft, config_hash=dev-0211f2e71a473fef3c30cd53fd0a269df45156a3d58e83097bac7a5638bf6180, confirmatory=False
18 passed in 0.17s
347 passed in 8.57s
```

The focused suite checks the tracked machine authority, canonical/tamper-evident hashing, frozen-state refusal, split and CRN invariants, suite-root isolation, forbidden fields, unavailable-channel leakage, path traversal, payload tampering, and dtype drift.

## Documentation and public boundary

Updated:

- `Reproducibility Packet/README.md`
- `Reproducibility Packet/scripts/utils/__init__.py`

The packet runbook now includes the draft validator and states the Gate-2/3 boundary. It does not present the foundation as a frozen config or research result.

The root live README remains unchanged. This implementation has not yet received cross-review, changes no scientific result, and is not a phase transition. Advancing the public log now would turn an internal unreviewed infrastructure state into a public milestone.

## Active transcript and append-only verification

I appended three times to:

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`

The first append closed the readiness-review loop and recorded the Gate-6/Gate-3 decisions before implementation. The second handed Claude the exact implemented state and requested explicit `APPROVE_GATE1_GATE2_FOUNDATION` or `BLOCK_GATE1_GATE2_FOUNDATION`. The third added the narrow cross-platform `.gitattributes` guard to the exact review target after closeout hygiene exposed the line-ending risk.

For both appends I used the transcript hard gate: physical UTF-8 tail, recorded pre-write line count, unique complete EOF anchor, exact-anchor `apply_patch`, header-after-boundary assertion, and pure-append numstat. The final Session-27 transcript delta is:

```text
+58 / -0
```

No transcript-order recurrence occurred, so the separate monitoring chat was not changed.

## Files created

- `.gitattributes`
- `Reproducibility Packet/schema/schema.json`
- `Reproducibility Packet/config/draft-config-v0.1.json`
- `Reproducibility Packet/scripts/utils/config_contract.py`
- `Reproducibility Packet/scripts/utils/storage_contract.py`
- `Reproducibility Packet/scripts/validate_data_contract.py`
- `Reproducibility Packet/tests/test_data_contract.py`
- `agents/Codex/Session Summaries/HumanReport27.md`

## Files updated

- `Reproducibility Packet/README.md`
- `Reproducibility Packet/scripts/utils/__init__.py`
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
- `agents/Codex/README.md`
- `agents/Codex/Summary of Only Necessary Context.md`

## Files deliberately not changed

- `Reproducibility Packet/config.json` — absent; final freeze remains blocked.
- Root `README.md` — no reviewed public milestone or phase transition.
- `.gitignore` — no generated artifacts, secret material, or large outputs were introduced. A narrow `.gitattributes` rule was added instead to make the byte-hashed machine schema portable.
- Gate-3 assignments and `test` payloads — explicitly outside this implementation slice.

## Review state at closeout

### Closed

- config-freeze readiness review;
- actuator recovery-action review;
- all earlier recorded same-state review loops.

### Open

- Claude review of the exact Gate-1 / Gate-2-foundation implementation.

Reviewer edits are not approval. If Claude changes the implementation, Codex must inspect the actual new state before approving it.

## Next-session instructions

Codex Session 28 should:

1. follow `AgentPrompt.md` from the beginning;
2. read the physical tail of the active Phase-2 transcript;
3. inspect Claude's exact response and repository state;
4. if Claude approves the unchanged foundation, explicitly close the review loop;
5. if Claude edits or blocks it, perform genuine owner re-review and address only supported changes;
6. continue Gate 2 with the live data/manifest builder and allowlisted supervised join;
7. prepare the full Gate-3 assignment manifest, but do not fit headline models until both agents approve the same assignment state;
8. keep `config.json` absent and every `test` role untouched; and
9. preserve the four-arm controller protocol and all development/confirmatory claim boundaries.

The next regular Codex progress report is Session 32.

## Closeout verification

Before commit:

- the complete packet suite passed;
- the tracked draft validator passed and reported `confirmatory=False`;
- no `config.json` or `test` payload exists;
- the active transcript is pure append at `+58/-0`;
- `git diff --check` and staged diff hygiene must pass apart from non-actionable line-ending notices;
- every intended file must be staged; and
- the exact commit message is `Codex Session 27`.
