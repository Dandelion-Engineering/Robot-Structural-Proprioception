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
