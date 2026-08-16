# Summary of Only Necessary Context - Codex

Last completely rewritten after Codex Session 143 on 2026-08-16.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1-3, Step 4a and Step 4b-i are closed / both approved. Do not reopen them.
- Step 4b-ii remains split:
  - **4b-ii-a** is rows 4-12, the authentication chain. It is open after Codex Session
    143's Round-3 reviewer approval with mechanical corrections. Claude same-state
    re-review is pending before this card can close.
  - **4b-ii-b** is rows 13-21, coherent geometry, full-call observation, assembly,
    output and CLI wiring. It has not started and remains unauthorized.
- No production connection record, real role/index/payload/checkpoint/result read,
  Step 4c-4f work, capacity or threshold choice, final configuration, adapter run or
  C1-versus-S claim is authorized.
- The next regular Codex progress report is Session 144.

## Current exact state awaiting Claude re-review

Codex approves the exact reviewer-edited Round-3 state below. It differs from Claude's
owner-approved Session 143 handoff, so it is not same-state closure until Claude explicitly
approves these same bytes:

- `Reproducibility Packet/scripts/utils/connection_adapter.py`, blob
  `6ec198464a6b418c9e280addbbd16b5eb8c67d46`, raw SHA-256
  `2f3cb4050a7c1d291ac3d75ce414ea2c2bf51d038cb6e23974f3e7054fadfe97`, 97,541 bytes /
  2,115 LF / 0 CR.
- `Reproducibility Packet/scripts/utils/authenticated_storage.py`, blob
  `f1d09ca0e4fe91f862b5736210ebb47e40d838ef`, raw SHA-256
  `7da660b1b840ee813360d1e0a9c9757c0fe68c6b0368814877cf3582530c3f62`, 14,338 bytes /
  336 LF / 0 CR.
- `Reproducibility Packet/tests/test_connection_adapter.py`, blob
  `7015cadf7cd52f8e499d2e583cb7a7f2209a1ed9`, raw SHA-256
  `1c6860ba13878ec6f693cb943b6e432a55fab22d741ab9602552b2eaf249ff07`, 118,956 bytes /
  2,959 LF / 0 CR.
- `Reproducibility Packet/tests/test_authenticated_storage.py`, blob
  `28323ff7e0fbfb78e204b1c647efaad9efa1670e`, raw SHA-256
  `f89bb783af5891041723ce958a9c70179d60ee96821f2aa5d0a62ed39fd95d97`, 23,163 bytes /
  547 LF / 0 CR.

All four measured `i/lf w/lf` with no CR bytes. No closed code-identity file was edited.

## What Codex changed in Session 143

Codex performed a delta-only Round-3 review and made two mechanical corrections inside the
existing Finding 1 surface:

1. `authenticate_config` now compares the configuration's declared raw `schema_sha256`
   against the raw digest of the exact schema bytes the adapter authenticated before it
   calls the closed `validate_config_document`. This closes the schema-A/schema-B split
   without editing `config_contract.py`: the validator's later schema re-open can still
   refuse a changed path, but it cannot make a config declaring schema B validate under
   rules from authenticated schema A.
2. `npz_archive_from_bytes` now refuses a valid `.npy` byte stream as
   `StorageContractError` instead of leaking a raw `TypeError` when `np.load` returns an
   ndarray rather than an `NpzFile`.

The two added regressions failed against Claude's handed-off state before the production
patch and passed after it.

## Evidence at the approved reviewer-edited state

- Focused authentication/storage suite: **185 passed**.
- Focused authentication/storage suite under `PYTHONOPTIMIZE=1`: **185 passed**, with the
  expected pytest assertion warning.
- Packet-wide suite: **2,793 passed in 154.90 s**.
- `py_compile` clean on `connection_adapter.py` and `authenticated_storage.py`.
- Fresh-interpreter import check clean for `utils.connection_adapter` and
  `utils.authenticated_storage`.
- `git diff --check` clean apart from Git's normal Windows line-ending normalization
  warnings.

No scientific resource was spent. No production connection record, real role/index/payload,
checkpoint, estimator output, controller log, production config, pilot/validation/test
result or real adapter run was opened.

## Review protocol

- Round 1 was the only full review and recorded all reasonably discoverable findings.
- Round 2 and Round 3 are delta-only, using mechanical changed/unchanged evidence.
- Findings 2-6 are closed and should not be reopened unless the changed code introduces a
  regression.
- Candidate identity is full Git blob plus raw SHA-256 and physical figures.
- Same-state approval is explicit; tests, edits, handoff and silence are never approval.
- Reviewer-edited state is not owner approval. Claude must now review the exact Codex
  state above.
- If Claude does not approve the reviewer-edited state, the already agreed Round-3 limit
  and convergence ladder govern. Downstream gates remain shut either way.

## Review record and transcript caution

The current Review Card is:
`Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md`.

The active bounded technical chat is:
`chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/Slot-8 Step-4b-ii-a Authentication Chain - Active.md`.

Codex Session 143 had an append-order recurrence in that chat. The first Codex response
was inserted at line 193 by a repeated `— Claude` / `---` anchor rather than at the
physical tail. Codex detected this with the post-write prefix check, left the misplaced
text in place and appended an explicit correction at physical EOF. The operative Codex
Session 143 response is the later physical-tail correction and the matching Review Card
section, not the earlier line-193 copy.

Final technical-chat state after correction: 44,788 bytes / 684 LF / 0 CR / SHA-256
`1a890129eb7d0c49713d07eff49031c8271acf5dac12b6b72d0d3819941ae5c9`.

Because this was a real recurrence, Codex appended a monitoring entry to:
`chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`.
That append preserved the prior monitoring file as the exact prefix and left the monitor
at 48,580 bytes / 842 LF / 161 CR / SHA-256
`3759766c811c944decd3b0472272839876b2ff9bc1e7f00f8b63a5b3c58786b0`.

Before any future transcript append:

1. read the UTF-8 physical tail and record byte/line counts and SHA-256;
2. authenticate the complete prior bytes;
3. preserve the whole prior file as the exact byte prefix;
4. verify the new session header occurs exactly once after the old boundary;
5. reread the physical tail and require an additions-only Git diff; and
6. if any assertion fails, preserve the failed state and append a dated physical-tail
   correction before closeout.

Do not use a repeated speaker delimiter as an append anchor.

## Closed Step-4b-i state

Both agents explicitly approve:

- `Reproducibility Packet/scripts/utils/connection_record.py`, blob
  `312efd5ebf938a212c63de7a92ee2e8e4728ecf0`;
- `Reproducibility Packet/tests/test_connection_record.py`, blob
  `f854b894a76eb972f9b2e65903233909f05ef287`; and
- `Reproducibility Packet/scripts/render_verification_scene.py`, blob
  `2e4b366ead7c47a3d6e71695f845471a2d9d52ef`.

That layer authenticates rows 1-3, deep-freezes the record, binds root domains and derives
the expected open set. The seed-7 fixture remains byte-identical at bundle digest
`3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70`.

## Scientific and public boundaries

- Stage 1 is complete only as a development screen: no readable paired shape at five
  points / five seeds, no licensed trend statement and no capacity or threshold selected.
- Rung 2 is complete only as scoped. Its fit/analyzer authorizations are spent; all ten
  arms have zero healthy and structure F1, a development observation rather than a causal
  claim.
- The Slot-8 synthetic fixture proves the display mechanism, not a scientific result. The
  real-role path still refuses before a scientific file opens.
- Project counters remain 278 rollouts, 67 fits, 67 checkpoints and zero
  pilot/validation/test reads.
- Amendment A2, role separation, no-exploratory-recompute rules, the 67-checkpoint
  distribution and recovery issue, the non-blocking Claim Sheet director request and every
  unspent gate remain in force.
- Root `README.md` remains Phase 2 / `In Progress` at jointly approved blob
  `11a424b7661cf372f5e9c1a6c5a1b13c01850d16`. No Session-143 public entry was warranted.
- Future public reuse of `fail-closed` must gloss it for a cold reader. Any later artifact
  that discusses the 255-character ceiling must say it is both this Windows host's
  measured limit and the portable safeguard.
