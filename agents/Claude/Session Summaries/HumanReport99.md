# Claude — Human Report, Session 99

**Date and time:** 2026-08-08 20:35 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset: 0. Checkpoint writes: 0. Data generated: 0. Plan artifacts
published: 0. Pilot / validation / test reads: 0.** Real-data touches of any kind: **none** — no
manifest, no `.npz`, no approved checkpoint. Plan mode takes no `--data-root`, and the three
invocations I ran wrote only into the system temp tree.

**Progress-report session:** no. My next regular report is Session 104 unless a phase transition or
an approved Claim Sheet amendment fires sooner.

---

## Summary

Session 98 ran the capacity sweep, it died on its second arm, and I found and repaired the defect
(**Finding AU**) that made it impossible for that program to ever complete a sweep. Codex reviewed
that repair in its own Session 98: it approved the production fix unchanged, ruled explicitly on the
one judgment call I had asked it to rule on, and then found that the three tests I wrote to prove the
fix **could still be fooled** — so it edited one of them and handed the file back. That left the
review loop open, and closing it honestly was this session's job.

I did not wave the edit through. I re-opened both files and drove the edit rather than reading it,
using a ten-case mutation sweep run against **both** test states — mine and Codex's — so every claim
below is a measurement of two suites side by side rather than an opinion about a diff.

**Codex's finding is real, and the hole was three times wider than it reported.** It demonstrated one
broken version that slipped through my tests (checking only one of the four model sizes). I found
that *two more* slipped through as well: checking three of the four, and checking all four in the
wrong order. Its single added assertion catches all three, because it pins the *sequence* rather than
the membership.

**And the one case my tests did catch, they caught by luck.** The mutation "check only the smallest
width" dies against my suite only because my other test happens to plant its trip-wire in the
*largest* width's directory. Had I written that fixture at 16 channels instead of 48, my suite would
have been blind to the single-point mutation in both directions, and Codex's probe would have been
the only thing standing between the project and a second dead run. That is the same failure shape as
the degenerate fixtures of Sessions 86 and 87 and the constant-blind parametrization of Session 71,
and I recorded it as a limitation rather than quietly fixing it, because the edited test now closes
it from the other side.

I looked hard for a defect in Codex's edit and did not find one. The one thing I went in suspicious
of — that its expected list is derived from the *same* expression the code under test iterates, which
is exactly the shape the project's requirement (z) warns about — I settled by measurement rather than
argument: three separate mutations show the derivation is anchored by things outside itself. I would
not have approved it on the reasoning. I approved it on the measurement.

**I explicitly approved both blobs unchanged. Codex approved the same two blobs in its Session 98, so
the executable review loop is closed.**

With the loop closed I did one more thing, at zero spend and entirely outside the repository:
re-measured the plan writer's byte-determinism against the repaired program (it had last been measured
against the *previous* version of the program, so it was not inherited), and published, in advance,
the exact digest and byte count the next plan must have. If the plan Codex writes next session does
not match the number I already computed, we find that out before any training rather than after.

## What was accomplished

### 1. Verified the handoff before reviewing it

- `git status` clean; `HEAD` at `85419ba` (Codex Session 98).
- Hashed the working tree: production `capacity_sweep.py` is still blob `53e5dcb7…`, exactly the
  state I handed off. Codex's "no production line changed in my review" is therefore verified, not
  accepted on its word.
- Test file is blob `6d49edde…`, the state Codex named.
- The whole diff is **+16 / −3** in one test: three docstring lines rewritten, a recorder wrapped
  around the real cleanliness guard, and one list-equality assertion.

### 2. Re-established the baseline on the exact handed-back bytes

```text
focused suite                   217 passed
focused suite under python -O   217 passed, one expected pytest assertion warning
full packet suite             1,768 passed  (133 s)
compileall                      clean
git diff --check                clean
```

Every figure matches what Codex reported, independently obtained.

### 3. The ten-case mutation sweep, run against both test states

The harness mutates the executable in place and restores it in a `finally` with the restore
digest-verified (`be07d95e…f641fa` before and after; the working tree is clean now). For each case it
runs the focused suite once against my Session-98 test blob and once against Codex's, so the two
suites are compared on identical inputs.

```text
case                                      Claude S98   Codex S98    caught by
M0  comment-only control                  SURVIVED     SURVIVED     -- (the control holds)
M1  for point in [48]                     SURVIVED     CAUGHT       whole-loop test
M2  for point in [16]                     CAUGHT       CAUGHT       stale-file test
M3  sorted(...)[1:]  three of four        SURVIVED     CAUGHT       whole-loop test
M4  sorted(..., reverse=True)             SURVIVED     CAUGHT       whole-loop test
M5  each point checked twice              CAUGHT       CAUGHT       AST test
M6  point_dir not under the run root      CAUGHT       CAUGHT       stale-file + one-definition
M7  "channels_" -> "chan_"                CAUGHT       CAUGHT       one-definition test
M8  CAPACITY_POINTS drops 40              CAUGHT (9)   CAUGHT (9)   nine tests
M9  the AU defect restored verbatim       CAUGHT (3)   CAUGHT (3)   all three
M10 curve_arms() widths (16,16,40,48)     CAUGHT (8)   CAUGHT (8)   eight tests
```

Run twice, identical both times. Three conclusions, each of which needed the sweep rather than a
reading of the diff:

- **The gap is real and three mutations wide** (M1, M3, M4), not the one Codex demonstrated.
- **Nothing was weakened.** Every case my suite caught, Codex's suite also catches. The repair is a
  strict improvement: +3 caught, −0.
- **M9 restores the actual Finding-AU defect byte-faithfully** (copied out of the pre-repair blob
  `61d4fb97`, including its own `try`/`except` shape) and it still dies against all three tests under
  both states, so the repair's original purpose survived the edit.

### 4. Settled the independence question by measurement

Codex's added assertion compares the recorded directory names against a list derived from
`sorted({channels for channels, _, _ in cs.curve_arms()})` — the *same* expression the loop under
test iterates — and records only `Path(directory).name`. Both are the shape requirement (z) exists to
catch: two sides of a comparison produced by one source. Three cases settle it:

- **M6** — dropping the `run_root /` prefix so the guard inspects a directory outside the claimed run
  root — is caught by the stale-file test and by the one-definition test. The `.name` reduction is
  therefore not a gap.
- **M7** — moving the directory-name format itself — is caught by the one-definition test, which is
  the Session-94 Finding-AS repair still doing its job.
- **M10** — the hardest case I could construct: `curve_arms()` emitting the widths `(16, 16, 40, 48)`,
  which moves *both* sides of the comparison together while preserving forty arms, both suites, five
  seeds, and nothing at the anchor width — fails eight tests, led by checkpoint-name uniqueness and
  C10's census.

A derived expectation is acceptable exactly when something independent pins the thing it derives
from. Here three things do.

### 5. Closed the loop

Explicitly approved, unchanged, both files:

```text
Reproducibility Packet/scripts/utils/capacity_sweep.py
  Git blob                 53e5dcb79d4f8c131b6856fd5fa57fce6049976a
  canonical/raw SHA-256    be07d95e4b4b9fa1a8934a165681fdbc9e7e885236bd1de3c38b661288f641fa
Reproducibility Packet/tests/test_capacity_sweep.py
  Git blob                 6d49edde03e24a262e4246669fad8e42859c6f8a
  canonical/raw SHA-256    640f23b5990d9fc9f17fe0eeb39bbf9192abaa26ab1726653d9df9942c1747d3
```

Codex approved the same two blobs in its Session 98, so both approvals now name the same state.
**The executable review loop is closed.** That closes the first of the four gates the sweep re-run has
to pass.

### 6. Re-measured section 7.1, and published the next plan's digest before the plan exists

Byte-determinism was last measured in my Session 97 against the *previous* executable. The module's
bytes moved with the AU repair, so that measurement is not inherited. Three plan-mode invocations at
`--run-label stage1-run-2`, into three different scratch `--output-dir`s under the system temp tree,
no `--data-root`:

```text
X_PLAN_OK: 40 new arms + 2 equivalence arms planned at run label stage1-run-2, 0 fits run
three destinations -> ONE digest
  ffb009650ae4cedd37a1b0c7b9beaef1c0c1555fa4583111cb22e9c0f9b7cb31
13,786 B, zero CR bytes, no final newline, raw == canonical
re-emission under sort_keys + compact separators is byte-identical
no absolute path anywhere in the document
```

So the destination does not enter the document, and section 7.1 holds under the repaired module.
Against the spent `bdf674d5…` plan, at **full leaf depth** and with **no import** from
`utils.capacity_sweep`: **413 leaves each side, 0 added, 0 removed, 48 changed** — the forty curve
checkpoint names, the two equivalence checkpoint names, `equivalence_artifact_relative_name`,
`equivalence_relative_namespace`, `logical_output_namespace`, `run_artifact_relative_name`,
`run_label`, and exactly one identity, `code_identity.capacity_sweep.py`, moving to `be07d95e…`,
which is the approved executable's own canonical digest. The ten anchors, both approved document
digests, the protocol block, the budget (42 / 42 / 0 / 0 / 0) and the other eight code identities are
byte-identical to the spent plan.

I deliberately did **not** publish a plan. Gate 2 is Codex's to run, for the same reason the last two
were: one agent produces the artifact and the other audits it as a second instrument. What I put on
the record instead is the number, in advance.

## Challenges, and how they were handled

**The temptation to accept a correct-looking edit.** Codex's edit is sixteen lines and obviously
well-intentioned, and the project is blocked on my approval. The playbook's named failure mode is
exactly this: accepting the diagnosis and swallowing the implementation. The discipline that made it
a real re-review was refusing to compare the two suites by reading them, and instead building an
instrument that runs both against the same ten mutations. That instrument is what found that the gap
was three wide rather than one, and what found the fixture accident in my own test — neither of which
is visible in the diff.

**A negative control that could have made the whole sweep meaningless.** M0 is a comment-only edit,
and it must survive. If it had been caught, the sweep would have been measuring pytest collection
rather than the tests, which is exactly the invalid-harness failure I hit in Session 92. It survived
under both states, twice.

**Reproducing the defect faithfully rather than approximately.** My first sketch of M9 spliced the
guard back into the curve loop at the wrong indentation and outside the exception handling that gave
the real defect its `X_OUTPUT_DIRTY` exit — which would have "caught" the mutation for the wrong
reason. I read the pre-repair blob `61d4fb97` and copied its actual six lines instead. A mutation that
fails for a different reason than the defect did is not evidence about the defect.

**A digest convention we have both been sloppy about.** Codex and I have both been quoting
"canonical/raw SHA-256" as one figure. That equality is a property of *this working tree*, not of the
repository: `.gitattributes` pins `eol=lf` for the schema, the assignment JSON and `protocol/*.md`,
and deliberately not for `.py`, so a fresh clone on Windows materializes both files as CRLF and the
**raw** digests move. I checked whether anything load-bearing depends on it and nothing does —
`code_identity()` digests in the line-ending-invariant Protocol-P text domain, so the executable's
identity and every gate reading it are portable. I recorded it in the chat as a scope note, did not
ask for a `.gitattributes` change, and asked only that we keep writing the canonical digest first,
since that is the one a stranger can reproduce.

## Important decisions

1. **Approve rather than edit.** I found no defect in Codex's edit. Session 71's heuristic — a round
   that finds only coverage is the signal to close, not to hunt for one more — applies directly, and
   the cost of one more round-trip here is a delayed sweep re-run.
2. **Record the fixture accident as a limitation, not a finding.** M2's catch is luck, but the edited
   test closes the same hole from the other direction, so a second fixture would be redundant guard
   rather than new coverage. The lesson is worth more than the test.
3. **Do not publish a plan.** Producing the gate-2 artifact myself would collapse the producer/auditor
   separation that has found something real at every plan gate so far. Publishing the *expected
   digest* instead gives the audit an independent expectation formed before the artifact exists,
   which is strictly more than I would have had by producing it.
4. **Re-measure byte-determinism now rather than at the audit.** If the repaired module had lost
   determinism, discovering it now costs nothing; discovering it during the gate-2 audit costs a
   round-trip and confuses the audit's finding with a property of the program.

## Insights

- **A test suite can be blind along an axis and look complete, and the thing that hides it is usually
  a fixture constant nobody chose deliberately.** My stale-file test plants its trip-wire at 48
  channels for no reason other than that 48 was in front of me when I wrote it. That arbitrary choice
  is the entire difference between a suite that catches "check only the smallest width" and one that
  does not. Sessions 71, 86, 87 and now 99 have all found this shape, each time in different clothes.
- **The right instrument for reviewing a test edit is a mutation sweep run against both states, not a
  reading of the diff.** A diff tells you what changed; a two-state sweep tells you what each state
  can *see*, which is the only property a test file actually has. It also protects against the failure
  I was most at risk of here — accepting an edit that fixes the reported case while silently losing
  coverage somewhere else.
- **"Derived from the same source" is a suspicion, not a verdict.** Requirement (z) is right that a
  comparison whose two sides come from one function is a report of a check. But the honest test is
  whether *anything else* pins the shared source, and that is measurable. Treating (z) as an automatic
  block would have cost a round-trip over a non-problem; treating it as an automatic pass would have
  been the cargo-cult version. The middle move — go measure — took twenty minutes.
- **An expectation published before the artifact exists is a different instrument from one formed
  after it.** Auditing Codex's plan after seeing it means my "independent" derivation happens with the
  answer already on screen. Computing the digest first, in the open, removes that. This is cheap and I
  should do it at every future artifact gate where the artifact is deterministic.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — appended my Session-99 owner re-review, the sweep table, the explicit two-blob approval, the
  digest-domain scope note, and the pre-registered gate-2 plan digest. Byte append, prior digest
  `a03f87a2…` asserted inside the writer, prefix re-verified after the write, header unique,
  physically last; **+138 / −0** at the Git level.
- `README.md` — one running-log entry (the repair is approved by both agents; the tests-could-be-fooled
  finding and how much wider it turned out to be; the pre-published plan digest). Append-only; banner
  unchanged, since no phase moved.
- `agents/Claude/Session Summaries/HumanReport99.md` — this report.
- `agents/Claude/Summary of Only Necessary Context.md` — rewritten.
- `agents/Claude/README.md` — updated.

**Nothing under `Reproducibility Packet/` was modified.** The mutation harness restored the executable
to `be07d95e…f641fa` and the test file to `640f23b5…`, both verified after the run, and the three plan
invocations wrote only into the system temp tree.

Scratch files (not committed), under the session scratchpad:
`au_review_sweep.py` (the two-state mutation harness), `plan_leaf_delta.py` (the full-leaf-depth plan
comparison, importing nothing from the executable), `append_chat.py` (the verified byte-append writer),
`au_sweep_pass1.json` / `au_sweep_pass2.json`, and `plan_a` / `plan_b` / `plan_c`.

## Next steps

The four gates, with the first now closed:

1. ~~Codex rules on the repair and the above-C9 placement; both agents approve the same executable and
   test state.~~ **CLOSED this session.**
2. **Codex publishes the zero-fit plan at `stage1-run-2` and I audit it.** It must be
   `ffb00965…f9b7cb31` at 13,786 bytes; if it is not, one of us is wrong and we settle that before any
   fit. Both agents approve the exact bytes.
3. **A new two-half Step-4 execution authorization naming that digest.** Both old halves are spent and
   neither carries; a retry is a second execution and a second authorization.
4. **The run.** C9 must re-establish itself inside it — the equivalence result is *not* inherited from
   `stage1-run-1`, because the module's bytes moved. Then both agents review the exact resulting state,
   then the section-5.4 read, then the C7 read-only analysis script.

Standing items unchanged: the failed `stage1-run-1` root is preserved evidence and must not be deleted,
cleaned up, or have its label reused; the declined analysis-vs-ledger guard remains a standing decision
Codex has not overruled; and the clean-machine anchor-recovery obligation for the Reproducibility Packet
(ten files today, fifty-two after a completed sweep) is still open for Phase 3.
