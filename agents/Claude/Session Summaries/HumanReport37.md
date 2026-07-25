# Human Report — Claude Session 37

**Current date and time:** 2026-07-25 16:44 PDT
**Phase:** Phase 2 — Execution
**Session role:** Answer Codex's Session-36 block by writing one clean, executable Protocol P v2
**Final config state:** **UNFROZEN** (`config.json` absent — verified this session)
**Governing decision:** `BLOCK_CONFIG_FREEZE_PENDING_PRECONFIRMATORY_BUILD_AND_VALIDATION`
**Session decision:** `AMENDMENT_A2_PROPOSAL_V4`
**Rollouts spent:** **0**

---

## Summary

### What I walked into

Codex reviewed my Session-36 amendment proposal (v3) and blocked it with
`BLOCK_AMENDMENT_A2_PROPOSAL_V3_PENDING_BRANCH_COMPLETE_SELECTION_AND_CELLWISE_NULL`.
That block was, in my judgement, entirely correct on both counts, and it also
*approved* five of the six choices I had explicitly handed to it for arbitration.
So the session had a clear shape from the start: accept the decisions, fix the two
structural defects, and pin the four execution details Codex said were still
analyst-chosen rather than specified.

The two blocking defects were real and I had not seen either:

1. **Stage A could stop before the ladder ever ran.** My v3 made a candidate
   ineligible if its detection statistic at the mildest damage level fell below a
   threshold `T1`. If *every* candidate fell below it, there would be no selected
   candidate, so the later stages would never run — and yet the protocol would
   have reported "nothing passes anywhere," which is a claim about all ten damage
   levels that no measurement had been taken on. Since I had explicitly removed the
   monotonicity assumption, I had no right to infer the unmeasured levels from the
   mildest one. Codex's repair drops the eligibility cutoff, always runs the ladder,
   and adds a separate terminal branch for the case where every candidate fails a
   hard safety gate.
2. **A pooled noise estimate is not a context-robust one.** My Stage C pooled 60
   healthy-vs-healthy distances across four background conditions into a single
   95th percentile. A pooled percentile can sit below the noisiest condition's own
   percentile, so a damage level could be declared testable against a threshold
   that under-covers the condition that actually binds. Codex offered two repairs;
   I took the per-condition one.

### What I set out to do, and what actually happened

The plan was to accept, repair, pin, and post. The pinning is what produced the
session's findings — three of them, none of which I expected when I started.

**Finding F — the number I had committed as `T1` was the five-sigma point of the
wrong random variable.** Codex asked me to pin the exact Stage-0 command and to
define what one sample of the null actually is. Doing that forced me to state, in
one line, what `T1` was the null *of* — and the answer was: not the quantity it was
being compared against. Protocol P's statistic is a **difference** between two
runs' harmonic coefficient vectors. The number I committed (`0.4388`) is the
five-sigma point of the norm of a **single** run's vector. Measured directly on the
sensor model at the protocol's own window, with 200 noise-only windows paired into
100 independent pairs: a single window gives mean `0.1957` and five-sigma `0.4388`
(reproducing last session's audit to four decimals, so the harness is sound); the
*difference* gives mean `0.2787` and five-sigma `0.6526`. The ratio of means is
`1.424` against a theoretical `sqrt(2) = 1.414`, which is the confirmation that the
two are exactly the objects I now think they are.

This is the third yardstick error in three sessions and the same species as
Session 36's Finding D. What makes it worse than a wrong number is that it is not
fixable by substituting `0.6526`: that value is the null for an **unmatched**
difference, while the protocol's Stage A and Stage B comparisons are **matched** on
the random-number seed by design, so the sensor noise largely cancels out of them.
The honest conclusion is that a matched difference has **no useful sensor-only
threshold at all**, and `T1` had to be retired as a bar rather than corrected.
Codex's own repair had already stripped `T1` of its ranking role; this removes it
from the comparison entirely. Where it *is* legitimate is as a reference for
Stage C, whose healthy-vs-healthy pairs are unmatched by construction — so that is
the single job I gave it.

**Finding G — a check that came back against my hypothesis.** Having been wrong
about a threshold's configuration twice, I re-measured the difference null at the
thermal excursion the delivered runs *actually* experience rather than the
deliberately aggressive 3 °C the committed analysis assumes, fully expecting to
find the same error a third time. I did not. The realized excursion over the
analysis window is `0.0000 °C` in the isothermal background and `0.5113 °C` in the
warm one — the assumption is six times the worst real value — and it makes no
difference whatsoever: the difference null's 95th percentile is `0.391`, `0.398`,
`0.396` at 0 °C, 0.5113 °C and 3 °C respectively. The reason is worth keeping:
thermal cross-sensitivity is deterministic given a temperature profile, and both
runs in any difference share their profile, so it **cancels exactly**. The sensor
pathology the project modelled most carefully cannot inflate this statistic's
noise. I reported this as a finding rather than quietly dropping the check,
because a check that fails to confirm your expectation is still information.

**Finding H — a safety gate everyone had already approved kills 15 of 24
candidates with arithmetic.** The probe-torque admissibility gate is
`F_peak × 2 × link_length ≤ 0.60 × torque_limit`. With the project's own constants
that is `F_peak ≤ 0.15 N` exactly. Five of the eight pre-registered probe
amplitudes are above it, so 15 of the 24 candidates are inadmissible before a
single simulation runs. Two details mattered enough to pin: the comparison must be
written `≤` rather than `<`, because 0.15 N lands exactly on the boundary and both
sides round to the identical double-precision value — `<` would silently discard
the strongest admissible probe; and Codex's own earlier screen defaults to exactly
these three amplitudes, which I take as independent corroboration rather than
coincidence. The consequence is that the screen's worst case drops from 288
rollouts to 108.

**Finding I — the terminal branch Codex asked me to define is empirically almost
empty.** Before writing a `NO_ADMISSIBLE_PROBE` branch I checked whether it was a
live risk, and realized the delivered development runs *are* one of the 24
candidates already evaluated in all four background conditions at three damage
levels. Every measurable safety gate passes with large margin: peak joint speed
`0.784` rad/s against a limit of `8.0`; peak joint angle `0.397` rad against `2.5`;
peak true strain `6.13` µε against `400`; zero saturated steps; no safety flags at
all, on all twelve runs. The branch stays defined, because branch-completeness is
not about likelihood, but it is a formality. The honest counterweight is that
Session 35 found 0.30 N violently unstable, so the dynamics turn sharply nonlinear
somewhere between 0.15 N and 0.30 N, and the dynamic gates may well bind at the top
of the admissible band even though they are inert at the bottom.

### The thing I think matters most this session

While computing the revised odds, a consequence surfaced that neither agent had
raised, and it is not a technical defect — it is a design problem that the *most
likely outcome* creates.

With the probe capped at 0.15 N, the strongest signal ever measured
(`0.552`, under friendly single-condition conditions at the more severe of the two
training damage levels) sits close to the ceiling of what can be selected, while
the noise threshold plausibly lands near `0.8`. Damage response grows superlinearly
with severity, so the severe end of the reserved ladder is where the chance lies.
That makes the most likely result: **only severe damage levels are testable — and
every damage level reserved for training is mild.**

If that lands, the model would be trained exclusively on damage its sensors cannot
distinguish from noise, and then graded on damage they can. A failure would be
uninterpretable: we could not separate "structural sensing does not help" from "the
model never saw a detectable example." That is a hypothesis-failure reading the
project would not be entitled to draw.

I deliberately did **not** pick a fix. I laid out three options — accept and report
it as a coverage-bounded result; rebalance damage levels across the splits; or
narrow the claim to what turns out testable — and flagged that option two is
dangerous in a specific direction, because choosing which severities land in the
final test set partly on measured detectability selects that set toward
detectability, and that bias favours the hypothesis I am supposed to be testing.
What I did insist on is the **timing**: whichever option we take must be fixed
*before* the ladder is measured. Afterwards, any choice is made in full knowledge
of which severities passed, and the second option in particular becomes
indefensible. That is the entire reason I raised it in this turn rather than in the
one that reports results.

### Challenges, and how they were handled

- **The temptation to quietly substitute a corrected number.** Finding F would have
  been much less embarrassing to report as "T1 is 0.6526, not 0.4388." That would
  have been wrong, because the matched comparison the protocol makes has no
  sensor-only null at all. I wrote the harder and more damaging version.
- **Choosing between two repairs Codex offered, where one favours me.** Its
  per-condition rule and its scalar rule are not equivalent: the scalar form
  strictly implies the per-condition form, so the one I picked passes at least as
  many damage levels. I proved the implication, stated plainly that I chose the
  laxer one, gave the reason I think it is the coherent comparison (the noise that
  obscures a signal in a given condition is that condition's own noise), supplied
  the physical mechanism from Finding G for expecting genuine condition-to-condition
  differences, committed to reporting the stricter form as a pre-declared
  sensitivity, and offered to switch without argument. This is Standing Lesson 13
  applied as designed.
- **Knowing when to exceed the brief.** Codex asked for a replacement that pins
  "only these repairs." One change I made is not a requested repair: raising the
  healthy replicate count per condition from 6 to 8. The per-condition repair makes
  the threshold an order statistic of 15 dependent distances drawn from only 6
  independent runs — at that size the 95th percentile is essentially the maximum, so
  one unlucky pair sets a condition's bar. Eight runs gives 28 pairs and costs 8
  extra rollouts, about four minutes. I flagged it explicitly as the one unrequested
  change, gave the cost, and said I would hold at 6 without re-arguing if Codex
  considers it scope creep.

### Decisions I made

1. Accept all six of Codex's arbitrated decisions, including the retraction of my
   Session-36 claim that ordinary-trajectory rows "can only shrink" the contrast.
   Codex is right: a per-sample mechanics block does not bound what a windowed
   learned estimator extracts from 768 samples, nor the finite-sample direction of
   a difference. I withdrew the claim and wrote the replacement wording.
2. Retire `T1` as a threshold; keep it as Stage C's validity tripwire only.
3. Pin the per-condition noise rule as operative; report the scalar form as a
   pre-declared sensitivity.
4. Keep the pre-registered 24-candidate grid intact and report the 15 arithmetic
   exclusions as *reporting*, not amending.
5. Move Stage A's third safety condition from the interior damage level to the most
   compliant one on the whole ladder — same rollout cost, strictly better coverage
   of the compliance range the selected probe will later be driven through.
6. Give Protocol P a screen-private random-number namespace rather than reusing
   development seeds, so no screen rollout shares randomness with any dataset row.

### Reasoning paths explored

The most productive one was refusing to write the `NO_ADMISSIBLE_PROBE` branch
until I knew whether it could actually happen — which led to realizing the
delivered data already *is* a Stage-A evaluation of one candidate, and turned a
speculative branch into a measured one. The least productive-looking one, the
thermal re-check, produced Finding G, which is a genuine property of the statistic
worth putting in the report. The one I am most wary of is the odds revision: it
rests on single-condition measurements from a previous session and on the
*direction* of a table whose magnitudes belong to a different configuration, and I
said so explicitly rather than importing those magnitudes.

### Insights gained

- **A threshold has to be the null of the operation you perform, not of the
  quantity you perform it on.** Three sessions of threshold errors all reduce to
  importing a number whose defining operation differed from the one in use.
- **Common random numbers do not just reduce noise; they can make a whole class of
  threshold meaningless.** Matching seeds cancels the sensor term, so there is
  nothing left for a sensor-only bar to bound.
- **Writing a specification so a stranger can execute it is a defect-finding
  technique, not a documentation chore.** All four of this session's findings came
  out of the act of pinning, not out of reviewing.
- **The most valuable thing a protocol design can produce is a decision that must be
  made before the measurement.** Finding the training-coverage problem now is worth
  more than any of the numbers, because in two sessions' time it would have been
  unfixable without bias.

### Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended the Session-37 turn (`AMENDMENT_A2_PROPOSAL_V4`, one clean Protocol P
  v2). Verified `+505 / −0`, header unique at line 5129, after the 5127-line
  pre-write boundary, prior bytes a byte-identical prefix.
- `README.md` (root, Live-Run) — one running-log entry, `+2 / −0`.
- `agents/Claude/Session Summaries/HumanReport37.md` — this report.
- `agents/Claude/README.md` — workspace index refreshed.
- `agents/Claude/Summary of Only Necessary Context.md` — fully rewritten.
- Not committed (scratchpad, recreate as needed): `probe_s37_pins.py`,
  `probe_s37_thermal.py`, `s37_pins.json`, `s37_thermal.json`, `turn_s37.md`,
  `append_turn.py`.

### Verification performed

- Packet suite scoped to `Reproducibility Packet/tests`: **399 passed** in 9.63 s.
- `config.json` confirmed absent at both candidate paths.
- Codex's Session-36 transcript append independently checked at the git level:
  `+145 / −0` — nothing deleted, moved or truncated. **Clean-append streak: three.**
  No entry added to the monitoring thread; the duty is to flag recurrences, and one
  clean check is already on the record.
- The startup git snapshot lagged reality again (it showed `Claude Session 34` as
  most recent when `Codex Session 36` was already `HEAD`). **Ten consecutive
  sessions.** I verify live state before trusting continuity, which is why this was
  caught rather than acted on.
- Seed derivation read from source (`utils/gate3_assignment.py:663-696`) rather than
  from my own notes; confirmed `utils/cable_plant.py` contains no random-number
  generator at all, so a rollout's stochastic identity is exactly
  `(sensor_seed, pair_id)`.
- Non-development payloads read: **0**. Confirmatory identities generated: **0**.

### Cross-review

Read Codex's `HumanReport36.md` and its complete Session-36 transcript turn. One
note: that report repeats `0.4388` as "the coherent vector-8 five-sigma threshold,"
which Finding F now corrects. Per the project's forward-propagation rule I have
**not** asked Codex to revise the earlier report — the correction lives in my
Session-37 turn and will carry into the Technical Report.

### Next steps

1. **Codex owns the next turn.** Four things need its word: the Stage-C rule choice,
   the 6→8 replicate change, whether Finding H's pruning counts as reporting rather
   than amending, and the open question about training coverage.
2. **Do not run Protocol P** until that settles.
3. If v4 is approved, the order is: implement Stage 0's new packet script → run
   Stages A/B/C (168 rollouts, ~78 min) → Codex reviews implementation, result and
   branch → written Amendment A2 → replacement assignment → full regeneration.
4. No progress report is due; my next regular one is Session 40, unless I write the
   approving turn on the written amendment first.

---

**Bottom line for the director:** no experimental result moved this session, and
none was supposed to. The protocol that will decide which damage levels the
experiment can legitimately test got its third measuring-stick correction, lost a
threshold that could not mean what it claimed, shed half its compute cost to a
safety limit nobody had done the arithmetic on, and — most importantly — surfaced a
design problem that would have been unfixable without bias if it had been found two
sessions later. The final test data remain untouched.
