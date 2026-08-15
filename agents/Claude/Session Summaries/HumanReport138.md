# Human Report — Claude Session 138

**Current date and time:** 2026-08-14 19:38 PDT (measured with the shell immediately before writing this report)

**Agent:** Claude · **Branch:** `main` · **Phase:** 2 (Execution)

**Outcome:** Round 3 of the Slot-8 Step-4b-i review is delivered. Codex's one remaining
blocking finding — that the output namespace the connection record composes was neither
length-bounded nor one-to-one — is accepted without contest and integrated at both layers,
with all three of its failure states re-driven against the pre-repair bytes first. The
mutation sweep then found a real survivor in my own new tests, and fixing it produced the
session's most transferable lesson. The candidate is with Codex for the final review under
this card. No scientific read, no run, no counter moved.

---

## 1. Where the session started

The project is deep in Phase 2. Every scientific lane is spent or shut; the only open loop is
Slot 8's verification artifact, and inside that, sub-step 4b of the connection-record design —
split for review into **4b-i** (the contract: read-order rows 1–3 and the expected-open-set
derivation) and **4b-ii** (the adapter, not started).

The 4b-i card was at Round 2. Codex had accepted my Round-1 repairs on findings 1, 2 and 3,
accepted the renderer scope expansion, and blocked the candidate on one remaining disposition
of findings 4 and 5:

> the accepted output namespace is neither length-bounded nor injective.

Concretely, three states the green 311-test suite accepted:

1. a 251-character `case_id` composes a 256-character `.json` filename — longer than any
   mainstream filesystem allows;
2. `case_id = "verification_bundle"` composes the renderer's own manifest filename;
3. `Case-A` and `case-a` are two ids and one file on Windows.

## 2. What I did first, and why it mattered

I did not repair anything until I had reproduced all three failures myself, from a staging
copy of the pre-repair bytes outside the repository. The measurements are the part worth
keeping, because two of them are sharper than the finding as written:

| probe | measured behaviour of the pre-repair candidate |
|---|---|
| 251-character `case_id` | **Three files written** — the bundle JSON, its `.sha256`, and the case PNG — and then a raw `OSError` [Errno 22] on the 256-character scene JSON. A partial publication, produced by the helper whose own docstring said it validated the complete write set *before* writing. |
| `case_id = "verification_bundle"` | **Accepted.** The file `verification_bundle.json` on disk held the *scene* document and digested `3f1fab04…`, while the returned manifest reported `bundle_sha256 = 608fd5ce…`. **Two different numbers**: the digest a reader is told to check no longer hashed the file it names. |
| `Case-A` + `case-a` | **Accepted.** The manifest reported four cases; the directory held **eight** files rather than ten. |

Reproducing a finding is not the same as agreeing with it, and neither is the same as
understanding it. The two digests in row 2 are the reason this was worth an hour: they turn "a
collision" into "the verification artifact's own integrity check stops being about the
verification artifact", which is exactly the class of failure Slot 8 exists to make impossible.

## 3. The repair, at two independent layers

**At the record boundary** (`scripts/utils/connection_record.py`):

- `MAX_PORTABLE_COMPONENT_CHARS = 255` — the component ceiling NTFS, ext4, APFS, HFS+, XFS and
  Btrfs share — now bounds every component of every declared path.
- `MAX_CASE_ID_CHARS = 250` bounds `case_id`, which is 255 less the longest suffix the renderer
  appends. Bounding the *token* at the filesystem's own limit would have accepted a token whose
  every derived filename is over it — which is precisely the state that failed.
- `_parse_cases` claims the two fixed bundle filenames before it reads a single case, then
  records `folded derived filename -> claiming case_id`. Both collision shapes now refuse with
  a sentence of their own.
- `_portable_fold` is `str.lower`, documented: the portable grammar is ASCII-only, where
  `lower` and `casefold` agree exactly.

**At the write boundary** (`scripts/render_verification_scene.py`): `_contained_output_paths`
enforces the same two properties again — a 255-UTF-8-byte ceiling per name, and pairwise
distinctness under the same fold — before the containment check, and all of it before the first
byte is written. The layer is genuinely independent: the renderer imports nothing from the
contract module, so deleting either rule leaves the other standing. That independence is the
whole point of a defence-in-depth check.

**Where the two layers had to share a fact**, they do it by equality rather than by import.
The renderer's two fixed filenames and two derived suffixes are stated as literals in the
contract module — importing the renderer would pull matplotlib into a module that opens nothing
and draws nothing — and one test derives both tuples from the **tracked Step-3 figure set**,
which is what the renderer actually wrote. A rename over there goes red here. It is the same
discipline the module's role names already get against `schema.json`.

## 4. The decision I reversed inside my own repair

My first version of the write-boundary length check took
`max(len(name), len(name.encode("utf-8")))`, meaning to cover ext4's byte count and NTFS's
UTF-16 unit count at once. **That maximum is always the byte count.** A string's UTF-8 length
is never below its UTF-16 length — every BMP character is 1–3 bytes against 1 unit, every
astral character is 4 bytes against 2 — so the first term could never decide anything, and
deleting it would have changed no observable behaviour.

That is the same defect as a guard duplicated at every write, which is what Round 1's finding 5
response was written to avoid: a branch no test can distinguish from its own deletion. The
repair is not another test. It is deleting the term and writing down the proof that one count
bounds both.

## 5. The measurement that went against me

The focused suite was green at every step. The mandatory two-pass mutation control — 27 mutants
(25 real plus 2 negative controls) across both files, staged entirely outside the repository —
**reported one survivor on its first pass, and it was in my new tests rather than in my new
code.**

Raising `MAX_PORTABLE_COMPONENT_CHARS` from 255 to 4096 survived. Every length in the new tests
had been written as an offset from the constant under test — `MAX_CASE_ID_CHARS + 1`,
`"x" * MAX_PORTABLE_COMPONENT_CHARS` — so the inputs moved with the mutation. **341 green tests
would have stayed green on a module that accepted a four-thousand-character filename.**

What the suite was holding was the *relationship* between the constants, which was never in
doubt. What it was not holding was the *value*, which is the only part a reviewer cannot check
by reading. Every length is a literal now, and one test pins both constants to their literal
values with the reason attached, so a later session with cause to move a number has to say so
out loud.

After the repair: **25 of 25 real mutants caught, both negative controls surviving, identical
across both passes**, no bad anchors, and both targets' SHA-256 restored equal afterwards.

This is the third consecutive build on which the sweep changed the tests rather than confirming
them. I do not read that as the tests getting worse — I read it as the sweep being the only
instrument that sees this class of defect, and as confirmation that it belongs in the budget
*before* the handoff rather than after.

## 6. Evidence

- Focused suite `tests/test_connection_record.py`: **341 passed** (from 311), and 341 again
  under `python -O`.
- Packet-wide suite: **2,608 passed, 0 failed, 0 collection errors** in 191 s.
- `py_compile` and `git diff --check` clean; `git status --porcelain` lists exactly the three
  candidate files and nothing else.
- **The Step-3 figure set is byte-identical after this renderer edit**, measured twice — once
  after the containment/uniqueness work and again after the byte-count change. Regenerating at
  `--fixture-seed 7` under `MPLBACKEND=Agg` reproduces all **ten** tracked files at the same
  SHA-256; bundle digest `3bf51e94…` unchanged. The regeneration went to a git-ignored scratch
  directory that was deleted afterwards.
- Two-pass mutation control as described above.
- Round-3 candidate identities, each named three ways per the rule adopted after Session 135:

      scripts/utils/connection_record.py
        blob 312efd5ebf938a212c63de7a92ee2e8e4728ecf0
        raw  efc547ad9aab9a3682fb29ebae906bfe314a11531ebb4d4da1095c6a7d3b019a
        80,296 B / 1,881 LF / 0 CR / pure ASCII / no BOM / final newline
      tests/test_connection_record.py
        blob f854b894a76eb972f9b2e65903233909f05ef287
        raw  2933e80bd72b1786b74acb335c35efaf5412b4c646c04e32332cc7481a52e2aa
        98,220 B / 2,369 LF / 0 CR / pure ASCII / no BOM / final newline
      scripts/render_verification_scene.py
        blob 2e4b366ead7c47a3d6e71695f845471a2d9d52ef
        raw  83473e7aa15c1f072204a4c378044639e41147b7865670018eec8b4bcf7c8ff4
        36,123 B / 895 LF / 0 CR / pure ASCII / no BOM / final newline

## 7. Cross-review

I read Codex's `HumanReport137.md` and its Round-2 return in full. Nothing in either is
contested: its authentication figures for the Round-2 blobs match mine, its account of which
findings closed matches what I measured, and its blocking disposition is correct as written. I
also read its two process appends — the scope-expansion rule it adopted into
`Playbooks/review-cycle.md` and `Review Card/README.md` — and have nothing to add to the rule
as adopted.

## 8. Decisions I made that a later session should not re-derive

1. **Two ceilings, not one.** `MAX_CASE_ID_CHARS` is derived arithmetically from
   `MAX_PORTABLE_COMPONENT_CHARS` minus the longest derived suffix, so adding a third suffix
   moves the ceiling instead of leaving a number that used to be right.
2. **The fold is `str.lower`, not `str.casefold`.** They agree exactly over the ASCII grammar
   the record allows, and `casefold` would additionally map characters that grammar has already
   refused. Stated in the helper's docstring so it is not "corrected" later.
3. **The renderer counts UTF-8 bytes, once.** See section 4.
4. **The fixed filenames are literals pinned by equality against the published figure set**,
   not an import. See section 3.

## 9. Files created or updated

- `Reproducibility Packet/scripts/utils/connection_record.py` — the record-boundary repair.
- `Reproducibility Packet/scripts/render_verification_scene.py` — the write-boundary repair.
- `Reproducibility Packet/tests/test_connection_record.py` — 18 new test functions, 30 new
  collected cases, four added import names, nothing else changed.
- `Review Card/Slot-8 Step-4b-i Connection-Record Contract.md` — Round-3 owner response, new
  candidate identities, superseded list, and the changed/byte-identical delta statement.
- `chats/Claude-Codex/Slot-8 Step-4b-i Connection-Record Contract/… - Active.md` — the Round-3
  handoff.
- `chats/Claude-Codex-Human/Review Boundary and Convergence/… - Active.md` — the scope-rule
  acknowledgement, the round-limit note, and the testing lesson.
- `agents/Claude/Permanent Instruments.md` — standing lessons 229, 230 and 231.
- `agents/Claude/Session Summaries/HumanReport138.md` — this report.
- `agents/Claude/README.md`, `agents/Claude/Summary of Only Necessary Context.md` — refreshed.

## 10. Next steps

1. **Codex's Round 3** is the final review under this card. If it approves the same bytes, the
   card closes and 4b-ii begins under a new card and a new chat. If it finds something real,
   the honest outcomes are *Revisions Required* on a new card or *Escalated* — the round limit
   never forces approval, and I have said so in the method chat in advance rather than in the
   moment.
2. **4b-ii remains not started** and carries two recorded forward items: the geometry
   producer's digest domain (a runtime that hashes a `*.py` file, which is the exact premise
   Codex's Session-128 no-EOL-pin ruling relied on), and the source-class interpretation.
3. **Nothing downstream moved.** No production connection record, no scientific read, no
   capacity or threshold selection, no configuration freeze, no adapter invocation, and no
   C1-versus-S statement is authorized by anything in this session.

## 11. Live-run README

Checked, deliberately not updated. This session neither finished an artifact nor closed a
phase; it delivered one review round inside an open one. The public log is lean by design and a
round-trip inside a review is not a milestone.
