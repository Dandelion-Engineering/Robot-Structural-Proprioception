# Human Report — Codex Session 137

**Current date and time:** 2026-08-14 18:16 PDT (measured with the shell immediately before writing this report)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

**Outcome:** Round 2 of the Slot-8 Step-4b-i review is complete. I accepted Claude's proposed
renderer scope expansion and verified that Findings 1–3 close and most of Finding 4 closes, but I
did not approve the three candidate blobs. The repaired filename/write-set contract still accepts
an unbounded and non-injective portable namespace: one valid case id overwrites the canonical
bundle JSON, case-only variants overwrite one another on Windows, and a long valid id creates a
partial publication followed by a raw `OSError`. Claude owns one bounded integration response; the
next Codex review is Round 3 and the last review under this card. No scientific or downstream gate
moved.

---

## 1. Session purpose and governing boundary

Claude Session 137 returned the complete Round-1 ledger in one owner response. All five findings
were accepted without contest. The response changed the two Step-4b-i files and proposed one
explicit scope expansion into the previously approved shared renderer because Finding 5 asked for
two layers: validation at the record boundary and containment at the write boundary.

The governing card is `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md`. Round 2 was
delta-only: authenticate the new states, rule on scope first, verify each recorded disposition,
check regressions introduced by the response, and leave unchanged Round-1 material alone absent
contrary evidence. I did not edit any candidate source or test.

## 2. Scope-expansion ruling

I accepted `Reproducibility Packet/scripts/render_verification_scene.py` as part of this card.
Finding 5 explicitly named the write boundary, so approving only the record-side half would have
left a blocking finding only partly answered, while silently moving the writer half to 4b-ii would
have made the card's disposition misleading. The added renderer state receives a real delta review
and inherits no approval from its earlier closed Step-2 blob.

This exposed a useful process rule. `Playbooks/review-cycle.md` and `Review Card/README.md` now state
that an owner may propose an out-of-card repair as an authenticated, bounded scope expansion with
the prior state named and revert/deferral offered. The reviewer rules scope before content. An
accepted expansion joins the current candidate without inheriting approval; a rejected or overbroad
one returns to its prior state and moves to a new card. The round and late-blocker counters do not
reset. I recorded the ruling in the director-visible method chat. No human triage is needed yet.

## 3. Candidate authentication and verification

I authenticated the three current Git objects independently:

- `connection_record.py`: blob `474f4abc4a646304261f47d536a33e05b7feef65`, raw SHA-256
  `ead247379da4b0167807eb7d14c3c8f39f48cbb4ac54fbb9c3e0f0908e01fbb3`, 73,745 bytes /
  1,763 LF / 0 CR.
- `test_connection_record.py`: blob `73d5d59e6cb4787ee4976c2e11e8acd03ebb55f5`, raw SHA-256
  `fc0b043afd6cf47610402cd0b2410f2f5a148936956b5cffc169da77a2f2d6c9`, 80,673 bytes /
  1,948 LF / 0 CR.
- `render_verification_scene.py`: blob `d15705e4f0db3816c2cc3f02ad1f21366b0249f1`, raw SHA-256
  `5ba9222939b350d7e2a6c09a17b6c8f3c6572979d76b45f975279477b7536564`, 33,167 bytes /
  847 LF / 0 CR.

Verification passed:

- focused `test_connection_record.py`: 311 tests;
- the same focused suite under `python -O`: 311 tests, with the expected Pytest warning;
- packet-wide suite: 2,578 passed, 0 failed, 0 collection errors in 211.45 seconds;
- `py_compile` over the module, renderer and focused test file;
- `git diff --check`.

These green suites remain necessary but not sufficient. The blocking states below are accepted by
the candidate and are absent from the suite.

## 4. Disposition of the Round-1 ledger

Findings 1, 2 and 3 close on the delta:

1. The record is bound to its one tracked location beneath the injected packet root, carried in
   `BoundPaths`, and included in the expected open set. Arbitrary, output-tree, wrong-label and
   wrong-filename copies are exercised under both authorities.
2. The authenticated record and every typed mapping are deeply immutable. Mapping proxies wrap
   private copies, JSON arrays become tuples, and the three bound-path maps are immutable too.
3. Huge integer literals are translated to `X_CONNECTION_UNAUTHORIZED` rather than escaping as raw
   `OverflowError`; the six float-shaped positions are exercised.

Finding 4's Windows alias/device/trailing-dot grammar, named resolution failures and root
containment repairs reproduce, including the no-privilege junction tests. Its portable-component
claim is still incomplete because the grammar has no component-length bound.

Finding 5's traversal boundary and path-containment check reproduce, but the write-set repair is
not injective and therefore does not prove the complete set it claims to validate.

## 5. Remaining blocker

The remaining blocker is one incomplete disposition spanning Findings 4 and 5, not a new unrelated
`LATE-BLOCKER`.

`_require_portable_segment` accepts arbitrarily long ASCII strings, and `_require_leaf_token`
therefore accepts a 251-character `case_id`. Appending `.json` produces a 256-character Windows
component. The new `_contained_output_paths` accepts the whole set; `render_bundle` writes the
canonical bundle JSON, its digest and the case PNG, then raises raw `OSError` while opening the scene
JSON. The promised pre-write validation becomes a partial publication.

The same helper stores `name -> path` without first proving the portable namespace is one-to-one:

- `case_id = "verification_bundle"` is accepted and causes the scene JSON to overwrite
  `verification_bundle.json`. The file no longer equals the canonical bundle document and the
  returned `bundle_sha256` no longer hashes it.
- `Case-A` and `case-a` are accepted as distinct ids. On this Windows host the returned manifest
  reports four cases, while only eight files exist instead of ten because those two JSON/PNG pairs
  collapse case-insensitively.

The owner response must bound component lengths at the record boundary; require every derived case
filename to be disjoint from the fixed bundle filenames and from every other derived filename under
an explicit portable case-insensitive comparison; repeat the length/uniqueness gate inside
`_contained_output_paths` before the first write; and add the three exact probes. I recorded this
verbatim in the card and subject chat and explicitly withheld approval of all three blobs.

## 6. Cross-review and public heartbeat

I read Claude's HumanReport137 and the files it points to. Its account of the five Round-1 repairs,
suite evidence, method question, earlier HumanReport136 omission and preserved resource boundaries
is accurate. The new blocker is in the candidate behavior, not in Claude's report.

I checked the root Live-Run README heartbeat and intentionally left it unchanged. No artifact or
phase closed; a Round-2 revisions-required return inside Step-4b-i is not a public milestone, and
the current banner already preserves the correct boundary.

Both active chat appends passed the hard physical-prefix gate. The Step-4b-i transcript preserved
its exact 25,332-byte prefix at SHA-256
`e6c7d3174f14c6cae759a7f9cf044b5cb0b1cfe29454f13e5a960170cc0bce14`, added one unique
post-boundary Codex header and remained additions-only at +50/−0. The method chat preserved its
exact 15,831-byte prefix at SHA-256
`cee838ccb839aafc2b9486f7e7d74ef6762b44e1a04ac25a2acfe3f1e238e9f4`, added one unique
post-boundary header and remained additions-only at +27/−0. Codex is physically last in both. No
Transcript Order Monitoring entry was needed.

## 7. Files created or updated

- `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md` — Round-2 scope ruling, evidence,
  disposition and remaining blocker.
- `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/Slot-8 Step-4b-i
  Connection-Record Contract - Active.md` — append-only Round-2 return.
- `Playbooks/review-cycle.md` — accepted scope-expansion rule.
- `Review Card/README.md` — matching Review Card operating rule.
- `chats/Claude-Codex-Human/Review Boundary and Convergence/Review Boundary and Convergence -
  Active.md` — director-visible method ruling and current no-triage state.
- `agents/Codex/Session Summaries/HumanReport137.md` — this report.
- `agents/Codex/README.md` — Session-137 index and current review state.
- `agents/Codex/Summary of Only Necessary Context.md` — rewritten resume state for Session 138.

No candidate source/test file and no public README byte was edited by Codex.

## 8. Preserved boundaries and next step

Project counters remain 278 rollouts, 67 fits and 67 checkpoints, with zero
pilot/validation/test reads. This session opened no role index, role payload, checkpoint,
estimator output, controller log, configuration or split result; built no MuJoCo model; stepped no
rollout; ran no fit; and wrote no production artifact. The three adversarial renderer probes used
temporary directories only.

Claude owns one bounded integration response. The following Codex delta review is Round 3 and the
last review under this card; the limit never forces approval. Step 4b-ii has not started. No
production connection record, real-role read, Steps 4c–4f work, capacity or threshold selection,
final configuration, adapter run, or C1-versus-S statement is authorized.
