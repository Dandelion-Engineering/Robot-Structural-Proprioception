# Codex — Human Report, Session 80

**Date and time:** 2026-08-05 18:12 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.
**Progress-report session:** yes — `agents/Codex/Progress Reports/Progress Report Session 80.md` was written in addition to the normal session work.

---

## Summary

This session genuinely re-reviewed Claude Session 80's development-only fitting-contract
handback. I accept Claude's shared `require_code_identity` predicate, its producer
post-condition, its two new in-domain type refusals, and its judgment that the remaining
forty fail-closed caller-shape exceptions do not need to expand this review round.

I did **not** approve Claude's exact returned blobs. Removing the producer's early label
validation looked redundant when each field was tested separately, but it was load-bearing
when two fields were malformed together. Direct synthetic probes found two consequences:

1. a path-shaped code label paired with a non-path value was quoted in full by the path
   refusal before the no-path-disclosure predicate could run; and
2. a mapping containing both string and non-string labels reached `sorted()` and raised a
   foreign `TypeError` before the shared post-condition could validate it.

I restored one early call to the already-shared `require_bare_name` predicate, added a
cross-field regression test, and explicitly approved the reviewer-edited state:

```text
Reproducibility Packet/scripts/utils/dev_fit_contract.py
  bd2c0d080f3046837af6fc38232b530749238e4c
Reproducibility Packet/tests/test_dev_fit_contract.py
  fbd941b592436d0303b2ddd6ec6c69906d08bd88
```

The review loop remains **open** because Claude must now re-open and genuinely owner-review
these exact bytes. No trainer exists, no model was fit, no checkpoint/result/dataset was
written, no delivered manifest or `.npz` payload was read, no rollout was spent, and final
`config/config.json` remains absent.

## Review input and accepted work

Claude handed back and explicitly approved:

```text
dev_fit_contract.py       9d6ecfea816833678fdfa667e956539d75e11ade
test_dev_fit_contract.py  d4202c8ea07bed623b4515cd39d9b51a4b470199
```

I re-opened both files, their diff from my Session-79 state, Claude's Session-80 report,
and the exact Phase-2 handoff. Claude correctly reproduced every Session-79 digest and
type finding. The new `require_code_identity` function is the right source of truth for
the mapping a checkpoint producer builds and a provenance consumer audits:

- the mapping must be non-empty;
- every label must be a path-free, single-line bare name;
- every digest must be exactly 64 lowercase hexadecimal characters; and
- both `code_identity()` and `DevFitProvenance.validate()` call that same predicate.

I also accept Claude's two producer-input guards. A non-mapping now fails before
`.items()`, and a non-path mapping value fails before `Path(...)`. Those are likely caller
errors and now remain inside `DevFitContractError` under ordinary and optimized Python.

Claude measured forty other foreign exceptions in the row-selection and completed-plan
entry points and deliberately left them unchanged. I accept that boundary. Every measured
case fails closed; none can cross a fitting authorization; no current caller depends on
the exception class. The later trainer review can tighten a specific ingress if its actual
control flow makes one of those caller shapes or exception domains load-bearing.

## Finding F — validation order across fields

Claude's mutation sweep reported the old in-loop label call as a survivor because deleting
it changed no single-field behavior: the final `require_code_identity(ordered)` call still
rejects a bad label. The untested state combined a bad label with another bad field.

Against Claude's approved blob:

```text
code_identity({"C:\\PRIVATE\\secret.py": None})
  -> DevFitContractError whose message quotes C:\PRIVATE\secret.py in full

code_identity({"net.py": valid_file, None: valid_file})
  -> TypeError: '<' not supported between instances of 'NoneType' and 'str'
```

The first state reaches the path-type refusal before `require_bare_name`, violating that
predicate's documented reason for not echoing a machine path. The second builds both
digests and reaches `dict(sorted(identity.items()))`; Python attempts to order incomparable
keys before the post-condition can run.

The correction calls `require_bare_name(label, "code identity label")` before path
validation. The rule still has one implementation. Its two calls are non-substitutable:
the early producer call establishes safe ordering before later operations, while the
shared final predicate asserts the completed mapping's non-empty, label, and digest
properties. The new test drives both dictionary orders for mixed labels and asserts that
the complete path-shaped label is absent from the refusal message.

## Verification

```text
pre-edit direct probes        full path disclosed; mixed labels raised TypeError
post-edit direct probes       3/3 DevFitContractError; full path absent
focused contract tests        93 passed in 2.21 s
focused under python -O       93 passed in 2.18 s; expected pytest warning only
full packet test suite        1,467 passed in 174.44 s
compileall                    clean
diff against Claude's state   source +7/-7; tests +28/-0
diff hygiene                  git diff --check clean
real-data touches             none
fits / checkpoints            0 / 0
generation / rollouts         0 / 0
final config.json             absent
```

The authoritative transcript handback used the complete programmatically verified unique
normalized EOF anchor. Before the write it had 1,367,293 physical bytes, 21,485 lines, and
SHA-256 `8031be30c6d98bebdf0a51c811641576d030cdc3e467b850d433690c703bf609`.
The first append passed every assertion and produced a `+92/-0` diff. Final diff hygiene
then found that its verification block said test diff `+27/-0` rather than the measured
`+28/-0`. I preserved that turn and appended a short forward bookkeeping correction from a
second verified boundary (1,371,908 bytes / 21,577 lines / SHA-256
`8e0d32013f51ca60c12b0ecbf6ec22d19e6a318676f5930be20393f32fada453`). Across both writes:

- the full 1,367,293-byte prior prefix is identical under that digest;
- each new Session-80 header occurs exactly once after its own recorded boundary;
- Codex is physically last;
- Git reports `+110/-0` for the transcript; and
- the file has 1,372,343 bytes / 21,595 lines with SHA-256
  `434a6ba91328cb23020642c3165a464cf63ac7fe25ba4014b5c9242083176a1b`.

No ordering repair was needed, and no entry was added to the director-visible monitoring
thread.

## Decisions and boundaries

- Claude's Finding E and shared-predicate design are accepted, but blobs `9d6ecfea...` /
  `d4202c8e...` are superseded and not approved.
- I explicitly approve only `bd2c0d08...` / `fbd941b5...`; Claude's owner re-review is
  required to close the exact-state loop.
- The forty measured fail-closed caller-shape exceptions remain outside this review round.
- Trainer construction remains sequenced after this contract loop. The trainer,
  checkpoint writer, result writer, and exact ten-arm execution path require their own
  two-agent executable review before any fit may run.
- Pilot, validation, test, new data generation, dataset supersession, payload measurement,
  final config materialization, and confirmatory work remain blocked.
- The root Live-Run README was deliberately left unchanged: an open contract review is not
  a finished public milestone, and the learned model remains untrained.

## Cross-review and progress report

I read Claude's `HumanReport80.md`, its continuity, the exact Phase-2 turn, and the two
handed-off files. I reproduced the accepted repairs rather than relying on Claude's report.
Because this is Codex Session 80, I also wrote the regular eight-session director update:
`agents/Codex/Progress Reports/Progress Report Session 80.md`.

## Files created or updated

- `Reproducibility Packet/scripts/utils/dev_fit_contract.py` — restored early shared
  bare-name validation before path handling and sorting; updated the ordering rationale.
- `Reproducibility Packet/tests/test_dev_fit_contract.py` — cross-field disclosure and
  mixed-label regression coverage.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — append-only exact-state review, approval, and owner handback.
- `agents/Codex/Progress Reports/Progress Report Session 80.md` — regular director update
  covering Sessions 73–80.
- `agents/Codex/Session Summaries/HumanReport80.md` — this report.
- `agents/Codex/README.md` — workspace index refreshed for Session 80.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten resume state.

## Next steps

1. Claude re-opens and genuinely reviews blobs `bd2c0d08...` / `fbd941b5...`.
2. If Claude approves them unchanged, the development-fit contract loop closes.
3. Claude then builds the bounded trainer/checkpoint/result writer and explicitly approves
   its exact executable handoff.
4. Codex reviews that exact executable state before any fit.
5. Only after that later review closes may the ten predeclared dev-only C1/S fits run.

The central research measurement still has not run. This session strengthened the
development-only training boundary; it produced no evidence about the hypothesis.
