# Human Report — Codex Session 52

**Current date and time:** 2026-08-01 02:10 PDT

**Phase:** Phase 2 — Execution

**Session role:** Exact-state reviewer of Claude Session 52's returned Protocol-P construction tests and public live-run entry

**Final config state:** **UNFROZEN**; no `config.json` exists

**Protocol-P execution state:** Stage 0 remains executed exactly once and jointly approved. No replay or Protocol-P stage rollout ran this session. Stages A/B/C remain unexecuted, their driver is not yet built or approved, and execution is unauthorized. The confirmatory test split remains untouched.

---

## Summary

Claude genuinely re-reviewed the four files Codex edited in Session 51. Claude independently confirmed both blocking findings, approved the production construction module and shared-test file unchanged, and returned the construction-test file with six additions covering five guards that Codex had added but not discriminated. I reviewed those tests against the actual guard paths and approve blob `1874773e...` unchanged.

That same-state approval closes the shared-primitives extraction and construction-layer review loops. The jointly approved construction set is now the production module at `7fdddf0e...`, the construction tests at `1874773e...`, and the shared tests at `f505877f...`. The driver remains a separate future implementation/review gate.

I could not approve the public README unchanged. Claude's `155 / 750` count update was correct, but the active entry said the approved 100-pair Stage-0 measurement had been re-derived bit-for-bit after the refactor. The actual post-refactor check intentionally ran only `pairs=2` and reproduced the artifact's first two distances; the spent 100-pair stage was not re-run. The entry also still described the construction layer as unapproved even though this review closes that loop. I corrected those current-state claims, advanced the banner date to 2026-08-01, and explicitly approved the new README blob `1b297607...`. Claude must genuinely re-review that exact state before the public-entry loop closes.

No production code, result artifact, protocol file, assignment, config, dataset payload, or confirmatory material changed. The focused tests pass 155/155, the full packet passes 750/750, and `compileall` is clean.

---

## What I reviewed

I followed the `AgentPrompt.md` workflow before acting:

- checked and claimed the project lock;
- read the current project details and Codex continuity;
- read every Codex-involving chat summary, the transcript-monitoring thread, and the authoritative Phase-2 transcript chronology/current tail;
- read the review-cycle, reproducibility-packet, and live-run README playbooks;
- read Claude's Session-52 handoff and `HumanReport52.md`; and
- reviewed the exact current blobs, Claude's diff, the production guards, and the new tests before running the focused and full packet suites.

The exact handed-back states were:

```text
Reproducibility Packet/tests/test_protocol_p_conditions.py
  blob 1874773e1ee8ed41bb763ca3a8a235d89e7c02e9

README.md
  blob 78b4a734303d36ded16d29788084305c30798d80
```

Claude also explicitly approved Codex's unchanged production/shared-test states:

```text
Reproducibility Packet/scripts/utils/protocol_p_conditions.py
  blob 7fdddf0eee5e3b3f02b2db21ecb1b70728234be5

Reproducibility Packet/tests/test_protocol_p_shared.py
  blob f505877fbc43adb8c3ec2311674008f0c3b0e337
```

---

## Construction-test decision

### Approved unchanged

The six new test functions cover the five mutation gaps for the intended reasons:

1. **Source base-pair and split-group guards.** The two parametrized mutations preserve the cell-4 scenario while substituting only cell-5's base pair or split group. Each therefore reaches the specific guard it is meant to test instead of stopping at the scenario check.
2. **Real-source reachability.** The document-backed test loads and expands the approved assignment, selects the four delivered healthy `dev/t01` reservations, accepts each for its own cell, and refuses it under every other cell. This checks the positive construction path that hand-built rejection fixtures cannot establish.
3. **Stage-C identity membership.** The three invalid identities are otherwise well-formed: a cell-5 Stage-C identity, cell 5's Stage-A/B identity, and a fabricated out-of-table cell-4 Stage-C pair. Each reaches the Stage-C membership site. The valid `k=0` reuse is deliberately excluded because I6 makes it the target cell's Stage-A/B identity.
4. **Closed stage vocabulary.** Each invented stage carries a valid cell-4 Stage-C identity. Removing the vocabulary guard therefore falls into the Stage-C branch and accepts, making the test discriminating rather than merely malformed-input coverage.
5. **Condition/fault binding.** The direct `rollout_provenance` cases distinguish fault count, onset, and severity. The onset case explicitly recreates the scientifically important step-0 versus step-500 fault mismatch.

I accept Claude's two recorded narrowings without requesting a production edit:

- the source/body relation is bound transitively by selecting from the I1-pinned assignment document, so the driver must select the source from that document and never construct one; and
- the `build_overrides` I13a call is presently tautological, although it models a meaningful future construction boundary. It must not be credited as an independently live guard in a report.

Exact jointly approved construction state:

```text
scripts/utils/protocol_p_conditions.py  7fdddf0eee5e3b3f02b2db21ecb1b70728234be5
tests/test_protocol_p_conditions.py     1874773e1ee8ed41bb763ca3a8a235d89e7c02e9
tests/test_protocol_p_shared.py         f505877fbc43adb8c3ec2311674008f0c3b0e337
```

---

## Public README finding and reviewer edit

Claude correctly updated the active entry's verification count from 141/736 to 155/750 and accurately noted that each agent found real defects during the two review passes. One separate statement remained too broad:

```text
the already-approved Stage-0 measurement re-derived from the refactored code
and identical to the recorded values bit for bit
```

The Phase-2 record is explicit that the pinned 100-pair invocation had been spent and was not re-run. The post-refactor numerical check was:

```text
recorded first two distances   0.17764883124109498   0.1894914916579524
fresh run_null(pairs=2)        0.17764883124109498   0.1894914916579524
spent 100-pair stage           not re-run
```

I reviewer-edited only the live banner and newest active-review entry:

1. advanced `Last updated` to `2026-08-01`;
2. changed the stale review status to say the construction layer is jointly approved while the driver is not built or approved; and
3. narrowed the numerical claim to the artifact's first two pair distances and explicitly preserved the no-rerun boundary.

Exact state handed back and explicitly approved by Codex:

```text
README.md
  git blob    1b2976070ace4ce173d06efef50b71b26e22c402
  raw sha256  77636189d149d0d8e483fbddf8f18ca79a1016ce93d7ab69281172b793c640dd
  bytes       76,618   UTF-8, no BOM, pure LF
```

No settled dated entry was changed. Claude owner re-review remains required because an edit is not approval.

---

## Verification

```text
focused construction + shared tests     155 passed in 0.75 s
full packet suite                        750 passed in 13.16 s
compileall                               clean
git diff --check                         clean (checkout-EOL warnings only)
config.json                              absent
Stage-0 artifact                         unchanged; not re-executed
replay / Protocol-P stage rollouts       none this session
confirmatory test split                  untouched
```

The transcript append passed the hard gate:

```text
pre-write lines                          12,409
pre-write bytes                          871,716
old-prefix SHA-256                       3938bd2fa237f1d3ee7e7d251d213122d1fbf7171281eb127b13cafe4433cb3b
old prefix after append                  exact
Codex Session-52 header                  exactly once, line 12,412
header after pre-write boundary          yes
transcript diff                          +128 / -0
physical tail                            Codex Session 52
```

---

## Challenges and reasoning

### Distinguishing real test coverage from test count

The handoff added fourteen collected cases, but count alone is not evidence. I traced each case to the production raise site that would disappear under the stated mutation and checked that no earlier guard masks it. This confirmed that the additions discriminate the five claimed gaps rather than merely increasing coverage volume.

### Keeping the public claim aligned with the instrument actually used

The public entry's broad wording was easy to accept because the first two re-derived values were bit-identical and the approved artifact itself did not change. But a two-pair path check is not a 100-pair re-derivation. The right correction names both what was verified and what was deliberately not executed.

### Updating current state without rewriting history

The newest public entry was still in active review, so reviewer-editing its count and current approval status is permitted under the review cycle. Earlier settled entries and corrections remain append-only. The banner is intentionally overwritten to stay current.

---

## Files created or updated

- `README.md` — reviewer-edited the active public state and banner; awaiting Claude owner re-review.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — appended the exact-state decision under the verified physical-EOF gate.
- `agents/Codex/Session Summaries/HumanReport52.md` — this report.
- `agents/Codex/README.md` — added Session 52 and updated the authoritative live-state descriptions.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for the next session.

No progress report was due: Session 52 is not an every-eighth session, and no phase transition or approved Claim Sheet amendment occurred.

---

## Next steps

1. Claude must genuinely re-open and review `README.md` at blob `1b297607...`, then explicitly approve it unchanged or edit-and-return.
2. If Claude approves that exact state, the public-entry loop closes and the results module plus Stage-A/B/C driver may be implemented and handed off for a new exact-state review.
3. Driver implementation permission is not execution permission. No replay or Stage-A/B/C rollout is authorized until the later driver review loop closes explicitly.
4. Configuration freeze, Amendment A2, replacement assignment, coherent regeneration, Gates 4–7, and confirmatory generation remain downstream and blocked.

— Codex
