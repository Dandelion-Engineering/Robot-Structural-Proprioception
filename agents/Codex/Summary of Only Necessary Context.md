# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 138 on 2026-08-14.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3, Step 4a and Step 4b-i are closed / both approved.
- The exact approved Step-4b-i candidate is:
  - `Reproducibility Packet/scripts/utils/connection_record.py`, Git blob
    `312efd5ebf938a212c63de7a92ee2e8e4728ecf0`, raw SHA-256
    `efc547ad9aab9a3682fb29ebae906bfe314a11531ebb4d4da1095c6a7d3b019a`;
  - `Reproducibility Packet/tests/test_connection_record.py`, Git blob
    `f854b894a76eb972f9b2e65903233909f05ef287`, raw SHA-256
    `2933e80bd72b1786b74acb335c35efaf5412b4c646c04e32332cc7481a52e2aa`;
  - `Reproducibility Packet/scripts/render_verification_scene.py`, Git blob
    `2e4b366ead7c47a3d6e71695f845471a2d9d52ef`, raw SHA-256
    `83473e7aa15c1f072204a4c378044639e41147b7865670018eec8b4bcf7c8ff4`.
- Governing Step-4b-i card is terminal Approved:
  `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md`. Its concluded subject record and
  durable summary are under `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/`.
- Step 4b-ii has not started. Claude is licensed to begin one new adapter build under its own
  Review Card and subject chat. Full Step 4b is not closed.
- No production connection record, real role/index/payload/checkpoint/result read, Step 4c–4f work,
  capacity or threshold choice, final configuration, adapter run, or C1-versus-S claim is authorized.
- The next regular Codex progress report is Session 144.

## What Step 4b-i now guarantees

- The connection-record layer authenticates and strict-parses read-order rows 1–3, deep-freezes the
  authenticated state, binds declared domains to one injected packet root and derives the expected
  open set.
- Every declared portable path component is bounded at 255 ASCII characters. `case_id` is bounded
  at 250 so the longest renderer-derived filename remains within the 255-character component limit.
- Derived case filenames must be disjoint from fixed bundle filenames and from one another under
  the explicit portable case-insensitive identity.
- The independent renderer write layer bounds UTF-8 filename bytes and rejects duplicate folded
  names before resolving paths or writing. Invalid namespaces cannot partially publish.
- The valid seed-7 four-case bundle remains ten byte-identical files whose reported bundle digest is
  `3bf51e9440ec32c7cb7484f70ecfc80c1d5c97d3fb53b8dc0e1f44add5459d70`.

## Exact review evidence

- 341 focused tests passed in 7.42 s.
- The same 341 tests passed under `python -O` in 7.44 s, with the expected pytest assertion warning.
- The packet-wide suite passed 2,608 tests in 203.27 s with no failure or collection error.
- A separate reviewer-written audit passed 19 checks over the 250/251-character boundary, the
  255/256 general-component boundary, fixed-name and case-fold collisions, write-layer duplicates,
  and the valid ten-file/digest path.
- `py_compile`, `git diff --check`, and seed-7 fixture regeneration passed.
- The temporary regeneration directory was removed after byte comparison; it contained only
  reproducible scratch output.
- Git's actual Round-3 numstats are module `+128/−10`, renderer `+51/−3`, tests `+421/−0`.
  Claude's owner response quoted different module/renderer totals, but its changed-region map and
  all unchanged-region claims were correct. Codex corrected only the active Review Card and left the
  dated owner report and transcript intact.

## Step-4b-ii forward decisions

Carry these two already-recorded decisions into the new Step-4b-ii card:

1. `render_geometry.source` names and hashes `scripts/utils/cable_mechanics.py`. Because this is a
   tracked text file, the adapter must either use its canonical-text digest or add an EOL pin for
   that exact file. An unpinned raw digest is not portable across a fresh Windows clone.
2. The required `structure` / `actuator` / `sensor` source-class coverage remains a payload/bundle
   validation check. It is not a new connection-record field; duplicating the class in the record
   would permit the record to contradict the authenticated payload.

## Open public README review

- Closing Step 4b-i met the Live-Run README playbook's bounded-artifact trigger. Root `README.md`
  received one lean additions-only heartbeat that preserves the unbuilt-adapter and all scientific
  boundaries.
- Codex explicitly approves README blob `3f5f300612adf988fbaa616c172e7f2f94e2a528`, raw SHA-256
  `dca6a2e6baf127d937636f41185efd79f1f6d08647767f012ba79288417a424f`, at `+2/−0` from its
  predecessor.
- Claude's review is open under `Review Card/Public README Step-4b-i Heartbeat.md` and
  `chats/Claude-Codex/Public README Step-4b-i Heartbeat/Public README Step-4b-i Heartbeat - Active.md`.
  This narrow review does not block the Step-4b-ii build.

## Review method and chat state

- The director's Review Card and convergence method supersedes the historical review-cycle text.
- Same-state explicit approval by both agents is required. Green tests, edits, downstream use,
  handoff and silence are not approval.
- The Step-4b-i subject chat is concluded. Do not append new work there.
- `chats/Claude-Codex-Human/Review Boundary and Convergence/Review Boundary and Convergence - Active.md`
  remains the active method-feedback chat. Its latest entry records the honest Round-3 closure,
  review-record numstat correction and no human-triage need.
- Use Transcript Order Monitoring only for an actual append-order/integrity recurrence. Both
  Session-138 appends preserved their complete prior byte prefixes, placed one unique Codex header
  after the boundary and remained additions-only.

## Public, reporting and scientific boundaries

- `agents/Codex/Session Summaries/HumanReport138.md` is the detailed record. The next regular
  progress report is Session 144.
- Stage 1 remains complete only as a development screen: no readable paired shape at five points /
  five seeds, no licensed trend statement, no capacity or threshold selected.
- Rung 2 remains complete only as scoped. Its fit/analyzer invocations are spent; all ten arms have
  zero healthy and structure F1, which is a development observation rather than a causal claim.
- The verified synthetic Slot-8 fixture proves the display mechanism, not a scientific result. Its
  real-role path still refuses before a scientific file opens.
- Project counters remain 278 rollouts, 67 fits, 67 checkpoints, and zero pilot/validation/test reads.
- Amendment A2, role separation, no-exploratory-recompute rules, the 67-checkpoint distribution /
  recovery issue, the non-blocking Claim Sheet director request and all unspent scientific gates
  remain in force.

## Append-only transcript discipline

Before any transcript append:

1. read the UTF-8 physical tail and record byte and line counts;
2. authenticate the complete prior bytes and programmatically verify a unique multi-line EOF anchor;
3. apply only against that exact verified tail;
4. verify the whole pre-write byte sequence is the new file prefix;
5. verify the new session header occurs exactly once after the old byte boundary; and
6. reread the physical tail and confirm the new message is last and the Git diff is additions-only.

If any assertion fails, stop and repair with a dated append-only correction before commit.
