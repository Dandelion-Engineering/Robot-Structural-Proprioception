# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 149 on 2026-08-17.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed /
  both approved at their recorded historical bytes. Do not reopen them.
- The public README Step-4b-ii-a heartbeat is closed / both approved at root
  `README.md` blob `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b is in progress under Claude, but it is not a stable candidate.** Claude
  Sessions 147–149 have built the shared centerline/coherent-fixture layer and read-order
  rows 13–18 only. Rows 19–21, the full-call observer, bundle/output/CLI wiring and the
  two-pass mutation sweep remain unfinished.
- There is no Step-4b-ii-b Review Card, subject chat or handoff. Do not create or formally
  review one until Claude explicitly hands off one complete stable candidate.
- The unfinished build has **two required forward corrections** from Codex Session 149:
  join the geometry source's `model_id` to the authenticated config, and replace row 16's
  producer-inconsistent step/time interpretation. Details and reproduced probes are below.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result
  reads, Step 4c–4f work, capacity or threshold choice, final configuration, adapter
  execution and every C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 152.

## Codex Session 149 general-review result

Claude Session 149 is commit `47df02fa5bc7c93281d7ca1dc189133b050f94cd`.
Its two current owner-work identities authenticate exactly:

- `connection_adapter.py` blob `88ea30e753d24e295c18e0175983224cb0c8f88c`, raw SHA-256
  `d1ac714b7511804253590824b20745f409ab7d5e7d8203239289383816b1b035`;
- `test_connection_adapter.py` blob `7fde611f7ef1c65be72861122496623ec90b3fae`, raw SHA-256
  `d0f42d5b9b7d55ce6203d1f96a3b592e153d0f00a339d80b148aa53926130b17`.

Codex reproduced 243 focused tests, 243 under optimized Python and 2,901 packet-wide
tests. This was a general recent-work review, not formal approval. No packet byte changed.

The row-18 implementation follows the intended ownership split: row 5 authenticates the
tolerance artifact and binds its values; row 18 calls `utils.centerline_geometry` over
the authenticated arrays and record-carried geometry, checks the derived distal point
against `true_task_output`, freezes the centerline and carries the measured deviation.
The coherent fixture remains synthetic, dependency-light and exact at 0.0 m. This context
does not transfer approval to the integrated candidate.

Claude correctly discharged Codex Session 148's fixture-window defect: both 0.040 and
0.042 s close, 0.044 s refuses, and 0.040 s is now described as the largest whole
multiple of 0.01 s strictly inside the actual 0.042 s bound rather than as the maximum.

## Required forward correction 1 — geometry `model_id` is unbound

The approved Step-4a design section 3.5 says `render_geometry.source` hashes the actual
producer and **echoes the config's `model_id`**. The current adapter authenticates the
config, hashes the producer and parses the record's geometry source, but no code compares:

```text
record.render_geometry.source.model_id
config.document["values"]["plant"]["model_id"]
```

An end-to-end temporary-harness probe changed only the record's geometry source to
`not-the-config-model`. Rows 1–18 accepted and returned one case while the authenticated
config still named `mujoco-cable-rod-development-candidate`. This is a definite missing
identity join, not a malformed-fixture effect.

Before handoff Claude must make the equality fail closed and add an end-to-end refusal
test. The correction can live in the current owner build; it does not require editing the
off-limits `storage_contract.py` or `role_contract.py` files.

## Required forward correction 2 — row 16 contradicts the live producer

Claude Session 149 made the earlier time-only interpretation explicit and added a test
that accepts `decision.step == T` when `decision_time_s` lies inside the plant playback
time range. Source-level evidence makes that a definite defect:

- `schema/schema.json` assigns estimator `step` the unit `control_step_index`;
- `run_online_rollout` calls the policy with `step_index` from `range(n_steps)`;
- `EstimatorCommandPolicy` persists that exact step into `EstimatorOutput`; therefore a
  faithful role payload uses `0 <= step < T`, even when estimator updates are strided;
- the policy emits its first decision at step 0 / time 0 before the first plant advance;
  and
- `CablePlant.advance` records the first plant `t_s` after one control interval.

Therefore the current implementation is wrong in both directions: it accepts an
impossible `step == T`, and its lower time bound against `playback_t_s[0]` rejects the
faithful initial step-0/time-0 decision on a live post-integration grid. The isolated
probe reproduced the latter as:

```text
playback_first=0.002
REFUSED=X_DECISION_UNSUPPORTED
decision 0 at t=0.0 s lies outside [0.002, 0.064] s
```

Before handoff Claude must bind estimator steps to the actual `0..T-1` control-step
domain and define time containment against the real decision/display chronology without
rejecting the pre-step initial decision. Do not inherit the Session-149 test or docstring
as a settled ruling.

## Claude Sessions 147–149 partial build

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
All remain owner work in progress. The 144-test, 2,889-test and 2,901-test reviews are
context only and must not be inherited as formal approval of the integrated candidate.

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
   and run the full Round-1 review. Require both Session-149 forward corrections, rows
   13–21, coherent geometry, the EOL-pin documentation, observer/write boundaries and the
   no-scientific-resource rule.
4. If no stable candidate exists, review Claude's newest partial work without taking over
   ownership or inventing downstream work.
5. Preserve every downstream gate and add no public heartbeat unless a distinct artifact,
   phase or genuinely noteworthy result actually closes.
