# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 140 on 2026-08-15.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a and Step 4b-i are closed / both approved. Do not reopen them.
- The public Step-4b-i heartbeat review is also closed at **Approved with Follow-ups** on exact
  `README.md` blob `11a424b7661cf372f5e9c1a6c5a1b13c01850d16`.
- The director's bounded review method and the replacement for blocking `Escalated` are implemented,
  jointly confirmed and documented in `Playbooks/review-cycle.md` and `Review Card/README.md`.
- Step 4b-ii has not started. Claude owns one new adapter-and-test build under a new Review Card and
  narrow subject chat. Codex should wait for the explicitly approved candidate and then perform the
  one full-artifact Round-1 review.
- No production connection record, real role/index/payload/checkpoint/result read, Step 4c–4f work,
  capacity or threshold choice, final configuration, adapter run, or C1-versus-S claim is authorized.
- The next regular Codex progress report is Session 144.

## Closed Step-4b-i state

Both agents explicitly approve:

- `Reproducibility Packet/scripts/utils/connection_record.py`, blob
  `312efd5ebf938a212c63de7a92ee2e8e4728ecf0`, raw SHA-256
  `efc547ad9aab9a3682fb29ebae906bfe314a11531ebb4d4da1095c6a7d3b019a`;
- `Reproducibility Packet/tests/test_connection_record.py`, blob
  `f854b894a76eb972f9b2e65903233909f05ef287`, raw SHA-256
  `2933e80bd72b1786b74acb335c35efaf5412b4c646c04e32332cc7481a52e2aa`;
- `Reproducibility Packet/scripts/render_verification_scene.py`, blob
  `2e4b366ead7c47a3d6e71695f845471a2d9d52ef`, raw SHA-256
  `83473e7aa15c1f072204a4c378044639e41147b7865670018eec8b4bcf7c8ff4`.

The connection-record layer strict-parses and authenticates rows 1–3, deep-freezes state, binds
declared paths to one injected packet root and derives the expected open set. Portable components
stop at 255 ASCII characters; `case_id` stops at 250 so renderer suffixes fit. Fixed/derived output
names are case-insensitively disjoint, and the renderer validates the complete write set before any
file publishes. The seed-7 fixture remains byte-identical at bundle digest
`3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70`.

Closure evidence: 341 focused, 341 optimized and 2,608 packet-wide passing tests; a separate
19-check boundary audit; `py_compile`; `git diff --check`; and exact seed-7 regeneration. Step
4b-i closure licenses only the separate Step-4b-ii build.

## Closed public README review

Both agents approve current `README.md` at:

- Git blob `11a424b7661cf372f5e9c1a6c5a1b13c01850d16`;
- raw SHA-256 `f3d1dd86de394bdf528e0cd99d0d93aca4fc0540819d106173ea2a211196851b`;
- 154,471 bytes / 220 LF / 0 CR / no BOM / final newline.

The original Step-4b-i heartbeat remains byte-identical. A dated forward correction says the
case-insensitive collision and partial-output failure reproduced on this project's Windows host,
while the 255-character ceiling is the portability safeguard. The banner date is 2026-08-15. The
review closed at **Approved with Follow-ups**:

1. if a future public entry reuses `fail-closed`, gloss it for a cold reader; and
2. any later artifact discussing the 255-character ceiling must say it is both this Windows host's
   measured limit (255 succeeds, 256 fails) and the portable safeguard.

These are forward obligations, not reasons to edit the approved README. The concluded card/chat
record is in `Review Card/Public README Step-4b-i Heartbeat.md` and
`chats/Claude-Codex/Public README Step-4b-i Heartbeat/`.

## Review method now in force

The Review Card protocol remains controlling: Round 1 is the only full-artifact review; later rounds
are delta-only; candidate ids are authenticated redundantly; owner responses mechanically identify
changed and unchanged regions; scope expansion is explicit and ruled before content; and same-state
approval is always explicit.

At the round limit, `Escalated` is no longer a blocking terminal outcome:

1. classify the residual disagreement as factual or judgment in the max-round turn;
2. a factual issue gets one precommitted probe and one counterproposal maximum, but the probe
   creates no authority and may spend no gated resource;
3. a judgment issue may split once into an exact narrow candidate carrying both positions verbatim,
   with one owner handoff, one reviewer response and one genuine owner re-review;
4. if that focused round-trip does not converge, withhold the contested element or whole candidate
   lawfully and fail closed; and
5. record both positions in the card and `director_requests.md` without blocking other work. Any
   later reinstatement is a new candidate under a new card.

The ceiling is at most two further agent sessions for a factual issue and three for a judgment
issue, measured from the classification turn. The concluded director-visible record is
`chats/Claude-Codex-Human/Review Boundary and Convergence/`.

## Step-4b-ii forward decisions

Claude's new card/build must carry both settled decisions:

1. `render_geometry.source.producer_sha256` uses `canonical_text_sha256` for
   `scripts/utils/cable_mechanics.py`, and the same tracked-text domain applies to other runtime
   text digests. The current file is 20,987 bytes / 527 LF / 0 CR; raw and canonical SHA-256 are
   both `1acaf60c4c4206ece0bb5ce6a6e7b13e26951b34a0f78c07f913015642b5d0bb` under
   `core.autocrlf=true`. Do not add an EOL pin merely to make an unportable raw rule pass.
2. Required `structure` / `actuator` / `sensor` coverage is a payload/bundle validation check, not
   a new record field. A case's source class comes from its authenticated `labels` payload; a
   duplicate record field would create a contradiction surface.

The build also carries read-order rows 4–21, the coherent geometry fixture, exit-15
`X_GEOMETRY_UNSUPPORTED`, the audit-hook observer, B2/B3/B4/B5/B8, roles CLI wiring, the additive
`build_role_bundle` change and a two-pass mutation sweep before handoff. These are planning facts,
not authorization for production or scientific reads.

## Scientific and public boundaries

- Stage 1 is complete only as a development screen: no readable paired shape at five points / five
  seeds, no licensed trend statement, and no capacity or threshold selected.
- Rung 2 is complete only as scoped. Its fit/analyzer authorizations are spent; all ten arms have
  zero healthy and structure F1, a development observation rather than a causal claim.
- The Slot-8 synthetic fixture proves the display mechanism, not a scientific result. The real-role
  path still refuses before a scientific file opens.
- Project counters remain 278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads.
- Amendment A2, role separation, no-exploratory-recompute rules, the 67-checkpoint distribution and
  recovery issue, the non-blocking Claim Sheet director request and every unspent gate remain in force.
- Root `README.md` remains Phase 2 / `In Progress`; no Session-140 public log entry was warranted.

## Chat and append discipline

- The Phase-2, Step-4a, Step-4b-i, public-heartbeat and review-method chats are concluded. Never
  append to them.
- The only active Codex-participating chat is Transcript Order Monitoring. Use it only for an
  actual integrity/order recurrence or a proposal to close.
- Claude's future Step-4b-ii build requires a new Review Card and a new narrow chat; do not reuse a
  concluded subject.

Before every transcript append:

1. read the UTF-8 physical tail and record byte/line counts and SHA-256;
2. authenticate the complete prior bytes;
3. write the whole prior file as the exact prefix plus the new payload;
4. verify the new session header occurs exactly once after the old byte boundary;
5. reread the physical tail and require an additions-only Git diff; and
6. if any assertion fails, preserve the failed state and append a dated physical-tail correction
   before closeout.

Do not use a text patch as evidence of byte preservation on a mixed-EOL file. The asserted prior
bytes themselves must travel as the prefix.
