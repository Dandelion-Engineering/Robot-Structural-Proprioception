# Codex — Human Report, Session 112

**Date and time:** 2026-08-10 19:14 PDT

**Phase:** Phase 2 — Execution, with limited Phase-3 packet assembly

**Progress-report session:** Yes. The regular Codex report covering Sessions 105–112 was created
at `agents/Codex/Progress Reports/Progress Report Session 112.md`. The next regular Codex report
is Session 120 unless a phase transition or approved Claim Sheet amendment triggers one sooner.

---

## Summary

Claude Session 112 genuinely re-opened Codex’s reviewer-approved rung-2 design, accepted all seven
Session-111 repairs, added two narrow specification clarifications, explicitly approved the new
state, and handed it back. I authenticated and re-read the complete returned document, verified
both new clauses independently, and explicitly approved the same exact blob:

```text
Reproducibility Packet/protocol/rung2-escalation-v0.1.md
Git blob                 404c9f1fc1b0112e5ed8164853b261e97d510662
raw/canonical SHA-256    9a154f902d7a98dcaa3e8bd34109e2ea6c4f29ba08c86a4ad301bfd62e69bf1f
size / physical lines    53,497 B / 807 LF
CR / BOM / final newline 0 / none / yes
Git attributes           text, eol=lf
delta from prior state   +19 / -9, three hunks
```

The design review loop is therefore **CLOSED / BOTH APPROVED at blob `404c9f1f...`**. That closure
authorizes only writing `Reproducibility Packet/scripts/utils/attribution_net_rung2.py` and its
tests. Claude owns the estimator lane. No executable, plan, fit, analyzer, role read, capacity,
threshold, or final configuration is authorized.

The general recent-work review found one separate public wording defect. Claude’s progress report
and new Live-Run entry called a 79-seed Stage-1 extension “a lunch break away.” The jointly
approved precision note instead projects 740 additional fits and roughly 2.15 hours under a loose
whole-invocation rate, with a 47–162 seed uncertainty range and no guaranteed timing-error
direction. I preserved the public history and appended a forward correction. I explicitly approve
the corrected README working blob `bb98b66e...`; Claude’s same-state owner re-review is open on
that README only. The design closure is separate and unaffected.

## Exact-state design review

### Returned edits

Claude’s three hunks did only the following:

1. updated the mutable review-candidate status to name both prior review states and state that the
   current bytes are a new state;
2. specified that the RNG fork is entered before `manual_seed(seed)` is called inside it; and
3. clarified that persisting the required rung-2-minus-rung-1 primitive does not itself assert a
   cross-rung direction, while no interpretation row licenses prose about that field.

No parameter count, component ledger, grid row, admissibility band, seed budget, runtime field,
objective gate, outcome row, resource ceiling, or sequencing step changed.

### Finding BI — RNG order

The source citation is exact. In the approved rung-1 module,
`attribution_net.py:317-318` enters `torch.random.fork_rng(...)` and then calls
`torch.random.manual_seed(seed)` inside the context.

I drove both orderings in the project virtual environment using synthetic modules only:

```text
seed inside the fork     caller RNG preserved     True
seed before the fork     caller RNG preserved     False
```

Both orders create the same parameter shapes, so the exact-count invariant cannot detect the
mistake. R13’s caller-RNG assertion is the load-bearing guard. Claude’s clause is correct and is
kept unchanged.

### Finding BJ — persist versus interpret

Section 5.2 requires the analyzer to persist `rung2_minus_rung1` primitives. Section 5.3 forbids
asserting a trend, slope, or direction across two rungs. Claude’s clarification makes the already
settled Stage-1 distinction explicit: record contents may be persisted and quoted, but no line or
direction may be inferred unless a predeclared interpretation row licenses it. Section 5.4 has no
row that reads or licenses prose about `rung2_minus_rung1`, so the edit closes the apparent
contradiction without widening the result.

### Approval decision

`git diff --check` is clean and the only file delta from Codex’s prior approved state is the three
hunks above. I explicitly approved blob `404c9f1fc1b0112e5ed8164853b261e97d510662` in the active
Phase-2 transcript. Claude had already explicitly approved that blob. The exact-state design loop
is closed.

## General recent-work review and public correction

I read Claude’s `HumanReport112.md`, `Progress Report Session 112.md`, exact design bytes, public
README diff, and active transcript turn. The report accurately described the design review. The
cost phrase did not preserve the precision note’s boundary.

The approved note states:

```text
all five widths to 79 seeds     740 new fits
rough elapsed projection        7,745 s / 2.15 h
seed-count uncertainty          47–162 under the pooled-SD interval
timing domain                   whole-invocation rate proxy
timing error direction          unknown; may over- or under-estimate
```

Calling that “a lunch break away” is unsupported and conflicts with the same public entry’s
correct statement that a one-sided cost bound had been withdrawn. I did not rewrite the existing
append-only log entry. I appended a dated cost correction immediately after it, preserved the
decision not to spend more seeds on the current Stage-1 statistic, and stated that the correction
changes no scientific result.

The corrected README working state is:

```text
Git blob                 bb98b66ecf4ed37f2c13bc38607fd3dd88ecdf24
local raw SHA-256        6139560487e011289d283ff78aec67440c20dbfb7e62a508e79d860d7c88c0e7
working diff             +2 / -0
review state             CODEX APPROVED / CLAUDE OWNER RE-REVIEW OPEN
```

The historical Claude progress report was not rewritten. The active transcript records the
forward correction and tells future work not to propagate the phrase.

## Transcript integrity

The Phase-2 append used the complete programmatically verified unique physical EOF block. All
post-write assertions passed:

```text
pre-write transcript       1,923,971 bytes / 31,048 LF
pre-write SHA-256          e6308855fb0d726e6ccb57234667bad44854b75940805f84918fe01f2939ca52
old prefix                 byte-identical
Codex header               unique at physical line 31,050
transcript diff            +69 / -0
last agent                 Codex
post-write transcript      1,928,013 bytes / 31,117 LF
post-write SHA-256         3694fd8e5a0eca0e2610df5d934c9206fcfbb202f47baeb505c02455d3ad3066
```

No Transcript Order Monitoring entry was needed. I accepted Claude’s proposed cross-agent
prior/post digest comparison as a standing non-blocking convention when the previous author has
published a digest; absence of one is not a new gate.

## Files created or updated

- `README.md` — appended the public cost correction; Claude owner re-review open.
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the exact design approval, public correction handoff, digest convention, and resource
  boundary.
- `agents/Codex/Progress Reports/Progress Report Session 112.md` — regular director-facing report
  covering Sessions 105–112.
- `agents/Codex/Session Summaries/HumanReport112.md` — this report.
- `agents/Codex/README.md` — updated navigation and current review state.
- `agents/Codex/Summary of Only Necessary Context.md` — completely rewritten for Session 113.

Deliberately unchanged: the jointly approved rung-2 design bytes, every executable/test, every
Stage-1 plan/result/artifact/checkpoint, the Claim Sheet, both `.gitattributes` files, both
`.gitignore` files, `director_requests.md`, and the absent final config.

## Resource and evidence boundary

This session ran one synthetic RNG-order probe and no project-data operation. It opened no
manifest, `.npz`, label payload, model checkpoint, pilot outcome, validation outcome, or test
outcome. It ran no fit, wrote no checkpoint, generated no data, spent no rollout, invoked no C7
reader, ran no plan mode, selected no capacity, set no threshold, and materialized no final
configuration.

Rollouts remain 278. The fit counter remains 13. Stage 1 remains complete as scoped and licenses
only its no-readable-shape sentence.

## Next steps

1. Claude genuinely re-opens README blob `bb98b66ecf4ed37f2c13bc38607fd3dd88ecdf24`
   and either explicitly approves it or returns another public README state.
2. Independently, Claude may begin the only act licensed by the closed rung-2 design: write
   `Reproducibility Packet/scripts/utils/attribution_net_rung2.py` and its tests.
3. Codex then reviews that exact module/test state. Module approval will not authorize the
   executable, plan, fits, analyzer, later-role read, capacity, threshold, or final config.
4. The 55-checkpoint clean-machine recovery/distribution limitation remains open for Phase 3.
5. Codex Session 120 is the next regular progress-report session.
