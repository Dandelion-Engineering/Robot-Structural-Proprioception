# Claude Human Report — Session 100

**Date and time:** 2026-08-09 00:26 PDT

**Phase:** Phase 2 — Execution

**Physical rollouts spent this session:** 0. Project lifetime Protocol-P-related total remains **278**.

**Fits against the delivered dataset:** 0. **Checkpoint writes:** 0. **Data generation:** 0.
**Pilot / validation / test outcome reads:** 0. **Lifetime fit counter unchanged at 13.**
No plan artifact was published and no `--mode execute` invocation was made.

**Progress-report session:** no. My next regular progress report is Session 104, unless a phase
transition or an approved Claim-Sheet amendment fires sooner.

---

## Summary

This session did the job my Session 99 reserved for it. Codex published the replacement capacity-
sweep plan at the end of its Session 99; my job was to audit it as a second instrument and either
approve the exact bytes or return an edit. I audited it in three parts (136 checks), approved it,
and **gate 2 is now closed** — both agents have approved the same plan document. I then issued, as
its own separate turn, **my half of the fresh Step-4 joint authorization** for the forty-two-fit
run. Codex's half does not exist yet, so nothing may run, and nothing did: the session spent zero
fits, zero checkpoints, zero rollouts and zero generation.

The plan matched, to the byte, the digest and byte count I put on the record in Session 99 *before
the artifact existed*. That prediction holding is the cleanest thing in the session, and it is
worth being precise about what it does and does not buy: it proves the bytes are the ones I
predicted, not that what I predicted was correct. So I ran the audit anyway.

Two things came out of it that were not in either agent's account beforehand. First, the plan was
published in a **new location** — a plan-history directory — and I measured, rather than argued,
whether a document's approval can depend on where the document is kept. Second, my own audit script
failed four checks on its first pass, and all four were the script's error rather than the
document's, in a way that reproduces a scope note I wrote myself three sessions ago.

I also made a real mistake this session, in my own transcript headers, and I fixed the instrument
rather than only reporting it. That is written up below.

## What was accomplished

### 1. Gate-2 audit, part A — 106 checks, importing nothing from the producer

The whole point of a second instrument is that it does not share code with the first one, so part A
imports nothing from `utils.capacity_sweep`. It re-derives each expected value from something
outside the producer: the files on disk, the two approved development artifacts, the frozen design
document's own text, and the consumed `stage1-run-1` plan.

- **Physical state and canonical-JSON conformance.** 13,786 bytes, zero CR bytes, no BOM, no final
  newline, pure ASCII, raw digest equal to canonical digest — and, the check that actually proves
  conformance, a compact re-emission of the parsed document compared **byte for byte** against the
  file.
- **Every bound identity recomputed from the file on disk**: the frozen design, the approved fit
  ledger, the approved analysis artifact, the assignment, the delivered manifest and the three role
  indexes.
- **All nine code identities recomputed**, and the eight inherited ones compared to the approved
  ledger's — the invariant that permits exactly one addition (`capacity_sweep.py`) and no more.
- **The finding-AT binding walked end to end**: the analyzer identity recorded inside the approved
  analysis, compared to the analyzer on disk, and confirmed *not* to be a tenth identity entry.
- **The ten anchors** hashed against their checkpoint files and, separately, against the digests the
  approved ledger records.
- **The forty new arms** rebuilt as {16, 24, 40, 48} × {C1, S} × seeds 0–4, none at the anchor
  width, with every parameter count checked against the design's section-4.2 table **grepped out of
  the frozen design's own text** rather than typed from memory.
- **The 44 declared destinations** distinct and packet-relative, no absolute path in any value or
  member name, the budget arithmetic re-derived from the plan's own arm lists, and the two
  analysis-sourced constants retrieved through the field paths the plan itself names.
- **A full-leaf delta against the consumed plan**, computed independently: 413 leaves each side,
  0 added, 0 removed, 48 changed — and the 48 are exactly the set I pre-registered. Every one of the
  47 path leaves differs from its predecessor *only* by `stage1-run-1` → `stage1-run-2`, checked as
  an equality rather than by reading the list.

### 2. Part B — 25 checks driving the module's own gates in call order

The opposite instrument: drive every pre-spend check the executable itself runs, in the order it
runs them, ending at the last one that sits below the first fit. `design_digest`,
`resolve_protocol`, `require_authorized_plan` at the exact bytes, `capacity_shape_map` and
`require_distinct_capacity_counts`, `require_anchor_comparability`,
`require_approved_analyzer_identity`, `approved_anchor_arms`, `sweep_code_identity` recomputed now
and compared to the plan's, and `load_dev_examples` returning C1 152 / S 152.

Two negative controls, because a gate that accepted everything would pass an exact-bytes check
identically: one flipped hex character is refused, and a one-token edit to the document body is
refused. And one check driven rather than assumed — **the consumed `bdf674d5…` plan is still
refused by the repaired module**, with `the authorized plan was written by a different code state`.
A spent plan cannot be resurrected by pointing `--approved-plan` at it.

I also re-took section 7.1's byte-determinism measurement at a **fourth independent destination**:
a fresh plan-mode invocation into a scratch directory reproduced the published bytes exactly.

### 3. Part C — the question the new plan location creates, measured

Codex deliberately published at `results/capacity_sweep/plans/stage1-run-2/`. The reasoning is
right on both halves: overwriting the consumed plan would destroy the exact bytes the failed run's
evidence names, and writing at the future run root would make the atomic root claim fail by
construction. But the choice raises a question nobody had answered, so I answered it twice.

**Can the location enter the document, or affect its approval?** No, and I measured it rather than
reading the source and concluding. The same bytes authenticate at a flat scratch directory, at a
three-deep scratch directory, and under a **different file name entirely**; the document nowhere
records its own path; no declared destination mentions the new directory; and a one-token edit at
those same foreign locations is still refused. The authorization gate names a document and the path
is only how you hand it over.

**Does the plan history collide with anything?** Partly, and it fails safe. The run root is bound to
`<base>/<run_label>/`, and `plans` is a legal run label under the design's own pattern, so the plan
history now reserves one name in the run-label namespace. I built a replica of the base under a
temporary directory and drove the claim function at it: the real label `stage1-run-2` **is**
claimable beside the plan history, and a run labelled `plans` is refused with the same
`RunRootOccupied` exit that already protects the preserved failed-run evidence. So the collision
fails in the direction that preserves the record. I recorded it as a scope note rather than a
finding, and asked only that future plans keep going under `plans/<label>/` so the reservation stays
exactly one name instead of growing one per publication.

I additionally checked that nothing downstream still points at the old plan path — no packet
document, runbook, test or README names it as a path a reader should pass to `--approved-plan` — so
there is no stale instruction telling a stranger to authorize the spent plan.

### 4. My own audit script failed four checks, and all four were mine

Part A's first pass reported four failures: the delivered manifest digest and the three role-index
digests did not match. They match the **raw** digests exactly — 945 / 945 / 473 / 473 CRLF pairs,
the same figures I recorded in Session 97. Those four files are git-ignored *generated* CSVs, and
Python's CSV writer pins `\r\n` as a standard-library constant on every platform, so they live in
the raw domain rather than the canonical text domain. My probe applied the tracked-text rule to
generated data.

This is my own Session-97 scope note arriving from the other side, and the fix is not to change the
comparison but to make the probe assert **both** directions — raw matches, canonical does not — so a
future silent move between domains fails loudly instead of passing by luck.

### 5. Gate 2 closed, and my Step-4 authorization half issued as its own turn

I explicitly approved plan blob `d7104e55b4fb9be3fbfa6bd685b002a055409673`, canonical SHA-256
`ffb00965…b7cb31`, unchanged. Codex approved the same blob in its Session 99, so both approvals now
name the same state.

Then, in a **separate turn** — never folded into the review, because bundling converts a review into
a spend — I issued Claude's half of the fresh Step-4 authorization. It names the plan document and
digest, the run label, the **base directory** (load-bearing: the executable refuses only
destinations at or inside the approved-checkpoint tree, so "every write is beneath the claimed root"
is exactly as strong as the base named in the authorization and no stronger), the data root, the
exact executable blob, the ten anchor digests plus a single checkable digest-of-the-ten, and the
maximum budget of forty-two fits and forty-two checkpoints with zero generation, zero rollouts and
zero reserved-data reads. It states explicitly what it does **not** authorize: the analysis script,
the pre-registered interpretation step, capacity selection, thresholds, the config freeze, any
generation, any rollout, and any pilot/validation/test read.

It also names the four residuals no mechanism closes, and repeats the honest scope statement about
this executable: it has no ephemerality bracket at all, so the correct sentence is not "here is what
the watch list misses" but **nothing outside the claimed run root is measured by this executable at
any point**.

**I am deliberately not the runner.** When my turn posted, only one half existed. Whoever runs must
be a session that can see both halves, and must re-check the anchors, the absent run root and
refusal sink, the unchanged blobs and the absence of a project-naming concurrent writer immediately
before the command.

### 6. Cross-review

I read Codex's `HumanReport99.md` in full and checked its load-bearing claims against my own
measurements rather than accepting them: the two approved blobs, the plan digest and byte count, the
preservation set, the leaf delta, and the absent execution root. Its account is accurate. Its
description of the delta ("+ 4 namespace/artifact paths + run_label + `capacity_sweep.py` identity")
matches my independent enumeration exactly. I have no correction to carry forward.

## Challenges, and how they were handled

### A sixteen-minute forward skew in my own transcript header — the session's real mistake

My authorization-half turn carries the header time `00:34 PDT`. It was written to the file at
`00:17:45 PDT`. My correction turn two lines later carries `00:23 PDT` against a write at about
`00:21:15` — smaller, same direction, same cause. I stamped each header while **drafting** the
message and never re-read the clock at the moment of the **append**, and for a long message those
are minutes apart.

This is the same shape as three defects already in this project's ledger — a field name remembered
rather than read, a rollout count carried forward rather than recounted, a digest domain assumed
rather than measured. A figure that comes from an instrument has to be taken from the instrument at
the moment it is used, and a header time is an instrument reading about when the file changed.

It matters because `AgentPrompt.md` says the timestamp is what lets you audit the order in which
session work was created, and a *forward* skew is the harmful direction: reconciled against file
modification times, a message appears to postdate its own write, and a sixteen-minute error is large
enough to invert an apparent order between two agents working the same day. The physical order in
the file was never wrong, which is precisely why the existing physical-tail check could not see this.

Both skewed headers stand exactly as posted; the correction is appended forward of them, per the
append-only rule. **The fix is a gate, not a promise**: my append writer now parses the timestamp out
of the header and compares it to the clock **inside the writer, at the write**, refusing the append
if the two differ by more than two minutes in either direction. The monitoring entry was itself
written through the gated writer, so its header is measured rather than recalled. Logged in
`chats/Claude-Codex-Human/Transcript Order Monitoring/`.

### Two probe errors, both of the same family, both caught by the probe failing rather than passing

Besides the digest-domain failure above, my part-B script called `capacity_point_directory` with a
guessed two-argument signature; the function takes one argument and returns a bare directory
component. I read the function at source and corrected the call. Both errors are the reason I keep
building probes that *fail loudly* on a wrong assumption rather than scripts that quietly compute
something plausible.

### The determinism sub-probe ran the module the wrong way

My first attempt at the fourth-destination reproduction invoked the executable by file path from the
project root, which breaks its package imports. The project's established invocation is
`-B -m utils.capacity_sweep` from the packet's `scripts/` directory. Corrected and re-run; the
reproduction is byte-identical.

## Important decisions

1. **Approve the plan on the measurement, not on the matching fingerprint.** A pre-registered digest
   matching is strong evidence the artifact is the predicted one, and no evidence at all that the
   prediction was right. Running all three audit parts anyway is what makes the approval mean
   something.
2. **Treat the plan-history location as a question to measure, not a style choice to wave through.**
   Three foreign locations, a different filename, and a replica of the base directory driven through
   the real claim function — because "the path obviously can't matter" is exactly the kind of
   obvious thing this project has been wrong about before.
3. **Record the run-label namespace reservation as a scope note, not a finding.** It fails into a
   refusal that the design already relies on, so demanding a change would be ceremony. Naming the
   convention that keeps it at one name is the proportionate response.
4. **Issue the authorization half in a separate turn, and refuse to be the runner.** One half is not
   an authorization. Being explicit that this session does not run anything is what keeps a later
   session from reading a single half broadly.
5. **Fix the timestamp failure at the instrument.** Reporting it and resolving to be careful would
   have been worth nothing; a writer that refuses the append is worth something.

## Files created or updated

- `chats/Claude-Codex/Phase 2 Integration and Config Freeze/Phase 2 Integration and Config Freeze - Active.md`
  — three append-only turns (`+232 / −0`): the gate-2 audit and approval, the Step-4 authorization
  half, and the timestamp correction.
- `chats/Claude-Codex-Human/Transcript Order Monitoring/Transcript Order Monitoring - Active.md`
  — one append-only monitoring entry (`+40 / −0`).
- `README.md` (Live-Run README) — one new dated log entry and the banner date advanced to
  2026-08-09 (`+3 / −1`).
- `agents/Claude/README.md` — workspace index updated for this session's Live-Run README action.
- `agents/Claude/Session Summaries/HumanReport100.md` — this report.
- `agents/Claude/Summary of Only Necessary Context.md` — completely rewritten.

**No source file, test file, protocol document, plan artifact, consumed plan, failed-run evidence,
checkpoint, configuration or data file was modified.** The working tree was clean before the
closeout edits and every audit write went to a temporary directory outside the repository.

## Verification

```text
part A, independent of the module                106 passed, 0 failed
part B, the module's own gates in call order      25 passed, 0 failed
part C, the run-label namespace replica            5 passed, 0 failed
full Reproducibility Packet suite               1,768 passed
compileall                                        clean
git diff --check                                  clean
working tree                                      clean before closeout
transcript appends                                prefix intact, header unique, physically last
```

## Next steps

1. **Codex issues its half of the Step-4 authorization** naming plan digest `ffb00965…b7cb31`, run
   label `stage1-run-2`, the base directory, the executable blob and the forty-two-fit ceiling. Both
   old halves are spent and neither carries.
2. **Only then may one `--mode execute` invocation run**, claiming
   `results/capacity_sweep/stage1-run-2/`. C9 must re-establish itself inside that run — it is not
   inherited from the failed one, because the module's bytes moved.
3. **The resulting artifact is evidence, not a result**, until both agents review the exact state.
   Only after that does the pre-registered interpretation step, and then the read-only analysis
   script, become available.
4. Capacity selection, any pilot / validation / test read, the final configuration freeze,
   generation, rollouts and every confirmatory use remain blocked.

**Next Claude session number:** 101.
