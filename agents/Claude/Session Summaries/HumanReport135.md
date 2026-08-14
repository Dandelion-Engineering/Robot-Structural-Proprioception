# Human Report — Claude Session 135

**Current date and time:** 2026-08-14 13:24 PDT (measured with `date` at the moment of writing)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

**Outcome:** The new review method was adopted and run for the first time on my side. Codex's
Round-1 blocker on the Slot-8 Step-4a design was accepted and integrated rather than answered with a
new finding, and I handed back an approved state. One real defect in the governing Review Card — a
Git blob id that does not exist — was found and corrected. No scientific read, run or counter
movement.

---

## 1. What the session was

Randy issued a new review protocol between my Session 134 and this one. Codex implemented it in its
Session 134; the playbook names **Claude Session 135** as my implementation session, so this session
had two jobs: adopt the method, and run the first owner half under it.

The method, in short: before review begins the owner writes a **Review Card** naming the exact
candidate state, what is in scope, the purpose, the acceptance tests, what counts as blocking, and
what is explicitly excluded. Round 1 is the only full-artifact review and must record every
reasonably discoverable finding in one numbered ledger. Round 2 and later are delta-only. A review
gets at most three owner–reviewer round-trips and must end in one of five named outcomes; the limit
never forces approval. Later implementation, amendments or new versions get new cards and new chats
rather than keeping an old review alive.

This is a direct correction to the failure mode my last several sessions demonstrated: the Step-4a
design review had reached round seven, and each of the last three rounds found a real defect in the
*previous round's own new text*. The method does not forbid that; it bounds it and it makes the unit
of approval explicit.

## 2. What I actually did

**Adopted the protocol first.** Read `Playbooks/review-cycle.md`'s superseding section, the two
new root files (`Review Card/README.md` and the transition card), and the new three-party governance
chat before touching the artifact. Worked only inside the new narrow subject chat; left the
concluded Phase-2 transcript untouched, as directed.

**Authenticated the boundary before reading anything.** The new subject chat was 1,610 bytes / 34 LF
/ 0 CR at SHA-256 `8e77062e…`, matching HEAD exactly, with Codex's header occurring once and Codex
physically last. Both digests Codex published for its reviewer state reproduce here byte for byte,
and so does my own Session-134 baseline.

**Reviewed the one open blocker (finding DE) on its merits, at source.** Codex's finding: my
Session-134 repair moved the final-config half of acceptance test B8 off the adapter path and onto
the config validator, so a hypothetical adapter that refused *every* final configuration could still
have passed the entire enumerated test set. That is correct, and it is the same blind spot Codex's
earlier finding DC identified for the development branch. I reproduced its legs in the live code
rather than accepting the account.

**Accepted it and integrated it, instead of raising a new finding.** This is the substantive change
in how I worked. I did find a gap in Codex's repair — see below — but because the card names me as
owner and this as my half of a round-trip, the right move was to build the correction into the state
I approve and record the reasoning in the section that owns it. Same technical content as a new
lettered finding would have carried; one fewer round.

**The gap I integrated.** Codex's repair introduces a shared internal "step-4 helper" that accepts an
explicit packet root, so a test can bind the real production branch to an isolated temporary packet
tree instead of the live packet. The idea is right. The naming was under-scoped: the same test's stop
condition is a *deliberate step-5 refusal*, and step 5 resolves its artifacts packet-relative, as do
step 3's domain binding and the section-4.7 output-parent rule. A helper scoped to step 4 alone would
leave those resolving against the **live** packet while only the config resolved against the
temporary one — so the test could not reach its own stop condition, and the half that did run would
exercise a parallel path rather than the production one. Codex's own definition of the helper ("the
single implementation used by the public roles path after record authentication") already implies the
wider seam, so this is the wording catching up with the object. One injected root is also strictly
narrower than the alternative: two root sources inside one traversal is the root-substitution hazard
itself.

I also added a **positive** requirement to invariant W8: a test must assert that the public path's
bound packet root *is* the live packet root. Proving that no override argument is parsed does not
prove what the root is.

**Scoped section 1.3 so the document stops saying two things.** It flatly refused to license writing
`config.json`; the repaired B8 now requires a test to write one below a temporary root. Both readings
were defensible, which is exactly the condition an earlier finding (DA) was raised under. 1.3 now
names the object it protects — the project's own `Reproducibility Packet/config.json` and anything
inside the live packet tree that could be taken for it — and points at the finding that draws the
fixture distinction.

**Wrote one measured contract fact into the test so the build round does not lose a day to it.** The
temporary tree's schema copy must be byte-exact rather than re-serialised, because the validator
requires the document's `schema_sha256` to equal the digest of the schema file it is handed. A
pretty-printed copy refuses for the wrong reason and the test would prove nothing about authority.

**Found and corrected a defect in the governing Review Card.** The card named the Round-1 owner
candidate as Git blob `968fa8959fc3b106895e794589c41954d0c2f901`. **That object does not exist in
this repository.** The true baseline is `968fa895fb81a04bfc04f4b743d8d03f3a1af612` — the first eight
characters are identical, which is exactly the width every summary and chat message in this project
quotes, so every eyeball check passes. Only asking the object store catches it. Codex's own chat
message authenticates the correct state by raw SHA-256, so the intent was never ambiguous; only the
id was wrong. I corrected the card, added the raw digest and byte figures beside the id so the same
slip is detectable next time, and disclosed the correction in both chats rather than fixing it
silently. Codex's Session-134 report carries the same id; that is a dated document and I have not
touched it — the correction propagates forward.

## 3. Measurements taken this session

| what | measured |
|---|---|
| my approved design state | blob `032db1666efbe00adec5696de70424d531ba33a2`, raw `f761a673ff8fcca6c58fe530a3faaed57630315a87a5e241d8ca9675a13c4ffc` |
| its physical form | 83,181 B / 1,062 LF / 0 CR / no BOM / final newline, LF-pinned (`git check-attr`) |
| my own design audit | `DESIGN_REVIEW_OK: 133 checks, 0 failed` |
| focused config-contract suite | `tests/test_data_contract.py`: 18 passed in 0.79 s |
| Codex's reviewer state | blob `425ce011…`, raw `a270d95d…`, 77,105 B / 993 LF — both reproduce |
| my Session-134 baseline | blob `968fa895fb81…`, raw `3fe6255c…`, 73,640 B / 951 LF — reproduces |
| the card's named baseline | `968fa8959fc3…` — **not an object**; `git cat-file -t` refuses it |
| `config.json` in the live packet | **none**, measured across the whole packet tree, not its root alone |
| packet-root derivation | `Path(__file__).resolve().parents[2]` from `scripts/utils/` is the packet root |
| chat appends | subject chat +7,832 B / 110 LF; governance chat +4,400 B / 64 LF; both prefix-verified, 0 CR |

My audit is deliberately structured around *what did not change*: it asserts section-by-section byte
equality against Codex's own state for every invariant except W8, every acceptance test except B8,
and all of sections 3, 4, 6, 8, 9.1–9.5 and 10. That turns the next round's "delta-only" from a
courtesy into a measured claim.

## 4. Challenges, and how they were handled

**The pull toward an eighth round.** Finding a defect in the reviewer's repair is, by now, the
default shape of this loop. The card is what broke it: it told me I was the owner, that this was my
half of round-trip 1, and that the finding was the unit of work. The self-test I settled on and
wrote into my standing lessons: *if I could write the repair myself in the same session, naming it
as a finding is a round spent on protocol, not on the work.*

**Deciding whether the card correction was mine to make.** The protocol lets reviewers apply
mechanical corrections directly and requires substantive changes to be proposed. This one is
mechanical in effect — the intent was unambiguous from the raw digest Codex published — but it sits
in a governing document, so a silent fix would have been the wrong shape. I made it and disclosed it
in full, with the reasoning, in both chats.

**Not over-editing.** The card's scope is finding 1, the acceptance tests and regressions. Two things
I noticed were deliberately kept *out* of the artifact: a stale docstring in a closed Step-2 blob
that carries the same wrong `--config` gloss an earlier finding corrected in the design (recorded as
a tracked follow-up for the build round), and the card's acceptance test 7 naming one agent's private
audit count as a criterion (raised as method feedback, not edited).

## 5. Decisions I made

1. **Accept finding DE in substance and integrate it** rather than hand back a new lettered finding.
2. **Widen the named seam** from a step-4 helper to the roles-mode entry point entered after record
   authentication, with its explicit packet root governing every packet-relative resolution in the
   read order — because the test's own stop condition is unreachable otherwise.
3. **Require a positive live-root binding assertion** in W8.
4. **Scope section 1.3** to the live packet tree rather than the bare filename.
5. **Correct the Review Card's baseline id** and add redundant identifiers beside it.
6. **Leave the Live-Run README untouched.** No artifact finished, no phase closed, nothing publicly
   noteworthy — the running log is lean by design, and this is the same call Codex made in its
   Session 134.

## 6. Insights worth keeping

- **An abbreviated identifier with the right prefix is not a verified identifier.** Eight matching
  characters defeated every human-and-agent check in the loop; one call to the object store found it
  in a second. Governing documents should name a state three ways.
- **Integration and finding carry the same technical content but different costs.** The difference is
  who holds the pen next. Reserve findings for disagreement.
- **A seam named after one step must be checked against the stop condition of the test that uses
  it.** Naming an injection point after the step under dispute silently under-scopes it.

All three are written into `agents/Claude/Permanent Instruments.md` as standing lessons 220–222.

## 7. Files created or updated

- `Reproducibility Packet/protocol/slot8-connection-record-v0.1.md` — owner integration of finding
  DE (status block, 1.3, 2.3, W8, B8, new 9.6 integration paragraph, section-11 ledger)
- `Review Card/Slot-8 Step-4a Connection-Record Design.md` — baseline id corrected, digests and
  byte figures added, round-trip-1 owner half and finding disposition recorded
- `chats/Claude-Codex/Slot-8 Step-4a Connection-Record Design/Slot-8 Step-4a Connection-Record Design - Active.md`
  — owner half of round-trip 1
- `chats/Claude-Codex-Human/Review Boundary and Convergence/Review Boundary and Convergence - Active.md`
  — method feedback, rollout problem 2, two interpretation notes
- `agents/Claude/Permanent Instruments.md` — standing lessons 220, 221, 222
- `agents/Claude/Session Summaries/HumanReport135.md` — this report
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — closeout

## 8. Boundary statement

I opened no role index, role payload, checkpoint, estimator output, controller log or
pilot/validation/test result; built no MuJoCo model; stepped no rollout; ran no fit; rendered no
figure; and wrote no config, connection record or production output. The one test run was the
focused config-contract suite, which touches no scientific input, and the packet-wide suite was not
re-run because no executable file changed. Counters stand at **278 rollouts, 67 fits, 67 checkpoints
and zero pilot/validation/test reads** — unchanged.

## 9. Next steps

1. **Codex's Round 2** on blob `032db166…`, delta-only: finding 1's integration, the card's
   acceptance tests, and any regression my response introduced. If it approves those exact bytes,
   sub-step 4a closes and 4b is authorized.
2. **If 4b is authorized**, the next real work is a large build round: the adapter and its tests,
   storage/refusal plumbing on the existing contract fixture, geometry on a dedicated coherent
   synthetic fixture, no real-data tolerance chosen, `require_frozen` selected from the record's
   authenticated authority, and B8's four legs under an isolated temporary packet root.
3. **If Codex edits or blocks**, the owner re-review is mine and comes first.
4. **My next regular progress report is Session 136** — the next session I run.

## 10. For Randy specifically

The method you introduced changed the outcome on its first use, not just the paperwork. I found the
same class of defect I have found in each of the last three rounds, and for the first time it did not
cost a round: it went into the state I approve, with the reasoning recorded, and the reviewer's next
pass is bounded to the delta. Whether 4a actually closes now depends on Codex's Round 2.

The one thing worth your attention is the Review Card defect. It is small and it is fixed, but it
landed in the exact place the method is load-bearing: the card exists to make "both agents approved
the same exact bytes" checkable, and it named bytes that do not exist. My suggestion — cards name
every state by blob id *and* raw SHA-256 *and* size, and whoever writes a card resolves each id
against the object store before it governs — is in the governance chat for you and Codex to accept
or amend.
