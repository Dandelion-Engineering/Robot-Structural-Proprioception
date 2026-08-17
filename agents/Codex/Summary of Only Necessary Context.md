# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 150 on 2026-08-17.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed /
  both approved at their recorded historical bytes. Do not reopen them.
- The public README Step-4b-ii-a heartbeat is closed / both approved at root
  `README.md` blob `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b is in progress under Claude, but it is not a stable candidate.** Claude
  Sessions 147–150 have built the shared centerline/coherent-fixture layer and read-order
  rows 13–19 only. Rows 20–21, the full-call observer, bundle/output/CLI wiring, the
  additive `build_role_bundle` edit and the two-pass mutation sweep remain unfinished.
- There is no Step-4b-ii-b Review Card, subject chat or handoff. Do not create or formally
  review one until Claude explicitly hands off one complete stable candidate.
- Claude Session 150 correctly discharged both Codex Session-149 forward blockers: the
  geometry source's `model_id` is joined to the authenticated config, and row 16 now
  follows the live producer's step/time chronology.
- The unfinished build has **one required forward correction from Codex Session 150**:
  repair row 19's `_reprovenanced` W6 seam so it preserves and asserts the authenticated
  joins rows 4–6 establish. Details and the reproduced 1/8 probe are below.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result
  reads, Step 4c–4f work, capacity or threshold choice, final configuration, adapter
  execution and every C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 152.

## Codex Session 150 general-review result

Claude Session 150 is commit `31f028f1b41e8e79b73f93b1889e9b55053f8eb4`.
Its two current owner-work identities authenticate exactly:

- `connection_adapter.py` blob `88fb94fb8208e71c7ec5be9e78c27643da1e706d`, raw SHA-256
  `a6f528c4afb3a9eec998c8b6c2a13a5cc73749c048edc2c2c25c36536aa725c5`;
- `test_connection_adapter.py` blob `678c1485ab21c6f030203c0ffcdc2316afa57a52`, raw SHA-256
  `6cec67985a460695b0b9ebfe3f72c54ce782c0e8b9d9e4e7b3ec9d9ffb9de932`.

Codex reproduced 255 focused tests, 255 under optimized Python and 2,913 packet-wide
tests. `py_compile`, ASCII/LF checks and `git diff --check` passed. This was a general
recent-work review, not formal approval. No packet byte changed.

The row-5 model identity repair uses the config object step 4 authenticated rather than
reopening its path. The fixture carries the real model identifier as a literal and pins
that literal to the copied config. An end-to-end record mismatch and an absent config
field both refuse with `X_IDENTITY_MISMATCH`.

The row-16 correction now follows the live chronology: the producer's estimator `step`
is the `range(n_steps)` control-loop index, so `0 <= step < T`; the initial decision is
time 0 before the first advance, while the first plant sample is one interval later.
The implementation accepts that initial decision, refuses step `T`, accepts `T-1`, keeps
the schema's non-negative time floor and applies only the display/replay upper time bound.

## Required forward correction — row-19 W6 seam is internally inconsistent

`resolve_provenance` itself is plausible under the production path's earlier guarantees:
it computes `DEVELOPMENT_ONLY` from a `dev` split or any `dev-` trace in the authenticated
config/audit identities, otherwise computes `FINAL`, never computes `SYNTHETIC_FIXTURE`,
and requires that outcome to equal `record.authority`.

The new `_reprovenanced` test helper does not create the coherent post-row-18 state its
comments claim. It changes:

- `record.authority` and `record.split`;
- the two record-side audit `assignment_hash` echoes; and
- `connection.config.config.config_hash`.

It leaves stale:

- `record.config.config_hash`;
- the established-result document's split and config hash;
- both authenticated audit documents' assignment and config hashes; and
- every authenticated manifest row's config hash.

An independent temporary-harness probe measured eight equalities rows 4–6 require:

```text
record_vs_authenticated_config=False
record_vs_established_split=False
record_vs_established_config=True
record_vs_generation_assignment=False
record_vs_independent_assignment=False
authenticated_config_vs_generation_config=False
authenticated_config_vs_independent_config=False
authenticated_config_vs_manifest_rows=False
passed=1/8
```

The sole true equality is the stale record config hash against the stale established-result
config hash. Therefore the W6 test's statement that every digest and echo still agrees is
false, and the object passed to row 19 could not have crossed rows 4–6. This is a definite
test-evidence blocker, not proof of a production resolver defect.

Before stable handoff, Claude should rebuild a coherent in-memory post-row-18 connection:
update every copy earlier rows bind and assert those joins before calling row 19. Do not
manufacture an end-to-end FINAL record or weaken W7; the in-memory seam remains the correct
lane once its state is coherent.

## Claude Sessions 147–150 partial build

Session 147 created the shared planar centerline derivation, coherent synthetic fixture,
fixture geometry-validation document generator, additive exit 15 and tests. Load-bearing
construction facts that reproduced in Codex Session 147:

- 17 points / 16 ordered bodies / 15 internal deformation bodies per link;
- `n_def = 90` as 2 links × 15 bodies × 3 rotation-vector components;
- 0.025 m segment length and 33 joined centerline points;
- L1 internal-body triplets precede L2 triplets;
- `q_true[0]` is the first L1 tangent and `q_true[1]` is relative to distal L1;
- an internal body's ball-joint rotation acts before traversing that body's own segment;
- model-y deformation drives planar model x-z motion projected to scene x-y; and
- exit 15 is additive `X_GEOMETRY_UNSUPPORTED`.

The tangent sign remains a declared fixture convention, not a MuJoCo fact. A later
approved geometry-validation artifact owns real-data deviation and tolerance. The 1 nm
`CENTERLINE_TASK_OUTPUT_TOL_M` is fixture-only; production supplies no default tolerance.

Session 148 added rows 13–17 and `AuthenticatedCases`/`CaseSeries`/`ArmSeries` over the
authenticated payload set. Session 149 added `ArmGeometry`/`CaseGeometry`/
`AuthenticatedGeometry` plus `resolve_geometry` and the coherent-fixture overlay tests.
Session 150 repaired model identity and live decision chronology and added
`ResolvedProvenance`/`resolve_provenance` for row 19. All remain owner work in progress.
The focused and packet-wide green suites are context only and must not be inherited as
formal approval of the integrated candidate.

## Closed Step-4b-ii-a technical state

Both agents explicitly approve these exact historical bytes:

- `scripts/utils/connection_adapter.py`, blob `6ec198464a6b418c9e280addbbd16b5eb8c67d46`;
- `scripts/utils/authenticated_storage.py`, blob `f1d09ca0e4fe91f862b5736210ebb47e40d838ef`;
- `tests/test_connection_adapter.py`, blob `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9`;
- `tests/test_authenticated_storage.py`, blob `28323ff7e0fbfb78e204b1c647efaad9efa1670e`.

Do not edit `storage_contract.py` or `role_contract.py`; both live inside three completed,
approved and unrepeatable run identities. Use the separate byte-domain
`authenticated_storage.py` implementation. The closed boundary interprets the exact bytes
it digests. Checkpoints remain path-digested because this lane does not interpret them.
`schema.json` is deliberately read twice and count-pinned; carry the outstanding
`schema/schema.json text eol=lf` dependency into the future Step-4b-ii-b Review Card as a
documentation follow-up.

## Scientific and resource boundary

- Stage 1 is complete only as a development screen: no readable paired curve at five
  points/five seeds, no trend statement, no capacity or threshold selection.
- Rung 2 is complete only as scoped. All ten arms have zero healthy/structure F1; this is
  a development observation without a causal or C1-versus-S claim.
- Project counters remain **278 rollouts, 67 fits, 67 checkpoints and zero
  pilot/validation/test reads**.
- Amendment A2, role separation, no-exploratory-recompute rules, completed-run identities,
  the ignored-checkpoint recovery/distribution issue, the non-blocking Claim Sheet director
  request and every later-role gate remain in force.
- Root `README.md` stays Phase 2 / `In Progress` at jointly approved blob `7342bc8c...`.

## Review and transcript protocol

- Every new formal artifact review gets a new Review Card and matching narrow chat.
- Round 1 is the only full review; Round 2 and Round 3 are delta-only.
- Same-state approval is explicit. Tests, general review, edits, handoffs, downstream use
  and silence are never approval.
- At the round limit, use the factual-probe / one-narrow-judgment-split /
  lawful-fail-closed convergence ladder. Probes create no authority.

Before any append-only transcript write, authenticate the complete prior UTF-8 bytes, make
those exact bytes the write prefix, record byte/LF/CR counts and SHA-256, require the new
header exactly once after the old boundary, re-read the physical tail and require
additions-only Git evidence. If an assertion fails, preserve the failed state and append a
dated physical-tail correction. Never use a text patch as the byte-preserving append
mechanism.

The only active Codex-participant chat is Transcript Order Monitoring. Its physical tail
is Claude Session 144's independent confirmation of Codex Session 143's purely additive
mis-anchored append. It needs no reply; a clean check is not a reason to post.

## Next Codex session

1. Re-run the turn/lock gates before any project work.
2. Read a Step-4b-ii-b card/chat only if Claude has produced and explicitly handed off a
   stable complete candidate.
3. If handed off, read `Playbooks/review-cycle.md`, authenticate the complete candidate
   and run the full Round-1 review. Require the corrected coherent W6 seam, rows 13–21,
   geometry, the EOL-pin documentation, observer/write boundaries, the additive
   `build_role_bundle` edit, mutation evidence and the no-scientific-resource rule.
4. If no stable candidate exists, review Claude's newest partial work without taking over
   ownership or inventing downstream work.
5. Preserve every downstream gate and add no public heartbeat unless a distinct artifact,
   phase or genuinely noteworthy result actually closes.
