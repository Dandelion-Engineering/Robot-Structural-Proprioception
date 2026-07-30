# Human Report — Codex Session 47

**Current date and time:** 2026-07-30 11:18 PDT

**Phase:** Phase 2 — Integration and Reproducibility Build

**Session role:** Exact-state review of Claude's extended Protocol-P Stage-0 implementation

**Final config state:** **UNFROZEN**; no final `config.json` exists

**Protocol-P execution state:** Stage 0 was **not run**. `Reproducibility Packet/results/protocol_p/`
remains absent. No Stage-0 identity, statistic, null distribution, or result artifact
exists. Stages A/B/C remain unauthorized. The confirmatory test split remains untouched.

---

## Summary

Claude Session 47 genuinely re-reviewed Codex's Session-46 corrections and found a
second member of the same config-binding class. Three of Stage 0's seven pinned CLI
values also exist in the configuration document whose hash the artifact identity would
stamp:

```text
window         768    <-> values.timing.window_steps
f_ctrl_hz      500.0  <-> values.timing.f_ctrl_hz
diagnostic_hz  0.8    <-> values.timing.diagnostic_probe.frequency_hz
```

Claude added a fail-loud equality guard and returned two extended files for review.
This session independently reproduced the exact handoff, verified the three-member
boundary against Protocol P and the committed config, and traced the reachability claim
through the real assignment-binding implementation.

The production correction is correct. Equality rather than adoption preserves Protocol
P Section 8 as the authority, and the exclusions are semantically right: `pairs`,
`seed`, and `pair_id` have no config counterpart, while the numeric `3.0` in the
validation environment is a sinusoidal plant-side quantity and is not Stage 0's imposed
linear sensor-path thermal excursion.

The review found no production defect, but it found two blocking defects in the new
test evidence:

1. one test described a divergent config as a currently constructible, correctly-bound
   end-to-end state even though it had to monkeypatch the real binding gate away; and
2. another test claimed to verify the binding gate while reimplementing the parent-hash
   arithmetic locally and never calling the production gate.

Codex corrected both tests directly, explicitly approved the resulting two-file state,
and returned it to Claude for genuine owner re-review. Because the test file changed,
the implementation loop remains open and Stage 0 remains unauthorized.

## Context and review method

The session followed the repo's controlling startup order:

1. read `AgentPrompt.md`;
2. read the complete project details;
3. read Codex continuity;
4. ingest all Codex-relevant chat summaries, active-thread routing, the newest Claude
   report, and Claude's physical-tail handoff;
5. read `Playbooks/review-cycle.md` and
   `Playbooks/reproducibility-packet.md`;
6. read the complete jointly approved
   `Reproducibility Packet/protocol/protocol-p-v2.3.3.md`; and
7. review the exact production diff, test diff, config, and assignment-binding source.

The repo began clean at commit `5514a609fffbe8adda7266bbfc16169631bd437a`
(`Claude Session 47`).

The handoff's exact byte claims reproduced:

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
  git blob    8435c764a76cb091278ffa47f14584dbf43b40ce
  raw sha256  4a9fc5955bb5d0f103d258525ee80f5766e0e9a46b01975c76ab895c53815b24
  bytes       40,098

Reproducibility Packet/tests/test_synchronous_difference_null.py
  git blob    85354c762c16f0e3268909b75ce13cb3b87c3762
  raw sha256  6cfb5f398054da9e4922ace74005ebb2724bd169bdc594ccc348260346fcadea
  bytes       44,032
```

Both were UTF-8 without BOM and pure LF. Protocol P's canonical digest also reproduced
at `5689dad7ce4194b9a7dbe381006027df178997adf732f5734a77ef048bdf421f`.

## Production review

### The shared timing boundary is exact

The three included pins are the only Stage-0 decision values that are also semantically
the same quantities in the bound timing block. The new
`CLI_TO_BOUND_TIMING_PATH` mapping is therefore complete without overreaching.

The new `require_bound_timing_matches_cli()` guard:

- walks each declared document path fail-loud;
- rejects missing, boolean, non-numeric, and non-finite values;
- requires exact equality with the protocol pin;
- returns the values it actually read for console disclosure; and
- is called after assignment binding but before identity construction, measurement,
  output-directory creation, or artifact writing.

The equality design is important. Reading timing from the config would silently transfer
authority away from Protocol P and defeat `require_pinned_cli()`. Requiring agreement
keeps the pre-registration authoritative.

### The reachability narrowing is correct

`validate_approved_assignment_binding()` reconstructs the approved parent config from
the current embedded-assignment draft by:

- replacing `values.scenario_manifest` with `None`;
- restoring the recorded parent open gates;
- restoring the recorded parent draft hash; and
- recomputing the canonical config hash.

The recomputed hash must equal the assignment-bound parent hash. Therefore, a rehashed
change to either `values.timing` or `values.sensor_model` fails the binding gate before
either bound-value guard runs.

This corrects Codex Session 46's wording forward: within the current I1-pinned assignment
lineage, a later valid sensor-model change cannot merely move the artifact identity while
leaving the measurement on stale defaults. It requires a new draft lineage, a replacement
assignment, and a new I1 pin. The timing and sensor guards protect code today — a skipped
or reordered binding gate, or a future caller — and become live data checks when the
pre-confirmatory lineage is legitimately re-derived.

Codex explicitly approved the production file unchanged at Claude's blob
`8435c764a76cb091278ffa47f14584dbf43b40ce`.

## Test-evidence corrections

### Correction 1 — distinguish a bypassed code path from an end-to-end data state

The original
`test_main_refuses_a_divergent_document_and_writes_nothing` claimed that its divergent
document was valid, schema-clean, correctly bound, and constructible end to end. The test
then monkeypatched `validate_approved_assignment_binding()` to accept the document.

Codex renamed it to
`test_main_guard_refuses_a_divergent_document_when_binding_is_bypassed` and rewrote the
docstring. It now states that the monkeypatch deliberately models the code defects named
by the production docstring: a caller that skips the binding gate or a future reordering
of `main()`. It explicitly disclaims a currently constructible end-to-end data state.

### Correction 2 — call the production binding gate

The original
`test_the_binding_gate_pins_the_blocks_both_guards_read` manually reconstructed the
parent hash. That proved the local arithmetic's sensitivity to the changed value, but it
did not prove that `validate_approved_assignment_binding()` enforces the comparison. A
mutant production gate that simply accepted the changed block could leave the test green.

The corrected test now:

1. loads the committed config and assignment;
2. requires the unmodified control binding to pass through the real gate;
3. changes either `timing.window_steps` or
   `sensor_model.gauge_noise_microstrain`;
4. recomputes the current document's own config hash, preventing a stale-self-hash
   shortcut; and
5. requires the real production binding gate to reject the changed document because it
   cannot reconstruct the approved parent.

An injected accept-all binding-gate mutant is caught by the corrected test.

### Count correction

`test_synchronous_difference_null.py` collects 99 tests, up from 81. The reported 117
is the correct combined focused total after adding the unchanged 18 tests in
`test_gauge_windows.py`; it is not the count of the Stage-0 test file alone. The active
transcript carries this forward correction rather than rewriting Claude's prior report.

## Reviewer-edited exact state

```text
Reproducibility Packet/scripts/analyze_synchronous_difference_null.py
  git blob    8435c764a76cb091278ffa47f14584dbf43b40ce
  raw sha256  4a9fc5955bb5d0f103d258525ee80f5766e0e9a46b01975c76ab895c53815b24
  bytes       40,098

Reproducibility Packet/tests/test_synchronous_difference_null.py
  git blob    9591c91bd6412a9dd60860e05c40fcbcccc9ff74
  raw sha256  2fe39d831fa500d5183108ee4aed6590ac676af8beafec122b9af4919c9402ff
  bytes       44,285
  encoding    UTF-8, no BOM, pure LF
  review diff +27 / -22 against Claude's handed-back blob
```

Codex explicitly approves this exact two-file state. Claude must genuinely owner-review
the changed test file and explicitly approve the same state before the implementation
loop can close.

## Verification

```text
Claude handoff: Stage-0 test file                  99 passed
Claude handoff: full packet suite                 595 passed
reviewer-edited Stage-0 test file                 99 passed in 1.45 s
reviewer-edited Stage-0 + gauge-helper files     117 passed in 1.50 s
reviewer-edited full packet suite                 595 passed in 12.56 s
compileall                                        clean
accept-all binding-gate mutant                    caught
git diff --check                                  clean
results/protocol_p                                absent
final config.json                                 absent
test-named payload paths in retained data root    0
```

No Stage-0 measurement was run. No output directory was created. No plant rollout,
dataset payload, assignment, config, protocol, replay gate, helper/floor file, or
confirmatory identity was changed.

## Transcript and public-state handling

The Phase-2 transcript append used the physical-tail hard gate:

```text
pre-write lines      10,414
pre-write bytes      773,918
pre-write sha256     9a600a18950aeda8c884e021b42d2420d5e54b868802b8f94e327786e42c3e01
Codex header         line 10,418; count 1; after the old boundary
old byte prefix      exact
transcript diff      +159 / -0
post-write lines     10,573
post-write bytes     781,095
post-write sha256    b266a49416aabd3ccedbf6d12f4dfdf85c6809b38dc16b260d3926c5dd4c6104
physical last author Codex
```

The first append attempt made no change because the terminal-rendered sign-off did not
match the stored Unicode em dash. The hard gate stopped safely. Codex read the literal
UTF-8 EOF representation, reapplied against the exact complete tail, and verified the
old byte prefix and additions-only diff.

No recurrence occurred, so the director-visible transcript-order monitoring thread was
not updated.

The public Live-Run README heartbeat was a deliberate no-op. This session closed no
artifact or phase, produced no Stage-0 result, and only advanced an internal review
round. Adding an entry would violate the README playbook's lean milestone rule.

## Files created or updated

- `Reproducibility Packet/tests/test_synchronous_difference_null.py` — corrected the
  bypassed-state claim and replaced duplicated hash arithmetic with the real binding
  gate.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended Codex Session 47 review and exact-state handback.
- `agents/Codex/Session Summaries/HumanReport47.md` — this report.
- `agents/Codex/README.md` — updated the session index and active Stage-0 review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the
  next session.

No source ledger update was needed; no external sources were read.

## Decisions

1. **Approve the production timing guard unchanged.**
2. **Block the handed-back test state** on the unreachable end-to-end claim and the
   reimplemented gate test.
3. **Correct the tests directly and approve the reviewer-edited state.**
4. **Keep Stage 0 unauthorized** until Claude explicitly approves the same state.
5. **Keep Stages A/B/C unauthorized**, final `config.json` absent, and the test split
   untouched.
6. **Do not update the public README** for an internal, still-open review round.
7. **Do not update the monitoring thread** because the append landed cleanly.

## Next steps

1. Claude re-opens the reviewer diff in
   `test_synchronous_difference_null.py`, verifies both corrections, reproduces the
   exact blob, and explicitly approves or edits-and-returns it.
2. Only after that same-state owner approval may exactly one pinned Stage-0 execution
   occur.
3. The Stage-0 result and artifact must receive a separate review before any later
   driver work.
4. Stage-A/B/C implementation and execution remain unauthorized until the Stage-0
   result review closes.
5. Amendment A2, replacement assignment, coherent from-zero regeneration, Gates 4–7,
   final config freeze, and confirmatory test materialization remain later gated work.
6. Codex's next regular progress report is due in Session 48 unless a phase transition
   or approved written Claim Sheet amendment triggers one earlier.
