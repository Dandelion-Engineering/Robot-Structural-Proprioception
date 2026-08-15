# Summary — Review Boundary and Convergence

**Participants:** Randy, Claude, Codex
**Date Range:** 2026-08-14 — 2026-08-15
**Status:** Concluded — the superseding Review Card method and its non-blocking convergence ladder are implemented and jointly confirmed.

## Outcome

Randy replaced the prior open-ended artifact-review loop with a bounded Review Card protocol:
one full-artifact Round 1, delta-only later rounds, explicit late-blocker rules, at most three
owner-reviewer round-trips, exact same-state approval, and new cards/chats for later versions or
downstream work. The transition ruling preserved the then-current Step-4a state without counting
pre-method exchanges. The first cards then closed Step 4a in Round 2 and Step 4b-i in Round 3.

The rollout also added three durable operating rules: every candidate is authenticated by full Git
blob, raw SHA-256 and physical figures; acceptance criteria name durable properties rather than a
private audit count; and delta responses mechanically identify changed and unchanged regions.
Findings that require an out-of-card repair use an explicit scope proposal, with the reviewer ruling
scope before content and no inherited approval.

## Convergence rule

At Randy's direction, `Escalated` is no longer a blocking terminal outcome. The jointly agreed rule
in `Playbooks/review-cycle.md` and `Review Card/README.md` classifies a max-round disagreement as
factual or judgment in the limit turn. A factual issue gets one precommitted probe and at most one
counterproposal, but the probe creates no new authority. A judgment issue may split once into an
exact narrow candidate with one focused owner-reviewer round-trip. If it still does not converge,
the contested element or whole candidate is withheld fail-closed, both positions are recorded in
`director_requests.md`, and all other work continues. Later reinstatement requires a new candidate
and Review Card. The mechanical ceiling is at most two further agent sessions for a factual issue
and three for a judgment issue, measured from the classification turn.

Codex reviewed the written sections in Session 140 and confirmed that they faithfully implement all
five reconciliations. The historical escalation text remains only as explicitly superseded context.
No scientific or downstream authorization changed in this process chat.
