# Claude — Human Report, Session 97

**Date and time:** 2026-08-08 12:18 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session: 0.** Project lifetime Protocol-P-related total remains
**278**.

**Fits: 0. Checkpoint writes: 0. Data generated: 0. Pilot / validation / test reads: 0.**
**New plan artifacts published: 0** — two review probes ran plan mode into scratch destinations
*outside the repository*, and the tracked artifact was never opened for writing.

**Progress-report session:** **no.** My next regular is Session 104. No phase transition and no
approved Claim-Sheet amendment occurred this session.

---

## Summary in one paragraph

Codex's Session 96 closed the capacity-sweep executable/test loop and then ran the one permitted
zero-fit plan regeneration, approving the resulting document and handing me the second
independent review. That review was this session's whole job, and I did it as a second
instrument rather than a second run of the producer: ninety-four checks that never import the
sweep module, every expected value re-derived from a file on disk, from the two approved
development documents, or from the frozen design's own prose. Everything Codex reported is
accurate, including its "exactly one field change" claim, which I confirmed by walking both
documents to full leaf depth — 413 leaves each, one changed. I then added the two measurements
its audit could not reach: section 7.1's byte-determinism requirement, which had not been
re-measured since the finding-AT repair moved the executable, and the authorization gate driven
against twenty-one *neighbours* rather than only the exact bytes. Both came back clean. I
explicitly approved the exact plan bytes, **closing Step 3**, and recorded two scope statements —
about a digest domain and about what one field does and does not certify — deliberately as
records rather than as findings. **No fit, checkpoint, generation, rollout, reserved-data read,
threshold choice, config freeze or confirmatory action occurred, and Step 4 does not exist.**

---

## What I set out to do, and why the method mattered

The object under review was one 13,786-byte JSON document: the regenerated capacity-sweep plan
at Git blob `c048b54b…` / SHA-256 `bdf674d5…1c0a5`. It is the document that will, if a separate
joint authorization is ever issued, license forty-two development fits.

Codex's audit of it was competent and I am not contesting any part of it. But its central
technique was to rebuild `plan_document()` in memory and require equality with the stored file.
**That checks the document against the builder; it does not check the builder against itself,
and it cannot notice anything both sides get wrong the same way.** So I deliberately chose the
opposite instrument, the same one I used in Session 95: audit the artifact **without importing
`utils.capacity_sweep` at all**, re-deriving every expected value from an independent source.
Where the sweep module was unavoidable — driving its own authorization gate — I used it only as
the *thing under test*, never as the source of the expected answer.

## What the audit found

**Everything Codex reported is accurate.** The physical state is exactly as stated: one canonical
JSON line, 13,786 bytes, no final newline, no BOM, pure ASCII, and — checked rather than assumed
— re-emitting the parsed document under the project's canonical-JSON convention reproduces the
file byte for byte, and raw equals canonical.

**The "exactly one field change" claim holds at full depth.** Rather than comparing the fields
either of us thought to name, I walked the superseded and regenerated documents to every scalar
leaf, list indices included. Both carry 413 leaves. Nothing was added, nothing removed, and
exactly one value differs: `code_identity.capacity_sweep.py`, moving from the superseded
executable's digest to the jointly approved `d91db2ef…`. That is precisely what the Session-95
repair should have changed and nothing else moved with it.

**Every binding was recomputed rather than compared to Codex's copy.** The design, ledger,
analysis and assignment digests each match a fresh canonical hash of the file on disk. The
`config_hash` was *recomputed from the draft config document* — the hash of its canonical JSON
with its own two hash members removed reproduces `712abf27…`, and the draft config's own recorded
value agrees. All nine `code_identity` entries were recomputed from the modules on disk, the
eight inherited ones are byte-equal to the approved ledger's, and the additions over the ledger's
set are exactly `{"capacity_sweep.py"}` — the one addition invariant C3 permits.

**The ten anchors are bound three ways over.** Each plan digest equals the approved ledger's
recorded digest, equals the approved analysis's recorded digest, *and* equals the raw SHA-256 of
the checkpoint file actually sitting in `results/dev_fit` today. The plan's anchor entries carry
identity only — no metric fields — which is the right shape for a plan.

**The forty curve arms are correct and cross-sourced.** The set is exactly widths
{16, 24, 40, 48} × suites {C1, S} × seeds 0–4, unique, with none at 32 channels (invariant C1).
Every arm's parameter count matches the frozen design's section-4.2 table, which I quoted out of
the design document's own text — and this is a genuine cross-source comparison rather than a
constant matching a constant, because `plan_document()` reads those counts off **freshly
constructed networks** via `capacity_shape_map()`. Every count sits inside Slot 9's rung-1 band.

**Finding AT's repair is intact end to end, verified through the published document.** Last
session I approved that repair by reading the code. This session I checked the chain in *these
bytes*: the plan binds `approved_analysis_sha256`, that digest matches the analysis artifact on
disk, that artifact records an analyzer identity of `4caa2938…`, and that value equals a fresh
canonical hash of `scripts/analyze_dev_fit.py`. The analyzer is bound transitively and is not a
tenth `code_identity` entry, so C3's cardinality is untouched. I also re-walked the analyzer's
import surface at source and confirmed every project-defined name it uses to score an arm sits
inside the bound nine.

## The two things Codex's audit did not cover

### 1. Section 7.1's byte-determinism requirement, unmeasured against this executable

The design requires that two plan runs at the same `run_label` into different host destinations
produce identical bytes. That is not decoration — it is what makes the plan's digest a statement
about the design of the run rather than about the machine that wrote it. **The last time it was
measured was my Session 95, before Codex's finding-AT repair moved the module.** Codex's
in-memory reconstruction does not re-establish it, because the same process produces both sides.

I ran plan mode twice into two unrelated scratch destinations outside the repository. Both
produced `bdf674d5…1c0a5`, identical to each other and to the published artifact under `cmp`.
Each destination afterwards contained exactly one file, and the worktree was clean before and
after. The requirement is now a measurement against the bytes actually under review.

### 2. The authorization gate, driven against its neighbours

Codex passed the exact artifact and digest through `require_authorized_plan()` and it accepted.
**A gate that accepted everything would pass that test identically.** Session 73's standing rule
is the one that applies: an authorization is worth exactly what the gate reading it is worth, so
drive it against the exact bytes *and their neighbours* before naming a digest.

I built twenty-one neighbours, each written to a temporary directory with its own recomputed
digest so only content differs, plus the exact bytes as a positive control. **22 / 22 behaved as
required: one accept, twenty-one refusals.** A dropped curve arm, an added 32-channel arm, a
budget raised to 43 fits, a budget granted a rollout, a zeroed anchor digest, a replaced analysis
digest, a parameter count off by one, a checkpoint destination rewritten to `C:/tmp/steal.pt`, a
flipped `plan_valid`, a changed mode, a tenth `code_identity` entry, an upper-cased digest — all
refused. So was the superseded `d2584d28` plan, with the sentence this whole two-session sequence
exists around: *written by a different code state*. Four checks the design names individually
fire with their own sentences; the rest are caught by document equality against a fresh rebuild,
which is the stronger check, so a shared generic reason there is not a defect. The published
artifact's digest was asserted unchanged at the end of the sweep.

## Two things I measured and deliberately did NOT raise

**The four delivered-data digests bind in the raw domain, and that is correct here.** My probe
assumed the canonical text domain and got four disagreements. Rather than reporting a finding, I
measured the question. All four files carry CRLF throughout (945 / 945 / 473 / 473 pairs) and
match the raw digest exactly. This is not a violation of the Session-59 domain rule: those files
are **git-ignored generated data, not tracked text**, so no checkout convention can move them,
and they are written by `csv.DictWriter` through `open(..., newline="")`, whose dialect pins the
line terminator to `'\r\n'` as a standard-library constant on every platform — which I read back
at runtime rather than trusting the documentation. A regeneration on another operating system
therefore produces the same bytes. Decisively, **all four values are byte-identical to the ones
the approved ledger and the approved analysis already carry**, so the domain was settled two
approvals ago and this plan is consistent with it.

**`role_index_sha256` is a provenance declaration, not a gate.** I traced the execute-time path.
`require_authorized_dataset` enforces the data-root name, the manifest digest and the config hash
against the same module constants, so those three declarations are backed by a refusal. But
**nothing in this read path ever opens an `index.csv`** — the trainer and analyzer reach payloads
through `manifest.csv` — so there is no execute-time gate a role-index digest could be. I
measured that all three still match the delivered files today. I recorded this because a reader
could take the field to mean *this run verified those three files*, and it does not; it means
*this is the delivered dataset the run is declared against*. Neither observation is a defect and
I asked for no change to either.

## A Step-4 precondition nobody had written down

Checking what the plan's ten anchor digests actually *name* turned up something that is not a
plan defect but had to be said before either agent issues an execution authorization, so I
posted it as a second, short chat turn.

**The ten approved 32-channel checkpoints exist only in this working tree.** Measured rather
than assumed: `git ls-files "*.pt"` returns zero files anywhere in the repository, and
`git check-ignore` traces the exclusion to the Reproducibility Packet's own `.gitignore`.
Meanwhile `capacity_sweep.py` reads them from a fixed packet-relative path with **no CLI
override** — the command surface is exactly seven pinned flags — and the C9 equivalence gate
refuses loudly if either approved checkpoint is absent. **So `--mode execute` is runnable on
this machine and nowhere else, and nothing in the plan, the design or the packet README says
so.** The refusal itself is correct behaviour; the silence about it is the gap.

There is a second edge to it. The packet README's regeneration step writes rebuilt checkpoints
into `results/dev_fit_reproduced`, and its analyzer step reads them from there. **The sweep
cannot follow that path** — it has no equivalent flag — so a reader who follows the runbook
still ends up with an empty `results/dev_fit`. I deliberately did *not* propose adding a flag: a
flag would let an operator point the equivalence gate at checkpoints nobody approved, which is a
worse failure than the constraint.

I put three things on the record: that whoever runs execute mode must do so in a tree already
holding those ten files, and that this is the one precondition the digest gate cannot check
*before* the decision to spend; that **whether a regeneration reproduces the ten recorded digests
bit-for-bit on a different machine is not established** — the trainer is seeded and pins its
convolution precision, but bit-identical across hosts is a stronger claim than anything measured,
and if it is false the packet cannot reproduce this sweep on a clean machine, which is a Phase-3
disclosure rather than a bug; and a question I handed to Codex to rule rather than deciding
alone — whether this belongs in `director_requests.md` or is purely an agent-side packet
obligation. My reading is the latter, since nothing here needs Randy's identity, judgment or
access, but it touches both the Slot-8 verification path and the fresh-environment validation the
packet owes, so the ruling is better made jointly.

**None of this changes the plan, my approval of it, or the fact that Step 3 is closed.**

**Why record these rather than raise them.** Last session I declined a guard on the same grounds
and named the failure mode: *the cargo-cult version of the last finding — the ritual of finding
AT applied where its mechanism does not exist*. Finding AT was live because an unbound file on
disk could move while the plan's bytes stayed identical. Neither of these has that shape. But an
observation a reviewer measured and then said nothing about is indistinguishable from one it
never made, so both go into the record with their reasoning exposed for Codex to overrule.

## Decisions I made

1. **Audit without importing the producer.** The single most consequential choice. Codex's
   rebuild-and-compare is a strong check but it cannot see an error both sides share; an
   independent re-derivation can.
2. **Approve rather than block.** Nothing I measured is wrong. Approving on the same bytes closes
   Step 3, which is exactly what the design's sequencing asks for at this point.
3. **Add the determinism measurement rather than inherit it.** A property measured against a
   superseded executable is not a property of the current one, and the summary I hand forward
   would otherwise have carried a true-sounding claim that no longer covered the artifact.
4. **Drive the gate against neighbours.** Applying my own standing rule to a review I was
   receiving rather than only to one I was giving.
5. **Record the two scope statements instead of raising them, and say why in the chat.** The
   reasoning is the reusable part; Codex can overrule the reasoning and not merely the code.
6. **Do not issue my half of the Step-4 authorization.** Plan correctness and permission to spend
   forty-two fits are deliberately separate gates. Bundling them into an approval message would
   quietly convert a review into a spend authorization.
7. **One lean public log entry.** Both agents approving the same plan closes a gate, which is a
   decision-relevant forward state; the previous entry ends with the review still open.

## Challenges

The only real one was distinguishing a defect from an inherited convention. Four checks failed on
first run, all of them digest-domain disagreements on delivered-data files — precisely the shape
of a Session-59-rule violation, and precisely the shape of the mutation survivor I closed last
session. The discipline that resolved it was to measure the question rather than trust either
instinct: read the writer, read the dialect constant at runtime, and check whether the two
already-approved documents record the same values. They do, which settles it. **The general
lesson is that a probe's failing check is a statement about the probe until its assumption has
been independently established.**

## Files created or updated

Updated:
- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config
  Freeze - Active.md` — two byte appends, `+287 / −0` total: my explicit approval with the two
  measurements, and the Step-4 precondition note.
- `README.md` — one lean running-log entry recording that planning is closed by both agents.
- `agents/Claude/README.md` — Session-97 navigation.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

Created:
- `agents/Claude/Session Summaries/HumanReport97.md` — this report.

Reviewed and deliberately unchanged:
- `Reproducibility Packet/results/capacity_sweep/capacity_sweep_plan.json` — approved as-is.
- `Reproducibility Packet/scripts/utils/capacity_sweep.py`,
  `Reproducibility Packet/tests/test_capacity_sweep.py`,
  `Reproducibility Packet/protocol/capacity-escalation-v0.1.md` — all closed, none reopened.
- `director_requests.md` — no new director-only blocker.
- `.gitignore` — current rules already cover the session lock, environments, caches and generated
  artifacts; nothing this session produced needs a new rule, and the probe scripts were written
  to the scratchpad outside the repository.

## Cross-review

I read Codex's `HumanReport96.md` in full and both of its Session-96 chat turns before doing any
work. Its account of what it did matches what the repository shows at every point I checked
independently: the transcript byte counts, the plan blob, the semantic diff and the digest it
named. I carried no correction forward from it. **One loop remains open in the other direction:
Codex owes a review of my Session-96 progress report** at `agents/Claude/Progress Reports/
Progress Report Session 96.md`. It is not blocking anything.

## Transcript hard gates

Two byte appends, not patches — on a mixed-EOL file only a byte append can promise a
byte-identical prefix.

```text
FIRST APPEND — the plan approval
pre-write bytes       1,658,183     (matches Codex's recorded Session-96 final state exactly)
pre-write lines       26,622
pre-write SHA-256     b10869d3368df9c1fd6369287a35a82e669abfd879a0b03cf9ecffb9d1cfb6d4
post-write bytes      1,672,788
post-write lines      26,846
prefix retained       EXACT
header                unique at line 26,624, after the recorded boundary

SECOND APPEND — the Step-4 precondition note
pre-write SHA-256     bf3c3df031a247604b105f4324ccca5c039e0c811331cd12c37fd5848cc47084
final bytes           1,676,645
final lines           26,909
final SHA-256         dd317527adb02326de68ea5c49db6f7b85b9ea10e28cb0f7e15296f8d8fdcf01
prefix retained       EXACT
header                the note's own header unique at line 26,848, byte 1,672,789,
                      confirmed >= the pre-write length
physically last       Claude
Git diff              +287 / −0 across both appends
```

**One honest note about my own instrument.** On the second append the writer reported
*"header occurrences 2 … after boundary NO"*. That was the gate describing the **wrong object**:
it searches for the session-prefix `**Claude (Session 97` and reports the position of the *first*
match, which is my earlier turn from the same session. The append itself was correct, and I
re-checked it by hand — the note's own header sits at byte 1,672,789 against a pre-write length
of 1,672,788, the prefix is byte-identical, and Claude is physically last. The fix is to key the
search on the payload's own full header line rather than a session prefix, and I recorded that in
my continuity summary so the next session does not reuse it unfixed. **A gate that reports a
true-sounding failure about the wrong object is the same defect family this project keeps
finding; I am not going to let mine pass unrecorded just because it fired conservatively.**

No Transcript Order Monitoring note was required — both appends landed at the physical tail.

## Verification

```text
INDEPENDENT AUDIT      94 checks, ZERO imports from utils.capacity_sweep
SEMANTIC DIFF          413 leaves both sides; 1 changed, 0 added, 0 removed
DETERMINISM            3 destinations, 1 digest, byte-identical under cmp
GATE NEIGHBOURS        22 / 22 — one accept, twenty-one refusals
FULL PACKET SUITE      1,765 passed in 133.32 s
GIT STATUS             clean before the probes; the only tracked changes are this session's
                       documents and the chat append
PRODUCTION BLOBS       plan c048b54b, capacity_sweep 61d4fb97, tests 8e97f6a9, design b45efa47,
                       analyze_dev_fit 31381b18, dev_fit_trainer caa00418, dev_fit_contract
                       bd2c0d08, attribution_net c4fa3c63 — ALL UNCHANGED
PACKET ARTIFACTS       ONE capacity_sweep_plan.json.  results/capacity_sweep/stage1-run-1/
                       absent.  No result artifact, no equivalence artifact, no .pt outside
                       results/dev_fit.  config/config.json still ABSENT.
FITS 0 | CHECKPOINTS 0 | GENERATION 0 | ROLLOUTS 0 | PUBLISHED PLAN ARTIFACTS 0
REAL DATA              READS ONLY, and only of the four delivered manifest/index CSVs, to settle
                       the digest-domain question.  No observation payload and no label payload
                       was opened; the ten approved checkpoints were opened only to hash their
                       bytes.  PILOT / VAL / TEST: 0.
                       LIFETIME PROTOCOL-P ROLLOUTS UNCHANGED AT 278.
```

## Next steps

1. **Step 3 is closed.** Both agents have explicitly approved plan SHA-256 `bdf674d5…1c0a5`.
2. **Step 4 — execution of the forty-two fits — remains a separate joint authorization that does
   not exist.** Neither agent has issued a half. When issued it must name that digest, and each
   agent should state what it checked *below* the spend rather than in exchange for it.
3. **The Step-4 precondition is open on Codex.** Whoever runs execute mode must do so in a tree
   holding the ten approved checkpoints; whether a regeneration reproduces their digests
   bit-for-bit on another machine is unestablished; and I asked Codex to rule whether this is a
   `director_requests.md` entry or a purely agent-side Phase-3 packet obligation.
4. The **C7 read-only analysis script** is still unbuilt and unauthorized. It is the next separate
   build, and it should import the section-5 pure functions that already exist in
   `capacity_sweep.py` rather than defining them a second time.
5. Codex's review of my Session-96 progress report is open.
6. My next regular progress report is **Session 104**, unless a phase transition or an approved
   written Claim-Sheet amendment fires one sooner.

— Claude
