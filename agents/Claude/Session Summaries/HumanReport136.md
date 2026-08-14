# Human Report — Claude Session 136

**Current date and time:** 2026-08-14 16:04 PDT (measured with the shell immediately before this report was created)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

**Outcome:** The Step-4a design closed at both approvals in Codex's Session 135, which licensed
the bounded Step-4b adapter-and-test build. I split that build in half and delivered the first
half — the connection-record contract implementing read-order steps 1, 2 and 3 — with 212 tests,
a two-pass mutation control, a Review Card and a new subject chat. **This session is also my
every-eighth progress-report session; the report covering S129–S136 is written.** Zero scientific
resource was spent: no role index, payload, checkpoint, config, split or result was opened, no
rollout stepped, no fit run, no figure rendered.

---

## 1. Session gates and context

`.agent-turn` named Claude, no `.agent-session.lock` existed, I created one and re-read the turn
file before starting work. `HEAD == 7818d96` (Codex Session 135), working tree clean.

I completed the context-first workflow: `Project Details.md` in full, `AgentPrompt.md`, my
continuity file, the superseding review protocol in `Playbooks/review-cycle.md`, both Review Cards,
every chat `Summary.md` that includes me, both active chats, and Codex's `HumanReport135.md` as my
general recent-work review. I raised no correction against it — its Round-2 review reproduced the
facts it relied on at source rather than accepting my handoff's description of them, and its three
recorded method refinements are the three I proposed.

The single most useful thing I learned from that reading is that **Step 4a is closed**: Codex
approved my exact bytes `032db166` in a delta-only Round 2, the subject chat is concluded with a
`Summary.md`, and the Review Card's terminal outcome is **Approved**. The seven-round pre-method
review and the one new-method round-trip that closed it are both now history.

## 2. The scoping decision I took, and why

Section 10 of the approved design names sub-step **4b** as one item: *the adapter and its tests are
built and reviewed.* Read literally, that item is a 21-row read order, fourteen refusal codes, a
dedicated coherent geometry fixture, an audit-hook open-set observer, and acceptance tests B1
through B8. Handing that to a reviewer as one candidate would produce precisely the artifact the
director's new protocol exists to prevent — a state too large to accept, reject or return inside
three round-trips.

I therefore split the build:

- **4b-i (this session):** read-order rows 1, 2 and 3 plus the section-4.2 expected-open-set
  derivation. Two new files, no tracked file modified.
- **4b-ii (next):** rows 4 through 21, the coherent geometry fixture, `X_GEOMETRY_UNSUPPORTED` at
  exit 15, the audit-hook observer, B2/B3/B4/B5/B8, the roles CLI wiring, and the additive
  `build_role_bundle` change including its stale `--config` docstring gloss.

**Sub-step 4b does not close when this card closes**, and I wrote that into the card in those
words. The boundary is the design's own: section 4.1 calls rows 1 and 2 "the first boundary" —
the record is authenticated before any scientific path is opened, and its own authentication needs
nothing but the record file itself — and row 3 completes it by binding every declared path to a
root without opening any of them. Everything in this candidate runs before the first scientific
byte is touched, which is why it can be built and reviewed whole while no role tree, config or
established result exists. The split moves no gate, precondition, invariant, exit code or
authorization; it is a review-scoping decision, and I asked Codex in the opening chat turn to rule
on it *before* reviewing the contents, since that is the cheapest round to spend on it.

## 3. What was built

**`Reproducibility Packet/scripts/utils/connection_record.py`** — 59,076 B / 1,468 LF / 0 CR, pure
ASCII, blob `b1a574650b1fcf673d04daf1df0b2d9c24f868f0`.

- **Step 1**, `authenticate_record_bytes`: reads the record's exact bytes and requires their
  SHA-256 to equal the digest the authorization named, refusing before anything is parsed.
- **Step 2**, `parse_connection_record`: strict-parses those bytes and validates the complete
  section-3.2 field table — sixteen frozen dataclasses, no optional field, no default, and no
  tolerated extra key at any level. That exact-key rule is also what enforces invariant W12: an
  approval-shaped field is refused wherever it is added, so the record cannot certify its own
  authorization.
- **Step 3**, `bind_root_domains`: takes the packet root as an **explicit parameter**, and that one
  root governs the schema, the config, all six source artifacts and the section-4.7 output parent
  together. This is the W8 seam Codex and I settled in the last card's round-trip 1, and it is what
  lets a test bind an isolated temporary tree while still exercising the production branch.
- `expected_open_set` derives the section-4.2 allowlist and opens nothing. It is the *expected*
  side of W3; the observed side is 4b-ii's audit-hook observer.

The reuse discipline is applied rather than described. Refusals raise
`utils.verification_scene.VerificationSceneError` with that module's own codes — this build adds no
error type and no code. The 20 schema-A manifest field names and the five that are integers are
derived from `utils.storage_contract.IdentityManifestRow` itself, not transcribed, so a schema-A
change moves the contract with it. The digest predicate is `storage_contract.re_full_sha256` and the
canonical rule is `protocol_p.canonical_json`.

**`Reproducibility Packet/tests/test_connection_record.py`** — 50,022 B / 1,245 LF / 0 CR, 212
tests, blob `6c89914502e0dff2f00e96a8b70b09d63349c30c`.

Three checks in it are worth naming because they hold facts against their owners rather than
restating them: `MANIFEST_ROW_FIELDS` is asserted **equal** to `IDENTITY_MANIFEST_FIELDS`;
`ROLE_NAMES` is asserted equal to the set derived from `schema.json`'s own `roles` keys minus
`identity_manifest` and `observations`; and W11's no-`torch`/no-`mujoco` claim is measured in a
**fresh interpreter** rather than read off a `sys.modules` that pytest has already filled, because
an import graph is a property of a checkout and not of a document.

## 4. Three decisions the design left to the build, taken with reasons

1. **Row 3's three refusal codes.** The read order lists `X_IDENTITY_MISMATCH`,
   `X_SPLIT_FORBIDDEN` and `X_PROVENANCE_UNRESOLVED` for row 3 without saying which failure takes
   which. I assigned by what the failure is *about*: a split under the wrong authority is a split
   refusal; a destination is a function of the authenticated authority, so a wrong `--output-dir`
   is a provenance disagreement rather than a digest complaint; everything else in row 3 is a claim
   that some named object is at some named place, which is identity. All three are stated in the
   chat as contestable now and expensive to move after 4b-ii is written against them.
2. **`FINAL` is not narrowed to one split.** It requires only that the split is not `dev`.
   Narrowing it to a named confirmatory split would make this contract the place that chose which
   split gets rendered, and that choice is a later, separately approved decision.
3. **Shape gates only, never range gates,** on the thresholds, the rung, the width and the distal
   tolerance. Their correctness is established at read-order step 5 by equality against each one's
   own named approved source. A plausibility band invented here would be an unapproved number
   entering the contract through the back door, and 4b is explicitly forbidden from choosing one.

I also had to interpret one thing the design states but its field table cannot express: section 3.2
says the menu must jointly contain a `structure`, an `actuator` and a `sensor` case, yet no
source-class field exists and a case's class is carried by its authenticated `labels` payload,
where `validate_bundle` already establishes it. So the record constrains *which* cases exist and
the check stays where the evidence is. Adding a `source_class` field would let an author assert a
class the payload contradicts — design property 2's own failure mode. The interpretation is in the
module's docstring, not only here.

## 5. The measurement that mattered, and it went against me

All 209 tests passed on the first run. That is a reason to check, not a reason to relax, so I ran
the packet's mandatory mutation-control shape: 44 mutants, `__pycache__` cleared and
`PYTHONDONTWRITEBYTECODE=1` in every child, no `-x`, anchors translated to the target's newline,
bad anchors reported separately from survivors, exact bytes restored in a `finally` and the digest
re-verified, and the whole sweep run twice requiring identical results. It ran entirely from a
scratch directory outside the repository.

**Pass 1 reported five survivors, and four of them were my own tests passing for the wrong
reason.**

The clearest is the trailing-newline rule. My test appended `\n` to a record and asserted that the
refusal message contained `"newline"`. But the canonical round-trip check one layer later *also*
refuses that record, and *its* sentence reads "no BOM, no trailing newline" — which contains the
word. Deleting the newline rule entirely left the suite green. The rooted-path branch, the
split-membership branch and the expected-digest-form branch had the same shape: each is subsumed by
a later check, and in three of the four the later check's message contained the phrase the
assertion was looking for.

This is the Session-71 lesson arriving from a new direction. That lesson says to assert a phrase
unique to one raise site. It is not sufficient: a *later* site can contain the phrase too, and no
reading of the test file finds that — only the sweep does. All four now assert a sentence that only
their own branch emits, and the parametrized path-token test names one expected sentence per
forbidden form so each overlapping branch is held separately.

The fifth survivor was different in kind. `_resolve_under`'s containment guard is unreachable from
a well-formed record, because the step-2 token rules already forbid every way of escaping a root. I
kept it — a token rule is an argument about spelling, while containment is the property that
matters — and held it with a direct unit test, because a guard no mutation can break is a guard
nothing checks.

**Pass 2 after the fixes: 42 of 42 real mutants caught, both negative controls surviving, identical
across both passes, target digest restored equal.** The two surviving negative controls are how I
know the instrument is measuring the tests rather than reporting everything as caught.

## 6. Suites and integrity

- Focused suite: **212 passed, 3.82 s**, and **212 again under `python -O`**.
- Packet-wide suite: **2,479 passed, 0 failed, 0 collection errors, 192.86 s** — the 2,267 baseline
  plus this file's 212.
- `git status --porcelain` shows the two new files and the closeout documents, and nothing else.
  `git diff --check` clean. The four closed Step-2 blobs, the ten Step-3 fixture blobs, both
  `.gitattributes`, both `.gitignore`, the packet README and the public README are untouched.
- Both new files are pure ASCII, LF-only in the blob, no BOM, final newline. **Disclosed in the
  card and the chat rather than left as a trap:** they are `*.py`, Codex's Session-128 ruling that
  no EOL pin is added for `*.py` stands, and `core.autocrlf` is `true` here — so a fresh Windows
  checkout renders both CRLF and its working-tree digest is a third number that is nobody's
  identity. The blob figures are the identity. This is limitation 129's shape, stated in advance.
- Every blob id in the card was resolved with `git cat-file -t` before the card governed anything,
  per the rule both agents adopted after Session 135's non-existent-baseline defect.

## 7. Two forward items recorded for the 4b-ii card

Neither is a finding against the closed design; both are decisions 4b-ii has to take, written down
now so that round does not rediscover them.

1. **The geometry producer's digest domain is unsettled, and it collides with a ruling.**
   `render_geometry.source` hashes `scripts/utils/cable_mechanics.py`, and read-order step 5 does
   that at runtime. Codex's Session-128 ruling declined an EOL pin for `*.py` on the stated premise
   that no packet runtime hashes those files. Step 5 ends that premise. Under the project's
   standing requirement (cc), a tracked text file's recorded digest belongs in the text domain, so
   4b-ii must either take that one field's digest with `canonical_text_sha256` or add an EOL pin
   for that one file. A raw digest with no pin is green here and red on a fresh Windows clone. I
   did not decide it this session because step 5 is not in this candidate.
2. **The source-class interpretation** in section 4 above, so that a later reader does not read
   section 3.2 as requiring a record field that does not exist.

## 8. Live-Run README heartbeat

Ran the check and **appended nothing**, which is the correct answer. No artifact finished — the
build half is handed to review, not approved — no phase closed, and Codex's Session-135 entry
already published the Step-4a closure on this same date. Codex's Session-127 ruling stands: the
lean public milestone is the *reviewed working* surface, not an unreviewed build. I re-read
`Playbooks/live-run-readme.md` in full before deciding, as in every session where the answer is no.

## 9. Files created or updated

- `Reproducibility Packet/scripts/utils/connection_record.py` — **new**, the contract.
- `Reproducibility Packet/tests/test_connection_record.py` — **new**, 212 tests.
- `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md` — **new**, the governing card.
- `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/Slot-8 Step-4b-i Connection-Record Contract - Active.md`
  — **new**, opened with the owner handoff for Round 1.
- `agents/Claude/Progress Reports/Progress Report Session 136.md` — **new**, the every-eighth
  report covering S129–S136.
- `agents/Claude/README.md` — the Progress Reports bullet, the Slot-8 design bullet (pruned from
  7,800 to 2,259 characters per this README's own Session-104 rule, with the review history left
  where it belongs), a new bullet for the 4b-i build, and both chat bullets.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.
- This report.

## 10. Boundaries

I opened no role index, role payload, checkpoint, estimator output, controller log, config or
split result; built no MuJoCo model; stepped no rollout; ran no fit, generation or render; read no
`dev`, `pilot`, `val` or `test` split; and wrote no config, connection record or production output.
Every path the new tests bind names a file that does not exist, under `tmp_path`. The only files
created outside the repository were the mutation harness and its transient mutants, all restored
and verified.

Counters remain **278 rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads**.

## 11. Next steps

1. Codex reviews the 4b-i candidate — Round 1, one numbered ledger, every reasonably discoverable
   finding, no stopping at the first blocker. It is also asked to rule on the 4b-i / 4b-ii split
   before reviewing contents.
2. If it holds, I open the 4b-ii card and build rows 4 through 21, the coherent geometry fixture,
   the audit-hook observer, B8's four authority/config drives under an isolated temporary packet
   root, and the additive `build_role_bundle` change. Sub-step 4b closes when both halves close.
3. Everything after that stays blocked on the config freeze, the capacity selection, the threshold
   calibration, the established result and the geometry-validation artifact.
