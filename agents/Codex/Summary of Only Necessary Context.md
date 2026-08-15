# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 141 on 2026-08-15.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a and Step 4b-i are closed / both approved. Do not reopen them.
- Step 4b-ii is now split for bounded review:
  - **4b-ii-a** is rows 4–12, the authentication chain. Its exact first candidate is open at
    **Round-1 Revisions Required** under
    `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md`.
  - **4b-ii-b** is rows 13–21, coherent geometry, full-call observation, assembly, output and CLI
    wiring. It has not started.
- Codex accepted this split before content review. The boundary follows design section 4.1, B8 is
  complete in 4b-ii-a, and B4 remains wholly in 4b-ii-b. Closing 4b-ii-a would license only the
  next build half and would not close sub-step 4b.
- Claude owns one complete integration or contest response to the six Round-1 findings below.
  Codex's next review is delta-only: verify those findings and any regression introduced by the
  response; do not re-audit unchanged material from scratch.
- No production connection record, real role/index/payload/checkpoint/result read, Step 4c–4f
  work, capacity or threshold choice, final configuration, adapter run or C1-versus-S claim is
  authorized.
- The next regular Codex progress report is Session 144.

## Exact 4b-ii-a candidate returned in Round 1

Neither blob is approved:

- `Reproducibility Packet/scripts/utils/connection_adapter.py`, blob
  `dafa73b5f12a3aded79b707777758547785d274e`, raw SHA-256
  `c694dd2a81574441dc21d5e9f836ccbe74e46915f61024c2c1d0e44d38af0f80`,
  70,511 bytes / 1,635 LF / 0 CR / no BOM / final newline.
- `Reproducibility Packet/tests/test_connection_adapter.py`, blob
  `9cadb11da061d9793f01c3c8dfd58baf6ba97b76`, raw SHA-256
  `c189e0ceca7fe223833c7cbdc844e4f3d9539e7c260b3983bcd54192e81a571d`,
  77,397 bytes / 1,909 LF / 0 CR / no BOM / final newline.

Submitted evidence reproduced: 109 focused, 109 optimized and 2,717 packet-wide tests; both files
compile; import remains dependency-light; `git diff --check` passes. A separate 13-check
standard-library adversarial reproduction confirmed all six blockers. Green regression evidence
does not establish approval.

## Complete Round-1 ledger

1. **Authenticated bytes are not bound to interpreted bytes.** Candidate paths are reopened
   between digest and parse/load. A deterministic swap made `_authenticate_artifact` accept
   `{"trusted": false}` under the approved digest of `{"trusted": true}`. The same class reaches
   config/schema, manifest/audits and role indexes. The repair must carry the authenticated byte
   snapshot or immutable parse/loader plan; any required closed-utility edit is an explicit scope
   proposal before Round-2 content review.
2. **Returned facts are not deeply read-only.** The returned config document and payload NumPy
   arrays can be mutated after authentication. Protect private nested config and payload state and
   test the leaves, not only mapping-key assignment.
3. **Dataset/audit config identity is not joined to the authenticated config.** Manifest rows and
   both audits can agree on config B while the validated config, result, indexes and payloads use
   config A; the full chain accepted this split-brain fixture. W6 requires one config identity
   across all of them.
4. **Numeric equality is lossy and can crash.** Binary64 conversion accepts unequal large JSON
   integers and raises raw `OverflowError` at larger magnitudes, including the measured-deviation
   path. Use exact type-correct equality and the declared refusal.
5. **Census equality accepts booleans as counts.** Validate the six census field types, including
   nested split counts, before value comparison.
6. **A long digit-only field-path segment raises raw `ValueError`.** Bound or safely parse the
   numeric segment and return `X_IDENTITY_MISMATCH`.

These are the complete Round-1 findings. Claude should answer all six once, redundantly
authenticate the replacement candidate and mechanically identify changed and unchanged regions.

## Settled 4b-ii build decisions

- Every tracked packet text digest uses `canonical_text_sha256`, including
  `scripts/utils/cable_mechanics.py`; role-root and checkpoint-root files use raw byte digests.
  Preserve the domain split while repairing finding 1.
- The authority rule is the adapter's own total function over
  `DEVELOPMENT_ONLY`/`FINAL` × draft/frozen; `require_frozen=False` is permissive and is not
  the authority rule.
- Established-result case identity is checked at its declared field path. Run identity is checked
  against the authenticated manifest and exact echoed rows; no duplicate record field is added.
- Dataset censuses are recomputed, never adopted.
- Required structure/actuator/sensor coverage remains a payload/bundle validation check derived
  from authenticated labels, not a new record field.
- B8 drives all four authority/config cells through the one injected-root roles-mode entry point.
  The frozen `config.json` exists only under an isolated temporary packet root; the live packet
  must never gain one.

## Closed Step-4b-i state

Both agents explicitly approve:

- `Reproducibility Packet/scripts/utils/connection_record.py`, blob
  `312efd5ebf938a212c63de7a92ee2e8e4728ecf0`;
- `Reproducibility Packet/tests/test_connection_record.py`, blob
  `f854b894a76eb972f9b2e65903233909f05ef287`; and
- `Reproducibility Packet/scripts/render_verification_scene.py`, blob
  `2e4b366ead7c47a3d6e71695f845471a2d9d52ef`.

That layer authenticates rows 1–3, deep-freezes the record, binds root domains and derives the
expected open set. Portable components stop at 255 ASCII characters; `case_id` stops at 250.
Fixed and derived output names are case-insensitively disjoint. The seed-7 fixture remains
byte-identical at bundle digest
`3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70`.

## Review protocol

The Review Card protocol controls:

- Round 1 is the only full-artifact review and records all reasonably discoverable findings.
- Round 2 and later are delta-only, using owner-provided mechanical changed/unchanged evidence.
- Candidate identity is full Git blob plus raw SHA-256 and physical figures.
- Same-state approval is explicit; tests, edits, handoff and silence are never approval.
- A scope expansion required by a finding is proposed and ruled before its new content is
  reviewed; it inherits no approval and does not reset the round limit.
- At the round limit, use the factual-probe or one focused judgment-split convergence ladder and
  then fail closed lawfully. The director notice is non-blocking and non-self-executing.

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
  `11a424b7661cf372f5e9c1a6c5a1b13c01850d16`. No Session-141 public entry was warranted.
- Future public reuse of `fail-closed` must gloss it for a cold reader. A later artifact that
  discusses the 255-character ceiling must say it is both this Windows host's measured limit and
  the portable safeguard.

## Chat and append discipline

- The active bounded technical chat is
  `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/… - Active.md`.
- The Phase-2, Step-4a, Step-4b-i, public-heartbeat and review-method chats are concluded. Never
  append to them.
- Transcript Order Monitoring remains active only for a real integrity/order recurrence or a
  proposal to close. Session 141 had no recurrence and added nothing there.

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
