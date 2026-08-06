# Progress Report — Codex, Session 80

**Date:** 2026-08-05
**Covers:** my Sessions 73–80 (previous regular report: Session 72)
**Phase:** 2 — Execution
**Written for:** Randy

---

## The short version

The last report ended just before the payload-boundary measurement. That measurement has
now run once, exactly as authorized, and both agents independently approved its stored
result. It found that the structural-damage signal clears the pre-registered detection
rule over progressively fewer damage levels as tip payload increases, and clears none of
the reserved levels at the two heaviest measured payloads. The nearby transition is not
precisely resolved, so the result is a bounded development finding rather than a physical
cutoff.

The project contract now records that limitation through Amendment A2. The amendment
keeps the full experiment and every original success threshold, but requires structural
results to be shown by payload and prevents a blind heavy-payload region from being
misreported as evidence that structural sensing has no value.

The first learned attribution model is also built and jointly approved. It remains
**untrained**. Before training, Claude and I are making the development-only data boundary
executable: which rows may be read, which ten matched fits may run, and what identity every
checkpoint must carry. That small contract has exposed several cases where ordinary green
tests did not cover combinations of malformed inputs. The review remains open on one
reviewer-edited exact state, so no fit has run and no trainer exists yet.

## What the payload measurement established

One authorized invocation spent 127 physical simulation rollouts: one replay check plus
126 planned measurements. The project lifetime Protocol-P-related count is now **278**.
No second invocation is authorized.

The measured development-context sets were:

```text
tip payload   structural severities that cleared the pre-registered rule
25 g          0.35, 0.40, 0.45, 0.50 remaining stiffness
50 g          0.35, 0.40, 0.45
75 g          0.35, 0.40
100 g         0.35
125 g         0.35
150 g         none
200 g         none
```

“None” does not mean the physical signal vanished. It means none of the reserved damage
levels rose above that payload's own doubled-noise threshold. The stored signal distances
remain nonzero. This distinction was important enough that the first amendment draft was
reviewer-edited to say “not testable under this rule,” rather than “does not exist.”

The 125-gram positive margin and 150-gram negative margin both lie inside the instrument's
pre-declared 10% reproducibility band. Therefore the work establishes an empty measured
heavy-payload region, but not a precise 150-gram cutoff, a smooth payload curve, or a
mechanism. Both agents independently audited the exact result document and approved the
same SHA-256 identity. SHA-256 is the standardized fingerprint used here to name exact
bytes, not to make a scientific claim ([NIST Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)).

## What Amendment A2 changes—and does not change

Amendment A2 is now part of both the technical and accessible Claim Sheets. It chooses the
most conservative evidence-licensed path: keep the full payload and damage ladders, report
the structural S-versus-C1 comparison separately by payload as well as pooled, and state
that a structural null transfers only where development screening showed the instrument
could see the reserved signal.

It changes no success threshold, confidence interval, non-inferiority margin, tracking-
improvement bar, seed requirement, safety condition, payload, severity, split, trajectory,
or data identity. It also does not authorize a new dataset, final configuration, or
confirmatory run. This is the purpose of preregistration: change the contract openly when
development evidence reveals a blind spot, without moving the numerical bar after seeing
the future result ([Center for Open Science](https://www.cos.io/initiatives/prereg)).

## The first learned model

The first learned attribution rung is a 39,594-parameter causal temporal-convolutional
network. “Causal” means a prediction at one time can use the present and past but not
future samples. C1 and S use the same architecture and parameter count; the controlled
difference is the sensor information, not model capacity.

The model's checkpoint loader also received a review correction. PyTorch can copy some
compatible tensors before reporting that a state dictionary is incomplete. Loading an
untrusted replacement directly into the live network could therefore leave a mixed model
with the old provenance label. The approved implementation validates on a deep copy and
only then copies the fully accepted tensors into the existing network object, preserving
attached optimizer references. PyTorch's own overview explains that a state dictionary is
the mapping of learned parameters used to save and restore a model
([PyTorch state-dictionary recipe](https://docs.pytorch.org/tutorials/recipes/recipes/what_is_state_dict.html)).

The architecture and loader are jointly approved. The model is still untrained, so none
of this is evidence that structural sensing improves attribution or control.

## Why the development-fit contract is taking several rounds

The contract is intentionally small. It says:

- read only persisted `dev` rows from the delivered dataset;
- fit C1 and S with the same protocol at training seeds 0–4;
- generate no plant or sensor data and spend zero physical rollouts; and
- stamp every checkpoint/result with its development-only authority, data identities,
  suite, seed, source-code identities, and checkpoint identity.

Review has found failure modes at the boundaries between rules, not in the headline plan.
Examples include a duplicate fit being collapsed by a set, an empty batch passing the
point-of-consumption guard, a digest with a terminal newline satisfying a regular-
expression anchor, and a producer returning an empty code-identity mapping that the
consumer refused one step later. Python's `fullmatch` operation is now used where the
contract promises the entire string is the identity
([Python regular-expression documentation](https://docs.python.org/3/library/re.html#re.Pattern.fullmatch)).

This session found another boundary combination. Claude had correctly centralized the
code-identity rule and removed an apparently redundant early label check. But if the label
and path were both malformed, path validation ran first and quoted the whole path-shaped
label; mixed label types could instead fail inside sorting before the shared final check.
The reviewer state restores an early call to the same shared bare-name predicate and adds
a test that combines the fields. The focused suite passes 93 tests normally and under
optimized Python; the full packet suite passes **1,467** tests.

## What is working

- The payload-boundary result is complete, independently reconstructed, and jointly
  approved at its exact development-only boundary.
- Amendment A2 is in force in technical and accessible form, with every original numerical
  success bar preserved.
- The first learned architecture and transactional checkpoint loader are jointly approved.
- The delivered development partition already exists; bounded fitting will not require
  new simulation or physical rollouts.
- The fitting contract now refuses every measured silent authorization leak, and its
  producer and consumer share the same code-identity rule.

## What is not working yet

- The learned model has not been trained, so the project still has no learned attribution
  result and no answer to the central research question.
- The development-fit contract review is open. Claude must owner-review Codex's exact
  reviewer state before that foundation closes.
- No trainer, checkpoint writer, or result writer exists. Those executable bytes require a
  separate two-agent review before fitting.
- Pilot, validation, test, final configuration, and confirmatory work remain untouched and
  blocked.
- The payload measurement did not identify a mechanism and did not persist raw gauge
  traces, so its approved audits begin from stored harmonic coefficient vectors rather
  than re-deriving them from time-series samples.

There is no director-only blocker at present.

## What happens next

Claude's next task is to genuinely review the exact contract state Codex approved. If it
approves those same bytes, Claude can build the bounded trainer and its checkpoint/result
writer. Codex then reviews that complete executable path. Only after both agents approve
the same trainer state may the ten predeclared C1/S development fits run.

That later fit can show whether the implementation learns on development data or expose a
training failure. It cannot set validation-owned thresholds, select a final headline
capacity, become a research result, or open confirmatory work. Those boundaries remain
deliberately separate.

The Slot-8 director verification artifact has no new state in this eight-session stretch,
so this report does not manufacture an update for it.
