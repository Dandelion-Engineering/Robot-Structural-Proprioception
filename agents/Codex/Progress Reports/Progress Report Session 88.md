# Progress Report — Codex, Session 88

**Date:** 2026-08-07
**Covers:** my Sessions 81–88 (previous regular report: Session 80)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The last report ended with an untrained attribution network and an open contract for the
first development fit. Eight Codex sessions later, the contract and trainer are approved,
the first ten matched development fits have run once, and their exact ledger and read-back
are jointly approved.

The network learned the training examples. At the one fitted size, however, the version with
four added structural-sensing channels scored slightly worse on average than the conventional
version, and the result moved sharply across the five training seeds. Those numbers are from
the same examples used to train the network. They are useful evidence that the executable
works and that the experiment has a stability problem; they are not evidence that structural
sensing helps or hurts on new data.

The next measurement is therefore a small development-only width sweep. Its design now maps
how each suite's own training score changes as the network gets wider. It deliberately does
not claim that width isolates “capacity”: changing width also changes how a network trains
within a fixed 20-epoch budget. The design is reviewer-edited and approved by Codex, but
Claude's same-state owner re-review is still open. No sweep program, plan, fit, checkpoint, or
later-role read is authorized yet.

## What the first learned fit established

Claude ran exactly ten fits in Session 84:

```text
sensor suites             C1 and S
training seeds            0, 1, 2, 3, 4
examples per arm          152 development windows
network size              39,594 trainable parameters
epochs                    20
physical simulation       none
new data generation       none
```

The same 152 examples were used both to fit and to score each arm. This is called an
**in-sample** read: it checks whether the machinery can learn the material it was shown, not
whether it will generalize to unseen examples.

Both suites beat simple in-sample reference rules. Their five-seed mean macro-F1 scores were:

```text
C1                         0.682
S                          0.650
paired S minus C1         -0.032
paired seed-to-seed SD     0.150
project success bar        0.050
```

“Macro-F1” gives each of the four fault classes equal weight instead of letting the most
common class dominate. The paired average is mildly negative, but its seed-to-seed spread is
about three times the effect size the final experiment is designed to detect. Two seeds put S
above C1 and two put it well below. That instability is the decision-relevant finding from the
read-back.

The boundary is just as important as the number: these are training-set scores with no OOD
examples and no held-out role. They do not select a model size, set a threshold, support a
sensor-suite conclusion, or answer the project's central question.

## Why the read-back took four more sessions

The fit itself was cheap. Most of the work was making sure the stored result could not quietly
mean more than it earned.

The review cycle hardened three layers:

- the trainer refused stale output directories instead of mixing checkpoints from different
  code states;
- the result ledger bound every arm to its data, schedule, training settings, code identities,
  and checkpoint identity; and
- the read-only analysis derived its class census, reference rules, losses, and paired metrics
  from the approved ledger rather than from hand-copied numbers.

The analysis tests were then probed by deliberately breaking the analyzer in narrow ways. A
synthetic fixture first hid a “pick the smallest class” error because every class count was
equal. After that was repaired, it still hid a “pick the last class” error because its counts
rose in order. The final fixture uses counts `(1, 2, 4, 3)`, so the correct majority is neither
first nor last and every published baseline number stays unchanged. Both agents now explicitly
approve that exact state.

This work did not change the learned result. It changed how confidently a future reader can
reproduce and audit what the result says.

## The width-sweep design

The proposed development grid is:

```text
channels             16      24      32      40      48
parameters        10,586  22,786  39,594  61,010  87,034
receptive field    1,023   1,023   1,023   1,023   1,023
```

The 32-channel arms are the approved fits and remain read-only. The other four widths would
add forty curve fits. Before those can run, a new width-parameterized fit path must reproduce
two approved 32-channel arms—one C1 and one S—bit-for-bit. Those two compatibility fits make
the maximum 42 fits and 42 scratch/new checkpoints, still with zero simulation rollouts.

The design carries several safeguards that were absent from its first draft:

- preserve the absolute C1 and S curves, not only their difference, so C1 worsening cannot be
  mistaken for S improving;
- emit exact descriptive observations, never a machine-generated causal verdict;
- exclude near-perfect pairs where arithmetic itself prevents a bar-sized difference;
- bind a deterministic zero-fit plan before execution;
- distinguish ten reused anchor arms from forty newly completed arms;
- reject every partial run as a complete curve; and
- restart retries in a fresh root rather than mixing unapproved partial checkpoints.

The most important limitation remains: a fixed-epoch width sweep changes both network size
and width-dependent training behavior. It can show that the observed scores are sensitive to
width under this protocol. It cannot prove why.

## What is working

- The first learned-model fit ledger and its read-only analysis are exact-state approved.
- Only development rows were read; pilot, validation, and test outcomes remain untouched.
- The trainer, checkpoints, result ledger, and analyzer preserve a complete provenance chain.
- The proposed sweep remains inside the Claim Sheet's smallest capacity rung and holds the
  1,023-sample receptive field fixed.
- The review cycle continues to find boundary defects before execution rather than after a
  result has to be interpreted.
- Project lifetime Protocol-P-related physical execution remains **278**; none of these eight
  Codex sessions added a rollout.

## What is not working yet

- The project still has no held-out learned-attribution result and no answer about whether
  structural sensing improves attribution or control.
- Five seeds are visibly unstable at the fitted size; the later confirmatory seed-count
  decision must address that warning, but this in-sample spread is not itself a power study.
- The capacity design is not frozen until Claude genuinely re-reviews Codex's exact edits.
- No capacity executable, zero-fit plan, or sweep result exists.
- Calibration, thresholds, final capacity selection, final `config.json`, confirmatory data,
  and the Slot-8 verification artifact remain unbuilt or blocked at their later gates.

Your Claim Sheet review in `director_requests.md` is still open. It is deliberately
non-blocking, so nothing above is waiting on you, but it remains the project's longest-running
director check that the contract still matches your intent.

## What happens next

Claude's next exact task is to re-open the reviewer-edited capacity design and the narrow
correction to Claude's own Session-88 progress report, then explicitly approve or contest
those states.

If the design closes unchanged, that authorizes writing the sweep executable and tests only.
The executable then receives its own review. A deterministic zero-fit plan is produced and
reviewed after that. Only a later, separate joint authorization can permit the two
compatibility fits and forty curve fits.

The Slot-8 director verification artifact has no new state in this eight-session stretch, so
this report does not manufacture an update for it.
