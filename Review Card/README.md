# Review Cards

This root folder holds the Review Card that an artifact owner creates before each formal review
under the superseding protocol in `Playbooks/review-cycle.md`.

Each card names the candidate state, artifacts and sections in scope, purpose, acceptance tests,
blocking-severity definition, and explicit exclusions or downstream gates. A later amendment,
implementation, data gate, new section or new version receives a new card and a new subject-scoped
chat; it does not extend a concluded review.

For every tracked candidate state, the card records the full Git blob id, raw SHA-256 and physical
size/line-ending figures, and its writer verifies the blob id with `git cat-file -t` before the card
governs review. Acceptance criteria name durable artifact properties or outcomes; private audit
instrument counts belong in the round evidence, not in the criterion itself. In a delta response,
the owner names both what changed and what remained byte-identical, with machine-checkable evidence
where practical, so later rounds can remain genuinely delta-only.

If a review finding requires a repair outside the card's declared artifact list, the owner records
the added artifact as a proposed scope expansion rather than answering partially or widening the
candidate silently. The response authenticates the new state, names its prior approved or baseline
state, explains why the card remains bounded, and offers revert or deferral. The reviewer rules on
scope before content. An accepted added artifact joins the current candidate without inheriting its
earlier approval; a rejected or overbroad expansion returns to its prior state and moves to a new
card. The round limit and late-blocker rules do not reset.

For a review already in progress when the protocol arrived, the director's transition ruling keeps
the then-current candidate, settled findings and open ledger, while starting the new round count at
that state. Earlier exchanges do not consume the new three-round limit. The initial transition card
is `Slot-8 Step-4a Connection-Record Design.md`.

## Convergence at the round limit

`Escalated` is not a terminal outcome. A card that reaches its round limit still in disagreement
runs the convergence ladder in `Playbooks/review-cycle.md` instead, and the card is where that
ladder is recorded.

The turn that first finds the review at its limit names the residual issue, classifies it factual
or judgment, states its own position, and — for a factual issue — proposes the decisive probe and
the binding outcome map, all in that same turn. Differing classifications make the issue judgment.
A factual issue is settled by one precommitted probe recorded in the card before it runs, with one
counterproposal permitted; the probe may spend no gated or otherwise unauthorized resource, and an
inconclusive result becomes judgment. A judgment issue splits exactly once, into a narrow card
carrying both positions verbatim, which permits one owner handoff, one reviewer response and one
owner re-review, cannot split again, and inherits no fresh round allowance. Uncontested material
closes only as an exact candidate state both agents approve.

If that focused round-trip does not converge, the contested element is withheld: a capability is
left refusing, a permission left denied, prose withheld rather than softened, and on an append-only
artifact the withholding is a forward correction or an omission from the next state, never a rewrite
of history. The terminal outcomes are `Approved — Contested Element Withheld` and `Withheld —
Contested Candidate Not Adopted`. The card and `director_requests.md` keep both positions and the
withheld state as a standing tracked item; the director notice is non-blocking, and reinstatement is
a new candidate under a new card rather than a retroactive approval of the withheld bytes.
