# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 148 on 2026-08-17.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed /
  both approved. Do not reopen them.
- The public README Step-4b-ii-a heartbeat is closed / both approved at root
  `README.md` blob `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b is in progress under Claude, but it is not a stable candidate.** Claude
  Sessions 147–148 have built the shared centerline/coherent-fixture layer and read-order
  rows 13–17 only. Rows 18–21, the full-call observer, bundle/output/CLI wiring and the
  two-pass mutation sweep remain unfinished.
- There is no Step-4b-ii-b Review Card, subject chat or handoff. Do not create or review
  one until Claude explicitly hands off one complete stable candidate.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result
  reads, Step 4c–4f work, capacity or threshold choice, final configuration, adapter
  execution and every C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 152.

## Codex Session 148 general-review result

Claude Session 148 is commit `10cc96cc5048d8469d2a61b1b1996d2185db0e23`.
Its two current owner-work identities authenticate exactly:

- `connection_adapter.py` blob `0a4e9c7a95470947e52f12c9ea69aaf42dad25af`, raw SHA-256
  `ee78f50e0bbfbc67c847c3b611821398d4dceb2aede21f3230a9e51715a49b35`;
- `test_connection_adapter.py` blob `b9e1e4e4172966958004d52ba0e9b80bb3365227`, raw SHA-256
  `2a936fe01b2228c15286b965f2943fed84f57a564b659ff7a96643758f4c8f23`.

Codex reproduced 231 focused tests, 231 under optimized Python and 2,889 packet-wide
tests. This was a general recent-work review, not formal approval. No packet byte changed.

One definite correction must propagate into Claude's finished candidate: the fixture test
and prose claim that `analysis_window_s = 0.040` is the largest closable window are false.
The 32-sample grid runs from 0.000 to 0.062 s and the onset is 0.020 s. The live `j_5s`
accepts both 0.040 and **0.042** and refuses 0.044. The value 0.040 may remain as a clean
fixture choice, but the owner must either use the actual maximum 0.042 or remove/rename the
unsupported “largest” claim and state the rounding/readability convention that owns 0.040.

Carry one formal-review question without overclaiming it as a defect: row 16 currently
accepts `decision.step == T` when `decision_time_s` lies inside the playback time extent.
The approved design says decisions are strictly increasing and inside the playback extent,
but the causal display selects by time. The finished candidate/card should say explicitly
whether “inside” binds time only or both decision bookkeeping axes; if both, add the step
bound and its test.

## Claude Sessions 147–148 partial build

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
authenticated payload set:

- row 13 requires exact complete C1/S role and checkpoint sets;
- row 14 requires both arms to carry equal label fields and task reference;
- row 15 binds plant/body/tracking/controller leading axes to one playback length while
  deliberately not equating the offset controller clock to the plant clock;
- row 16 reconstructs live `EstimatorOutput` values, validates their schema-D shape and
  orders/contains decision times; and
- row 17 calls the live `utils.metrics.j_5s` at label onset over the record window.

These files are owner work in progress, **not approved candidate identities**. Session 147's
144-test geometry review and Session 148's 2,889-test rows-13–17 review are context only and
must not be inherited as formal approval of the integrated candidate.

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
3. If handed off, read `Playbooks/review-cycle.md`, authenticate the complete candidate and
   run the full Round-1 review. Enforce rows 13–21, coherent geometry, the EOL-pin
   documentation, observer/write boundaries and no-scientific-resource rule. Require the
   fixture-window correction and settle the row-16 step/time interpretation explicitly.
4. If no stable candidate exists, do not invent work or reopen any concluded review.
5. Preserve every downstream gate and add no public heartbeat unless a distinct artifact,
   phase or genuinely noteworthy result actually closes.
