# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 142 on 2026-08-15.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a and Step 4b-i are closed / both approved. Do not reopen them.
- Step 4b-ii remains split:
  - **4b-ii-a** is rows 4–12, the authentication chain. Its Review Card is open after **Round-2
    Revisions Required**. Findings 2–6 are closed; Finding 1 is the only remaining blocker.
  - **4b-ii-b** is rows 13–21, coherent geometry, full-call observation, assembly, output and CLI
    wiring. It has not started and remains unauthorized.
- Claude owns one integrated **Round-3** response using the accepted bounded utility expansion.
  Round 3 is the final ordinary delta round under this card; the expansion does not reset the limit.
- Codex's next review is delta-only: verify Finding 1 and regressions introduced by the expanded
  utility surface. Do not re-audit Findings 2–6 or unchanged prior material from scratch.
- No production connection record, real role/index/payload/checkpoint/result read, Step 4c–4f
  work, capacity or threshold choice, final configuration, adapter run or C1-versus-S claim is
  authorized.
- The next regular Codex progress report is Session 144.

## Exact Round-2 candidate — not approved

- `Reproducibility Packet/scripts/utils/connection_adapter.py`, blob
  `01653d9c7989fe25e7c50f75cac2f6a63f1432b6`, raw SHA-256
  `5c74d6c1d802f90ccd10ad1e7ead82eacaae352f42b64b9dada80ae2306b6ae4`, 92,425 bytes /
  2,050 LF / 0 CR / no BOM / final newline.
- `Reproducibility Packet/tests/test_connection_adapter.py`, blob
  `c5d4e023dafdd44598f11c6749c33751e0a0e371`, raw SHA-256
  `3156b28fd5fa329ee38552d80f2280b42e3ae1fc13e6506196d02673525ea2f9`, 104,170 bytes /
  2,619 LF / 0 CR / no BOM / final newline.

The exact delta from Round 1 is module `+502/-87` and tests `+711/-1`. Reviewer evidence passed 156
focused tests, 156 under optimized Python, 2,764 packet-wide tests, `py_compile`, `git diff --check`
and the dependency-light import check. Green regression evidence is not approval.

## Round-2 disposition

### Finding 1 remains blocking

Adapter-owned JSON inputs now use one authenticated byte snapshot, and the config uses the existing
document-level validator. Before/after brackets detect persistent manifest and index changes, but
they cannot bind what path-only utilities interpreted to the bytes authenticated outside the call.

The current state is worse than only the admitted swap-and-revert window. An independent
deterministic probe let `RolePayloadLoader.load` hash the original valid plant NPZ, replaced the
path immediately after that digest returned with a different schema-valid NPZ, and left the
replacement present. The complete `authenticate_connection` call accepted and returned replacement
`q_true[0,0] = -0.013959530380285051` under authenticated original
`-0.13895953038028505`. The candidate calls `loader.load` without any post-load identity check.

This is the existing Finding 1 on the changed row-12 seam, not a late blocker. A post bracket could
catch the persistent probe but not a within-call change and revert. Round 3 must make:

1. manifest rows derive from the exact bytes authenticated at row 6;
2. role-index rows derive from the exact bytes authenticated at row 8; and
3. payload arrays derive from the exact bytes authenticated at row 11.

Tests must directly drive the persistent payload swap and change-and-revert inside every formerly
path-only parser/loader seam. Final path equality does not prove the required property.

### Findings 2–6 are closed

- Validated config leaves are deeply read-only; payload arrays use immutable buffers and preserve
  dtype, shape and values, including zero-dimensional arrays.
- Both audits and every manifest row join to the authenticated config; all split-brain variants
  refuse.
- Numeric equality is exact without binary64 conversion; large unequal integers and huge deviation
  paths refuse with `X_IDENTITY_MISMATCH` rather than agreeing or crashing.
- Scalar and nested census counts require non-boolean JSON integers before equality.
- Field-path indexes are ASCII and length-bounded before integer conversion.

Do not reopen these findings in Round 3 unless the utility expansion changes their regions and
introduces a regression.

## Accepted bounded scope expansion

The expansion into the two closed foundational utilities is required and accepted under the current
card. It inherits no approval and does not reset the round limit.

Current baselines:

- `scripts/utils/storage_contract.py`: blob `9b1b9a4afe7547d7078b8391d157a42fa3ee2378`, raw
  SHA-256 `40b0f88c75d4f283197011f2470f8b97af639b78573734130c07bcafbc1a20fa`.
- `scripts/utils/role_contract.py`: blob `3d01f3d0bc39a2f083baee32c79975c691f9593c`, raw
  SHA-256 `c50bebe5dfab8685b16f421928c0774dddd24e4a6f87542954b65ddc48810a21`.
- `tests/test_role_contract.py`: blob `a2832859340049e71d9977b94172d42095b5cbb8`, raw
  SHA-256 `16637c535b40e09a3ddd4992e97ab7a5080552aac4bc409dfb13359c82a8d641`.
- `tests/test_data_contract.py`: blob `c205de5e62e7db28ad1a2a500d7e1b4f8636d741`, raw
  SHA-256 `4996c3103dd21824e40ffdad9432b6fd604935f3b783011a7382ff6e954d5ad6`.

Claude may touch only the utility-test files actually needed. Every touched file receives full Git
blob, raw SHA-256, physical figures and mechanical changed/unchanged evidence. Preserve utility
ownership of manifest/index parsing and payload containment/digest/schema/semantic validation;
do not reimplement those facts in the adapter. Existing path APIs should remain compatible wrappers
unless a separate justification is presented.

## Review protocol

- Round 1 is the only full review and records all reasonably discoverable findings.
- Round 2 and Round 3 are delta-only, using mechanical changed/unchanged evidence.
- Candidate identity is full Git blob plus raw SHA-256 and physical figures.
- Same-state approval is explicit; tests, edits, handoff and silence are never approval.
- Scope-expanded artifacts inherit no approval and do not reset the round limit.
- If Round 3 does not reach same-state closure, apply the already agreed factual/judgment
  convergence ladder and lawful fail-closed outcome. The director notice remains non-blocking and
  non-self-executing.

## Closed Step-4b-i state

Both agents explicitly approve:

- `Reproducibility Packet/scripts/utils/connection_record.py`, blob
  `312efd5ebf938a212c63de7a92ee2e8e4728ecf0`;
- `Reproducibility Packet/tests/test_connection_record.py`, blob
  `f854b894a76eb972f9b2e65903233909f05ef287`; and
- `Reproducibility Packet/scripts/render_verification_scene.py`, blob
  `2e4b366ead7c47a3d6e71695f845471a2d9d52ef`.

That layer authenticates rows 1–3, deep-freezes the record, binds root domains and derives the
expected open set. Portable components stop at 255 ASCII characters; `case_id` stops at 250. Fixed
and derived output names are case-insensitively disjoint. The seed-7 fixture remains byte-identical
at bundle digest `3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70`.

## Scientific and public boundaries

- Stage 1 is complete only as a development screen: no readable paired shape at five points / five
  seeds, no licensed trend statement and no capacity or threshold selected.
- Rung 2 is complete only as scoped. Its fit/analyzer authorizations are spent; all ten arms have
  zero healthy and structure F1, a development observation rather than a causal claim.
- The Slot-8 synthetic fixture proves the display mechanism, not a scientific result. The real-role
  path still refuses before a scientific file opens.
- Project counters remain 278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test
  reads.
- Amendment A2, role separation, no-exploratory-recompute rules, the 67-checkpoint distribution and
  recovery issue, the non-blocking Claim Sheet director request and every unspent gate remain in
  force.
- Root `README.md` remains Phase 2 / `In Progress` at jointly approved blob
  `11a424b7661cf372f5e9c1a6c5a1b13c01850d16`. No Session-142 public entry was warranted.
- Future public reuse of `fail-closed` must gloss it for a cold reader. Any later artifact that
  discusses the 255-character ceiling must say it is both this Windows host's measured limit and
  the portable safeguard.

## Chat and append discipline

- The active bounded technical chat is
  `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/… - Active.md`.
- After Codex Session 142 it is 29,767 bytes / 454 LF / 0 CR at SHA-256
  `553a81fbf5d6e0b367838182f8656c147f5c7cc79ea5a334b9f1855f9c0ebc20`.
- The Phase-2, Step-4a, Step-4b-i, public-heartbeat and review-method chats are concluded. Never
  append to them.
- Transcript Order Monitoring remains active only for a real integrity/order recurrence or a
  proposal to close. Session 142 had no recurrence and added nothing there.

Before every transcript append:

1. read the UTF-8 physical tail and record byte/line counts and SHA-256;
2. authenticate the complete prior bytes;
3. preserve the whole prior file as the exact byte prefix;
4. verify the new session header occurs exactly once after the old boundary;
5. reread the physical tail and require an additions-only Git diff; and
6. if any assertion fails, preserve the failed state and append a dated physical-tail correction
   before closeout.

Do not use a text patch as evidence of byte preservation on a mixed-EOL file. The asserted prior
bytes themselves must travel as the prefix.
