# Summary of Only Necessary Context — Codex

Last completely rewritten after Codex Session 137 on 2026-08-14.

## Resume here

- Branch: `main`.
- Slot-8 Steps 1–3 and Step 4a are closed / both approved. Step-4a exact design blob is
  `032db1666efbe00adec5696de70424d531ba33a2`, raw SHA-256
  `f761a673ff8fcca6c58fe530a3faaed57630315a87a5e241d8ca9675a13c4ffc`.
- Step 4b-i is **OPEN — Round-2 revisions required; awaiting Claude's one bounded owner response**.
  Codex does not approve any current candidate blob. The next Codex review is Round 3 and the last
  review under this card; the round limit never forces approval.
- Governing card: `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md`.
- Active subject chat: `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/Slot-8
  Step-4b-i Connection-Record Contract - Active.md`.
- The proposed renderer scope expansion is accepted. It is part of this card because Finding 5
  explicitly required a write-boundary guard, but it inherits no approval from its former closed
  Step-2 state.
- Step 4b-ii has not started and is not authorized while 4b-i is open. Even 4b-i closure would
  authorize only a new, separately reviewed 4b-ii build; it would not close full Step 4b.
- No production connection record, real role/index/payload/checkpoint/result read, Step 4c–4f work,
  capacity or threshold choice, final configuration, adapter run, or C1-versus-S claim is authorized.
- The next regular Codex progress report is Session 144.

## Exact Round-2 candidate — all three unapproved

- `Reproducibility Packet/scripts/utils/connection_record.py`: Git blob
  `474f4abc4a646304261f47d536a33e05b7feef65`, raw SHA-256
  `ead247379da4b0167807eb7d14c3c8f39f48cbb4ac54fbb9c3e0f0908e01fbb3`, 73,745 bytes /
  1,763 LF / 0 CR.
- `Reproducibility Packet/tests/test_connection_record.py`: Git blob
  `73d5d59e6cb4787ee4976c2e11e8acd03ebb55f5`, raw SHA-256
  `fc0b043afd6cf47610402cd0b2410f2f5a148936956b5cffc169da77a2f2d6c9`, 80,673 bytes /
  1,948 LF / 0 CR.
- `Reproducibility Packet/scripts/render_verification_scene.py`: Git blob
  `d15705e4f0db3816c2cc3f02ad1f21366b0249f1`, raw SHA-256
  `5ba9222939b350d7e2a6c09a17b6c8f3c6572979d76b45f975279477b7536564`, 33,167 bytes /
  847 LF / 0 CR. Its earlier approved Step-2 base was
  `0ae5b19d4a5957d3be662b1aa337c8e3bb9353a5`.
- Independent verification passed 311 focused, 311 under `python -O`, 2,578 packet-wide,
  `py_compile` and `git diff --check`.

## Round-2 disposition

- Finding 1 closes: the authenticated record is bound to its one tracked packet-relative location,
  carried by `BoundPaths.record_path`, and included in the exact expected open set.
- Finding 2 closes: the parsed document and every typed/bound mapping are immutable views over
  private copies; arrays are tuples.
- Finding 3 closes: huge JSON integers at float-shaped positions translate to the named refusal.
- Finding 4's Windows alias/device/trailing-dot grammar, named resolution failures and containment
  checks reproduce. Its portable-component claim remains incomplete because length is unbounded.
- Finding 5's traversal refusal and writer containment reproduce, but the output namespace remains
  non-injective and can partially publish before a raw failure.

## The one remaining blocking disposition

Findings 4 and 5 are not fully closed because the accepted output namespace is neither
length-bounded nor injective. This is not a new unrelated `LATE-BLOCKER`; it is a direct gap in the
recorded path/filename repair.

Three exact current-state probes:

1. `case_id = "verification_bundle"` is accepted. `render_bundle` overwrites
   `verification_bundle.json` with the scene JSON. The file no longer equals the canonical bundle
   document and the returned bundle digest does not hash it.
2. `Case-A` and `case-a` are accepted as distinct ids. On Windows the renderer reports four cases
   but writes only eight files instead of ten because the two JSON/PNG pairs collapse
   case-insensitively.
3. A 251-character ASCII case id is accepted. Its `.json` filename is 256 characters on Windows.
   The complete-path helper accepts it; the renderer writes the two fixed bundle files plus the PNG,
   then raises raw `OSError` while opening the scene JSON, leaving a partial publication.

Claude's bounded response must:

- impose portable component lengths at the record boundary;
- require derived case filenames to be disjoint from fixed bundle filenames and from one another
  under an explicit portable case-insensitive comparison;
- enforce the same length/uniqueness properties in `_contained_output_paths` before the first write;
  and
- add all three exact probes.

Do not introduce a new item serially in Round 3 unless the superseding late-blocker/triage rule is
actually satisfied. Review only this disposition, its tests and regressions caused by the delta.

## Review method and chat state

- The director's Review Card and convergence method supersedes the historical review-cycle text.
- An out-of-card repair is proposed explicitly, redundantly authenticated, bounded, tied to its
  prior state and offered with revert/deferral. The reviewer rules scope before content. If accepted,
  the artifact joins the candidate without inheriting prior approval; if rejected, it returns to its
  prior state and moves to a new card. Round and late-blocker counters do not reset.
- Authenticate every candidate with full Git blob, raw SHA-256, byte count and EOL figures, and
  verify the Git object resolves.
- Same-state explicit approval by both agents is required. Green tests, edits, downstream use,
  handoff and silence are not approval.
- Use only the active Step-4b-i subject chat for this contract. The Step-4a and broad Phase-2 chats
  are concluded.
- The director-visible Review Boundary and Convergence chat carries method feedback only. The scope
  rule is adopted and no human triage is currently open.
- Use Transcript Order Monitoring only for an actual append-order/integrity recurrence. Both Session-
  137 appends preserved their exact byte prefixes, placed unique headers after the boundaries and
  remained additions-only.

## Public, reporting and scientific boundaries

- `agents/Codex/Session Summaries/HumanReport137.md` is the detailed record. The next regular progress
  report is Session 144.
- Root `README.md` was intentionally unchanged: no bounded artifact or phase closed.
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
