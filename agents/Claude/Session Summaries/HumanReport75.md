# Claude — Human Report, Session 75

**Date and time:** 2026-08-04 20:52 PDT
**Phase:** Phase 2 — Execution
**Physical rollouts spent this session:** **0.** Project lifetime Protocol-P-related total remains **278**.

---

## Summary

This session did one thing: it wrote **Amendment A2** — the change to the project's
contract that the payload measurement has been pointing at for fifteen sessions — into
both the technical `Claim Sheet.md` and the plain-language `Accessible Claim Sheet.md`,
and handed the exact two-file state to Codex for review.

A2 was assigned to me by Codex in its Session 74, under the default writer convention.
Both agents had already agreed the direction (**Option C**) in our Session-74 turns, so
this session was not a design decision; it was the writing, plus the checking that the
writing says only what the evidence supports.

**Nothing about the success bar changed.** Every threshold, interval, margin, and seed
requirement in the contract stands exactly as pre-declared, and A2 says so explicitly so
that a reader cannot mistake an amendment for a loosening. What changed is the pre-declared
*shapes* — what a positive means, what a negative means, and what neither means — plus one
reporting requirement.

## The problem A2 exists to fix, in one paragraph

The arm carries a small weight at its wrist. The contract treated that weight as a
nuisance a real effect should survive. The measurement that ran in Codex's Session 73
showed it is not a nuisance: it is the strongest single influence on whether the structural
damage signal exists at all. The set of detectable damage levels never grows with payload
and shrinks from four to zero across the measured range, and at the two
payload weights reserved for the project's **final test split** there is no detectable
signal left at any damage level the project planned to test. Had the confirmatory
experiment been run and reported pooled across payload, it would very likely have produced
"structural sensing didn't help" — and we would have published a statement about how much
the arm was carrying while presenting it as a statement about structural sensing.

## The one new inference in the amendment

Everything else in A2 restates approved results. This does not, and I flagged it to Codex
as the thing to push on:

```text
The project's role-coverage read gave validation and test one detectable damage level
each.  That read came from the executed screen, and THE SCREEN RAN ONLY AT 0.000 kg
AND 0.050 kg — and the assignment reserves BOTH of those weights for DEVELOPMENT.

  validation reserves 0.100 / 0.125 kg   its one severity, 0.40, is sub-threshold at both
  test       reserves 0.150 / 0.200 kg   its one severity, 0.35, is sub-threshold at both

Measured at the weights each split actually carries, the coverage is 0 / 0 / 0 / 0.
```

I sourced the weight-to-split map from the assignment configuration file directly rather
than from either result artifact, so the claim that development owns both screened weights
does not depend on the artifact that motivated the question.

## The second finding: my own S74 disclosure did not go far enough

In Session 74 I established that the *boundary* of the empty payload region is unresolved,
and Codex accepted that disclosure. That analysis asked what a single measurement flip does
to **the outcome**. It does not ask what a flip does to the **role-retention sentence**, and
those are different questions, because the classifier's rule for "some mass is empty" fires
before the rule about roles and hides it.

Re-run this session against the persisted artifact:

```text
CHEAPEST OWN-ROLE RUNG PER MASS, AS PERCENT OF THAT MASS'S OWN THRESHOLD
  0.025 pilot  0.60   -18.233%          0.100 val   0.40    -5.746%   <- inside the band
  0.050 dev    0.50    -5.013% <- band  0.125 val   0.40   -17.605%
  0.075 pilot  0.60   -50.305%          0.150 test  0.35    -4.141%   <- inside the band
  0.200 test   0.35   -22.583%
```

Three of the seven role losses sit inside the same 10% reproducibility band the protocol
had declared untrustworthy *before* the measurement ran. A single well-shaped flip at any
one of them would make that mass retain its role — while changing neither the outcome nor
the Option-B cap, which is exactly why my Session-74 sweep filed all three under "well
shaped and unchanged" and said nothing about them.

So A2 writes the **aggregate** sentence and not the universal one: *no measured mass
retained its own reserved severity, and at three of the seven the margin was inside the
instrument's own reproducibility band.* Nothing about which options are licensed moves —
Option B still breaks at the first mass, 18.2% out, well outside the band, and I verified
that no combination of in-band flips repairs it. This only stops the amendment from
asserting a sharper universal than the instrument supports.

**This is the third consecutive session in which the thing worth reporting was a limit on
our own claim rather than a defect in the artifact.** I think that is the correct shape for
a project at this stage, but it is worth naming rather than letting it look like caution
for its own sake.

## The correction A2 carries into the contract

A2 also corrects an operational expectation both agents have carried since Session 33.

Both continuity files say the delivered 472-reservation development dataset is "slated for
full regeneration from zero after A2." That was true when A2 was expected to **add a
severity band**: the data generator expands fault settings in a fixed order (healthy →
structure → actuator → sensor, per split) and derives each run's seed from its ordinal, so
inserting a new structural severity renumbers and reseeds everything after it.

**Option C inserts nothing.** No reserved severity moves, no payload level moves, no split
assignment moves. So A2 shifts no seed ordinal and by itself invalidates no already-generated
data, requires no `archive/` move, and performs none. I wrote that into the amendment rather
than only into my notes, because it is a statement about what the contract does and a future
reader should not have to reconstruct it from two agents' private files. If the delivered
set is superseded, it will be for some other reason, under its own authorization, with its
own exclusion trail — and I asked Codex specifically to block this if it sees a reason on
the assignment or config side that I do not.

## What A2 says, section by section

| Section | What it does |
|---|---|
| A2.1 | The four development measurements in order, the seven-mass table, and the three things in it that are the amendment — including the 0/0/0/0 recount and the scope statement that all of it is one development context |
| A2.2 | Why it changes the path: payload was treated as a generalization axis and is in fact the determinant |
| A2.3 | Option C adopted; A and B shown unavailable against the frozen document's own licensing clause; the no-regeneration correction |
| A2.4 | Slot 11 — bars unchanged, stated as unchanged; a scope bound on the *sentence* a success licenses |
| A2.5 | Slot 12 — a structural null is a hypothesis failure only where the screen found signal; this makes our clean negative **harder** to claim |
| A2.6 | Slot 13 — the new payload-bounded non-transfer shape, four parts, structural family only |
| A2.7 | Slot 7 — the confirmatory structural comparison is reported stratified by payload as well as pooled; explicitly a reporting rule, no new bars |
| A2.8 | Six claim-strength limits binding on A2, the Technical Report, and the Accessible Piece |
| A2.9 | What approving A2 does not authorize — named inside the contract so approval cannot be read as reaching downstream |

Both files also gained an `# Amendments` section with a numbering note recording that **A1
is not in the Claim Sheet** — it amended the schema and is recorded there — and both opening
sections now point a reader at the amendments before the slots, since an amendment that
governs a slot is useless if the reader stops at the slot.

## Challenges, and how they were handled

**The temptation to write the stronger sentence.** The measured result reads cleanly as
"the empty region starts at 150 g" and "no payload level keeps its own damage levels." Both
sentences are sharper than the instrument, and both were available. The discipline that
caught them is not judgment; it is that the protocol had fixed a reproducibility band
*before* the measurement existed, so checking a sentence against it is arithmetic rather
than taste. Every claim in A2 that sits inside that band is labelled.

**Not re-litigating the direction.** Six earlier versions of A2 were blocked, and the
instinct to reopen the option choice was real. It is settled: the frozen extension document
pinned in advance which outcome licenses which option, the outcome is `X_CASE_EMPTY`, and
both agents named Option C in Session 74. I wrote what was settled and confined my own
judgment to the two places I flagged as judgments.

**Keeping the two documents genuinely in sync rather than nominally.** The plain-language
version was written as a translation, not a summary, and I walked it back against the
technical one for content parity — which surfaced three gaps in my own first pass: the
payload-conditioning measurement was missing entirely, the development-only scope caveat was
missing, and the "this is not a research result" limit was missing. All three were added.

## Verification

```text
0 ROLLOUTS.  No plan mode, no replay, no execute mode.
UNTOUCHED   protocol file, extension document, assignment, draft config, seam, driver,
            every script, every test, every result artifact.  I re-hashed
            payload_boundary.json after all edits: canonical 7746372f…9aa04, unchanged.
            config/config.json still absent.  Test split untouched at 0 identities.
RE-DERIVED  every figure A2 quotes, from the persisted artifact rather than from my own
            Session-74 notes: the seven testable sets, all 70 margins as a percentage of
            their own threshold, the six in-band rungs, the four well-shaped flips, and
            the 0/0/0/0 recount.
SOURCES     weight-to-split map from config/proposed-gate3-assignment-v0.1.json;
            role-severity map from the frozen extension document; screen ladder from
            results/protocol_p/role_coverage.json.  A2 quotes no figure that exists only
            in a summary file.
DATES       screen executed 2026-08-01 (Codex S57), extension executed 2026-08-04
            (Codex S73) — taken from the transcript and Codex's reports, not recalled.
LINK        the one new external link in the accessible sheet (a preregistration
            explainer) was fetched and read this session, not cited from memory.
FILES       Claim Sheet.md             blob d4c2fea2b64de359be536908c52331edc3d673af  +146/-0
            Accessible Claim Sheet.md  blob 5bd4a93dfcb2bba1e803d885a7cb813dfec2067b  +103/-0
            Both are pure insertions; nothing above Slot 15 in either file was rewritten.
            Two late narrowing edits to A2.1 moved these blobs after the handoff turn was
            written; I appended a blob-correction turn naming the superseded pair rather
            than leaving the handoff pointing at bytes that no longer exist.  Transcript
            diff for that second append: +236/-0, all four assertions pass again.
```

**Transcript order — clean this session.** *(I am deliberately not quoting a streak
number. My own workspace README still says "thirty-two, through my Session 65," which has
been stale for ten sessions, and this project has already had one count be wrong five times
in a row because each correction trusted the previous one. The per-session assertions below
are the record; the streak figure needs a sweep, not a memory.)* Pre-write state
recorded before touching the file: 1,273,919 bytes, sha256
`c1533bc049b087ebbbfab02e8d0d28d877387fa68433d7863bb0807683aafd4c`, 19,764 lines, 19,329 CR
/ 19,764 LF. Post-write assertions all pass: the 1,273,919-byte prefix is byte-identical
and re-hashes to the same digest, my Session-75 header occurs exactly once and after the
boundary, I am physically last, the pre-existing CR count is unchanged at 19,329, and the
diff is `+201 / -0`.

**Live-Run README — heartbeat check run, no entry added, deliberately.** A2 is a proposal
until both agents approve the same bytes of both files. Logging a proposal as a decision is
precisely the over-claim A2 exists to prevent, and the log's newest entry (my Session-74
audit and its boundary caveat) is still exactly true. The entry belongs on the log when the
loop closes, and whoever writes it owes the reader the fact that the contract changed and
the bars did not.

## Cross-review

I read Codex's `HumanReport74.md`, its Session-74 transcript turn, and the frozen §9.5
licensing clause and both playbooks it pointed me at. Its independent reproduction of the
three load-bearing margins (`+2.123331840%`, `-4.141235418%`, `-22.583478651%`) agrees with
mine to every published digit, and its two-strength framing — *established* versus *measured
but not boundary-resolved* — is the framing A2.8 is built on. I found nothing to correct in
it. Its assignment of the draft to me, and its four requirements for the draft (dated
append, the four required contents, the exact non-transfer condition, the accessible sheet in
the same state), are all discharged.

## Files created or updated

- `Claim Sheet.md` — Amendment A2 appended; opening section points at it
- `Accessible Claim Sheet.md` — the same amendment in plain language; opening section points at it
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md` — Session-75 handoff turn with owner approval
- `agents/Claude/Session Summaries/HumanReport75.md` — this report
- `agents/Claude/README.md`
- `agents/Claude/Summary of Only Necessary Context.md`

## Next steps

1. **Codex reviews the exact two-file state** and either approves it or edits and hands it
   back with its own explicit approval. **A2 is not in force until both approvals name the
   same bytes of both files.**
2. **If Codex edits, I re-open both files and genuinely re-review** — that step is mine and
   it is the one the review-cycle playbook says most often does not happen.
3. **When the loop closes, two things fire in the same session:** the Live-Run README entry,
   and a progress report — an approved Claim-Sheet amendment is a report trigger regardless
   of the per-agent count. My next regular report is Session 80 either way.
4. **Only after A2 is in force** may the agents separately decide whether to authorize
   assignment lineage, coherent regeneration, and final config materialization. None of that
   is authorized now, and A2 says so in its own text.
