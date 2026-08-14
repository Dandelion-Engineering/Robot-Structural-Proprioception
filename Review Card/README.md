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

For a review already in progress when the protocol arrived, the director's transition ruling keeps
the then-current candidate, settled findings and open ledger, while starting the new round count at
that state. Earlier exchanges do not consume the new three-round limit. The initial transition card
is `Slot-8 Step-4a Connection-Record Design.md`.
