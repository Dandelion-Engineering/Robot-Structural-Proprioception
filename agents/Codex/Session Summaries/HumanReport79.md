# Codex — Human Report, Session 79

**Date and time:** 2026-08-05 14:12 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.

---

## Summary

This session genuinely re-reviewed Claude's Session-79 development-only fitting-contract
handback. I accept all six of Claude's repairs: the single-line bare-name post-condition,
the strict matched-plan entry shapes, and four new tests that make previously untested
guards fail when removed.

I did **not** approve Claude's exact returned blobs. Direct synthetic probes found two
additional contract failures:

1. all four documented exact digest fields accepted a terminal line feed because the
   regular expressions used `$` through `Pattern.match`; and
2. malformed provenance types escaped as `TypeError` or `AttributeError` instead of the
   module's own `DevFitContractError`.

I corrected both defects, added ten regression cases, and explicitly approved the new
exact state:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py
  872c6b125d823db584c06749a23dda2a46c71377
Reproducibility Packet/tests/test_dev_fit_contract.py
  3125a618dfdb435e67a32500073d76608855147d
```

The review loop remains **open** because Claude must now re-open and genuinely owner-review
these reviewer-edited bytes. I deliberately did not build or run the trainer. No model was
fit, no checkpoint/result/dataset was written, no real dataset or delivered manifest was
read, no physical rollout was spent, and the final configuration remains absent.

## Review input and accepted work

Claude handed back:

```text
dev_fit_contract.py       2448ad4df5107e4442687c17228510360a11024f
test_dev_fit_contract.py  2aa5f762ac52c535218d8527a2086f0e9d78bfa8
```

I re-opened both exact files rather than treating the handoff or Claude's approval as my
approval. The focused test file executed the all-codepoint line-boundary derivation twice
and the full packet suite executed it a third time. The returned source correctly:

- refuses all interpreter-recognized line boundaries in bare names while retaining the
  independently live ASCII-control rule;
- rejects bool and float training seeds before Python set equality can alias them to the
  declared integer seeds;
- turns malformed and unhashable completed-plan entries into contract refusals before set
  arithmetic;
- drives the expected-suite, requested-suite, DEL, and exact-authority guards with states
  that fail if those guards are removed; and
- preserves my two broad suite-message assertions while adding unique-phrase assertions,
  which resolves rather than buries the test-specificity concern.

I accept all of those changes and recorded that acceptance explicitly in the Phase-2 chat.

## Finding 1 — exact digest predicates accepted an extra line

The module compiled `^[0-9a-f]{64}$` and `^dev-[0-9a-f]{64}$`, then called
`Pattern.match`. Python's `$` anchor may match immediately before a final newline. Against
Claude's approved blob, I directly constructed four otherwise-valid provenance records and
measured:

```text
manifest_sha256     64 lowercase hex + LF    ACCEPTED
config_hash         dev- + 64 hex + LF       ACCEPTED
checkpoint_sha256   64 lowercase hex + LF    ACCEPTED
code-identity hash  64 lowercase hex + LF    ACCEPTED
```

Those values are not the exact 64-character identities promised by the error messages and
can occupy two physical lines. I removed the redundant anchors and now use
`Pattern.fullmatch` at every digest site. The four probes now receive
`DevFitContractError`.

## Finding 2 — malformed audit records leaked foreign exceptions

`DevFitProvenance.validate()` is the audit boundary, and this module defines
`DevFitContractError` so a fitting-contract violation fails in its own domain under both
ordinary and optimized Python. Four synthetic malformed records instead escaped below that
boundary:

```text
manifest_sha256=None     TypeError from regex
checkpoint_sha256=None   TypeError from regex
code_identity=list       AttributeError from .items()
row_disclosure=None      AttributeError from .strip()
```

I added string checks to the manifest, configuration, checkpoint, and code-identity digest
predicates; required `code_identity` to be a non-empty mapping before iteration; and
required `row_disclosure` to be a non-empty string before stripping it. Six malformed-type
cases now all produce `DevFitContractError`.

## Verification

```text
pre-edit direct probes        4 terminal-LF digests accepted; 4 foreign exceptions
post-edit direct probes       8/8 contract refusals
focused contract tests        77 passed in 1.89 s
focused under python -O       77 passed in 1.86 s; expected pytest warning only
full packet test suite        1,451 passed in 130.87 s
compileall                    clean
diff against Claude's state   source +11/-8; tests +34/-0
diff hygiene                  git diff --check clean
real-data touches             none; tests used only synthetic temporary manifests
fits / checkpoints            0 / 0
generation / rollouts         0 / 0
final config.json             absent
```

The transcript append used the complete programmatically verified unique physical EOF
anchor. Before the write it had 1,353,059 bytes, 21,216 lines, and SHA-256
`f5eb33122cfe2c71a81b3fd0959958d18934abfedb1224dcaebf93448c016bb7`. Afterward:

- the full prior byte prefix is identical under that digest;
- the new Session-79 header occurs exactly once, after the recorded boundary;
- Codex is physically last;
- the file has 1,357,886 bytes and 21,316 lines; and
- Git reports `+100/-0` for the transcript.

No repair was needed.

## Decisions and boundaries

- Claude's Session-79 fixes are accepted, but blobs `2448ad4d` / `2aa5f762` are
  superseded and not approved.
- I explicitly approve only `872c6b12...` / `3125a618...`; Claude's owner re-review is
  required to close this exact-state loop.
- Trainer construction remains sequenced after this contract loop. Its own
  checkpoint/result writer must then receive a separate executable review before any fit.
- The already-delivered dev partition is conceptually authorized for the later bounded
  ten-arm C1/S fit, but this session consumed none of it.
- Pilot, validation, test, new data generation, dataset supersession, payload measurement,
  final config materialization, and confirmatory work remain blocked.
- The public Live-Run README was deliberately left unchanged: an open contract review is
  not a finished milestone, and the model remains untrained.

## Files created or updated

- `Reproducibility Packet/scripts/utils/dev_fit_contract.py` — exact digest matching and
  total provenance-type refusal.
- `Reproducibility Packet/tests/test_dev_fit_contract.py` — four terminal-LF digest cases
  and six malformed-type cases.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — append-only exact-state review, approval, and owner handback.
- `agents/Codex/Session Summaries/HumanReport79.md` — this report.
- `agents/Codex/README.md` — workspace index refreshed for Session 79.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten resume state.

## Next steps

1. Claude re-opens and genuinely reviews blobs `872c6b12...` / `3125a618...`.
2. If Claude approves them unchanged, the development-fit contract loop closes.
3. Claude then builds the bounded trainer/checkpoint/result writer; both agents review the
   exact executable state before any fit.
4. Only after that later review closes may the ten predeclared dev-only C1/S fits run.
5. Codex Session 80 writes the next regular progress report in addition to its normal work.

The central research measurement has still not run. This session improved the integrity of
the development-only training boundary; it did not produce evidence about the hypothesis.
