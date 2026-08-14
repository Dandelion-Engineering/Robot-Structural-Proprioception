# Human Report — Codex Session 136

**Current date and time:** 2026-08-14 16:19 PDT (measured with the shell immediately before this report was created)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

**Outcome:** Slot-8 Step 4b-i remains open after Round 1. I accept the connection-record/parser versus
source-read/bundle split, but do not approve module blob `b1a5746...` or test blob `6c89914...`.
Independent verification passed 2,479 packet tests, while exact-state probes reproduced five blocking
contract failures. Claude owns one complete bounded response; Step 4b-ii and every scientific action
remain unauthorized.

---

## 1. Session scope and controlling boundary

The `.agent-turn` gate named Codex, no `.agent-session.lock` existed, and the turn still named Codex
after I created the lock. I then completed the context-first workflow in `AgentPrompt.md`: Project
Details, Codex continuity and README, every chat summary involving Codex, every active Codex chat, the
newest Claude report and progress report, Claude's current Permanent Instruments, the applicable review,
packet, progress-report and live-run playbooks, and the active Review Card and candidate.

The repository began clean at `HEAD == origin/main == 0bf316e74337f8ac60d03af2c0cef6374bf516b9`
(`Claude Session 136`). Claude opened a first-half Step-4b review over exactly two previously committed
files:

- `Reproducibility Packet/scripts/utils/connection_record.py` — record loading, validation, typed
  construction and packet-root binding;
- `Reproducibility Packet/tests/test_connection_record.py` — the first-half contract suite.

I accept the proposed 4b-i / 4b-ii division. It follows the approved design's rows 1–3 versus rows 4–7,
can be reviewed without opening a scientific file, and explicitly does not allow first-half approval to
stand in for full Step-4b approval.

No production connection record, source read, bundle construction, adapter invocation, capacity or
threshold choice, final configuration, execution, or C1-versus-S statement was in scope.

## 2. Candidate authentication and baseline evidence

I independently reproduced both identities from Git objects:

- module Git blob `b1a574650b1fcf673d04daf1df0b2d9c24f868f0`, raw SHA-256
  `12bf71e5626f817f2ccc271882906af13afacc24cc7120a55aa96cffa3713046`, 59,076 bytes /
  1,468 LF / 0 CR;
- test Git blob `6c89914502e0dff2f00e96a8b70b09d63349c30c`, raw SHA-256
  `5b24716dd541d2f2ea7b6aa7585ad68b6470f9497818cbe7c2c5cec9238e5d25`, 50,022 bytes /
  1,245 LF / 0 CR.

The owner's positive baseline reproduced cleanly:

- 212 focused tests passed;
- the same 212 passed under `python -O` (with the expected pytest assertion-rewrite warning);
- the complete packet suite passed **2,479 tests**, with zero failures and zero collection errors, in
  196.34 seconds;
- both candidate modules compiled with `py_compile`; and
- `git diff --check` passed at the candidate boundary.

Those results establish a valuable regression baseline. They do not establish the unconstructed
negative states below.

## 3. Round-1 complete finding ledger

### Finding 1 — record location and expected-open-set binding

`load_connection_record` authenticates bytes but accepts them from an arbitrary filesystem location.
`bind_root_domains` receives no record path, so it cannot require the design's
`packet_root / record_relative_path(record_label)` identity, and `expected_open_set` omits the record
although design section 4.2 includes it.

The probe copied valid bytes to an arbitrary directory, loaded them successfully, then reported that the
record was absent from the expected set. This breaks the tracked-location guarantee, the sibling-tree
constraint and W3's exact whole-call open-set equality. The owner must bind the actual record path to the
injected root and authenticated label, carry it in `BoundPaths`, include it in the expected set, and test
both arbitrary and output-tree-nested copies.

### Finding 2 — shallow rather than deep immutability

The dataclasses use `frozen=True`, but their nested mappings remain ordinary dictionaries. The probe
replaced the parsed C1 plant role with the labels reference and changed
`record.document["record_label"]`; both mutations succeeded.

A later stage can therefore observe or bind a different allowlist than the authenticated bytes. Every
typed mapping and the retained document tree must become deeply immutable, with mutation-refusal tests
for each mapping-bearing layer.

### Finding 3 — non-total finite-number refusal

A canonical record with `analysis_window_s = 10**400` passes the recursive non-finite scan and reaches
`float(value)`, which raises raw `OverflowError: int too large to convert to float`. The public contract
requires the named Step-2 refusal instead of an implementation exception.

The conversion helper must translate overflow and equivalent conversion failures, and tests must drive
the huge-integer JSON form through each numeric helper class. The existing `1e9999` case is not
equivalent because the JSON parser has already converted that token to infinity.

### Finding 4 — portable path grammar and containment

An embedded NUL passes Step 2 and produces raw `ValueError` during `Path.resolve()`. On Windows,
alternate-stream syntax (`schema.json:stream`), the `CON` device alias and components ending in dot or
space also pass. These spellings do not represent one portable path identity.

The authority-specific output parent is additionally resolved directly rather than through the helper
that proves containment below the injected packet root. A packet-internal junction or symlink can
therefore redirect the accepted destination outside the root while preserving the lexical equality.
Step 2 needs a total portable-component grammar, Step 3 must translate resolution failures into the
named refusal, and every source or destination must prove containment under the same packet root.

### Finding 5 — unchecked `case_id` reaches a filename

The record accepts `case_id = "../escape"`. The already approved shared renderer uses the case id in
the PNG and JSON filenames. My integration probe drove `../escaped-case` through that writer and created
both files beside the requested bundle directory, with none inside it.

This is directly reachable from the new external record and violates the design's exclusive output
set. The record boundary needs a portable leaf-token rule, and the renderer/write boundary should retain
a defense-in-depth containment check. Tests must exercise separators, traversal, drive/ADS/device aliases
and assert every emitted file remains below the exclusive-created record-label root.

## 4. Decision and owner handoff

I copied the same complete numbered ledger into the governing Review Card and the active narrow subject
chat. I did not stop at the first defect and changed no candidate source or test. The card is now
**Open — Round 1 reviewer ledger complete; awaiting owner response**.

The Round-1 candidate is not approved. Claude must integrate or contest all five findings in one owner
response and mechanically identify both changed and byte-identical regions. Round 2 will be delta-only
under the governing review method. Step 4b-ii must not begin while Step 4b-i is open, and closing 4b-i
would still close no source-read or bundle-construction work.

The subject-chat append passed the physical-tail gate: the exact 9,473-byte / 150-LF prior file remained
the prefix at SHA-256 `844e5bf2...`; the new 14,188-byte file has 221 LF / 0 CR at SHA-256
`0c85333e...`; the Session-136 header occurs once after byte 9,474; Codex is physically last; and the
Git diff is additions-only. No Transcript Order Monitoring entry was warranted.

## 5. Progress report, public heartbeat and recent-work review

Session 136 is divisible by eight, so I created `agents/Codex/Progress Reports/Progress Report Session
136.md`. It covers Sessions 129–136: synthetic fixture closure, Step-4a convergence, the first full use
of the Review Card method, the current green-suite/blocked-contract distinction and the preserved
scientific boundaries.

I left root `README.md` unchanged. No artifact, phase or bounded review loop closed in this session;
the existing Session-135 entry already states that Step 4a is approved and only the synthetic Step-4b
build is open. Publishing another public heartbeat for a rejected first-half candidate would add motion
without a public milestone.

As a non-blocking recent-work observation, Claude's HumanReport136 file list omits
`agents/Claude/Permanent Instruments.md`, although Claude Session 136 changed that file by 25 lines.
This does not alter the formal Step-4b decision, but Claude should reconcile the session record on the
next general review.

## 6. Files created or updated

- `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md` — Round-1 evidence, five-item blocking
  ledger and awaiting-owner status.
- `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/Slot-8 Step-4b-i Connection-Record
  Contract - Active.md` — additions-only reviewer decision and bounded owner request.
- `agents/Codex/Progress Reports/Progress Report Session 136.md` — seventeenth regular director update.
- `agents/Codex/README.md`, `agents/Codex/Summary of Only Necessary Context.md`, and this report —
  index and next-session continuity.

No candidate implementation or test file and no root public README was edited.

## 7. Preserved boundaries and next steps

I opened no role index, role payload, checkpoint, estimator output, controller log or result; built no
MuJoCo model; stepped no rollout; ran no fit, generation or render against project data; read no `dev`,
`pilot`, `val` or `test` split; and wrote no config, connection record or production output. The one
renderer probe used an in-memory adversarial synthetic case and a temporary output tree solely to prove
the write-containment defect. Counters remain **278 rollouts, 67 fits, 67 checkpoints and zero
pilot/validation/test reads**.

Next:

1. Claude answers the complete ledger and returns exact candidate identities plus changed/unchanged
   region evidence.
2. Codex reviews only the delta, the five closures and introduced regressions.
3. If and only if both agents approve the same Step-4b-i state, Claude may open Step 4b-ii under its own
   Review Card and narrow chat.
4. A production record, scientific reads, capacity/threshold choices, final configuration and every run
   remain separately blocked.
