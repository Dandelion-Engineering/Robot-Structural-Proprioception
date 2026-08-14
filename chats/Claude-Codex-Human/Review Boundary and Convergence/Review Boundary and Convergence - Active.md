# Review Boundary and Convergence

**Opened:** 2026-08-14

**Participants:** Randy, Claude, Codex

**Purpose:** Implement and test the director's superseding review method, record rollout problems,
and keep human triage separate from artifact-specific review chats.

---

**Codex (Session 134, 2026-08-14 12:22 PDT):**

Randy has directed both agents to replace the prior open-ended review loop with the following
method:

> ## Review boundary and convergence
>
> Before review begins, the owner creates a Review Card (in a new Review Card folder in the root
> directory) naming the candidate state, artifacts and sections in scope, purpose, acceptance
> tests, blocking-severity definition, and explicit exclusions or downstream gates. The candidate
> must be stable enough to accept, reject, or return; open-ended co-design happens before formal
> review.
>
> Round 1 is the only full-artifact review. The reviewer records all reasonably discoverable
> findings in one numbered ledger and does not stop at the first blocker.
>
> Round 2 and later are delta-only. They verify recorded findings and regressions introduced by the
> response. Unchanged, previously reviewed material is not re-audited from scratch.
>
> A new pre-existing blocker after Round 1 must be marked LATE-BLOCKER, must be genuinely capable
> of invalidating the scoped purpose, and must state why it was missed. A second late blocker, or
> any new blocker after Round 2, triggers human triage or a split. Non-blocking late findings become
> tracked follow-ups.
>
> A review has at most three owner-reviewer round-trips. The limit never forces approval. At the
> limit the outcome must be Approved, Approved with Follow-ups, Revisions Required, Split/Redesign
> Required, or Escalated.
>
> Once both agents approve the scoped candidate, that review closes. Later amendments,
> implementation work, data gates, new sections, or new versions receive new Review Cards and new
> chats. They do not keep the concluded review active.
>
> Reviewers may directly apply mechanical corrections. Substantive scientific, architectural, or
> interpretive changes are proposed as findings or patches for the owner to integrate, unless
> ownership is explicitly transferred.

Randy also directs us to conclude the overbroad `Phase 2 Integration and Config Freeze` chat. New
chats must be scoped to subjects and concluded when those subjects are done; “all of Phase 2” is not
a sufficiently bounded subject. This shared chat stays active so Randy can receive feedback on the
new method and see any problems that arise from it.

**Implementation sessions.** The protocol is appended to `Playbooks/review-cycle.md` and explicitly
supersedes the rest of that playbook. It is implemented in **Codex Session 134**. Claude Session 134
ended before Randy issued this direction, so it is not backdated; Claude's implementation session
is **Claude Session 135**.

**My feedback.** This is a strong correction to the failure mode the current project exposed. A
Review Card makes the unit of approval explicit; one complete Round-1 ledger prevents serial
discovery from masquerading as convergence; delta-only later rounds stop unchanged text from being
re-litigated; and the terminal outcomes preserve the right to block without allowing a review to
become permanent co-design. Separating later implementation and data gates into new cards/chats is
especially important here, because the old Phase-2 thread accumulated unrelated review histories
and made “same review” ambiguous.

**Immediate rollout problem — ESCALATED for human triage.** The active Slot-8 Step-4 connection-
record design predates this protocol, has no owner-created Review Card, and my Session-134 response
would have been its eighth alternating round. It has therefore already exceeded the new three-
round maximum, and the latest issue is another blocker discovered after Round 2. I am not treating
the new rule as retroactive approval. The legacy review's outcome is **Escalated**: its current
reviewer-approved candidate is blob `425ce0118bddc44daccfa69b19362aec6ea70d00`, but Claude has not
approved those bytes and Step 4a is not closed. Before more review occurs, Randy should choose
whether Claude integrates the final patch and opens a new, narrow Review Card for a bounded
delta/acceptance review, or whether the design/test-contract work is split. No 4b implementation or
scientific read is authorized meanwhile.

Two interpretation points may need refinement as we test the method:

1. “Mechanical” versus “substantive” should be judged by effect, not edit size: a small change that
   alters behavior, evidence, architecture, scientific meaning or authorization is substantive.
2. A Review Card's exclusions cannot shield an integration defect that genuinely invalidates its
   stated purpose. Such a defect is still a blocker; after Round 1 it must satisfy the LATE-BLOCKER
   rule and explain the miss.

I will keep this chat active and report concrete problems here rather than silently inventing
exceptions.

— Codex

---

**Codex correction (Session 134, 2026-08-14 12:32 PDT):**

Randy has clarified the transition: my immediate escalation ruling above was wrong because it
applied the new three-round limit retroactively. **Withdraw that escalation.** We will take the
Step-4a review exactly as it stood when the new method arrived and start the new method from there;
the earlier exchanges do not consume its round limit.

The transition now has a Review Card at `Review Card/Slot-8 Step-4a Connection-Record Design.md`
and a narrow active owner-reviewer chat at
`chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/Slot-8 Step-4a Connection-Record Design - Active.md`.
Codex's Session-134 full-artifact review is Round 1, with one numbered open blocker (formerly DE).
Claude's response will be the owner half of new-method round-trip 1, and Codex's next review will be
Round 2 / delta-only.

The first concrete rollout lesson is now recorded: the protocol needs an explicit migration rule
for reviews already in progress. That rule has been added to the playbook. The method chat remains
active for further feedback or problems.

— Codex

---
