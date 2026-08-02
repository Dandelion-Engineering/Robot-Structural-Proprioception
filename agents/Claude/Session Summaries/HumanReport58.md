# Human Report — Claude Session 58

**Current date and time:** 2026-08-02 00:20 PDT

**Phase:** Phase 2 — Execution

**Session role:** Owner-side exact-state review of the four artifacts Codex handed off
after executing the Protocol-P Stage-A/B/C screen; independent verification of the
result; and closure of whatever the review found.

**Protocol-P execution state:** **Zero rollouts spent this session.** The screen was not
re-run, Stage 0 was not re-executed, and the replay gate was not run. The confirmatory
test split remains untouched at zero identities and zero payloads. `config.json` remains
absent.

**Final config state:** **UNFROZEN.**

---

## Summary

Codex's Session 57 crossed the execution gate: it ran the one-row replay, then ran Stages
A, B and C for the first time, spending 135 physical rollouts over roughly 74 minutes, and
produced a bounded **Case-B** development result. It handed me four artifacts for
exact-state review.

My job this session was to actually review them rather than ratify them. The measurement
survived that review completely. One pre-registered output did not exist at all.

### What I verified, and how

I recomputed the entire result from the persisted artifact and the assignment document
alone, deliberately without importing Codex's driver or the results layer, so that a
defect shared between the producer and a producer-importing checker could not hide from
the check. Everything reproduced:

```text
all ten min_margin values, recomputed from per-cell d and q95_c        EXACT
all 40 per-cell operative_threshold == 2*q95_c and margin == d - thr   EXACT
all four Q95_c, recomputed from the 28 persisted distances at
  method="higher", confirmed to sit at the 27th of 28 order statistics EXACT
all eight headline D values, recomputed as ||b_fault - b_healthy||
  from the raw persisted 8-vectors at the matched identity             EXACT
census: 135 ledger entries / 135 distinct stamps / 147 logical rows /
  12 reuses, each reused stamp cited exactly twice, 168 - 11*3 = 135    PASS
provenance hygiene: every stamp dev-<64 hex>, none equal to the base
  config hash, all 3000 steps, no negative elapsed, no drive-letter     PASS
```

I also made a mistake worth recording, because it is the reason to persist raw vectors in
the first place. My first recomputation of `D` paired each fault against a healthy vector
selected without matching `sensor_seed` and `pair_id`, and produced eight values that
matched nothing — until I noticed they were sitting inside Codex's own `d_unmatched`
lists. I had paired each fault against a Stage-C replicate rather than its matched
partner. My instrument was wrong, not the artifact, and the artifact was detailed enough
to prove which.

### The finding: a pre-registered read that was never implemented

Section 9 of the protocol contains a short, explicit instruction:

> **Role coverage — pre-declared, read before the ladder.** Count known-class testable
> structural settings per split and report the count 0/1/2. OOD at 0.45/0.55 never counts.
> `zero dev -> no testable structural training support` … Any of those three zeroes yields
> a named **role-coverage-bounded non-transfer outcome**.

A search for it across the driver, the results layer and every test returns **zero hits**.
It had never been implemented, in any of the four files both agents reviewed and jointly
approved while declaring the pre-execution implementation list empty, before 135 rollouts
were spent.

That it belongs to this screen is not my inference. The ten ladder severities are exactly
the union of the four splits' own known-class structural severities plus the two
structural OOD severities, and the assignment-derived OOD pair equals the protocol's
pinned `(0.45, 0.55)`. The ladder was built so that coverage could be read off it.

Applying the pre-registered rule to the measured verdicts:

```text
  split   known-class severities   testable    count
    dev   0.5, 0.75                --              0     <-- zero
  pilot   0.6, 0.85                --              0
    val   0.4, 0.9                 0.4             1     thin
   test   0.35, 0.65               0.35            1     thin
```

**Dev at zero fires the named role-coverage-bounded non-transfer outcome: no testable
structural training support.** Zero pilot relabels nothing but disables data-driven
downsizing, so maximum test replication is retained and the limitation must be named.
Val and test are count-1 thin single-severity roles.

This does not make Case B wrong and it does not waste a single rollout. It says Case B is
only half of the Section-9 outcome, and the missing half is the half that bears on what
happens next: Gate 4 trains structural attribution on **dev**, and at the probe the screen
selected, dev contains no structural setting measurable above the operative null. In plain
terms, the structural signature is only measurable at damage more severe than anything the
project reserved for teaching its models. Amendment A2 is the right place to act on that,
which is precisely why finding it before A2 is written matters rather than after.

### What I built

Because the read is a deterministic function of two already-persisted documents, it costs
zero rollouts, so I implemented it rather than only reporting it:

```text
Reproducibility Packet/scripts/analyze_protocol_p_role_coverage.py
Reproducibility Packet/tests/test_protocol_p_role_coverage.py       24 tests
Reproducibility Packet/results/protocol_p/role_coverage.json        the derived outcome
```

It is a separate script rather than a driver change, deliberately. Putting the read inside
the driver would leave the executed artifact unable to carry it without re-spending 135
rollouts to regenerate a number the existing artifact already determines. The script
refuses a plan-mode artifact, a terminal run, a ladder that is not ten distinct values, a
severity that has drifted off the ladder, and an assignment whose OOD pair no longer
equals the protocol's pin.

Full packet suite: **997 passed** (975 + my 22 at the time of the run; 24 after the two
tests added below). Mutation sweep over the new code: 14 cases, **14 caught, 0 survivors,
0 bad anchors** — after fixing two real gaps the first pass found.

### Corrections to my own prior work

**The simulator-cost figure is fifteen, not fourteen.** Codex corrected my thirteen to
fourteen, and it was right that I had missed Session 41's separate all-None regression.
Its recount was itself short by one. Sweeping every session record of both agents rather
than re-reading the one report the previous correction pointed at shows that **Session 39
cost two runs — both agents independently spent one in their own Session 39**, and every
recount so far credited only one of them. With Codex's Session-57 replay and 135 stage
rollouts, the project total is **151**.

The pattern behind five successive wrong values is worth more than the number. Each
correction re-read only the record the previous one pointed at. My own sweep is the
clearest case: I swept the sessions I expected to be *zero* and carried the nonzero ones
forward from my own notes without re-deriving them. I audited the cheap half — which feels
like diligence while leaving the actual sum untouched.

**My proposed readback rule was wrong, and worse than the reason Codex gave for rejecting
it.** Codex rejected my whole-run `max_abs_gauge_true` rule because that maximum spans the
bit-identical pre-onset prefix. Correct, and I accept the replacement without reservation.
But I had also claimed the *direction* — healthy < remEI 0.75 < remEI 0.35 — was
"configuration-free". Measured against the completed run:

```text
cell   healthy   remEI 0.75   remEI 0.35    non-equality   monotone
  4    5.051447   5.403175     7.625701         True         True
  5    5.018674   5.019007     7.457945         True         True
  6    4.766323   4.833703     4.652393         True        FALSE
  7    4.835135   4.720637     5.076979         True        FALSE
```

The monotonicity clause fails in half the cells on a run whose construction is
demonstrably correct. Adopted as written it would have raised a construction alarm on a
valid measurement. I proposed promoting a diagnostic to a hard gate and never measured its
false-positive rate — my own standing lesson, violated in the session after I cited it at
someone else's work.

---

## Challenges and how they were overcome

**Distinguishing a real gap from a misread specification.** "Role coverage — read before
the ladder" reads oddly, since coverage depends on ladder verdicts. Rather than argue from
the phrase, I checked whether the ladder was constructed to serve it, and the union
identity settled it exactly. The phrase governs interpretation order, not computation
order.

**Verifying my own instrument before reporting a discrepancy.** Eight mismatched `D`
values looked at first like a defect in the result. Checking my own pairing before
reporting it showed the fault was mine. This is the standing rule — check a flaw is real
before reporting it — and it nearly failed here because the discrepancy was large and
consistent, which reads as a real defect rather than a lookup bug.

**Two mutations survived my first sweep, and one exposed a test that proved nothing.** My
test asserting that OOD severities are excluded from the counts passed because this
assignment's per-split grids never contain them — the exclusion filter is a no-op on the
current document, so the test verified a property of the *document*, not of my code. I
replaced it with a constructed test that puts an OOD severity inside a split's grid and
asserts it is still excluded, and added a second constructed test that reaches the
empty-known guard. Both mutations are now caught.

---

## Files created or updated

### Created
- `Reproducibility Packet/scripts/analyze_protocol_p_role_coverage.py`
- `Reproducibility Packet/tests/test_protocol_p_role_coverage.py`
- `Reproducibility Packet/results/protocol_p/role_coverage.json`
- `agents/Claude/Session Summaries/HumanReport58.md`

### Updated
- `Reproducibility Packet/README.md` — Step 25 role-coverage section and the
  current-boundary paragraph (reviewer edit, handed back to Codex)
- `agents/Claude/Progress Reports/Progress Report Session 56.md` — fourteen to fifteen
- `README.md` — one new dated Live-Run entry, `+1/−0`, no dated entry edited
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/… - Active.md` — `+253/−0`
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

No Protocol-P driver, results-layer, specification, seam, assignment, draft-config,
Stage-0 artifact, or dataset payload was changed. No new dependency was added.

---

## Dispositions handed to Codex

```text
APPROVED, exact state, unchanged
  results/protocol_p/stage_abc_screen.json         209a87ae...
  README.md (root), Codex's dated 2026-08-01 entry c67a00c3...
    approved as a dated record and NOT edited; its "fourteen / 150" is superseded
    by my new entry, per the standing rule that dated entries are never edited

REVIEWER-EDITED BY ME, HANDED BACK FOR CODEX APPROVAL
  Reproducibility Packet/README.md
  agents/Claude/Progress Reports/Progress Report Session 56.md

NEW, MINE, UNDER CODEX REVIEW
  scripts/analyze_protocol_p_role_coverage.py
  tests/test_protocol_p_role_coverage.py    24 tests
  results/protocol_p/role_coverage.json
```

---

## Next steps

1. Codex reviews the role-coverage script, its tests, its artifact, my packet-README edit,
   and the fifteen-run progress-report state.
2. If Codex disagrees that Section 9's role coverage is a required output of the screen
   rather than a later Gate-7 obligation, that goes to the director rather than into more
   rounds — it decides whether Case B is reportable on its own.
3. Write Amendment A2 at the measured Case-B boundary **and** the role-coverage counts.
   The zero-dev result is a direct input to what A2's severity grid should become.
4. Produce the replacement assignment/config lineage; regenerate the superseded
   development/pilot/validation payloads coherently from zero.
5. Resume Gates 4–7 only after that lineage is approved.

My next regular progress report is Session 64, unless a phase transition or an approved
written amendment triggers one sooner.
