# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 144 on 2026-08-16.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1-3, Step 4a, Step 4b-i and **Step 4b-ii-a** are closed / both
  approved. Do not reopen them.
- **Step 4b-ii-b** is the only unbuilt part of the connection adapter. It covers
  read-order rows 13-21: coherent geometry, full-call observation, bundle assembly,
  output and CLI wiring. It is licensed to begin only under a new Review Card and a
  new narrow subject chat; it has not started.
- The active task Codex handed back is the public README Step-4b-ii-a heartbeat. Claude
  owns one bounded Round-2 prose repair after Codex returned two accuracy blockers.
- Full Step 4b, production connection records, real role/index/payload/checkpoint/result
  reads, Step 4c-4f work, capacity or threshold choice, final configuration, adapter
  execution and every C1-versus-S claim remain unauthorized.
- The next regular Codex progress report is Session 152.

## Closed Step-4b-ii-a technical state

Both agents explicitly approve these exact bytes:

- `Reproducibility Packet/scripts/utils/connection_adapter.py`, blob
  `6ec198464a6b418c9e280addbbd16b5eb8c67d46`, raw SHA-256
  `2f3cb4050a7c1d291ac3d75ce414ea2c2bf51d038cb6e23974f3e7054fadfe97`,
  97,541 bytes / 2,115 LF / 0 CR.
- `Reproducibility Packet/scripts/utils/authenticated_storage.py`, blob
  `f1d09ca0e4fe91f862b5736210ebb47e40d838ef`, raw SHA-256
  `7da660b1b840ee813360d1e0a9c9757c0fe68c6b0368814877cf3582530c3f62`,
  14,338 bytes / 336 LF / 0 CR.
- `Reproducibility Packet/tests/test_connection_adapter.py`, blob
  `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9`, raw SHA-256
  `1c6860ba13878ec6f693cb943b6e432a55fab22d741ab9602552b2eaf249ff07`,
  118,956 bytes / 2,959 LF / 0 CR.
- `Reproducibility Packet/tests/test_authenticated_storage.py`, blob
  `28323ff7e0fbfb78e204b1c647efaad9efa1670e`, raw SHA-256
  `f89bb783af5891041723ce958a9c70179d60ee96821f2aa5d0a62ed39fd95d97`,
  23,163 bytes / 547 LF / 0 CR.

The final evidence is 185 focused tests, 185 focused tests under optimized Python,
2,793 packet-wide tests, clean `py_compile`, clean fresh-interpreter imports and clean
`git diff --check` apart from ordinary Windows EOL warnings.

### Why the new storage module must remain separate

`role_contract.py` and `storage_contract.py` are two of the eight files in
`dev_fit_trainer.training_code_identity`. Three completed, jointly approved and
unrepeatable lanes record their exact digests: the development fit, Stage-1 capacity
sweep and rung-2 escalation. Editing the two closed files made the packet-wide suite
reach 52 failed / 25 errors and made the two read-only analyzers refuse those runs.

Do not edit those closed files or “de-duplicate” `authenticated_storage.py` back into
them. The new module reuses their validation rules while supplying byte-domain parsing
and loading mechanics outside every completed run identity.

### Authentication boundary that now holds

- `authenticated_bytes` opens once, hashes the bytes returned by that read, compares
  the digest and returns those same bytes for interpretation.
- Manifests, indexes and payloads are parsed/loaded from authenticated bytes; mappings
  and arrays are deeply read-only at the handoff.
- Checkpoints stay path-digested deliberately because this lane does not interpret them.
- `authenticate_config` compares the config's declared raw `schema_sha256` against the
  raw digest of the exact schema bytes the adapter authenticated before calling the
  closed config validator.
- One schema second read intentionally survives: `validate_config_document` re-derives
  the raw digest from `schema_path`. The complete-chain read count is pinned at two.
- `schema/schema.json text eol=lf` is therefore load-bearing for a second consumer.
  Carry one explicit documentation sentence about this into the Step-4b-ii-b card.
- `npz_archive_from_bytes` refuses a valid `.npy` stream as `StorageContractError`
  instead of leaking raw `TypeError`.

The governing closed card and durable summary are:

- `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md`
- `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/Summary.md`

## Active public README review

The active card/chat are:

- `Review Card/Public README Step-4b-ii-a Heartbeat.md`
- `chats/Claude-Codex/Public README Step-4b-ii-a Heartbeat/Public README Step-4b-ii-a Heartbeat - Active.md`

Claude's owner-approved candidate is root `README.md` at Git blob
`81ddcdac2fc93739e43c408f72c1847c3fa94a60`, raw SHA-256
`bec7c98c289c27a21d84d571d10ad73b5435c169897f6ffafca00e7cedd7ce13`,
155,610 bytes / 222 LF / 0 CR. The jointly approved predecessor is blob
`11a424b7661cf372f5e9c1a6c5a1b13c01850d16`, raw SHA-256
`f3d1dd86de394bdf528e0cd99d0d93aca4fc0540819d106173ea2a211196851b`.

Codex Session 144 authenticated the exact `+3/-1` delta and reconstructed the predecessor
byte for byte, but returned **Revisions Required** on two findings:

1. The entry says the reverted edit “broke 52 tests,” while the primary record is
   **52 failed and 25 errors**. State both categories or accurately summarize all 77
   non-passing cases.
2. The entry says “Every file the chain touches is now read exactly once,” although
   `schema.json` is deliberately read twice. Scope the first clause to the repaired
   manifest/index/payload path and explicitly name the count-pinned schema exception.

These are the complete Round-1 ledger. The banner date, append-only property, lean shape,
public-state boundary, earlier-log consistency and all non-authorizations pass. Codex made
no README edit and does not approve the candidate. Claude owns one bounded Round-2 prose
delta with exact changed/unchanged evidence.

## Closed upstream state that must stay closed

- Step 4b-i closed at exact blobs:
  - `connection_record.py` `312efd5ebf938a212c63de7a92ee2e8e4728ecf0`;
  - `test_connection_record.py` `f854b894a76eb972f9b2e65903233909f05ef287`;
  - `render_verification_scene.py` `2e4b366ead7c47a3d6e71695f845471a2d9d52ef`.
- Step 4a design closed at blob `032db1666efbe00adec5696de70424d531ba33a2`.
- The synthetic four-case fixture and figures prove the display mechanism only. They are
  fabricated, visibly labelled and not scientific evidence.
- `build_role_bundle` still refuses unconditionally with `X_CONNECTION_UNAUTHORIZED`.
  That is correct until the whole of Step 4b closes.

## Scientific and resource boundary

- Stage 1 is complete only as a development screen: no readable paired curve at five
  points/five seeds, no trend statement, no capacity or threshold selection.
- Rung 2 is complete only as scoped. All ten arms have zero healthy/structure F1; this is
  a development observation without a causal or C1-versus-S claim.
- Project counters remain **278 rollouts, 67 fits, 67 checkpoints and zero
  pilot/validation/test reads**.
- Amendment A2, role separation, no-exploratory-recompute rules, the completed-run code
  identities, the ignored-checkpoint recovery/distribution issue, the non-blocking Claim
  Sheet director request and every later-role gate remain in force.
- The root README remains Phase 2 / `In Progress`. Its current Step-4b-ii-a entry is under
  review and is not jointly approved.

## Review and transcript protocol

- Every new formal artifact review gets a new Review Card and matching narrow chat.
- Round 1 is the only complete review; Round 2 and Round 3 are delta-only.
- Same-state approval is explicit. Tests, edits, handoffs, downstream use and silence are
  never approval.
- If the round limit ends in disagreement, use the factual-probe / one-narrow-judgment-split /
  lawful-fail-closed convergence ladder. Probes create no authority.

Before every append-only transcript write:

1. read the UTF-8 physical tail and record byte/LF/CR counts plus SHA-256;
2. authenticate the complete prior bytes;
3. make the entire prior file travel as the exact byte prefix;
4. require the new session header exactly once after the old boundary;
5. reread the physical tail and require an additions-only Git diff; and
6. if an assertion fails, preserve the failed state and append a dated physical-tail
   correction before closeout.

Do not use a repeated speaker delimiter as a patch anchor. Codex Session 144's heartbeat
append passed: prior 3,728 bytes preserved exactly, header once after the boundary,
`+26/-0`, new chat SHA-256
`eb404abf5357819fead17b7c7431f2666898a585172a47e116e601755cc75a8e`.

## Next Codex session

1. Re-run the turn/lock gates before any project work.
2. Read the current Review Card and active heartbeat chat. If Claude returned Round 2,
   authenticate the new candidate, verify only the two repaired regions plus introduced
   regressions, and issue an explicit same-state verdict.
3. If Claude instead opened Step-4b-ii-b, enforce its new-card/new-chat boundary, confirm
   the EOL-pin follow-up is present and perform the appropriate full Round-1 review without
   reading any scientific resource.
4. Preserve every downstream gate and write no public heartbeat unless an artifact or
   review loop actually closes.
