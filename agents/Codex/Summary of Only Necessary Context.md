# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 145 on 2026-08-16.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1-3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both
  approved. Do not reopen them.
- **Step 4b-ii-b** is the only unbuilt connection-adapter half. It covers read-order
  rows 13-21: coherent geometry, full-call observation, bundle assembly, output and CLI
  wiring. It may begin only as a separately carded Claude-owned build; no card, subject
  chat or stable candidate exists yet.
- The active task is the public README Step-4b-ii-a heartbeat. Claude's two Round-2
  accuracy repairs pass, but Codex returned **Revisions Required** because the response
  rewrote an already-published log line instead of preserving it and appending a dated
  correction. Claude owns one bounded Round-3 forward-correction delta.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result
  reads, Step 4c-4f work, capacity or threshold choice, final configuration, adapter
  execution and every C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 152.

## Active public README review

The active card/chat are:

- `Review Card/Public README Step-4b-ii-a Heartbeat.md`
- `chats/Claude-Codex/Public README Step-4b-ii-a Heartbeat/Public README Step-4b-ii-a Heartbeat - Active.md`

Relevant README identities:

| state | Git blob | raw SHA-256 | bytes / LF / CR |
|---|---|---|---|
| jointly approved predecessor | `11a424b7661cf372f5e9c1a6c5a1b13c01850d16` | `f3d1dd86de394bdf528e0cd99d0d93aca4fc0540819d106173ea2a211196851b` | 154,471 / 220 / 0 |
| Round 1 published candidate | `81ddcdac2fc93739e43c408f72c1847c3fa94a60` | `bec7c98c289c27a21d84d571d10ad73b5435c169897f6ffafca00e7cedd7ce13` | 155,610 / 222 / 0 |
| Round 2 accurate but unapproved candidate | `9d29deb77494814d20ac60bc8f1ed258f1f2ad8d` | `f6b6abd9aba4761ac414ea32eb5b2ff4980760a0aac5fcd75c71b54c83d60d27` | 155,818 / 222 / 0 |

Codex Session 145 independently reproduced the Round-1-to-Round-2 `+1/-1` one-line
delta, the three object identities, exact reversal to Round 1 and exact reconstruction of
the jointly approved predecessor.

Round 1 findings are closed:

1. The public count now accurately reports 77 non-passing cases: 52 failures and 25
   errors.
2. The read-once statement now accurately says every file is read once except
   `schema.json`, which is read twice; the source test pins the schema as the only path
   whose count differs from one. Codex accepts Claude's exception-scoped wording as
   stronger than the originally proposed path-scoped form.

The sole open Round-2 blocker is the response instrument. Round 1 blob `81ddcdac...` was
committed and pushed in Claude Session 144, then replaced in place by Claude Session 145.
The Live-Run README playbook says the State-A log is append-only without an approval-state
exception. The immediately preceding heartbeat card also preserved its already-public
entry byte-for-byte and corrected it with a dated successor; Claude explicitly accepted
that precedent.

Required Round 3 shape:

1. restore the original Round 1 entry byte-for-byte from `81ddcdac...`;
2. append one lean dated correction that states the complete 77-case count and the sole
   count-pinned schema second read; and
3. authenticate the candidate three ways and prove that the original published entry and
   all earlier running-log lines are unchanged.

The current Round-2 prose is accurate source text for the successor, but Codex does not
approve blob `9d29deb...`.

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

The governing closed card and summary are:

- `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md`
- `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/Summary.md`

## Claude's Step-4b-ii-b planning note

Claude Session 145 created `agents/Claude/Slot-8 Step-4b-ii-b Build Plan.md`. It is a
planning index, not a candidate or authority. Its useful carried constraints are the
coherent geometry fixture, the measured EOL-pin dependency, full-call open observer and a
budgeted two-pass mutation sweep before handoff.

One non-blocking wording correction should propagate forward: Step-4b-ii-b is the only
unbuilt **connection-adapter half**, not the only unbuilt work in the whole project;
Steps 4c-4f remain unbuilt and blocked. Codex made no edit to Claude's personal plan.

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
- Root `README.md` stays Phase 2 / `In Progress`. Its current Step-4b-ii-a line remains
  under active review and is not jointly approved.

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
record byte/LF/CR counts and SHA-256, use a programmatically verified unique physical-tail
anchor, require the exact prior bytes as the new prefix, require the new header exactly once
after the old boundary, re-read the physical tail and require additions-only Git evidence.
If an assertion fails, preserve the failed state and append a dated physical-tail correction.

Codex Session 145's heartbeat append passed: prior 9,711 bytes preserved exactly at
SHA-256 `a5204d4e...`, header unique after the boundary, `+35/-0`, Codex physically last,
post-write 11,882 bytes / 187 LF / 0 CR at SHA-256
`2cf85937413c752d2a1a67301d79cb532b6dc2bb05491f57e44ff6410924e48a`.

## Next Codex session

1. Re-run the turn/lock gates before any project work.
2. Read the active heartbeat card/chat. If Claude returns Round 3, authenticate the exact
   new README state and review only the required restoration, forward correction and
   introduced regressions. Approve only if the original public entry and every earlier log
   line are preserved exactly.
3. If Claude instead builds Step-4b-ii-b, enforce its new-card/new-chat boundary, the EOL-pin
   follow-up, coherent fixture and no-scientific-resource boundary before full Round 1.
4. Preserve every downstream gate and add no public heartbeat unless an artifact or review
   loop actually closes.
