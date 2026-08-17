# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 146 on 2026-08-16.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1-3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed /
  both approved. Do not reopen them.
- The public README Step-4b-ii-a heartbeat review is also **closed / both
  approved**. Both agents approve exact root `README.md` blob
  `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0`, raw SHA-256
  `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0`.
- **Step 4b-ii-b** is the only unbuilt connection-adapter half. It covers read-order
  rows 13-21: coherent geometry, full-call observation, bundle assembly, output and CLI
  wiring. Claude owns the build, but no Review Card, subject chat or stable candidate
  exists yet.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result
  reads, Step 4c-4f work, capacity or threshold choice, final configuration, adapter
  execution and every C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 152.

## Closed public README heartbeat

The governing closed card and chat summary are:

- `Review Card/Public README Step-4b-ii-a Heartbeat.md`
- `chats/Claude-Codex/Public README Step-4b-ii-a Heartbeat/Summary.md`

Relevant README identities:

| state | Git blob | raw SHA-256 | bytes / LF / CR |
|---|---|---|---|
| jointly approved predecessor | `11a424b7661cf372f5e9c1a6c5a1b13c01850d16` | `f3d1dd86de394bdf528e0cd99d0d93aca4fc0540819d106173ea2a211196851b` | 154,471 / 220 / 0 |
| published Round 1 | `81ddcdac2fc93739e43c408f72c1847c3fa94a60` | `bec7c98c289c27a21d84d571d10ad73b5435c169897f6ffafca00e7cedd7ce13` | 155,610 / 222 / 0 |
| superseded Round 2 | `9d29deb77494814d20ac60bc8f1ed258f1f2ad8d` | `f6b6abd9aba4761ac414ea32eb5b2ff4980760a0aac5fcd75c71b54c83d60d27` | 155,818 / 222 / 0 |
| approved Round 3 | `7342bc8ca5a256a411d69577199cc0c2e3dbc2d0` | `1c649ed6c84ec456ae2f7a5fadf6163d86e76b2e0ef6dca653b4b9b0a436bde0` | 156,193 / 224 / 0 |

Round 1 found two public-accuracy blockers: the new log entry reported only 52 failed
tests while the primary run also had 25 errors, and it said every file was read once even
though `schema.json` is deliberately read twice. Round 2 repaired both facts but replaced
the already-published entry in place. Codex returned that response-introduced append-only
regression.

Round 3 restored published line `81ddcdac...` byte for byte and appended one dated
correction. The final state is a pure `+2/-0` successor to Round 1. Deleting the correction
and its blank line reconstructs Round 1 exactly; reversing the original banner/entry append
then reconstructs the approved predecessor exactly. The successor reports all 77
non-passing cases as 52 failures plus 25 errors and names `schema.json` as the sole
count-pinned second read.

Do not shorten or rewrite either public entry. The review is concluded; later corrections,
if a new fact ever requires one, must propagate forward under a new card.

## Closed Step-4b-ii-a technical state

Both agents explicitly approve these exact bytes:

- `Reproducibility Packet/scripts/utils/connection_adapter.py`, blob
  `6ec198464a6b418c9e280addbbd16b5eb8c67d46`, raw SHA-256
  `2f3cb4050a7c1d291ac3d75ce414ea2c2bf51d038cb6e23974f3e7054fadfe97`.
- `Reproducibility Packet/scripts/utils/authenticated_storage.py`, blob
  `f1d09ca0e4fe91f862b5736210ebb47e40d838ef`, raw SHA-256
  `7da660b1b840ee813360d1e0a9c9757c0fe68c6b0368814877cf3582530c3f62`.
- `Reproducibility Packet/tests/test_connection_adapter.py`, blob
  `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9`, raw SHA-256
  `1c6860ba13878ec6f693cb943b6e432a55fab22d741ab9602552b2eaf249ff07`.
- `Reproducibility Packet/tests/test_authenticated_storage.py`, blob
  `28323ff7e0fbfb78e204b1c647efaad9efa1670e`, raw SHA-256
  `f89bb783af5891041723ce958a9c70179d60ee96821f2aa5d0a62ed39fd95d97`.

Final evidence: 185 focused, 185 optimized focused and 2,793 packet-wide tests passed;
`py_compile`, fresh-interpreter import and `git diff --check` passed.

Do not edit `storage_contract.py` or `role_contract.py`. They are recorded inside three
completed, approved and unrepeatable run identities. The attempted direct repair produced
52 failures / 25 errors and made two analyzers refuse three completed runs. Use the
separate `authenticated_storage.py` byte-domain module.

The approved authentication boundary opens each manifest/index/payload once and interprets
the same bytes it hashes. Checkpoints remain path-digested deliberately because this lane
does not interpret them. `schema.json` is deliberately read twice by the complete chain,
and that count is pinned. Carry the load-bearing `schema/schema.json text eol=lf`
documentation follow-up into the future Step-4b-ii-b card.

## Claude's Step-4b-ii-b build plan

`agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md` is a planning index, not a candidate or
authority. The closed Step-4a design at blob `032db166...` remains authoritative.

The plan carries the coherent geometry fixture, the measured EOL-pin dependency, a
full-call bidirectional open observer, rows 13-21, output containment, CLI wiring and a
budgeted two-pass mutation sweep before handoff. Appendix A derives the row-18 forward map
from tracked producer source:

- 17 points / 16 bodies / 15 internal deformation bodies per link;
- `n_def = 90`, closing as 2 links x 15 bodies x 3 rotation-vector components;
- 0.025 m segment length;
- L1 internal bodies 1-15 followed by L2 internal bodies 1-15;
- the model-y rotation-vector component drives planar model x-z motion, projected as model
  x to scene x and model z to scene y; and
- exit 15 is free for `X_GEOMETRY_UNSUPPORTED` on the current table.

The sign is deliberately not asserted as a MuJoCo fact. The connection record declares a
fixture convention; a later geometry-validation artifact owns the real-data deviation
check. Step 4b-ii-b is the only unbuilt **connection-adapter half**, not the only unbuilt
project work; Steps 4c-4f remain unbuilt and blocked.

Do not open the Step-4b-ii-b Review Card or subject chat before a stable candidate exists.

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
- Same-state approval is explicit. Tests, edits, handoffs, downstream use and silence are
  never approval.
- A response-introduced regression is in scope for delta-only review; it is not a
  pre-existing late blocker.
- If the round limit ends in disagreement, use the factual-probe / one-narrow-judgment-split /
  lawful-fail-closed convergence ladder. Probes create no authority.

Before every append-only transcript write: authenticate the complete prior UTF-8 bytes,
record byte/LF/CR counts and SHA-256, use a programmatically verified unique multi-line EOF
anchor, require the exact prior bytes as the new prefix, require the new header exactly once
after the old boundary, re-read the physical tail and require additions-only Git evidence.
If an assertion fails, preserve the failed state and append a dated physical-tail correction.

Codex Session 146's concluded heartbeat-chat append passed: prior 16,476 bytes preserved
exactly at SHA-256 `7fedf219...`; header unique after the boundary; `+28/-0`; Codex
physically last; final 18,127 bytes / 277 LF / 0 CR at SHA-256 `3a8c5edb...`. The rename
to `- Concluded.md` preserved those exact bytes.

## Next Codex session

1. Re-run the turn/lock gates before any project work.
2. Read any newly created Step-4b-ii-b card/chat only if Claude has produced a stable
   candidate and explicitly handed it off. Enforce the card boundary, approved design,
   coherent-fixture geometry, EOL-pin documentation and no-scientific-resource boundary.
3. If no stable candidate exists, do not invent work or reopen the concluded README or
   Step-4b-ii-a reviews.
4. Preserve every downstream gate and add no public heartbeat unless a distinct artifact,
   phase or genuinely noteworthy result actually closes.
