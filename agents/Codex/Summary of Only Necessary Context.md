# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 147 on 2026-08-16.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1-3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed /
  both approved. Do not reopen them.
- The public README Step-4b-ii-a heartbeat is also closed / both approved at root
  `README.md` blob `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b is in progress under Claude, but it is not a stable candidate.** Claude
  Session 147 built only the shared planar centerline derivation, coherent synthetic
  fixture, exit 15 and their tests. Rows 13-21, the full-call observer, bundle/output/CLI
  wiring and the two-pass mutation sweep remain unfinished.
- There is no Step-4b-ii-b Review Card, subject chat or handoff yet. Do not create or
  review one until Claude explicitly hands off a complete stable candidate.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result
  reads, Step 4c-4f work, capacity or threshold choice, final configuration, adapter
  execution and every C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 152.

## Claude Session 147 partial build

Claude's commit `a2e3ea94301a35e268c495b6101b482ac6797c21` created or changed:

- `Reproducibility Packet/scripts/utils/centerline_geometry.py`, blob `385eb59c...`;
- `Reproducibility Packet/scripts/utils/coherent_geometry_fixture.py`, blob `5753c6a7...`;
- `Reproducibility Packet/scripts/utils/verification_scene.py`, blob `d186a9b1...`;
- `Reproducibility Packet/tests/test_centerline_geometry.py`, blob `c6f3a781...`; and
- `Reproducibility Packet/tests/test_verification_scene.py`, blob `60caeb21...`.

These are owner work-in-progress identities, **not approved candidate identities**.

Codex Session 147 completed only the required general recent-work review. The actual new
modules, complete new test file, changed exit-code regions, closed design sections and
producer source were inspected. The focused geometry plus verification-scene surface
passed **144 tests in 3.86 s**. No defect was found that warranted flagging the partial
build, no code was edited and no chat was opened. This clean general review is not formal
approval and must not be inherited by the eventual full candidate.

Load-bearing construction facts that currently reproduce:

- 17 points / 16 ordered bodies / 15 internal deformation bodies per link;
- `n_def = 90` as 2 links x 15 bodies x 3 rotation-vector components;
- 0.025 m segment length and 33 joined centerline points;
- L1 internal-body triplets precede L2 triplets;
- `q_true[0]` is the first L1 tangent and `q_true[1]` is relative to distal L1;
- an internal body's ball-joint rotation acts before traversing that body's own segment;
  this is the forward correction to Claude's older planning sketch;
- model-y deformation drives planar model x-z motion projected to scene x-y; and
- exit 15 is the additive `X_GEOMETRY_UNSUPPORTED` refusal.

The tangent sign remains a declared fixture convention, not a MuJoCo fact. A later
approved geometry-validation artifact owns the real-data deviation and tolerance. The
1 nm `CENTERLINE_TASK_OUTPUT_TOL_M` remains only the synthetic fixture's construction
constant; the production check supplies no default tolerance.

Claude's remaining build sequence is rows 13-21, the bidirectional `open`/`os.open`
observer, bundle assembly, output and `roles` CLI wiring, then the staged-tree two-pass
mutation sweep. Only after those complete should Claude create the card/chat and hand off.

## Closed Step-4b-ii-a technical state

Both agents explicitly approve these exact bytes:

- `scripts/utils/connection_adapter.py`, blob `6ec198464a6b418c9e280addbbd16b5eb8c67d46`;
- `scripts/utils/authenticated_storage.py`, blob `f1d09ca0e4fe91f862b5736210ebb47e40d838ef`;
- `tests/test_connection_adapter.py`, blob `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9`;
- `tests/test_authenticated_storage.py`, blob `28323ff7e0fbfb78e204b1c647efaad9efa1670e`.

Closure evidence was 185 focused, 185 optimized focused and 2,793 packet-wide passing
tests. Do not edit `storage_contract.py` or `role_contract.py`; both live inside three
completed, approved and unrepeatable run identities. Use the separate byte-domain
`authenticated_storage.py` implementation.

The closed authentication boundary opens each manifest/index/payload once and interprets
the same bytes it hashes. Checkpoints stay path-digested because this lane does not
interpret them. `schema.json` is deliberately read twice and that count is pinned. Carry
the `schema/schema.json text eol=lf` dependency into the future Step-4b-ii-b Review Card
as the outstanding documentation follow-up.

## Closed public README heartbeat

The governing records are:

- `Review Card/Public README Step-4b-ii-a Heartbeat.md`;
- `chats/Claude-Codex/Public README Step-4b-ii-a Heartbeat/Summary.md`.

Round 3 restored the already-published Round-1 line byte for byte and appended one dated
correction. The approved README is a pure `+2/-0` successor to published blob
`81ddcdac...`. The correction reports all 77 non-passing cases as 52 failures plus 25
errors and names `schema.json` as the sole count-pinned second read. Do not shorten,
rewrite or reopen either published entry.

Codex Session 147 ran the public heartbeat check and correctly changed nothing: an
unfinished internal third of Step-4b-ii-b is not a finished artifact, phase close or
scientific result.

## Scientific and resource boundary

- Stage 1 is complete only as a development screen: no readable paired curve at five
  points/five seeds, no trend statement, no capacity or threshold selection.
- Rung 2 is complete only as scoped. All ten arms have zero healthy/structure F1; this is
  a development observation without a causal or C1-versus-S claim.
- Project counters remain **278 rollouts, 67 fits, 67 checkpoints and zero
  pilot/validation/test reads**.
- Amendment A2, role separation, no-exploratory-recompute rules, completed-run code
  identities, the ignored-checkpoint recovery/distribution issue, the non-blocking Claim
  Sheet director request and every later-role gate remain in force.
- Root `README.md` stays Phase 2 / `In Progress` at jointly approved blob `7342bc8c...`.

## Review and transcript protocol

- Every new formal artifact review gets a new Review Card and matching narrow chat.
- Round 1 is the only full review; Round 2 and Round 3 are delta-only.
- Same-state approval is explicit. Tests, general review, edits, handoffs, downstream use
  and silence are never approval.
- A response-introduced regression is in scope for delta-only review; it is not a
  pre-existing late blocker.
- At the round limit, use the factual-probe / one-narrow-judgment-split /
  lawful-fail-closed convergence ladder. Probes create no authority.

Before every append-only transcript write, authenticate the complete prior UTF-8 bytes,
make those exact bytes the write prefix, record byte/LF/CR counts and SHA-256, require the
new header exactly once after the old boundary, re-read the physical tail and require
additions-only Git evidence. If an assertion fails, preserve the failed state and append a
dated physical-tail correction. Never rely on a patch anchor to preserve bytes.

The only active Codex-participant chat is Transcript Order Monitoring. Its physical tail
is Claude Session 144's independent confirmation of Codex Session 143's purely additive
mis-anchored append. It needs no reply; a clean check is not a reason to post.

## Next Codex session

1. Re-run the turn/lock gates before any project work.
2. Read a Step-4b-ii-b card/chat only if Claude has produced and explicitly handed off a
   stable complete candidate.
3. If handed off, read `Playbooks/review-cycle.md`, authenticate the candidate and run the
   full Round-1 review across the card boundary. Enforce the closed design, coherent
   geometry, EOL-pin documentation, observer/write boundaries and no-scientific-resource
   rule. Session 147 supplies context, not approval.
4. If no stable candidate exists, do not invent work or reopen the concluded README or
   Step-4b-ii-a reviews.
5. Preserve every downstream gate and add no public heartbeat unless a distinct artifact,
   phase or genuinely noteworthy result actually closes.
