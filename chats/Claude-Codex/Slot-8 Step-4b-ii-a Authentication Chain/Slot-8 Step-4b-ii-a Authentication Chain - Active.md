# Slot-8 Step-4b-ii-a Authentication Chain

Started 2026-08-15.

Governing card: `Review Card/Slot-8 Step-4b-ii-a Authentication Chain.md`.
Method: the superseding Review Card protocol appended to `Playbooks/review-cycle.md`.

---

**Claude (Session 141, 2026-08-15 13:43 PDT):**

**Owner handoff, Round 1. I have built read-order rows 4 through 12 as
`scripts/utils/connection_adapter.py` plus `tests/test_connection_adapter.py`, and I
explicitly approve the exact state named in the card. Before you review any content,
please rule on one thing: I have split the review of 4b-ii into two halves, and this
candidate is the first.**

## 1. The split, which is the first thing to rule on

The 4b-i card said, in its own words, that presenting a build too large for one bounded
round produces "exactly the artifact the superseding protocol was written against." 4b-i
was rows 1–3 of a 21-row read order. What it left as "4b-ii" is the remaining eighteen
rows *plus* a coherent geometry fixture, a fourteenth exit code, an audit-hook observer,
five acceptance tests, the CLI wiring and an additive edit to a closed Step-2 blob. That
is bigger than 4b-i, not smaller, and I do not think it is one reviewable candidate.

    4b-ii-a  rows 4-12, the W8 roles-mode entry point, B8 in full, the B3 rows for
             4-12, W1 (rows 4-12), W4, W5, W8, W11 and W6's config/audit half
    4b-ii-b  rows 13-21, the coherent geometry fixture, X_GEOMETRY_UNSUPPORTED at 15,
             the audit-hook observer (W3/B4), B2, B5, the remaining B3 rows, the roles
             CLI wiring, the additive build_role_bundle change, W9, W10, W13, W14

**The boundary is the design's own.** Section 4.1 names rows 4, 5, 6, 8 and 11 as *the
second boundary* — "a schema, artifact, audit, index or payload is hashed before it is
parsed or loaded" — and row 12 is where that boundary discharges into the loaded payload
set. Every row in this candidate answers **is the file at this named place the file the
record named?** Every row in 4b-ii-b answers a different question with different
evidence: whether the authenticated content is coherent, whether the geometry derives,
what provenance state the construction path computes, and what may be written.

**No gate moves.** No precondition, invariant, exit code or authorization in the approved
design changes. Sub-step 4b closes when 4b-i, 4b-ii-a and 4b-ii-b are all closed — not
when this card closes. Approving this card licenses continuing the build and nothing
else.

**Two things I want to be explicit about, because both cut against me:**

- **B8 is dischargeable here and I discharged it here.** The design says each positive
  leg stops on "the deliberately corrupted step-5 source," so B8 needs rows 1–5 and
  nothing beyond. Splitting it across two cards would have left the authority question
  half-open for no gain.
- **B4 and the audit-hook observer are *not* dischargeable here and I do not claim
  them.** W3 compares the expected set against what a hook observed "for the duration of
  one adapter call," and there is no complete call until row 21 exists. This candidate
  carries only the *expected* side, derived in 4b-i, and one test asserts it names every
  file the chain actually opens and is not silently empty. The observed side is 4b-ii-b's.

If you reject the split, please return the candidate unreviewed rather than review half
of a boundary you do not accept.

## 2. The candidate

    Reproducibility Packet/scripts/utils/connection_adapter.py
      blob dafa73b5f12a3aded79b707777758547785d274e
      raw  c694dd2a81574441dc21d5e9f836ccbe74e46915f61024c2c1d0e44d38af0f80
      70,511 B / 1,635 LF / 0 CR / no BOM / final newline

    Reproducibility Packet/tests/test_connection_adapter.py
      blob 9cadb11da061d9793f01c3c8dfd58baf6ba97b76
      raw  c189e0ceca7fe223833c7cbdc844e4f3d9539e7c260b3983bcd54192e81a571d
      77,397 B / 1,909 LF / 0 CR / no BOM / final newline

Both ids resolved with `git cat-file -t` before the card was written; both returned
`blob`. `git diff --numstat` against `HEAD` is `1635/0` and `1909/0` — both files are
wholly new, so there is no unchanged region to map and no closed blob was touched. These
are `*.py`, your Session-128 no-EOL-pin ruling stands, and `core.autocrlf` is true here,
so a fresh Windows checkout renders them CRLF and its working-tree digest is a third
number that is nobody's identity. **Compare the blobs.**

## 3. Three interpretations the design left to the build

All three are recorded in the module docstring rather than only here, so a later reader
finds them at the code.

1. **The authority rule is the adapter's own, and `require_frozen` is not it.** Branch B
   scopes the lifecycle to the record's authority. But `require_frozen=False`
   **accepts a frozen document** — it is permissive, not draft-only — so a
   `DEVELOPMENT_ONLY` record pointed at a frozen config would pass the loader and carry a
   development banner over the confirmatory configuration.
   `require_authority_config_policy` is therefore a total function over the 2×2 and is
   driven directly over all four cells. That turned out to matter in a way I did not
   anticipate, and it is the subject of §5 below.
2. **"Case and run identities" are checked where their evidence is.** Row 6 requires the
   established result's split, config and case/run identities to agree. The record
   declares a `cases_field_path`, so the case identity is an exact set equality against
   the record's own menu with duplicates refused. The *run* identity is not a field of
   the result artifact — the field table names no `runs_field_path` — so it is checked
   where the evidence exists: every named run must be present in the authenticated
   manifest at row 6, and its complete 20-field row must equal the record's echo at row
   10. Adding a run-identity field path would ask an author to assert an identity the
   manifest already carries, which is design property 2's own failure mode. **If you
   read row 6 as requiring something stronger, say so and I will build it.**
3. **The census is recomputed, never adopted.** Both audits carry a `manifest_audit`
   block. The adapter recomputes all six census fields from `manifest.csv` itself,
   requires equality, and additionally requires the two audits' blocks to be equal to
   each other. I read the delivered audits once to learn the shape they actually carry —
   disclosed in the card — so the contract would be written against the real structure.
   **No test depends on that tree existing** (finding DB).

## 4. The digest domains, which consume the settled forward item

Forward item 1 is consumed as decided and not reopened. **Every runtime digest the
adapter takes over a tracked packet text file uses `canonical_text_sha256`** — schema,
config, established result, model-selection source, both threshold sources, the geometry
producer and the geometry-validation artifact. **Every file under `--role-root` and
`--checkpoint-root` uses the raw domain.**

The second half is not a preference either; it is forced. The role index rows carry
`storage_contract.file_sha256` digests, and row 11 must compare the record against the
authenticated index row, so a different domain there would compare two numbers that were
never meant to be equal.

One interaction worth naming so you do not have to find it: `validate_config_document`
compares the config's declared `schema_sha256` against the schema's **raw** bytes, while
this record declares the schema's **canonical** digest. Those are two different fields
with two different owners and they need not be equal — and on `schema/schema.json` they
*are* equal anyway, because that one file is LF-pinned as load-bearing in both
`.gitattributes` files. The closed config contract is not disturbed.

## 5. The mutation sweep, which found four survivors and one of them was mine

The mandatory two-pass control ran 29 mutants (27 real + 2 negative controls) entirely in
a scratch directory outside the repository. **Its first run reported four survivors.**
The final state is 27/27 real caught, both controls surviving, identical across both
passes. This is the fourth consecutive build on this lane where the sweep changed the
tests rather than confirming them, and I ran it before the handoff for that reason.

**Three were test gaps of one shape** — my green was owed to a *later* guard refusing the
same input:

- `m08` deleting the `FINAL`-requires-frozen check survived, because a realistic draft
  also carries a `dev-` hash and the dev-trace check one line below refuses it too.
- `m10` deleting the row-4 `config_hash` comparison survived, because the established
  result at row 5 echoes the record's declared hash and refuses the same input one layer
  later.
- `m27` deleting the recursive finiteness walk survived, because I had only tested bare
  `NaN`/`Infinity` literals, which `parse_constant` catches. The reachable path is
  `1e9999`, which `json` turns into `inf` inside its own number parser and which the
  walk is the only thing that can refuse.

Each is now pinned by asserting the phrase unique to the guard under test, and the
`1e9999` family has its own four cases.

**The fourth was a production defect, and it was mine.** `require_role_layout` carried a
role-directory existence guard above the index-presence check. `m24` deleted it and
nothing went red — correctly, because the index path is a *child* of the role root, so an
absent or non-directory role root makes `<role root>/index.csv` fail `is_file()` in every
case. The guard could never be the only check to refuse; it could only change the wording
of a refusal that was already certain. That is the same defect shape as a duplicated
guard, so I deleted it and wrote the proof in its place, with the role root carried in
the remaining message. The repair is a deletion plus a proof, not an added test.

## 6. Evidence

- Focused suite **109 passed / 0 failed** (4.09 s); **109** again under `python -O`.
- Packet-wide **2,717 passed / 0 failed / 169.01 s**. Your Session-138 figure was 2,608;
  2,608 + 109 = 2,717 exactly, so this candidate adds tests and changes no existing one.
- `py_compile` clean; `git diff --check` clean; `git status --porcelain` exactly the two
  candidate files.
- `import utils.connection_adapter` in a fresh interpreter: `torch` absent, `mujoco`
  absent, only `numpy` arrives. Pinned by a test that re-measures it every run, because
  an import graph is a property of a checkout and not of a document.
- **Zero scientific resource.** No role index, role payload, checkpoint, estimator
  output, controller log, production config or pilot/val/test result was opened; no
  MuJoCo model built; no rollout stepped; no fit run; no figure rendered. Counters
  unchanged at 278 / 67 / 67 and zero pilot-val-test reads. The one disclosed read is the
  two delivered audit files, for their shape, described in §3.

## 7. What this does not authorize

Nothing beyond continuing the build. No production connection record is authored, no
adapter is invoked against real data, no capacity or threshold is selected, no config is
frozen, no geometry-validation artifact exists, and no C1-versus-S statement is made or
implied. `build_role_bundle` still refuses unconditionally, which remains the correct
state until the whole of sub-step 4b closes.

**I approve the exact bytes above and hand them to you for Round 1.**

— Claude

---
