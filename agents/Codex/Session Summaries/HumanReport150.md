# Human Report — Codex Session 150

**Current date and time:** 2026-08-17 15:10 PDT (measured with the shell immediately before closeout writing)

**Agent:** Codex · **Branch:** `main` · **Phase:** 2 (Execution)

---

## Summary

This session completed the required general recent-work review of Claude Session 150's
fourth partial Step-4b-ii-b build. Claude accepted and correctly repaired both forward
blockers from Codex Session 149: the geometry source's `model_id` is now joined to the
authenticated config at row 5, and row 16 now accepts the faithful pre-advance
step-0/time-0 decision while refusing estimator steps outside the producer's `0..T-1`
control-step domain. Claude also added read-order row 19, which computes the connection's
provenance state and requires it to equal the record's claimed authority.

The two prior repairs reproduce and match their owning source contracts. Row 19's
production implementation also follows the approved design at the code level: it derives
`DEVELOPMENT_ONLY` from a `dev` split or any authenticated `dev-` trace, otherwise derives
`FINAL`, never derives `SYNTHETIC_FIXTURE`, and refuses a computed/claimed mismatch with
`X_PROVENANCE_UNRESOLVED`.

I found one definite forward blocker in the **evidence for row 19**, not a demonstrated
production-code failure. The `_reprovenanced` seam helper says it returns a connection in
which the four provenance identities have changed and the new W6 test says that rows 1–18
would accept the resulting state. It does not. The helper changes the validated config
hash and the record-side authority/split/audit assignment echoes, but leaves the other
authenticated copies from rows 4–6 stale. An independent probe checked eight equalities
that the earlier rows require and found only one still true:

```text
record_vs_authenticated_config=False
record_vs_established_split=False
record_vs_established_config=True
record_vs_generation_assignment=False
record_vs_independent_assignment=False
authenticated_config_vs_generation_config=False
authenticated_config_vs_independent_config=False
authenticated_config_vs_manifest_rows=False
passed=1/8
```

The test therefore drives `resolve_provenance` with an `AuthenticatedConnection` that
could not have crossed rows 4, 5 and 6, while its comments claim every digest and echo
still agrees. That does not disprove `resolve_provenance`; the real path establishes those
equalities before row 19. It does mean the current W6 test does not construct the coherent
post-row-18 state it claims to construct, and its passing result is not yet the required
evidence for invariant W6. Before stable handoff, Claude should make the seam update all
prior-row copies and assert their agreement, or provide another coherent post-row-18
construction that preserves W7's deliberate ban on manufacturing a production connection
record.

No packet implementation or test byte was edited by Codex. Claude still owns the unfinished
build. This is not a Review Card round, does not approve the current bytes, and does not
reopen the historically approved Step-4b-ii-a state.

## Exact state reviewed

Claude Session 150 is commit `31f028f1b41e8e79b73f93b1889e9b55053f8eb4`.
The two current owner-work files authenticate exactly:

- `Reproducibility Packet/scripts/utils/connection_adapter.py` — Git blob
  `88fb94fb8208e71c7ec5be9e78c27643da1e706d`, raw SHA-256
  `a6f528c4afb3a9eec998c8b6c2a13a5cc73749c048edc2c2c25c36536aa725c5`,
  145,409 bytes / 3,094 LF / 0 CR / ASCII;
- `Reproducibility Packet/tests/test_connection_adapter.py` — Git blob
  `678c1485ab21c6f030203c0ffcdc2316afa57a52`, raw SHA-256
  `6cec67985a460695b0b9ebfe3f72c54ce782c0e8b9d9e4e7b3ec9d9ffb9de932`,
  186,977 bytes / 4,540 LF / 0 CR / ASCII.

Git measures the Session-150 delta from Codex Session 149 as `+223/-51` in the module,
`+396/-36` in the test file and `+121/-0` in Claude's build plan. These are still
unapproved Step-4b-ii-b owner bytes.

## Review evidence

### The Session-149 repairs are discharged

The new row-5 join compares the `model_id` in the record's authenticated geometry source
against `values.plant.model_id` in the config object row 4 authenticated. It does not
reopen the config path. The fixture now carries the real model identifier as a literal,
and a separate test reads the copied config and pins that literal against its source. An
end-to-end record mutation to `not-the-config-model` now refuses with
`X_IDENTITY_MISMATCH`; deleting the config field also refuses through the same named path.

The corrected row-16 rule agrees with the live producer:

- `run_online_rollout` iterates `step_index in range(n_steps)`, reads the plant time and
  calls the policy before `plant.advance`;
- `EstimatorCommandPolicy` persists that exact `step_index` in each emitted output; and
- `CablePlant.advance` records the plant sample after integration.

The implementation therefore binds `step < T`, accepts the faithful step-0 decision at
time 0 even when the first playback sample is one control interval later, and keeps only
the design's upper display-containment bound on time. The focused tests drive both sides
of each boundary, including acceptance of `T-1`, refusal of `T`, rejection of a negative
time by the schema-D contract and deliberate non-pairing of each decision time to its
same-index plant sample.

### Row 19 production logic

The approved Step-4a design says authority constrains provenance rather than setting it.
Rows 3 and 4 already bind authority to split and config lifecycle; row 6 already joins the
manifest and audit config identities to the authenticated config. The one remaining
development marker is the dataset assignment identity. `resolve_provenance` reads the
authenticated config hash, both record-side audit assignment echoes and the split, carries
the named development traces in a read-only mapping, computes one of the two public states
and compares that state to `record.authority`.

That is a sensible implementation under the row-6 post-condition that the record's audit
echoes equal the authenticated audit documents. The new blocker is that the unit-test seam
does not preserve that post-condition while claiming that it does.

### Independent row-19 seam probe

I built Claude's isolated harness in a fresh temporary directory and called the exact
`_reprovenanced` helper used by the W6 and FINAL-accept tests. I then compared the changed
state at the joins the production path establishes before row 19:

- record config hash against the validated config hash;
- record split and config hash against the established-result document;
- both record audit assignment hashes against the authenticated audit documents;
- the validated config hash against both authenticated audit documents; and
- the validated config hash against every authenticated manifest row.

Seven of those eight equalities were false. The only surviving equality was the stale
record config hash against the stale established-result config hash. In particular, the
new W6 test's statement that its assignment edit leaves “every digest and every echo” in
agreement is false for the exact object the test passes to `resolve_provenance`.

The repair does not require an end-to-end FINAL artifact and must not weaken W7. A coherent
in-memory post-row-18 seam is enough, but it has to update all copies that rows 4–6 bind and
assert those joins before asking row 19 for a verdict. This will also keep later mutations
from silently weakening the seam again.

## Verification

All Python commands used the required project interpreter. The tests exercised only
tracked development code and synthetic temporary trees.

- focused adapter/authenticated-storage suite: **255 passed in 7.00 s**;
- the same suite under optimized Python: **255 passed in 6.69 s**, with the expected
  pytest optimized-assertion warning;
- packet-wide suite: **2,913 passed in 154.02 s**;
- `py_compile` passed for both edited files;
- both files are ASCII with LF endings, zero CR and a final newline; and
- `git diff --check` was clean before closeout edits.

The green aggregate suites coexist with the incoherent seam object because none of the
row-19 tests asserts the earlier-row equalities after `_reprovenanced` changes the state.

## Reasoning and decisions

- I treated this as the constitution's general recent-work review, not a formal review.
  Claude explicitly says the candidate is incomplete and has created no Review Card,
  subject chat or handoff.
- I accepted the two Session-149 repairs only after re-reading their production sources
  and reproducing the exact file identities and focused tests.
- I did not convert the row-19 seam defect into a production-code verdict. The real
  production path establishes the missing equalities, so the evidence supports “test
  construction is incoherent,” not “provenance resolution is wrong.”
- I did not patch Claude-owned files. The correction belongs in the still-open owner build
  before the complete mutation sweep and stable handoff.
- The only active Codex-participant chat remains Transcript Order Monitoring. Its physical
  tail requires no reply; a clean check and an unrelated technical finding are not reasons
  to post there.
- The Live-Run README heartbeat was checked and left unchanged. A partial internal build
  with one pre-handoff evidence correction is not a public milestone.
- Session 150 is not a regular progress-report trigger. The next regular Codex progress
  report remains Session 152.

## Scientific and authorization boundary

Project counters remain **278 rollouts, 67 fits, 67 checkpoints and zero
pilot/validation/test reads**. No production connection record, real role index/payload,
checkpoint content, estimator result, controller log, final configuration or scientific
result was opened. No model was built, rollout stepped, fit run, capacity selected,
threshold selected or C1-versus-S claim made.

Slot-8 Steps 1–3, Step 4a, Step 4b-i and Step 4b-ii-a remain closed / both approved at
their recorded historical bytes. Step 4b-ii-b remains Claude-owned, incomplete and
unapproved. Rows 20–21, the audit-hook observer, bundle/output/CLI wiring, the additive
`build_role_bundle` edit and the two-pass mutation sweep remain unfinished. Full Step 4b,
production adapter execution, Steps 4c–4f and every later scientific gate remain closed.

## Files created or updated by Codex

- `agents/Codex/Session Summaries/HumanReport150.md` — this detailed session record.
- `agents/Codex/README.md` — added Session 150 and the current partial-build boundary.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the
  next Codex session.

No packet code, packet test, Review Card, chat transcript, root README or scientific
artifact was changed by Codex.

## Next steps

1. Claude should repair the row-19 seam so the W6 mismatch and FINAL accept-side tests
   begin from an internally coherent state satisfying the joins rows 4–6 establish, and
   should assert those joins inside the seam test.
2. Claude should then finish rows 20–21, the full-call observer, bundle/output/CLI wiring,
   the additive `build_role_bundle` edit and the two-pass mutation sweep.
3. Only after one complete stable candidate exists should Claude create the
   Step-4b-ii-b Review Card and matching subject chat and explicitly approve the exact
   handed-off state.
4. The next Codex session should run the full Round-1 Review Card review only after that
   handoff; otherwise it should continue the required general recent-work review without
   taking over Claude's build or opening downstream work.
