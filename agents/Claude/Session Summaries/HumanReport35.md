# Human Report — Claude Session 35

**Current date and time:** 2026-07-25 14:50 PDT
**Phase:** Phase 2 — Execution
**Session role:** Respond to Codex's block on Amendment A2; audit the margin yardstick; discharge the forward correction
**Final config state:** **UNFROZEN** (`Reproducibility Packet/config.json` remains absent)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Session decision:** `ACCEPT_BLOCK_AMENDMENT_A2_PROPOSAL`; corrected A2 posted; **my own S34 headline characterisation withdrawn on new evidence**

---

## Summary

### What I set out to do, and what actually happened

I opened the session expecting a drafting job: Codex had blocked Amendment A2 on two
narrow formulations, and the task was to replace them and hand back corrected text.

Before writing that text I went to audit the one quantity the amendment is
denominated in — the "2.0× margin over the 0.405 µε detection floor" that A2 part (3)
proposed re-deriving the diagnostic probe against. That audit invalidated the premise
of my own Session-34 headline. The session became an investigation, and the corrected
amendment that came out of it is materially different from the one I proposed.

**The short version:** the experiment has been probing itself with a substantially
weaker excitation than the one it screened and approved, because a shape parameter of
that excitation was never written into the configuration. My Session-34 conclusion —
that the reserved damage levels are "2× to 40× too mild" — was measured under that
weaker excitation and is withdrawn.

### The audit, in three findings

**Finding A — the delivered probe is not the probe that was screened.**
`screen_synchronous_safe_probe` selected the 0.05 N amplitude on a measured structural
signature of **1.015 µε** at remaining EI 0.50. The delivered dataset, at the same
severity and amplitude, produces **0.1749 µε** — a **5.8× shortfall**. The margin that
justified the amplitude was never realised in the generated data.

Part of the gap is a concrete implementation discontinuity I traced to a single line.
The draft config pins the probe as `{peak_force_n: 0.05, frequency_hz: 0.8, cycles: 1,
envelope: "raised_cosine"}` and **does not pin the ramp width**.
`assignment_generator._physical_config:337` hard-codes `ramp = duration / 2` (0.625 s,
the maximum the mechanics validator allows — a pure Hann with no plateau), while
**every screen in the evidence base** used `ramp_period_fraction = 0.125` (0.15625 s).
Measured on the delivered development diagnostic trajectory, matched sensor seed:

```text
ramp 0.625 s   (delivered)   privileged 0.1871   observed 0.1749 µε   0.43×
ramp 0.15625 s (screened)    privileged 0.2885   observed 0.2927 µε   0.72×
                                                 ratio 1.54×
```

This is Standing Lesson 7 firing on the project: the pre-registered text did not
generate the pre-registered data.

**Finding B — the generator's unpinned choice is nevertheless the better one.**
I nearly proposed "restore the screened ramp." Measuring first stopped me. Sweeping
amplitude against the A1 safety envelope:

```text
delivered ramp 0.625 s                    screened ramp 0.15625 s
0.05 N  0.43×  |qd|  0.78  PASS           0.05 N  0.72×  |qd|  1.09  PASS
0.10 N  0.90×  |qd|  1.54  PASS           0.075N  1.04×  |qd|  1.57  PASS
0.15 N  1.36×  |qd|  2.17  PASS           0.09 N  1.22×  |qd|  5.16  BLOCK
0.30 N  2.58×  |qd| 62.35  BLOCK          0.15 N  1.98×  |qd| 58.69  BLOCK
```

The sharp envelope gives 1.54× more signal per newton but destabilises the closed loop
at 0.09 N; the gentle one tolerates 0.15 N. **Net achievable margin: 1.36× gentle vs
1.04× sharp — the generator's unscreened choice wins.** The defect is that it is
unpinned and unvalidated, not that it is wrong. Standing Lesson 9's corollary earned
its keep here: I searched the history before calling a settled parameter a defect,
found no record of the choice, measured it anyway, and the measurement reversed me.

**Finding C — the binding constraint is closed-loop stability, far inside A1.**
At 0.15 N the plant sits at `|qd|` 2.17 rad/s against a 10 rad/s ceiling and `|gauge|`
5.45 against 500 — enormous kinematic headroom. At 0.30 N it is violently unstable
(`|qd|` 62 rad/s, `|gauge|` 2486 µε). The 0.15→0.30 N boundary coincides with shoulder
actuator authority (tip moment arm 0.80 m × `torque_abs_limit[0]` 0.20 N·m → 0.25 N).
The sharp envelope destabilises at 36% of that limit, so envelope shape matters
independently — broadband transient content excites compliant modes the 0.005
derivative gain cannot reject. **None of this is visible from the spike configuration
the probe was screened in**, which ran near the kinematic limits and therefore hit
safety blocks before authority blocks.

### What this does to my Session-34 headline

At the largest A1-admissible amplitude the achievable margin at remaining EI 0.50 rises
from 0.43× to **1.36×** — a factor of 3.2 — which moves the detectability threshold to a
severity substantially milder than the ~0.17 I reported, plausibly near the reserved
grid's lower end. **I withdrew the "2× to 40× too mild" characterisation** in the chat
and in the public running log. It is an artefact of measuring at an amplitude that was
never the screened one.

The Session-34 separability result itself is unaffected and I did not retract it: it
measured what the delivered data actually contain, both suites saw identical excitation,
and the actuator positive control ran through the same instrument. What changes is the
*diagnosis* — the structural settings are **under-excited relative to their own screen**,
not merely too mild.

### The corrected Amendment A2

Posted to the Phase-2 chat. Both of Codex's objections accepted without argument.

- **Objection 1 (mild stratum).** Adopted Codex's exact formulation, scoped to the
  assigned development contexts at remaining EI 0.75 and 0.50. No claim is made about
  the mild stratum as a whole; the 472 delivered payloads become a superseded
  pre-amendment set in the packet exclusion trail.
- **Objection 2 (undefined estimand).** Answered prospectively and **conditionally**,
  because whether strata exist at all depends on the selection's outcome. Case A (probe
  fix clears every reserved severity) → the existing single estimand stands unchanged.
  Case B (clears a subset) → a testable stratum and a sub-threshold stratum, with
  non-structural rows **shared**, each row weight 1, the paired bootstrap drawing shared
  rows once per replicate to preserve dependence, **one** confirmatory decision (so no
  multiplicity correction), one model per suite trained across both strata with
  stratified evaluation. Case C (nothing passes) → Slot-12 method failure plus a
  Slot-13 excitation-bounded shape, not dressed as a hypothesis result.
- **Parts (2) and (3) merged** into a single joint selection of excitation and severity,
  since Findings A–C show they trade against the same margin and the amplitude was
  mis-set. Protocol P is stated in full — exact candidate grids for ramp and amplitude,
  hard admissibility conditions, a **worst-cell** margin rule over every development
  context (Codex's "not from one favourable cell"), tie-breaking toward the smallest
  amplitude per the Efficiency standard, and a declared failure action.
- **Deliberately not run.** Codex required the rule be stated before the selection
  executes. Protocol P is posted unrun. My amplitude sweeps are labelled **scoping** —
  single-cell, disclosed in full, and incapable of determining the outcome because the
  pass rule is a minimum over all cells.

### Forward correction discharged

Codex flagged that `screen_structural_separability.py:742` hard-codes "exact 8-cell
floor (p = 0.0078)" into both rendered reports. It was right, and the defect was worse
than a label: at `n_cells = 4` the exact two-sided sign test bottoms out at **p = 0.125**,
so the `p <= 0.05` listing filter **can never admit a column** — the diagnostic report's
empty attribution table was arithmetically forced and read as an empirical null. The
script now derives the floor from `n_cells` and, when it exceeds 0.05, states in the
report that no column *can* clear it and that the empty table is not evidence of absent
effects. Both tracked reports regenerated from their tracked JSON; the diff is exactly
and only those lines.

I also corrected my own Session-34 continuity note, which recorded the eight development
context cells as "mirrored across both trajectories." They are not — `t00` and `t01`
carry different context sets (cell index is `(trajectory_index * realizations +
replicate) % 8`). The load-bearing property survives: healthy and fault runs at the same
`tXX_rYY` still share a context cell, which is what makes the contrasts paired.

### Cross-review

Read Codex's `HumanReport34.md` and its two Session-34 chat turns in full. Verified its
self-reported transcript-order recurrence **independently at the git level** rather than
on trust: commit `ee779fb` shows the technical transcript at `+137 / −0` and the
monitoring thread at `+31 / −0`, so nothing pre-existing was deleted, moved or
truncated, and the reapplied turn is the only copy. Repair confirmed clean; I added
nothing to the monitoring thread beyond confirming it in the technical chat.

Standing Lesson 5 held for the **eighth consecutive session**: the startup git snapshot
showed `Codex Session 28` as HEAD while the live repository was at `Codex Session 34`.

## Challenges

- **The 5.8× discrepancy was not visible from any single artifact.** It only appeared by
  comparing a results report against a live measurement in the delivered configuration.
  Reading either alone would have missed it.
- **I nearly "fixed" the wrong thing.** The obvious inference from Finding A is that the
  generator's ramp is a bug. Measuring both ramps against the safety envelope reversed
  that. This is the second session running where simulating a design's consequences beat
  reading it.
- **Staying inside the pre-registration boundary while needing evidence to write a
  sensible rule.** Resolved by separating *scoping* (one cell, fully disclosed, cannot
  determine the outcome) from *selection* (all cells, worst-case rule, runs only after
  approval), and saying so explicitly.

## Files created

- `agents/Claude/Session Summaries/HumanReport35.md`

## Files updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — append-only Session-35 turn (`+274 / −0`, header at the physical tail, four gates asserted).
- `Reproducibility Packet/scripts/screen_structural_separability.py` — sign-test floor
  derived from `n_cells`; forced-empty-table caveat added.
- `Reproducibility Packet/results/structural_separability/pooled_trajectories/structural_separability_screen_report.md`
- `Reproducibility Packet/results/structural_separability/diagnostic_trajectory_only/structural_separability_screen_report.md`
- `README.md` — banner date; append-only running-log entry recording the withdrawal.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md`

## Verification

```text
ramp + amplitude probes        development split only, 32 rollouts
pilot / validation / test read 0
packet suite                   399 passed
tracked report diff            label lines only, rest byte-identical
S34 ladder reproduction        0.1871 vs 0.1867 µε (independent re-run)
transcript append              +274 / -0, header unique, after physical tail
config.json                    absent
protocol P                     stated, NOT run
```

## Claim boundaries

This session establishes that the delivered excitation is mis-set relative to its own
screen, and that A1 admits materially more of it. It does **not** establish where the
detectability threshold lands, which severities become testable, or anything about S
versus C1. It fits no model, freezes no config, and answers no research question.

## Next steps

1. Codex reviews the corrected A2 and either approves or blocks the exact text.
2. On approval, run Protocol P on development mechanics; the outcome selects Case A, B
   or C and determines what the written amendment says.
3. Write the amendment (Slots 11–13, split/manifest contract, exclusion trail, packet
   instructions, Accessible Claim Sheet) for whichever branch P lands in, plus the
   replacement assignment; both agents approve the exact state.
4. Full regeneration from zero, re-audit, then Gate 4.
