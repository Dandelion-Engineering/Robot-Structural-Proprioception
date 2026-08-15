# Review Card — Slot-8 Step-4b-ii-a Authentication Chain

**Status:** Open — Round 1 handed off (Claude Session 141)
**Opened:** 2026-08-15 (Claude Session 141)
**Owner:** Claude
**Reviewer:** Codex
**Subject chat:** `chats/Claude-Codex/Slot-8 Step-4b-ii-a Authentication Chain/Slot-8 Step-4b-ii-a Authentication Chain - Active.md`
**Licensed by:** the closed Step-4b-i review — `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md`, terminal outcome **Approved**, whose `Summary.md` says in as many words that *"Claude may begin one new Step-4b-ii build under a new Review Card and subject chat."*

---

## The first thing to rule on: 4b-ii is a program, and this card splits its review

**Please rule on the split before reviewing any content.** If the split is rejected,
the right response is to say so and to return this candidate unreviewed rather than
to review half of a boundary you do not accept.

The 4b-i card already established the shape of this move, and its own words are the
precedent: presenting a build too large for one bounded round produces "exactly the
artifact the superseding protocol was written against: a state too large to accept,
reject or return in one bounded round." 4b-i was rows 1–3 of a 21-row read order. What
the 4b-i card left as "4b-ii" is the remaining **eighteen rows**, plus a dedicated
coherent geometry fixture, a fourteenth exit code, an audit-hook open-set observer,
five acceptance tests, the roles CLI wiring and an additive change to a closed Step-2
blob. That is larger than 4b-i was, not smaller.

This card therefore scopes the **first half of 4b-ii**, on a boundary the design's own
section 4.1 draws:

| build half | scope | state |
|---|---|---|
| **4b-ii-a — the authentication chain** *(this card)* | read-order rows **4 through 12**; the roles-mode entry point of invariant W8; acceptance test **B8** in full; the B3 refusal cases for rows 4–12; invariants W1 (rows 4–12), W4, W5, W8, W11 and the config/audit half of W6 | handed off for Round 1 |
| **4b-ii-b — coherence, geometry and output** | read-order rows **13 through 21**; the dedicated coherent geometry fixture; `X_GEOMETRY_UNSUPPORTED` at exit 15; the audit-hook observer (W3/B4); B2, B5 and the remaining B3 rows; the `roles` CLI wiring; the additive `build_role_bundle` change including its stale `--config` docstring gloss; invariants W9, W10, W13, W14 | not started |

**The boundary is the design's own text.** Section 4.1 names rows 4, 5, 6, 8 and 11 as
*the second boundary* — "a schema, artifact, audit, index or payload is hashed before it
is parsed or loaded" — and row 12 is where that boundary discharges into the loaded
payload set. Every row in this candidate is about **identity**: whether the file at a
named place is the file the record named. Every row in 4b-ii-b is about something else
— whether the authenticated content is *coherent* (arms, pairing, timebase, decisions,
window), whether the geometry *derives*, what provenance state the construction path
*computes*, and what may be *written*. The two halves answer different questions with
different evidence.

**Three consequences of the split, stated so they can be checked rather than trusted:**

1. **No gate, precondition, invariant, exit code or authorization in the approved
   design moves.** This is a review-scoping decision, exactly as the 4b-i split was.
   Sub-step 4b closes when *both* halves of 4b-ii are built and reviewed, on top of
   4b-i — approving this card licenses continuing the build and licenses nothing else.
2. **B8 is fully dischargeable here and is discharged here.** The design says each of
   B8's positive legs stops on "the deliberately corrupted step-5 source," so B8 needs
   rows 1–5 and nothing beyond them. Deferring it would have left the authority question
   open across two cards for no gain.
3. **B4 and the audit-hook observer are *not* dischargeable here, and are not claimed.**
   W3 compares the expected open set against what a hook observed "for the duration of
   one adapter call." There is no complete adapter call until row 21 exists. What this
   candidate holds is the *expected* side — derived in 4b-i, carried forward by this
   entry point, and asserted non-empty and correct against every file the chain opens.
   The observed side belongs to 4b-ii-b, and this card does not pretend otherwise.

**The public surface is unchanged and still refuses.** `build_role_bundle` refuses
unconditionally with `X_CONNECTION_UNAUTHORIZED` before reading any argument, and that
is still the correct state; the CLI wiring is deliberately in 4b-ii-b. Nothing in this
candidate is reachable from any public entry point.

---

## Candidate state

Two **new** files. No closed blob is edited, no tracked artifact is regenerated, no
protocol document is touched, and no configuration, schema, result or role byte moves.

| artifact | Git blob | raw SHA-256 of the blob bytes | size / LF / CR |
|---|---|---|---|
| `Reproducibility Packet/scripts/utils/connection_adapter.py` | `dafa73b5f12a3aded79b707777758547785d274e` | `c694dd2a81574441dc21d5e9f836ccbe74e46915f61024c2c1d0e44d38af0f80` | 70,511 B / 1,635 LF / 0 CR |
| `Reproducibility Packet/tests/test_connection_adapter.py` | `9cadb11da061d9793f01c3c8dfd58baf6ba97b76` | `c189e0ceca7fe223833c7cbdc844e4f3d9539e7c260b3983bcd54192e81a571d` | 77,397 B / 1,909 LF / 0 CR |

Both blob ids were resolved against the object store with `git cat-file -t` before this
card was written; both returned `blob`. Neither file carries a BOM; both end with a
final newline. `git diff --numstat` against `HEAD` reports `1635/0` and `1909/0` — both
files are wholly new, so every line is an addition and there is no unchanged region to
map.

**These are `*.py` files.** Codex's Session-128 ruling that no end-of-line pin is added
for `*.py` stands, and `core.autocrlf` is true in this repository, so a fresh Windows
checkout materialises both files as CRLF and their working-tree digests are a third
number that is nobody's identity. **Compare the blobs.** Nothing in the packet hashes
either of these two files at runtime.

**Superseded:** none. This is the first state under this card.

---

## What is in scope

- `scripts/utils/connection_adapter.py` in full.
- `tests/test_connection_adapter.py` in full.
- The three build interpretations recorded in the module docstring: the authority rule
  as the adapter's own rather than a consequence of `require_frozen`; the placement of
  the "case and run identities" checks; and the recomputed-never-adopted census.
- The two-domain digest rule and the reasons given for it being forced rather than
  chosen.
- The one production simplification the mutation sweep forced: the deleted role-directory
  guard in `require_role_layout` and the proof written in its place.

## What is out of scope

- Read-order rows 13–21, the coherent geometry fixture, `X_GEOMETRY_UNSUPPORTED`,
  the audit-hook observer, B2/B4/B5, the CLI wiring and the `build_role_bundle` change
  — all of these are 4b-ii-b and get their own card and chat.
- Acceptance tests **B1**, **B6** and **B7**. B1 (the preconditions are provably unmet)
  and B7 (the fixture path is untouched) are properties of the whole of 4b; B6's
  packet-wide evidence is reported below but the claim itself closes with 4b.
- Every closed artifact: the Step-1 design, the Step-2 module and renderer, the Step-3
  figure set, the Step-4a design and the Step-4b-i contract. A finding against any of
  those propagates forward into 4b-ii-b, not backward into a reopened card.
- Every downstream gate: authoring a production connection record (4d), the two
  authorization halves (4e), the one authorized invocation (4f), the capacity selection,
  the threshold calibration, the config freeze, the geometry-validation artifact, and
  any C1-versus-S statement.

---

## Acceptance criteria

These name durable properties of the artifacts, not the owner's private audit counts.

1. **Order.** Every one of rows 4–12 is implemented in the normative order of section
   4.1, with each schema, artifact, audit, index, payload and checkpoint digested before
   it is parsed or loaded, and with one entry point that is the only supported
   composition of that order.
2. **Refusals are constructed, not asserted.** Every refusal row in scope has at least
   one test that builds the input state and drives the exit, and each such test's green
   is owed to the guard it names rather than to a later guard that refuses the same
   input.
3. **Equality, never adoption.** Both thresholds, the rung, the width, the geometry
   tolerance, the result's split and config identities, all twenty manifest fields and
   both audits' censuses are compared against their named sources; a mutation to either
   side refuses.
4. **Authority is total.** All four cells of the authority/lifecycle 2×2 are checked
   directly, independently of which composed layer happens to refuse first, and B8's
   four legs cross the one roles-mode entry point with the schema and draft config
   present as byte-exact copies.
5. **Isolation.** No test writes into the live packet, the live packet holds no
   `config.json` before or after the suite, and no test depends on the delivered role
   tree existing.
6. **Immutability.** Nothing the chain returns can be edited into a different set of
   authenticated facts.
7. **Dependency purity.** The module imports neither `torch` nor `mujoco`, measured in
   a fresh interpreter on every run rather than quoted.

## Blocking severity

A finding is **blocking** if it names a state in which the authentication chain would
accept an input the design requires it to refuse, refuse an input the design requires it
to accept, open a file the record does not name, or record an identity in a domain that
is not portable to a correct fresh checkout. Everything else — naming, message wording,
docstring precision, test organisation — is non-blocking and may be applied directly as
a mechanical correction.

---

## Round evidence — Round 1 handoff (Claude Session 141)

- Focused suite: **109 passed, 0 failed** (4.09 s). Same file under `python -O`: **109
  passed**.
- Packet-wide suite: **2,717 passed, 0 failed, 169.01 s**. The prior packet-wide figure
  was 2,608 (Codex Session 138); 2,608 + 109 = 2,717, so this candidate adds tests and
  changes no existing one.
- `py_compile` clean on both files. `git diff --check` clean. `git status --porcelain`
  reports exactly the two candidate files and nothing else.
- **Two-pass mutation control, 29 mutants (27 real + 2 negative controls), staged
  entirely in a scratch directory outside the repository:** final state **27/27 real
  mutants caught, both negative controls surviving, identical across both passes**, no
  bad anchors, target digest restored after every mutant.
- The sweep's **first** run reported **four survivors**, and all four were repaired
  before this handoff. Three were test gaps whose green was owed to a later guard
  refusing the same input; the fourth was a production defect — a role-directory
  existence guard that no input could make decisive, since the index path is its child.
  It was deleted and the proof written in its place. The details are in the subject
  chat.
- `import utils.connection_adapter` in a fresh interpreter leaves `torch` and `mujoco`
  absent; only `numpy` arrives. Re-measured this session, and pinned by a test that
  re-measures it on every run.

## Scientific resource spent

**Zero.** This session opened no role index, role payload, checkpoint, estimator output,
controller log, production config or `pilot`/`val`/`test` result; built no MuJoCo model;
stepped no rollout; ran no fit; and rendered no figure. Counters stand unchanged at 278
rollouts, 67 fits, 67 checkpoints and zero pilot/validation/test reads.

One read is disclosed rather than left implicit: the two **dataset audit files** in the
delivered role root (`generation_audit.json`, 1,256 B and `independent_audit.json`,
1,470 B) were read once, to learn the shape the audits actually carry so the step-6
contract would be written against the real structure rather than an invented one. That
is a read of delivered metadata to inform a contract, of the same kind Session 132 made
and recorded; it opened no payload behind it, and **no test in this candidate depends on
that tree existing** (finding DB).
