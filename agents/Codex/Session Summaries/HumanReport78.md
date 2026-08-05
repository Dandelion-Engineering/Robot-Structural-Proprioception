# Codex — Human Report, Session 78

**Date and time:** 2026-08-05 10:13 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.

---

## Summary

This session reviewed Claude Session 78's returned Gate-4 attribution-rung repair and its
new development-only fitting contract. The attribution two-file loop is now closed at a
state both agents explicitly approve. The dev-fit contract was not approved as submitted:
four synthetic, zero-training probes reproduced contract states the prose claimed to
refuse but the implementation accepted or described incorrectly. I corrected only that
module and its tests, explicitly approved the replacement bytes, and returned them for
Claude's genuine owner re-review.

No model was trained. No checkpoint or result was written. No observation payload was
opened, no data was generated, and no rollout was spent. Pilot, validation, test, final
configuration, and confirmatory work remain blocked.

## 1. Attribution-rung loop closed

Claude accepted the Session-77 finding that PyTorch's strict state-dictionary load may
partially mutate a live model before raising, but found a second defect in my repair. My
candidate-copy implementation installed the validated network by rebinding `self.net`.
An optimizer created before checkpoint resume would therefore keep stepping an orphaned
module while the estimator answered from a different one.

Claude's returned implementation preserves both required properties: it validates the
incoming state on a deep copy, then copies the validated tensors into the existing live
network object. The optimizer consequence test and the success/refusal identity tests all
pass. I re-opened the exact returned state and explicitly approved the same bytes Claude
approved:

```text
Reproducibility Packet/scripts/utils/attribution_net.py
  c4fa3c63e7439236e09f4e5eeb08b7c76a6087ab
Reproducibility Packet/tests/test_attribution_net.py
  5a401ca14be170d0002c508111b7ce32a5291bb0
```

That two-file review cycle is closed.

## 2. Submitted dev-fit contract review

Claude's new `utils/dev_fit_contract.py` correctly establishes the intended foundation:

- only the already-delivered development partition may be selected;
- the matched plan is C1 and S crossed with training seeds 0–4;
- every checkpoint provenance record carries the exact development-only authority, data
  identity, suite, seed, source-code identity, and checkpoint identity;
- the approved Gate-3 assignment digest is required exactly; and
- the module imports neither MuJoCo nor PyTorch.

I approved the four design choices Claude flagged. The authority remains a local literal
because importing an entry-point script into `utils` is the wrong dependency direction and
moving it would edit a closed executable; tests pin the literal against both the script
and frozen protocol. The configuration identity must retain its `dev-` prefix. The
assignment digest is equality-bound rather than shape-checked. The persisted data root is
a path-free bare name paired with a manifest digest, not a local machine path.

I also agreed that the trainer and evaluation driver must share
`deterministic_conv_precision()` for forward and backward computation, that binary
checkpoints use raw digests, and that tracked source identities use the canonical-text
digest domain.

## 3. Four reproduced defects and reviewer edits

Direct probes against Claude's exact submitted blobs reproduced four issues:

1. `require_complete_matched_plan()` collapsed the input to a set, so the exact ten-fit
   plan plus a duplicate `(C1, 0)` was accepted. The reviewer state refuses duplicate
   suite/seed pairs before checking missing or unexpected fits.
2. `require_dev_only()` accepted an empty caller-built batch and accepted a `dev/C0`
   batch. It now refuses empty input, refuses suites outside C1/S, and accepts an optional
   expected suite so an S fit cannot consume C1 rows or vice versa.
3. A selected `dev/S` row beside a withheld `dev/C0` row was disclosed as one withheld
   "non-dev" row. The census now reports non-dev rows and unmatched-suite dev rows
   separately.
4. A data-root name containing a newline passed the bare-name predicate and could turn the
   promised one-line provenance string into multiple lines. Bare names and code labels now
   refuse ASCII control characters without echoing the rejected value.

The original submitted contract state is blocked:

```text
scripts/utils/dev_fit_contract.py   73e5e743393ee5d0b0a2e548da6070bfceb1599e
tests/test_dev_fit_contract.py      3959ff28cad18efd8e55c3e8786951d1cea78e51
```

I explicitly approve and returned this reviewer-edited state:

```text
scripts/utils/dev_fit_contract.py   6541cebcbd78d10918d5d6ab58b5f5501340ebf9
tests/test_dev_fit_contract.py      9df7d7f79a7120e42ab84a81ba3bd76b1494ec32
```

That loop remains open until Claude explicitly approves these same bytes or edits and
hands back another state.

## 4. Documentation review

The corrected pre-freeze training sequence and packet boundary survive review unchanged:

```text
Reproducibility Packet/scripts/utils/estimator.py   b2abf463d9a4b2678f182568f50417774a6191e7
Reproducibility Packet/scripts/utils/__init__.py    04647db4f61b18aac33e088543c6c49d54feb584
Reproducibility Packet/README.md                    ebef72fef5e423779901ba8a47529ae64d6a4433
```

The root public README heartbeat was checked and deliberately left unchanged. The
attribution model is still untrained, the trainer does not exist, and the dev-fit contract
loop remains open; this is review progress, not a new public result or completed milestone.

## 5. Verification

```text
pre-edit direct probes              duplicate plan / empty batch / dev-C0 batch /
                                    cross-suite batch / newline name reproduced
post-edit direct probes             all five refused with DevFitContractError
focused suites, normal              126 passed (68 attribution + 58 contract)
focused suites, python -O           126 passed (expected pytest warning only)
full packet suite                   1,432 passed in 130.27 s
compileall                          clean
delivered manifest, read-only       944 total; 304 dev; C1 152 / S 152;
                                    640 withheld; one dev-712... config identity
payload files read                  0
fits / checkpoints / generation    0 / 0 / 0
config/config.json                  absent
physical rollouts                   0
```

The delivered-manifest read used only `manifest.csv`. Its raw SHA-256 was
`55ea5f0e74ddd24b05eafc51a2b9fc424eda99eac1901534946f42b6012ebe12`; no `.npz` payload
was opened.

## 6. Transcript integrity

Before the append, the authoritative Phase-2 transcript was 1,337,850 bytes / 20,937
lines with SHA-256
`70518b713090a9e595ec5b78089acd558f60a527fbe24f453cb6feb10898c43f`. The complete
final Claude block used by the patch occurred exactly once at the physical tail.

Post-write checks passed:

- the complete 1,337,850-byte prefix remains byte-identical at the same SHA-256;
- the Session-78 Codex header occurs exactly once after the recorded boundary;
- Codex is physically last;
- the transcript is now 1,343,389 bytes / 21,045 lines; and
- the transcript diff is additions-only at `+108/-0`.

No transcript repair or monitoring-chat report was needed.

## Files created or updated

- `Reproducibility Packet/scripts/utils/dev_fit_contract.py` — duplicate-plan,
  point-of-consumption, disclosure, and single-line provenance corrections
- `Reproducibility Packet/tests/test_dev_fit_contract.py` — regressions for all four
  corrected boundaries
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — exact-state decision, design rulings, verification, and owner handback
- `agents/Codex/Session Summaries/HumanReport78.md` — this report
- `agents/Codex/README.md` — workspace index and current review gate
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten resume state

The `.gitignore` already covers the session lock, virtual environment, local dataset,
caches, scratch outputs, and model/checkpoint formats. No ignore update was needed.

## Next steps

1. Claude must genuinely re-review and either explicitly approve `6541cebc...` /
   `9df7d7f7...` or edit and return a replacement.
2. After that loop closes, Claude may build the trainer against the jointly approved
   attribution implementation and dev-fit contract, then hand its exact executable/test
   state back for review.
3. No development fit may run before the trainer review closes. Any later fit is limited
   to the already-delivered 304-row `dev` partition and the ten predeclared C1/S seed arms.
4. Pilot, validation, test, final `config.json`, additional payload measurement, new data
   generation, and all confirmatory work remain blocked.
5. The next regular Codex progress report remains Session 80.
